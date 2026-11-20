# Research Rover - System Architecture & Flowcharts Document

## 1. Detailed System Flowchart

```mermaid
flowchart TD
    subgraph SECTION1["1. USER & FRONTEND LAYER"]
        U_START(["User Accesses Research Rover"])
        U_INPUT["Enter Query / Filters<br/>(Query string, max results, date range)"]
        U_NAV{"Select Page View"}
        PAGE_SEARCH["Search Page<br/>(SearchPage.tsx, SearchContext.tsx)"]
        PAGE_ANALYTICS["Analytics Page<br/>(AnalyticsPage.tsx, AnalyticsContext.tsx)"]
        PAGE_CHAT["Chat Page<br/>(ChatPage.tsx, ChatContext.tsx)"]
    end

    subgraph SECTION2["2. FRONTEND API CLIENT LAYER"]
        API_CLIENT["Axios API Client<br/>(services/api.ts - Base URL: /api/v1)"]
        REQ_SEARCH["POST /api/v1/search/query"]
        REQ_FILES["GET /api/v1/files/list<br/>POST /api/v1/files/upload"]
        REQ_KW["POST /api/v1/analysis/generate<br/>GET /api/v1/analysis/{file}/matrix"]
        REQ_COUNTRY["GET /api/v1/analysis/{file}/countries<br/>GET /api/v1/analysis/{file}/country-collaboration"]
        REQ_CHAT["POST /api/v1/chat/query<br/>POST /api/v1/embeddings/generate"]
    end

    subgraph SECTION3["3. BACKEND ROUTING & CONTROLLER LAYER"]
        ROUTE_SEARCH["Search Controller<br/>(api/routes/search.py)"]
        ROUTE_FILES["Files Controller<br/>(api/routes/files.py)"]
        ROUTE_ANALYSIS["Analysis Controller<br/>(api/routes/analysis.py)"]
        ROUTE_CHAT["Chat & Embedding Controller<br/>(api/routes/chat.py & embeddings.py)"]
        VALIDATE{"Request Validation<br/>(models/schemas.py Pydantic)"}
        ERR_VALIDATION["Return HTTP 400 / 404 / 500<br/>Error Payload"]
    end

    subgraph SECTION4["4. DATA COLLECTION & EXTERNAL INTEGRATION"]
        SRV_SEARCH["Search Service Orchestrator<br/>(services/search_service.py)"]
        SRV_PUBMED["PubMed Service<br/>(services/pubmed_service.py)"]
        API_NCBI["NCBI Entrez E-Utilities API<br/>(esearch.fcgi & efetch.fcgi)"]
        XML_PARSER["ElementTree XML Parser<br/>(Extract PMID, Title, Abstract, Journal, Year, Authors, Affiliations)"]
        ENRICH_AFF["Affiliation Enricher Fallback<br/>(services/pubmed_affiliation_enricher.py)"]
        RERANKER["MedCPT Semantic Reranker<br/>(services/reranker_service.py - PyTorch & Transformers)"]
    end

    subgraph SECTION5["5. DATA CLEANING & ENRICHMENT"]
        DEDUP["Deduplication Engine<br/>(Deduplicate by PMID, DOI, and Title)"]
        EXTRACT_CTRY["Country Extractor Utility<br/>(utils/country_extractor.py - Regex & ISO 3166-1 Map)"]
        CSV_LOADER["CSV Loader & Writer<br/>(utils/csv_loader.py - UTF-8-BOM / Latin-1 Fallbacks)"]
        DATA_STORE[("Local CSV Data Storage<br/>data/*.csv")]
    end

    subgraph SECTION6["6. ANALYSIS & COMPUTATION ENGINES"]
        SRV_KW["Analysis Service<br/>(services/analysis_service.py)"]
        KW_FREQ["Phase 1: Keyword Frequency & Percentage"]
        KW_GRAPH["Phase 2: Co-Occurrence Graph & Matrix"]
        KW_CENTRALITY["Phase 3: NetworkX Centralities<br/>(Degree, Closeness, Betweenness, Eigenvector, Clustering)"]
        KW_PRESENCE["Phase 4: Binary Keyword Presence Matrix"]
        KW_CACHE[("Cached Summary Artifacts<br/>data/*_summary.json")]

        SRV_CTRY["Country Service<br/>(services/country_service.py)"]
        CTRY_STATS["Country Publication Frequency & Coverage %"]
        CTRY_GRAPH["International Co-Authorship Graph<br/>(Nodes & Weighted Collaboration Links)"]

        SRV_EMBED["Embedding & Vector Service<br/>(services/embedding_service.py)"]
        FAISS_STORE[("FAISS Vector Index<br/>data/*.index & *.pkl")]

        SRV_CHAT["RAG Chat Service<br/>(services/chat_service.py)"]
        LLM_API["LLM Provider API<br/>(OpenAI / DeepSeek / Groq)"]
    end

    subgraph SECTION7["7. VISUALIZATION & USER OUTPUT LAYER"]
        ERR_BOUND["React Error Boundaries<br/>(components/ErrorBoundary.tsx)"]
        VIEW_KW["Keyword Analytics View<br/>(DashCards, WordCloudSvg, NetworkGraph)"]
        VIEW_MAP["Geographic World Map<br/>(components/WorldMap.tsx - react-simple-maps)"]
        VIEW_2D["2D Collaboration Network<br/>(components/CountryCollaboration2D.tsx - react-force-graph-2d)"]
        VIEW_3D["3D Collaboration Network<br/>(components/CountryCollaboration3D.tsx - react-force-graph-3d)"]
        VIEW_STATS["Summary Stats & Ranking Tables<br/>(components/CountryAnalysisView.tsx)"]
        VIEW_CHAT["Interactive RAG Stream & Citations<br/>(pages/ChatPage.tsx)"]
        U_OUTPUT(["User Insights & Exported CSV/JSON/PNG"])
    end

    %% Flow Connections
    U_START --> U_INPUT --> U_NAV
    U_NAV -->|Search Query| PAGE_SEARCH
    U_NAV -->|Analyze CSV| PAGE_ANALYTICS
    U_NAV -->|Chat Query| PAGE_CHAT

    PAGE_SEARCH --> API_CLIENT
    PAGE_ANALYTICS --> API_CLIENT
    PAGE_CHAT --> API_CLIENT

    API_CLIENT -->|Search| REQ_SEARCH --> ROUTE_SEARCH
    API_CLIENT -->|File Ops| REQ_FILES --> ROUTE_FILES
    API_CLIENT -->|Keyword Analysis| REQ_KW --> ROUTE_ANALYSIS
    API_CLIENT -->|Country Analysis| REQ_COUNTRY --> ROUTE_ANALYSIS
    API_CLIENT -->|Chat / Embed| REQ_CHAT --> ROUTE_CHAT

    ROUTE_SEARCH --> VALIDATE
    ROUTE_FILES --> VALIDATE
    ROUTE_ANALYSIS --> VALIDATE
    ROUTE_CHAT --> VALIDATE

    VALIDATE -->|Invalid| ERR_VALIDATION --> API_CLIENT
    VALIDATE -->|Valid| SRV_SEARCH
    VALIDATE -->|Valid| SRV_KW
    VALIDATE -->|Valid| SRV_CTRY
    VALIDATE -->|Valid| SRV_EMBED
    VALIDATE -->|Valid| SRV_CHAT

    SRV_SEARCH --> SRV_PUBMED
    SRV_PUBMED <-->|HTTP GET/POST| API_NCBI
    SRV_PUBMED --> XML_PARSER
    XML_PARSER -->|Missing Affiliation| ENRICH_AFF
    XML_PARSER --> DEDUP
    ENRICH_AFF --> DEDUP
    DEDUP --> RERANKER
    RERANKER --> EXTRACT_CTRY
    EXTRACT_CTRY --> CSV_LOADER --> DATA_STORE

    DATA_STORE --> SRV_KW
    SRV_KW --> KW_FREQ --> KW_GRAPH --> KW_CENTRALITY --> KW_PRESENCE --> KW_CACHE

    DATA_STORE --> SRV_CTRY
    SRV_CTRY --> CTRY_STATS
    SRV_CTRY --> CTRY_GRAPH

    DATA_STORE --> SRV_EMBED --> FAISS_STORE
    FAISS_STORE --> SRV_CHAT
    SRV_CHAT <--> LLM_API

    KW_CACHE --> ERR_BOUND
    CTRY_STATS --> ERR_BOUND
    CTRY_GRAPH --> ERR_BOUND
    SRV_CHAT --> VIEW_CHAT

    ERR_BOUND --> VIEW_KW
    ERR_BOUND --> VIEW_MAP
    ERR_BOUND --> VIEW_2D
    ERR_BOUND --> VIEW_3D
    ERR_BOUND --> VIEW_STATS

    VIEW_KW --> U_OUTPUT
    VIEW_MAP --> U_OUTPUT
    VIEW_2D --> U_OUTPUT
    VIEW_3D --> U_OUTPUT
    VIEW_STATS --> U_OUTPUT
    VIEW_CHAT --> U_OUTPUT
```

---

## 2. Simplified PPT-Friendly Flowchart

```mermaid
flowchart LR
    A["1. User Query & Interface<br/>(React / Tailwind CSS)"] --> B["2. API Gateway & Controllers<br/>(FastAPI / Pydantic)"]
    B --> C["3. External Data Retrieval<br/>(NCBI PubMed E-Utilities)"]
    C --> D["4. Data Cleaning & Extraction<br/>(Deduplication & Country Extractor)"]
    D --> E[("5. Dataset Storage<br/>(Local CSV Files)")]
    E --> F["6. Analytics Engine<br/>(NetworkX / FAISS / LLM RAG)"]
    F --> G["7. Interactive Dashboard<br/>(World Map, 2D/3D Force Networks, Word Cloud)"]
```

---

## 3. Explanation of System Blocks

1. **User & Frontend Layer**: Manages user input, search query filters, page switching (`SearchPage.tsx`, `AnalyticsPage.tsx`, `ChatPage.tsx`), and UI context state (`SearchContext`, `AnalyticsContext`, `ChatContext`, `EmbeddingContext`).
2. **Frontend API Client Layer**: Axios client (`frontend/src/services/api.ts`) pointing to `/api/v1` base URL. Handles HTTP requests for search queries, file operations, keyword analytics, country analytics, embeddings, and chat completions.
3. **Backend Routing Layer**: FastAPI controllers (`api/routes/*.py`) that parse requests, validate input schemas with Pydantic (`models/schemas.py`), and return structured JSON responses or HTTP error status codes.
4. **Data Collection Layer**: Integrates with external NCBI Entrez E-Utilities (`esearch` + `efetch`), parses XML payloads, retrieves author affiliations (with fallback enrichment), and re-ranks papers semantically using MedCPT (`ncbi/MedCPT-Query-Encoder` & `ncbi/MedCPT-Article-Encoder`).
5. **Data Cleaning & Storage Layer**: Removes duplicate papers by PMID/DOI/Title, normalizes country names via regex & ISO-3166-1 mappings (`country_extractor.py`), and saves data to CSV files in `data/` via `csv_loader.py`.
6. **Analytics Engine Layer**:
   - `analysis_service.py`: Computes keyword frequencies, co-occurrence matrices, NetworkX centralities, and presence matrices.
   - `country_service.py`: Computes publication volume per country, coverage percentages, and international co-authorship collaboration graph networks.
   - `embedding_service.py` & `chat_service.py`: Builds FAISS vector store indices for RAG Q&A via LLM APIs (OpenAI, DeepSeek, Groq).
7. **Visualization & User Output Layer**: Renders interactive widgets wrapped in React Error Boundaries: TopoJSON World Map (`WorldMap.tsx`), 2D Force-Directed Network (`CountryCollaboration2D.tsx`), 3D Force-Directed Space (`CountryCollaboration3D.tsx`), Word Cloud SVG, and allows direct exports (CSV, JSON, PNG).

---

## 4. Source Code File & Module Mapping Table

| Layer / Block | Module Functionality | Actual Source Code File Paths |
| :--- | :--- | :--- |
| **Frontend UI** | Page views & state contexts | `frontend/src/pages/SearchPage.tsx`<br/>`frontend/src/pages/AnalyticsPage.tsx`<br/>`frontend/src/pages/ChatPage.tsx`<br/>`frontend/src/context/*.tsx` |
| **API Client** | Axios HTTP client & types | `frontend/src/services/api.ts`<br/>`frontend/src/types/index.ts` |
| **API Routes** | FastAPI controller endpoints | `backend/app/api/routes/search.py`<br/>`backend/app/api/routes/analysis.py`<br/>`backend/app/api/routes/chat.py`<br/>`backend/app/api/routes/embeddings.py`<br/>`backend/app/api/routes/files.py`<br/>`backend/app/models/schemas.py` |
| **Data Collection** | PubMed fetcher & MedCPT reranker | `backend/app/services/pubmed_service.py`<br/>`backend/app/services/pubmed_affiliation_enricher.py`<br/>`backend/app/services/search_service.py`<br/>`backend/app/services/reranker_service.py` |
| **Cleaning & Storage** | Normalization & CSV storage | `backend/app/utils/country_extractor.py`<br/>`backend/app/utils/csv_loader.py`<br/>`backend/data/*.csv` |
| **Analytics Engine** | Bibliometric, NetworkX & RAG | `backend/app/services/analysis_service.py`<br/>`backend/app/services/country_service.py`<br/>`backend/app/services/embedding_service.py`<br/>`backend/app/services/chat_service.py` |
| **Visualizations** | World map, 2D & 3D force networks | `frontend/src/components/CountryAnalysisView.tsx`<br/>`frontend/src/components/WorldMap.tsx`<br/>`frontend/src/components/CountryCollaboration2D.tsx`<br/>`frontend/src/components/CountryCollaboration3D.tsx`<br/>`frontend/src/components/ErrorBoundary.tsx` |

---

## 5. Architectural Clarifications

1. **Database**: The system uses file-system CSV storage (`data/*.csv`) and FAISS vector indices (`.index`, `.pkl`), not a SQL database like PostgreSQL or MongoDB.
2. **Citation Networks**: Paper records store numeric citation counts or reference strings from PubMed metadata, but explicit paper-to-paper citation graph network analysis is not implemented (co-authorship and keyword co-occurrence graphs are implemented).
