"""
scripts/render_layer_07.py
Layer 7: Visualization & User Output Layer (Pink)
Exact architecture extracted from reference.
"""

import os
from pathlib import Path
os.environ["MPLCONFIGDIR"] = os.environ.get("TEMP", "C:/Users/AkashDeep/AppData/Local/Temp")

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

from layer_helpers import save_all_formats

MMD_CONTENT = """flowchart TD
    %% =========================================================================
    %% LAYER 7: VISUALIZATION & USER OUTPUT LAYER (PINK)
    %% Standalone Enlarged Flowchart with Boundary Connectors
    %% =========================================================================

    classDef pinkNode fill:#FFF1F2,stroke:#E11D48,stroke-width:2.5px,color:#9F1239,font-size:14px;
    classDef wrapperNode fill:#FFE4E6,stroke:#BE123C,stroke-width:3px,color:#881337,font-weight:bold,font-size:15px;
    classDef outputNode fill:#F43F5E,stroke:#9F1239,stroke-width:3px,color:#FFFFFF,font-weight:bold,font-size:16px;
    classDef boundaryInL6 fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,stroke-dasharray: 5 5,color:#581C87,font-size:13px;

    subgraph IN_L6["INPUTS FROM LAYER 6 (ANALYSIS & COMPUTATION)"]
        IN_L6_KW_CACHE[["From Layer 6: Cached Summary Artifacts<br/>(data/*_summary.json)"]]:::boundaryInL6
        IN_L6_CTRY_STATS[["From Layer 6: Country Frequency & Coverage %"]]:::boundaryInL6
        IN_L6_CTRY_GRAPH[["From Layer 6: International Collaboration Graph"]]:::boundaryInL6
        IN_L6_RAG[["From Layer 6: RAG Chat Service<br/>(Synthesized Answers & Citations)"]]:::boundaryInL6
    end

    subgraph L7_CORE["LAYER 7: VISUALIZATION & USER OUTPUT LAYER"]
        ERR_BOUND["React Error Boundaries<br/>(components/ErrorBoundary.tsx)"]:::wrapperNode
        
        VIEW_KW["Keyword Analytics View<br/>(DashCards, WordCloudSvg, NetworkGraph)"]:::pinkNode
        VIEW_MAP["Geographic World Map<br/>(components/WorldMap.tsx - react-simple-maps)"]:::pinkNode
        VIEW_2D["2D Collaboration Network<br/>(components/CountryCollaboration2D.tsx - react-force-graph-2d)"]:::pinkNode
        VIEW_3D["3D Collaboration Network<br/>(components/CountryCollaboration3D.tsx - react-force-graph-3d)"]:::pinkNode
        VIEW_STATS["Summary Stats & Ranking Tables<br/>(components/CountryAnalysisView.tsx)"]:::pinkNode
        VIEW_CHAT["Interactive RAG Stream & Citations<br/>(pages/ChatPage.tsx)"]:::pinkNode
        
        U_OUTPUT(["User Insights & Exported CSV/JSON/PNG"]):::outputNode
    end

    %% Internal Connections
    IN_L6_KW_CACHE --> ERR_BOUND
    IN_L6_CTRY_STATS --> ERR_BOUND
    IN_L6_CTRY_GRAPH --> ERR_BOUND
    IN_L6_RAG --> VIEW_CHAT

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
"""

SVG_CONTENT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 950" width="100%" height="100%">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="2" dy="4" stdDeviation="4" flood-color="#000000" flood-opacity="0.12"/>
    </filter>
    <linearGradient id="pinkGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFF1F2"/>
      <stop offset="100%" stop-color="#FFE4E6"/>
    </linearGradient>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#BE123C"/>
      <stop offset="100%" stop-color="#E11D48"/>
    </linearGradient>
    <marker id="arrowPink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#E11D48"/>
    </marker>
    <marker id="arrowPurple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#9333EA"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1600" height="950" fill="#FFF1F2"/>
  <rect x="20" y="20" width="1560" height="910" rx="16" fill="#FFFFFF" stroke="#FECDD3" stroke-width="2"/>

  <!-- Header Banner -->
  <rect x="50" y="40" width="1500" height="70" rx="12" fill="url(#headerGrad)" filter="url(#shadow)"/>
  <text x="80" y="82" font-family="system-ui, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF">
    LAYER 7: VISUALIZATION &amp; USER OUTPUT LAYER
  </text>
  <text x="1060" y="82" font-family="system-ui, sans-serif" font-size="14" fill="#FFE4E6">
    Color Theme: Pink | Scope: Error Boundaries, 2D/3D Force Graphs &amp; User Delivery
  </text>

  <!-- Left: Inputs from Layer 6 -->
  <rect x="50" y="130" width="340" height="780" rx="14" fill="#FAF5FF" stroke="#9333EA" stroke-width="1.5" stroke-dasharray="5 4"/>
  <text x="75" y="160" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#7C3AED">
    INPUTS &larr; FROM LAYER 6
  </text>

  <g filter="url(#shadow)">
    <rect x="70" y="200" width="300" height="85" rx="10" fill="#FFFFFF" stroke="#9333EA" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="220" y="235" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#581C87" text-anchor="middle">
      From Layer 6: Summary Artifacts
    </text>
    <text x="220" y="258" font-family="monospace" font-size="11" fill="#7C3AED" text-anchor="middle">
      data/*_summary.json (Keywords)
    </text>
  </g>

  <g filter="url(#shadow)">
    <rect x="70" y="340" width="300" height="85" rx="10" fill="#FFFFFF" stroke="#9333EA" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="220" y="375" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#581C87" text-anchor="middle">
      From Layer 6: Country Statistics
    </text>
    <text x="220" y="398" font-family="monospace" font-size="11" fill="#7C3AED" text-anchor="middle">
      Publication Frequency &amp; Coverage %
    </text>
  </g>

  <g filter="url(#shadow)">
    <rect x="70" y="480" width="300" height="85" rx="10" fill="#FFFFFF" stroke="#9333EA" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="220" y="515" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#581C87" text-anchor="middle">
      From Layer 6: Collaboration Graph
    </text>
    <text x="220" y="538" font-family="monospace" font-size="11" fill="#7C3AED" text-anchor="middle">
      (Nodes &amp; Weighted Links Topology)
    </text>
  </g>

  <g filter="url(#shadow)">
    <rect x="70" y="650" width="300" height="85" rx="10" fill="#FFFFFF" stroke="#9333EA" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="220" y="685" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#581C87" text-anchor="middle">
      From Layer 6: RAG Chat Service
    </text>
    <text x="220" y="708" font-family="monospace" font-size="11" fill="#7C3AED" text-anchor="middle">
      (LLM Streaming Responses &amp; Citations)
    </text>
  </g>

  <!-- Center-Right Container: Layer 7 Core -->
  <rect x="420" y="130" width="1130" height="780" rx="14" fill="#FFF1F2" stroke="#E11D48" stroke-width="2.5" stroke-dasharray="6 4"/>
  <text x="445" y="160" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#BE123C">
    7. VISUALIZATION &amp; USER OUTPUT LAYER (Internal Architecture)
  </text>

  <!-- Error Boundary Wrapper Node -->
  <g filter="url(#shadow)">
    <rect x="450" y="190" width="1070" height="80" rx="12" fill="#FFE4E6" stroke="#BE123C" stroke-width="3"/>
    <text x="985" y="228" font-family="system-ui, sans-serif" font-size="17" font-weight="bold" fill="#881337" text-anchor="middle">
      React Error Boundaries Wrapper
    </text>
    <text x="985" y="252" font-family="monospace" font-size="12" fill="#9F1239" text-anchor="middle">
      (components/ErrorBoundary.tsx - Prevents unhandled crash in WebGL &amp; Canvas views)
    </text>
  </g>

  <!-- Arrows from Inputs into Error Boundary -->
  <path d="M 370 242 L 410 242 L 410 220 L 450 220" fill="none" stroke="#9333EA" stroke-width="2" marker-end="url(#arrowPurple)"/>
  <path d="M 370 382 L 410 382 L 410 230 L 450 230" fill="none" stroke="#9333EA" stroke-width="2" marker-end="url(#arrowPurple)"/>
  <path d="M 370 522 L 410 522 L 410 240 L 450 240" fill="none" stroke="#9333EA" stroke-width="2" marker-end="url(#arrowPurple)"/>

  <!-- Visualizations Grid (5 views from Error Boundary, 1 direct RAG view) -->
  <!-- 1. Keyword Analytics View -->
  <g filter="url(#shadow)">
    <rect x="450" y="310" width="330" height="95" rx="10" fill="url(#pinkGrad)" stroke="#E11D48" stroke-width="2.5"/>
    <text x="615" y="347" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#9F1239" text-anchor="middle">
      Keyword Analytics View
    </text>
    <text x="615" y="372" font-family="monospace" font-size="11" fill="#BE123C" text-anchor="middle">
      (DashCards, WordCloudSvg, Graph)
    </text>
  </g>
  <path d="M 615 270 L 615 310" stroke="#E11D48" stroke-width="2" marker-end="url(#arrowPink)"/>

  <!-- 2. Geographic World Map -->
  <g filter="url(#shadow)">
    <rect x="820" y="310" width="330" height="95" rx="10" fill="url(#pinkGrad)" stroke="#E11D48" stroke-width="2.5"/>
    <text x="985" y="347" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#9F1239" text-anchor="middle">
      Geographic World Map
    </text>
    <text x="985" y="372" font-family="monospace" font-size="11" fill="#BE123C" text-anchor="middle">
      (WorldMap.tsx - react-simple-maps)
    </text>
  </g>
  <path d="M 985 270 L 985 310" stroke="#E11D48" stroke-width="2" marker-end="url(#arrowPink)"/>

  <!-- 3. Summary Stats & Tables -->
  <g filter="url(#shadow)">
    <rect x="1190" y="310" width="330" height="95" rx="10" fill="url(#pinkGrad)" stroke="#E11D48" stroke-width="2.5"/>
    <text x="1355" y="347" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#9F1239" text-anchor="middle">
      Summary Stats &amp; Tables
    </text>
    <text x="1355" y="372" font-family="monospace" font-size="11" fill="#BE123C" text-anchor="middle">
      (CountryAnalysisView.tsx)
    </text>
  </g>
  <path d="M 1355 270 L 1355 310" stroke="#E11D48" stroke-width="2" marker-end="url(#arrowPink)"/>

  <!-- 4. 2D Collaboration Network -->
  <g filter="url(#shadow)">
    <rect x="450" y="450" width="330" height="95" rx="10" fill="url(#pinkGrad)" stroke="#E11D48" stroke-width="2.5"/>
    <text x="615" y="487" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#9F1239" text-anchor="middle">
      2D Collaboration Network
    </text>
    <text x="615" y="512" font-family="monospace" font-size="11" fill="#BE123C" text-anchor="middle">
      (react-force-graph-2d Canvas)
    </text>
  </g>
  <path d="M 615 270 L 430 270 L 430 497 L 450 497" fill="none" stroke="#E11D48" stroke-width="1.5" marker-end="url(#arrowPink)"/>

  <!-- 5. 3D Collaboration Network -->
  <g filter="url(#shadow)">
    <rect x="820" y="450" width="330" height="95" rx="10" fill="url(#pinkGrad)" stroke="#E11D48" stroke-width="2.5"/>
    <text x="985" y="487" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#9F1239" text-anchor="middle">
      3D Collaboration Network
    </text>
    <text x="985" y="512" font-family="monospace" font-size="11" fill="#BE123C" text-anchor="middle">
      (Three.js &amp; react-force-graph-3d)
    </text>
  </g>
  <path d="M 985 270 L 800 270 L 800 497 L 820 497" fill="none" stroke="#E11D48" stroke-width="1.5" marker-end="url(#arrowPink)"/>

  <!-- 6. Interactive RAG Stream & Citations (Direct from Layer 6 Chat) -->
  <g filter="url(#shadow)">
    <rect x="1190" y="450" width="330" height="95" rx="10" fill="url(#pinkGrad)" stroke="#E11D48" stroke-width="2.5"/>
    <text x="1355" y="487" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#9F1239" text-anchor="middle">
      Interactive RAG Stream
    </text>
    <text x="1355" y="512" font-family="monospace" font-size="11" fill="#BE123C" text-anchor="middle">
      (pages/ChatPage.tsx - Citations)
    </text>
  </g>
  <!-- Direct arrow from Chat Input -->
  <path d="M 370 692 L 1355 692 L 1355 545" fill="none" stroke="#9333EA" stroke-width="2" marker-end="url(#arrowPurple)"/>

  <!-- Converging Connections from All 6 Views to Final Output Node -->
  <!-- Final Terminal Output Node -->
  <g filter="url(#shadow)">
    <rect x="450" y="750" width="1070" height="85" rx="42.5" fill="#F43F5E" stroke="#9F1239" stroke-width="3"/>
    <text x="985" y="792" font-family="system-ui, sans-serif" font-size="20" font-weight="bold" fill="#FFFFFF" text-anchor="middle">
      User Insights &amp; Exported CSV / JSON / PNG
    </text>
    <text x="985" y="818" font-family="system-ui, sans-serif" font-size="13" fill="#FFE4E6" text-anchor="middle">
      (Final deliverable insights, high-resolution visual plots, and reproducible research artifacts)
    </text>
  </g>

  <!-- Arrows into Terminal Node -->
  <path d="M 615 545 L 615 750" stroke="#E11D48" stroke-width="2.5" marker-end="url(#arrowPink)"/>
  <path d="M 985 545 L 985 750" stroke="#E11D48" stroke-width="2.5" marker-end="url(#arrowPink)"/>
  <path d="M 1355 545 L 1355 750" stroke="#E11D48" stroke-width="2.5" marker-end="url(#arrowPink)"/>
</svg>
"""

def generate_layer_07():
    fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300)
    fig.patch.set_facecolor('#FFF1F2')
    ax.set_facecolor('#FFF1F2')
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 950)
    ax.axis('off')

    # Card background
    card = FancyBboxPatch((30, 30), 1540, 890, boxstyle="round,pad=10,rounding_size=20",
                          facecolor="#FFFFFF", edgecolor="#FECDD3", linewidth=2)
    ax.add_patch(card)

    # Header
    hdr = FancyBboxPatch((50, 840), 1500, 60, boxstyle="round,pad=5,rounding_size=12",
                         facecolor="#BE123C", edgecolor="none")
    ax.add_patch(hdr)
    ax.text(80, 870, "LAYER 7: VISUALIZATION & USER OUTPUT LAYER",
            fontsize=18, fontweight='bold', color="#FFFFFF", va='center')
    ax.text(1450, 870, "Theme: Pink | M.Tech Architecture Specification",
            fontsize=11, color="#FFE4E6", va='center', ha='right')

    # Left Container: Inputs from L6
    in_box = FancyBboxPatch((50, 60), 340, 750, boxstyle="round,pad=8,rounding_size=12",
                            facecolor="#FAF5FF", edgecolor="#9333EA", linewidth=1.5, linestyle="--")
    ax.add_patch(in_box)
    ax.text(75, 785, "INPUTS ← FROM LAYER 6", fontsize=11, fontweight='bold', color="#7C3AED")

    inputs = [
        ("From Layer 6: Summary Artifacts", "data/*_summary.json (Keywords)", 670),
        ("From Layer 6: Country Statistics", "Frequency & Coverage %", 530),
        ("From Layer 6: Collaboration Graph", "(Nodes & Links Topology)", 390),
        ("From Layer 6: RAG Chat Service", "(LLM Answers & Citations)", 250),
    ]

    for title, desc, y in inputs:
        box = FancyBboxPatch((70, y), 300, 75, boxstyle="round,pad=6,rounding_size=8",
                             facecolor="#FFFFFF", edgecolor="#9333EA", linewidth=2, linestyle="--")
        ax.add_patch(box)
        ax.text(220, y + 42, title, fontsize=10, fontweight='bold', color="#581C87", ha='center')
        ax.text(220, y + 20, desc, fontsize=8, fontfamily='monospace', color="#7C3AED", ha='center')

    # Center-Right Container: Layer 7 Core
    c_box = FancyBboxPatch((420, 60), 1130, 750, boxstyle="round,pad=8,rounding_size=12",
                           facecolor="#FFF1F2", edgecolor="#E11D48", linewidth=2.5, linestyle="--")
    ax.add_patch(c_box)
    ax.text(445, 785, "7. VISUALIZATION & USER OUTPUT LAYER (Internal Architecture)",
            fontsize=12, fontweight='bold', color="#BE123C")

    # Error Boundary Wrapper
    err_bound = FancyBboxPatch((450, 690), 1070, 70, boxstyle="round,pad=8,rounding_size=10",
                               facecolor="#FFE4E6", edgecolor="#BE123C", linewidth=3)
    ax.add_patch(err_bound)
    ax.text(985, 735, "React Error Boundaries Wrapper", fontsize=15, fontweight='bold', color="#881337", ha='center')
    ax.text(985, 710, "(components/ErrorBoundary.tsx - Prevents unhandled crashes in Canvas/WebGL views)",
            fontsize=10, fontfamily='monospace', color="#9F1239", ha='center')

    # Wiring from Inputs to Error Boundary
    ax.annotate('', xy=(450, 735), xytext=(370, 707),
                arrowprops=dict(arrowstyle="->", color="#9333EA", lw=2, mutation_scale=12))
    ax.annotate('', xy=(450, 725), xytext=(370, 567),
                arrowprops=dict(arrowstyle="->", color="#9333EA", lw=2, mutation_scale=12))
    ax.annotate('', xy=(450, 715), xytext=(370, 427),
                arrowprops=dict(arrowstyle="->", color="#9333EA", lw=2, mutation_scale=12))

    # Grid of Views (Row 1 and Row 2)
    views_row1 = [
        ("Keyword Analytics View", "(DashCards, WordCloudSvg, Graph)", 450, 560),
        ("Geographic World Map", "(WorldMap.tsx - react-simple-maps)", 820, 560),
        ("Summary Stats & Tables", "(CountryAnalysisView.tsx)", 1190, 560),
    ]

    views_row2 = [
        ("2D Collaboration Network", "(react-force-graph-2d Canvas)", 450, 420),
        ("3D Collaboration Network", "(Three.js & react-force-graph-3d)", 820, 420),
        ("Interactive RAG Stream", "(pages/ChatPage.tsx - Citations)", 1190, 420),
    ]

    for title, desc, x, y in views_row1 + views_row2:
        v_box = FancyBboxPatch((x, y), 330, 80, boxstyle="round,pad=6,rounding_size=8",
                               facecolor="#FFF1F2", edgecolor="#E11D48", linewidth=2.5)
        ax.add_patch(v_box)
        ax.text(x + 165, y + 45, title, fontsize=11, fontweight='bold', color="#9F1239", ha='center')
        ax.text(x + 165, y + 20, desc, fontsize=8, fontfamily='monospace', color="#BE123C", ha='center')

        # Downward arrows from Error Boundary to Row 1
        if y == 560:
            ax.annotate('', xy=(x + 165, y + 80), xytext=(x + 165, 690),
                        arrowprops=dict(arrowstyle="->", color="#E11D48", lw=1.5, mutation_scale=10))

    # Direct Arrow from RAG Input to RAG Chat View
    ax.plot([370, 1355, 1355], [287, 287, 420], color="#9333EA", lw=2)
    ax.annotate('', xy=(1355, 420), xytext=(1355, 410),
                arrowprops=dict(arrowstyle="->", color="#9333EA", lw=2, mutation_scale=12))

    # Terminal Node: User Insights & Exported CSV/JSON/PNG
    terminal = FancyBboxPatch((450, 160), 1070, 85, boxstyle="round,pad=10,rounding_size=35",
                              facecolor="#F43F5E", edgecolor="#9F1239", linewidth=3)
    ax.add_patch(terminal)
    ax.text(985, 215, "User Insights & Exported CSV / JSON / PNG", fontsize=16, fontweight='bold', color="#FFFFFF", ha='center')
    ax.text(985, 185, "(Final deliverable insights, high-resolution visual plots, and reproducible research artifacts)",
            fontsize=10, color="#FFE4E6", ha='center')

    # Arrows from views to terminal node
    for x in [615, 985, 1355]:
        ax.annotate('', xy=(x, 245), xytext=(x, 420),
                    arrowprops=dict(arrowstyle="->", color="#E11D48", lw=2, mutation_scale=12))

    save_all_formats("layer_07_visualization_output", MMD_CONTENT, SVG_CONTENT, fig)

if __name__ == "__main__":
    generate_layer_07()
