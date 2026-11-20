"""
Model Manager for Research Rover.

Tracks actual runtime initialization states of required local models (SentenceTransformer),
lazy-loaded semantic re-rankers (MedCPT), and remote AI models (Gemini).
Never loads heavyweight models merely to check their status.
"""

import logging
import threading
import time
from typing import Any, Dict, Optional

from app.core.config import get_settings

logger = logging.getLogger("research_rover")


class ModelManager:
    """Singleton manager for model initialization and real-time readiness tracking."""

    _instance: Optional["ModelManager"] = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ModelManager, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self._initialized = True
        self._init_lock = threading.Lock()

        # Sentence Transformer (Local required embedding model)
        self._sentence_model = None
        self._sentence_status: str = "not_loaded"  # not_loaded, loading, loaded, error
        self._sentence_error: Optional[str] = None
        self._sentence_loaded_at: Optional[float] = None
        self._sentence_thread: Optional[threading.Thread] = None

    def start_background_initialization(self) -> None:
        """
        Initiate asynchronous background loading of the local SentenceTransformer model.
        Does not block FastAPI startup or HTTP request loops.
        """
        with self._init_lock:
            if self._sentence_status in ("loading", "loaded"):
                logger.debug(f"Sentence transformer already in state: {self._sentence_status}")
                return

            self._sentence_status = "loading"
            self._sentence_error = None

            self._sentence_thread = threading.Thread(
                target=self._load_sentence_model_worker,
                name="sentence-transformer-loader",
                daemon=True,
            )
            self._sentence_thread.start()
            logger.info("Started background loading of SentenceTransformer embedding model")

    def _load_sentence_model_worker(self) -> None:
        """Worker thread to load SentenceTransformer weights into memory."""
        settings = get_settings()
        t0 = time.time()
        try:
            logger.info(f"Loading local SentenceTransformer model: {settings.EMBEDDING_MODEL}")
            from sentence_transformers import SentenceTransformer

            model = SentenceTransformer(settings.EMBEDDING_MODEL)
            with self._init_lock:
                self._sentence_model = model
                self._sentence_status = "loaded"
                self._sentence_loaded_at = time.time()
                self._sentence_error = None
            duration = round(time.time() - t0, 2)
            logger.info(f"SentenceTransformer model '{settings.EMBEDDING_MODEL}' loaded successfully in {duration}s")
        except Exception as e:
            with self._init_lock:
                self._sentence_model = None
                self._sentence_status = "error"
                self._sentence_error = str(e)
            logger.error(f"Failed to load SentenceTransformer model: {e}", exc_info=True)

    def get_sentence_model(self):
        """
        Retrieve the SentenceTransformer model instance.
        If loading is already in progress, waits for the background thread to finish.
        If not yet started, loads synchronously and caches.
        """
        if self._sentence_status == "loaded" and self._sentence_model is not None:
            return self._sentence_model

        if self._sentence_status == "loading" and self._sentence_thread is not None:
            logger.info("Waiting for background SentenceTransformer loading to complete...")
            self._sentence_thread.join(timeout=60)
            if self._sentence_status == "loaded" and self._sentence_model is not None:
                return self._sentence_model
            raise RuntimeError(f"SentenceTransformer model failed to load: {self._sentence_error or 'timeout'}")

        # If not started or previously errored, load directly
        with self._init_lock:
            if self._sentence_status == "loaded" and self._sentence_model is not None:
                return self._sentence_model

            self._sentence_status = "loading"
            try:
                settings = get_settings()
                from sentence_transformers import SentenceTransformer

                self._sentence_model = SentenceTransformer(settings.EMBEDDING_MODEL)
                self._sentence_status = "loaded"
                self._sentence_loaded_at = time.time()
                self._sentence_error = None
                return self._sentence_model
            except Exception as e:
                self._sentence_status = "error"
                self._sentence_error = str(e)
                raise RuntimeError(f"Failed to load sentence model: {e}")

    def get_models_status(self) -> Dict[str, Any]:
        """
        Non-blocking read of current runtime model initialization states.
        Never triggers heavy model loading or external network calls during this check.
        """
        settings = get_settings()

        # 1. Local SentenceTransformer status
        embedding_status = self._sentence_status
        embedding_info = {
            "name": settings.EMBEDDING_MODEL,
            "status": embedding_status,
            "type": "local",
            "required": True,
            "details": self._sentence_error if embedding_status == "error" else None,
        }

        # 2. Local MedCPT Re-Ranker status
        reranker_status = "not_loaded"
        reranker_details = "Lazy loaded on PubMed semantic re-rank"
        if not settings.RERANK_ENABLED:
            reranker_status = "disabled"
            reranker_details = "RERANK_ENABLED is False"
        else:
            try:
                from app.core.dependencies import get_reranker
                # get_reranker is cached, returns the MedCPTReRanker instance if created
                reranker_instance = get_reranker()
                if reranker_instance is not None:
                    if getattr(reranker_instance, "_loaded", False):
                        reranker_status = "loaded"
                        reranker_details = "MedCPT bi-encoder loaded in memory"
                    elif getattr(reranker_instance, "_unavailable", False):
                        reranker_status = "error"
                        reranker_details = "MedCPT initialization failed"
            except Exception as e:
                logger.debug(f"Error checking reranker status: {e}")

        reranker_info = {
            "name": "ncbi/MedCPT",
            "status": reranker_status,
            "type": "local",
            "required": False,
            "details": reranker_details,
        }

        # 3. Remote LLM (Gemini) status
        llm_status = "not_configured"
        llm_details = "GOOGLE_GENAI_API_KEY is not configured"
        has_api_key = bool(settings.GOOGLE_GENAI_API_KEY and settings.GOOGLE_GENAI_API_KEY.strip())

        if has_api_key:
            try:
                from app.core.dependencies import get_llm_instance
                llm_instance = get_llm_instance()
                if llm_instance is not None:
                    llm_status = "available"
                    llm_details = f"Configured for model: {settings.GEMINI_MODEL}"
                else:
                    llm_status = "unavailable"
                    llm_details = "LLM client initialization returned None"
            except Exception as e:
                llm_status = "error"
                llm_details = f"LLM configuration error: {e}"

        llm_info = {
            "name": settings.GEMINI_MODEL,
            "status": llm_status,
            "type": "remote",
            "required": False,
            "details": llm_details,
        }

        # 4. Overall models status calculation
        # Priority:
        # - If embedding is loading: "loading"
        # - If embedding is error: "error"
        # - If embedding is not loaded: "not_loaded"
        # - If embedding is loaded:
        #     - If LLM is available: "loaded"
        #     - If LLM is not configured/unavailable: "partial" (local ready, remote unavailable)
        if embedding_status == "loading":
            overall_status = "loading"
        elif embedding_status == "error":
            overall_status = "error"
        elif embedding_status == "not_loaded":
            overall_status = "not_loaded"
        elif embedding_status == "loaded":
            if llm_status in ("available", "loaded"):
                overall_status = "loaded"
            else:
                overall_status = "partial"
        else:
            overall_status = "not_loaded"

        return {
            "status": overall_status,
            "components": {
                "embedding": embedding_info,
                "reranker": reranker_info,
                "llm": llm_info,
            },
        }

    def reset_for_testing(
        self,
        status: str = "not_loaded",
        model: Any = None,
        error: Optional[str] = None,
    ) -> None:
        """Helper for unit tests to simulate various model states."""
        with self._init_lock:
            self._sentence_status = status
            self._sentence_model = model
            self._sentence_error = error
            self._sentence_thread = None


# Global singleton instance
model_manager = ModelManager()
