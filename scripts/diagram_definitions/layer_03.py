"""
Layer 3: Backend Processing & Controller Layer
Covers Uvicorn ASGI server, FastAPI routing, controller endpoints, Pydantic validation,
SSRF security checks, background task orchestration, error handling (HTTP 400, 404, 422, 500),
and controller-to-service communication.
"""

from .common import THEMES, get_svg_header, get_svg_footer
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

def get_mermaid():
    return """flowchart TD
    %% =========================================================================
    %% LAYER 3: BACKEND PROCESSING & CONTROLLER LAYER
    %% Project: Research Rover
    %% Focus: FastAPI Routing, Controller Handlers, Pydantic Schemas, Exception Handling
    %% =========================================================================

    classDef startEnd fill:#FAF5FF,stroke:#9333EA,stroke-width:2.5px,color:#581C87,font-weight:bold;
    classDef server fill:#F8FAFC,stroke:#A855F7,stroke-width:1.5px,color:#0F172A;
    classDef route fill:#F3E8FF,stroke:#7E22CE,stroke-width:1.5px,color:#3B0764,font-weight:bold;
    classDef decision fill:#FEF3C7,stroke:#D97706,stroke-width:2px,color:#78350F,font-weight:bold;
    classDef errorState fill:#FEE2E2,stroke:#EF4444,stroke-width:1.5px,color:#991B1B;
    classDef serviceCall fill:#ECFEFF,stroke:#0891B2,stroke-width:1.5px,color:#164E63;
    classDef output fill:#ECFDF5,stroke:#10B981,stroke-width:2px,color:#064E3B;

    B_ENTRY(["3.0 Entry: Incoming HTTP Requests on Port 8000<br/>(Received from Layer 2: Frontend API Client)"]):::startEnd

    %% ─── ASGI SERVER & FASTAPI GATEWAY ───────────────────────────────────────
    subgraph SUB_GATEWAY["ASGI SERVER & APPLICATION GATEWAY (backend/main.py)"]
        UVICORN["3.1 Uvicorn ASGI Server (0.0.0.0:8000)<br/>Worker threads, auto-reload, structured logging"]:::server
        FASTAPI_APP["3.2 FastAPI App Instance<br/>Docs: /docs (Swagger UI) • /redoc (ReDoc)"]:::server
        LIFESPAN["3.3 Lifespan Context Manager<br/>• Ensures data/ directory exists<br/>• Launches background model loading (model_manager)"]:::server
        CORS_MW["3.4 CORS Middleware<br/>allow_origins=['*'], allow_methods=['*'], allow_headers=['*']"]:::server
    end

    %% ─── ROUTER MOUNTING ─────────────────────────────────────────────────────
    subgraph SUB_ROUTERS["FASTAPI ROUTER DISPATCHING (backend/app/api/routes)"]
        R_SEARCH["Search Router<br/>prefix: /api/v1/search<br/>(routes/search.py)"]:::route
        R_FILES["Files Router<br/>prefix: /api/v1/files<br/>(routes/files.py)"]:::route
        R_CHAT["Chat Router<br/>prefix: /api/v1/chat<br/>(routes/chat.py)"]:::route
        R_EMBED["Embeddings Router<br/>prefix: /api/v1/embeddings<br/>(routes/embeddings.py)"]:::route
        R_ANALYSIS["Analysis Router<br/>prefix: /api/v1/analysis<br/>(routes/analysis.py)"]:::route
        R_SYSTEM["System Router<br/>prefix: /api/v1/system<br/>(routes/system.py)"]:::route
        R_HEALTH["Health & Root<br/>GET /health & GET /<br/>(main.py inline)"]:::route
    end

    %% ─── PYDANTIC VALIDATION ENGINE ──────────────────────────────────────────
    subgraph SUB_VALIDATION["PYDANTIC REQUEST VALIDATION ENGINE (models/schemas.py)"]
        V_CHECK{"3.5 Validate Payload Schema & Types"}:::decision
        V_FAIL["Return HTTP 422 Unprocessable Entity<br/>Field errors, type mismatches, range violations"]:::errorState
        V_PASS["Schema Validated Successfully<br/>SearchRequest, ChatRequest, AnalysisRequest, etc."]:::output
    end

    %% ─── CONTROLLER HANDLERS & SECURITY ──────────────────────────────────────
    subgraph SUB_CONTROLLERS["CONTROLLER ENDPOINT LOGIC & SECURITY VALIDATION"]
        CTRL_SEARCH["Search Controller<br/>• POST /: Cancels prior task, starts asyncio background task<br/>• GET /progress: Reads module-global search_progress_state<br/>• POST /cancel: Sets _cancel_event.set()<br/>• GET /results: Slices _last_results array"]:::server
        CTRL_FILES["Files Controller<br/>• POST /upload: Probes CSV encoding via detect_csv_encoding<br/>• GET /download-pdf: SSRF security check (validate_safe_url)<br/>• GET /csv/{fn}/data: Reads CSV into records<br/>• GET /list: Returns FileInfo[] list"]:::server
        CTRL_CHAT["Chat Controller<br/>• POST /{fn}: Checks if FAISS index exists in data/<br/>• If present: invokes ChatService.generate_response()<br/>• If missing: falls back to general Gemini response"]:::server
        CTRL_EMBED["Embeddings Controller<br/>• POST /{fn}: Checks existing artifacts (skips unless force=True)<br/>• Schedules EmbeddingService on BackgroundTasks<br/>• GET /progress: Returns stage 0-3 percent"]:::server
        CTRL_ANALYSIS["Analysis Controller<br/>• POST /generate: Calls AnalysisService.build_analysis_artifacts<br/>• GET /{fn}/summary: Loads cached JSON or generates<br/>• GET /{fn}/country-collaboration: Invokes CountryService"]:::server
        CTRL_SYSTEM["System Controller<br/>• GET /status: Queries model_manager without blocking"]:::server
    end

    %% ─── EXCEPTION HANDLING ──────────────────────────────────────────────────
    subgraph SUB_EXCEPTIONS["CENTRALIZED EXCEPTION & ERROR CODE MAPPING"]
        EX_CHECK{"3.6 Exception Handler"}:::decision
        EX_400["HTTP 400 Bad Request<br/>• Non-CSV file uploaded<br/>• Malformed / SSRF forbidden URL<br/>• CSVLoadError / unreadable encoding"]:::errorState
        EX_404["HTTP 404 Not Found<br/>• FileNotFoundError: Dataset or index not found"]:::errorState
        EX_500["HTTP 500 Internal Server Error<br/>• External service crash / uncaught exception"]:::errorState
    end

    %% ─── SERVICE INVOCATION TARGETS ──────────────────────────────────────────
    subgraph SUB_SERVICES["DELEGATION TO DOMAIN SERVICE MANAGERS"]
        TO_L4["Layer 4: Data Collection & External Sources<br/>(SearchService, PubMedService, OpenAlexService)"]:::serviceCall
        TO_L5["Layer 5: Data Cleaning & Enrichment<br/>(UnifiedSearchService, country_extractor, csv_loader)"]:::serviceCall
        TO_L6["Layer 6: Analysis & Computation Layer<br/>(AnalysisService, CountryService, MedCPT, FAISS, Gemini)"]:::serviceCall
    end

    B_OUT(["3.7 Response Generation & Serialization<br/>(JSONResponse, FileResponse, StreamingResponse returned to Layer 2)"]):::startEnd

    %% Connections
    B_ENTRY --> UVICORN --> FASTAPI_APP --> LIFESPAN & CORS_MW --> SUB_ROUTERS
    SUB_ROUTERS --> V_CHECK
    V_CHECK -->|Invalid| V_FAIL --> B_OUT
    V_CHECK -->|Valid| V_PASS --> SUB_CONTROLLERS

    SUB_CONTROLLERS --> EX_CHECK
    EX_CHECK -->|Error Raised| EX_400 & EX_404 & EX_500 --> B_OUT
    EX_CHECK -->|Clean Execution| SUB_SERVICES

    TO_L4 --> B_OUT
    TO_L5 --> B_OUT
    TO_L6 --> B_OUT
"""

def get_svg():
    w, h = 1750, 1250
    header = get_svg_header(
        w, h,
        title="Layer 3: Backend Processing & Controller Layer Flowchart",
        subtitle="FastAPI ASGI Routing, Pydantic Schema Validation, Controller Logic, Security Boundaries & Exception Handling",
        layer_badge="LAYER 03",
        theme_key="layer_03"
    )

    content = '''
  <!-- Inter-layer Connectivity Cards -->
  <g transform="translate(45, 115)">
    <rect x="0" y="0" width="380" height="42" rx="8" fill="#e0e7ff" stroke="#6366f1" stroke-width="1.5"/>
    <text x="15" y="26" font-size="12" font-weight="bold" fill="#3730a3">INPUT SOURCE:</text>
    <text x="120" y="26" font-size="12" fill="#334155">Layer 2: HTTP Requests from Axios API Client</text>
  </g>
  <g transform="translate(1325, 115)">
    <rect x="0" y="0" width="380" height="42" rx="8" fill="#ecfeff" stroke="#0891b2" stroke-width="1.5"/>
    <text x="15" y="26" font-size="12" font-weight="bold" fill="#155e75">OUTPUT TARGET:</text>
    <text x="130" y="26" font-size="12" fill="#334155">Layer 4, 5, 6 &amp; HTTP Responses to Layer 2</text>
  </g>

  <!-- Left: ASGI Server & Routing Gateway -->
  <g transform="translate(45, 175)">
    <rect x="0" y="0" width="460" height="970" rx="14" fill="#fafafa" stroke="#a855f7" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="430" height="34" rx="6" fill="#f3e8ff"/>
    <text x="230" y="37" font-size="13" font-weight="bold" fill="#6b21a8" text-anchor="middle">ASGI SERVER &amp; ROUTING GATEWAY</text>

    <!-- Uvicorn & FastAPI App -->
    <rect x="20" y="65" width="420" height="90" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="90" font-size="11.5" font-weight="bold" fill="#0f172a">3.1 Uvicorn ASGI Server (0.0.0.0:8000)</text>
    <text x="35" y="108" font-size="9.5" fill="#475569">• Async event loop, multi-worker support, structured logging</text>
    <text x="35" y="124" font-size="9.5" fill="#475569">• FastAPI 2.0.0 App instance • Swagger UI docs at /docs</text>
    <text x="35" y="140" font-size="9.5" fill="#475569">• CORS Middleware: allow_origins=['*'], allow_credentials=True</text>

    <!-- Lifespan Context -->
    <rect x="20" y="170" width="420" height="75" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="195" font-size="11" font-weight="bold" fill="#0f172a">3.2 Lifespan Startup &amp; Shutdown Manager</text>
    <text x="35" y="213" font-size="9.5" fill="#475569">• Automatically ensures data/ storage directory exists</text>
    <text x="35" y="229" font-size="9.5" fill="#475569">• Triggers model_manager.start_background_initialization()</text>

    <!-- Router Mounts -->
    <rect x="20" y="260" width="420" height="660" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="285" font-size="11.5" font-weight="bold" fill="#581c87">3.3 Mounted API Router Controllers</text>

    <!-- Router items -->
    <rect x="30" y="300" width="400" height="85" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
    <text x="45" y="322" font-size="10.5" font-weight="bold" fill="#1e1b4b">/api/v1/search (api/routes/search.py)</text>
    <text x="45" y="340" font-size="9" fill="#475569">• POST /: background search task via asyncio.create_task</text>
    <text x="45" y="356" font-size="9" fill="#475569">• GET /progress: progress stage (0-4), status, percent</text>
    <text x="45" y="372" font-size="9" fill="#475569">• POST /cancel: sets _cancel_event • GET /results: paginated slice</text>

    <rect x="30" y="395" width="400" height="85" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
    <text x="45" y="417" font-size="10.5" font-weight="bold" fill="#1e1b4b">/api/v1/files (api/routes/files.py)</text>
    <text x="45" y="435" font-size="9" fill="#475569">• POST /upload: checks .csv, probe encoding via detect_csv_encoding</text>
    <text x="45" y="451" font-size="9" fill="#475569">• GET /download/{fn}: FileResponse stream • GET /list: FileInfo[]</text>
    <text x="45" y="467" font-size="9" fill="#475569">• GET /download-pdf: SSRF security validation &amp; proxy stream</text>

    <rect x="30" y="490" width="400" height="85" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
    <text x="45" y="512" font-size="10.5" font-weight="bold" fill="#1e1b4b">/api/v1/chat (api/routes/chat.py)</text>
    <text x="45" y="530" font-size="9" fill="#475569">• POST /{filename} &amp; POST /: synchronous RAG execution</text>
    <text x="45" y="546" font-size="9" fill="#475569">• Ingests ChatRequest {message, filename?}</text>
    <text x="45" y="562" font-size="9" fill="#475569">• Checks FAISS index presence, falls back to general Gemini if missing</text>

    <rect x="30" y="585" width="400" height="85" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
    <text x="45" y="607" font-size="10.5" font-weight="bold" fill="#1e1b4b">/api/v1/embeddings (api/routes/embeddings.py)</text>
    <text x="45" y="625" font-size="9" fill="#475569">• POST /{filename}: schedules job on BackgroundTasks</text>
    <text x="45" y="641" font-size="9" fill="#475569">• GET /progress: stage 0-3 percent • POST /cancel: aborts job</text>
    <text x="45" y="657" font-size="9" fill="#475569">• GET /{filename}/status: checks 3 HDBSCAN artifact files</text>

    <rect x="30" y="680" width="400" height="85" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
    <text x="45" y="702" font-size="10.5" font-weight="bold" fill="#1e1b4b">/api/v1/analysis (api/routes/analysis.py)</text>
    <text x="45" y="720" font-size="9" fill="#475569">• POST /generate &amp; GET /{fn}/summary: AnalysisSummary artifacts</text>
    <text x="45" y="736" font-size="9" fill="#475569">• GET /{fn}/matrix: keyword presence matrix preview</text>
    <text x="45" y="752" font-size="9" fill="#475569">• GET /{fn}/country-collaboration &amp; GET /{fn}/countries: CountryService</text>

    <rect x="30" y="775" width="400" height="75" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
    <text x="45" y="797" font-size="10.5" font-weight="bold" fill="#1e1b4b">/api/v1/system &amp; /health</text>
    <text x="45" y="815" font-size="9" fill="#475569">• GET /system/status: queries model_manager without blocking</text>
    <text x="45" y="831" font-size="9" fill="#475569">• GET /health: root health verification check</text>
  </g>

  <!-- Middle: Pydantic Validation & Security -->
  <g transform="translate(535, 175)">
    <rect x="0" y="0" width="460" height="970" rx="14" fill="#fafafa" stroke="#a855f7" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="430" height="34" rx="6" fill="#f3e8ff"/>
    <text x="230" y="37" font-size="13" font-weight="bold" fill="#6b21a8" text-anchor="middle">VALIDATION, SECURITY &amp; EXCEPTIONS</text>

    <!-- Pydantic Validation Box -->
    <rect x="20" y="65" width="420" height="240" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="90" font-size="11.5" font-weight="bold" fill="#0f172a">3.4 Pydantic Schemas Engine (models/schemas.py)</text>
    <text x="35" y="110" font-size="9.5" fill="#475569">• SearchRequest: query string, keywords list, date range, sort_mode</text>
    <text x="35" y="126" font-size="9.5" fill="#475569">• ChatRequest: message text, filename binding</text>
    <text x="35" y="142" font-size="9.5" fill="#475569">• EmbeddingOptions: scrape_full_text bool, max_scrape, force rebuild</text>
    <text x="35" y="158" font-size="9.5" fill="#475569">• AnalysisRequest: filename, top_keywords (1-500), minimum_frequency</text>
    <text x="35" y="174" font-size="9.5" fill="#475569">• Response models: SearchResponse, ChatResponse, AnalysisSummary,</text>
    <text x="35" y="190" font-size="9.5" fill="#475569">  CountryCollaborationGraphResponse, CountryStatisticsResponse</text>

    <polygon points="230,220 340,245 230,270 120,245" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
    <text x="230" y="243" font-size="10" font-weight="bold" fill="#78350f" text-anchor="middle">Schema Valid?</text>
    <text x="230" y="255" font-size="8" fill="#92400e" text-anchor="middle">Type &amp; bounds check</text>

    <!-- Validation Failure -->
    <rect x="20" y="320" width="420" height="60" rx="8" fill="#fee2e2" stroke="#ef4444" stroke-width="1.2"/>
    <text x="35" y="342" font-size="10.5" font-weight="bold" fill="#991b1b">HTTP 422 Unprocessable Entity</text>
    <text x="35" y="360" font-size="9" fill="#b91c1c">FastAPI RequestValidationError returned with detail field errors</text>

    <!-- Security: SSRF Validation -->
    <rect x="20" y="395" width="420" height="155" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="420" font-size="11.5" font-weight="bold" fill="#0f172a">3.5 Security: SSRF Prevention (validate_safe_url)</text>
    <text x="35" y="440" font-size="9.5" fill="#475569">• Mandatory check before downloading external PDF links</text>
    <text x="35" y="456" font-size="9.5" fill="#475569">• Resolves DNS hostname to IP address via socket.getaddrinfo</text>
    <text x="35" y="472" font-size="9.5" fill="#475569">• Rejects private IP addresses: ipaddress.is_private</text>
    <text x="35" y="488" font-size="9.5" fill="#475569">• Rejects loopback addresses: ipaddress.is_loopback (127.0.0.1, ::1)</text>
    <text x="35" y="504" font-size="9.5" fill="#475569">• Rejects link-local and multicast networks</text>
    <text x="35" y="520" font-size="9.5" fill="#475569">• Enforces HTTP and HTTPS protocols exclusively</text>

    <!-- Centralized Exception Handling -->
    <rect x="20" y="565" width="420" height="235" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="590" font-size="11.5" font-weight="bold" fill="#0f172a">3.6 Centralized HTTP Error Code Mapping</text>

    <rect x="30" y="605" width="400" height="50" rx="6" fill="#fee2e2" stroke="#fca5a5" stroke-width="1"/>
    <text x="45" y="625" font-size="10" font-weight="bold" fill="#991b1b">HTTP 400 Bad Request</text>
    <text x="45" y="641" font-size="8.5" fill="#b91c1c">CSVLoadError, invalid file extension, SSRF violation, unreadable encoding</text>

    <rect x="30" y="665" width="400" height="50" rx="6" fill="#fee2e2" stroke="#fca5a5" stroke-width="1"/>
    <text x="45" y="685" font-size="10" font-weight="bold" fill="#991b1b">HTTP 404 Not Found</text>
    <text x="45" y="701" font-size="8.5" fill="#b91c1c">FileNotFoundError: Target CSV, summary JSON, or FAISS index missing in data/</text>

    <rect x="30" y="725" width="400" height="50" rx="6" fill="#fee2e2" stroke="#fca5a5" stroke-width="1"/>
    <text x="45" y="745" font-size="10" font-weight="bold" fill="#991b1b">HTTP 500 Internal Server Error</text>
    <text x="45" y="761" font-size="8.5" fill="#b91c1c">External service failure or unexpected exception with logger.error trace</text>
  </g>

  <!-- Right: Service Orchestration & Delegation -->
  <g transform="translate(1025, 175)">
    <rect x="0" y="0" width="680" height="970" rx="14" fill="#fafafa" stroke="#a855f7" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="650" height="34" rx="6" fill="#f3e8ff"/>
    <text x="340" y="37" font-size="13" font-weight="bold" fill="#6b21a8" text-anchor="middle">CONTROLLER-TO-SERVICE ORCHESTRATION PIPELINES</text>

    <!-- Delegation to Layer 4 -->
    <rect x="20" y="65" width="640" height="145" rx="8" fill="#ffffff" stroke="#0891b2" stroke-width="1.5"/>
    <rect x="25" y="70" width="630" height="26" rx="4" fill="#cffafe"/>
    <text x="340" y="87" font-size="11.5" font-weight="bold" fill="#155e75" text-anchor="middle">DELEGATION TO LAYER 4: DATA COLLECTION &amp; RETRIEVAL</text>
    <text x="35" y="115" font-size="9.5" fill="#0e7490">• SearchController delegates to SearchService.search_papers()</text>
    <text x="35" y="133" font-size="9.5" fill="#0e7490">• Triggers UnifiedSearchService to query NCBI PubMed &amp; OpenAlex in parallel</text>
    <text x="35" y="151" font-size="9.5" fill="#0e7490">• Handles cooperative cancellation via cancel_event threading.Event</text>
    <text x="35" y="169" font-size="9.5" fill="#0e7490">• Non-blocking fault tolerance: falls back to active provider if one service fails</text>

    <!-- Delegation to Layer 5 -->
    <rect x="20" y="225" width="640" height="145" rx="8" fill="#ffffff" stroke="#059669" stroke-width="1.5"/>
    <rect x="25" y="230" width="630" height="26" rx="4" fill="#d1fae5"/>
    <text x="340" y="247" font-size="11.5" font-weight="bold" fill="#065f46" text-anchor="middle">DELEGATION TO LAYER 5: DATA CLEANING &amp; ENRICHMENT</text>
    <text x="35" y="275" font-size="9.5" fill="#047857">• Multi-priority deduplication: DOI → PMID → OpenAlex ID → Title+Year+Author</text>
    <text x="35" y="293" font-size="9.5" fill="#047857">• Geographic entity recognition via country_extractor.py (700+ ISO aliases)</text>
    <text x="35" y="311" font-size="9.5" fill="#047857">• Affiliation fallback enrichment via pubmed_affiliation_enricher.py</text>
    <text x="35" y="329" font-size="9.5" fill="#047857">• Centralized CSV storage in data/*.csv via csv_loader.py (UTF-8-SIG)</text>

    <!-- Delegation to Layer 6 -->
    <rect x="20" y="385" width="640" height="185" rx="8" fill="#ffffff" stroke="#d97706" stroke-width="1.5"/>
    <rect x="25" y="390" width="630" height="26" rx="4" fill="#fef3c7"/>
    <text x="340" y="407" font-size="11.5" font-weight="bold" fill="#92400e" text-anchor="middle">DELEGATION TO LAYER 6: ANALYSIS &amp; COMPUTATION</text>
    <text x="35" y="435" font-size="9.5" fill="#b45309">• AnalysisController calls AnalysisService: keyword frequency, presence matrix,</text>
    <text x="35" y="451" font-size="9.5" fill="#b45309">  co-occurrence graph, and NetworkX centralities (5 metrics)</text>
    <text x="35" y="471" font-size="9.5" fill="#b45309">• Calls CountryService: country publication stats &amp; international co-authorship graph</text>
    <text x="35" y="491" font-size="9.5" fill="#b45309">• EmbeddingsController calls EmbeddingService: full-text scrape, HDBSCAN, FAISS Flat L2</text>
    <text x="35" y="511" font-size="9.5" fill="#b45309">• ChatController calls ChatService: Gemini query decomposition &amp; cited RAG answer</text>
    <text x="35" y="531" font-size="9.5" fill="#b45309">• MedCPT Neural Re-ranker: PyTorch bi-encoder semantic ranking (0-100 scores)</text>

    <!-- Response Generation -->
    <rect x="20" y="585" width="640" height="150" rx="8" fill="#f0fdf4" stroke="#10b981" stroke-width="1.8"/>
    <text x="40" y="612" font-size="12" font-weight="bold" fill="#065f46">3.7 Final HTTP Response Generation &amp; Serialization</text>
    <text x="40" y="632" font-size="9.5" fill="#047857">• Pydantic models automatically serialize to compliant JSON payloads</text>
    <text x="40" y="650" font-size="9.5" fill="#047857">• FileResponse streams raw dataset CSV files for client-side download</text>
    <text x="40" y="668" font-size="9.5" fill="#047857">• StreamingResponse proxies binary PDF paper documents with Content-Disposition</text>
    <text x="40" y="686" font-size="9.5" fill="#047857">• Structured HTTP status codes (200, 400, 404, 422, 500) transmitted to Layer 2</text>
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
    header = FancyBboxPatch((0.4, 10.8), 17.2, 0.9, boxstyle="round,pad=0,rounding_size=0.15",
                            facecolor="#7E22CE", edgecolor="#6B21A8", linewidth=1.5, zorder=2)
    ax.add_patch(header)
    ax.text(0.6, 11.45, "LAYER 03: BACKEND PROCESSING & CONTROLLER LAYER FLOWCHART", fontsize=15, fontweight='bold', color="#FFFFFF", zorder=3)
    ax.text(0.6, 11.08, "FastAPI Routing, Pydantic Validation, Controller Handlers, Security Boundaries & Exception Handling", fontsize=9.5, color="#F3E8FF", zorder=3)
    ax.text(17.4, 11.25, "Research Rover v2.0", fontsize=10, fontweight='bold', color="#D8B4FE", ha='right', zorder=3)

    # Column 1: ASGI Server & Routing Gateway
    col1 = FancyBboxPatch((0.5, 0.5), 5.2, 10.0, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#A855F7", linewidth=1.5, zorder=2)
    ax.add_patch(col1)
    ax.text(3.1, 10.2, "ASGI SERVER & ROUTING GATEWAY", fontsize=11, fontweight='bold', color="#6B21A8", ha='center', zorder=3)
    ax.text(3.1, 9.5, "3.1 Uvicorn Server (0.0.0.0:8000)\nFastAPI Application Instance\nLifespan Context Manager (model init)\nCORS Middleware (allow all origins)", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    ax.text(3.1, 8.2, "[Mounted Router Controllers]\n• /api/v1/search (routes/search.py)\n  POST /, GET /progress, POST /cancel, GET /results\n• /api/v1/files (routes/files.py)\n  POST /upload, GET /download/{fn}, GET /download-pdf\n• /api/v1/chat (routes/chat.py)\n  POST /{fn}, POST / (RAG completions)\n• /api/v1/embeddings (routes/embeddings.py)\n  POST /{fn}, GET /progress, GET /status\n• /api/v1/analysis (routes/analysis.py)\n  POST /generate, GET /summary, GET /matrix\n• /api/v1/system & /health\n  GET /system/status, GET /health", fontsize=8, color="#3B0764", ha='center', zorder=3)

    # Column 2: Validation, Security & Exceptions
    col2 = FancyBboxPatch((6.0, 0.5), 5.2, 10.0, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#A855F7", linewidth=1.5, zorder=2)
    ax.add_patch(col2)
    ax.text(8.6, 10.2, "VALIDATION, SECURITY & EXCEPTIONS", fontsize=11, fontweight='bold', color="#6B21A8", ha='center', zorder=3)

    ax.text(8.6, 9.4, "3.4 Pydantic Schemas Engine (schemas.py)\nValidates SearchRequest, ChatRequest,\nAnalysisRequest, EmbeddingOptions\nIf invalid → HTTP 422 Unprocessable Entity", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    ax.text(8.6, 7.6, "3.5 Security: SSRF Prevention (validate_safe_url)\nDNS resolution via socket.getaddrinfo\n• Rejects ipaddress.is_private\n• Rejects ipaddress.is_loopback (127.0.0.1)\n• Rejects link-local & multicast\n• Allows only HTTP/HTTPS protocols", fontsize=8.5, color="#78350F", ha='center', zorder=3)

    ax.text(8.6, 5.2, "3.6 Exception Code Mapping\n• HTTP 400 Bad Request:\n  CSVLoadError, invalid file extension,\n  SSRF violation, unreadable encoding\n• HTTP 404 Not Found:\n  FileNotFoundError (missing CSV or FAISS index)\n• HTTP 500 Internal Server Error:\n  External service crash, logged via logger.error", fontsize=8.5, color="#991B1B", ha='center', zorder=3)

    # Column 3: Delegation & Services
    col3 = FancyBboxPatch((11.5, 0.5), 6.0, 10.0, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#A855F7", linewidth=1.5, zorder=2)
    ax.add_patch(col3)
    ax.text(14.5, 10.2, "SERVICE ORCHESTRATION PIPELINES", fontsize=11, fontweight='bold', color="#6B21A8", ha='center', zorder=3)

    ax.text(14.5, 9.3, "[Delegation to Layer 4: Data Collection]\nSearchService & UnifiedSearchService\nQueries NCBI PubMed & OpenAlex in parallel\nHandles cooperative task cancellation", fontsize=8.5, color="#0E7490", ha='center', zorder=3)

    ax.text(14.5, 7.5, "[Delegation to Layer 5: Data Cleaning]\nDeduplication (DOI, PMID, OpenAlex ID, Title key)\nCountry extraction via country_extractor.py (700+ aliases)\nCentralized CSV storage in data/*.csv (UTF-8-SIG)", fontsize=8.5, color="#047857", ha='center', zorder=3)

    ax.text(14.5, 5.4, "[Delegation to Layer 6: Analysis Engine]\nAnalysisService: Keyword frequency, matrix, NetworkX\nCountryService: Country statistics & 2D/3D collab graph\nEmbeddingService: Full-text scrape + HDBSCAN + FAISS\nChatService: Gemini query decomposition & RAG\nMedCPT: PyTorch bi-encoder semantic re-ranking", fontsize=8.5, color="#B45309", ha='center', zorder=3)

    ax.text(14.5, 2.6, "3.7 HTTP Response Generation\nPydantic JSONResponse serialization\nFileResponse for CSV dataset downloads\nStreamingResponse for binary PDF proxy streams\nTransmitted to Layer 2: Frontend Client", fontsize=8.5, fontweight='bold', color="#065F46", ha='center', zorder=3)

    plt.tight_layout()
    plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated PNG: {png_path}")
