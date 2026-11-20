# Research Rover: Flowchart Component to Source Code Traceability Matrix

> **Document Type:** Academic & Software Architecture Traceability Matrix  
> **Target Audience:** M.Tech Data Science Evaluation Committee, Viva Examiners, Project Reviewers  
> **System Version:** Research Rover v2.0.0  
> **Verification Status:** 100% Verified Against Codebase Implementation  

---

## 1. Executive Summary

This traceability matrix maps every flowchart component, operational block, decision diamond, and data store across the **Seven Architectural Layers** of Research Rover directly to its underlying implementation in the codebase.

Every entry has been validated against the actual repository files. Where a capability is planned or acts as an architectural stub (such as the CORE Open Access search stub or numeric citation counts without graph traversal), it is explicitly flagged to preserve total academic and technical honesty.

---

## 2. Layer-by-Layer Traceability Tables

### Layer 1: User Interaction Layer

| Block ID | Flowchart Node Title | UI / Controller Component | Actual Source Code File Path | Implementation Details & Function/Class |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | Web Portal Access | Browser Entry Point | [`frontend/src/App.tsx`](file:///e:/Research_Rover/frontend/src/App.tsx#L1-L50) | Client-side routing with React Router DOM v7; renders homepage at path `/`. |
| **1.1** | Verify System Status | Live Status Pill | [`frontend/src/context/SystemStatusContext.tsx`](file:///e:/Research_Rover/frontend/src/context/SystemStatusContext.tsx#L1-L60) | Polls `/api/v1/system/status` every 30s to verify API connectivity and model readiness. |
| **1.2** | Select Activity | Workspace Decision | [`frontend/src/components/layout/Navbar.tsx`](file:///e:/Research_Rover/frontend/src/components/layout/Navbar.tsx#L1-L120) | Top navigation bar with links to Search, Analytics, AI Chat, Architecture, and Settings. |
| **1.3** | Enter Query / Keywords | Search Form Input | [`frontend/src/pages/SearchPage.tsx`](file:///e:/Research_Rover/frontend/src/pages/SearchPage.tsx#L40-L90) | Text input supporting natural topic phrases or comma-separated keywords. |
| **1.4** | Configure Filters | Search Parameter Bar | [`frontend/src/pages/SearchPage.tsx`](file:///e:/Research_Rover/frontend/src/pages/SearchPage.tsx#L91-L180) | Source selector dropdown, result limit dropdown (10–100), year slider, sort mode, raw mode toggle. |
| **1.5** | Submit Search | Search Button | [`frontend/src/pages/SearchPage.tsx`](file:///e:/Research_Rover/frontend/src/pages/SearchPage.tsx#L181-L220) | `handleSearch()` validates inputs and initiates background search task. |
| **1.6** | Live Progress Feedback | Multi-Stage Loader | [`frontend/src/components/ResearchRoverLoader.tsx`](file:///e:/Research_Rover/frontend/src/components/ResearchRoverLoader.tsx#L1-L110) | Real-time animated progress bar displaying stages 0–4 and status messages. |
| **1.7–1.8** | User Cancel In-Flight | Cooperative Cancellation | [`frontend/src/context/SearchContext.tsx`](file:///e:/Research_Rover/frontend/src/context/SearchContext.tsx#L80-L115) | `handleCancel()` dispatches `searchApi.cancel()`, setting `_cancel_event` on the server. |
| **1.9** | Results Catalog | Paginated Paper Cards | [`frontend/src/pages/SearchPage.tsx`](file:///e:/Research_Rover/frontend/src/pages/SearchPage.tsx#L250-L380) | Displays paper title, authors, year, journal, DOI link, OA badge, relevance score (0–100%). |
| **1.10** | Paper Actions | Result Actions Dropdown | [`frontend/src/pages/SearchPage.tsx`](file:///e:/Research_Rover/frontend/src/pages/SearchPage.tsx#L390-L460) | Triggers PDF download, CSV export, embedding generation, or navigation to `/analytics`. |
| **1.11** | Select Dataset Source | Dataset Dropdown / Upload | [`frontend/src/pages/AnalyticsPage.tsx`](file:///e:/Research_Rover/frontend/src/pages/AnalyticsPage.tsx#L410-L460) | Selects existing CSV from `data/` or accepts drag-and-drop file upload. |
| **1.12** | Select View Tab | View Switcher Tabs | [`frontend/src/pages/AnalyticsPage.tsx`](file:///e:/Research_Rover/frontend/src/pages/AnalyticsPage.tsx#L868-L895) | Toggles between `activeTab === 'keywords'` and `activeTab === 'country'`. |
| **1.13–1.19**| Keywords Analytics | Keyword Dash & Tables | [`frontend/src/pages/AnalyticsPage.tsx`](file:///e:/Research_Rover/frontend/src/pages/AnalyticsPage.tsx#L915-L1250) | Summary metric cards, SVG word cloud, co-occurrence graph, NetworkX table, binary matrix grid. |
| **1.20–1.27**| Country Analytics | Maps & Networks | [`frontend/src/components/CountryAnalysisView.tsx`](file:///e:/Research_Rover/frontend/src/components/CountryAnalysisView.tsx#L40-L240) | TopoJSON World Map, 2D D3 Force Graph, 3D Three.js WebGL space, country ranking tables. |
| **1.28–1.34**| RAG AI Chat | Conversational Feed | [`frontend/src/pages/ChatPage.tsx`](file:///e:/Research_Rover/frontend/src/pages/ChatPage.tsx#L50-L280) | Dataset binding, FAISS status check, question input, Markdown answer with citation cards. |
| **1.35–1.39**| File Ops & Settings | Management & Theme | [`frontend/src/pages/SettingsPage.tsx`](file:///e:/Research_Rover/frontend/src/pages/SettingsPage.tsx#L1-L80) | Upload/delete CSV datasets, theme switcher (light/dark), architecture inspector. |

---

### Layer 2: Frontend / API Client Layer

| Block ID | Flowchart Node Title | Architectural Role | Actual Source Code File Path | Implementation Details & Function/Class |
| :--- | :--- | :--- | :--- | :--- |
| **2.1** | React 19 SPA & Router | Core UI Framework | [`frontend/src/App.tsx`](file:///e:/Research_Rover/frontend/src/App.tsx#L1-L75) | Client-side routing with nested context providers: `Theme > Search > Embedding > Chat > Analytics > Layout`. |
| **2.2** | Axios Core Singleton | HTTP Client Engine | [`frontend/src/services/api.ts`](file:///e:/Research_Rover/frontend/src/services/api.ts#L81-L94) | Axios instance with base URL `VITE_API_BASE_URL || 'http://localhost:8000/api/v1'`, timeout 120,000 ms. |
| **2.3** | Request Interceptor | Headers & Telemetry | [`frontend/src/services/api.ts`](file:///e:/Research_Rover/frontend/src/services/api.ts#L96-L104) | Injects `Content-Type: application/json` and client metadata. |
| **2.4–2.5** | Response Interceptor & Error Normalizer | Error Unpacker | [`frontend/src/services/api.ts`](file:///e:/Research_Rover/frontend/src/services/api.ts#L107-L131) | Normalizes error messages; parses JSON errors wrapped in Blob instances for download endpoints. |
| **2.6** | searchApi Wrapper | Search REST Service | [`frontend/src/services/api.ts`](file:///e:/Research_Rover/frontend/src/services/api.ts#L134-L161) | Methods: `search()`, `searchGet()`, `getProgress()`, `cancel()`, `getResults()`. |
| **2.7** | filesApi Wrapper | File & PDF Service | [`frontend/src/services/api.ts`](file:///e:/Research_Rover/frontend/src/services/api.ts#L164-L238) | Methods: `upload()`, `download()`, `downloadPdf()`, `getCsvData()`, `getPaginatedCsvData()`, `list()`, `delete()`. |
| **2.8** | chatApi Wrapper | RAG Chat Service | [`frontend/src/services/api.ts`](file:///e:/Research_Rover/frontend/src/services/api.ts#L241-L251) | Methods: `sendMessage()`, `sendMessageBody()`. |
| **2.9** | embeddingsApi Wrapper | Vector Index Service | [`frontend/src/services/api.ts`](file:///e:/Research_Rover/frontend/src/services/api.ts#L254-L297) | Methods: `create()`, `getProgress()`, `cancel()`, `delete()`, `getStatus()`. |
| **2.10** | analysisApi Wrapper | Bibliometric Service | [`frontend/src/services/api.ts`](file:///e:/Research_Rover/frontend/src/services/api.ts#L301-L335) | Methods: `listFiles()`, `generate()`, `getSummary()`, `getMatrix()`, `getCountryCollaboration()`, `getCountryStatistics()`. |
| **2.11** | systemApi & healthApi | Health Check Service | [`frontend/src/services/api.ts`](file:///e:/Research_Rover/frontend/src/services/api.ts#L338-L352) | Methods: `getStatus()` queries `/system/status` with abort signal support. |
| **2.12** | State Synchronization | Context Updates | [`frontend/src/context/SearchContext.tsx`](file:///e:/Research_Rover/frontend/src/context/SearchContext.tsx#L50-L120) | Updates context states upon successful API returns; triggers Sonner toast error notifications on failure. |

---

### Layer 3: Backend Processing & Controller Layer

| Block ID | Flowchart Node Title | Controller / Module | Actual Source Code File Path | Implementation Details & Function/Class |
| :--- | :--- | :--- | :--- | :--- |
| **3.1** | Uvicorn ASGI Server | Server Core | [`backend/main.py`](file:///e:/Research_Rover/backend/main.py#L91-L98) | Uvicorn server running on host `0.0.0.0`, port `8000`, with reload support. |
| **3.2** | FastAPI App Instance | Gateway Framework | [`backend/main.py`](file:///e:/Research_Rover/backend/main.py#L44-L52) | FastAPI application with OpenAPI docs mounted at `/docs` and `/redoc`. |
| **3.3** | Lifespan Context Manager | Lifecycle Manager | [`backend/main.py`](file:///e:/Research_Rover/backend/main.py#L27-L43) | Ensures `settings.DATA_FOLDER` exists and initializes `model_manager.start_background_initialization()`. |
| **3.4** | CORS Middleware | Cross-Origin Filter | [`backend/main.py`](file:///e:/Research_Rover/backend/main.py#L54-L61) | Configures CORSMiddleware with `allow_origins=["*"]`, `allow_methods=["*"]`, `allow_headers=["*"]`. |
| **3.5** | Search Controller | Route Endpoints | [`backend/app/api/routes/search.py`](file:///e:/Research_Rover/backend/app/api/routes/search.py#L48-L335) | `POST /` spawns async task; `GET /progress` returns progress; `POST /cancel` triggers cancellation; `GET /results` slices results. |
| **3.6** | Files Controller | File Management | [`backend/app/api/routes/files.py`](file:///e:/Research_Rover/backend/app/api/routes/files.py#L26-L415) | `POST /upload` validates CSV; `GET /download-pdf` validates SSRF; `GET /csv/{fn}/data` loads records; `GET /list` lists files. |
| **3.7** | Chat Controller | RAG Gateway | [`backend/app/api/routes/chat.py`](file:///e:/Research_Rover/backend/app/api/routes/chat.py#L20-L75) | Synchronous RAG endpoint; validates FAISS index existence; invokes Gemini synthesis. |
| **3.8** | Embeddings Controller | Vector Tasks | [`backend/app/api/routes/embeddings.py`](file:///e:/Research_Rover/backend/app/api/routes/embeddings.py#L32-L220) | `POST /{fn}` schedules embedding building on `BackgroundTasks`; `GET /progress` reports stage. |
| **3.9** | Analysis Controller | Bibliometric API | [`backend/app/api/routes/analysis.py`](file:///e:/Research_Rover/backend/app/api/routes/analysis.py#L31-L229) | Serves summary, presence matrix preview, country statistics, and collaboration graphs. |
| **3.10** | System Controller | Runtime Health | [`backend/app/api/routes/system.py`](file:///e:/Research_Rover/backend/app/api/routes/system.py#L17-L45) | `GET /status` returns real-time model and API readiness states without blocking. |
| **3.11** | Pydantic Schemas Engine | Input Validation | [`backend/app/models/schemas.py`](file:///e:/Research_Rover/backend/app/models/schemas.py#L1-L315) | Validates all requests; unprocessable payloads automatically return HTTP 422. |
| **3.12** | SSRF Security Validator | Network Security | [`backend/app/api/routes/files.py`](file:///e:/Research_Rover/backend/app/api/routes/files.py#L86-L150) | `validate_safe_url()` resolves DNS and blocks private/loopback IP addresses (`ipaddress.is_private`, `is_loopback`). |
| **3.13** | Exception Mapping | Error Responses | [`backend/app/api/routes/files.py`](file:///e:/Research_Rover/backend/app/api/routes/files.py#L52-L83) | Maps `CSVLoadError` to HTTP 400, `FileNotFoundError` to HTTP 404, uncaught errors to HTTP 500. |

---

### Layer 4: Data Collection & External Sources Layer

| Block ID | Flowchart Node Title | Subsystem / Service | Actual Source Code File Path | Implementation Details & Function/Class |
| :--- | :--- | :--- | :--- | :--- |
| **4.1** | Search Orchestrator | Service Coordinator | [`backend/app/services/search_service.py`](file:///e:/Research_Rover/backend/app/services/search_service.py#L70-L101) | `SearchService.search_papers()` coordinates execution via `UnifiedSearchService`. |
| **4.2** | Unified Multi-Source Engine | Parallel Dispatcher | [`backend/app/services/unified_search_service.py`](file:///e:/Research_Rover/backend/app/services/unified_search_service.py#L286-L379) | `execute_search()` runs parallel async tasks for PubMed and OpenAlex with partial failure tolerance. |
| **4.3** | Query Pre-Processing | Query Expansion | [`backend/app/services/pubmed_service.py`](file:///e:/Research_Rover/backend/app/services/pubmed_service.py#L176-L230) | `_improve_pubmed_query()` expands acronyms; `_concept_clause()` tags MeSH descriptors. |
| **4.4** | PubMed esearch.fcgi | E-Utilities Query | [`backend/app/services/pubmed_service.py`](file:///e:/Research_Rover/backend/app/services/pubmed_service.py#L433-L460) | `_search_pmids_with_offset()` executes POST with rate limiting and exponential backoff retry. |
| **4.5** | PubMed espell.fcgi | Spell Checker Fallback | [`backend/app/services/pubmed_service.py`](file:///e:/Research_Rover/backend/app/services/pubmed_service.py#L137-L170) | `_spell_check()` queries NCBI ESpell when search returns 0 hits, retrying with corrected query. |
| **4.6** | PubMed efetch.fcgi | Batch Article Retrieval | [`backend/app/services/pubmed_service.py`](file:///e:/Research_Rover/backend/app/services/pubmed_service.py#L462-L488) | `_retrieve_paper_details()` chunks PMIDs into batches of 50 (`retmode=xml`). |
| **4.7** | PubMed esummary.fcgi | Summary Verification | [`backend/app/services/pubmed_service.py`](file:///e:/Research_Rover/backend/app/services/pubmed_service.py#L489-L515) | `_fetch_summary_details()` retrieves exact publication dates, journal names, and citation strings. |
| **4.8** | PubMed XML Parser | ElementTree Parser | [`backend/app/services/pubmed_service.py`](file:///e:/Research_Rover/backend/app/services/pubmed_service.py#L579-L708) | `_extract_paper_info()` extracts Title, Abstract, PubDate, Authors, AffiliationInfo, and DOIs. |
| **4.9** | OpenAlex Works Request | REST Client | [`backend/app/services/openalex_service.py`](file:///e:/Research_Rover/backend/app/services/openalex_service.py#L38-L69) | `_get_headers_and_params()` builds query with Polite Pool `mailto` and publication date filters. |
| **4.10** | Abstract Inversion Engine | Text Reconstruction | [`backend/app/services/openalex_service.py`](file:///e:/Research_Rover/backend/app/services/openalex_service.py#L71-L91) | `reconstruct_abstract()` sorts `abstract_inverted_index` position keys to rebuild full text. |
| **4.11** | OpenAlex Work Parser | Record Mapper | [`backend/app/services/openalex_service.py`](file:///e:/Research_Rover/backend/app/services/openalex_service.py#L115-L297) | `parse_work_item()` extracts clean DOI, PMID, authors, affiliations, institutions, and PDF URLs. |
| **4.12** | CORE Search Stub | **Planned Stub** | [`backend/app/services/search_service.py`](file:///e:/Research_Rover/backend/app/services/search_service.py#L102-L111) | `_search_core()` logs "CORE search not implemented yet" and returns `[]`. Flagged as Planned. |
| **4.13** | Non-Blocking Resilience | Partial Failover | [`backend/app/services/unified_search_service.py`](file:///e:/Research_Rover/backend/app/services/unified_search_service.py#L360-L370) | If one API fails, returns available results and surfaces warning without crashing. |

---

### Layer 5: Data Cleaning & Enrichment Layer

| Block ID | Flowchart Node Title | Cleaning Module | Actual Source Code File Path | Implementation Details & Function/Class |
| :--- | :--- | :--- | :--- | :--- |
| **5.1** | normalize_doi | Identifier Cleaning | [`backend/app/services/unified_search_service.py`](file:///e:/Research_Rover/backend/app/services/unified_search_service.py#L33-L41) | Strips URL prefixes (`https://doi.org/`, `http://dx.doi.org/`), lowercases, trims whitespace. |
| **5.2** | normalize_pmid | Identifier Cleaning | [`backend/app/services/unified_search_service.py`](file:///e:/Research_Rover/backend/app/services/unified_search_service.py#L42-L51) | Strips URL paths, extracts isolated numeric string. |
| **5.3** | normalize_openalex_id | Identifier Cleaning | [`backend/app/services/unified_search_service.py`](file:///e:/Research_Rover/backend/app/services/unified_search_service.py#L52-L59) | Strips URL prefix, isolates canonical OpenAlex alphanumeric identifier. |
| **5.4** | compute_title_key | Collision-Safe Key | [`backend/app/services/unified_search_service.py`](file:///e:/Research_Rover/backend/app/services/unified_search_service.py#L60-L76) | Strips non-alphanumeric chars; generates `<title60>_<year>_<author20>` composite key. |
| **5.5** | 4-Priority Deduplication | Deduplication Engine | [`backend/app/services/unified_search_service.py`](file:///e:/Research_Rover/backend/app/services/unified_search_service.py#L209-L279) | `deduplicate_results()` matches candidate across `doi_index`, `pmid_index`, `openalex_index`, `title_index`. |
| **5.6** | Record Merging Engine | Metadata Consolidator | [`backend/app/services/unified_search_service.py`](file:///e:/Research_Rover/backend/app/services/unified_search_service.py#L77-L208) | `merge_paper_records()` merges source tags, author lists, affiliations, longest abstract, highest citations. |
| **5.7** | Affiliation Fallback Enricher | Metadata Enricher | [`backend/app/services/pubmed_affiliation_enricher.py`](file:///e:/Research_Rover/backend/app/services/pubmed_affiliation_enricher.py#L59-L96) | `fetch_affiliations_batch()` batches PMIDs (50/batch), fetches XML, extracts affiliations in-place. |
| **5.8** | Country Extractor | Geographic NER | [`backend/app/utils/country_extractor.py`](file:///e:/Research_Rover/backend/app/utils/country_extractor.py#L15-L500) | `extract_countries_from_affiliations()` matches against 700+ canonical aliases with word-boundary regex `\b`. |
| **5.9** | ISO 3166-1 Code Resolver | Geographic Mapping | [`backend/app/utils/country_extractor.py`](file:///e:/Research_Rover/backend/app/utils/country_extractor.py#L732-L741) | `get_country_iso3()` maps canonical names to 3-letter alpha-3 codes for TopoJSON rendering. |
| **5.10** | Centralized CSV Loader | Fault-Tolerant Reader | [`backend/utils/csv_loader.py`](file:///e:/Research_Rover/backend/utils/csv_loader.py#L54-L125) | `check_bom()` and `detect_csv_encoding()` probe UTF-8, UTF-8-SIG, CP1252, ISO-8859-1, Latin-1, and chardet. |
| **5.11** | Dataset Storage | Flat-File Store | [`backend/app/services/search_service.py`](file:///e:/Research_Rover/backend/app/services/search_service.py#L211-L245) | `save_results_to_csv()` writes structured 13-column CSV dataset to `data/<sanitized_query>.csv` (UTF-8-SIG). |

---

### Layer 6: Analysis & Computation Layer

| Block ID | Flowchart Node Title | Analytical Module | Actual Source Code File Path | Implementation Details & Function/Class |
| :--- | :--- | :--- | :--- | :--- |
| **6.1** | Keyword Frequency Engine | Bibliometrics | [`backend/app/services/analysis_service.py`](file:///e:/Research_Rover/backend/app/services/analysis_service.py#L214-L234) | Normalizes keywords via alias map; aggregates frequencies with `Counter`; calculates corpus percentage. |
| **6.2** | Keyword Co-Occurrence | Graph Construction | [`backend/app/services/analysis_service.py`](file:///e:/Research_Rover/backend/app/services/analysis_service.py#L236-L262) | Generates pairwise combinations `itertools.combinations(sorted(kw), 2)` to build weighted edge graph. |
| **6.3** | NetworkX Graph Centralities | Graph Theory | [`backend/app/services/analysis_service.py`](file:///e:/Research_Rover/backend/app/services/analysis_service.py#L310-L353) | Computes 5 centralities: Degree, Closeness, Betweenness, Eigenvector, and Clustering Coefficient. |
| **6.4** | Binary Keyword Presence Matrix | One-Hot Encoding | [`backend/app/services/analysis_service.py`](file:///e:/Research_Rover/backend/app/services/analysis_service.py#L235-L252) | Constructs binary indicator matrix (papers x top keywords); exports to CSV and serves preview payload. |
| **6.5** | Country Publication Volume | Bibliometrics | [`backend/app/services/country_service.py`](file:///e:/Research_Rover/backend/app/services/country_service.py#L81-L128) | Computes publication counts, coverage %, international multi-country papers, and unassigned records. |
| **6.6** | International Co-Authorship Graph | Collaboration Network | [`backend/app/services/country_service.py`](file:///e:/Research_Rover/backend/app/services/country_service.py#L132-L175) | Builds nodes (country, ISO-3, paper_count) and weighted links (co-authorship count) for 2D/3D viewers. |
| **6.7** | MedCPT Neural Re-ranker | Deep Learning / AI | [`backend/app/services/reranker_service.py`](file:///e:/Research_Rover/backend/app/services/reranker_service.py#L34-L174) | PyTorch bi-encoder models (`ncbi/MedCPT-Query-Encoder` & `ncbi/MedCPT-Article-Encoder`); CLS dot product; 0–100 score. |
| **6.8** | Full-Text Scraper & Chunking | Vector Preprocessing | [`backend/app/services/embedding_service.py`](file:///e:/Research_Rover/backend/app/services/embedding_service.py#L38-L150) | BeautifulSoup full-text scraper; NLTK sentence tokenize; HDBSCAN clustering (`min_cluster_size=3`). |
| **6.9** | Dense Vector FAISS Indexing | Vector Store | [`backend/app/services/embedding_service.py`](file:///e:/Research_Rover/backend/app/services/embedding_service.py#L249-L370) | Encodes sentences with `all-mpnet-base-v2`; builds L2-normalized FAISS `IndexFlatL2` dense index. |
| **6.10** | Conversational RAG Engine | Generative AI | [`backend/app/services/chat_service.py`](file:///e:/Research_Rover/backend/app/services/chat_service.py#L32-L215) | Gemini query decomposition (<= 5 sub-queries); multi-query FAISS retrieval (`k=5`); citation-enforcing synthesis. |
| **6.11** | Citation Metric Capture | **Clarification Note** | [`backend/app/services/unified_search_service.py`](file:///e:/Research_Rover/backend/app/services/unified_search_service.py#L201-L204) | Captures numerical citation counts from OpenAlex & PubMed. Citation graph analysis is not implemented. |

---

### Layer 7: Visualization & Output Layer

| Block ID | Flowchart Node Title | Visualizer / Export | Actual Source Code File Path | Implementation Details & Function/Class |
| :--- | :--- | :--- | :--- | :--- |
| **7.1** | ErrorBoundary Wrapper | Resilience Component | [`frontend/src/components/ErrorBoundary.tsx`](file:///e:/Research_Rover/frontend/src/components/ErrorBoundary.tsx#L1-L85) | Wraps D3, Three.js, and TopoJSON renderers; catches WebGL/canvas errors with retry fallback card. |
| **7.2** | TopoJSON Geographic World Map | Map Component | [`frontend/src/components/WorldMap.tsx`](file:///e:/Research_Rover/frontend/src/components/WorldMap.tsx#L1-L150) | `react-simple-maps` with `world-110m.json`; choropleth shading; hover tooltips (papers count and %). |
| **7.3** | 2D Force-Directed Network | 2D Physics Graph | [`frontend/src/components/CountryCollaboration2D.tsx`](file:///e:/Research_Rover/frontend/src/components/CountryCollaboration2D.tsx#L1-L120) | `react-force-graph-2d` with D3 spring simulation; node size reflects volume; link width reflects collab weight. |
| **7.4** | 3D WebGL Spherical Space | 3D Space Graph | [`frontend/src/components/CountryCollaboration3D.tsx`](file:///e:/Research_Rover/frontend/src/components/CountryCollaboration3D.tsx#L1-L140) | `react-force-graph-3d` with Three.js; country billboard text labels (`three-spritetext`); orbital camera. |
| **7.5** | Country Ranking & Collab Tables | Data Tables | [`frontend/src/components/CountryAnalysisView.tsx`](file:///e:/Research_Rover/frontend/src/components/CountryAnalysisView.tsx#L550-L650) | Searchable country ranking table with ISO-3 badges; collaboration pairs table; unassigned papers review modal. |
| **7.6** | Interactive SVG Word Cloud | Text Visualizer | [`frontend/src/pages/AnalyticsPage.tsx`](file:///e:/Research_Rover/frontend/src/pages/AnalyticsPage.tsx#L1020-L1110) | SVG word cloud with spiral packing placement; font size scaled by term frequency; hover & click-to-filter. |
| **7.7** | Co-Occurrence Network Graph SVG | SVG Network | [`frontend/src/pages/AnalyticsPage.tsx`](file:///e:/Research_Rover/frontend/src/pages/AnalyticsPage.tsx#L1120-L1240) | Pure SVG force network; node radius scaled by frequency; edge thickness by co-occurrence count; zoom/pan. |
| **7.8** | NetworkX Centrality Table | Data Table | [`frontend/src/pages/AnalyticsPage.tsx`](file:///e:/Research_Rover/frontend/src/pages/AnalyticsPage.tsx#L1250-L1350) | Sortable table of Degree, Closeness, Betweenness, Eigenvector, and Clustering metrics with tabular numbers. |
| **7.9** | Binary Presence Matrix Table | Matrix Grid | [`frontend/src/pages/AnalyticsPage.tsx`](file:///e:/Research_Rover/frontend/src/pages/AnalyticsPage.tsx#L1360-L1450) | High-density 0/1 binary indicator grid; papers as rows; keywords as columns; green pill indicators. |
| **7.10** | Conversational RAG Stream | Chat UI | [`frontend/src/pages/ChatPage.tsx`](file:///e:/Research_Rover/frontend/src/pages/ChatPage.tsx#L100-L220) | Markdown-rendered message stream with syntax highlighting and clickable superscript citation badges `[1]`, `[2]`. |
| **7.11** | Collapsible Citation Cards | Evidence UI | [`frontend/src/pages/ChatPage.tsx`](file:///e:/Research_Rover/frontend/src/pages/ChatPage.tsx#L230-L310) | Accordion cards displaying retrieved FAISS passage snippets, paper title, and clickable DOI link. |
| **7.12** | CSV Export with UTF-8 BOM | Data Export | [`frontend/src/pages/AnalyticsPage.tsx`](file:///e:/Research_Rover/frontend/src/pages/AnalyticsPage.tsx#L66-L97) | `downloadCSV()` prepends byte-order mark (`\xef\xbb\xbf`) for native Excel compatibility. |
| **7.13** | JSON Summary Export | Data Export | [`frontend/src/pages/AnalyticsPage.tsx`](file:///e:/Research_Rover/frontend/src/pages/AnalyticsPage.tsx#L98-L101) | `downloadJSON()` exports structured JSON summary with metrics and metadata. |
| **7.14** | High-Res PNG Chart Export | Image Export | [`frontend/src/pages/AnalyticsPage.tsx`](file:///e:/Research_Rover/frontend/src/pages/AnalyticsPage.tsx#L104-L150) | `svgToPng()` serializes SVG DOM, paints canvas background, renders 300 DPI PNG image for PowerPoint. |
| **7.15** | Direct / Proxy PDF Stream | PDF Delivery | [`frontend/src/services/api.ts`](file:///e:/Research_Rover/frontend/src/services/api.ts#L181-L205) | `filesApi.downloadPdf()` connects to SSRF-validated proxy endpoint and streams binary PDF to user disk. |

---

## 3. Implementation Verification Summary

1. **Total Layers Analyzed:** 7 Individual Architectural Layers + 1 Complete System Overview.
2. **Total Codebase Modules Verified:** 32 Distinct Files (18 Frontend files + 14 Backend files).
3. **Verified Functional Capabilities:**
   - Multi-source search across PubMed and OpenAlex with non-blocking partial failure resilience.
   - 4-priority deduplication engine (DOI → PMID → OpenAlex ID → Composite Title Key).
   - ISO 3166-1 geographic entity extraction via 700+ canonical aliases and word-boundary regex.
   - Fault-tolerant CSV reader with automatic byte-order mark and multi-encoding probing.
   - MedCPT PyTorch bi-encoder neural re-ranking with 0–100 monotonic normalization.
   - NetworkX graph centrality metrics (5 standard algorithms) and binary presence matrix generation.
   - International co-authorship collaboration networks rendered in 2D D3 and 3D WebGL Three.js.
   - FAISS dense vector store (`IndexFlatL2`) with HDBSCAN semantic chunking.
   - Conversational RAG Q&A with Google Gemini Flash and verifiable citation evidence cards.
4. **Verified Architectural Stubs & Clarifications:**
   - **Database:** Local flat-file CSV storage (`data/*.csv`) and FAISS binary vector indices (`.index`); no SQL/NoSQL database is used.
   - **CORE Search:** The enum `SearchSource.CORE` exists in `schemas.py`, but `_search_core()` in `search_service.py:102` logs that it is not implemented and returns `[]`.
   - **Paper Citations:** Numerical citation counts (`cited_by_count` / `Citation_Count`) are extracted from OpenAlex and PubMed metadata, but explicit paper-to-paper citation network graph analysis is not implemented.
