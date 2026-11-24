"""
Chat service for AI-powered paper analysis
"""

import os
import json
import faiss
import asyncio
import sys
from typing import List, Dict, Any, Optional, AsyncGenerator, Callable, Awaitable
import logging

from app.models.schemas import ChatResponse
from app.core.config import Settings

# Import original functions
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'backend'))

from features.embedding_and_indexing import search_faiss
from utils.result_processor import get_context_from_result

logger = logging.getLogger("research_rover")


class GeminiDailyQuotaExhaustedError(RuntimeError):
    """Raised when Google Gemini daily request quota is exhausted (non-retryable in short intervals)."""
    pass


def is_daily_quota_error(exc: Exception) -> bool:
    """
    Determine if an exception represents daily request quota exhaustion
    (e.g. Free Tier requests per day cap) as opposed to temporary/per-minute rate limits.
    Inspects structured Google API error metadata, violations, and error strings.
    """
    if isinstance(exc, GeminiDailyQuotaExhaustedError):
        return True

    daily_indicators = [
        "generaterequestsperday",
        "requests per day",
        "generaterequestsperdaypermodel-freetier",
        "generaterequestsperdayperprojectpermodel-freetier",
        "generate_content_free_tier_requests",
        "per day limit exceeded",
        "daily limit",
        "daily quota",
        "free tier requests",
    ]

    # 1. String inspection
    err_str = str(exc).lower()
    if any(ind in err_str for ind in daily_indicators):
        return True

    # 2. Inspect structured Google API exception attributes (metadata, details, violations, errors)
    for attr in ("metadata", "trailing_metadata", "details", "errors", "violations"):
        val = getattr(exc, attr, None)
        if callable(val):
            try:
                val = val()
            except Exception:
                val = None
        if val:
            val_str = str(val).lower()
            if any(ind in val_str for ind in daily_indicators):
                return True

    # 3. Inspect args for structured dicts or protobuf objects
    if hasattr(exc, "args"):
        for arg in exc.args:
            arg_str = str(arg).lower()
            if any(ind in arg_str for ind in daily_indicators):
                return True

    return False


class ChatService:
    """Service for handling AI chat with research papers"""
    
    def __init__(self, settings: Settings, sentence_model, llm):
        self.settings = settings
        self.sentence_model = sentence_model
        self.llm = llm
    
    async def generate_response(
        self,
        filename: Optional[str],
        query: str,
        history: Optional[List[Any]] = None
    ) -> ChatResponse:
        """
        Generate AI response based on paper context or general knowledge if embeddings don't exist
        """
        try:
            # Handle query with no selected dataset
            if not filename or not filename.strip():
                logger.info("No research collection specified. Providing general AI response.")
                response_text = await self._generate_general_response(query, history=history)
                disclaimer = (
                    "[Notice: No dataset selected. The following response is based on general AI knowledge. "
                    "Select an indexed research dataset to receive document-grounded answers with citations.]\n\n"
                )
                return ChatResponse(
                    response=disclaimer + response_text,
                    sources=[],
                    query=query
                )

            # Get file paths
            base_filename = filename.replace(".csv", "")
            faiss_index_path = os.path.join(
                self.settings.DATA_FOLDER, 
                f"{base_filename}_paper_chunks_hdbscan.index"
            )
            metadata_path = os.path.join(
                self.settings.DATA_FOLDER, 
                f"{base_filename}_paper_chunk_metadata_hdbscan.json"
            )
            
            # Check if embedding files exist and are ready (non-empty)
            if (
                not os.path.exists(faiss_index_path) 
                or not os.path.exists(metadata_path)
                or os.path.getsize(faiss_index_path) == 0
                or os.path.getsize(metadata_path) == 0
            ):
                logger.info(f"Embeddings not found or incomplete for {filename}. Providing general response with explicit notice.")
                # Generate response without paper context
                response_text = await self._generate_general_response(query, history=history)
                disclaimer = (
                    f"[Notice: Semantic search index has not been generated for '{filename}' yet. "
                    "The following response is based on general AI knowledge and does not cite papers from this collection. "
                    "Please generate embeddings for this collection to enable document-grounded answers.]\n\n"
                )
                return ChatResponse(
                    response=disclaimer + response_text,
                    sources=[],
                    query=query
                )
            
            # Load FAISS index and metadata safely
            try:
                faiss_index = faiss.read_index(faiss_index_path)
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    all_chunk_metadata = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load FAISS index or metadata for {filename}: {e}")
                # Fall back gracefully to general AI response when index is corrupted or unreadable
                response_text = await self._generate_general_response(query, history=history)
                disclaimer = (
                    f"[Notice: The search index for '{filename}' appears corrupted or unreadable. "
                    "The following response is based on general AI knowledge. "
                    "Please click 'Recreate embeddings' above to rebuild the index.]\n\n"
                )
                return ChatResponse(
                    response=disclaimer + response_text,
                    sources=[],
                    query=query
                )
            
            # Decompose query into sub-queries, passing conversation history for contextual resolution
            sub_queries = await self._decompose_query(query, history=history)
            
            # Search for each sub_query (matching original backend logic)
            all_results_raw = []
            search_k_per_query = 5  # How many results to fetch per sub-query
            
            for sub_q in sub_queries:
                try:
                    # Call search function (matching original backend)
                    loop = asyncio.get_running_loop()
                    results = await loop.run_in_executor(
                        None,
                        search_faiss,
                        sub_q,
                        self.sentence_model,
                        faiss_index,
                        all_chunk_metadata,
                        search_k_per_query
                    )
                    if results:
                        all_results_raw.extend(results)
                        logger.info(f"Retrieved {len(results)} results for sub-query: '{sub_q}'")
                except Exception as e:
                    logger.error(f"Error searching for sub-query '{sub_q}': {e}")
            
            # Deduplicate results (matching original backend logic)
            unique_results_map = {}
            for result in all_results_raw:
                # Determine a unique key for the chunk
                chunk_key = result.get('chunk_id')
                # Fallback using DOI and text hash (more robust than text alone)
                if chunk_key is None:
                    text_hash = hash(result.get('text', ''))
                    doi = result.get('doi', 'Unknown DOI')
                    chunk_key = (doi, text_hash)  # Tuple as key
                
                if chunk_key not in unique_results_map:
                    unique_results_map[chunk_key] = result
                else:
                    # Keep the result with the smaller distance (higher relevance)
                    if result.get('distance', float('inf')) < unique_results_map[chunk_key].get('distance', float('inf')):
                        unique_results_map[chunk_key] = result
            
            search_results = list(unique_results_map.values())
            # Sort final unique results by distance for consistent context ordering
            search_results.sort(key=lambda x: x.get('distance', float('inf')))
            logger.info(f"Total unique results after deduplication: {len(search_results)}")
            
            if not search_results:
                logger.info(f"No relevant documents found for query: '{query}' in {filename}")
                return ChatResponse(
                    response=(
                        f"I couldn't find relevant sections in the indexed papers for: \"{query}\".\n\n"
                        "Try rephrasing your question with different keywords, asking about specific methodologies or concepts, "
                        "or exploring the topics covered in this collection."
                    ),
                    sources=[],
                    query=query
                )
            
            if search_results:
                logger.info(f"Search results found: {len(search_results)}")
                # Process Search Results and Prepare Context (matching original backend)
                llm_context_string, final_paper_titles, final_download_urls = get_context_from_result(search_results, filename)
                
                # Generate AI response using original backend prompt enriched with recent conversation history
                response_text = await self._generate_ai_response_original(query, llm_context_string, history=history)
                
                # Return response with rich citation previews containing actual chunk excerpts
                return ChatResponse(
                    response=response_text,
                    sources=self._create_sources_from_results(search_results, final_paper_titles, final_download_urls),
                    query=query
                )
            
        except Exception as e:
            logger.error(f"Error generating chat response: {e}")
            return ChatResponse(
                response=f"I encountered an error while analyzing the papers: {str(e)}. Please check your dataset and query, and try again.",
                sources=[],
                query=query
            )
    
    async def _call_gemini_with_retry(self, prompt: str, max_retries: int = 2) -> str:
        """
        Execute Gemini content generation with bounded retries and exponential backoff.
        Handles rate limits (429), server overloads (503), timeouts, and empty responses.
        Fails fast on authentication/permission errors.
        """
        loop = asyncio.get_running_loop()
        last_exception = None

        for attempt in range(max_retries + 1):
            try:
                response = await loop.run_in_executor(
                    None,
                    lambda: self.llm.generate_content(prompt)
                )

                # Extract response text safely
                response_text = ""
                if hasattr(response, 'text'):
                    try:
                        response_text = response.text or ""
                    except Exception as text_err:
                        logger.warning(f"Failed to access response.text directly: {text_err}")
                        response_text = ""

                if not response_text and hasattr(response, 'parts') and response.parts:
                    response_text = "".join(part.text for part in response.parts if hasattr(part, 'text'))

                if not response_text and hasattr(response, 'candidates') and response.candidates:
                    first_cand = response.candidates[0]
                    finish_reason = getattr(first_cand, 'finish_reason', None)
                    if finish_reason in (2, 'SAFETY'):
                        logger.warning("Gemini generation candidate flagged by safety filter.")
                        return "The response was blocked by safety filters. Please try rephrasing your research query."
                    if hasattr(first_cand, 'content') and hasattr(first_cand.content, 'parts'):
                        response_text = "".join(
                            p.text for p in first_cand.content.parts if hasattr(p, 'text')
                        )

                response_text = response_text.strip()
                if response_text:
                    return response_text

                logger.warning(f"Gemini returned an empty response (attempt {attempt + 1}/{max_retries + 1})")
                if attempt < max_retries:
                    await asyncio.sleep(1.0 * (attempt + 1))
                    continue
                else:
                    return "The AI model returned an empty response. Please try rephrasing your question."

            except Exception as e:
                last_exception = e
                err_str = str(e).lower()

                # Fail fast on authentication, permission, or invalid API key
                is_auth_error = any(kw in err_str for kw in [
                    "api_key_invalid", "api key not valid", "invalid api key",
                    "permission_denied", "permission denied", "forbidden", "403"
                ])
                if is_auth_error:
                    logger.error(f"Gemini API authentication failed: {e}")
                    raise RuntimeError("Gemini API authentication failed. Please verify that your GEMINI_API_KEY in backend/.env is valid.")

                # Fail fast immediately on daily request quota exhaustion (no sleep, no retries)
                if is_daily_quota_error(e):
                    logger.error(f"Gemini daily request quota exhausted: {e}")
                    raise GeminiDailyQuotaExhaustedError(
                        "The Gemini AI daily request quota was reached. Please wait for the daily quota to reset or upgrade your plan."
                    )

                # Check if error is transient (rate limit, service overload, network timeout)
                is_transient = any(kw in err_str for kw in [
                    "429", "resource_exhausted", "resourceexhausted", "quota",
                    "rate limit", "503", "service unavailable", "unavailable",
                    "timeout", "deadline", "connection", "try again"
                ])

                if is_transient and attempt < max_retries:
                    backoff = 1.5 * (attempt + 1)
                    logger.warning(
                        f"Transient Gemini error on attempt {attempt + 1}/{max_retries + 1}: {e}. "
                        f"Retrying in {backoff:.1f}s..."
                    )
                    await asyncio.sleep(backoff)
                    continue

                logger.error(f"Gemini generation error on attempt {attempt + 1}: {e}")
                if attempt >= max_retries:
                    break

        if last_exception:
            err_lower = str(last_exception).lower()
            if "429" in err_lower or "resource_exhausted" in err_lower or "quota" in err_lower:
                return "The Gemini AI rate limit was reached. Please wait a few seconds before trying again."
            if "503" in err_lower or "unavailable" in err_lower:
                return "The Gemini AI service is currently unavailable or overloaded. Please try again in a few moments."
            return f"AI generation temporarily failed ({str(last_exception)}). Please try again."

        return "I apologize, but I could not generate a response at this time. Please try again."

    async def _decompose_query(self, query: str, history: Optional[List[Any]] = None) -> List[str]:
        """
        Decompose complex or follow-up queries into self-contained search questions.
        If conversation history is provided, contextual references (pronouns, 'the second paper', etc.)
        are resolved.
        """
        try:
            history_context = ""
            if history:
                formatted_history = []
                for msg in history[-6:]:
                    role = "User" if (getattr(msg, "role", "") == "user" or (isinstance(msg, dict) and msg.get("role") == "user")) else "Assistant"
                    content = getattr(msg, "content", "") if not isinstance(msg, dict) else msg.get("content", "")
                    if content:
                        # Truncate each historical turn for decomposition prompt efficiency
                        formatted_history.append(f"{role}: {content[:300]}")
                if formatted_history:
                    history_context = "Recent Conversation History:\n" + "\n".join(formatted_history) + "\n\n"

            decomposition_prompt = f"""{history_context}Current User Query: '{query}'

Task: Break down the current query into 1 to 3 distinct, self-contained search questions or search terms for retrieving relevant research paper chunks from a vector database.
Guidelines:
- If the current query is a contextual follow-up or contains pronouns/references to the conversation history (e.g. "what methodology did it use?", "compare the first two papers", "tell me more about that"), resolve the references using the conversation history so every search query is complete, specific, and self-contained.
- If the query is already focused and self-contained, just return the query on a single line.
- List each distinct question/term on a new line without numbering or bullets.

Example 1:
Current User Query: What is machine learning, why is it important in healthcare and what are its setbacks?
Output:
What is machine learning?
Why is machine learning important in healthcare?
What are the setbacks and limitations of machine learning in healthcare?

Example 2:
Recent Conversation History:
User: Which papers discuss CNN architectures in medicine?
Assistant: Paper [1] 'Deep Learning for Medical Imaging' discusses CNN architectures.
Current User Query: What dataset did they evaluate it on?
Output:
What dataset was used to evaluate Deep Learning for Medical Imaging?
Evaluation datasets for medical CNN architectures

Current User Query: {query}
Output:"""
            
            logger.info(f"Decomposing query: {query}")
            
            try:
                response_text = await self._call_gemini_with_retry(decomposition_prompt, max_retries=1)
                sub_queries = []
                
                # Check if Gemini returned an error or fallback message instead of sub-queries
                is_error_text = False
                if response_text:
                    resp_lower = response_text.lower()
                    error_markers = [
                        "rate limit", "quota", "unavailable", "temporarily failed",
                        "i apologize", "safety filter", "generation error", "llm generation failed",
                        "empty response"
                    ]
                    if any(marker in resp_lower for marker in error_markers):
                        is_error_text = True
                        logger.warning(
                            f"Query decomposition returned error text ('{response_text[:60]}...'). "
                            "Falling back to original user query without retrying Gemini."
                        )

                if response_text and not is_error_text:
                    sub_queries = [q.strip() for q in response_text.split('\n') if q.strip()]
                
                if not sub_queries:  # Fallback if decomposition fails, returns empty, or returned error text
                    logger.warning("Query decomposition returned empty or error, using original query.")
                    sub_queries = [query]
                else:
                    # Limit the number of sub-queries to avoid excessive searching
                    max_sub_queries = 5
                    if len(sub_queries) > max_sub_queries:
                        logger.warning(f"Too many sub-queries ({len(sub_queries)}), limiting to {max_sub_queries}.")
                        sub_queries = sub_queries[:max_sub_queries]
                    logger.info(f"Decomposed into sub-queries: {sub_queries}")
                
                return sub_queries
                
            except Exception as e:
                logger.warning(f"Error during query decomposition: {e}. Falling back to original query.")
                return [query]  # Fallback
            
        except Exception as e:
            logger.warning(f"Query decomposition failed: {e}")
            return [query]
    
    async def _generate_ai_response_original(
        self,
        query: str,
        llm_context_string: str,
        history: Optional[List[Any]] = None
    ) -> str:
        """
        Generate AI response using the original backend's prompt and logic, enriched with conversation history
        """
        try:
            history_section = ""
            if history:
                formatted_history = []
                for msg in history[-6:]:
                    role = "User" if (getattr(msg, "role", "") == "user" or (isinstance(msg, dict) and msg.get("role") == "user")) else "Assistant"
                    content = getattr(msg, "content", "") if not isinstance(msg, dict) else msg.get("content", "")
                    if content:
                        formatted_history.append(f"{role}: {content}")
                if formatted_history:
                    history_section = "\nRecent Conversation History:\n" + "\n".join(formatted_history) + "\n"

            llm_prompt = f"""
Your task is to answer the following question based ONLY on the context documents provided below, while maintaining awareness of recent conversation context when answering follow-up queries.

Instructions:
- Answer the question solely using the information present in the 'Context Documents' section.
- Do not use any external knowledge or prior assumptions.
- Use 'Recent Conversation History' to understand context and follow-up references, but answer strictly using facts present in the 'Context Documents'.

- **Identify Intent for Paper Lists**:
    - If the user's query explicitly asks for a list of papers that discuss a specific topic, methodology, or concept (e.g., "Which papers discuss agile methodology?", "List papers on software testing frameworks", "What are the papers related to blockchain in IoT?"), your primary goal is to identify and list the **titles** of those relevant papers found within the 'Context Documents'.
    - In such cases, provide a concise list of paper titles. If no relevant papers are found in the context, clearly state that.

- **Paraphrase and Synthesize:**
    - **Do NOT copy sentences directly** from the context documents.
    - Rephrase the information accurately in your own words, preserving the original meaning.
    - Synthesize information from multiple sources where appropriate to provide a cohesive answer.

- **Citation Requirements:**
    - You MUST cite the source(s) for every piece of information presented in your answer.
    - Use the index number provided in brackets (e.g., [1], [2]) corresponding to the source document listed in the 'Context Documents' (e.g., `[1] [Source Title: ...]`).
    - **Place the citation(s) ONLY at the end of the sentence, or at the end of a sequence of sentences, that are directly supported by that source(s).**
    - **Citation Placement Example:** If sentence A and sentence B are both based *only* on source [1], and sentence C is based *only* on source [4], the correct format is: "Sentence A. Sentence B.[1] Sentence C.[4]".
    - **Multiple Sources Example:** If a statement synthesizes information from sources [1] and [3], cite it as: "Synthesized statement.[1][3]".

- **Clarity:** Define pronouns clearly (e.g., avoid ambiguous "it" or "they"). Refer back to specific entities mentioned in the context.

- **Structure for Multi-Part Questions:**
    - **Identify Sub-Questions:** Analyze the main question to see if it contains multiple distinct parts or sub-questions (e.g., asking "what" and "how", or asking about multiple different items).
    - **Address Sequentially:** If sub-questions are identified, structure your answer to address each one separately and in the order they appear in the question.
    - **Use Paragraphs:** **Use distinct paragraphs for the answer to each sub-question.** This separation is crucial for clarity.
    - **Example:** For a query like "What is machine learning and how does it affect the healthcare industry?", first provide a paragraph explaining machine learning (citing relevant sources), and then provide a *separate, second* paragraph explaining its effects on healthcare (citing relevant sources).

- **Completeness:** Ensure all identified parts (sub-questions) of the question are addressed if possible within the context. If a part cannot be answered from the context, state so clearly for that specific part before moving to the next, or at the end if it's the last part.

- **Unknown Answer:** If the *entire* answer (or a specific sub-part) cannot be found within the provided context documents, explicitly state: "I cannot answer [the question / this part of the question] based on the provided context."

- **Conciseness:** Be direct and avoid unnecessary waffle within each section.


Context Documents:
{llm_context_string}
{history_section}
Question:
{query}

Answer (Paraphrased text based *only* on the context above. **Address sub-questions in separate paragraphs.** Citations MUST be placed at the end of the sentence or group of sentences they support, like sentence1. sentence2.[1] sentence3.[4]):
"""
            
            logger.info("Sending prompt to LLM with retry.")
            response_text = await self._call_gemini_with_retry(llm_prompt, max_retries=2)
            logger.info("LLM response received.")
            return response_text.strip()
            
        except Exception as e:
            logger.error(f"Error calling LLM: {e}")
            return f"LLM generation failed: {e}"
    
    async def _generate_general_response(self, query: str, history: Optional[List[Any]] = None) -> str:
        """
        Generate general AI response when no paper context is available, with history awareness
        """
        try:
            history_section = ""
            if history:
                formatted_history = []
                for msg in history[-6:]:
                    role = "User" if (getattr(msg, "role", "") == "user" or (isinstance(msg, dict) and msg.get("role") == "user")) else "Assistant"
                    content = getattr(msg, "content", "") if not isinstance(msg, dict) else msg.get("content", "")
                    if content:
                        formatted_history.append(f"{role}: {content}")
                if formatted_history:
                    history_section = "Recent Conversation History:\n" + "\n".join(formatted_history) + "\n\n"

            prompt = f"""{history_section}The user is asking a research question, but no paper embeddings are available for the selected dataset. Please provide a helpful, informative response based on your general knowledge.

User Question: {query}

Please provide a comprehensive and accurate answer. Mention that more detailed, document-grounded answers with citations could be available once research papers are indexed and embeddings are created."""
            
            logger.info("Sending general knowledge prompt to LLM with retry.")
            response_text = await self._call_gemini_with_retry(prompt, max_retries=2)
            return response_text.strip()
                
        except Exception as e:
            logger.error(f"Error generating general response: {e}")
            return "I encountered an error while processing your question. Please try again later."

    def _build_context_prompt(
        self,
        query: str,
        llm_context_string: str,
        history: Optional[List[Any]] = None
    ) -> str:
        """Construct the prompt for document-grounded paper QA with history"""
        history_section = ""
        if history:
            formatted_history = []
            for msg in history[-6:]:
                role = "User" if (getattr(msg, "role", "") == "user" or (isinstance(msg, dict) and msg.get("role") == "user")) else "Assistant"
                content = getattr(msg, "content", "") if not isinstance(msg, dict) else msg.get("content", "")
                if content:
                    formatted_history.append(f"{role}: {content}")
            if formatted_history:
                history_section = "\nRecent Conversation History:\n" + "\n".join(formatted_history) + "\n"

        return f"""
Your task is to answer the following question based ONLY on the context documents provided below, while maintaining awareness of recent conversation context when answering follow-up queries.

Instructions:
- Answer the question solely using the information present in the 'Context Documents' section.
- Do not use any external knowledge or prior assumptions.
- Use 'Recent Conversation History' to understand context and follow-up references, but answer strictly using facts present in the 'Context Documents'.

- **Identify Intent for Paper Lists**:
    - If the user's query explicitly asks for a list of papers that discuss a specific topic, methodology, or concept (e.g., "Which papers discuss agile methodology?", "List papers on software testing frameworks", "What are the papers related to blockchain in IoT?"), your primary goal is to identify and list the **titles** of those relevant papers found within the 'Context Documents'.
    - In such cases, provide a concise list of paper titles. If no relevant papers are found in the context, clearly state that.

- **Paraphrase and Synthesize:**
    - **Do NOT copy sentences directly** from the context documents.
    - Rephrase the information accurately in your own words, preserving the original meaning.
    - Synthesize information from multiple sources where appropriate to provide a cohesive answer.

- **Citation Requirements:**
    - You MUST cite the source(s) for every piece of information presented in your answer.
    - Use the index number provided in brackets (e.g., [1], [2]) corresponding to the source document listed in the 'Context Documents' (e.g., `[1] [Source Title: ...]`).
    - **Place the citation(s) ONLY at the end of the sentence, or at the end of a sequence of sentences, that are directly supported by that source(s).**
    - **Citation Placement Example:** If sentence A and sentence B are both based *only* on source [1], and sentence C is based *only* on source [4], the correct format is: "Sentence A. Sentence B.[1] Sentence C.[4]".
    - **Multiple Sources Example:** If a statement synthesizes information from sources [1] and [3], cite it as: "Synthesized statement.[1][3]".

- **Clarity:** Define pronouns clearly (e.g., avoid ambiguous "it" or "they"). Refer back to specific entities mentioned in the context.

- **Structure for Multi-Part Questions:**
    - **Identify Sub-Questions:** Analyze the main question to see if it contains multiple distinct parts or sub-questions (e.g., asking "what" and "how", or asking about multiple different items).
    - **Address Sequentially:** If sub-questions are identified, structure your answer to address each one separately and in the order they appear in the question.
    - **Use Paragraphs:** **Use distinct paragraphs for the answer to each sub-question.** This separation is crucial for clarity.
    - **Example:** For a query like "What is machine learning and how does it affect the healthcare industry?", first provide a paragraph explaining machine learning (citing relevant sources), and then provide a *separate, second* paragraph explaining its effects on healthcare (citing relevant sources).

- **Completeness:** Ensure all identified parts (sub-questions) of the question are addressed if possible within the context. If a part cannot be answered from the context, state so clearly for that specific part before moving to the next, or at the end if it's the last part.

- **Unknown Answer:** If the *entire* answer (or a specific sub-part) cannot be found within the provided context documents, explicitly state: "I cannot answer [the question / this part of the question] based on the provided context."

- **Conciseness:** Be direct and avoid unnecessary waffle within each section.


Context Documents:
{llm_context_string}
{history_section}
Question:
{query}

Answer (Paraphrased text based *only* on the context above. **Address sub-questions in separate paragraphs.** Citations MUST be placed at the end of the sentence or group of sentences they support, like sentence1. sentence2.[1] sentence3.[4]):
"""

    def _build_general_prompt(
        self,
        query: str,
        history: Optional[List[Any]] = None
    ) -> str:
        """Construct the prompt for general AI knowledge responses with history"""
        history_section = ""
        if history:
            formatted_history = []
            for msg in history[-6:]:
                role = "User" if (getattr(msg, "role", "") == "user" or (isinstance(msg, dict) and msg.get("role") == "user")) else "Assistant"
                content = getattr(msg, "content", "") if not isinstance(msg, dict) else msg.get("content", "")
                if content:
                    formatted_history.append(f"{role}: {content}")
            if formatted_history:
                history_section = "Recent Conversation History:\n" + "\n".join(formatted_history) + "\n\n"

        return f"""{history_section}The user is asking a research question, but no paper embeddings are available for the selected dataset. Please provide a helpful, informative response based on your general knowledge.

User Question: {query}

Please provide a comprehensive and accurate answer. Mention that more detailed, document-grounded answers with citations could be available once research papers are indexed and embeddings are created."""

    @staticmethod
    def _extract_chunk_text(chunk: Any) -> str:
        """Extract text content safely from a Gemini response chunk"""
        if hasattr(chunk, 'text'):
            try:
                return chunk.text or ""
            except Exception:
                pass
        if hasattr(chunk, 'parts') and chunk.parts:
            return "".join(p.text for p in chunk.parts if hasattr(p, 'text'))
        if hasattr(chunk, 'candidates') and chunk.candidates:
            cand = chunk.candidates[0]
            if hasattr(cand, 'content') and hasattr(cand.content, 'parts'):
                return "".join(p.text for p in cand.content.parts if hasattr(p, 'text'))
        return ""

    async def _stream_gemini_with_retry(
        self,
        prompt: str,
        max_retries: int = 2,
        is_cancelled_check: Optional[Callable[[], Awaitable[bool]]] = None
    ) -> AsyncGenerator[str, None]:
        """
        Execute Gemini async streaming with safe retry handling.
        Retries are allowed before any text is emitted; once text is yielded,
        retrying is disallowed to avoid duplicate responses.
        """
        has_emitted_text = False
        attempt = 0

        while attempt <= max_retries:
            if is_cancelled_check and await is_cancelled_check():
                raise asyncio.CancelledError("Client disconnected")

            if attempt > 0:
                if has_emitted_text:
                    logger.warning("Error occurred after tokens were emitted. Halting stream without restarting.")
                    break
                backoff = 1.5 * attempt
                logger.info(f"Retrying Gemini stream (attempt {attempt + 1}/{max_retries + 1}) after {backoff:.1f}s...")
                await asyncio.sleep(backoff)

            try:
                # Invoke native async streaming
                if hasattr(self.llm, "generate_content_async"):
                    response_stream = await self.llm.generate_content_async(prompt, stream=True)
                else:
                    # Fallback for sync LLM instances
                    loop = asyncio.get_running_loop()
                    response_stream = await loop.run_in_executor(
                        None, lambda: self.llm.generate_content(prompt, stream=True)
                    )

                # Iterate through chunks
                if hasattr(response_stream, "__aiter__"):
                    async for chunk in response_stream:
                        if is_cancelled_check and await is_cancelled_check():
                            raise asyncio.CancelledError("Client disconnected")
                        chunk_text = self._extract_chunk_text(chunk)
                        if chunk_text:
                            has_emitted_text = True
                            yield chunk_text
                else:
                    # Sync iterator wrapped
                    for chunk in response_stream:
                        if is_cancelled_check and await is_cancelled_check():
                            raise asyncio.CancelledError("Client disconnected")
                        chunk_text = self._extract_chunk_text(chunk)
                        if chunk_text:
                            has_emitted_text = True
                            yield chunk_text

                if not has_emitted_text:
                    logger.warning(f"Gemini stream yielded no text (attempt {attempt + 1}/{max_retries + 1})")
                    if attempt < max_retries:
                        attempt += 1
                        continue
                    else:
                        raise RuntimeError("The AI model returned an empty response. Please try rephrasing your question.")

                # Stream completed successfully
                return

            except asyncio.CancelledError:
                raise
            except Exception as e:
                err_str = str(e).lower()
                is_auth_error = any(kw in err_str for kw in [
                    "api_key_invalid", "api key not valid", "invalid api key",
                    "permission_denied", "permission denied", "forbidden", "403"
                ])
                if is_auth_error:
                    logger.error(f"Gemini authentication failed during stream: {e}")
                    raise RuntimeError("Gemini API authentication failed. Please verify your GEMINI_API_KEY in backend/.env.")

                # Fail fast immediately on daily request quota exhaustion (no sleep, no retries)
                if is_daily_quota_error(e):
                    logger.error(f"Gemini daily request quota exhausted during stream: {e}")
                    raise GeminiDailyQuotaExhaustedError(
                        "The Gemini AI daily request quota was reached. Please wait for the daily quota to reset or upgrade your plan."
                    )

                is_transient = any(kw in err_str for kw in [
                    "429", "resource_exhausted", "quota", "rate limit",
                    "503", "service unavailable", "unavailable", "timeout", "deadline", "connection"
                ])

                if is_transient and not has_emitted_text and attempt < max_retries:
                    attempt += 1
                    continue

                logger.error(f"Error during Gemini streaming: {e}")
                raise e

    async def generate_response_stream(
        self,
        filename: Optional[str],
        query: str,
        history: Optional[List[Any]] = None,
        is_client_disconnected: Optional[Callable[[], Awaitable[bool]]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream response tokens and citation metadata using SSE events.
        Yields dictionaries with format: {"event": "<name>", "data": {...}}
        """
        if is_client_disconnected and await is_client_disconnected():
            raise asyncio.CancelledError("Client disconnected")

        # Case 1: No dataset selected (General Chat)
        if not filename or not filename.strip():
            logger.info("Streaming response for General Chat (no dataset selected)")
            yield {
                "event": "status",
                "data": {"stage": "retrieving", "message": "General AI knowledge mode (no collection selected)..."}
            }
            yield {
                "event": "citations",
                "data": {"sources": []}
            }
            disclaimer = (
                "[Notice: No dataset selected. The following response is based on general AI knowledge. "
                "Select an indexed research dataset to receive document-grounded answers with citations.]\n\n"
            )
            yield {
                "event": "delta",
                "data": {"text": disclaimer}
            }
            yield {
                "event": "status",
                "data": {"stage": "generating", "message": "Generating response..."}
            }
            prompt = self._build_general_prompt(query, history=history)
            async for token in self._stream_gemini_with_retry(prompt, is_cancelled_check=is_client_disconnected):
                yield {"event": "delta", "data": {"text": token}}
            return

        # Case 2: Check embedding files readiness
        base_filename = filename.replace(".csv", "")
        faiss_index_path = os.path.join(self.settings.DATA_FOLDER, f"{base_filename}_paper_chunks_hdbscan.index")
        metadata_path = os.path.join(self.settings.DATA_FOLDER, f"{base_filename}_paper_chunk_metadata_hdbscan.json")

        if (
            not os.path.exists(faiss_index_path)
            or not os.path.exists(metadata_path)
            or os.path.getsize(faiss_index_path) == 0
            or os.path.getsize(metadata_path) == 0
        ):
            logger.info(f"Embeddings not ready for {filename}. Streaming general response with notice.")
            yield {
                "event": "status",
                "data": {"stage": "retrieving", "message": "Embeddings not indexed; switching to general knowledge..."}
            }
            yield {
                "event": "citations",
                "data": {"sources": []}
            }
            disclaimer = (
                f"[Notice: Semantic search index has not been generated for '{filename}' yet. "
                "The following response is based on general AI knowledge and does not cite papers from this collection. "
                "Please generate embeddings for this collection to enable document-grounded answers.]\n\n"
            )
            yield {
                "event": "delta",
                "data": {"text": disclaimer}
            }
            yield {
                "event": "status",
                "data": {"stage": "generating", "message": "Generating response..."}
            }
            prompt = self._build_general_prompt(query, history=history)
            async for token in self._stream_gemini_with_retry(prompt, is_cancelled_check=is_client_disconnected):
                yield {"event": "delta", "data": {"text": token}}
            return

        # Case 3: Load FAISS index safely
        try:
            faiss_index = faiss.read_index(faiss_index_path)
            with open(metadata_path, 'r', encoding='utf-8') as f:
                all_chunk_metadata = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load FAISS index or metadata for {filename}: {e}")
            yield {
                "event": "status",
                "data": {"stage": "retrieving", "message": "Index unreadable; generating general response..."}
            }
            yield {
                "event": "citations",
                "data": {"sources": []}
            }
            disclaimer = (
                f"[Notice: The search index for '{filename}' appears corrupted or unreadable. "
                "The following response is based on general AI knowledge. "
                "Please click 'Recreate embeddings' above to rebuild the index.]\n\n"
            )
            yield {"event": "delta", "data": {"text": disclaimer}}
            prompt = self._build_general_prompt(query, history=history)
            async for token in self._stream_gemini_with_retry(prompt, is_cancelled_check=is_client_disconnected):
                yield {"event": "delta", "data": {"text": token}}
            return

        # Case 4: Query decomposition & search
        yield {
            "event": "status",
            "data": {"stage": "searching", "message": "Analyzing question and searching indexed papers..."}
        }
        sub_queries = await self._decompose_query(query, history=history)
        all_results_raw = []
        search_k_per_query = 5

        for sub_q in sub_queries:
            if is_client_disconnected and await is_client_disconnected():
                raise asyncio.CancelledError("Client disconnected")
            try:
                loop = asyncio.get_running_loop()
                results = await loop.run_in_executor(
                    None,
                    search_faiss,
                    sub_q,
                    self.sentence_model,
                    faiss_index,
                    all_chunk_metadata,
                    search_k_per_query
                )
                if results:
                    all_results_raw.extend(results)
            except Exception as e:
                logger.error(f"Error searching sub-query '{sub_q}': {e}")

        # Deduplicate results
        unique_results_map = {}
        for result in all_results_raw:
            chunk_key = result.get('chunk_id')
            if chunk_key is None:
                text_hash = hash(result.get('text', ''))
                doi = result.get('doi', 'Unknown DOI')
                chunk_key = (doi, text_hash)
            if chunk_key not in unique_results_map:
                unique_results_map[chunk_key] = result
            elif result.get('distance', float('inf')) < unique_results_map[chunk_key].get('distance', float('inf')):
                unique_results_map[chunk_key] = result

        search_results = list(unique_results_map.values())
        search_results.sort(key=lambda x: x.get('distance', float('inf')))

        if not search_results:
            yield {
                "event": "citations",
                "data": {"sources": []}
            }
            no_results_text = (
                f"I couldn't find relevant sections in the indexed papers for: \"{query}\".\n\n"
                "Try rephrasing your question with different keywords, asking about specific methodologies or concepts, "
                "or exploring the topics covered in this collection."
            )
            yield {
                "event": "delta",
                "data": {"text": no_results_text}
            }
            return

        llm_context_string, final_paper_titles, final_download_urls = get_context_from_result(search_results, filename)
        sources = self._create_sources_from_results(search_results, final_paper_titles, final_download_urls)

        # Deliver citations before text generation starts
        yield {
            "event": "citations",
            "data": {"sources": sources}
        }
        yield {
            "event": "status",
            "data": {"stage": "generating", "message": "Generating grounded answer from paper context..."}
        }

        # Stream text generation from Gemini
        llm_prompt = self._build_context_prompt(query, llm_context_string, history=history)
        async for token in self._stream_gemini_with_retry(llm_prompt, is_cancelled_check=is_client_disconnected):
            yield {
                "event": "delta",
                "data": {"text": token}
            }

    def _create_sources_from_results(
        self,
        search_results: List[Dict[str, Any]],
        paper_titles: List[str],
        download_urls: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Create source citations from search results with real chunk/abstract excerpts,
        preserving title, URL, DOI, and source metadata.
        """
        sources = []
        try:
            for i, result in enumerate(search_results):
                title = paper_titles[i] if i < len(paper_titles) else (result.get('paperTitle') or result.get('title') or 'Unknown Title')
                url = download_urls[i] if i < len(download_urls) else ''
                doi = str(result.get('doi', '')).strip()
                if doi in ('Unknown DOI', 'nan'):
                    doi = ''
                
                # Extract actual chunk text or abstract
                chunk_text = str(result.get('text', '') or result.get('abstract', '') or '').strip()
                clean_preview = ' '.join(chunk_text.split())
                
                if len(clean_preview) > 280:
                    content_preview = clean_preview[:280] + '...'
                elif clean_preview:
                    content_preview = clean_preview
                else:
                    content_preview = title
                
                source = {
                    "id": i + 1,
                    "type": "research_paper",
                    "title": title,
                    "url": url,
                    "doi": doi,
                    "source": str(result.get('source', '')),
                    "year": int(result.get('yearPublished', 0)) if result.get('yearPublished') else 0,
                    "content_preview": content_preview
                }
                sources.append(source)
        except Exception as e:
            logger.warning(f"Error creating sources from results: {e}")
        return sources

    def _create_sources_from_papers(self, paper_titles: List[str], download_urls: List[str]) -> List[Dict[str, Any]]:
        """
        Create sources from paper titles and URLs (legacy backward-compatible method)
        """
        dummy_results = [{"title": t, "text": t} for t in paper_titles]
        return self._create_sources_from_results(dummy_results, paper_titles, download_urls)
    
    def _extract_sources(self, contexts: List[str]) -> List[Dict[str, Any]]:
        """
        Extract source information from contexts (legacy method)
        """
        sources = []
        
        try:
            for i, context in enumerate(contexts):
                # Simple source extraction - enhance as needed
                source = {
                    "id": i + 1,
                    "type": "research_paper",
                    "content_preview": context[:200] + "..." if len(context) > 200 else context
                }
                sources.append(source)
                
        except Exception as e:
            logger.warning(f"Error extracting sources: {e}")
        
        return sources