"""
Layer 1: User Interaction Layer
Covers the complete user journey, entry points, configuration parameters, workspace branching,
user-visible decisions, cancellation, result exploration, and exports.
"""

from .common import THEMES, get_svg_header, get_svg_footer
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Circle

def get_mermaid():
    return """flowchart TD
    %% =========================================================================
    %% LAYER 1: USER INTERACTION LAYER
    %% Project: Research Rover
    %% Focus: Complete User Journey, Workspace Decisions & Operational Branches
    %% =========================================================================

    classDef startEnd fill:#EFF6FF,stroke:#2563EB,stroke-width:2.5px,color:#1E3A8A,font-weight:bold;
    classDef process fill:#F8FAFC,stroke:#3B82F6,stroke-width:1.5px,color:#0F172A;
    classDef decision fill:#FEF3C7,stroke:#D97706,stroke-width:2px,color:#78350F,font-weight:bold;
    classDef action fill:#EEF2FF,stroke:#6366F1,stroke-width:1.5px,color:#312E81;
    classDef storage fill:#F1F5F9,stroke:#64748B,stroke-width:1.5px,color:#0F172A;
    classDef output fill:#ECFDF5,stroke:#10B981,stroke-width:2px,color:#064E3B;

    U_START(["1.0 Start: User Accesses Research Rover Web Portal<br/>(URL: http://localhost:5173/ on Desktop/Tablet)"]):::startEnd
    U_STATUS["1.1 Check Live System Readiness Indicator<br/>(API connectivity, Gemini LLM & MedCPT readiness)"]:::process
    U_DECIDE{"1.2 Select Primary Research Activity<br/>(Navigation Bar or Homepage Quick-Action Cards)"}:::decision

    %% ─── BRANCH A: LITERATURE SEARCH ─────────────────────────────────────────
    subgraph SUB_SEARCH["WORKSPACE A: LITERATURE SEARCH (/search)"]
        S_INPUT["1.3 Enter Topic Query or Comma-Separated Keywords<br/>(e.g., 'machine learning cancer', 'diabetes therapy')"]:::process
        S_FILTERS{"1.4 Configure Search Parameters & Criteria"}:::decision
        S_F_SOURCE["Data Source:<br/>• Unified (PubMed + OpenAlex) [Default]<br/>• PubMed Biomedical Only<br/>• OpenAlex Universal Only"]:::action
        S_F_LIMIT["Result Limit:<br/>10, 20, 50, or 100 papers"]:::action
        S_F_YEAR["Date Bounds:<br/>1950 to Present (or exact start/end dates)"]:::action
        S_F_MODE["Sorting Mode:<br/>• Relevance (MedCPT Bi-encoder)<br/>• Recency (Year descending)"]:::action
        S_F_RAW["Query Mode:<br/>• Expanded (MeSH + Synonyms)<br/>• Raw (Literal match)"]:::action
        S_SUBMIT["1.5 Click 'Search Papers' Button"]:::process
        S_PROGRESS["1.6 Observe Real-Time Animated Progress Loader<br/>(Stage 0: Init → 1: Query → 2: Metadata → 3: Save → 4: Done)"]:::action
        S_CANCEL{"1.7 User Cancels Search In-Flight?"}:::decision
        S_ABORT["1.8 Abort Background Task via /search/cancel<br/>(Cooperative cancellation event set)"]:::process
        S_RESULTS["1.9 Explore Paginated Search Results Catalog<br/>(Title, Authors, Journal, Year, DOI link, Relevance score badge, OA badge)"]:::output
        S_ACTIONS{"1.10 Select Paper Action"}:::decision
        S_ACT_PDF["Download Direct PDF / Proxy Stream"]:::action
        S_ACT_CSV["Export Full Search Catalog CSV"]:::action
        S_ACT_EMBED["Trigger Vector Embeddings Creation"]:::action
        S_ACT_NAV_ANALYTICS["Open in Analytics Workspace"]:::action
    end

    %% ─── BRANCH B: BIBLIOMETRIC & GEOGRAPHIC ANALYTICS ─────────────────────────
    subgraph SUB_ANALYTICS["WORKSPACE B: BIBLIOMETRIC & GEOGRAPHIC ANALYTICS (/analytics)"]
        A_SELECT["1.11 Select Dataset Source<br/>(Choose from saved CSV files or Upload new CSV)"]:::process
        A_TABS{"1.12 Select Analytics View Tab"}:::decision
        
        subgraph TAB_KW["Tab 1: Keywords Analytics View"]
            KW_METRICS["1.13 View Summary Metric Cards<br/>(Total Papers, Papers with Keywords, Unique Keywords)"]:::process
            KW_FREQ["1.14 Explore Keyword Frequency Distribution<br/>(Ranked frequency bar chart & token badges)"]:::process
            KW_CLOUD["1.15 Inspect Interactive SVG Word Cloud<br/>(Dynamic font sizing based on keyword frequency)"]:::process
            KW_GRAPH["1.16 Explore Keyword Co-Occurrence Network<br/>(Zoom, pan, and drag co-occurrence graph)"]:::process
            KW_CENTRALITY["1.17 Analyze NetworkX Centrality Rankings<br/>(Degree, Closeness, Betweenness, Eigenvector, Clustering)"]:::process
            KW_MATRIX["1.18 Preview Binary Keyword Presence Matrix<br/>(Paper rows x Top keyword columns 0/1 indicators)"]:::process
            KW_EXPORTS["1.19 Export Keyword Artifacts<br/>(CSV tables, JSON summary, PNG graph image)"]:::output
        end

        subgraph TAB_CTRY["Tab 2: Country Analytics & Collaborations View"]
            C_METRICS["1.20 View Geographic Summary Metrics<br/>(Coverage %, Unique Countries, International Papers)"]:::process
            C_VIEWS{"1.21 Select Geographic View Mode"}:::decision
            C_MAP["1.22 Explore TopoJSON World Map<br/>(Choropleth country frequency & hover tooltip details)"]:::process
            C_2D["1.23 Explore 2D Force-Directed Network<br/>(D3 physics simulation of co-authorship links)"]:::process
            C_3D["1.24 Explore 3D WebGL Spherical Space<br/>(Orbital camera, Three.js rotating globe, sprite labels)"]:::process
            C_TABLES["1.25 Inspect Country Ranking & Collaborations Tables<br/>(Searchable volume, weighted collaboration pairs)"]:::process
            C_UNASSIGNED["1.26 Review Unassigned Papers Modal<br/>(Papers lacking institutional affiliation data)"]:::process
            C_EXPORT["1.27 Export Country Collaborations CSV"]:::output
        end
    end

    %% ─── BRANCH C: CONVERSATIONAL RAG AI CHAT ──────────────────────────────────
    subgraph SUB_CHAT["WORKSPACE C: CONVERSATIONAL RAG AI CHAT (/chat)"]
        CH_SELECT["1.28 Select Target Dataset CSV File<br/>(Dropdown of available literature catalogs)"]:::process
        CH_STATUS{"1.29 Are FAISS Embeddings Built?"}:::decision
        CH_BUILD["1.30 Click 'Create Embeddings'<br/>(Toggle full-text web scrape, observe progress modal)"]:::action
        CH_READY["1.31 Conversational Input Unlocked<br/>(FAISS flat L2 vector index ready)"]:::process
        CH_QUERY["1.32 Enter Natural Language Research Question<br/>(e.g., 'What are the reported clinical efficacy endpoints?')"]:::process
        CH_RESPONSE["1.33 Receive Synthesized AI Response with Citations<br/>(Markdown formatted text with superscript [1], [2] badges)"]:::output
        CH_CARDS["1.34 Click Citation Badge to Open Source Cards<br/>(View Paper Title, DOI URL link, Extracted Passage Preview)"]:::action
    end

    %% ─── BRANCH D: DATASETS & SETTINGS ─────────────────────────────────────────
    subgraph SUB_FILES_SETTINGS["WORKSPACE D: DATASETS, ARCHITECTURE & SETTINGS"]
        F_UPLOAD["1.35 Upload Custom CSV Dataset<br/>(Drag-and-drop proprietary research CSV)"]:::action
        F_DELETE["1.36 Delete Obsolete Datasets & Vector Indices"]:::action
        ST_THEME["1.37 Toggle Light / Dark UI Theme"]:::action
        ST_ARCH["1.38 Inspect Interactive System Architecture Diagram<br/>(Toggle between User Perspective and Technical Tiers)"]:::action
    end

    U_END(["1.39 Complete Research Task & Download Deliverables<br/>(Dispatches requests to Layer 2: Frontend / API Client Layer)"]):::startEnd

    %% Connections
    U_START --> U_STATUS --> U_DECIDE
    U_DECIDE -->|Search Literature| S_INPUT
    U_DECIDE -->|Analyze Bibliometrics| A_SELECT
    U_DECIDE -->|Chat with Papers| CH_SELECT
    U_DECIDE -->|Manage Files / Settings| F_UPLOAD

    S_INPUT --> S_FILTERS
    S_FILTERS --> S_F_SOURCE & S_F_LIMIT & S_F_YEAR & S_F_MODE & S_F_RAW --> S_SUBMIT
    S_SUBMIT --> S_PROGRESS --> S_CANCEL
    S_CANCEL -->|Yes: Cancel| S_ABORT
    S_CANCEL -->|No: Completed| S_RESULTS
    S_RESULTS --> S_ACTIONS
    S_ACTIONS -->|Direct PDF| S_ACT_PDF
    S_ACTIONS -->|Export CSV| S_ACT_CSV
    S_ACTIONS -->|Vector Index| S_ACT_EMBED --> CH_BUILD
    S_ACTIONS -->|Analyze| S_ACT_NAV_ANALYTICS --> A_SELECT

    A_SELECT --> A_TABS
    A_TABS -->|Keywords Tab| KW_METRICS --> KW_FREQ --> KW_CLOUD --> KW_GRAPH --> KW_CENTRALITY --> KW_MATRIX --> KW_EXPORTS
    A_TABS -->|Country Tab| C_METRICS --> C_VIEWS
    C_VIEWS -->|World Map| C_MAP
    C_VIEWS -->|2D Network| C_2D
    C_VIEWS -->|3D Space| C_3D
    C_VIEWS -->|All Views| C_MAP & C_2D & C_TABLES
    C_MAP & C_2D & C_3D --> C_TABLES --> C_UNASSIGNED --> C_EXPORT

    CH_SELECT --> CH_STATUS
    CH_STATUS -->|No| CH_BUILD --> CH_READY
    CH_STATUS -->|Yes| CH_READY
    CH_READY --> CH_QUERY --> CH_RESPONSE --> CH_CARDS

    F_UPLOAD --> A_SELECT
    F_DELETE --> U_END
    ST_THEME --> U_END
    ST_ARCH --> U_END
    S_ACT_PDF & S_ACT_CSV & KW_EXPORTS & C_EXPORT & CH_CARDS --> U_END
"""

def get_svg():
    w, h = 1750, 1250
    header = get_svg_header(
        w, h,
        title="Layer 1: User Interaction Layer Flowchart",
        subtitle="End-to-End User Journey, Configuration Controls, Workspace Branching, and User-Visible Operations",
        layer_badge="LAYER 01",
        theme_key="layer_01"
    )

    content = '''
  <!-- Inter-layer Connectivity Cards -->
  <g transform="translate(45, 115)">
    <rect x="0" y="0" width="380" height="42" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="15" y="26" font-size="12" font-weight="bold" fill="#1e40af">INPUT:</text>
    <text x="70" y="26" font-size="12" fill="#334155">User navigation, search keywords, filters, uploaded CSV files</text>
  </g>
  <g transform="translate(1325, 115)">
    <rect x="0" y="0" width="380" height="42" rx="8" fill="#f0fdf4" stroke="#10b981" stroke-width="1.5"/>
    <text x="15" y="26" font-size="12" font-weight="bold" fill="#065f46">OUTPUT TARGET:</text>
    <text x="130" y="26" font-size="12" fill="#334155">Layer 2 (Frontend / API Client Layer)</text>
  </g>

  <!-- Flowchart Nodes -->
  <!-- Start & Decision -->
  <g transform="translate(45, 180)">
    <!-- Start -->
    <rect x="0" y="0" width="340" height="54" rx="27" fill="#eff6ff" stroke="#2563eb" stroke-width="2.5" filter="url(#shadow-sm)"/>
    <text x="170" y="26" font-size="13" font-weight="bold" fill="#1e3a8a" text-anchor="middle">1.0 User Accesses Research Rover</text>
    <text x="170" y="42" font-size="10.5" fill="#475569" text-anchor="middle">Browser on Desktop / Tablet (http://localhost:5173/)</text>

    <!-- Arrow -->
    <line x1="340" y1="27" x2="385" y2="27" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow)"/>

    <!-- Status Check -->
    <rect x="390" y="0" width="300" height="54" rx="10" fill="#f8fafc" stroke="#3b82f6" stroke-width="1.5" filter="url(#shadow-sm)"/>
    <text x="540" y="25" font-size="12.5" font-weight="bold" fill="#0f172a" text-anchor="middle">1.1 Verify System Status</text>
    <text x="540" y="41" font-size="10" fill="#475569" text-anchor="middle">Live indicator: API online, Gemini &amp; MedCPT ready</text>

    <!-- Arrow -->
    <line x1="690" y1="27" x2="735" y2="27" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow)"/>

    <!-- Workflow Decision -->
    <polygon points="850,0 960,27 850,54 740,27" fill="#fef3c7" stroke="#d97706" stroke-width="2" filter="url(#shadow-sm)"/>
    <text x="850" y="23" font-size="11" font-weight="bold" fill="#78350f" text-anchor="middle">1.2 Select Activity</text>
    <text x="850" y="37" font-size="9" fill="#92400e" text-anchor="middle">Navbar / Quick Cards</text>
  </g>

  <!-- Branch Connecting Lines -->
  <path d="M 895 234 L 895 280 L 220 280 L 220 310" stroke="#2563eb" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
  <path d="M 895 234 L 895 280 L 680 280 L 680 310" stroke="#2563eb" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
  <path d="M 895 234 L 895 280 L 1150 280 L 1150 310" stroke="#2563eb" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
  <path d="M 895 234 L 895 280 L 1550 280 L 1550 310" stroke="#2563eb" stroke-width="2" fill="none" marker-end="url(#arrow)"/>

  <!-- WORKSPACE A: LITERATURE SEARCH -->
  <g transform="translate(45, 310)">
    <rect x="0" y="0" width="370" height="840" rx="14" fill="#fafafa" stroke="#3b82f6" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="340" height="34" rx="6" fill="#eff6ff"/>
    <text x="185" y="37" font-size="13" font-weight="bold" fill="#1e40af" text-anchor="middle">WORKSPACE A: LITERATURE SEARCH</text>

    <!-- Query Input -->
    <rect x="20" y="65" width="330" height="52" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="185" y="87" font-size="12" font-weight="bold" fill="#0f172a" text-anchor="middle">1.3 Enter Query / Keywords</text>
    <text x="185" y="103" font-size="10" fill="#64748b" text-anchor="middle">e.g., 'machine learning cancer', 'diabetes AND therapy'</text>
    <line x1="185" y1="117" x2="185" y2="135" stroke="#3b82f6" stroke-width="1.8" marker-end="url(#arrow)"/>

    <!-- Filter Configuration -->
    <polygon points="185,138 285,165 185,192 85,165" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
    <text x="185" y="161" font-size="10.5" font-weight="bold" fill="#78350f" text-anchor="middle">1.4 Configure Filters</text>
    <text x="185" y="174" font-size="8.5" fill="#92400e" text-anchor="middle">Parameters &amp; Options</text>
    <line x1="185" y1="192" x2="185" y2="210" stroke="#3b82f6" stroke-width="1.8" marker-end="url(#arrow)"/>

    <!-- Filters List -->
    <rect x="20" y="210" width="330" height="135" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
    <text x="35" y="230" font-size="10" font-weight="bold" fill="#1e293b">• Data Source: Unified (PubMed + OpenAlex) | PubMed | OpenAlex</text>
    <text x="35" y="252" font-size="10" font-weight="bold" fill="#1e293b">• Result Limit: 10, 20, 50, 100 papers</text>
    <text x="35" y="274" font-size="10" font-weight="bold" fill="#1e293b">• Year Slider: 1950 to Present (or exact start/end dates)</text>
    <text x="35" y="296" font-size="10" font-weight="bold" fill="#1e293b">• Sort Mode: Relevance (MedCPT neural) | Recency</text>
    <text x="35" y="318" font-size="10" font-weight="bold" fill="#1e293b">• Query Mode: Expanded (MeSH + Synonyms) | Raw (Literal)</text>
    <line x1="185" y1="345" x2="185" y2="365" stroke="#3b82f6" stroke-width="1.8" marker-end="url(#arrow)"/>

    <!-- Submit Search -->
    <rect x="20" y="365" width="330" height="46" rx="8" fill="#2563eb" stroke="#1d4ed8" stroke-width="1.5"/>
    <text x="185" y="393" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">1.5 Click 'Search Papers' Button</text>
    <line x1="185" y1="411" x2="185" y2="430" stroke="#3b82f6" stroke-width="1.8" marker-end="url(#arrow)"/>

    <!-- Progress Polling -->
    <rect x="20" y="430" width="330" height="52" rx="8" fill="#e0e7ff" stroke="#6366f1" stroke-width="1.2"/>
    <text x="185" y="452" font-size="11.5" font-weight="bold" fill="#312e81" text-anchor="middle">1.6 Real-Time Progress Feedback</text>
    <text x="185" y="468" font-size="9.5" fill="#4338ca" text-anchor="middle">Animated stages (0-4), status bar, cancel option</text>
    <line x1="185" y1="482" x2="185" y2="502" stroke="#3b82f6" stroke-width="1.8" marker-end="url(#arrow)"/>

    <!-- Cancel Decision -->
    <polygon points="185,502 280,528 185,554 90,528" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
    <text x="185" y="525" font-size="10.5" font-weight="bold" fill="#78350f" text-anchor="middle">1.7 Cancel Search?</text>
    <text x="185" y="538" font-size="8.5" fill="#92400e" text-anchor="middle">User abort decision</text>

    <!-- Abort or Complete -->
    <line x1="280" y1="528" x2="330" y2="528" stroke="#ef4444" stroke-width="1.8" marker-end="url(#arrow)"/>
    <rect x="220" y="565" width="130" height="40" rx="6" fill="#fee2e2" stroke="#ef4444" stroke-width="1"/>
    <text x="285" y="582" font-size="9.5" font-weight="bold" fill="#991b1b" text-anchor="middle">1.8 Abort Search</text>
    <text x="285" y="595" font-size="8" fill="#b91c1c" text-anchor="middle">/search/cancel called</text>

    <line x1="185" y1="554" x2="185" y2="620" stroke="#10b981" stroke-width="1.8" marker-end="url(#arrow-success)"/>
    <text x="145" y="590" font-size="9" font-weight="bold" fill="#047857">Completed</text>

    <!-- Search Results View -->
    <rect x="20" y="620" width="330" height="65" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
    <text x="185" y="643" font-size="11.5" font-weight="bold" fill="#064e3b" text-anchor="middle">1.9 Explore Results Catalog</text>
    <text x="185" y="659" font-size="9.5" fill="#047857" text-anchor="middle">Title, authors, year, journal, DOI link, OA badge</text>
    <text x="185" y="673" font-size="9.5" fill="#047857" text-anchor="middle">Relevance score badge (0-100%), pagination</text>
    <line x1="185" y1="685" x2="185" y2="705" stroke="#3b82f6" stroke-width="1.8" marker-end="url(#arrow)"/>

    <!-- Paper Actions -->
    <rect x="20" y="705" width="330" height="115" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
    <text x="185" y="724" font-size="10.5" font-weight="bold" fill="#1e293b" text-anchor="middle">1.10 Select Result Action</text>
    <text x="35" y="746" font-size="9.5" fill="#334155">• Click 'Download PDF' → Direct or proxy PDF stream</text>
    <text x="35" y="766" font-size="9.5" fill="#334155">• Click 'Export CSV' → Download &lt;query&gt;.csv dataset</text>
    <text x="35" y="786" font-size="9.5" fill="#334155">• Click 'Generate Embeddings' → Launch FAISS builder</text>
    <text x="35" y="806" font-size="9.5" fill="#334155">• Click 'Open in Analytics' → Navigate with dataset</text>
  </g>

  <!-- WORKSPACE B: BIBLIOMETRIC & GEOGRAPHIC ANALYTICS -->
  <g transform="translate(445, 310)">
    <rect x="0" y="0" width="460" height="840" rx="14" fill="#fafafa" stroke="#3b82f6" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="430" height="34" rx="6" fill="#eff6ff"/>
    <text x="230" y="37" font-size="13" font-weight="bold" fill="#1e40af" text-anchor="middle">WORKSPACE B: BIBLIOMETRIC &amp; GEOGRAPHIC ANALYTICS</text>

    <!-- Source Selection -->
    <rect x="20" y="65" width="420" height="52" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="230" y="87" font-size="12" font-weight="bold" fill="#0f172a" text-anchor="middle">1.11 Select Dataset Source</text>
    <text x="230" y="103" font-size="10" fill="#64748b" text-anchor="middle">Pick from saved CSV catalog or Drag-and-Drop upload new CSV</text>
    <line x1="230" y1="117" x2="230" y2="135" stroke="#3b82f6" stroke-width="1.8" marker-end="url(#arrow)"/>

    <!-- Tab Decision -->
    <polygon points="230,138 340,165 230,192 120,165" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
    <text x="230" y="161" font-size="10.5" font-weight="bold" fill="#78350f" text-anchor="middle">1.12 Select View Tab</text>
    <text x="230" y="174" font-size="8.5" fill="#92400e" text-anchor="middle">Keywords vs Country</text>

    <!-- Branch to Keywords and Country -->
    <path d="M 120 165 L 70 165 L 70 215" stroke="#3b82f6" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>
    <path d="M 340 165 L 390 165 L 390 215" stroke="#3b82f6" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>

    <!-- Tab 1: Keywords Sub-card -->
    <rect x="15" y="215" width="205" height="490" rx="8" fill="#ffffff" stroke="#93c5fd" stroke-width="1.2"/>
    <rect x="20" y="222" width="195" height="26" rx="4" fill="#dbeafe"/>
    <text x="117" y="239" font-size="10.5" font-weight="bold" fill="#1e40af" text-anchor="middle">Tab 1: Keywords Analytics</text>
    <text x="25" y="265" font-size="9" font-weight="bold" fill="#0f172a">1.13 Summary Metric Cards</text>
    <text x="32" y="279" font-size="8" fill="#475569">Total papers, keywords, unique terms</text>
    <text x="25" y="305" font-size="9" font-weight="bold" fill="#0f172a">1.14 Frequency Distribution</text>
    <text x="32" y="319" font-size="8" fill="#475569">Ranked keyword frequency &amp; %</text>
    <text x="25" y="345" font-size="9" font-weight="bold" fill="#0f172a">1.15 SVG Word Cloud</text>
    <text x="32" y="359" font-size="8" fill="#475569">Font scaled by term occurrence</text>
    <text x="25" y="385" font-size="9" font-weight="bold" fill="#0f172a">1.16 Co-Occurrence Graph</text>
    <text x="32" y="399" font-size="8" fill="#475569">Force-directed network, zoom/pan</text>
    <text x="25" y="425" font-size="9" font-weight="bold" fill="#0f172a">1.17 Centrality Scores Table</text>
    <text x="32" y="439" font-size="8" fill="#475569">Degree, Betweenness, Closeness,</text>
    <text x="32" y="451" font-size="8" fill="#475569">Eigenvector, Clustering metrics</text>
    <text x="25" y="475" font-size="9" font-weight="bold" fill="#0f172a">1.18 Binary Presence Matrix</text>
    <text x="32" y="489" font-size="8" fill="#475569">0/1 binary indicator grid</text>
    <text x="25" y="515" font-size="9" font-weight="bold" fill="#065f46">1.19 Export Artifacts</text>
    <text x="32" y="529" font-size="8" fill="#047857">CSV frequency, matrix, JSON, PNG</text>

    <!-- Tab 2: Country Sub-card -->
    <rect x="235" y="215" width="210" height="490" rx="8" fill="#ffffff" stroke="#93c5fd" stroke-width="1.2"/>
    <rect x="240" y="222" width="200" height="26" rx="4" fill="#dbeafe"/>
    <text x="340" y="239" font-size="10.5" font-weight="bold" fill="#1e40af" text-anchor="middle">Tab 2: Country &amp; Collaborations</text>
    <text x="245" y="265" font-size="9" font-weight="bold" fill="#0f172a">1.20 Geographic Metrics</text>
    <text x="252" y="279" font-size="8" fill="#475569">Coverage %, unique countries, co-authors</text>
    <text x="245" y="305" font-size="9" font-weight="bold" fill="#0f172a">1.21 Select View Mode</text>
    <text x="252" y="319" font-size="8" fill="#475569">All Views | Map | Network toggle</text>
    <text x="245" y="345" font-size="9" font-weight="bold" fill="#0f172a">1.22 TopoJSON World Map</text>
    <text x="252" y="359" font-size="8" fill="#475569">Choropleth shading, hover tooltips</text>
    <text x="245" y="385" font-size="9" font-weight="bold" fill="#0f172a">1.23 2D Force Network</text>
    <text x="252" y="399" font-size="8" fill="#475569">D3 spring physics collaboration graph</text>
    <text x="245" y="425" font-size="9" font-weight="bold" fill="#0f172a">1.24 3D WebGL Orbital Space</text>
    <text x="252" y="439" font-size="8" fill="#475569">Three.js spherical space, sprite labels</text>
    <text x="245" y="465" font-size="9" font-weight="bold" fill="#0f172a">1.25 Ranking &amp; Collab Tables</text>
    <text x="252" y="479" font-size="8" fill="#475569">Filterable publication &amp; link weights</text>
    <text x="245" y="505" font-size="9" font-weight="bold" fill="#0f172a">1.26 Unassigned Papers Modal</text>
    <text x="252" y="519" font-size="8" fill="#475569">Papers lacking author affiliation data</text>
    <text x="245" y="545" font-size="9" font-weight="bold" fill="#065f46">1.27 Export Collaborations</text>
    <text x="252" y="559" font-size="8" fill="#047857">Download country collaborations CSV</text>

    <!-- Combined Export Bar -->
    <rect x="20" y="720" width="420" height="100" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
    <text x="230" y="740" font-size="10.5" font-weight="bold" fill="#1e293b" text-anchor="middle">Export &amp; Reporting Options</text>
    <text x="35" y="762" font-size="9" fill="#334155">• Download CSV: Keyword frequencies, presence matrix, collaborations</text>
    <text x="35" y="782" font-size="9" fill="#334155">• Download JSON: Complete structured analysis summary</text>
    <text x="35" y="802" font-size="9" fill="#334155">• Export PNG: High-res chart &amp; network image exports for PowerPoint</text>
  </g>

  <!-- WORKSPACE C: CONVERSATIONAL RAG AI CHAT -->
  <g transform="translate(935, 310)">
    <rect x="0" y="0" width="410" height="840" rx="14" fill="#fafafa" stroke="#3b82f6" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="380" height="34" rx="6" fill="#eff6ff"/>
    <text x="205" y="37" font-size="13" font-weight="bold" fill="#1e40af" text-anchor="middle">WORKSPACE C: CONVERSATIONAL RAG AI CHAT</text>

    <!-- Dataset Selection -->
    <rect x="20" y="65" width="370" height="52" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="205" y="87" font-size="12" font-weight="bold" fill="#0f172a" text-anchor="middle">1.28 Select Research Dataset</text>
    <text x="205" y="103" font-size="10" fill="#64748b" text-anchor="middle">Choose CSV file from dropdown or upload new paper catalog</text>
    <line x1="205" y1="117" x2="205" y2="135" stroke="#3b82f6" stroke-width="1.8" marker-end="url(#arrow)"/>

    <!-- Embedding Status Check -->
    <polygon points="205,138 305,165 205,192 105,165" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
    <text x="205" y="161" font-size="10.5" font-weight="bold" fill="#78350f" text-anchor="middle">1.29 Embeddings Built?</text>
    <text x="205" y="174" font-size="8.5" fill="#92400e" text-anchor="middle">FAISS vector store status</text>

    <!-- Build Embeddings -->
    <line x1="105" y1="165" x2="55" y2="165" stroke="#d97706" stroke-width="1.5"/>
    <line x1="55" y1="165" x2="55" y2="215" stroke="#d97706" stroke-width="1.5" marker-end="url(#arrow)"/>
    <rect x="20" y="215" width="165" height="85" rx="8" fill="#fffbeb" stroke="#f59e0b" stroke-width="1.2"/>
    <text x="102" y="235" font-size="10" font-weight="bold" fill="#92400e" text-anchor="middle">1.30 Build Embeddings</text>
    <text x="102" y="252" font-size="8.5" fill="#78350f" text-anchor="middle">Toggle full-text web scrape</text>
    <text x="102" y="268" font-size="8.5" fill="#78350f" text-anchor="middle">HDBSCAN semantic chunking</text>
    <text x="102" y="284" font-size="8.5" fill="#78350f" text-anchor="middle">FAISS IndexFlatL2 built</text>

    <line x1="102" y1="300" x2="102" y2="340" stroke="#10b981" stroke-width="1.5"/>
    <line x1="102" y1="340" x2="150" y2="340" stroke="#10b981" stroke-width="1.5" marker-end="url(#arrow-success)"/>

    <!-- Direct to Ready -->
    <line x1="205" y1="192" x2="205" y2="320" stroke="#10b981" stroke-width="1.8" marker-end="url(#arrow-success)"/>
    <text x="215" y="260" font-size="9" font-weight="bold" fill="#047857">Yes: Index Ready</text>

    <!-- Chat Ready -->
    <rect x="150" y="320" width="240" height="45" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="270" y="342" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">1.31 Conversational Input Unlocked</text>
    <text x="270" y="356" font-size="9" fill="#64748b" text-anchor="middle">Dataset vectorized and ready for RAG querying</text>
    <line x1="270" y1="365" x2="270" y2="390" stroke="#3b82f6" stroke-width="1.8" marker-end="url(#arrow)"/>

    <!-- Query Input -->
    <rect x="20" y="390" width="370" height="60" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="205" y="414" font-size="11.5" font-weight="bold" fill="#0f172a" text-anchor="middle">1.32 Ask Research Question</text>
    <text x="205" y="432" font-size="9.5" fill="#64748b" text-anchor="middle">e.g., 'What are the reported clinical efficacy endpoints across papers?'</text>
    <line x1="205" y1="450" x2="205" y2="475" stroke="#3b82f6" stroke-width="1.8" marker-end="url(#arrow)"/>

    <!-- Response Display -->
    <rect x="20" y="475" width="370" height="90" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
    <text x="205" y="500" font-size="11.5" font-weight="bold" fill="#064e3b" text-anchor="middle">1.33 AI Synthesized Response with Citations</text>
    <text x="205" y="518" font-size="9" fill="#047857" text-anchor="middle">Rendered rich Markdown response with clickable superscript</text>
    <text x="205" y="534" font-size="9" fill="#047857" text-anchor="middle">citation badges [1], [2] referencing paper chunks</text>
    <line x1="205" y1="565" x2="205" y2="590" stroke="#3b82f6" stroke-width="1.8" marker-end="url(#arrow)"/>

    <!-- Source Cards -->
    <rect x="20" y="590" width="370" height="100" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="205" y="612" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">1.34 Explore Collapsible Citation Cards</text>
    <text x="35" y="632" font-size="9" fill="#334155">• Click citation pill [1] to jump directly to corresponding evidence card</text>
    <text x="35" y="652" font-size="9" fill="#334155">• View exact paper title, DOI clickable link, and text snippet</text>
    <text x="35" y="672" font-size="9" fill="#334155">• Trace claims to primary literature without hallucinations</text>
  </g>

  <!-- WORKSPACE D: DATASETS, ARCHITECTURE & SETTINGS -->
  <g transform="translate(1375, 310)">
    <rect x="0" y="0" width="330" height="840" rx="14" fill="#fafafa" stroke="#3b82f6" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="300" height="34" rx="6" fill="#eff6ff"/>
    <text x="165" y="37" font-size="12" font-weight="bold" fill="#1e40af" text-anchor="middle">WORKSPACE D: DATASETS &amp; SETTINGS</text>

    <!-- File Operations -->
    <rect x="20" y="65" width="290" height="85" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="165" y="88" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">1.35 Upload Custom CSV Dataset</text>
    <text x="165" y="105" font-size="9" fill="#64748b" text-anchor="middle">Upload external tabular literature CSV</text>
    <text x="165" y="120" font-size="9" fill="#64748b" text-anchor="middle">Auto-probes UTF-8 / CP1252 / Latin-1 encoding</text>

    <rect x="20" y="170" width="290" height="75" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="165" y="195" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">1.36 Delete Obsolete Datasets</text>
    <text x="165" y="212" font-size="9" fill="#64748b" text-anchor="middle">Deletes CSV, JSON summaries, and</text>
    <text x="165" y="226" font-size="9" fill="#64748b" text-anchor="middle">FAISS vector indices cleanly</text>

    <rect x="20" y="265" width="290" height="75" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="165" y="290" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">1.37 System Theme Settings</text>
    <text x="165" y="307" font-size="9" fill="#64748b" text-anchor="middle">Toggle Light / Dark Mode with persistent</text>
    <text x="165" y="321" font-size="9" fill="#64748b" text-anchor="middle">local storage theme synchronization</text>

    <rect x="20" y="360" width="290" height="95" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="165" y="385" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">1.38 Architecture &amp; Guide View</text>
    <text x="165" y="402" font-size="9" fill="#64748b" text-anchor="middle">Inspect verified 8-layer codebase diagram</text>
    <text x="165" y="416" font-size="9" fill="#64748b" text-anchor="middle">Review M.Tech thesis system walkthrough</text>
    <text x="165" y="430" font-size="9" fill="#64748b" text-anchor="middle">Explore module code inventory</text>

    <!-- Outward connection to Layer 2 -->
    <rect x="20" y="500" width="290" height="150" rx="8" fill="#f0fdf4" stroke="#10b981" stroke-width="1.5"/>
    <text x="165" y="530" font-size="12" font-weight="bold" fill="#065f46" text-anchor="middle">1.39 Complete Research Task</text>
    <text x="165" y="555" font-size="9.5" fill="#047857" text-anchor="middle">All user operations dispatch typed</text>
    <text x="165" y="570" font-size="9.5" fill="#047857" text-anchor="middle">HTTP events to Layer 2:</text>
    <text x="165" y="590" font-size="11" font-weight="bold" fill="#064e3b" text-anchor="middle">Frontend / API Client Layer</text>
    <text x="165" y="610" font-size="9" fill="#047857" text-anchor="middle">(frontend/src/services/api.ts)</text>
  </g>
'''

    return header + content + get_svg_footer()

def render_matplotlib(png_path):
    fig, ax = plt.subplots(figsize=(18, 12), dpi=300)
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Background
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Header Banner
    header = FancyBboxPatch((0.4, 10.8), 17.2, 0.9, boxstyle="round,pad=0,rounding_size=0.15",
                            facecolor="#1D4ED8", edgecolor="#1E40AF", linewidth=1.5, zorder=2)
    ax.add_patch(header)
    ax.text(0.6, 11.45, "LAYER 01: USER INTERACTION LAYER FLOWCHART", fontsize=15, fontweight='bold', color="#FFFFFF", zorder=3)
    ax.text(0.6, 11.08, "End-to-End User Journey, Configuration Controls, Workspace Branching, and User-Visible Operations", fontsize=9.5, color="#DBEAFE", zorder=3)
    ax.text(17.4, 11.25, "Research Rover v2.0", fontsize=10, fontweight='bold', color="#93C5FD", ha='right', zorder=3)

    # Start Node
    start_box = FancyBboxPatch((0.5, 9.6), 4.2, 0.7, boxstyle="round,pad=0,rounding_size=0.35",
                               facecolor="#EFF6FF", edgecolor="#2563EB", linewidth=2.0, zorder=3)
    ax.add_patch(start_box)
    ax.text(2.6, 10.05, "1.0 User Accesses Research Rover", fontsize=10, fontweight='bold', color="#1E3A8A", ha='center', zorder=4)
    ax.text(2.6, 9.78, "Browser on Desktop / Tablet (http://localhost:5173/)", fontsize=8, color="#475569", ha='center', zorder=4)

    # Arrow to Status
    ax.annotate('', xy=(5.2, 9.95), xytext=(4.7, 9.95), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.8), zorder=3)

    # Status Node
    status_box = FancyBboxPatch((5.2, 9.6), 3.8, 0.7, boxstyle="round,pad=0,rounding_size=0.12",
                                facecolor="#F8FAFC", edgecolor="#3B82F6", linewidth=1.5, zorder=3)
    ax.add_patch(status_box)
    ax.text(7.1, 10.05, "1.1 Verify System Status", fontsize=10, fontweight='bold', color="#0F172A", ha='center', zorder=4)
    ax.text(7.1, 9.78, "API online, Gemini LLM & MedCPT ready", fontsize=8, color="#475569", ha='center', zorder=4)

    # Arrow to Decision
    ax.annotate('', xy=(9.5, 9.95), xytext=(9.0, 9.95), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.8), zorder=3)

    # Decision Diamond
    diamond = Polygon([[11.0, 10.4], [12.4, 9.95], [11.0, 9.5], [9.6, 9.95]],
                      facecolor="#FEF3C7", edgecolor="#D97706", linewidth=1.8, zorder=3)
    ax.add_patch(diamond)
    ax.text(11.0, 10.05, "1.2 Select Activity", fontsize=9.5, fontweight='bold', color="#78350F", ha='center', zorder=4)
    ax.text(11.0, 9.82, "Navbar / Quick Cards", fontsize=7.5, color="#92400E", ha='center', zorder=4)

    # Connecting branches
    ax.plot([11.0, 11.0, 2.3, 2.3], [9.5, 9.1, 9.1, 8.8], color="#2563EB", lw=1.5, zorder=2)
    ax.plot([11.0, 11.0, 6.7, 6.7], [9.5, 9.1, 9.1, 8.8], color="#2563EB", lw=1.5, zorder=2)
    ax.plot([11.0, 11.0, 11.3, 11.3], [9.5, 9.1, 9.1, 8.8], color="#2563EB", lw=1.5, zorder=2)
    ax.plot([11.0, 11.0, 15.6, 15.6], [9.5, 9.1, 9.1, 8.8], color="#2563EB", lw=1.5, zorder=2)

    # Column 1: Workspace A - Search
    col1 = FancyBboxPatch((0.5, 0.4), 3.8, 8.4, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#3B82F6", linewidth=1.5, zorder=2)
    ax.add_patch(col1)
    ax.text(2.4, 8.5, "WORKSPACE A: LITERATURE SEARCH", fontsize=10, fontweight='bold', color="#1E40AF", ha='center', zorder=3)
    ax.text(2.4, 7.9, "1.3 Enter Query & Keywords\ne.g., 'machine learning cancer'", fontsize=8.5, color="#0F172A", ha='center', zorder=3)
    ax.text(2.4, 6.9, "1.4 Configure Parameters\n• Source: Unified / PubMed / OpenAlex\n• Limit: 10 to 100 papers\n• Year: 1950 - Present\n• Mode: Relevance / Recency", fontsize=8, color="#334155", ha='center', zorder=3)
    ax.text(2.4, 5.7, "1.5 Submit Search Papers", fontsize=8.5, fontweight='bold', color="#1D4ED8", ha='center', zorder=3)
    ax.text(2.4, 4.8, "1.6 Live Progress Feedback\nPolling stages 0-4 (with cancel)", fontsize=8, color="#4338CA", ha='center', zorder=3)
    ax.text(2.4, 3.6, "1.9 Explore Results Catalog\nRelevance score (0-100%), OA badge,\nauthors, journal, pagination", fontsize=8, color="#047857", ha='center', zorder=3)
    ax.text(2.4, 2.2, "1.10 Paper Actions\n• Download Direct / Proxy PDF\n• Export Search CSV\n• Generate FAISS Embeddings\n• Open in Analytics", fontsize=8, color="#0F172A", ha='center', zorder=3)

    # Column 2: Workspace B - Analytics
    col2 = FancyBboxPatch((4.7, 0.4), 4.2, 8.4, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#3B82F6", linewidth=1.5, zorder=2)
    ax.add_patch(col2)
    ax.text(6.8, 8.5, "WORKSPACE B: ANALYTICS", fontsize=10, fontweight='bold', color="#1E40AF", ha='center', zorder=3)
    ax.text(6.8, 8.0, "1.11 Select Dataset Source\nSaved CSV or Upload Custom CSV", fontsize=8.5, color="#0F172A", ha='center', zorder=3)
    ax.text(6.8, 7.3, "1.12 Select Analytics View Tab", fontsize=8.5, fontweight='bold', color="#78350F", ha='center', zorder=3)
    ax.text(6.8, 5.7, "[Tab 1: Keywords Analytics]\n• Keyword Frequency Bar Chart\n• Interactive SVG Word Cloud\n• Co-occurrence Network Graph\n• NetworkX Centralities (5 metrics)\n• Binary Presence Matrix Preview", fontsize=8, color="#334155", ha='center', zorder=3)
    ax.text(6.8, 3.8, "[Tab 2: Country Analytics]\n• TopoJSON World Choropleth Map\n• 2D D3 Force-Directed Network\n• 3D WebGL Spherical Space\n• Country Ranking & Collab Tables\n• Unassigned Papers Review", fontsize=8, color="#334155", ha='center', zorder=3)
    ax.text(6.8, 1.8, "1.19 & 1.27 Export Deliverables\nCSV tables, JSON summary, PNG graphs", fontsize=8, color="#065F46", ha='center', zorder=3)

    # Column 3: Workspace C - AI Chat
    col3 = FancyBboxPatch((9.3, 0.4), 4.0, 8.4, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#3B82F6", linewidth=1.5, zorder=2)
    ax.add_patch(col3)
    ax.text(11.3, 8.5, "WORKSPACE C: RAG AI CHAT", fontsize=10, fontweight='bold', color="#1E40AF", ha='center', zorder=3)
    ax.text(11.3, 7.9, "1.28 Select Literature Dataset\nDropdown of paper catalogs", fontsize=8.5, color="#0F172A", ha='center', zorder=3)
    ax.text(11.3, 6.8, "1.29 Check FAISS Index Status\nIf missing: 1.30 Build Embeddings\n(Scrape + HDBSCAN + FAISS Flat)", fontsize=8, color="#92400E", ha='center', zorder=3)
    ax.text(11.3, 5.5, "1.31 Conversational Input Ready\nFAISS dense vector index active", fontsize=8.5, color="#047857", ha='center', zorder=3)
    ax.text(11.3, 4.5, "1.32 Ask Research Question\ne.g., 'What are the reported clinical endpoints?'", fontsize=8, color="#0F172A", ha='center', zorder=3)
    ax.text(11.3, 3.2, "1.33 AI Synthesized Response\nRich Markdown text with\nsuperscript [1], [2] citation badges", fontsize=8, color="#065F46", ha='center', zorder=3)
    ax.text(11.3, 1.8, "1.34 Citation Source Cards\nClick citation pill to view title,\nDOI link, and extracted snippet", fontsize=8, color="#334155", ha='center', zorder=3)

    # Column 4: Workspace D - Datasets & Settings
    col4 = FancyBboxPatch((13.7, 0.4), 3.8, 8.4, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#3B82F6", linewidth=1.5, zorder=2)
    ax.add_patch(col4)
    ax.text(15.6, 8.5, "WORKSPACE D: DATASETS & SETTINGS", fontsize=9.5, fontweight='bold', color="#1E40AF", ha='center', zorder=3)
    ax.text(15.6, 7.5, "1.35 Upload Custom CSV\nDrag & drop literature CSV,\nauto-probes UTF-8/Latin-1", fontsize=8, color="#0F172A", ha='center', zorder=3)
    ax.text(15.6, 6.2, "1.36 Dataset Management\nDownload CSVs, delete obsolete\ncollections and vector indices", fontsize=8, color="#0F172A", ha='center', zorder=3)
    ax.text(15.6, 4.9, "1.37 System Theme Settings\nToggle Light / Dark mode with\npersistent local storage", fontsize=8, color="#0F172A", ha='center', zorder=3)
    ax.text(15.6, 3.6, "1.38 Architecture Explorer\nInteractive 8-layer diagram &\ncode inventory table", fontsize=8, color="#0F172A", ha='center', zorder=3)
    ax.text(15.6, 1.8, "1.39 Complete Research Task\nDispatches typed requests to\nLayer 2: Frontend / API Client", fontsize=8.5, fontweight='bold', color="#065F46", ha='center', zorder=3)

    plt.tight_layout()
    plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated PNG: {png_path}")
