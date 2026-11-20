"""
Layer 2: Frontend / API Client Layer
Covers React 19 SPA hierarchy, context state management, user event dispatching,
Axios API client wrappers, HTTP request construction, endpoint mapping, response interceptors,
loading/error states, and context data synchronization.
"""

from .common import THEMES, get_svg_header, get_svg_footer
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

def get_mermaid():
    return """flowchart TD
    %% =========================================================================
    %% LAYER 2: FRONTEND / API CLIENT LAYER
    %% Project: Research Rover
    %% Focus: React Context Architecture, Axios Client, Typed Wrappers, State Synchronization
    %% =========================================================================

    classDef startEnd fill:#EEF2FF,stroke:#4F46E5,stroke-width:2.5px,color:#312E81,font-weight:bold;
    classDef comp fill:#F8FAFC,stroke:#6366F1,stroke-width:1.5px,color:#0F172A;
    classDef context fill:#E0E7FF,stroke:#4338CA,stroke-width:1.5px,color:#1E1B4B,font-weight:bold;
    classDef apiCore fill:#FDF4FF,stroke:#C026D3,stroke-width:2px,color:#701A75,font-weight:bold;
    classDef decision fill:#FEF3C7,stroke:#D97706,stroke-width:2px,color:#78350F,font-weight:bold;
    classDef endpoint fill:#ECFEFF,stroke:#0891B2,stroke-width:1.5px,color:#164E63;
    classDef errorState fill:#FEE2E2,stroke:#EF4444,stroke-width:1.5px,color:#991B1B;
    classDef output fill:#ECFDF5,stroke:#10B981,stroke-width:2px,color:#064E3B;

    F_ENTRY(["2.0 Entry: User Actions & Component Mounts<br/>(Received from Layer 1: User Interaction Layer)"]):::startEnd

    %% ─── COMPONENT HIERARCHY ────────────────────────────────────────────────
    subgraph SUB_FRONTEND["REACT 19 SPA & COMPONENT HIERARCHY (frontend/src)"]
        APP_ROOT["2.1 App Root & Router Setup<br/>(App.tsx & main.tsx with React Router DOM v7)"]:::comp
        
        subgraph SUB_CONTEXTS["Global State Management: Context Providers Stack"]
            CTX_THEME["ThemeProvider (Theme state: light | dark | system)"]:::context
            CTX_STATUS["SystemStatusProvider (Polls /system/status every 30s)"]:::context
            CTX_SIDEBAR["SidebarProvider (Mobile drawer & sidebar collapse)"]:::context
            CTX_SEARCH["SearchProvider (Query, filters, results, polling loop)"]:::context
            CTX_EMBED["EmbeddingProvider (App-wide embedding job, percent, modal)"]:::context
            CTX_CHAT["ChatProvider (Chat history, sources, selectedFile sync)"]:::context
            CTX_ANALYTICS["AnalyticsProvider (Selected file, paperCache, summary, matrix)"]:::context
        end

        subgraph SUB_PAGES["Page Views & UI Layout Components"]
            PAGE_SEARCH["SearchPage.tsx (Query form, filters slider, results catalog)"]:::comp
            PAGE_ANALYTICS["AnalyticsPage.tsx (Keywords & Country tabs, word cloud, exports)"]:::comp
            PAGE_CHAT["ChatPage.tsx (Interactive RAG messages, source cards, status)"]:::comp
            PAGE_ARCH["ArchitecturePage.tsx (Interactive viewer & component inventory)"]:::comp
            PAGE_SETTINGS["SettingsPage.tsx (Theme toggles & runtime options)"]:::comp
            COMP_COUNTRY["CountryAnalysisView.tsx (WorldMap, 2D/3D collaboration networks)"]:::comp
            COMP_LOADER["ResearchRoverLoader.tsx (Animated multi-stage progress feedback)"]:::comp
            COMP_MODAL["EmbeddingProgressModal.tsx (HDBSCAN vector build dialog)"]:::comp
            COMP_ERR["ErrorBoundary.tsx (Catches WebGL & render crashes)"]:::comp
        end
    end

    %% ─── USER EVENT HANDLING ────────────────────────────────────────────────
    subgraph SUB_EVENTS["USER EVENT DISPATCHING & FORM BINDING"]
        EV_SEARCH["handleSearch() → Validates keywords, resets results, sets isLoading"]:::comp
        EV_POLL["pollProgress() → 1000ms recurring timer while status === 'searching'"]:::comp
        EV_CANCEL["handleCancel() → Calls cancel endpoint, sets cancelled status"]:::comp
        EV_UPLOAD["handleFileUpload(file) → Constructs multipart FormData"]:::comp
        EV_ANALYTICS["handleGenerateAnalytics() → Triggers summary, matrix, or country graph"]:::comp
        EV_CHAT["handleSendMessage(text) → Appends user message, initiates RAG query"]:::comp
        EV_EMBED["handleStartEmbeddings() → Triggers background HDBSCAN vector job"]:::comp
        EV_PDF["handleDownloadPdf(url) → Initiates secure blob stream download"]:::comp
    end

    %% ─── AXIOS API CLIENT ───────────────────────────────────────────────────
    subgraph SUB_API_CLIENT["AXIOS API CLIENT CORE (frontend/src/services/api.ts)"]
        AXIOS_CORE["2.2 Axios Core Instance<br/>Base URL: /api/v1 (or VITE_API_BASE_URL)<br/>Timeout: 120,000 ms • Content-Type: application/json"]:::apiCore
        REQ_INTERCEPT["2.3 Request Interceptor<br/>Injects headers & client telemetry"]:::comp
        RESP_INTERCEPT{"2.4 Response Interceptor<br/>Inspect HTTP Status & Payload Format"}:::decision
        ERR_NORMALIZER["2.5 Error Normalizer & Blob Decoder<br/>Extracts nested JSON error from Blob responses<br/>Constructs ApiError {error, detail, code}"]:::errorState
    end

    %% ─── TYPED API WRAPPERS ─────────────────────────────────────────────────
    subgraph SUB_WRAPPERS["TYPED API WRAPPERS & PAYLOAD CONSTRUCTORS"]
        API_SEARCH["searchApi<br/>• search(SearchRequest): POST /search/<br/>• getProgress(): GET /search/progress<br/>• cancel(): POST /search/cancel<br/>• getResults(p, n): GET /search/results"]:::endpoint
        API_FILES["filesApi<br/>• upload(FormData): POST /files/upload<br/>• download(name): GET /files/download/{fn}<br/>• downloadPdf(url): GET /files/download-pdf<br/>• getCsvData(name): GET /files/csv/{fn}/data<br/>• list(): GET /files/list • delete(): DELETE /{fn}"]:::endpoint
        API_CHAT["chatApi<br/>• sendMessageBody(ChatRequest): POST /chat/<br/>• sendMessage(fn, req): POST /chat/{fn}"]:::endpoint
        API_EMBED["embeddingsApi<br/>• create(fn, opts): POST /embeddings/{fn}<br/>• getProgress(): GET /embeddings/progress<br/>• cancel(): POST /embeddings/cancel<br/>• getStatus(fn): GET /embeddings/{fn}/status"]:::endpoint
        API_ANALYSIS["analysisApi<br/>• listFiles(): GET /analysis/files<br/>• generate(req): POST /analysis/generate<br/>• getSummary(fn): GET /analysis/{fn}/summary<br/>• getMatrix(fn): GET /analysis/{fn}/matrix<br/>• getCountryCollaboration(fn): GET ...<br/>• getCountryStatistics(fn): GET ..."]:::endpoint
        API_SYSTEM["systemApi & healthApi<br/>• getStatus(signal): GET /system/status<br/>• check(): GET /health"]:::endpoint
    end

    %% ─── STATE SYNCHRONIZATION ──────────────────────────────────────────────
    subgraph SUB_STATE_SYNC["CLIENT STATE SYNCHRONIZATION & TOAST FEEDBACK"]
        SYNC_SEARCH["Update SearchContext<br/>allResults: Paper[], csvFilename, displayedResults"]:::output
        SYNC_ANALYTICS["Update AnalyticsContext<br/>summary, matrix, countryData, paperCache Map"]:::output
        SYNC_CHAT["Update ChatContext<br/>messages: ChatMessage[], sources cards, completedFile"]:::output
        SYNC_EMBED["Update EmbeddingContext<br/>currentJob, isEmbedding, percent progress"]:::output
        SYNC_TOAST["Sonner Toast Notifications<br/>toast.success() | toast.error()"]:::comp
    end

    F_OUT(["2.6 Exit: Transmit HTTP Payloads to Layer 3 (Backend Processing & Controller Layer)"]):::startEnd

    %% Connections
    F_ENTRY --> APP_ROOT --> SUB_CONTEXTS
    SUB_CONTEXTS --> SUB_PAGES
    SUB_PAGES --> SUB_EVENTS
    SUB_EVENTS --> SUB_WRAPPERS

    SUB_WRAPPERS --> AXIOS_CORE --> REQ_INTERCEPT --> F_OUT
    F_OUT -.->|HTTP Responses Returned| RESP_INTERCEPT

    RESP_INTERCEPT -->|Success: HTTP 200| SUB_STATE_SYNC
    RESP_INTERCEPT -->|Failure: HTTP 400/404/500| ERR_NORMALIZER --> SYNC_TOAST
"""

def get_svg():
    w, h = 1750, 1250
    header = get_svg_header(
        w, h,
        title="Layer 2: Frontend & API Client Layer Flowchart",
        subtitle="React 19 Context Hierarchy, Component Event Dispatchers, Axios Client Engine, and State Synchronization",
        layer_badge="LAYER 02",
        theme_key="layer_02"
    )

    content = '''
  <!-- Inter-layer Connectivity Cards -->
  <g transform="translate(45, 115)">
    <rect x="0" y="0" width="380" height="42" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="15" y="26" font-size="12" font-weight="bold" fill="#1e40af">INPUT SOURCE:</text>
    <text x="120" y="26" font-size="12" fill="#334155">Layer 1: User Actions, Clicks, and Inputs</text>
  </g>
  <g transform="translate(1325, 115)">
    <rect x="0" y="0" width="380" height="42" rx="8" fill="#faf5ff" stroke="#a855f7" stroke-width="1.5"/>
    <text x="15" y="26" font-size="12" font-weight="bold" fill="#6b21a8">OUTPUT TARGET:</text>
    <text x="130" y="26" font-size="12" fill="#334155">Layer 3 (Backend Processing &amp; Controllers)</text>
  </g>

  <!-- Left: React 19 Component & Context Tree -->
  <g transform="translate(45, 175)">
    <rect x="0" y="0" width="480" height="970" rx="14" fill="#fafafa" stroke="#6366f1" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="450" height="34" rx="6" fill="#e0e7ff"/>
    <text x="240" y="37" font-size="13" font-weight="bold" fill="#3730a3" text-anchor="middle">REACT 19 SPA &amp; CONTEXT HIERARCHY</text>

    <!-- App Root -->
    <rect x="20" y="65" width="440" height="52" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="240" y="87" font-size="12" font-weight="bold" fill="#0f172a" text-anchor="middle">2.1 App Root &amp; Routing Gateway (App.tsx)</text>
    <text x="240" y="103" font-size="10" fill="#64748b" text-anchor="middle">React Router DOM v7 client-side routing (/ , /search, /analytics, /chat)</text>
    <line x1="240" y1="117" x2="240" y2="135" stroke="#6366f1" stroke-width="1.8" marker-end="url(#arrow)"/>

    <!-- Context Providers Stack -->
    <rect x="20" y="135" width="440" height="320" rx="10" fill="#f8fafc" stroke="#c7d2fe" stroke-width="1.5"/>
    <rect x="30" y="145" width="420" height="26" rx="4" fill="#e0e7ff"/>
    <text x="240" y="162" font-size="11" font-weight="bold" fill="#312e81" text-anchor="middle">Context Providers Stack (Persists Across Page Navigation)</text>

    <text x="35" y="195" font-size="10" font-weight="bold" fill="#1e1b4b">• ThemeProvider: Light / Dark / System theme state</text>
    <text x="35" y="225" font-size="10" font-weight="bold" fill="#1e1b4b">• SystemStatusProvider: 30s polling of API &amp; Model health (/system/status)</text>
    <text x="35" y="255" font-size="10" font-weight="bold" fill="#1e1b4b">• SidebarProvider: Responsive navigation drawer &amp; collapsed state</text>
    <text x="35" y="285" font-size="10" font-weight="bold" fill="#1e1b4b">• SearchProvider: Active query, year bounds, paper results, polling loop</text>
    <text x="35" y="315" font-size="10" font-weight="bold" fill="#1e1b4b">• EmbeddingProvider: Single active vector job, percentage, cancel handler</text>
    <text x="35" y="345" font-size="10" font-weight="bold" fill="#1e1b4b">• ChatProvider: Conversational messages, citation cards, auto-file select</text>
    <text x="35" y="375" font-size="10" font-weight="bold" fill="#1e1b4b">• AnalyticsProvider: Dataset source, summary/matrix cache, paperCache Map</text>
    <text x="35" y="405" font-size="10" font-weight="bold" fill="#1e1b4b">• Layout Shell: Navbar.tsx, Sidebar.tsx, Footer.tsx</text>

    <line x1="240" y1="455" x2="240" y2="475" stroke="#6366f1" stroke-width="1.8" marker-end="url(#arrow)"/>

    <!-- UI Pages & Views -->
    <rect x="20" y="475" width="440" height="470" rx="10" fill="#ffffff" stroke="#c7d2fe" stroke-width="1.5"/>
    <rect x="30" y="485" width="420" height="26" rx="4" fill="#e0e7ff"/>
    <text x="240" y="502" font-size="11" font-weight="bold" fill="#312e81" text-anchor="middle">Active Pages &amp; Specialized Presentation Components</text>

    <text x="35" y="535" font-size="10" font-weight="bold" fill="#0f172a">SearchPage.tsx</text>
    <text x="45" y="550" font-size="9" fill="#475569">Topic input form, date pickers, year slider, client-side pagination</text>

    <text x="35" y="580" font-size="10" font-weight="bold" fill="#0f172a">AnalyticsPage.tsx</text>
    <text x="45" y="595" font-size="9" fill="#475569">Keywords tab, SVG word cloud, NetworkX table, binary matrix grid</text>

    <text x="35" y="625" font-size="10" font-weight="bold" fill="#0f172a">CountryAnalysisView.tsx</text>
    <text x="45" y="640" font-size="9" fill="#475569">WorldMap.tsx, CountryCollaboration2D.tsx, CountryCollaboration3D.tsx</text>

    <text x="35" y="670" font-size="10" font-weight="bold" fill="#0f172a">ChatPage.tsx</text>
    <text x="45" y="685" font-size="9" fill="#475569">Conversational RAG feed, superscript citation badges, collapsible source cards</text>

    <text x="35" y="715" font-size="10" font-weight="bold" fill="#0f172a">ArchitecturePage.tsx &amp; UseCasesPage.tsx</text>
    <text x="45" y="730" font-size="9" fill="#475569">Interactive architecture viewer, component inventory, UML use cases</text>

    <text x="35" y="760" font-size="10" font-weight="bold" fill="#0f172a">EmbeddingProgressModal.tsx &amp; ResearchRoverLoader.tsx</text>
    <text x="45" y="775" font-size="9" fill="#475569">Real-time progress feedback, multi-stage loaders, cancel action</text>

    <text x="35" y="805" font-size="10" font-weight="bold" fill="#0f172a">ErrorBoundary.tsx</text>
    <text x="45" y="820" font-size="9" fill="#475569">Catches 3D Three.js / WebGL / canvas crashes without breaking the app</text>
  </g>

  <!-- Middle: User Event Dispatchers & Handlers -->
  <g transform="translate(555, 175)">
    <rect x="0" y="0" width="370" height="970" rx="14" fill="#fafafa" stroke="#6366f1" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="340" height="34" rx="6" fill="#e0e7ff"/>
    <text x="185" y="37" font-size="13" font-weight="bold" fill="#3730a3" text-anchor="middle">EVENT DISPATCHING &amp; BINDING</text>

    <rect x="15" y="65" width="340" height="90" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="25" y="88" font-size="11" font-weight="bold" fill="#1e1b4b">handleSearch(request)</text>
    <text x="25" y="105" font-size="9" fill="#475569">• Validates query or keyword list</text>
    <text x="25" y="120" font-size="9" fill="#475569">• Sets isLoading: true, stage: 0</text>
    <text x="25" y="135" font-size="9" fill="#475569">• Invokes searchApi.search(request)</text>

    <rect x="15" y="170" width="340" height="90" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="25" y="193" font-size="11" font-weight="bold" fill="#1e1b4b">pollSearchProgress()</text>
    <text x="25" y="210" font-size="9" fill="#475569">• 1000ms recurring setInterval timer</text>
    <text x="25" y="225" font-size="9" fill="#475569">• Calls searchApi.getProgress()</text>
    <text x="25" y="240" font-size="9" fill="#475569">• On completed: fetches searchApi.getResults()</text>

    <rect x="15" y="275" width="340" height="90" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="25" y="298" font-size="11" font-weight="bold" fill="#1e1b4b">handleCancelSearch()</text>
    <text x="25" y="315" font-size="9" fill="#475569">• Invokes searchApi.cancel()</text>
    <text x="25" y="330" font-size="9" fill="#475569">• Sets status to 'cancelled'</text>
    <text x="25" y="345" font-size="9" fill="#475569">• Clears active polling timer</text>

    <rect x="15" y="380" width="340" height="90" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="25" y="403" font-size="11" font-weight="bold" fill="#1e1b4b">handleFileUpload(file)</text>
    <text x="25" y="420" font-size="9" fill="#475569">• Checks .csv extension</text>
    <text x="25" y="435" font-size="9" fill="#475569">• Packs into FormData(file)</text>
    <text x="25" y="450" font-size="9" fill="#475569">• Invokes filesApi.upload(formData)</text>

    <rect x="15" y="485" width="340" height="90" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="25" y="508" font-size="11" font-weight="bold" fill="#1e1b4b">handleFetchAnalytics(filename)</text>
    <text x="25" y="525" font-size="9" fill="#475569">• Checks paperCache Map</text>
    <text x="25" y="540" font-size="9" fill="#475569">• Calls analysisApi.getCountryCollaboration()</text>
    <text x="25" y="555" font-size="9" fill="#475569">• Calls analysisApi.getSummary() or getMatrix()</text>

    <rect x="15" y="590" width="340" height="90" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="25" y="613" font-size="11" font-weight="bold" fill="#1e1b4b">handleSendMessage(text)</text>
    <text x="25" y="630" font-size="9" fill="#475569">• Appends user message to state</text>
    <text x="25" y="645" font-size="9" fill="#475569">• Calls chatApi.sendMessageBody({msg, fn})</text>
    <text x="25" y="660" font-size="9" fill="#475569">• Renders Markdown answer &amp; source cards</text>

    <rect x="15" y="695" width="340" height="90" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="25" y="718" font-size="11" font-weight="bold" fill="#1e1b4b">handleStartEmbeddings(fn)</text>
    <text x="25" y="735" font-size="9" fill="#475569">• Calls embeddingsApi.create(fn, options)</text>
    <text x="25" y="750" font-size="9" fill="#475569">• Starts 1s progress polling loop</text>
    <text x="25" y="765" font-size="9" fill="#475569">• Opens EmbeddingProgressModal dialog</text>

    <rect x="15" y="800" width="340" height="90" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="25" y="823" font-size="11" font-weight="bold" fill="#1e1b4b">handleDownloadPdf(url, title)</text>
    <text x="25" y="840" font-size="9" fill="#475569">• Calls filesApi.downloadPdf(params)</text>
    <text x="25" y="855" font-size="9" fill="#475569">• Receives blob stream &amp; parses filename</text>
    <text x="25" y="870" font-size="9" fill="#475569">• Triggers browser save dialog</text>
  </g>

  <!-- Right: Axios Client Core & Typed Service Modules -->
  <g transform="translate(955, 175)">
    <rect x="0" y="0" width="750" height="970" rx="14" fill="#fafafa" stroke="#6366f1" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="720" height="34" rx="6" fill="#e0e7ff"/>
    <text x="375" y="37" font-size="13" font-weight="bold" fill="#3730a3" text-anchor="middle">AXIOS API CLIENT ENGINE &amp; TYPED SERVICE WRAPPERS (services/api.ts)</text>

    <!-- Axios Core Box -->
    <rect x="20" y="65" width="710" height="95" rx="10" fill="#fdf4ff" stroke="#c026d3" stroke-width="1.8"/>
    <text x="40" y="92" font-size="12" font-weight="bold" fill="#701a75">2.2 Axios Singleton Client Configuration</text>
    <text x="40" y="112" font-size="10" fill="#4a044e">• Base URL: resolved via import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'</text>
    <text x="40" y="128" font-size="10" fill="#4a044e">• Timeout: 120,000 ms (2 minutes for deep RAG &amp; heavy embedding queries)</text>
    <text x="40" y="144" font-size="10" fill="#4a044e">• Request Interceptor: headers injection • Response Interceptor: nested Blob error decoder</text>

    <!-- 6 Typed Service Modules -->
    <!-- searchApi -->
    <rect x="20" y="175" width="345" height="135" rx="8" fill="#ffffff" stroke="#0891b2" stroke-width="1.2"/>
    <rect x="25" y="180" width="335" height="24" rx="4" fill="#cffafe"/>
    <text x="192" y="196" font-size="11" font-weight="bold" fill="#155e75" text-anchor="middle">searchApi (async / poll-based)</text>
    <text x="35" y="222" font-size="9" fill="#0e7490"><b>POST /api/v1/search/</b> → {status: 'searching'}</text>
    <text x="35" y="242" font-size="9" fill="#0e7490"><b>GET /api/v1/search/progress</b> → SearchProgress</text>
    <text x="35" y="262" font-size="9" fill="#0e7490"><b>POST /api/v1/search/cancel</b> → {cancelled: true}</text>
    <text x="35" y="282" font-size="9" fill="#0e7490"><b>GET /api/v1/search/results</b> → SearchResponse</text>

    <!-- filesApi -->
    <rect x="385" y="175" width="345" height="135" rx="8" fill="#ffffff" stroke="#0891b2" stroke-width="1.2"/>
    <rect x="390" y="180" width="335" height="24" rx="4" fill="#cffafe"/>
    <text x="557" y="196" font-size="11" font-weight="bold" fill="#155e75" text-anchor="middle">filesApi (File &amp; PDF Management)</text>
    <text x="400" y="222" font-size="9" fill="#0e7490"><b>POST /api/v1/files/upload</b> → {message, filename}</text>
    <text x="400" y="242" font-size="9" fill="#0e7490"><b>GET /api/v1/files/download/{fn}</b> → Blob stream</text>
    <text x="400" y="262" font-size="9" fill="#0e7490"><b>GET /api/v1/files/download-pdf</b> → SSRF-safe PDF</text>
    <text x="400" y="282" font-size="9" fill="#0e7490"><b>GET /api/v1/files/csv/{fn}/data</b> → Paper[]</text>

    <!-- chatApi -->
    <rect x="20" y="325" width="345" height="135" rx="8" fill="#ffffff" stroke="#0891b2" stroke-width="1.2"/>
    <rect x="25" y="330" width="335" height="24" rx="4" fill="#cffafe"/>
    <text x="192" y="346" font-size="11" font-weight="bold" fill="#155e75" text-anchor="middle">chatApi (Conversational RAG)</text>
    <text x="35" y="372" font-size="9" fill="#0e7490"><b>POST /api/v1/chat/{fn}</b> (filename in path)</text>
    <text x="35" y="392" font-size="9" fill="#0e7490"><b>POST /api/v1/chat/</b> (filename in JSON body)</text>
    <text x="35" y="412" font-size="9" fill="#0e7490">Body: {message: string, filename?: string}</text>
    <text x="35" y="432" font-size="9" fill="#0e7490">Response: ChatResponse {response, sources[]}</text>

    <!-- embeddingsApi -->
    <rect x="385" y="325" width="345" height="135" rx="8" fill="#ffffff" stroke="#0891b2" stroke-width="1.2"/>
    <rect x="390" y="330" width="335" height="24" rx="4" fill="#cffafe"/>
    <text x="557" y="346" font-size="11" font-weight="bold" fill="#155e75" text-anchor="middle">embeddingsApi (FAISS Indexing)</text>
    <text x="400" y="372" font-size="9" fill="#0e7490"><b>POST /api/v1/embeddings/{fn}</b> → {message}</text>
    <text x="400" y="392" font-size="9" fill="#0e7490"><b>GET /api/v1/embeddings/progress</b> → percent %</text>
    <text x="400" y="412" font-size="9" fill="#0e7490"><b>POST /api/v1/embeddings/cancel</b> → abort job</text>
    <text x="400" y="432" font-size="9" fill="#0e7490"><b>GET /api/v1/embeddings/{fn}/status</b> → check files</text>

    <!-- analysisApi -->
    <rect x="20" y="475" width="345" height="155" rx="8" fill="#ffffff" stroke="#0891b2" stroke-width="1.2"/>
    <rect x="25" y="480" width="335" height="24" rx="4" fill="#cffafe"/>
    <text x="192" y="496" font-size="11" font-weight="bold" fill="#155e75" text-anchor="middle">analysisApi (Bibliometrics &amp; Networks)</text>
    <text x="35" y="522" font-size="9" fill="#0e7490"><b>GET /api/v1/analysis/files</b> → CSV sources</text>
    <text x="35" y="542" font-size="9" fill="#0e7490"><b>POST /api/v1/analysis/generate</b> → summary</text>
    <text x="35" y="562" font-size="9" fill="#0e7490"><b>GET /api/v1/analysis/{fn}/summary</b></text>
    <text x="35" y="582" font-size="9" fill="#0e7490"><b>GET /api/v1/analysis/{fn}/country-collaboration</b></text>
    <text x="35" y="602" font-size="9" fill="#0e7490"><b>GET /api/v1/analysis/{fn}/countries</b></text>

    <!-- systemApi -->
    <rect x="385" y="475" width="345" height="155" rx="8" fill="#ffffff" stroke="#0891b2" stroke-width="1.2"/>
    <rect x="390" y="480" width="335" height="24" rx="4" fill="#cffafe"/>
    <text x="557" y="496" font-size="11" font-weight="bold" fill="#155e75" text-anchor="middle">systemApi &amp; healthApi (Health &amp; Models)</text>
    <text x="400" y="522" font-size="9" fill="#0e7490"><b>GET /api/v1/system/status</b> → SystemStatus</text>
    <text x="400" y="542" font-size="9" fill="#0e7490">• Checks API: 'online' • Models: 'ready'</text>
    <text x="400" y="562" font-size="9" fill="#0e7490">• Reports Gemini, MedCPT, &amp; MPNet state</text>
    <text x="400" y="582" font-size="9" fill="#0e7490"><b>GET /health</b> → Root application health</text>
    <text x="400" y="602" font-size="9" fill="#0e7490">• Safe non-blocking query</text>

    <!-- State Sync and Output Box -->
    <rect x="20" y="650" width="710" height="135" rx="10" fill="#f0fdf4" stroke="#10b981" stroke-width="1.8"/>
    <text x="40" y="675" font-size="12" font-weight="bold" fill="#065f46">2.6 State Synchronization &amp; UI Feedback</text>
    <text x="40" y="695" font-size="9.5" fill="#047857">• Successful responses update Context hooks: SearchContext, AnalyticsContext, ChatContext</text>
    <text x="40" y="713" font-size="9.5" fill="#047857">• Cached paper datasets in paperCache Map prevent redundant network requests</text>
    <text x="40" y="731" font-size="9.5" fill="#047857">• ErrorInterceptor catches HTTP 400/404/500 → surfaces toast.error(detail) alerts via Sonner</text>
    <text x="40" y="749" font-size="9.5" fill="#047857">• Outgoing requests serialized into HTTP specifications dispatched to Layer 3</text>
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
                            facecolor="#4338CA", edgecolor="#3730A3", linewidth=1.5, zorder=2)
    ax.add_patch(header)
    ax.text(0.6, 11.45, "LAYER 02: FRONTEND / API CLIENT LAYER FLOWCHART", fontsize=15, fontweight='bold', color="#FFFFFF", zorder=3)
    ax.text(0.6, 11.08, "React 19 Context Hierarchy, Component Event Dispatchers, Axios Client Engine, and State Synchronization", fontsize=9.5, color="#E0E7FF", zorder=3)
    ax.text(17.4, 11.25, "Research Rover v2.0", fontsize=10, fontweight='bold', color="#A5B4FC", ha='right', zorder=3)

    # Column 1: React 19 SPA & Context Stack
    col1 = FancyBboxPatch((0.5, 0.5), 5.2, 10.0, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#6366F1", linewidth=1.5, zorder=2)
    ax.add_patch(col1)
    ax.text(3.1, 10.2, "REACT 19 SPA & CONTEXT STACK", fontsize=11, fontweight='bold', color="#3730A3", ha='center', zorder=3)
    ax.text(3.1, 9.6, "2.1 App Root & Routing Gateway\nApp.tsx + main.tsx (React Router DOM v7)", fontsize=9, fontweight='bold', color="#0F172A", ha='center', zorder=3)

    ax.text(3.1, 8.8, "[Context Providers Hierarchy]\n• ThemeProvider: light / dark / system\n• SystemStatusProvider: 30s status polling\n• SidebarProvider: drawer & responsive toggle\n• SearchProvider: query, results, 1s polling\n• EmbeddingProvider: single active job\n• ChatProvider: history & source cards\n• AnalyticsProvider: CSV source & cache", fontsize=8.5, color="#312E81", ha='center', zorder=3)

    ax.text(3.1, 5.2, "[Presentation Pages & Components]\n• SearchPage.tsx (filters, query, results catalog)\n• AnalyticsPage.tsx (word cloud, NetworkX table)\n• CountryAnalysisView.tsx (WorldMap, 2D/3D nets)\n• ChatPage.tsx (RAG chat feed, citations)\n• ArchitecturePage.tsx (interactive viewer)\n• EmbeddingProgressModal.tsx (HDBSCAN dialog)\n• ResearchRoverLoader.tsx (stage loader)\n• ErrorBoundary.tsx (WebGL crash catcher)", fontsize=8.5, color="#334155", ha='center', zorder=3)

    # Column 2: Event Dispatchers
    col2 = FancyBboxPatch((6.0, 0.5), 4.4, 10.0, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#6366F1", linewidth=1.5, zorder=2)
    ax.add_patch(col2)
    ax.text(8.2, 10.2, "EVENT DISPATCHERS & HANDLERS", fontsize=11, fontweight='bold', color="#3730A3", ha='center', zorder=3)
    ax.text(8.2, 9.5, "handleSearch(request)\nValidates query, sets isLoading, dispatches", fontsize=8.5, color="#0F172A", ha='center', zorder=3)
    ax.text(8.2, 8.4, "pollSearchProgress()\n1s interval timer, polls /search/progress", fontsize=8.5, color="#0F172A", ha='center', zorder=3)
    ax.text(8.2, 7.3, "handleCancelSearch()\nCalls /search/cancel, cooperative abort", fontsize=8.5, color="#0F172A", ha='center', zorder=3)
    ax.text(8.2, 6.2, "handleFileUpload(file)\nBuilds FormData, checks CSV extension", fontsize=8.5, color="#0F172A", ha='center', zorder=3)
    ax.text(8.2, 5.1, "handleFetchAnalytics(fn)\nLoads country collab, stats & summary", fontsize=8.5, color="#0F172A", ha='center', zorder=3)
    ax.text(8.2, 4.0, "handleSendMessage(text)\nDispatches /chat/, renders citations", fontsize=8.5, color="#0F172A", ha='center', zorder=3)
    ax.text(8.2, 2.9, "handleStartEmbeddings(fn)\nCalls /embeddings/{fn}, opens modal", fontsize=8.5, color="#0F172A", ha='center', zorder=3)
    ax.text(8.2, 1.8, "handleDownloadPdf(url)\nSSRF-safe proxy download stream", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    # Column 3: Axios Client & Typed Wrappers
    col3 = FancyBboxPatch((10.7, 0.5), 6.8, 10.0, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#6366F1", linewidth=1.5, zorder=2)
    ax.add_patch(col3)
    ax.text(14.1, 10.2, "AXIOS API CLIENT & TYPED WRAPPERS", fontsize=11, fontweight='bold', color="#3730A3", ha='center', zorder=3)

    ax.text(14.1, 9.4, "2.2 Axios Core Instance (services/api.ts)\nBase URL: /api/v1 (or VITE_API_BASE_URL) • Timeout: 120s\nInterceptors: Headers injection & Blob error normalizer", fontsize=8.5, color="#701A75", ha='center', zorder=3)

    ax.text(14.1, 7.8, "searchApi: POST /search/ • GET /search/progress • GET /search/results", fontsize=8.5, color="#0E7490", ha='center', zorder=3)
    ax.text(14.1, 6.8, "filesApi: POST /files/upload • GET /files/download/{fn} • GET /files/download-pdf", fontsize=8.5, color="#0E7490", ha='center', zorder=3)
    ax.text(14.1, 5.8, "chatApi: POST /chat/{fn} • POST /chat/ (JSON body) → ChatResponse", fontsize=8.5, color="#0E7490", ha='center', zorder=3)
    ax.text(14.1, 4.8, "embeddingsApi: POST /embeddings/{fn} • GET /progress • GET /status", fontsize=8.5, color="#0E7490", ha='center', zorder=3)
    ax.text(14.1, 3.8, "analysisApi: GET /analysis/files • GET /{fn}/summary • GET /country-collab", fontsize=8.5, color="#0E7490", ha='center', zorder=3)
    ax.text(14.1, 2.8, "systemApi & healthApi: GET /system/status • GET /health (Non-blocking)", fontsize=8.5, color="#0E7490", ha='center', zorder=3)

    ax.text(14.1, 1.4, "2.6 State Synchronization & Output\nUpdates SearchContext, AnalyticsContext, ChatContext\nDispatches HTTP requests to Layer 3: Backend Processing", fontsize=8.5, fontweight='bold', color="#065F46", ha='center', zorder=3)

    plt.tight_layout()
    plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated PNG: {png_path}")
