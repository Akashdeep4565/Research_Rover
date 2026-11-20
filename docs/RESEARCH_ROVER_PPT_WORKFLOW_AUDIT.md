# Research Rover: PowerPoint Workflow Audit & Verification Report

**Audited File:** `media_1795086816454_604f38b2.pptx`  
**Audit Standard:** ISO/IEC 19505:2012 / Research Rover Production Codebase (v2.0)  
**Evaluator:** Senior Software Architect & Quality Assurance Lead  
**Audit Date:** November 2026  

---

## 1. Overall Verdict: `Wrong` (Functionally Flawed & Architecturally Inaccurate)

> **Verdict Summary:**  
> The presentation outlines the general feature aspirations of Research Rover but is **fundamentally inaccurate and architecturally flawed** in its workflow logic. It misrepresents the data pipeline by placing local FAISS vector indexing inside live PubMed external search (conflating the offline RAG chat indexing with database retrieval), isolates Bibliographic Analysis and AI Chat into disconnected dead-end swimlanes with zero interconnecting data flow, omits the core multi-source OpenAlex integration, and contains zero decision diamonds or error-handling paths.

---

## 2. Task 1: Workflow Presence Check

The presentation was extracted and parsed across all XML layers (shape trees, grouped shapes, connectors, geometry records, and speaker notes).

- **Slide 1:** `ResearchRover User Features` — **Contains a User-Facing Feature Workflow** (portrayed as three vertical disconnected silos).
- **Slide 2:** `ResearchRover Software Pipeline` — **Contains an Architectural Software Pipeline Diagram** (portrayed across three horizontal swimlanes with severe broken links and dead ends).

**Finding:** Workflows are present on **both slides (Slide 1 and Slide 2)**. Neither slide contains speaker notes.

---

## 3. Task 2: Complete Extraction of the PPT Workflows

### 3.1. Slide 1: User-Facing Workflow (`ResearchRover User Features`)

The slide organizes user interactions into three isolated vertical columns under a top badge labeled `ResearchRover Dashboard`:

```
========================================================================================================
                                   SLIDE 1 EXTRACTED FLOW DIAGRAM
========================================================================================================

   [ Research Article Search ]          [ Bibliographic Data Analysis ]         [ AI Interaction Session ]
              │                                      │                                      │
              ▼                                      ▼                                      ▼
   1.1. Input Research Topic            2.1. Upload Bibliographic Data         3.1. Upload Bibliographic Data
              │                              (CSV file)                             (CSV file) / Article PDF
              ▼                                      │                                      │
   1.2. Select Source Database,                      ▼                                      ▼
        Publication Duration,           2.2. Perform Data Analysis:            3.2. Interact with AI Research
        Number of Articles                   - Word Cloud                           Assistant on the Topic
              │                              - Keyword Frequency                            │
              ▼                              - Keyword Co-occurrence                        ▼
   1.3. Download Bibliographic Data          - Collaboration Map                      [ TERMINAL ]
        (CSV file) and Article PDFs                  │
              │                                      ▼
              ▼                              2.3. Download Result
        [ TERMINAL ]                                 │
                                                     ▼
                                               [ TERMINAL ]
========================================================================================================
```

- **Trigger / Start State:** User navigates to the ResearchRover Dashboard.
- **Branching / Decision Points:** **None.** (Linear downward arrows only; zero error checking or validation).
- **End States:** Three separate terminal download/interaction points (`Download Bibliographic Data and Article PDFs`, `Download Result`, and `Interact with AI Research Assistant`).
- **Owner / Tooling:** End-user interacting with web forms and downloading files.

---

### 3.2. Slide 2: Technical Pipeline Workflow (`ResearchRover Software Pipeline`)

The slide attempts to model the software backend across three horizontal swimlanes:

```
========================================================================================================
                                   SLIDE 2 EXTRACTED FLOW DIAGRAM
========================================================================================================

SWIMLANE 1: "Research Article Search"
  [User Interface] (Query seq., duration, max article no.)
        │
        ▼ (Connector 76)
  [Query Preprocess] (Clean, tokenize, MeSH expansion)
        │
        ▼ (Connector 5)
  [Candidate Fetch] (Esearch, Efetch, XML parser) <=========> [Database API] (E-utility)
        │                                                     (Connector 21: bidirectional)
        ▼ (Connectors 69, 64, 19: routed around)
  [Semantic Ranking Sub-Container]
     [Embedding] (Database vectors)
        │
        ▼ (Connector 17)
     [FAISS Indexing] (Top-k similarity)
        │
        ▼ (Connector 58)
     [Ranking] (Filter, dedupe, sort)
        │
        ▼ (Connector 82)
     [Result Store] (Pandas DataFrame of metadata)
        │
        ├──────────────────────────────────────────────────┐
        │ (Connector 103)                                  │ (No explicit connector)
        ▼                                                  ▼
  [CSV Exporter] (Metadata to file)              [Open-access Sources] (Open access PDFs)
                                                           │
                                                           ▼ (Connector 96)
                                                 [PDF Fetcher] (Open access links only)

SWIMLANE 2: "Bibliographic Data Analysis" (ISOLATED DEAD END)
  [Perform Data Analysis] (Word Cloud, Keyword Frequency, Keyword Co-occurrence Network, Collaboration Map)
  * No incoming connector from Swimlane 1.
  * No outgoing connector to user interface or downloads.

SWIMLANE 3: "Interaction with AI Research Assistant" (ISOLATED DEAD END)
  [AI Interaction Session] (Interact with AI Research Assistant on the Topic)
  * No incoming connector from FAISS, Embeddings, or Swimlane 1.
  * No outgoing connector to user interface.
========================================================================================================
```

- **Trigger / Start State:** User Interface query submission (`Query seq., duration, max article no.`).
- **End State:** Top swimlane ends at `CSV Exporter` and `PDF Fetcher`. Swimlanes 2 and 3 have no start triggers or end terminals.
- **Decision Points:** **Zero.**
- **Systems & Tools Mentioned:** E-utilities, Esearch, Efetch, XML parser, FAISS indexing, Pandas DataFrame, Open-access PDF fetcher.

---

## 4. Task 3: Comprehensive Verification (Right vs. Wrong Audit)

Evaluating the slides against the **actual implemented Research Rover codebase** (`backend/app/*` and `frontend/src/*`) reveals critical conceptual, sequence, and architectural errors:

### Critical Discrepancy 1: Severe Misplacement of FAISS & Embeddings (Slide 2)
- **What the PPT claims:** Slide 2 places `Embedding (Database vectors)` $\to$ `FAISS indexing (Top-k similarity)` directly inside the live search candidate retrieval pipeline between `Candidate Fetch` and `Result Store`.
- **The Codebase Reality:**  
  - PubMed contains **over 36 million papers**. A local application **never** downloads database vectors from the NCBI Entrez API to perform local FAISS top-$k$ similarity during live search! NCBI Entrez E-Utilities perform search indexing server-side via inverted indexes.
  - In Research Rover, **FAISS indexing is strictly part of the AI Research Assistant (RAG) pipeline** (`backend/app/services/embedding_service.py` and `backend/app/services/chat_service.py`). FAISS chunks and embeds *only the local retrieved/uploaded paper corpus* (`SentenceTransformer all-MiniLM-L6-v2`) to perform semantic retrieval when the user asks questions in Chat!
  - For candidate search re-ranking, Research Rover uses an optional **MedCPT cross-encoder neural model** (`backend/app/services/reranker_service.py`), NOT FAISS vector indexing.
- **Verdict:** **FACTUALLY WRONG & ARCHITECTURALLY IMPOSSIBLE.**

---

### Critical Discrepancy 2: Total Disconnection of Analysis and AI (Slide 2 Dead Ends)
- **What the PPT claims:** Swimlane 2 (`Bibliographic Data Analysis`) and Swimlane 3 (`Interaction with AI Research Assistant`) float as isolated boxes with zero connectors.
- **The Codebase Reality:**  
  - The pipeline is fully integrated. In `SearchService`, search results are normalized into canonical records and saved to `data/<corpus>.csv`.
  - `AnalysisService` directly consumes this CSV to calculate keyword frequency distributions, AST keyword alias mappings, NetworkX degree centralities, and country collaboration matrices.
  - `ChatService` and `EmbeddingService` directly consume this CSV to build chunk metadata, build the local FAISS index, and power the Google Gemini RAG assistant.
  - Presenting Analysis and AI as disconnected islands breaks the entire software architecture narrative.
- **Verdict:** **BROKEN ARROWS & DEAD ENDS.**

---

### Critical Discrepancy 3: Complete Omission of Unified Search & OpenAlex
- **What the PPT claims:** Slide 1 lists *"Select Source Database"* (singular), and Slide 2 lists only `Database API (E-utility)` with `Esearch` and `Efetch`.
- **The Codebase Reality:**  
  - One of Research Rover's core innovations is **Unified Multi-Source Search** (`backend/app/services/unified_search_service.py`), querying **both NCBI PubMed and the OpenAlex REST API** concurrently.
  - The real pipeline includes **Multi-Source Deduplication & Merging** across 4 priority levels (DOI $\to$ PMID $\to$ OpenAlex ID $\to$ Title+Year+Author composite key) and abstract reconstruction from OpenAlex inverted indexes.
  - Omitting OpenAlex conceals half of the platform's scholarly literature ingestion engine.
- **Verdict:** **INCOMPLETE & FACTUALLY OUTDATED.**

---

### Critical Discrepancy 4: Manual Re-upload Anti-Pattern (Slide 1)
- **What the PPT claims:** Slide 1 mandates that after downloading a CSV from search, the user must manually re-upload the CSV to run analytics, and manually re-upload the CSV/PDF to chat with the AI.
- **The Codebase Reality:**  
  - While Research Rover supports custom CSV uploads via `/api/v1/files/upload`, **the primary application workflow is seamless**. Once a search completes, the active dataset is automatically loaded into the React `SearchContext` and `AnalyticsContext`.
  - The researcher simply clicks the **Analytics** tab (`/analytics`) or **Chat** tab (`/chat`) to instantly explore visualizations and chat without manual download/re-upload friction.
- **Verdict:** **MISLEADING USER WORKFLOW.**

---

### Critical Discrepancy 5: Complete Lack of Decision Points & Resilience
- **What the PPT claims:** Both slides show purely linear success flows with no branch conditions.
- **The Codebase Reality:**  
  - Real academic workflows involve frequent network timeouts, rate limits, empty query results, paywalled non-OA PDFs, and unassigned affiliation data.
  - Research Rover implements **FastAPI background task orchestration** with cooperative cancellation tokens (`threading.Event`), non-blocking partial failure fallbacks (if PubMed fails, OpenAlex results survive), empty result handlers, and SSRF-protected PDF proxy streaming. None of these essential engineering mechanisms are represented.
- **Verdict:** **UNREALISTIC & FRAGILE SPECIFICATION.**

---

## 5. Slide-by-Slide Verification Table

| Slide # | Workflow Step in PPT | Status | Issue & Required Fix |
| :---: | :--- | :---: | :--- |
| **Slide 1** | `Select Source Database, Publication Duration, Number of Articles` | **Partially Right** | **Issue:** Uses singular *"Database"* and implies only duration/count. Does not mention Unified Search, OpenAlex, or Sort Mode (relevance vs. recency).<br>**Fix:** Label as *"Select Search Options: Source (Unified / PubMed / OpenAlex), Date Range, Limit, Sort Mode"* |
| **Slide 1** | `Download Bibliographic Data (CSV file) and Article PDFs` | **Partially Right** | **Issue:** Conflates CSV download with bulk PDF download. Full-text PDFs are only available for open-access papers and are fetched via individual cards.<br>**Fix:** Distinguish between *"Save Structured Corpus (CSV)"* and *"Stream Available Open-Access PDFs"*. |
| **Slide 1** | `Upload Bibliographic Data (CSV file)` (in Analysis column) | **Wrong** | **Issue:** Portrays manual CSV upload as a mandatory prerequisite for analytics, breaking user flow.<br>**Fix:** Show search results automatically persisting to the active corpus, with manual CSV upload as an optional secondary entry path. |
| **Slide 1** | `AI Interaction session -> Upload CSV/Article PDF` | **Wrong** | **Issue:** AI Chat in Research Rover operates on the generated vector index of the corpus; users do not manually upload files inside the chat view.<br>**Fix:** Connect active corpus directly to *"Generate Local Vector Embeddings (FAISS) -> Contextual Q&A"*. |
| **Slide 2** | `Database API (E-utility)` & `Candidate Fetch (Esearch, Efetch)` | **Partially Right** | **Issue:** Only models NCBI PubMed. Completely omits OpenAlex REST API and asynchronous parallel execution.<br>**Fix:** Expand block to *"Query Scholarly APIs (PubMed E-Utilities + OpenAlex Works API)"*. |
| **Slide 2** | `Semantic ranking -> Embedding (Database vectors) -> FAISS indexing` | **Wrong** | **Issue:** Severe architectural error. Local FAISS does NOT index remote database vectors during search. FAISS is used exclusively in the downstream RAG AI Chat.<br>**Fix:** Remove FAISS from search pipeline. Replace with *"Deduplicate & Merge (DOI/PMID/Title)"* and optional *"MedCPT Cross-Encoder Re-Ranking"*. |
| **Slide 2** | `Result store (Pandas DataFrame) -> CSV exporter` | **Right** | **Accurate:** Correctly reflects backend logic where metadata is structured into Pandas DataFrames and exported to disk in `data/`. |
| **Slide 2** | `Bibliographic Data Analysis` (Swimlane 2) | **Missing / Broken** | **Issue:** Dead end. Completely disconnected from Swimlane 1. Has no inputs and no outputs.<br>**Fix:** Add incoming arrow from `Result Store / CSV` into `Analysis Engine` and route outputs to frontend visualization views. |
| **Slide 2** | `Interaction with AI Research Assistant` (Swimlane 3) | **Missing / Broken** | **Issue:** Dead end. Completely disconnected from metadata, embeddings, and UI.<br>**Fix:** Move FAISS Indexing here: route `Clean Corpus CSV -> Chunking & SentenceTransformer -> FAISS Vector Store -> Gemini RAG Synthesis`. |
| **Slide 2** | Entire Diagram | **Missing** | **Issue:** Zero decision points. Fails to model: (1) API failures, (2) Zero results returned, (3) Non-OA paywalled papers, (4) Missing affiliations.<br>**Fix:** Introduce standard decision diamonds with clear `Yes`/`No` recovery branches. |

---

## 6. The Corrected, Production-Grade Workflow

The following corrected workflow reflects the verified, production-grade architecture of Research Rover, eliminating dead ends and aligning with actual backend services (`FastAPI`, `UnifiedSearchService`, `AnalysisService`, `CountryService`, `EmbeddingService`, and `ChatService`):

```
+-------------------------------------------------------------------------------------------------------------------------------+
|                                    RESEARCH ROVER: CORRECTED END-TO-END WORKFLOW                                              |
+-------------------------------------------------------------------------------------------------------------------------------+

[ STAGE 1: USER INTERACTION & SEARCH CONFIGURATION ]
  (1) [User Opens Research Rover Web Application]
        │
        ▼
  (2) [Enter Research Query (Topic, Keywords, or MeSH Terms)]
        │
        ▼
  (3) [Configure Search Options: Unified (PubMed + OpenAlex), Date Range, Max Results, Sort Mode]
        │
        ▼
  (4) [Submit Search Request (POST /api/v1/search/)]
        │
        ▼
[ STAGE 2: BACKEND ORCHESTRATION & DATA INGESTION ]
  (5) [FastAPI Background Orchestrator (Async Task + Cooperative Cancel Token)]
        │
        ▼
  (6) [Query Scholarly APIs Concurrently: PubMed Entrez E-Utilities & OpenAlex REST API]
        │
        ▼
     < DECISION POINT 1: API Request Successful? >
        ├────────────────────── [NO: Both APIs Failed / Timeout]
        │                             │
        │                             ▼
        │                       [Display API Error Toast & Prompt Retry] ---> (Loop back to Step 2)
        │
        └────────────────────── [YES: At least one API responded]
                                      │
                                      ▼
  (7) [Retrieve Paper Candidates & Raw Metadata Records]
        │
        ▼
     < DECISION POINT 2: Research Papers Found? (Count >= 1) >
        ├────────────────────── [NO: Zero Papers Matched]
        │                             │
        │                             ▼
        │                       [Display "No Papers Found" & Suggest Query Refinement] ---> (Loop back to Step 2)
        │
        └────────────────────── [YES: Valid Candidates Retrieved]
                                      │
                                      ▼
[ STAGE 3: DATA CLEANING, NORMALIZATION & CORPUS PERSISTENCE ]
  (8) [Multi-Source Deduplication & Record Merging (Match by DOI -> PMID -> OpenAlex ID -> Title Key)]
        │
        ▼
  (9) [Affiliation Text Mining & Country Normalization (Canonical Mapping to ISO-3166 alpha-3)]
        │
        ▼
  (10) [Save Standardized Corpus (UTF-8 BOM CSV in data/ Directory)]
        │
        ├───────────────────────────────────────────────────────┬───────────────────────────────────────┐
        ▼                                                       ▼                                       ▼
[ STAGE 4A: BIBLIOMETRIC ANALYTICS ]          [ STAGE 4B: AI RAG VECTOR PIPELINE ]    [ STAGE 4C: LITERATURE BROWSER ]
  (11) [Compute Keyword Metrics:                (14) [Chunk Abstracts & Full-Text:       (17) [Render Interactive
        - Acronym Normalization                       SentenceTransformer                     Paper Cards:
        - Frequency Distribution                      (all-MiniLM-L6-v2)]                      - Title, Authors, Year
        - Co-occurrence Matrix]                                │                               - DOI / PMID Links
        │                                                      ▼                               - Citation Counts
        ▼                                       (15) [Build Local FAISS Vector Index          - Open Access Badges]
  (12) [Build Network Models:                         (_paper_chunks_hdbscan.index)]            │
        - NetworkX Degree Centrality]                          │                                ▼
        │                                                      ▼                     < DECISION POINT 4: OA PDF? >
        ▼                                       (16) [RAG AI Research Assistant:        ├────── [NO: Paywalled]
  (13) [Country Analytics:                            - Top-k Vector Semantic Match     │          │
        - Publication Volume Rankings                 - Grounded Context Assembly       │          ▼
        - International Collab Edges]                 - Gemini LLM Answer Synthesis     │    [Link to Publisher DOI]
        │                                             - Clickable Source Chips]         │
        ▼                                                      │                        └────── [YES: Open Access]
     < DECISION POINT 3: Analysis Success? >                   │                                   │
        ├────── [NO] ---> [Fallback Metadata View]             │                                   ▼
        │                        │                             │                             (18) [Download PDF via
        └────── [YES]                    │                             │                                   Secure SSRF-
                   │                     │                             │                                   Protected
                   ▼                     │                             │                                   Proxy Stream]
[ STAGE 5: VISUALIZATION & EXPORT ]      │                             │                                   │
  (19) [Render Interactive Dashboards: <─┴─────────────────────────────┴───────────────────────────────────┘
        - SVG Interactive Word Cloud
        - Frequency Bar Charts & TopoJSON World Choropleth Map
        - 2D / 3D Force-Directed International Collaboration Graphs
        - Document-by-Keyword Binary Presence Matrix Preview]
        │
        ▼
  (20) [Terminal State: User Explores Insights, Downloads Charts (PNG/SVG), & Exports Clean Dataset (CSV)]
+---------------------------------------------------------------------------------------------------------------+
```

---

## 7. Recommended Action Plan for Presentation Slides

1. **Replace Slide 1:** Deprecate the three disconnected vertical silos. Replace with a unified **User Workflow** showing: `Search Query -> Unified Results -> Automatic Analysis Dashboard -> AI Q&A Chat -> Export`.
2. **Replace Slide 2:** 
   - Remove `FAISS indexing` from the PubMed search candidate box.
   - Add **OpenAlex** alongside PubMed.
   - Show `Deduplicate & Merge` feeding into `Corpus CSV`.
   - Show `Corpus CSV` branching into:
     - **Analytics Engine:** Word Cloud, NetworkX Centrality, Country TopoJSON Map.
     - **AI RAG Pipeline:** SentenceTransformer chunking $\to$ Local FAISS index $\to$ Gemini Chat.
   - Add the **3 decision diamonds** (`API Success?`, `Papers Found?`, `OA PDF Available?`) to demonstrate engineering rigor.
3. **Use the Generated Artifacts:** Embed the pre-rendered 300 DPI diagram [`diagram/research_rover_block_diagram.png`](file:///e:/Research_Rover/diagram/research_rover_block_diagram.png) directly into PowerPoint Slide 2. It already adheres to the clean Miro presentation standard.
