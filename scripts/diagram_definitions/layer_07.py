"""
Layer 7: Visualization & Output Layer
Covers all interactive UI widgets, TopoJSON World Map, 2D/3D Force Networks,
Word Cloud SVG, NetworkX Tables, RAG Chat Stream, Error Boundaries, and Export Pipelines.
"""

from .common import THEMES, get_svg_header, get_svg_footer
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

def get_mermaid():
    return """flowchart TD
    %% =========================================================================
    %% LAYER 7: VISUALIZATION & OUTPUT LAYER
    %% Project: Research Rover
    %% Focus: Real UI Renderers, Geographic Maps, 2D/3D Force Graphs, RAG Chat & File Exports
    %% =========================================================================

    classDef startEnd fill:#FFF1F2,stroke:#E11D48,stroke-width:2.5px,color:#9F1239,font-weight:bold;
    classDef inputDS fill:#F1F5F9,stroke:#64748B,stroke-width:1.5px,color:#0F172A;
    classDef vizComp fill:#F8FAFC,stroke:#F43F5E,stroke-width:1.5px,color:#0F172A;
    classDef errBound fill:#FEE2E2,stroke:#EF4444,stroke-width:1.5px,color:#991B1B;
    classDef exportAction fill:#ECFDF5,stroke:#10B981,stroke-width:1.8px,color:#064E3B,font-weight:bold;
    classDef userOut fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E3A8A,font-weight:bold;

    V_ENTRY(["7.0 Entry: Analytics Payloads & Vector Outputs Received<br/>(From Layer 6: Analysis & Computation Layer)"]):::startEnd

    %% ─── ERROR BOUNDARY WRAPPERS ─────────────────────────────────────────────
    subgraph SUB_ERR["REACT ERROR BOUNDARY PROTECTION (ErrorBoundary.tsx)"]
        EB_WRAP["7.1 ErrorBoundary Component Wrappers<br/>Wraps WebGL, Three.js & D3 Canvas renderers<br/>Catches rendering exceptions & displays fallback retry card"]:::errBound
    end

    %% ─── GEOGRAPHIC & COLLABORATION VISUALIZATIONS ───────────────────────────
    subgraph SUB_GEO_VIZ["GEOGRAPHIC & INTERNATIONAL COLLABORATION VISUALIZATIONS"]
        VIZ_MAP["7.2 TopoJSON Geographic World Map (WorldMap.tsx)<br/>• react-simple-maps + world-110m.json TopoJSON<br/>• Logarithmic / linear color choropleth shading<br/>• Interactive hover tooltip: country name, papers count & percentage"]:::vizComp
        
        VIZ_2D["7.3 2D Force-Directed Collaboration Network (CountryCollaboration2D.tsx)<br/>• react-force-graph-2d with D3 spring-charge physics simulation<br/>• Node radius proportional to country publication volume<br/>• Link width proportional to international collaboration weight<br/>• Canvas zoom, pan, and click-to-focus interactions"]:::vizComp
        
        VIZ_3D["7.4 3D WebGL Spherical Collaboration Space (CountryCollaboration3D.tsx)<br/>• react-force-graph-3d + Three.js WebGL space<br/>• Country sprite text labels (three-spritetext)<br/>• Glowing orbital particles along collaboration links, rotating camera controls"]:::vizComp
        
        VIZ_TABLES["7.5 Bibliometric Ranking & Unassigned Tables (CountryAnalysisView.tsx)<br/>• Searchable country publication volume ranking table with ISO-3 badges<br/>• Country collaboration pairs table with weights<br/>• Unassigned papers review modal for records lacking affiliations"]:::vizComp
    end

    %% ─── KEYWORD & BIBLIOMETRIC VISUALIZATIONS ───────────────────────────────
    subgraph SUB_KW_VIZ["KEYWORD ANALYTICS & GRAPH VISUALIZATIONS (AnalyticsPage.tsx)"]
        VIZ_CLOUD["7.6 Interactive SVG Word Cloud<br/>Dynamic font sizing scaled by keyword frequency<br/>Frequency-colored tokens with hover & click-to-filter"]:::vizComp
        
        VIZ_GRAPH["7.7 Keyword Co-Occurrence Network Graph SVG<br/>Force-directed layout of keyword nodes and co-occurrence links<br/>Degree-based node coloring, zoom, pan, and fullscreen toggle"]:::vizComp
        
        VIZ_CENTRALITY["7.8 NetworkX Centrality Scores Table<br/>Sortable table: Degree, Closeness, Betweenness, Eigenvector, Clustering"]:::vizComp
        
        VIZ_MATRIX["7.9 Binary Keyword Presence Matrix Table<br/>Paginated table of paper records x top keyword binary 0/1 indicators"]:::vizComp
    end

    %% ─── CONVERSATIONAL RAG & CITATIONS ──────────────────────────────────────
    subgraph SUB_RAG_VIZ["CONVERSATIONAL RAG CHAT & CITATION STREAM (ChatPage.tsx)"]
        VIZ_CHAT["7.10 Interactive RAG Message Stream<br/>• Markdown-rendered answer stream with code syntax highlighting<br/>• Clickable superscript citation badges [1], [2]"]:::vizComp
        
        VIZ_CARDS["7.11 Collapsible Citation Evidence Cards<br/>• Displays exact paper title, DOI clickable link, and text snippet<br/>• Direct evidence tracing without AI hallucinations"]:::vizComp
    end

    %% ─── EXPORT & USER OUTPUT PIPELINES ──────────────────────────────────────
    subgraph SUB_EXPORTS["PRESENTATION-READY EXPORT PIPELINES"]
        EXP_CSV["7.12 CSV Download with UTF-8 BOM (downloadCSV)<br/>Prepend UTF-8 BOM (\\xef\\xbb\\xbf) for Microsoft Excel compatibility<br/>Exports keyword frequency, presence matrix, or country collaborations"]:::exportAction
        
        EXP_JSON["7.13 JSON Metadata Export (downloadJSON)<br/>Exports complete structured analysis summary payload"]:::exportAction
        
        EXP_PNG["7.14 High-Resolution PNG Chart Export (svgToPng)<br/>Serializes SVG DOM, paints canvas background, renders high-res PNG for slides"]:::exportAction
        
        EXP_PDF["7.15 Direct / Proxy PDF Paper Downloads (filesApi.downloadPdf)<br/>Proxies open-access PDF streams directly to client browser"]:::exportAction
    end

    V_FINAL(["7.16 Final Research Insights Presented to User<br/>(Interactive Dashboards, Exported Reports, and Viva Presentation Assets)"]):::userOut

    %% Connections
    V_ENTRY --> EB_WRAP
    EB_WRAP --> SUB_GEO_VIZ & SUB_KW_VIZ & SUB_RAG_VIZ

    SUB_GEO_VIZ --> SUB_EXPORTS
    SUB_KW_VIZ --> SUB_EXPORTS
    SUB_RAG_VIZ --> SUB_EXPORTS

    SUB_EXPORTS --> V_FINAL
"""

def get_svg():
    w, h = 1850, 1300
    header = get_svg_header(
        w, h,
        title="Layer 7: Visualization & Output Layer Flowchart",
        subtitle="TopoJSON World Map, 2D/3D Force Networks, Word Cloud SVG, NetworkX Tables, RAG Citations & Export Pipelines",
        layer_badge="LAYER 07",
        theme_key="layer_07"
    )

    content = '''
  <!-- Inter-layer Connectivity Cards -->
  <g transform="translate(45, 115)">
    <rect x="0" y="0" width="380" height="42" rx="8" fill="#fffbeb" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="15" y="26" font-size="12" font-weight="bold" fill="#92400e">INPUT SOURCE:</text>
    <text x="120" y="26" font-size="12" fill="#334155">Layer 6: Analytical Engines &amp; Vector Stores</text>
  </g>
  <g transform="translate(1425, 115)">
    <rect x="0" y="0" width="380" height="42" rx="8" fill="#eff6ff" stroke="#2563eb" stroke-width="1.5"/>
    <text x="15" y="26" font-size="12" font-weight="bold" fill="#1e40af">FINAL RECIPIENT:</text>
    <text x="140" y="26" font-size="12" fill="#334155">Researcher / Student / M.Tech Evaluator</text>
  </g>

  <!-- 3 Major Presentation Pillars -->
  <!-- Pillar 1: Geographic & Collaboration Networks -->
  <g transform="translate(45, 175)">
    <rect x="0" y="0" width="560" height="1020" rx="14" fill="#fafafa" stroke="#e11d48" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="530" height="34" rx="6" fill="#ffe4e6"/>
    <text x="280" y="37" font-size="13" font-weight="bold" fill="#9f1239" text-anchor="middle">GEOGRAPHIC &amp; COLLABORATION VISUALIZATIONS</text>

    <!-- World Map -->
    <rect x="20" y="65" width="520" height="175" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="90" font-size="11.5" font-weight="bold" fill="#0f172a">7.1 TopoJSON Geographic World Map (WorldMap.tsx)</text>
    <text x="35" y="110" font-size="9.5" fill="#475569">• Framework: react-simple-maps + world-110m.json TopoJSON data</text>
    <text x="35" y="126" font-size="9.5" fill="#475569">• Aligns country records via ISO 3166-1 alpha-3 codes (get_country_iso3)</text>
    <text x="35" y="142" font-size="9.5" fill="#475569">• Color scales: Logarithmic / linear choropleth shading based on publication count</text>
    <text x="35" y="158" font-size="9.5" fill="#475569">• Interactive hover tooltips: displays country name, paper count, and corpus %</text>
    <text x="35" y="174" font-size="9.5" fill="#475569">• Full zoom &amp; pan controls with smooth spring animation</text>
    <text x="35" y="190" font-size="9.5" font-weight="bold" fill="#e11d48">• Wrapped in ErrorBoundary to prevent map failures from breaking the app</text>

    <!-- 2D Force Network -->
    <rect x="20" y="255" width="520" height="175" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="280" font-size="11.5" font-weight="bold" fill="#0f172a">7.2 2D Force-Directed Collaboration Network (CountryCollaboration2D.tsx)</text>
    <text x="35" y="300" font-size="9.5" fill="#475569">• Framework: react-force-graph-2d with D3 spring-charge physical simulation</text>
    <text x="35" y="316" font-size="9.5" fill="#475569">• Nodes: circle radius dynamically scaled by country publication volume</text>
    <text x="35" y="332" font-size="9.5" fill="#475569">• Links: line stroke width and opacity scaled by collaboration weight</text>
    <text x="35" y="348" font-size="9.5" fill="#475569">• Interactive drag, zoom, pan, and click-to-center physics navigation</text>
    <text x="35" y="364" font-size="9.5" fill="#475569">• Dark / Light mode canvas color adaptation with high-DPI retina rendering</text>
    <text x="35" y="380" font-size="9.5" font-weight="bold" fill="#e11d48">• Displays total collaboration edges count and connected component clusters</text>

    <!-- 3D WebGL Space -->
    <rect x="20" y="445" width="520" height="175" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="470" font-size="11.5" font-weight="bold" fill="#0f172a">7.3 3D WebGL Spherical Collaboration Space (CountryCollaboration3D.tsx)</text>
    <text x="35" y="490" font-size="9.5" fill="#475569">• Framework: react-force-graph-3d + Three.js WebGL rendering engine</text>
    <text x="35" y="506" font-size="9.5" fill="#475569">• Country sprite labels rendered in 3D billboard space via three-spritetext</text>
    <text x="35" y="522" font-size="9.5" fill="#475569">• Glowing particle flow animations along international collaboration links</text>
    <text x="35" y="538" font-size="9.5" fill="#475569">• Orbital camera controls: rotate, pitch, pan, and spherical zoom</text>
    <text x="35" y="554" font-size="9.5" fill="#475569">• Dark space aesthetic with dynamic lighting and bloom effects</text>
    <text x="35" y="570" font-size="9.5" font-weight="bold" fill="#e11d48">• Provides presentation-grade visual immersion for international research</text>

    <!-- Ranking & Unassigned Tables -->
    <rect x="20" y="635" width="520" height="160" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="660" font-size="11.5" font-weight="bold" fill="#0f172a">7.4 Country Ranking Tables &amp; Unassigned Modal</text>
    <text x="35" y="680" font-size="9.5" fill="#475569">• Filterable country volume ranking table with ISO-3 country pill badges</text>
    <text x="35" y="696" font-size="9.5" fill="#475569">• International collaboration pairs table with exact co-authorship counts</text>
    <text x="35" y="712" font-size="9.5" fill="#475569">• Unassigned papers inspection modal: reviews records lacking affiliations</text>
    <text x="35" y="728" font-size="9.5" fill="#475569">• Quick export button: triggers download of collaborations CSV</text>
  </g>

  <!-- Pillar 2: Keyword Analytics & Graph Centralities -->
  <g transform="translate(645, 175)">
    <rect x="0" y="0" width="560" height="1020" rx="14" fill="#fafafa" stroke="#e11d48" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="530" height="34" rx="6" fill="#ffe4e6"/>
    <text x="280" y="37" font-size="13" font-weight="bold" fill="#9f1239" text-anchor="middle">KEYWORD ANALYTICS &amp; GRAPH RENDERERS</text>

    <!-- Word Cloud -->
    <rect x="20" y="65" width="520" height="175" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="90" font-size="11.5" font-weight="bold" fill="#0f172a">7.5 Interactive SVG Word Cloud (AnalyticsPage.tsx)</text>
    <text x="35" y="110" font-size="9.5" fill="#475569">• Scalable vector text tokens placed via spiral packing algorithm</text>
    <text x="35" y="126" font-size="9.5" fill="#475569">• Font size scaled dynamically based on keyword frequency and bounds</text>
    <text x="35" y="142" font-size="9.5" fill="#475569">• Frequency-based color palette (accentuating dominant research topics)</text>
    <text x="35" y="158" font-size="9.5" fill="#475569">• Interactive hover tooltips displaying exact count and paper percentage</text>
    <text x="35" y="174" font-size="9.5" fill="#475569">• Click keyword token to filter downstream presence matrix</text>
    <text x="35" y="190" font-size="9.5" font-weight="bold" fill="#e11d48">• Clean SVG serialization enables direct high-res PNG export</text>

    <!-- Co-Occurrence Network Graph -->
    <rect x="20" y="255" width="520" height="175" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="280" font-size="11.5" font-weight="bold" fill="#0f172a">7.6 Keyword Co-Occurrence Network Graph SVG</text>
    <text x="35" y="300" font-size="9.5" fill="#475569">• Pure SVG force-directed simulation of semantic keyword links</text>
    <text x="35" y="316" font-size="9.5" fill="#475569">• Node radius reflects individual keyword publication volume</text>
    <text x="35" y="332" font-size="9.5" fill="#475569">• Edge stroke thickness represents co-occurrence pair strength</text>
    <text x="35" y="348" font-size="9.5" fill="#475569">• Interactive drag, zoom, pan, and fullscreen expansion controls</text>
    <text x="35" y="364" font-size="9.5" fill="#475569">• Degree-based node coloring highlights central disciplinary hub terms</text>
    <text x="35" y="380" font-size="9.5" font-weight="bold" fill="#e11d48">• Self-contained SVG paints background rect for crisp PNG export</text>

    <!-- Centrality Scores Table -->
    <rect x="20" y="445" width="520" height="175" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="470" font-size="11.5" font-weight="bold" fill="#0f172a">7.7 NetworkX Centrality Scores Table (AnalyticsPage.tsx)</text>
    <text x="35" y="490" font-size="9.5" fill="#475569">• Sortable 5-metric mathematical centrality table:</text>
    <text x="45" y="508" font-size="9" fill="#1e293b">• <b>Degree Centrality:</b> measures direct co-occurrence volume</text>
    <text x="45" y="524" font-size="9" fill="#1e293b">• <b>Closeness Centrality:</b> measures proximity across research graph</text>
    <text x="45" y="540" font-size="9" fill="#1e293b">• <b>Betweenness Centrality:</b> identifies bridging interdisciplinary terms</text>
    <text x="45" y="556" font-size="9" fill="#1e293b">• <b>Eigenvector Centrality:</b> identifies influence through connected hubs</text>
    <text x="45" y="572" font-size="9" fill="#1e293b">• <b>Clustering Coefficient:</b> measures modular cohesion of sub-topics</text>
    <text x="35" y="595" font-size="9.5" font-weight="bold" fill="#e11d48">• Tabular numbers formatting with copy and sorting interactions</text>

    <!-- Binary Presence Matrix Preview -->
    <rect x="20" y="635" width="520" height="160" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="660" font-size="11.5" font-weight="bold" fill="#0f172a">7.8 Binary Keyword Presence Matrix Grid</text>
    <text x="35" y="680" font-size="9.5" fill="#475569">• High-density 0/1 binary indicator grid</text>
    <text x="35" y="696" font-size="9.5" fill="#475569">• Rows: papers (Title, year, journal) • Columns: top keywords</text>
    <text x="35" y="712" font-size="9.5" fill="#475569">• Visual highlighting for present keywords (green pill 1 badges)</text>
    <text x="35" y="728" font-size="9.5" fill="#475569">• Controls for preview rows limit (12, 25, 50, 100 rows)</text>
  </g>

  <!-- Pillar 3: RAG Stream, Citation Cards & Export Pipelines -->
  <g transform="translate(1245, 175)">
    <rect x="0" y="0" width="560" height="1020" rx="14" fill="#fafafa" stroke="#e11d48" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="530" height="34" rx="6" fill="#ffe4e6"/>
    <text x="280" y="37" font-size="13" font-weight="bold" fill="#9f1239" text-anchor="middle">RAG CHAT STREAM &amp; EXPORT DELIVERABLES</text>

    <!-- Interactive RAG Chat -->
    <rect x="20" y="65" width="520" height="175" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="90" font-size="11.5" font-weight="bold" fill="#0f172a">7.9 Interactive RAG Message Stream (ChatPage.tsx)</text>
    <text x="35" y="110" font-size="9.5" fill="#475569">• Real-time message list with user questions and AI responses</text>
    <text x="35" y="126" font-size="9.5" fill="#475569">• Rendered Markdown formatting with code syntax highlighting</text>
    <text x="35" y="142" font-size="9.5" fill="#475569">• Clickable superscript citation badges [1], [2] inside answer body</text>
    <text x="35" y="158" font-size="9.5" fill="#475569">• Smooth scroll-to-bottom and typing loader animations</text>
    <text x="35" y="174" font-size="9.5" fill="#475569">• Input disabled automatically while embeddings are building</text>
    <text x="35" y="190" font-size="9.5" font-weight="bold" fill="#e11d48">• Displays model banner confirming Google Gemini + FAISS indexing</text>

    <!-- Citation Cards -->
    <rect x="20" y="255" width="520" height="175" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="280" font-size="11.5" font-weight="bold" fill="#0f172a">7.10 Collapsible Citation Evidence Cards</text>
    <text x="35" y="300" font-size="9.5" fill="#475569">• Accordion cards displaying exact evidence retrieved from FAISS vectors</text>
    <text x="35" y="316" font-size="9.5" fill="#475569">• Card header: [Source n] + Paper Title + DOI link badge</text>
    <text x="35" y="332" font-size="9.5" fill="#475569">• Card body: Extracted semantic chunk text snippet</text>
    <text x="35" y="348" font-size="9.5" fill="#475569">• Direct link opens official publisher or DOI landing page</text>
    <text x="35" y="364" font-size="9.5" fill="#475569">• Ensures complete transparency and academic verifiability</text>
    <text x="35" y="380" font-size="9.5" font-weight="bold" fill="#e11d48">• Prevents AI hallucinations during literature review tasks</text>

    <!-- Presentation-Ready Export Pipelines -->
    <rect x="20" y="445" width="520" height="350" rx="8" fill="#f0fdf4" stroke="#10b981" stroke-width="1.8"/>
    <rect x="25" y="450" width="510" height="26" rx="4" fill="#d1fae5"/>
    <text x="280" y="467" font-size="11" font-weight="bold" fill="#065f46" text-anchor="middle">PRESENTATION-READY EXPORT PIPELINES</text>

    <text x="35" y="495" font-size="10" font-weight="bold" fill="#064e3b">7.11 CSV Download with UTF-8 BOM (downloadCSV)</text>
    <text x="45" y="513" font-size="9" fill="#047857">• Prepends byte-order mark (\\xef\\xbb\\xbf) so Excel renders special characters</text>
    <text x="45" y="527" font-size="9" fill="#047857">• Exports keyword frequencies, presence matrix, or country collaborations</text>

    <text x="35" y="555" font-size="10" font-weight="bold" fill="#064e3b">7.12 JSON Analysis Export (downloadJSON)</text>
    <text x="45" y="573" font-size="9" fill="#047857">• Serializes full analysis summary payload with metadata and metrics</text>

    <text x="35" y="601" font-size="10" font-weight="bold" fill="#064e3b">7.13 High-Resolution PNG Chart Export (svgToPng)</text>
    <text x="45" y="619" font-size="9" fill="#047857">• Rasterizes SVG through HTML5 Canvas at scale=2 for 300 DPI clarity</text>
    <text x="45" y="633" font-size="9" fill="#047857">• Directly usable in PowerPoint slides and M.Tech thesis figures</text>

    <text x="35" y="661" font-size="10" font-weight="bold" fill="#064e3b">7.14 Direct / Proxy PDF Paper Downloads (filesApi.downloadPdf)</text>
    <text x="45" y="679" font-size="9" fill="#047857">• SSRF-validated proxy streams open-access PDF files directly to user disk</text>

    <text x="35" y="705" font-size="10" font-weight="bold" fill="#064e3b">7.15 Final Research Insights Presented to User</text>
    <text x="45" y="723" font-size="9" fill="#047857">• User review, viva examination defense, and research thesis completion</text>
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
                            facecolor="#BE123C", edgecolor="#9F1239", linewidth=1.5, zorder=2)
    ax.add_patch(header)
    ax.text(0.6, 11.45, "LAYER 07: VISUALIZATION & OUTPUT LAYER FLOWCHART", fontsize=15, fontweight='bold', color="#FFFFFF", zorder=3)
    ax.text(0.6, 11.08, "TopoJSON World Map, 2D/3D Force Networks, Word Cloud SVG, NetworkX Tables, RAG Citations & Export Pipelines", fontsize=9.5, color="#FFE4E6", zorder=3)
    ax.text(17.4, 11.25, "Research Rover v2.0", fontsize=10, fontweight='bold', color="#FDA4AF", ha='right', zorder=3)

    # Column 1: Geographic Visualizations
    col1 = FancyBboxPatch((0.5, 0.5), 5.4, 10.0, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#E11D48", linewidth=1.5, zorder=2)
    ax.add_patch(col1)
    ax.text(3.2, 10.2, "GEOGRAPHIC & COLLABORATION VIZ", fontsize=11, fontweight='bold', color="#9F1239", ha='center', zorder=3)

    ax.text(3.2, 9.4, "7.1 TopoJSON World Map (WorldMap.tsx)\n• react-simple-maps + world-110m.json\n• Logarithmic / linear choropleth shading\n• Hover tooltips: country name, count, %\n• Zoom & pan controls with spring physics\n• ErrorBoundary protected against crashes", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    ax.text(3.2, 6.8, "7.2 2D Force-Directed Network (2D.tsx)\n• react-force-graph-2d with D3 physics\n• Node radius scaled by publication volume\n• Link width scaled by collaboration weight\n• Drag, zoom, pan, and click-to-focus\n• High-DPI canvas retina rendering", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    ax.text(3.2, 4.4, "7.3 3D WebGL Spherical Space (3D.tsx)\n• react-force-graph-3d + Three.js\n• Country sprite labels (three-spritetext)\n• Glowing particle flows along collab links\n• 3D orbital camera rotation and pitch", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    ax.text(3.2, 2.2, "7.4 Ranking & Collab Tables\n• Filterable country volume table (ISO-3)\n• Co-authorship pairs with link weights\n• Unassigned papers review modal", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    # Column 2: Keyword & Graph Renderers
    col2 = FancyBboxPatch((6.2, 0.5), 5.4, 10.0, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#E11D48", linewidth=1.5, zorder=2)
    ax.add_patch(col2)
    ax.text(8.9, 10.2, "KEYWORD ANALYTICS & GRAPH SVG", fontsize=11, fontweight='bold', color="#9F1239", ha='center', zorder=3)

    ax.text(8.9, 9.4, "7.5 Interactive SVG Word Cloud\n• Spiral packing algorithm placement\n• Font size scaled by keyword frequency\n• Frequency color-coded tokens\n• Hover tooltip: exact count and corpus %\n• Click token to filter presence matrix", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    ax.text(8.9, 6.8, "7.6 Keyword Co-Occurrence Graph SVG\n• Pure SVG force-directed simulation\n• Node radius = keyword frequency\n• Edge thickness = co-occurrence count\n• Interactive drag, zoom, and fullscreen\n• Degree-based coloring highlights hubs", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    ax.text(8.9, 4.4, "7.7 NetworkX Centralities Table\n• Sortable 5-metric table:\n  Degree, Closeness, Betweenness,\n  Eigenvector, and Clustering\n• Tabular nums formatting & sorting", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    ax.text(8.9, 2.2, "7.8 Binary Keyword Presence Matrix\n• High-density 0/1 binary indicator grid\n• Rows: papers • Columns: top keywords\n• Green pill badges for present keywords\n• Preview rows controls (12-100 rows)", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    # Column 3: RAG Chat & Export Pipelines
    col3 = FancyBboxPatch((11.9, 0.5), 5.6, 10.0, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#E11D48", linewidth=1.5, zorder=2)
    ax.add_patch(col3)
    ax.text(14.7, 10.2, "RAG CHAT STREAM & EXPORTS", fontsize=11, fontweight='bold', color="#9F1239", ha='center', zorder=3)

    ax.text(14.7, 9.4, "7.9 Interactive RAG Chat Stream\n• Rendered Markdown with syntax styling\n• Superscript citation pills [1], [2]\n• Smooth scroll and typing animations\n• Verified Google Gemini + FAISS banner", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    ax.text(14.7, 7.4, "7.10 Collapsible Citation Evidence Cards\n• Accordion cards displaying retrieved chunks\n• Title, DOI link badge, extracted passage\n• Direct literature tracing without hallucination", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    ax.text(14.7, 5.0, "[Presentation-Ready Export Pipelines]\n7.11 CSV Export with UTF-8 BOM (downloadCSV)\n  Prepends \\xef\\xbb\\xbf for Excel compatibility\n7.12 JSON Metadata Export (downloadJSON)\n7.13 High-Res PNG Chart Export (svgToPng)\n  Canvas rasterization at scale=2 for 300 DPI\n7.14 Direct / Proxy PDF Paper Downloads", fontsize=8.5, color="#065F46", ha='center', zorder=3)

    ax.text(14.7, 1.8, "7.15 Final Research Insights Delivered\nInteractive dashboards, exported reports,\nand viva examination presentation deliverables", fontsize=8.5, fontweight='bold', color="#1E3A8A", ha='center', zorder=3)

    plt.tight_layout()
    plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated PNG: {png_path}")
