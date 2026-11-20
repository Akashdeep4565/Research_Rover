"""
System Architecture Overview
Unified end-to-end flowchart connecting all seven architectural layers of Research Rover.
Target: Master M.Tech Project Defense, Thesis Report Architecture Chapter, and Viva Examination.
"""

from .common import THEMES, get_svg_header, get_svg_footer
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

def get_mermaid():
    return """flowchart TD
    %% =========================================================================
    %% COMPLETE SYSTEM ARCHITECTURE OVERVIEW: RESEARCH ROVER
    %% Unified 7-Layer Flowchart Connecting All Subsystems
    %% =========================================================================

    classDef l1 fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E3A8A,font-weight:bold;
    classDef l2 fill:#EEF2FF,stroke:#4F46E5,stroke-width:2px,color:#312E81,font-weight:bold;
    classDef l3 fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#581C87,font-weight:bold;
    classDef l4 fill:#ECFEFF,stroke:#0891B2,stroke-width:2px,color:#155E75,font-weight:bold;
    classDef l5 fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#064E3B,font-weight:bold;
    classDef l6 fill:#FFFBEB,stroke:#D97706,stroke-width:2px,color:#78350F,font-weight:bold;
    classDef l7 fill:#FFF1F2,stroke:#E11D48,stroke-width:2px,color:#9F1239,font-weight:bold;
    classDef storage fill:#F1F5F9,stroke:#64748B,stroke-width:2px,color:#0F172A;

    subgraph L1["LAYER 1: USER INTERACTION LAYER"]
        U_START(["User Accesses Research Rover"]):::l1
        U_INPUT["Query & Filter Configuration<br/>(Sources, limits, date sliders, sort mode)"]:::l1
        U_WORKSPACES{"Select Workspace Branch"}:::l1
        WS_SEARCH["Search Workspace (/search)"]:::l1
        WS_ANALYTICS["Analytics Workspace (/analytics)"]:::l1
        WS_CHAT["Conversational RAG Chat (/chat)"]:::l1
        WS_FILES["Files & Architecture (/files)"]:::l1
    end

    subgraph L2["LAYER 2: FRONTEND / API CLIENT LAYER"]
        SPA_STACK["React 19 SPA & Router<br/>(Context Providers: Search, Analytics, Chat, Embedding, Status)"]:::l2
        EVENT_DISPATCH["Event Handlers & 1s Polling Loops"]:::l2
        AXIOS_CORE["Axios API Client (services/api.ts)<br/>Typed modules: searchApi, filesApi, chatApi, embeddingsApi, analysisApi"]:::l2
    end

    subgraph L3["LAYER 3: BACKEND PROCESSING & CONTROLLERS"]
        UVICORN_GATEWAY["Uvicorn ASGI Gateway (main.py) • Port 8000"]:::l3
        ROUTERS["Mounted FastAPIRouters<br/>/search, /files, /chat, /embeddings, /analysis, /system"]:::l3
        PYDANTIC_ENGINE["Pydantic Validation (schemas.py) & SSRF Checks"]:::l3
        CONTROLLER_LOGIC["Controller Endpoint Logic & Task Orchestration"]:::l3
        EXCEPTION_MAP["HTTP Error Code Mapping (400, 404, 422, 500)"]:::l3
    end

    subgraph L4["LAYER 4: DATA COLLECTION & EXTERNAL SOURCES"]
        SEARCH_ORCH["SearchService & UnifiedSearchService"]:::l4
        NCBI_PUBMED["NCBI PubMed Entrez E-Utilities<br/>(esearch, efetch batch 50, esummary, espell fallback)"]:::l4
        OPENALEX_API["OpenAlex Universal Works REST API<br/>(Abstract inversion, authors, institutions, OA links)"]:::l4
        CORE_STUB["CORE Repository Harvester (Planned Stub)"]:::l4
        FAULT_TOLERANCE["Non-Blocking Partial Failure Resilience"]:::l4
    end

    subgraph L5["LAYER 5: DATA CLEANING & ENRICHMENT"]
        NORM_ENGINE["Identifier Normalization (DOI, PMID, OpenAlex ID, Title Key)"]:::l5
        DEDUP_ENGINE["4-Priority Deduplication Engine<br/>(Match DOI → PMID → OpenAlex ID → Title Key)"]:::l5
        MERGE_ENGINE["Record Merging: Sources, Authors, Longer Abstract, Highest Citations"]:::l5
        AFF_FALLBACK["PubMed Affiliation Fallback Enricher (batch EFetch XML)"]:::l5
        GEO_EXTRACTOR["ISO 3166-1 Country Extractor (700+ aliases & regex word boundary)"]:::l5
        CSV_STORE[("Persistent Dataset Storage<br/>data/<sanitized_query>.csv (UTF-8-SIG)")]:::storage
    end

    subgraph L6["LAYER 6: ANALYSIS & COMPUTATION LAYER"]
        KW_FREQ_ENG["1. Keyword Frequency & Distribution Engine"]:::l6
        NETWORKX_ENG["2. NetworkX Centralities (Degree, Closeness, Betweenness, Eigenvector, Clustering)"]:::l6
        MATRIX_ENG["3. Binary Keyword Presence Matrix Engine"]:::l6
        CTRY_STATS_ENG["4. Country Publication Volume & Coverage Statistics"]:::l6
        CTRY_GRAPH_ENG["5. International Co-Authorship Collaboration Network Engine"]:::l6
        MEDCPT_ENG["6. MedCPT PyTorch Bi-Encoder Neural Re-ranking Engine"]:::l6
        FAISS_ENG["7. HDBSCAN Semantic Chunking & FAISS Flat L2 Vector Store"]:::l6
        RAG_ENG["8. Conversational RAG Query Decomposition & Gemini Synthesis"]:::l6
        CITATION_NOTE["9. Numerical Citation Metrics (No Citation Graph)"]:::l6
    end

    subgraph L7["LAYER 7: VISUALIZATION & OUTPUT LAYER"]
        ERR_BOUND["React Error Boundary Wrappers"]:::l7
        GEO_MAP["TopoJSON World Choropleth Map (WorldMap.tsx)"]:::l7
        GRAPH_2D["2D Force Collaboration Graph (react-force-graph-2d)"]:::l7
        GRAPH_3D["3D WebGL Spherical Space (Three.js & react-force-graph-3d)"]:::l7
        WORD_CLOUD["Interactive SVG Word Cloud (scaled text tokens)"]:::l7
        KW_GRAPH_SVG["Keyword Co-Occurrence Network Graph SVG"]:::l7
        RANK_TABLES["Centrality & Country Publication Ranking Tables"]:::l7
        RAG_STREAM["Conversational RAG Chat Stream & Citation Cards"]:::l7
        EXPORTS["Export Pipelines: UTF-8 BOM CSV, JSON Summaries, High-Res PNG, PDF Downloads"]:::l7
        U_OUTPUT(["Presentation-Ready Insights Delivered to User"]):::l7
    end

    %% Flow Connections Between Layers
    U_START --> U_INPUT --> U_WORKSPACES
    U_WORKSPACES --> WS_SEARCH & WS_ANALYTICS & WS_CHAT & WS_FILES
    WS_SEARCH & WS_ANALYTICS & WS_CHAT & WS_FILES --> SPA_STACK

    SPA_STACK --> EVENT_DISPATCH --> AXIOS_CORE
    AXIOS_CORE -->|HTTP Requests| UVICORN_GATEWAY

    UVICORN_GATEWAY --> ROUTERS --> PYDANTIC_ENGINE --> CONTROLLER_LOGIC
    CONTROLLER_LOGIC --> EXCEPTION_MAP

    CONTROLLER_LOGIC -->|Search Query| SEARCH_ORCH
    SEARCH_ORCH --> NCBI_PUBMED & OPENALEX_API & CORE_STUB --> FAULT_TOLERANCE

    FAULT_TOLERANCE -->|Raw Paper Records| NORM_ENGINE
    NORM_ENGINE --> DEDUP_ENGINE --> MERGE_ENGINE --> AFF_FALLBACK --> GEO_EXTRACTOR --> CSV_STORE

    CSV_STORE --> KW_FREQ_ENG & NETWORKX_ENG & MATRIX_ENG & CTRY_STATS_ENG & CTRY_GRAPH_ENG & MEDCPT_ENG & FAISS_ENG & RAG_ENG & CITATION_NOTE

    KW_FREQ_ENG & MATRIX_ENG --> WORD_CLOUD & RANK_TABLES
    NETWORKX_ENG --> KW_GRAPH_SVG & RANK_TABLES
    CTRY_STATS_ENG & CTRY_GRAPH_ENG --> GEO_MAP & GRAPH_2D & GRAPH_3D & RANK_TABLES
    MEDCPT_ENG --> WS_SEARCH
    FAISS_ENG & RAG_ENG --> RAG_STREAM

    GEO_MAP & GRAPH_2D & GRAPH_3D & WORD_CLOUD & KW_GRAPH_SVG & RANK_TABLES & RAG_STREAM --> ERR_BOUND --> EXPORTS --> U_OUTPUT
"""

def get_svg():
    w, h = 1850, 1300
    header = get_svg_header(
        w, h,
        title="Research Rover: Complete System Architecture Overview",
        subtitle="Unified 7-Layer Flowchart Connecting User Interface, API Gateway, Scholarly APIs, Deduplication, NetworkX, FAISS & Visualizers",
        layer_badge="SYSTEM OVERVIEW",
        theme_key="overview"
    )

    content = '''
  <!-- 7 Stacked Horizontal Tiers -->
  <!-- Layer 1 -->
  <g transform="translate(45, 120)">
    <rect x="0" y="0" width="1760" height="125" rx="10" fill="#eff6ff" stroke="#2563eb" stroke-width="1.8" filter="url(#shadow-sm)"/>
    <rect x="15" y="15" width="220" height="28" rx="6" fill="#2563eb"/>
    <text x="125" y="34" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">LAYER 1: USER INTERACTION</text>
    <text x="250" y="34" font-size="11" font-weight="bold" fill="#1e3a8a">Researcher Web Portal Access • Query Input • Parameter Configuration • Workspace Branching</text>
    <text x="25" y="65" font-size="10" fill="#1e293b"><b>Entry:</b> Desktop/Tablet browser access at / • Live API &amp; Model health verification pill</text>
    <text x="25" y="85" font-size="10" fill="#1e293b"><b>Workspaces:</b> [A] Search (/search: PubMed/OpenAlex, year bounds, MedCPT sort) • [B] Analytics (/analytics: Keywords &amp; Country tabs)</text>
    <text x="25" y="105" font-size="10" fill="#1e293b"><b>Conversational AI &amp; Files:</b> [C] RAG Chat (/chat: natural language Q&amp;A, source cards) • [D] Custom CSV upload &amp; architecture guide</text>
    <text x="1740" y="70" font-size="12" font-weight="bold" fill="#2563eb" text-anchor="end">↓ User Events</text>
  </g>

  <!-- Layer 2 -->
  <g transform="translate(45, 265)">
    <rect x="0" y="0" width="1760" height="125" rx="10" fill="#eef2ff" stroke="#4f46e5" stroke-width="1.8" filter="url(#shadow-sm)"/>
    <rect x="15" y="15" width="220" height="28" rx="6" fill="#4f46e5"/>
    <text x="125" y="34" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">LAYER 2: FRONTEND / API CLIENT</text>
    <text x="250" y="34" font-size="11" font-weight="bold" fill="#312e81">React 19 SPA Architecture • Context Providers Stack • Axios Singleton Client • Error Normalization</text>
    <text x="25" y="65" font-size="10" fill="#1e293b"><b>Context State Hierarchy:</b> ThemeProvider → SystemStatusProvider → SidebarProvider → SearchProvider → EmbeddingProvider → ChatProvider → AnalyticsProvider</text>
    <text x="25" y="85" font-size="10" fill="#1e293b"><b>Event Handlers &amp; Polling:</b> handleSearch(), pollProgress() (1000ms recurring timer), handleCancelSearch(), handleFileUpload() (FormData)</text>
    <text x="25" y="105" font-size="10" fill="#1e293b"><b>Axios Client Core (services/api.ts):</b> Base URL: /api/v1 • Timeout: 120s • Typed modules: searchApi, filesApi, chatApi, embeddingsApi, analysisApi, systemApi</text>
    <text x="1740" y="70" font-size="12" font-weight="bold" fill="#4f46e5" text-anchor="end">↓ HTTP Requests</text>
  </g>

  <!-- Layer 3 -->
  <g transform="translate(45, 410)">
    <rect x="0" y="0" width="1760" height="125" rx="10" fill="#faf5ff" stroke="#9333ea" stroke-width="1.8" filter="url(#shadow-sm)"/>
    <rect x="15" y="15" width="220" height="28" rx="6" fill="#9333ea"/>
    <text x="125" y="34" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">LAYER 3: BACKEND CONTROLLERS</text>
    <text x="250" y="34" font-size="11" font-weight="bold" fill="#581c87">FastAPI Application Gateway • Pydantic Schema Validation • SSRF Security Check • Async Scheduling</text>
    <text x="25" y="65" font-size="10" fill="#1e293b"><b>ASGI Core (backend/main.py):</b> Uvicorn (0.0.0.0:8000) • Lifespan background model loader • CORS middleware (allow all)</text>
    <text x="25" y="85" font-size="10" fill="#1e293b"><b>Mounted Routers:</b> /api/v1/search (asyncio.Task) • /api/v1/files (SSRF safe download) • /api/v1/chat (RAG) • /api/v1/embeddings (BackgroundTasks) • /api/v1/analysis</text>
    <text x="25" y="105" font-size="10" fill="#1e293b"><b>Validation &amp; Error Mapping:</b> Pydantic schemas (schemas.py) → HTTP 422 • FileNotFoundError → HTTP 404 • CSVLoadError/SSRF → HTTP 400 • Crash → HTTP 500</text>
    <text x="1740" y="70" font-size="12" font-weight="bold" fill="#9333ea" text-anchor="end">↓ Service Invocations</text>
  </g>

  <!-- Layer 4 -->
  <g transform="translate(45, 555)">
    <rect x="0" y="0" width="1760" height="125" rx="10" fill="#ecfeff" stroke="#0891b2" stroke-width="1.8" filter="url(#shadow-sm)"/>
    <rect x="15" y="15" width="220" height="28" rx="6" fill="#0891b2"/>
    <text x="125" y="34" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">LAYER 4: DATA COLLECTION</text>
    <text x="250" y="34" font-size="11" font-weight="bold" fill="#155e75">External Scholarly APIs • Parallel Dispatch • XML &amp; Inverted Index Parsers • Non-Blocking Resilience</text>
    <text x="25" y="65" font-size="10" fill="#1e293b"><b>Search Orchestrators:</b> SearchService &amp; UnifiedSearchService launch parallel async queries across PubMed &amp; OpenAlex</text>
    <text x="25" y="85" font-size="10" fill="#1e293b"><b>NCBI PubMed (E-Utilities):</b> esearch (PMIDs, rate limit 0.10s) → espell (spell correction) → efetch (XML batches of 50) → esummary (exact dates)</text>
    <text x="25" y="105" font-size="10" fill="#1e293b"><b>OpenAlex API &amp; CORE Stub:</b> reconstruct_abstract() inverts abstract dictionary • extracts authors, affiliations, OA links • CORE planned stub</text>
    <text x="1740" y="70" font-size="12" font-weight="bold" fill="#0891b2" text-anchor="end">↓ Raw Paper Records</text>
  </g>

  <!-- Layer 5 -->
  <g transform="translate(45, 700)">
    <rect x="0" y="0" width="1760" height="125" rx="10" fill="#ecfdf5" stroke="#059669" stroke-width="1.8" filter="url(#shadow-sm)"/>
    <rect x="15" y="15" width="220" height="28" rx="6" fill="#059669"/>
    <text x="125" y="34" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">LAYER 5: CLEANING &amp; STORAGE</text>
    <text x="250" y="34" font-size="11" font-weight="bold" fill="#065f46">Identifier Normalization • 4-Priority Deduplication • Country Extractor • Centralized CSV Storage</text>
    <text x="25" y="65" font-size="10" fill="#1e293b"><b>Normalization:</b> normalize_doi (strip prefixes), normalize_pmid, normalize_openalex_id, compute_title_key (title60_year_author20)</text>
    <text x="25" y="85" font-size="10" fill="#1e293b"><b>4-Priority Deduplication (deduplicate_results):</b> Match P1: DOI → P2: PMID → P3: OpenAlex ID → P4: title_key • Merge sources &amp; longer text</text>
    <text x="25" y="105" font-size="10" fill="#1e293b"><b>Geographic Recognition &amp; CSV Store:</b> country_extractor.py (700+ aliases, ISO-3 code resolution) • data/*.csv storage via csv_loader.py (UTF-8-SIG)</text>
    <text x="1740" y="70" font-size="12" font-weight="bold" fill="#059669" text-anchor="end">↓ Structured Datasets</text>
  </g>

  <!-- Layer 6 -->
  <g transform="translate(45, 845)">
    <rect x="0" y="0" width="1760" height="125" rx="10" fill="#fffbeb" stroke="#d97706" stroke-width="1.8" filter="url(#shadow-sm)"/>
    <rect x="15" y="15" width="220" height="28" rx="6" fill="#d97706"/>
    <text x="125" y="34" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">LAYER 6: ANALYSIS &amp; COMPUTATION</text>
    <text x="250" y="34" font-size="11" font-weight="bold" fill="#78350f">8 Parallel Computational Engines • NetworkX Graph Theory • MedCPT Bi-Encoder • FAISS Vector Store • RAG</text>
    <text x="25" y="65" font-size="10" fill="#1e293b"><b>Keywords &amp; Graphs (analysis_service.py):</b> Keyword frequency % • NetworkX centralities (Degree, Closeness, Betweenness, Eigenvector, Clustering)</text>
    <text x="25" y="85" font-size="10" fill="#1e293b"><b>Country &amp; Collaborations (country_service.py):</b> Publication volume, coverage %, international papers, co-authorship collaboration network (nodes &amp; links)</text>
    <text x="25" y="105" font-size="10" fill="#1e293b"><b>AI Neural Models &amp; Vectors:</b> MedCPT bi-encoder reranking (0-100 scores) • HDBSCAN semantic chunking + FAISS IndexFlatL2 • Gemini RAG query decomposition</text>
    <text x="1740" y="70" font-size="12" font-weight="bold" fill="#d97706" text-anchor="end">↓ Computed Payloads</text>
  </g>

  <!-- Layer 7 -->
  <g transform="translate(45, 990)">
    <rect x="0" y="0" width="1760" height="125" rx="10" fill="#fff1f2" stroke="#e11d48" stroke-width="1.8" filter="url(#shadow-sm)"/>
    <rect x="15" y="15" width="220" height="28" rx="6" fill="#e11d48"/>
    <text x="125" y="34" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">LAYER 7: VISUALIZATION &amp; OUTPUT</text>
    <text x="250" y="34" font-size="11" font-weight="bold" fill="#9f1239">Interactive UI Components • World Map • 2D/3D Force Networks • Word Cloud • RAG Citations • Export Pipelines</text>
    <text x="25" y="65" font-size="10" fill="#1e293b"><b>Geographic &amp; Network Visualizers:</b> TopoJSON World Map (react-simple-maps) • 2D Force Network (react-force-graph-2d) • 3D Spherical Space (Three.js WebGL)</text>
    <text x="25" y="85" font-size="10" fill="#1e293b"><b>Bibliometrics &amp; Tables:</b> Interactive SVG Word Cloud • Keyword Co-occurrence Network Graph SVG • Sortable Centrality &amp; Country Ranking Tables</text>
    <text x="25" y="105" font-size="10" fill="#1e293b"><b>Conversational AI &amp; Exports:</b> RAG Markdown stream with [1], [2] citation pills • Collapsible source cards • CSV (UTF-8 BOM), JSON summary, PNG charts, PDF downloads</text>
    <text x="1740" y="70" font-size="12" font-weight="bold" fill="#e11d48" text-anchor="end">★ User Value</text>
  </g>

  <!-- Bottom Final Output -->
  <g transform="translate(45, 1135)">
    <rect x="0" y="0" width="1760" height="50" rx="10" fill="#f0fdf4" stroke="#10b981" stroke-width="2"/>
    <text x="880" y="31" font-size="13" font-weight="bold" fill="#065f46" text-anchor="middle">END-TO-END RESEARCH ROVER WORKFLOW: From Topic Inquiry to Bibliometric Insights, Verified Citations, and M.Tech Presentation Assets</text>
  </g>
'''

    return header + content + get_svg_footer()

def render_matplotlib(png_path):
    fig, ax = plt.subplots(figsize=(18, 12), dpi=300)
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 12)
    ax.axis('off')

    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Header Banner
    header = FancyBboxPatch((0.4, 10.9), 17.2, 0.85, boxstyle="round,pad=0,rounding_size=0.15",
                            facecolor="#0F172A", edgecolor="#1E293B", linewidth=1.5, zorder=2)
    ax.add_patch(header)
    ax.text(0.6, 11.5, "RESEARCH ROVER: COMPLETE SYSTEM ARCHITECTURE OVERVIEW", fontsize=15, fontweight='bold', color="#FFFFFF", zorder=3)
    ax.text(0.6, 11.12, "Unified 7-Layer Flowchart Connecting User Interface, API Gateway, Scholarly APIs, Deduplication, NetworkX, FAISS & Visualizers", fontsize=9.5, color="#CBD5E1", zorder=3)
    ax.text(17.4, 11.3, "Research Rover v2.0", fontsize=10, fontweight='bold', color="#38BDF8", ha='right', zorder=3)

    tiers = [
        ("LAYER 1: USER INTERACTION", "#2563EB", "#EFF6FF", 9.4,
         "Researcher Web Portal Access • Query Input • Parameter Configuration • Workspace Branching",
         "Workspaces: Search (/search), Analytics (/analytics: Keywords & Country), RAG Chat (/chat), Custom CSV Upload"),
        
        ("LAYER 2: FRONTEND / API CLIENT", "#4F46E5", "#EEF2FF", 8.0,
         "React 19 Context Hierarchy • Component Event Dispatchers • Axios Client Engine (services/api.ts)",
         "Providers Stack (Search, Analytics, Chat, Embedding, Status) • 1s Polling Loops • Error Normalizer"),
        
        ("LAYER 3: BACKEND CONTROLLERS", "#9333EA", "#FAF5FF", 6.6,
         "FastAPI ASGI Gateway (main.py:8000) • Pydantic Validation (schemas.py) • SSRF Security Prevention",
         "Routers (/search, /files, /chat, /embeddings, /analysis, /system) • Exception Mapping (400, 404, 422, 500)"),
        
        ("LAYER 4: DATA COLLECTION", "#0891B2", "#ECFEFF", 5.2,
         "NCBI PubMed E-Utilities (esearch, efetch, esummary, espell) • OpenAlex Universal Works REST API",
         "Parallel Search Orchestration • Abstract Inversion Engine • Author Affiliation Extraction • CORE Planned Stub"),
        
        ("LAYER 5: CLEANING & STORAGE", "#059669", "#ECFDF5", 3.8,
         "Identifier Normalization • 4-Priority Deduplication (DOI → PMID → OpenAlex ID → Title Key) • Merging Engine",
         "Affiliation Fallback Enricher • ISO 3166-1 Country Extractor (700+ aliases) • CSV Storage data/*.csv (UTF-8-SIG)"),
        
        ("LAYER 6: ANALYSIS & COMPUTATION", "#D97706", "#FFFBEB", 2.4,
         "8 Parallel Analytical Engines • NetworkX Graph Centralities • MedCPT Neural Re-ranking (0-100 scores)",
         "Keyword Frequency % • Binary Presence Matrix • Co-authorship Graph • HDBSCAN Chunking + FAISS • Gemini RAG"),
        
        ("LAYER 7: VISUALIZATION & OUTPUT", "#E11D48", "#FFF1F2", 1.0,
         "TopoJSON World Map • 2D D3 Force Graph • 3D WebGL Spherical Space • Word Cloud SVG • RAG Chat Stream",
         "Sortable Centrality & Country Ranking Tables • Export Pipelines: UTF-8 BOM CSV, JSON, PNG Charts, Direct PDF"),
    ]

    for title, border_col, fill_col, y_pos, line1, line2 in tiers:
        box = FancyBboxPatch((0.5, y_pos), 17.0, 1.25, boxstyle="round,pad=0,rounding_size=0.12",
                             facecolor=fill_col, edgecolor=border_col, linewidth=1.6, zorder=2)
        ax.add_patch(box)
        badge = FancyBboxPatch((0.7, y_pos + 0.8), 3.2, 0.35, boxstyle="round,pad=0,rounding_size=0.08",
                               facecolor=border_col, edgecolor=border_col, linewidth=1, zorder=3)
        ax.add_patch(badge)
        ax.text(2.3, y_pos + 0.97, title, fontsize=9.5, fontweight='bold', color="#FFFFFF", ha='center', zorder=4)
        ax.text(4.2, y_pos + 0.97, line1, fontsize=8.5, fontweight='bold', color="#0F172A", zorder=3)
        ax.text(0.8, y_pos + 0.35, line2, fontsize=8, color="#334155", zorder=3)

        # Connector arrow
        if y_pos > 1.0:
            ax.annotate('', xy=(9.0, y_pos), xytext=(9.0, y_pos - 0.15),
                        arrowprops=dict(arrowstyle="->", color=border_col, lw=1.5), zorder=4)

    # Bottom Footer
    footer = FancyBboxPatch((0.5, 0.2), 17.0, 0.55, boxstyle="round,pad=0,rounding_size=0.1",
                            facecolor="#ECFDF5", edgecolor="#10B981", linewidth=1.5, zorder=2)
    ax.add_patch(footer)
    ax.text(9.0, 0.47, "END-TO-END RESEARCH ROVER WORKFLOW: Literature Search → Data Extraction → Deduplication → Bibliometric Graph Analysis → RAG AI Citations",
            fontsize=8.5, fontweight='bold', color="#064E3B", ha='center', zorder=3)

    plt.tight_layout()
    plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated PNG: {png_path}")
