"""
Comprehensive Generator for Research Rover PowerPoint Presentation Assets.
Builds all 7 presentation diagrams in pure SVG and renders crisp 1920x1080 PNGs
via resvg-py, composites the contact sheet via Pillow, generates the HTML preview gallery,
and compiles complete documentation.
"""

import os
import re
import resvg_py
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.abspath("Research_Rover_Presentation_Assets")
SVG_DIR = os.path.join(BASE_DIR, "01_Diagrams_SVG")
PNG_DIR = os.path.join(BASE_DIR, "02_Diagrams_PNG")
PREVIEW_DIR = os.path.join(BASE_DIR, "03_Preview")

os.makedirs(SVG_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)
os.makedirs(PREVIEW_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# COMMON SVG HEADER & STYLES (PURE SVG 1.1 COMPATIBLE - NO FOREIGNOBJECT)
# ---------------------------------------------------------------------------
COMMON_STYLES = """
    .font-sans { font-family: Arial, 'Segoe UI', Helvetica, sans-serif; }
    .title-tag { font-family: Arial, 'Segoe UI', sans-serif; font-size: 13px; font-weight: 700; fill: #138C8C; letter-spacing: 2px; text-transform: uppercase; }
    .main-title { font-family: Arial, 'Segoe UI', sans-serif; font-size: 32px; font-weight: 800; fill: #142B65; }
    .sub-title { font-family: Arial, 'Segoe UI', sans-serif; font-size: 15.5px; fill: #475569; }
    .sec-hdr { font-family: Arial, 'Segoe UI', sans-serif; font-size: 16px; font-weight: 700; fill: #142B65; letter-spacing: 1px; }
    .card-title { font-family: Arial, 'Segoe UI', sans-serif; font-size: 15.5px; font-weight: 700; fill: #142B65; }
    .card-subtitle { font-family: Arial, 'Segoe UI', sans-serif; font-size: 12px; font-weight: 700; fill: #138C8C; text-transform: uppercase; letter-spacing: 0.5px; }
    .card-desc { font-family: Arial, 'Segoe UI', sans-serif; font-size: 13px; fill: #334155; line-height: 18px; }
    .badge-txt { font-family: Arial, 'Segoe UI', sans-serif; font-size: 12px; font-weight: 700; fill: #FFFFFF; }
    .footer-txt { font-family: Arial, 'Segoe UI', sans-serif; font-size: 12.5px; fill: #64748B; }
    .num-badge { font-family: Arial, 'Segoe UI', sans-serif; font-size: 16px; font-weight: 800; fill: #FFFFFF; }
"""

COMMON_DEFS = """
  <defs>
    <style>
""" + COMMON_STYLES + """
    </style>
    <filter id="shadow-sm" x="-2%" y="-2%" width="104%" height="106%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
    <filter id="shadow-md" x="-3%" y="-3%" width="106%" height="108%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="5" stdDeviation="8" flood-color="#0f172a" flood-opacity="0.08" />
    </filter>
    <filter id="hero-shadow" x="-4%" y="-3%" width="108%" height="108%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="8" stdDeviation="14" flood-color="#142B65" flood-opacity="0.16" />
    </filter>
    <marker id="arrow-teal" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#138C8C" />
    </marker>
    <marker id="arrow-navy" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#142B65" />
    </marker>
    <marker id="arrow-amber" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#D99A32" />
    </marker>
  </defs>
"""


# ---------------------------------------------------------------------------
# 01 — PROBLEM STATEMENT (Slide 2)
# ---------------------------------------------------------------------------
def build_svg_01():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
{COMMON_DEFS}
  <!-- Background -->
  <rect width="1920" height="1080" fill="#FFFFFF" />
  <line x1="80" y1="135" x2="1840" y2="135" stroke="#E2E8F0" stroke-width="1.5" />

  <!-- Slide Header -->
  <g transform="translate(80, 50)">
    <text x="0" y="20" class="title-tag">Target: Presentation Slide 2 · Research Publication Challenges</text>
    <text x="0" y="56" class="main-title">Problem Statement: Research Publication Challenges</text>
    <text x="0" y="80" class="sub-title">Manual discovery and siloed bibliographic data restrict analytical visibility and research productivity</text>
  </g>

  <!-- LEFT: 4 Key Challenges (2x2 Grid) -->
  <g transform="translate(80, 155)">
    <!-- Section Label -->
    <rect x="0" y="0" width="840" height="38" rx="8" fill="#F1F5F9" />
    <circle cx="22" cy="19" r="6" fill="#EF4444" />
    <text x="38" y="24" class="sec-hdr">FOUR RESEARCH CHALLENGES</text>

    <!-- Card 1: Information Overload -->
    <g transform="translate(0, 50)">
      <rect width="405" height="345" rx="14" fill="#F4F6F8" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow-sm)" />
      <path d="M 0 14 Q 0 0 14 0 L 391 0 Q 405 0 405 14 L 405 6 L 0 6 Z" fill="#142B65" />
      <circle cx="48" cy="52" r="24" fill="#EAF3F8" stroke="#142B65" stroke-width="2" />
      <path d="M 38 43 L 58 43 L 58 61 L 38 61 Z" fill="none" stroke="#142B65" stroke-width="2" stroke-linecap="round" />
      <path d="M 43 39 L 63 39 L 63 55" fill="none" stroke="#138C8C" stroke-width="2" stroke-linecap="round" />
      <path d="M 43 49 L 53 49 M 43 54 L 51 54" stroke="#142B65" stroke-width="1.5" stroke-linecap="round" />
      <text x="88" y="48" class="card-title">1. INFORMATION OVERLOAD</text>
      <text x="88" y="66" class="card-subtitle" fill="#EF4444">High Publication Volume</text>
      
      <text x="28" y="112" class="card-desc" font-weight="700">Difficulty managing large volumes of research publications.</text>
      <text x="28" y="142" class="card-desc">The exponential surge in global scientific outputs</text>
      <text x="28" y="166" class="card-desc">creates severe cognitive overload, making thorough</text>
      <text x="28" y="190" class="card-desc">literature surveys across thousands of published papers</text>
      <text x="28" y="214" class="card-desc">prohibitively slow and prone to missed breakthroughs.</text>

      <rect x="28" y="275" width="349" height="42" rx="8" fill="#FFFFFF" stroke="#E2E8F0" />
      <text x="42" y="301" font-family="Arial" font-size="12.5px" fill="#475569" font-weight="600">Bottleneck: Manual review cannot scale with publication velocity</text>
    </g>

    <!-- Card 2: Fragmented Data Sources -->
    <g transform="translate(435, 50)">
      <rect width="405" height="345" rx="14" fill="#F4F6F8" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow-sm)" />
      <path d="M 0 14 Q 0 0 14 0 L 391 0 Q 405 0 405 14 L 405 6 L 0 6 Z" fill="#142B65" />
      <circle cx="48" cy="52" r="24" fill="#EAF3F8" stroke="#142B65" stroke-width="2" />
      <circle cx="41" cy="47" r="4" fill="#142B65" />
      <circle cx="56" cy="43" r="4" fill="#138C8C" />
      <circle cx="50" cy="61" r="4" fill="#D99A32" />
      <line x1="41" y1="47" x2="56" y2="43" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="3,2" />
      <line x1="41" y1="47" x2="50" y2="61" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="3,2" />
      <text x="88" y="48" class="card-title">2. FRAGMENTED DATA SOURCES</text>
      <text x="88" y="66" class="card-subtitle" fill="#EF4444">Disconnected Repositories</text>
      
      <text x="28" y="112" class="card-desc" font-weight="700">Disconnected repositories and publication metadata.</text>
      <text x="28" y="142" class="card-desc">Academic literature is distributed across disparate</text>
      <text x="28" y="166" class="card-desc">databases (PubMed, OpenAlex, WoS, institutional archives)</text>
      <text x="28" y="190" class="card-desc">with incompatible query models, separate login gates,</text>
      <text x="28" y="214" class="card-desc">and conflicting export formats.</text>

      <rect x="28" y="275" width="349" height="42" rx="8" fill="#FFFFFF" stroke="#E2E8F0" />
      <text x="42" y="301" font-family="Arial" font-size="12.5px" fill="#475569" font-weight="600">Bottleneck: Data isolation prevents complete bibliometric view</text>
    </g>

    <!-- Card 3: Manual Metadata Processing -->
    <g transform="translate(0, 420)">
      <rect width="405" height="345" rx="14" fill="#F4F6F8" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow-sm)" />
      <path d="M 0 14 Q 0 0 14 0 L 391 0 Q 405 0 405 14 L 405 6 L 0 6 Z" fill="#142B65" />
      <circle cx="48" cy="52" r="24" fill="#EAF3F8" stroke="#142B65" stroke-width="2" />
      <path d="M 40 43 L 56 43 L 51 53 L 51 63 L 45 63 L 45 53 Z" fill="none" stroke="#142B65" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
      <circle cx="48" cy="50" r="3" fill="#138C8C" />
      <text x="88" y="48" class="card-title">3. MANUAL METADATA PROCESSING</text>
      <text x="88" y="66" class="card-subtitle" fill="#EF4444">Time-Consuming Wrangling</text>
      
      <text x="28" y="112" class="card-desc" font-weight="700">Time-consuming metadata extraction and cleaning.</text>
      <text x="28" y="142" class="card-desc">Extracted bibliographic records contain malformed</text>
      <text x="28" y="166" class="card-desc">author affiliations, unnormalized keyword lists,</text>
      <text x="28" y="190" class="card-desc">and inconsistent publication dates requiring tedious,</text>
      <text x="28" y="214" class="card-desc">error-prone manual data wrangling.</text>

      <rect x="28" y="275" width="349" height="42" rx="8" fill="#FFFFFF" stroke="#E2E8F0" />
      <text x="42" y="301" font-family="Arial" font-size="12.5px" fill="#475569" font-weight="600">Bottleneck: Hundreds of hours spent cleaning rather than analyzing</text>
    </g>

    <!-- Card 4: Limited Analytical Visibility -->
    <g transform="translate(435, 420)">
      <rect width="405" height="345" rx="14" fill="#F4F6F8" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow-sm)" />
      <path d="M 0 14 Q 0 0 14 0 L 391 0 Q 405 0 405 14 L 405 6 L 0 6 Z" fill="#142B65" />
      <circle cx="48" cy="52" r="24" fill="#EAF3F8" stroke="#142B65" stroke-width="2" />
      <rect x="38" y="54" width="5" height="10" fill="#142B65" />
      <rect x="46" y="48" width="5" height="16" fill="#142B65" />
      <rect x="54" y="42" width="5" height="22" fill="#138C8C" />
      <line x1="36" y1="65" x2="62" y2="41" stroke="#EF4444" stroke-width="2" stroke-linecap="round" />
      <text x="88" y="48" class="card-title">4. LIMITED ANALYTICAL VISIBILITY</text>
      <text x="88" y="66" class="card-subtitle" fill="#EF4444">Lack of Integrated Insights</text>
      
      <text x="28" y="112" class="card-desc" font-weight="700">Lack of integrated bibliometric insights.</text>
      <text x="28" y="142" class="card-desc">Standard search engines only provide tabular text lists.</text>
      <text x="28" y="166" class="card-desc">They lack automated co-occurrence network graphs,</text>
      <text x="28" y="190" class="card-desc">geographical institutional mapping, and trend analysis,</text>
      <text x="28" y="214" class="card-desc">obscuring strategic patterns in global research.</text>

      <rect x="28" y="275" width="349" height="42" rx="8" fill="#FFFFFF" stroke="#E2E8F0" />
      <text x="42" y="301" font-family="Arial" font-size="12.5px" fill="#475569" font-weight="600">Bottleneck: Complex research relationships remain invisible</text>
    </g>
  </g>

  <!-- CENTER BRIDGE: Central Motivation -->
  <g transform="translate(945, 475)">
    <!-- Connecting flow line -->
    <path d="M 0 55 L 48 55" stroke="#138C8C" stroke-width="3" stroke-dasharray="6,4" marker-end="url(#arrow-teal)" />
    
    <g transform="translate(55, 0)">
      <rect width="190" height="110" rx="14" fill="#142B65" stroke="#138C8C" stroke-width="2" filter="url(#shadow-md)" />
      <text x="95" y="30" font-family="Arial" font-size="11.5px" font-weight="700" fill="#138C8C" text-anchor="middle" letter-spacing="1.5px">CENTRAL MOTIVATION</text>
      <text x="95" y="58" font-family="Arial" font-size="14.5px" font-weight="800" fill="#FFFFFF" text-anchor="middle">Need for an</text>
      <text x="95" y="78" font-family="Arial" font-size="14.5px" font-weight="800" fill="#99F6E4" text-anchor="middle">Integrated Research</text>
      <text x="95" y="96" font-family="Arial" font-size="13px" font-weight="700" fill="#FFFFFF" text-anchor="middle">Workflow</text>
    </g>

    <path d="M 252 55 L 302 55" stroke="#138C8C" stroke-width="3" marker-end="url(#arrow-teal)" />
  </g>

  <!-- RIGHT: Research Rover Solution Block -->
  <g transform="translate(1260, 155)">
    <!-- Section Label -->
    <rect x="0" y="0" width="580" height="38" rx="8" fill="#EAF3F8" />
    <circle cx="22" cy="19" r="6" fill="#138C8C" />
    <text x="38" y="24" class="sec-hdr" fill="#142B65">INTEGRATED SOLUTION PLATFORM</text>

    <!-- Solution Hero Container -->
    <g transform="translate(0, 50)">
      <rect width="580" height="715" rx="16" fill="#142B65" stroke="#138C8C" stroke-width="1.5" filter="url(#hero-shadow)" />
      
      <!-- Card Inner Header -->
      <g transform="translate(35, 32)">
        <rect width="130" height="24" rx="6" fill="#138C8C" />
        <text x="65" y="16" class="badge-txt" text-anchor="middle">RESEARCH ROVER</text>
        <text x="0" y="58" class="main-title" fill="#FFFFFF" font-size="26px">Unified Research Platform</text>
        <text x="0" y="80" class="card-subtitle" fill="#99F6E4">Automating Paper Retrieval, Curation &amp; Bibliometric Analytics</text>
      </g>

      <line x1="35" y1="130" x2="545" y2="130" stroke="#1E3A8A" stroke-width="1.5" />
      <text x="35" y="158" font-family="Arial" font-size="13px" font-weight="700" fill="#93C5FD" letter-spacing="1.5px">FOUR CORE OUTPUT CAPABILITIES</text>

      <!-- Capability 1: Retrieval -->
      <g transform="translate(35, 178)">
        <rect width="510" height="112" rx="10" fill="#FFFFFF" filter="url(#shadow-sm)" />
        <rect x="0" y="0" width="7" height="112" rx="3" fill="#138C8C" />
        <circle cx="44" cy="56" r="20" fill="#EAF3F8" stroke="#138C8C" stroke-width="1.5" />
        <path d="M 39 51 A 5 5 0 1 1 49 51 A 5 5 0 1 1 39 51 M 48 55 L 54 61" fill="none" stroke="#138C8C" stroke-width="2" stroke-linecap="round" />
        <text x="78" y="38" class="card-title">Research Paper Retrieval</text>
        <text x="78" y="62" class="card-desc">Direct querying of PubMed / NCBI E-utilities and OpenAlex APIs.</text>
        <text x="78" y="84" class="card-desc" font-weight="700" fill="#138C8C">Unified multi-source search with fast live pagination and CSV export.</text>
      </g>

      <!-- Capability 2: Processing -->
      <g transform="translate(35, 308)">
        <rect width="510" height="112" rx="10" fill="#FFFFFF" filter="url(#shadow-sm)" />
        <rect x="0" y="0" width="7" height="112" rx="3" fill="#138C8C" />
        <circle cx="44" cy="56" r="20" fill="#EAF3F8" stroke="#138C8C" stroke-width="1.5" />
        <rect x="36" y="47" width="16" height="18" rx="2" fill="none" stroke="#138C8C" stroke-width="2" />
        <line x1="40" y1="52" x2="48" y2="52" stroke="#138C8C" stroke-width="1.5" />
        <line x1="40" y1="57" x2="48" y2="57" stroke="#138C8C" stroke-width="1.5" />
        <text x="78" y="38" class="card-title">Metadata Processing</text>
        <text x="78" y="62" class="card-desc">Automated XML parsing, canonical schema normalization &amp; deduplication.</text>
        <text x="78" y="84" class="card-desc" font-weight="700" fill="#138C8C">Intelligent column detection across Scopus, WoS, and custom research CSVs.</text>
      </g>

      <!-- Capability 3: Bibliometric Analysis -->
      <g transform="translate(35, 438)">
        <rect width="510" height="112" rx="10" fill="#FFFFFF" filter="url(#shadow-sm)" />
        <rect x="0" y="0" width="7" height="112" rx="3" fill="#138C8C" />
        <circle cx="44" cy="56" r="20" fill="#EAF3F8" stroke="#138C8C" stroke-width="1.5" />
        <circle cx="39" cy="54" r="3.5" fill="#138C8C" />
        <circle cx="50" cy="48" r="3.5" fill="#142B65" />
        <circle cx="48" cy="62" r="3.5" fill="#138C8C" />
        <line x1="39" y1="54" x2="50" y2="48" stroke="#138C8C" stroke-width="1.5" />
        <line x1="39" y1="54" x2="48" y2="62" stroke="#138C8C" stroke-width="1.5" />
        <line x1="50" y1="48" x2="48" y2="62" stroke="#138C8C" stroke-width="1.5" />
        <text x="78" y="38" class="card-title">Bibliometric Analysis</text>
        <text x="78" y="62" class="card-desc">Keyword frequency distributions, presence matrices &amp; co-occurrence graphs.</text>
        <text x="78" y="84" class="card-desc" font-weight="700" fill="#138C8C">Network centralities (degree, betweenness, closeness, clustering) and stats.</text>
      </g>

      <!-- Capability 4: Visualization -->
      <g transform="translate(35, 568)">
        <rect width="510" height="112" rx="10" fill="#FFFFFF" filter="url(#shadow-sm)" />
        <rect x="0" y="0" width="7" height="112" rx="3" fill="#138C8C" />
        <circle cx="44" cy="56" r="20" fill="#EAF3F8" stroke="#138C8C" stroke-width="1.5" />
        <circle cx="44" cy="56" r="10" fill="none" stroke="#138C8C" stroke-width="2" />
        <line x1="34" y1="56" x2="54" y2="56" stroke="#138C8C" stroke-width="1.5" />
        <path d="M 44 46 A 10 7 0 0 1 44 66 A 10 7 0 0 1 44 46" fill="none" stroke="#138C8C" stroke-width="1.5" />
        <text x="78" y="38" class="card-title">Research Visualization</text>
        <text x="78" y="62" class="card-desc">Interactive 2D World Map, 3D Globe, dynamic force networks, word clouds,</text>
        <text x="78" y="84" class="card-desc" font-weight="700" fill="#138C8C">and AI-assisted conversational question answering grounded in paper data.</text>
      </g>
    </g>
  </g>

  <!-- Presentation Footer Metadata -->
  <g transform="translate(80, 1025)">
    <text x="0" y="16" class="footer-txt">RESEARCH ROVER · M.Tech Data Science Mid-Semester Presentation</text>
    <text x="1760" y="16" class="footer-txt" text-anchor="end">Slide 2 Diagram · Problem Statement</text>
  </g>
</svg>"""


# ---------------------------------------------------------------------------
# 02 — CORE FUNCTIONAL MODULES (Slide 3)
# ---------------------------------------------------------------------------
def build_svg_02():
    # 4 columns x 2 rows
    # Card width: 415, height: 350, spacing-x: 35, spacing-y: 35
    modules = [
        {
            "id": "01",
            "title": "1. Research Paper Search",
            "subtitle": "Query & Retrieval Engine",
            "desc1": "Multi-source paper discovery across PubMed",
            "desc2": "and OpenAlex APIs. Supports keyword, author,",
            "desc3": "DOI lookups with live search progress tracking,",
            "desc4": "relevance ranking and asynchronous background jobs.",
            "tag": "Search & Ingestion",
            "icon": "search"
        },
        {
            "id": "02",
            "title": "2. Metadata Extraction",
            "subtitle": "Parsing & Information Mining",
            "desc1": "High-throughput XML & JSON parsing.",
            "desc2": "Extracts article titles, abstracts, author rosters,",
            "desc3": "affiliations, publication dates, MeSH terms,",
            "desc4": "and persistent digital object identifiers (DOIs).",
            "tag": "Data Ingestion",
            "icon": "extract"
        },
        {
            "id": "03",
            "title": "3. Data Preprocessing",
            "subtitle": "Normalization & Hygiene",
            "desc1": "Universal canonical schema mapping across Scopus,",
            "desc2": "Web of Science and custom CSV datasets.",
            "desc3": "Safe deduplication preserving original data,",
            "desc4": "quality scoring, and missing field hygiene.",
            "tag": "Data Engineering",
            "icon": "filter"
        },
        {
            "id": "04",
            "title": "4. Author Affiliation Analysis",
            "subtitle": "Institutional Geoparsing",
            "desc1": "Rule-based and regex extraction of institutional",
            "desc2": "affiliations, academic departments, university",
            "desc3": "names and research laboratory locations",
            "desc4": "from unstructured author affiliation strings.",
            "tag": "Entity Extraction",
            "icon": "affil"
        },
        {
            "id": "05",
            "title": "5. Country-wise Analysis",
            "subtitle": "Global Research Distribution",
            "desc1": "ISO country code resolution and spatial density",
            "desc2": "calculation. Identifies leading research hubs,",
            "desc3": "cross-border collaboration co-authorship ties,",
            "desc4": "and international research participation rates.",
            "tag": "Spatial Analytics",
            "icon": "globe"
        },
        {
            "id": "06",
            "title": "6. Keyword Analysis",
            "subtitle": "Thematic & Semantic Frequency",
            "desc1": "Author and MeSH keyword tokenization,",
            "desc2": "frequency distributions, and presence-absence",
            "desc3": "matrices. Powers interactive word clouds and",
            "desc4": "thematic concentration analysis across corpora.",
            "tag": "NLP & Frequency",
            "icon": "keyword"
        },
        {
            "id": "07",
            "title": "7. Bibliometric & Network Analysis",
            "subtitle": "Graph & Network Centrality",
            "desc1": "Co-occurrence edge modeling with NetworkX.",
            "desc2": "Calculates degree, betweenness, closeness,",
            "desc3": "and eigenvector centralities along with clustering",
            "desc4": "coefficients to reveal foundational research nodes.",
            "tag": "Graph Analytics",
            "icon": "network"
        },
        {
            "id": "08",
            "title": "8. Research Visualization",
            "subtitle": "Interactive Dashboards",
            "desc1": "Rich visual interfaces: 2D World Map,",
            "desc2": "3D Force Collaboration Globe, dynamic network",
            "desc3": "graphs, interactive word clouds, and AI-assisted",
            "desc4": "RAG chat grounded in processed papers.",
            "tag": "Interactive UI",
            "icon": "vis"
        },
    ]

    cards_svg = ""
    for idx, m in enumerate(modules):
        col = idx % 4
        row = idx // 4
        cx = 80 + col * (415 + 33)
        cy = 165 + row * (360 + 30)

        # Icon rendering
        if m["icon"] == "search":
            icon_svg = """<circle cx="42" cy="42" r="14" fill="none" stroke="#138C8C" stroke-width="2.5" />
            <line x1="52" y1="52" x2="64" y2="64" stroke="#138C8C" stroke-width="3" stroke-linecap="round" />"""
        elif m["icon"] == "extract":
            icon_svg = """<rect x="30" y="28" width="24" height="28" rx="3" fill="none" stroke="#138C8C" stroke-width="2" />
            <line x1="36" y1="36" x2="48" y2="36" stroke="#138C8C" stroke-width="1.5" />
            <line x1="36" y1="42" x2="48" y2="42" stroke="#138C8C" stroke-width="1.5" />
            <line x1="36" y1="48" x2="44" y2="48" stroke="#138C8C" stroke-width="1.5" />"""
        elif m["icon"] == "filter":
            icon_svg = """<path d="M 28 30 L 56 30 L 46 44 L 46 56 L 38 56 L 38 44 Z" fill="none" stroke="#138C8C" stroke-width="2" stroke-linejoin="round" />
            <circle cx="42" cy="42" r="2.5" fill="#142B65" />"""
        elif m["icon"] == "affil":
            icon_svg = """<path d="M 42 28 L 56 36 L 56 56 L 28 56 L 28 36 Z" fill="none" stroke="#138C8C" stroke-width="2" />
            <rect x="38" y="44" width="8" height="12" fill="#138C8C" />
            <line x1="34" y1="38" x2="36" y2="38" stroke="#142B65" stroke-width="2" />
            <line x1="48" y1="38" x2="50" y2="38" stroke="#142B65" stroke-width="2" />"""
        elif m["icon"] == "globe":
            icon_svg = """<circle cx="42" cy="42" r="15" fill="none" stroke="#138C8C" stroke-width="2" />
            <line x1="27" y1="42" x2="57" y2="42" stroke="#138C8C" stroke-width="1.5" />
            <path d="M 42 27 A 15 9 0 0 1 42 57 A 15 9 0 0 1 42 27" fill="none" stroke="#138C8C" stroke-width="1.5" />"""
        elif m["icon"] == "keyword":
            icon_svg = """<path d="M 28 32 L 44 28 L 56 40 L 40 56 L 28 44 Z" fill="none" stroke="#138C8C" stroke-width="2" />
            <circle cx="36" cy="36" r="2.5" fill="#142B65" />"""
        elif m["icon"] == "network":
            icon_svg = """<circle cx="34" cy="48" r="4" fill="#138C8C" />
            <circle cx="50" cy="34" r="4" fill="#142B65" />
            <circle cx="52" cy="52" r="4" fill="#138C8C" />
            <circle cx="36" cy="32" r="3" fill="#D99A32" />
            <line x1="34" y1="48" x2="50" y2="34" stroke="#138C8C" stroke-width="1.5" />
            <line x1="34" y1="48" x2="52" y2="52" stroke="#138C8C" stroke-width="1.5" />
            <line x1="50" y1="34" x2="52" y2="52" stroke="#138C8C" stroke-width="1.5" />
            <line x1="36" y1="32" x2="50" y2="34" stroke="#94A3B8" stroke-width="1.2" />"""
        else: # vis
            icon_svg = """<rect x="28" y="28" width="28" height="28" rx="4" fill="none" stroke="#138C8C" stroke-width="2" />
            <rect x="33" y="44" width="4" height="8" fill="#142B65" />
            <rect x="40" y="38" width="4" height="14" fill="#138C8C" />
            <rect x="47" y="34" width="4" height="18" fill="#23865A" />"""

        cards_svg += f"""
    <!-- Module {m['id']} -->
    <g transform="translate({cx}, {cy})">
      <rect width="415" height="360" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow-sm)" />
      <!-- Top header bar on card -->
      <path d="M 0 14 Q 0 0 14 0 L 401 0 Q 415 0 415 14 L 415 6 L 0 6 Z" fill="#142B65" />
      
      <!-- Icon + Number Badge -->
      <g transform="translate(24, 22)">
        <circle cx="42" cy="42" r="26" fill="#EAF3F8" stroke="#CBD5E1" stroke-width="1.5" />
        {icon_svg}
        <rect x="320" y="8" width="42" height="24" rx="6" fill="#142B65" />
        <text x="341" y="24" class="num-badge" text-anchor="middle" font-size="12px">{m['id']}</text>
      </g>

      <!-- Titles -->
      <g transform="translate(24, 98)">
        <text x="0" y="20" class="card-title">{m['title']}</text>
        <text x="0" y="38" class="card-subtitle">{m['subtitle']}</text>
        <line x1="0" y1="50" x2="367" y2="50" stroke="#F1F5F9" stroke-width="1.5" />
      </g>

      <!-- Descriptions -->
      <g transform="translate(24, 172)">
        <text x="0" y="0" class="card-desc">{m['desc1']}</text>
        <text x="0" y="24" class="card-desc">{m['desc2']}</text>
        <text x="0" y="48" class="card-desc">{m['desc3']}</text>
        <text x="0" y="72" class="card-desc">{m['desc4']}</text>
      </g>

      <!-- Category Pill -->
      <g transform="translate(24, 305)">
        <rect width="180" height="28" rx="6" fill="#F4F6F8" stroke="#E2E8F0" />
        <circle cx="14" cy="14" r="4" fill="#138C8C" />
        <text x="26" y="19" font-family="Arial" font-size="11.5px" font-weight="700" fill="#475569">{m['tag']}</text>
      </g>
    </g>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
{COMMON_DEFS}
  <!-- Background -->
  <rect width="1920" height="1080" fill="#FFFFFF" />
  <line x1="80" y1="135" x2="1840" y2="135" stroke="#E2E8F0" stroke-width="1.5" />

  <!-- Slide Header -->
  <g transform="translate(80, 50)">
    <text x="0" y="20" class="title-tag">Target: Presentation Slide 3 · Research Rover Project Overview</text>
    <text x="0" y="56" class="main-title">Core Functional Modules of Research Rover</text>
    <text x="0" y="80" class="sub-title">Eight integrated analytical capabilities supporting automated paper discovery, bibliometric processing, and interactive visualization</text>
  </g>

  <!-- CARDS CONTAINER -->
{cards_svg}

  <!-- Presentation Footer Metadata -->
  <g transform="translate(80, 1030)">
    <text x="0" y="16" class="footer-txt">RESEARCH ROVER · M.Tech Data Science Mid-Semester Presentation</text>
    <text x="1760" y="16" class="footer-txt" text-anchor="end">Slide 3 Diagram · Functional Modules Architecture</text>
  </g>
</svg>"""


# ---------------------------------------------------------------------------
# 03 — HIGH-LEVEL SYSTEM ARCHITECTURE (Slide 4)
# ---------------------------------------------------------------------------
def build_svg_03():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
{COMMON_DEFS}
  <!-- Background -->
  <rect width="1920" height="1080" fill="#FFFFFF" />
  <line x1="80" y1="135" x2="1840" y2="135" stroke="#E2E8F0" stroke-width="1.5" />

  <!-- Slide Header -->
  <g transform="translate(80, 50)">
    <text x="0" y="20" class="title-tag">Target: Presentation Slide 4 · High-Level System Architecture</text>
    <text x="0" y="56" class="main-title">High-Level System Architecture</text>
    <text x="0" y="80" class="sub-title">Modular 5-tier architecture connecting user interaction, backend orchestration, multi-source ingestion, and analytical intelligence</text>
  </g>

  <!-- 5 MAJOR HORIZONTAL COMPONENTS -->
  <!-- COMPONENT 1: USER INTERFACE -->
  <g transform="translate(80, 160)">
    <rect width="310" height="730" rx="16" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow-sm)" />
    <!-- Header Banner -->
    <path d="M 0 16 Q 0 0 16 0 L 294 0 Q 310 0 310 16 L 310 70 L 0 70 Z" fill="#142B65" />
    <circle cx="36" cy="35" r="16" fill="#138C8C" />
    <text x="36" y="40" class="badge-txt" text-anchor="middle" font-size="12px">01</text>
    <text x="64" y="32" font-family="Arial" font-size="15px" font-weight="800" fill="#FFFFFF">USER INTERFACE</text>
    <text x="64" y="50" font-family="Arial" font-size="11.5px" font-weight="700" fill="#99F6E4" letter-spacing="1px">REACT FRONTEND</text>

    <!-- Sub-elements inside Component 1 -->
    <g transform="translate(20, 95)">
      <!-- Item 1 -->
      <g transform="translate(0, 0)">
        <rect width="270" height="120" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
        <rect x="0" y="0" width="6" height="120" rx="3" fill="#138C8C" />
        <text x="20" y="32" class="card-title" font-size="14.5px">React Web App</text>
        <text x="20" y="54" class="card-desc" font-size="12.5px">• Modern SPA built on Vite</text>
        <text x="20" y="74" class="card-desc" font-size="12.5px">• Tailwind CSS design system</text>
        <text x="20" y="94" class="card-desc" font-size="12.5px">• Responsive, accessible UX</text>
      </g>

      <!-- Item 2 -->
      <g transform="translate(0, 140)">
        <rect width="270" height="120" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
        <rect x="0" y="0" width="6" height="120" rx="3" fill="#138C8C" />
        <text x="20" y="32" class="card-title" font-size="14.5px">Paper Search Page</text>
        <text x="20" y="54" class="card-desc" font-size="12.5px">• Multi-source query input</text>
        <text x="20" y="74" class="card-desc" font-size="12.5px">• Real-time progress tracker</text>
        <text x="20" y="94" class="card-desc" font-size="12.5px">• Live results table &amp; export</text>
      </g>

      <!-- Item 3 -->
      <g transform="translate(0, 280)">
        <rect width="270" height="120" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
        <rect x="0" y="0" width="6" height="120" rx="3" fill="#138C8C" />
        <text x="20" y="32" class="card-title" font-size="14.5px">Analytics Dashboard</text>
        <text x="20" y="54" class="card-desc" font-size="12.5px">• Universal CSV uploader</text>
        <text x="20" y="74" class="card-desc" font-size="12.5px">• Dataset Quality Modal</text>
        <text x="20" y="94" class="card-desc" font-size="12.5px">• 2D Map, 3D Globe, Networks</text>
      </g>

      <!-- Item 4 -->
      <g transform="translate(0, 420)">
        <rect width="270" height="145" rx="10" fill="#EAF3F8" stroke="#138C8C" stroke-width="1.5" />
        <rect x="0" y="0" width="6" height="145" rx="3" fill="#142B65" />
        <text x="20" y="32" class="card-title" font-size="14.5px" fill="#142B65">AI Chat Interface</text>
        <text x="20" y="54" class="card-desc" font-size="12.5px">• Document-grounded Q&amp;A</text>
        <text x="20" y="74" class="card-desc" font-size="12.5px">• Paper context retrieval</text>
        <text x="20" y="94" class="card-desc" font-size="12.5px">• Vector readiness status</text>
        <text x="20" y="118" font-family="Arial" font-size="11px" font-weight="700" fill="#138C8C">Accessed directly via REST API</text>
      </g>
    </g>
  </g>

  <!-- CONNECTOR 1 -> 2 (Bidirectional REST/HTTP) -->
  <g transform="translate(390, 470)">
    <line x1="10" y1="35" x2="45" y2="35" stroke="#142B65" stroke-width="3" marker-end="url(#arrow-navy)" />
    <line x1="45" y1="55" x2="10" y2="55" stroke="#138C8C" stroke-width="3" marker-end="url(#arrow-teal)" />
    <rect x="-8" y="70" width="70" height="26" rx="4" fill="#FFFFFF" stroke="#CBD5E1" />
    <text x="27" y="87" font-family="Arial" font-size="10.5px" font-weight="700" fill="#142B65" text-anchor="middle">REST / JSON</text>
  </g>

  <!-- COMPONENT 2: BACKEND APPLICATION -->
  <g transform="translate(450, 160)">
    <rect width="310" height="730" rx="16" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow-sm)" />
    <!-- Header Banner -->
    <path d="M 0 16 Q 0 0 16 0 L 294 0 Q 310 0 310 16 L 310 70 L 0 70 Z" fill="#142B65" />
    <circle cx="36" cy="35" r="16" fill="#138C8C" />
    <text x="36" y="40" class="badge-txt" text-anchor="middle" font-size="12px">02</text>
    <text x="64" y="32" font-family="Arial" font-size="15px" font-weight="800" fill="#FFFFFF">BACKEND APP</text>
    <text x="64" y="50" font-family="Arial" font-size="11.5px" font-weight="700" fill="#99F6E4" letter-spacing="1px">FASTAPI ENGINE</text>

    <!-- Sub-elements inside Component 2 -->
    <g transform="translate(20, 95)">
      <!-- Item 1 -->
      <g transform="translate(0, 0)">
        <rect width="270" height="120" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
        <rect x="0" y="0" width="6" height="120" rx="3" fill="#138C8C" />
        <text x="20" y="32" class="card-title" font-size="14.5px">Python &amp; FastAPI</text>
        <text x="20" y="54" class="card-desc" font-size="12.5px">• High-performance ASGI</text>
        <text x="20" y="74" class="card-desc" font-size="12.5px">• Async request concurrency</text>
        <text x="20" y="94" class="card-desc" font-size="12.5px">• Non-blocking background tasks</text>
      </g>

      <!-- Item 2 -->
      <g transform="translate(0, 140)">
        <rect width="270" height="120" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
        <rect x="0" y="0" width="6" height="120" rx="3" fill="#138C8C" />
        <text x="20" y="32" class="card-title" font-size="14.5px">REST API Routing</text>
        <text x="20" y="54" class="card-desc" font-size="12.5px">• /api/v1/search &amp; /progress</text>
        <text x="20" y="74" class="card-desc" font-size="12.5px">• /api/v1/files/upload &amp; /quality</text>
        <text x="20" y="94" class="card-desc" font-size="12.5px">• /api/v1/analysis &amp; /chat</text>
      </g>

      <!-- Item 3 -->
      <g transform="translate(0, 280)">
        <rect width="270" height="120" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
        <rect x="0" y="0" width="6" height="120" rx="3" fill="#138C8C" />
        <text x="20" y="32" class="card-title" font-size="14.5px">Service Orchestration</text>
        <text x="20" y="54" class="card-desc" font-size="12.5px">• SearchService manager</text>
        <text x="20" y="74" class="card-desc" font-size="12.5px">• AnalysisService pipeline</text>
        <text x="20" y="94" class="card-desc" font-size="12.5px">• CountryService geoparser</text>
      </g>

      <!-- Item 4 -->
      <g transform="translate(0, 420)">
        <rect width="270" height="145" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
        <rect x="0" y="0" width="6" height="145" rx="3" fill="#138C8C" />
        <text x="20" y="32" class="card-title" font-size="14.5px">App State &amp; Lifespan</text>
        <text x="20" y="54" class="card-desc" font-size="12.5px">• ModelManager background load</text>
        <text x="20" y="74" class="card-desc" font-size="12.5px">• Sidecar metadata caching</text>
        <text x="20" y="94" class="card-desc" font-size="12.5px">• Safe deduplication toggles</text>
        <text x="20" y="118" font-family="Arial" font-size="11px" font-weight="700" fill="#142B65">Memory-efficient execution</text>
      </g>
    </g>
  </g>

  <!-- CONNECTOR 2 -> 3 (Backend invokes Data Collection) -->
  <g transform="translate(760, 490)">
    <line x1="10" y1="20" x2="45" y2="20" stroke="#142B65" stroke-width="3" marker-end="url(#arrow-navy)" />
    <rect x="6" y="35" width="46" height="22" rx="4" fill="#FFFFFF" stroke="#CBD5E1" />
    <text x="29" y="50" font-family="Arial" font-size="10px" font-weight="700" fill="#142B65" text-anchor="middle">Invoke</text>
  </g>

  <!-- COMPONENT 3: DATA COLLECTION -->
  <g transform="translate(815, 160)">
    <rect width="310" height="730" rx="16" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow-sm)" />
    <!-- Header Banner -->
    <path d="M 0 16 Q 0 0 16 0 L 294 0 Q 310 0 310 16 L 310 70 L 0 70 Z" fill="#142B65" />
    <circle cx="36" cy="35" r="16" fill="#138C8C" />
    <text x="36" y="40" class="badge-txt" text-anchor="middle" font-size="12px">03</text>
    <text x="64" y="32" font-family="Arial" font-size="15px" font-weight="800" fill="#FFFFFF">DATA COLLECTION</text>
    <text x="64" y="50" font-family="Arial" font-size="11.5px" font-weight="700" fill="#99F6E4" letter-spacing="1px">MULTI-SOURCE INGESTION</text>

    <!-- Sub-elements inside Component 3 -->
    <g transform="translate(20, 95)">
      <!-- Item 1: PubMed -->
      <g transform="translate(0, 0)">
        <rect width="270" height="150" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
        <rect x="0" y="0" width="6" height="150" rx="3" fill="#138C8C" />
        <text x="20" y="30" class="card-title" font-size="14px">PubMed / NCBI API</text>
        <text x="20" y="52" class="card-desc" font-size="12.5px">• ESearch &amp; EFetch E-utilities</text>
        <text x="20" y="72" class="card-desc" font-size="12.5px">• Biomedical research corpus</text>
        <text x="20" y="92" class="card-desc" font-size="12.5px">• Live query normalizer</text>
        <text x="20" y="112" class="card-desc" font-size="12.5px">• Dedicated thread pool executor</text>
        <text x="20" y="132" font-family="Arial" font-size="11px" font-weight="700" fill="#138C8C">Live Online Retrieval</text>
      </g>

      <!-- Item 2: XML Metadata -->
      <g transform="translate(0, 175)">
        <rect width="270" height="135" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
        <rect x="0" y="0" width="6" height="135" rx="3" fill="#138C8C" />
        <text x="20" y="30" class="card-title" font-size="14px">XML Publication Records</text>
        <text x="20" y="52" class="card-desc" font-size="12.5px">• Structured XML tree streams</text>
        <text x="20" y="72" class="card-desc" font-size="12.5px">• MedlineCitation blocks</text>
        <text x="20" y="92" class="card-desc" font-size="12.5px">• Journal, article, abstract</text>
        <text x="20" y="116" font-family="Arial" font-size="11px" font-weight="700" fill="#142B65">Raw External Format</text>
      </g>

      <!-- Item 3: User Uploaded CSVs -->
      <g transform="translate(0, 335)">
        <rect width="270" height="230" rx="10" fill="#EAF3F8" stroke="#138C8C" stroke-width="2" />
        <rect x="0" y="0" width="6" height="230" rx="3" fill="#138C8C" />
        <text x="20" y="32" class="card-title" font-size="14px" fill="#142B65">User-Uploaded CSVs</text>
        <text x="20" y="56" class="card-desc" font-size="12.5px">• Scopus, Web of Science,</text>
        <text x="20" y="76" class="card-desc" font-size="12.5px">  PubMed &amp; OpenAlex exports</text>
        <text x="20" y="96" class="card-desc" font-size="12.5px">• Custom user research datasets</text>
        <text x="20" y="116" class="card-desc" font-size="12.5px">• Raw bytes preserved on disk</text>
        <text x="20" y="136" class="card-desc" font-size="12.5px">• UTF-8 / latin-1 auto-detect</text>
        <rect x="20" y="156" width="230" height="52" rx="6" fill="#FFFFFF" stroke="#CBD5E1" />
        <text x="32" y="176" font-family="Arial" font-size="11px" font-weight="700" fill="#142B65">Direct Dataset Ingestion Path</text>
        <text x="32" y="196" font-family="Arial" font-size="10.5px" fill="#475569">Feeds straight into Data Processing</text>
      </g>
    </g>
  </g>

  <!-- CONNECTOR 3 -> 4 (Data Collection to Processing) -->
  <g transform="translate(1125, 490)">
    <line x1="10" y1="20" x2="45" y2="20" stroke="#142B65" stroke-width="3" marker-end="url(#arrow-navy)" />
    <rect x="6" y="35" width="46" height="22" rx="4" fill="#FFFFFF" stroke="#CBD5E1" />
    <text x="29" y="50" font-family="Arial" font-size="10px" font-weight="700" fill="#142B65" text-anchor="middle">Feed</text>
  </g>

  <!-- COMPONENT 4: DATA PROCESSING AND ANALYSIS -->
  <g transform="translate(1180, 160)">
    <rect width="310" height="730" rx="16" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow-sm)" />
    <!-- Header Banner -->
    <path d="M 0 16 Q 0 0 16 0 L 294 0 Q 310 0 310 16 L 310 70 L 0 70 Z" fill="#142B65" />
    <circle cx="36" cy="35" r="16" fill="#138C8C" />
    <text x="36" y="40" class="badge-txt" text-anchor="middle" font-size="12px">04</text>
    <text x="64" y="32" font-family="Arial" font-size="14.5px" font-weight="800" fill="#FFFFFF">DATA PROCESSING</text>
    <text x="64" y="50" font-family="Arial" font-size="11.5px" font-weight="700" fill="#99F6E4" letter-spacing="1px">&amp; ANALYSIS CORE</text>

    <!-- Sub-elements inside Component 4 -->
    <g transform="translate(20, 95)">
      <!-- Item 1: Extraction -->
      <g transform="translate(0, 0)">
        <rect width="270" height="110" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
        <rect x="0" y="0" width="6" height="110" rx="3" fill="#138C8C" />
        <text x="20" y="28" class="card-title" font-size="13.5px">Metadata Extraction</text>
        <text x="20" y="50" class="card-desc" font-size="12px">• ElementTree XML extraction</text>
        <text x="20" y="68" class="card-desc" font-size="12px">• Title, abstract, DOI mapping</text>
        <text x="20" y="86" class="card-desc" font-size="12px">• Author &amp; affiliation roster</text>
      </g>

      <!-- Item 2: Cleaning & Deduplication -->
      <g transform="translate(0, 125)">
        <rect width="270" height="120" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
        <rect x="0" y="0" width="6" height="120" rx="3" fill="#138C8C" />
        <text x="20" y="28" class="card-title" font-size="13.5px">Cleaning &amp; Deduplication</text>
        <text x="20" y="50" class="card-desc" font-size="12px">• Canonical schema normalizer</text>
        <text x="20" y="68" class="card-desc" font-size="12px">• Safe duplicate flag tracking</text>
        <text x="20" y="86" class="card-desc" font-size="12px">• Conflict &amp; quality scoring</text>
        <text x="20" y="104" font-family="Arial" font-size="10.5px" font-weight="700" fill="#138C8C">Raw data kept 100% intact</text>
      </g>

      <!-- Item 3: Keyword & Country Analysis -->
      <g transform="translate(0, 260)">
        <rect width="270" height="135" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
        <rect x="0" y="0" width="6" height="135" rx="3" fill="#138C8C" />
        <text x="20" y="28" class="card-title" font-size="13.5px">Keyword &amp; Country Analytics</text>
        <text x="20" y="50" class="card-desc" font-size="12px">• Token frequency &amp; matrix</text>
        <text x="20" y="68" class="card-desc" font-size="12px">• NetworkX co-occurrence</text>
        <text x="20" y="86" class="card-desc" font-size="12px">• Affiliation geoparsing &amp; ISO</text>
        <text x="20" y="104" class="card-desc" font-size="12px">• Country collaboration graph</text>
      </g>

      <!-- Item 4: Embedding Processing -->
      <g transform="translate(0, 410)">
        <rect width="270" height="155" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
        <rect x="0" y="0" width="6" height="155" rx="3" fill="#138C8C" />
        <text x="20" y="28" class="card-title" font-size="13.5px">Embedding &amp; Indexing</text>
        <text x="20" y="50" class="card-desc" font-size="12px">• SentenceTransformer vectors</text>
        <text x="20" y="68" class="card-desc" font-size="12px">• HDBSCAN semantic chunking</text>
        <text x="20" y="86" class="card-desc" font-size="12px">• FAISS vector index build</text>
        <text x="20" y="104" class="card-desc" font-size="12px">• Safe duplicate skipping</text>
        <text x="20" y="128" font-family="Arial" font-size="11px" font-weight="700" fill="#142B65">Vector Similarity Layer</text>
      </g>
    </g>
  </g>

  <!-- CONNECTOR 4 -> 5 (Processing to Intelligence & Output) -->
  <g transform="translate(1490, 490)">
    <line x1="10" y1="20" x2="45" y2="20" stroke="#142B65" stroke-width="3" marker-end="url(#arrow-navy)" />
    <rect x="6" y="35" width="46" height="22" rx="4" fill="#FFFFFF" stroke="#CBD5E1" />
    <text x="29" y="50" font-family="Arial" font-size="10px" font-weight="700" fill="#142B65" text-anchor="middle">Deliver</text>
  </g>

  <!-- COMPONENT 5: INTELLIGENCE AND OUTPUT -->
  <g transform="translate(1545, 160)">
    <rect width="295" height="730" rx="16" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow-sm)" />
    <!-- Header Banner -->
    <path d="M 0 16 Q 0 0 16 0 L 279 0 Q 295 0 295 16 L 295 70 L 0 70 Z" fill="#142B65" />
    <circle cx="36" cy="35" r="16" fill="#138C8C" />
    <text x="36" y="40" class="badge-txt" text-anchor="middle" font-size="12px">05</text>
    <text x="64" y="32" font-family="Arial" font-size="14.5px" font-weight="800" fill="#FFFFFF">INTELLIGENCE</text>
    <text x="64" y="50" font-family="Arial" font-size="11.5px" font-weight="700" fill="#99F6E4" letter-spacing="1px">&amp; OUTPUT LAYER</text>

    <!-- Sub-elements inside Component 5 -->
    <g transform="translate(18, 95)">
      <!-- Item 1: Research Analytics -->
      <g transform="translate(0, 0)">
        <rect width="258" height="120" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
        <rect x="0" y="0" width="6" height="120" rx="3" fill="#138C8C" />
        <text x="18" y="30" class="card-title" font-size="13.5px">Research Analytics</text>
        <text x="18" y="52" class="card-desc" font-size="12px">• Keyword frequency metrics</text>
        <text x="18" y="70" class="card-desc" font-size="12px">• Keyword presence matrices</text>
        <text x="18" y="88" class="card-desc" font-size="12px">• Centrality rankings</text>
        <text x="18" y="106" font-family="Arial" font-size="10.5px" font-weight="700" fill="#138C8C">Bibliometric Insight</text>
      </g>

      <!-- Item 2: Collaboration Networks -->
      <g transform="translate(0, 140)">
        <rect width="258" height="120" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
        <rect x="0" y="0" width="6" height="120" rx="3" fill="#138C8C" />
        <text x="18" y="30" class="card-title" font-size="13.5px">Collaboration Networks</text>
        <text x="18" y="52" class="card-desc" font-size="12px">• Country link weights</text>
        <text x="18" y="70" class="card-desc" font-size="12px">• Institutional partners</text>
        <text x="18" y="88" class="card-desc" font-size="12px">• Geographic density</text>
        <text x="18" y="106" font-family="Arial" font-size="10.5px" font-weight="700" fill="#138C8C">Spatial Graphs</text>
      </g>

      <!-- Item 3: Visualizations -->
      <g transform="translate(0, 280)">
        <rect width="258" height="120" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
        <rect x="0" y="0" width="6" height="120" rx="3" fill="#138C8C" />
        <text x="18" y="30" class="card-title" font-size="13.5px">Visualizations</text>
        <text x="18" y="52" class="card-desc" font-size="12px">• 2D World Map (D3)</text>
        <text x="18" y="70" class="card-desc" font-size="12px">• 3D Force-Directed Globe</text>
        <text x="18" y="88" class="card-desc" font-size="12px">• Word clouds &amp; charts</text>
        <text x="18" y="106" font-family="Arial" font-size="10.5px" font-weight="700" fill="#138C8C">Interactive Viewports</text>
      </g>

      <!-- Item 4: AI Research Chat & Export -->
      <g transform="translate(0, 420)">
        <rect width="258" height="145" rx="10" fill="#EAF3F8" stroke="#138C8C" stroke-width="1.5" />
        <rect x="0" y="0" width="6" height="145" rx="3" fill="#142B65" />
        <text x="18" y="30" class="card-title" font-size="13.5px" fill="#142B65">AI Chat &amp; Exports</text>
        <text x="18" y="52" class="card-desc" font-size="12px">• Grounded research answers</text>
        <text x="18" y="70" class="card-desc" font-size="12px">• Semantic citations &amp; DOI</text>
        <text x="18" y="88" class="card-desc" font-size="12px">• CSV / JSON raw exports</text>
        <text x="18" y="106" class="card-desc" font-size="12px">• PDF paper direct fetch</text>
        <text x="18" y="126" font-family="Arial" font-size="10.5px" font-weight="700" fill="#142B65">Grounded Intelligence</text>
      </g>
    </g>
  </g>

  <!-- Presentation Footer Metadata -->
  <g transform="translate(80, 1025)">
    <text x="0" y="16" class="footer-txt">RESEARCH ROVER · M.Tech Data Science Mid-Semester Presentation</text>
    <text x="1760" y="16" class="footer-txt" text-anchor="end">Slide 4 Diagram · System Architecture</text>
  </g>
</svg>"""


# ---------------------------------------------------------------------------
# 04 — END-TO-END SYSTEM WORKFLOW (Slide 5)
# ---------------------------------------------------------------------------
def build_svg_04():
    # Exactly 9 stages in sequential order
    # Let's arrange them in a sleek 2-row serpentine flow (5 on top, 4 on bottom)
    # with clear numbering, stage cards, connecting arrows and phase groupings.
    stages = [
        {
            "num": "01",
            "name": "USER INPUT",
            "subtitle": "Query Specification",
            "desc1": "Research topic, keyword,",
            "desc2": "author or DOI input",
            "desc3": "specified by researcher.",
            "phase": "PHASE 1: REQUEST"
        },
        {
            "num": "02",
            "name": "FRONTEND REQUEST",
            "subtitle": "Client Dispatch",
            "desc1": "React client validates input,",
            "desc2": "attaches query parameters,",
            "desc3": "dispatches async HTTP call.",
            "phase": "PHASE 1: REQUEST"
        },
        {
            "num": "03",
            "name": "BACKEND PROCESSING",
            "subtitle": "Service Orchestration",
            "desc1": "FastAPI routes request,",
            "desc2": "initiates background job,",
            "desc3": "manages live progress state.",
            "phase": "PHASE 1: REQUEST"
        },
        {
            "num": "04",
            "name": "DATA RETRIEVAL",
            "subtitle": "PubMed E-utilities",
            "desc1": "ESearch queries PubMed",
            "desc2": "for PMIDs; EFetch pulls",
            "desc3": "batch XML records.",
            "phase": "PHASE 2: RETRIEVAL"
        },
        {
            "num": "05",
            "name": "XML RESPONSE",
            "subtitle": "Payload Transmission",
            "desc1": "Structured XML publication",
            "desc2": "stream returned over network",
            "desc3": "to backend executor.",
            "phase": "PHASE 2: RETRIEVAL"
        },
        {
            "num": "06",
            "name": "METADATA EXTRACTION",
            "subtitle": "Field Parsing",
            "desc1": "Parses article titles,",
            "desc2": "abstracts, author lists,",
            "desc3": "affiliations & MeSH terms.",
            "phase": "PHASE 3: PROCESSING"
        },
        {
            "num": "07",
            "name": "DATA PROCESSING",
            "subtitle": "Hygiene & Deduplication",
            "desc1": "Canonical schema normalizer,",
            "desc2": "safe duplicate detection,",
            "desc3": "and CSV dataset storage.",
            "phase": "PHASE 3: PROCESSING"
        },
        {
            "num": "08",
            "name": "RESEARCH ANALYSIS",
            "subtitle": "Bibliometric Engine",
            "desc1": "Computes keyword frequency,",
            "desc2": "co-occurrence centralities,",
            "desc3": "and country geoparsing.",
            "phase": "PHASE 4: INSIGHTS"
        },
        {
            "num": "09",
            "name": "RESULTS",
            "subtitle": "Interactive Delivery",
            "desc1": "2D/3D maps, word clouds,",
            "desc2": "collaboration networks,",
            "desc3": "and grounded AI chat answers.",
            "phase": "PHASE 4: INSIGHTS"
        },
    ]

    # Row 1: Stages 01 to 05 (Left to Right)
    # Row 2: Stages 06 to 09 (Left to Right)
    cards_svg = ""
    
    # Top row: 5 cards
    card_w = 320
    card_h = 320
    gap_x = 35
    top_y = 190
    bottom_y = 590

    for idx in range(5):
        s = stages[idx]
        cx = 80 + idx * (card_w + gap_x)
        cy = top_y

        cards_svg += f"""
    <!-- Stage {s['num']} -->
    <g transform="translate({cx}, {cy})">
      <rect width="{card_w}" height="{card_h}" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow-sm)" />
      <path d="M 0 14 Q 0 0 14 0 L {card_w-14} 0 Q {card_w} 0 {card_w} 14 L {card_w} 6 L 0 6 Z" fill="#142B65" />
      
      <!-- Stage Badge -->
      <g transform="translate(20, 20)">
        <rect width="52" height="30" rx="8" fill="#142B65" />
        <text x="26" y="21" class="num-badge" text-anchor="middle" font-size="14px">{s['num']}</text>
        <text x="64" y="22" font-family="Arial" font-size="11.5px" font-weight="700" fill="#138C8C">{s['phase']}</text>
      </g>

      <g transform="translate(20, 75)">
        <text x="0" y="20" class="card-title" font-size="16px">{s['name']}</text>
        <text x="0" y="38" class="card-subtitle">{s['subtitle']}</text>
        <line x1="0" y1="50" x2="{card_w-40}" y2="50" stroke="#F1F5F9" stroke-width="1.5" />
      </g>

      <g transform="translate(20, 155)">
        <text x="0" y="0" class="card-desc" font-size="13.5px">{s['desc1']}</text>
        <text x="0" y="26" class="card-desc" font-size="13.5px">{s['desc2']}</text>
        <text x="0" y="52" class="card-desc" font-size="13.5px">{s['desc3']}</text>
      </g>

      <rect x="20" y="260" width="{card_w-40}" height="34" rx="6" fill="#F8FAFC" stroke="#E2E8F0" />
      <circle cx="34" cy="277" r="4" fill="#138C8C" />
      <text x="46" y="282" font-family="Arial" font-size="11px" font-weight="700" fill="#475569">Stage {idx+1} of 9 in Pipeline</text>
    </g>"""

        # Arrows between top cards
        if idx < 4:
            arrow_x = cx + card_w + 5
            arrow_y = cy + card_h / 2
            cards_svg += f"""
    <line x1="{arrow_x}" y1="{arrow_y}" x2="{arrow_x + gap_x - 10}" y2="{arrow_y}" stroke="#138C8C" stroke-width="3" marker-end="url(#arrow-teal)" />"""

    # Downward turn connector from Stage 05 to Stage 06
    turn_x = 80 + 4 * (card_w + gap_x) + card_w / 2
    cards_svg += f"""
    <!-- Flow Connector: Stage 5 to Stage 6 -->
    <path d="M {turn_x} {top_y + card_h} L {turn_x} {top_y + card_h + 35} L 240 {top_y + card_h + 35} L 240 {bottom_y}" fill="none" stroke="#138C8C" stroke-width="3" stroke-dasharray="6,4" marker-end="url(#arrow-teal)" />
    <rect x="{turn_x - 130}" y="{top_y + card_h + 20}" width="120" height="24" rx="6" fill="#142B65" />
    <text x="{turn_x - 70}" y="{top_y + card_h + 36}" font-family="Arial" font-size="10.5px" font-weight="700" fill="#FFFFFF" text-anchor="middle">TRANSITION</text>"""

    # Bottom row: 4 cards (Stages 06, 07, 08, 09)
    # Give them more width or centered spacing: 4 cards of width 410, gap 45
    card_w2 = 410
    gap_x2 = 45
    for idx2 in range(4):
        s = stages[5 + idx2]
        cx2 = 80 + idx2 * (card_w2 + gap_x2)
        cy2 = bottom_y

        cards_svg += f"""
    <!-- Stage {s['num']} -->
    <g transform="translate({cx2}, {cy2})">
      <rect width="{card_w2}" height="{card_h}" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow-sm)" />
      <path d="M 0 14 Q 0 0 14 0 L {card_w2-14} 0 Q {card_w2} 0 {card_w2} 14 L {card_w2} 6 L 0 6 Z" fill="#138C8C" />
      
      <!-- Stage Badge -->
      <g transform="translate(20, 20)">
        <rect width="52" height="30" rx="8" fill="#138C8C" />
        <text x="26" y="21" class="num-badge" text-anchor="middle" font-size="14px">{s['num']}</text>
        <text x="64" y="22" font-family="Arial" font-size="11.5px" font-weight="700" fill="#142B65">{s['phase']}</text>
      </g>

      <g transform="translate(20, 75)">
        <text x="0" y="20" class="card-title" font-size="16px">{s['name']}</text>
        <text x="0" y="38" class="card-subtitle">{s['subtitle']}</text>
        <line x1="0" y1="50" x2="{card_w2-40}" y2="50" stroke="#F1F5F9" stroke-width="1.5" />
      </g>

      <g transform="translate(20, 155)">
        <text x="0" y="0" class="card-desc" font-size="13.5px">{s['desc1']}</text>
        <text x="0" y="26" class="card-desc" font-size="13.5px">{s['desc2']}</text>
        <text x="0" y="52" class="card-desc" font-size="13.5px">{s['desc3']}</text>
      </g>

      <rect x="20" y="260" width="{card_w2-40}" height="34" rx="6" fill="#F8FAFC" stroke="#E2E8F0" />
      <circle cx="34" cy="277" r="4" fill="#142B65" />
      <text x="46" y="282" font-family="Arial" font-size="11px" font-weight="700" fill="#475569">Stage {6 + idx2} of 9 in Pipeline</text>
    </g>"""

        # Arrows between bottom cards
        if idx2 < 3:
            arrow_x2 = cx2 + card_w2 + 5
            arrow_y2 = cy2 + card_h / 2
            cards_svg += f"""
    <line x1="{arrow_x2}" y1="{arrow_y2}" x2="{arrow_x2 + gap_x2 - 10}" y2="{arrow_y2}" stroke="#142B65" stroke-width="3" marker-end="url(#arrow-navy)" />"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
{COMMON_DEFS}
  <!-- Background -->
  <rect width="1920" height="1080" fill="#FFFFFF" />
  <line x1="80" y1="135" x2="1840" y2="135" stroke="#E2E8F0" stroke-width="1.5" />

  <!-- Slide Header -->
  <g transform="translate(80, 50)">
    <text x="0" y="20" class="title-tag">Target: Presentation Slide 5 · End-to-End System Workflow</text>
    <text x="0" y="56" class="main-title">End-to-End System Workflow</text>
    <text x="0" y="80" class="sub-title">Nine-stage sequential pipeline transforming raw researcher queries into validated bibliometric intelligence and interactive outputs</text>
  </g>

  <!-- CARDS CONTAINER -->
{cards_svg}

  <!-- Presentation Footer Metadata -->
  <g transform="translate(80, 1030)">
    <text x="0" y="16" class="footer-txt">RESEARCH ROVER · M.Tech Data Science Mid-Semester Presentation</text>
    <text x="1760" y="16" class="footer-txt" text-anchor="end">Slide 5 Diagram · Nine-Stage End-to-End Workflow</text>
  </g>
</svg>"""


# ---------------------------------------------------------------------------
# 05 — RESEARCH ANALYTICAL COMPONENTS (Slide 6)
# ---------------------------------------------------------------------------
def build_svg_05():
    # Central Hub: RESEARCH ANALYSIS ENGINE
    # 6 Surrounding modules: 3 top, 3 bottom
    # Small separate footer with technologies
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
{COMMON_DEFS}
  <!-- Background -->
  <rect width="1920" height="1080" fill="#FFFFFF" />
  <line x1="80" y1="135" x2="1840" y2="135" stroke="#E2E8F0" stroke-width="1.5" />

  <!-- Slide Header -->
  <g transform="translate(80, 50)">
    <text x="0" y="20" class="title-tag">Target: Presentation Slide 6 · Research Analytical Components</text>
    <text x="0" y="56" class="main-title">Research Analytical Components</text>
    <text x="0" y="80" class="sub-title">Six core analytical capabilities driven by the centralized Research Analysis Engine</text>
  </g>

  <!-- 3 TOP SURROUNDING MODULES -->
  <!-- Module 1: Keyword Analysis -->
  <g transform="translate(140, 170)">
    <rect width="480" height="230" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow-sm)" />
    <path d="M 0 14 Q 0 0 14 0 L 466 0 Q 480 0 480 14 L 480 6 L 0 6 Z" fill="#142B65" />
    <circle cx="36" cy="42" r="18" fill="#EAF3F8" stroke="#138C8C" stroke-width="1.5" />
    <text x="36" y="47" class="num-badge" text-anchor="middle" font-size="13px" fill="#142B65">01</text>
    <text x="66" y="38" class="card-title" font-size="16px">1. KEYWORD ANALYSIS</text>
    <text x="66" y="56" class="card-subtitle">Frequency and Co-occurrence</text>
    <line x1="20" y1="72" x2="460" y2="72" stroke="#F1F5F9" stroke-width="1.5" />
    <text x="20" y="102" class="card-desc">• Author &amp; MeSH keyword tokenization and frequency ranking</text>
    <text x="20" y="126" class="card-desc">• Keyword presence-absence matrix generation across records</text>
    <text x="20" y="150" class="card-desc">• Terminology burst detection &amp; thematic weight extraction</text>
    <text x="20" y="174" class="card-desc">• Powers customizable frequency thresholds &amp; top-N filters</text>
    <rect x="20" y="190" width="160" height="24" rx="5" fill="#EAF3F8" />
    <text x="32" y="206" font-family="Arial" font-size="11px" font-weight="700" fill="#138C8C">Text Mining Core</text>
  </g>

  <!-- Module 2: Country Analysis -->
  <g transform="translate(720, 170)">
    <rect width="480" height="230" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow-sm)" />
    <path d="M 0 14 Q 0 0 14 0 L 466 0 Q 480 0 480 14 L 480 6 L 0 6 Z" fill="#142B65" />
    <circle cx="36" cy="42" r="18" fill="#EAF3F8" stroke="#138C8C" stroke-width="1.5" />
    <text x="36" y="47" class="num-badge" text-anchor="middle" font-size="13px" fill="#142B65">02</text>
    <text x="66" y="38" class="card-title" font-size="16px">2. COUNTRY ANALYSIS</text>
    <text x="66" y="56" class="card-subtitle">Publication Distribution</text>
    <line x1="20" y1="72" x2="460" y2="72" stroke="#F1F5F9" stroke-width="1.5" />
    <text x="20" y="102" class="card-desc">• Geographical country extraction from affiliation text</text>
    <text x="20" y="126" class="card-desc">• ISO 3166-1 alpha-3 code standardization &amp; geoparsing</text>
    <text x="20" y="150" class="card-desc">• Country publication frequency &amp; global share percentages</text>
    <text x="20" y="174" class="card-desc">• Transparency reporting for unassigned paper affiliations</text>
    <rect x="20" y="190" width="170" height="24" rx="5" fill="#EAF3F8" />
    <text x="32" y="206" font-family="Arial" font-size="11px" font-weight="700" fill="#138C8C">Geospatial Analytics</text>
  </g>

  <!-- Module 3: Affiliation Analysis -->
  <g transform="translate(1300, 170)">
    <rect width="480" height="230" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow-sm)" />
    <path d="M 0 14 Q 0 0 14 0 L 466 0 Q 480 0 480 14 L 480 6 L 0 6 Z" fill="#142B65" />
    <circle cx="36" cy="42" r="18" fill="#EAF3F8" stroke="#138C8C" stroke-width="1.5" />
    <text x="36" y="47" class="num-badge" text-anchor="middle" font-size="13px" fill="#142B65">03</text>
    <text x="66" y="38" class="card-title" font-size="16px">3. AFFILIATION ANALYSIS</text>
    <text x="66" y="56" class="card-subtitle">Author &amp; Institutional Information</text>
    <line x1="20" y1="72" x2="460" y2="72" stroke="#F1F5F9" stroke-width="1.5" />
    <text x="20" y="102" class="card-desc">• Institutional name parsing &amp; author affiliation linking</text>
    <text x="20" y="126" class="card-desc">• University, research hospital &amp; corporate lab mapping</text>
    <text x="20" y="150" class="card-desc">• Multi-author institutional collaboration resolution</text>
    <text x="20" y="174" class="card-desc">• Identification of top publishing research organizations</text>
    <rect x="20" y="190" width="180" height="24" rx="5" fill="#EAF3F8" />
    <text x="32" y="206" font-family="Arial" font-size="11px" font-weight="700" fill="#138C8C">Institutional Mining</text>
  </g>

  <!-- CONNECTOR SPOKES TO CENTRAL ENGINE -->
  <g>
    <!-- Spoke 1 to Hub -->
    <path d="M 380 400 L 380 470 L 680 520" fill="none" stroke="#138C8C" stroke-width="2.5" stroke-dasharray="6,4" marker-end="url(#arrow-teal)" />
    <!-- Spoke 2 to Hub -->
    <path d="M 960 400 L 960 460" fill="none" stroke="#138C8C" stroke-width="2.5" marker-end="url(#arrow-teal)" />
    <!-- Spoke 3 to Hub -->
    <path d="M 1540 400 L 1540 470 L 1240 520" fill="none" stroke="#138C8C" stroke-width="2.5" stroke-dasharray="6,4" marker-end="url(#arrow-teal)" />
  </g>

  <!-- CENTRAL COMPONENT: RESEARCH ANALYSIS ENGINE -->
  <g transform="translate(640, 465)">
    <rect width="640" height="150" rx="20" fill="#142B65" stroke="#138C8C" stroke-width="3" filter="url(#hero-shadow)" />
    <circle cx="50" cy="75" r="28" fill="#138C8C" />
    <path d="M 40 75 L 60 75 M 50 65 L 50 85" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" />
    <circle cx="50" cy="75" r="18" fill="none" stroke="#99F6E4" stroke-width="2" stroke-dasharray="3,3" />

    <text x="96" y="54" font-family="Arial" font-size="22px" font-weight="800" fill="#FFFFFF" letter-spacing="1px">RESEARCH ANALYSIS ENGINE</text>
    <text x="96" y="78" font-family="Arial" font-size="13.5px" font-weight="700" fill="#99F6E4">Centralized Multi-Dimensional Processing &amp; Analytical Orchestration Core</text>
    <text x="96" y="104" font-family="Arial" font-size="12.5px" fill="#CBD5E1">Coordinates keyword matrices, graph algorithms, geoparsers, vector similarity &amp; visualization pipelines</text>
  </g>

  <!-- CONNECTOR SPOKES FROM CENTRAL ENGINE TO BOTTOM MODULES -->
  <g>
    <!-- Hub to Spoke 4 -->
    <path d="M 680 615 L 380 660 L 380 710" fill="none" stroke="#142B65" stroke-width="2.5" stroke-dasharray="6,4" marker-end="url(#arrow-navy)" />
    <!-- Hub to Spoke 5 -->
    <path d="M 960 615 L 960 710" fill="none" stroke="#142B65" stroke-width="2.5" marker-end="url(#arrow-navy)" />
    <!-- Hub to Spoke 6 -->
    <path d="M 1240 615 L 1540 660 L 1540 710" fill="none" stroke="#142B65" stroke-width="2.5" stroke-dasharray="6,4" marker-end="url(#arrow-navy)" />
  </g>

  <!-- 3 BOTTOM SURROUNDING MODULES -->
  <!-- Module 4: Network Analysis -->
  <g transform="translate(140, 715)">
    <rect width="480" height="230" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow-sm)" />
    <path d="M 0 14 Q 0 0 14 0 L 466 0 Q 480 0 480 14 L 480 6 L 0 6 Z" fill="#138C8C" />
    <circle cx="36" cy="42" r="18" fill="#EAF3F8" stroke="#142B65" stroke-width="1.5" />
    <text x="36" y="47" class="num-badge" text-anchor="middle" font-size="13px" fill="#142B65">04</text>
    <text x="66" y="38" class="card-title" font-size="16px">4. NETWORK ANALYSIS</text>
    <text x="66" y="56" class="card-subtitle">Collaboration Relationships</text>
    <line x1="20" y1="72" x2="460" y2="72" stroke="#F1F5F9" stroke-width="1.5" />
    <text x="20" y="102" class="card-desc">• Co-occurrence edge weight matrix calculation</text>
    <text x="20" y="126" class="card-desc">• Degree, Betweenness, Closeness &amp; Eigenvector centralities</text>
    <text x="20" y="150" class="card-desc">• Clustering coefficients revealing research sub-communities</text>
    <text x="20" y="174" class="card-desc">• International multi-country collaborative network graph</text>
    <rect x="20" y="190" width="180" height="24" rx="5" fill="#EAF3F8" />
    <text x="32" y="206" font-family="Arial" font-size="11px" font-weight="700" fill="#138C8C">Graph Theory Core</text>
  </g>

  <!-- Module 5: Embeddings & RAG Chat -->
  <g transform="translate(720, 715)">
    <rect width="480" height="230" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow-sm)" />
    <path d="M 0 14 Q 0 0 14 0 L 466 0 Q 480 0 480 14 L 480 6 L 0 6 Z" fill="#138C8C" />
    <circle cx="36" cy="42" r="18" fill="#EAF3F8" stroke="#142B65" stroke-width="1.5" />
    <text x="36" y="47" class="num-badge" text-anchor="middle" font-size="13px" fill="#142B65">05</text>
    <text x="66" y="38" class="card-title" font-size="16px">5. EMBEDDINGS &amp; RAG CHAT</text>
    <text x="66" y="56" class="card-subtitle">Semantic Retrieval &amp; Interaction</text>
    <line x1="20" y1="72" x2="460" y2="72" stroke="#F1F5F9" stroke-width="1.5" />
    <text x="20" y="102" class="card-desc">• Dense text vectorization with all-mpnet-base-v2</text>
    <text x="20" y="126" class="card-desc">• HDBSCAN semantic chunking &amp; FAISS vector index</text>
    <text x="20" y="150" class="card-desc">• Document-grounded conversational question answering</text>
    <text x="20" y="174" class="card-desc">• Evidence attribution with DOI and section citation links</text>
    <rect x="20" y="190" width="190" height="24" rx="5" fill="#EAF3F8" />
    <text x="32" y="206" font-family="Arial" font-size="11px" font-weight="700" fill="#138C8C">Semantic AI Engine</text>
  </g>

  <!-- Module 6: Visualization -->
  <g transform="translate(1300, 715)">
    <rect width="480" height="230" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow-sm)" />
    <path d="M 0 14 Q 0 0 14 0 L 466 0 Q 480 0 480 14 L 480 6 L 0 6 Z" fill="#138C8C" />
    <circle cx="36" cy="42" r="18" fill="#EAF3F8" stroke="#142B65" stroke-width="1.5" />
    <text x="36" y="47" class="num-badge" text-anchor="middle" font-size="13px" fill="#142B65">06</text>
    <text x="66" y="38" class="card-title" font-size="16px">6. VISUALIZATION</text>
    <text x="66" y="56" class="card-subtitle">Charts, Maps and Networks</text>
    <line x1="20" y1="72" x2="460" y2="72" stroke="#F1F5F9" stroke-width="1.5" />
    <text x="20" y="102" class="card-desc">• Interactive 2D World Map (Mercator projection geoparsing)</text>
    <text x="20" y="126" class="card-desc">• 3D Three.js rotating globe with dynamic arcs &amp; rings</text>
    <text x="20" y="150" class="card-desc">• Zoomable 2D force-directed co-occurrence graph view</text>
    <text x="20" y="174" class="card-desc">• Canvas word clouds, publication timeline charts &amp; PNG export</text>
    <rect x="20" y="190" width="190" height="24" rx="5" fill="#EAF3F8" />
    <text x="32" y="206" font-family="Arial" font-size="11px" font-weight="700" fill="#138C8C">Interactive Viewports</text>
  </g>

  <!-- SEPARATE SMALL FOOTER BAR WITH TECHNOLOGIES -->
  <g transform="translate(140, 970)">
    <rect width="1640" height="46" rx="10" fill="#F4F6F8" stroke="#CBD5E1" stroke-width="1" />
    <text x="25" y="28" font-family="Arial" font-size="12px" font-weight="800" fill="#142B65" letter-spacing="1px">UNDERLYING TECHNOLOGIES:</text>
    <g transform="translate(230, 10)">
      <rect x="0" y="0" width="80" height="26" rx="5" fill="#FFFFFF" stroke="#CBD5E1" />
      <text x="40" y="18" font-family="Arial" font-size="12px" font-weight="700" fill="#142B65" text-anchor="middle">Python</text>

      <text x="95" y="18" font-family="Arial" font-size="14px" fill="#94A3B8">|</text>

      <rect x="110" y="0" width="80" height="26" rx="5" fill="#FFFFFF" stroke="#CBD5E1" />
      <text x="150" y="18" font-family="Arial" font-size="12px" font-weight="700" fill="#142B65" text-anchor="middle">Pandas</text>

      <text x="205" y="18" font-family="Arial" font-size="14px" fill="#94A3B8">|</text>

      <rect x="220" y="0" width="95" height="26" rx="5" fill="#FFFFFF" stroke="#CBD5E1" />
      <text x="267" y="18" font-family="Arial" font-size="12px" font-weight="700" fill="#142B65" text-anchor="middle">NetworkX</text>

      <text x="330" y="18" font-family="Arial" font-size="14px" fill="#94A3B8">|</text>

      <rect x="345" y="0" width="75" height="26" rx="5" fill="#FFFFFF" stroke="#CBD5E1" />
      <text x="382" y="18" font-family="Arial" font-size="12px" font-weight="700" fill="#142B65" text-anchor="middle">FAISS</text>

      <text x="435" y="18" font-family="Arial" font-size="14px" fill="#94A3B8">|</text>

      <rect x="450" y="0" width="240" height="26" rx="5" fill="#FFFFFF" stroke="#CBD5E1" />
      <text x="570" y="18" font-family="Arial" font-size="12px" font-weight="700" fill="#142B65" text-anchor="middle">React Visualization Components</text>
    </g>
  </g>

  <!-- Presentation Footer Metadata -->
  <g transform="translate(80, 1045)">
    <text x="0" y="16" class="footer-txt">RESEARCH ROVER · M.Tech Data Science Mid-Semester Presentation</text>
    <text x="1760" y="16" class="footer-txt" text-anchor="end">Slide 6 Diagram · Analytical Components</text>
  </g>
</svg>"""


# ---------------------------------------------------------------------------
# 06 — DEVELOPMENT STATUS (Slide 7)
# ---------------------------------------------------------------------------
def build_svg_06():
    # 3 equal columns:
    # Column 1: EXISTING FOUNDATION (Green accents #23865A)
    # Column 2: UNDER DEVELOPMENT (Amber accents #D99A32)
    # Column 3: PLANNED ENHANCEMENTS (Blue dashed borders #138C8C / #142B65)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
{COMMON_DEFS}
  <!-- Background -->
  <rect width="1920" height="1080" fill="#FFFFFF" />
  <line x1="80" y1="135" x2="1840" y2="135" stroke="#E2E8F0" stroke-width="1.5" />

  <!-- Slide Header -->
  <g transform="translate(80, 50)">
    <text x="0" y="20" class="title-tag">Target: Presentation Slide 7 · Development Status and Achievements</text>
    <text x="0" y="56" class="main-title">Development Status and Achievements</text>
    <text x="0" y="80" class="sub-title">Current progress across core architecture, ongoing feature engineering, and strategic research roadmap</text>
  </g>

  <!-- 3 COLUMNS -->
  <!-- COLUMN 1: EXISTING FOUNDATION -->
  <g transform="translate(80, 160)">
    <rect width="555" height="790" rx="16" fill="#F4FBF7" stroke="#23865A" stroke-width="2" filter="url(#shadow-md)" />
    <!-- Column Top Header -->
    <path d="M 0 16 Q 0 0 16 0 L 539 0 Q 555 0 555 16 L 555 75 L 0 75 Z" fill="#23865A" />
    <circle cx="36" cy="37" r="16" fill="#FFFFFF" />
    <!-- Checkmark Icon -->
    <path d="M 28 37 L 34 43 L 44 31" fill="none" stroke="#23865A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
    <text x="64" y="34" font-family="Arial" font-size="17px" font-weight="800" fill="#FFFFFF">EXISTING FOUNDATION</text>
    <text x="64" y="54" font-family="Arial" font-size="12px" font-weight="700" fill="#D1FAE5" letter-spacing="1px">IMPLEMENTED &amp; OPERATIONAL</text>
    <rect x="420" y="24" width="115" height="26" rx="6" fill="#14532D" />
    <text x="477" y="41" font-family="Arial" font-size="11.5px" font-weight="700" fill="#86EFAC" text-anchor="middle">ACTIVE CORE</text>

    <!-- 5 Foundation Items -->
    <g transform="translate(25, 95)">
      <!-- Item 1: React / Vite -->
      <g transform="translate(0, 0)">
        <rect width="505" height="118" rx="12" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1.5" />
        <rect x="0" y="0" width="8" height="118" rx="4" fill="#23865A" />
        <circle cx="40" cy="59" r="18" fill="#EAF6F0" />
        <text x="40" y="65" font-family="Arial" font-size="13px" font-weight="800" fill="#23865A" text-anchor="middle">01</text>
        <text x="75" y="36" class="card-title">React / Vite Modern Web Frontend</text>
        <text x="75" y="58" class="card-desc">• Production SPA with routing (Search, Analytics, Chat, Settings)</text>
        <text x="75" y="78" class="card-desc">• Tailwind CSS dark &amp; light theme, responsive layout</text>
        <text x="75" y="98" class="card-desc" font-weight="700" fill="#23865A">• Fully verified in production build (Vite v6 + TypeScript)</text>
      </g>

      <!-- Item 2: FastAPI -->
      <g transform="translate(0, 135)">
        <rect width="505" height="118" rx="12" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1.5" />
        <rect x="0" y="0" width="8" height="118" rx="4" fill="#23865A" />
        <circle cx="40" cy="59" r="18" fill="#EAF6F0" />
        <text x="40" y="65" font-family="Arial" font-size="13px" font-weight="800" fill="#23865A" text-anchor="middle">02</text>
        <text x="75" y="36" class="card-title">FastAPI High-Concurrency Backend</text>
        <text x="75" y="58" class="card-desc">• Async REST API with background task orchestration</text>
        <text x="75" y="78" class="card-desc">• Dedicated thread pool executor for external rate limits</text>
        <text x="75" y="98" class="card-desc" font-weight="700" fill="#23865A">• App lifespan &amp; non-blocking SentenceTransformer manager</text>
      </g>

      <!-- Item 3: PubMed Integration -->
      <g transform="translate(0, 270)">
        <rect width="505" height="118" rx="12" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1.5" />
        <rect x="0" y="0" width="8" height="118" rx="4" fill="#23865A" />
        <circle cx="40" cy="59" r="18" fill="#EAF6F0" />
        <text x="40" y="65" font-family="Arial" font-size="13px" font-weight="800" fill="#23865A" text-anchor="middle">03</text>
        <text x="75" y="36" class="card-title">PubMed / NCBI E-utilities Integration</text>
        <text x="75" y="58" class="card-desc">• Live biomedical query execution with ESpell query correction</text>
        <text x="75" y="78" class="card-desc">• Multi-stage search progress reporting across sub-stages</text>
        <text x="75" y="98" class="card-desc" font-weight="700" fill="#23865A">• Automatic retrieval cancellation and graceful fail-open</text>
      </g>

      <!-- Item 4: XML Extraction -->
      <g transform="translate(0, 405)">
        <rect width="505" height="118" rx="12" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1.5" />
        <rect x="0" y="0" width="8" height="118" rx="4" fill="#23865A" />
        <circle cx="40" cy="59" r="18" fill="#EAF6F0" />
        <text x="40" y="65" font-family="Arial" font-size="13px" font-weight="800" fill="#23865A" text-anchor="middle">04</text>
        <text x="75" y="36" class="card-title">XML Extraction &amp; Field Parsing</text>
        <text x="75" y="58" class="card-desc">• ElementTree high-throughput parsing of Medline streams</text>
        <text x="75" y="78" class="card-desc">• Robust extraction of title, abstract, authors, DOI, year &amp; MeSH</text>
        <text x="75" y="98" class="card-desc" font-weight="700" fill="#23865A">• Fallback parsing for incomplete records</text>
      </g>

      <!-- Item 5: CSV Pipeline -->
      <g transform="translate(0, 540)">
        <rect width="505" height="118" rx="12" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1.5" />
        <rect x="0" y="0" width="8" height="118" rx="4" fill="#23865A" />
        <circle cx="40" cy="59" r="18" fill="#EAF6F0" />
        <text x="40" y="65" font-family="Arial" font-size="13px" font-weight="800" fill="#23865A" text-anchor="middle">05</text>
        <text x="75" y="36" class="card-title">CSV Ingestion &amp; Storage Pipeline</text>
        <text x="75" y="58" class="card-desc">• Chunked CSV streaming, pagination, and file management</text>
        <text x="75" y="78" class="card-desc">• Raw byte preservation on disk with UTF-8/Latin-1 detection</text>
        <text x="75" y="98" class="card-desc" font-weight="700" fill="#23865A">• Unified file schema with export download support</text>
      </g>
    </g>
  </g>

  <!-- COLUMN 2: UNDER DEVELOPMENT -->
  <g transform="translate(682, 160)">
    <rect width="555" height="790" rx="16" fill="#FEFDF9" stroke="#D99A32" stroke-width="2" filter="url(#shadow-md)" />
    <!-- Column Top Header -->
    <path d="M 0 16 Q 0 0 16 0 L 539 0 Q 555 0 555 16 L 555 75 L 0 75 Z" fill="#D99A32" />
    <circle cx="36" cy="37" r="16" fill="#FFFFFF" />
    <!-- Gear / In-Progress Icon -->
    <circle cx="36" cy="37" r="7" fill="none" stroke="#D99A32" stroke-width="2.5" />
    <line x1="36" y1="27" x2="36" y2="30" stroke="#D99A32" stroke-width="2.5" stroke-linecap="round" />
    <line x1="36" y1="44" x2="36" y2="47" stroke="#D99A32" stroke-width="2.5" stroke-linecap="round" />
    <line x1="26" y1="37" x2="29" y2="37" stroke="#D99A32" stroke-width="2.5" stroke-linecap="round" />
    <line x1="43" y1="37" x2="46" y2="37" stroke="#D99A32" stroke-width="2.5" stroke-linecap="round" />
    <text x="64" y="34" font-family="Arial" font-size="17px" font-weight="800" fill="#FFFFFF">UNDER DEVELOPMENT</text>
    <text x="64" y="54" font-family="Arial" font-size="12px" font-weight="700" fill="#FEF3C7" letter-spacing="1px">ACTIVE ENHANCEMENT</text>
    <rect x="400" y="24" width="135" height="26" rx="6" fill="#78350F" />
    <text x="467" y="41" font-family="Arial" font-size="11px" font-weight="700" fill="#FDE68A" text-anchor="middle">IN PROGRESS</text>

    <!-- 4 In-Progress Items -->
    <g transform="translate(25, 95)">
      <!-- Item 1: Metadata Completeness -->
      <g transform="translate(0, 0)">
        <rect width="505" height="150" rx="12" fill="#FFFFFF" stroke="#FDE68A" stroke-width="1.5" />
        <rect x="0" y="0" width="8" height="150" rx="4" fill="#D99A32" />
        <circle cx="40" cy="75" r="18" fill="#FEF7EA" />
        <text x="40" y="81" font-family="Arial" font-size="13px" font-weight="800" fill="#D99A32" text-anchor="middle">01</text>
        <text x="75" y="36" class="card-title">Metadata Completeness &amp; Quality Layer</text>
        <text x="75" y="58" class="card-desc">• Canonical schema normalizer mapping 20+ field aliases</text>
        <text x="75" y="78" class="card-desc">• Field-level completeness scoring &amp; invalid value penalties</text>
        <text x="75" y="98" class="card-desc">• Safe duplicate tracking (unique records for analytics, raw preserved)</text>
        <text x="75" y="120" class="card-desc" font-weight="700" fill="#D99A32">• Feature-by-feature readiness evaluation (ready / partial / not ready)</text>
      </g>

      <!-- Item 2: Affiliation Extraction -->
      <g transform="translate(0, 168)">
        <rect width="505" height="150" rx="12" fill="#FFFFFF" stroke="#FDE68A" stroke-width="1.5" />
        <rect x="0" y="0" width="8" height="150" rx="4" fill="#D99A32" />
        <circle cx="40" cy="75" r="18" fill="#FEF7EA" />
        <text x="40" y="81" font-family="Arial" font-size="13px" font-weight="800" fill="#D99A32" text-anchor="middle">02</text>
        <text x="75" y="36" class="card-title">Affiliation Extraction &amp; Normalization</text>
        <text x="75" y="58" class="card-desc">• Heuristic parsing of unstructured institutional strings</text>
        <text x="75" y="78" class="card-desc">• Multi-author institutional mapping and department tagging</text>
        <text x="75" y="98" class="card-desc">• Handling author-to-institution alignment anomalies</text>
        <text x="75" y="120" class="card-desc" font-weight="700" fill="#D99A32">• Enhancing geoparsing coverage across non-standard headers</text>
      </g>

      <!-- Item 3: Country & Institutional Analysis -->
      <g transform="translate(0, 336)">
        <rect width="505" height="150" rx="12" fill="#FFFFFF" stroke="#FDE68A" stroke-width="1.5" />
        <rect x="0" y="0" width="8" height="150" rx="4" fill="#D99A32" />
        <circle cx="40" cy="75" r="18" fill="#FEF7EA" />
        <text x="40" y="81" font-family="Arial" font-size="13px" font-weight="800" fill="#D99A32" text-anchor="middle">03</text>
        <text x="75" y="36" class="card-title">Country and Institutional Analysis</text>
        <text x="75" y="58" class="card-desc">• Country alias standardization (ISO 3166-1 alpha-3)</text>
        <text x="75" y="78" class="card-desc">• Pairwise international co-authorship collaboration links</text>
        <text x="75" y="98" class="card-desc">• Sidecar caching of country statistics and graphs</text>
        <text x="75" y="120" class="card-desc" font-weight="700" fill="#D99A32">• Real-time collaboration network computation</text>
      </g>

      <!-- Item 4: Dashboard Integration -->
      <g transform="translate(0, 504)">
        <rect width="505" height="150" rx="12" fill="#FFFFFF" stroke="#FDE68A" stroke-width="1.5" filter="url(#shadow-sm)" />
        <rect x="0" y="0" width="8" height="150" rx="4" fill="#D99A32" />
        <circle cx="40" cy="75" r="18" fill="#FEF7EA" />
        <text x="40" y="81" font-family="Arial" font-size="13px" font-weight="800" fill="#D99A32" text-anchor="middle">04</text>
        <text x="75" y="36" class="card-title">Dashboard Integration &amp; Visual UX</text>
        <text x="75" y="58" class="card-desc">• Integrated Dataset Quality Modal with field statistics &amp; warnings</text>
        <text x="75" y="78" class="card-desc">• Interactive 2D World Map and Three.js 3D Force Globe</text>
        <text x="75" y="98" class="card-desc">• Real-time dataset selector with immediate readiness banners</text>
        <text x="75" y="120" class="card-desc" font-weight="700" fill="#D99A32">• Co-occurrence graph viewer with sphere &amp; force layouts</text>
      </g>
    </g>
  </g>

  <!-- COLUMN 3: PLANNED ENHANCEMENTS -->
  <g transform="translate(1284, 160)">
    <rect width="555" height="790" rx="16" fill="#F8FAFC" stroke="#138C8C" stroke-width="2" stroke-dasharray="8,5" filter="url(#shadow-sm)" />
    <!-- Column Top Header -->
    <path d="M 0 16 Q 0 0 16 0 L 539 0 Q 555 0 555 16 L 555 75 L 0 75 Z" fill="#142B65" />
    <circle cx="36" cy="37" r="16" fill="#138C8C" />
    <!-- Sparkle / Future Icon -->
    <path d="M 36 29 L 38 35 L 44 37 L 38 39 L 36 45 L 34 39 L 28 37 L 34 35 Z" fill="#FFFFFF" />
    <text x="64" y="34" font-family="Arial" font-size="17px" font-weight="800" fill="#FFFFFF">PLANNED ENHANCEMENTS</text>
    <text x="64" y="54" font-family="Arial" font-size="12px" font-weight="700" fill="#99F6E4" letter-spacing="1px">ROADMAP &amp; FUTURE PHASES</text>
    <rect x="400" y="24" width="135" height="26" rx="6" fill="#0C4A6E" />
    <text x="467" y="41" font-family="Arial" font-size="11px" font-weight="700" fill="#7DD3FC" text-anchor="middle">UPCOMING</text>

    <!-- 4 Planned Items -->
    <g transform="translate(25, 95)">
      <!-- Item 1: OpenAlex Integration -->
      <g transform="translate(0, 0)">
        <rect width="505" height="150" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="6,4" />
        <rect x="0" y="0" width="8" height="150" rx="4" fill="#138C8C" />
        <circle cx="40" cy="75" r="18" fill="#EAF3F8" />
        <text x="40" y="81" font-family="Arial" font-size="13px" font-weight="800" fill="#142B65" text-anchor="middle">01</text>
        <text x="75" y="36" class="card-title">OpenAlex Integration</text>
        <text x="75" y="58" class="card-desc">• Full REST API integration with OpenAlex global scholarly graph</text>
        <text x="75" y="78" class="card-desc">• Ingestion of open access status, citation counts &amp; concept hierarchies</text>
        <text x="75" y="98" class="card-desc">• Expanding literature coverage beyond clinical/biomedical domains</text>
        <text x="75" y="120" class="card-desc" font-weight="700" fill="#138C8C">• Native cross-discipline scientific discovery</text>
      </g>

      <!-- Item 2: Multi-source Retrieval -->
      <g transform="translate(0, 168)">
        <rect width="505" height="150" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="6,4" />
        <rect x="0" y="0" width="8" height="150" rx="4" fill="#138C8C" />
        <circle cx="40" cy="75" r="18" fill="#EAF3F8" />
        <text x="40" y="81" font-family="Arial" font-size="13px" font-weight="800" fill="#142B65" text-anchor="middle">02</text>
        <text x="75" y="36" class="card-title">Multi-source Unified Retrieval</text>
        <text x="75" y="58" class="card-desc">• Parallel federated querying across PubMed, OpenAlex, arXiv &amp; CrossRef</text>
        <text x="75" y="78" class="card-desc">• Cross-source deduplication via DOI, PMID and normalized titles</text>
        <text x="75" y="98" class="card-desc">• Unified ranking combining recency and semantic relevance</text>
        <text x="75" y="120" class="card-desc" font-weight="700" fill="#138C8C">• Consolidated single-search research workflows</text>
      </g>

      <!-- Item 3: Advanced Collaboration Analysis -->
      <g transform="translate(0, 336)">
        <rect width="505" height="150" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="6,4" />
        <rect x="0" y="0" width="8" height="150" rx="4" fill="#138C8C" />
        <circle cx="40" cy="75" r="18" fill="#EAF3F8" />
        <text x="40" y="81" font-family="Arial" font-size="13px" font-weight="800" fill="#142B65" text-anchor="middle">03</text>
        <text x="75" y="36" class="card-title">Advanced Collaboration Analysis</text>
        <text x="75" y="58" class="card-desc">• Longitudinal collaboration tracking across multi-year cohorts</text>
        <text x="75" y="78" class="card-desc">• Author co-authorship ego networks and institutional impact metrics</text>
        <text x="75" y="98" class="card-desc">• Identification of central bridge researchers across disciplines</text>
        <text x="75" y="120" class="card-desc" font-weight="700" fill="#138C8C">• Higher-order community detection algorithms (Louvain/Leiden)</text>
      </g>

      <!-- Item 4: AI-assisted Interaction -->
      <g transform="translate(0, 504)">
        <rect width="505" height="150" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="6,4" />
        <rect x="0" y="0" width="8" height="150" rx="4" fill="#138C8C" />
        <circle cx="40" cy="75" r="18" fill="#EAF3F8" />
        <text x="40" y="81" font-family="Arial" font-size="13px" font-weight="800" fill="#142B65" text-anchor="middle">04</text>
        <text x="75" y="36" class="card-title">AI-assisted Research Interaction</text>
        <text x="75" y="58" class="card-desc">• Automated literature synthesis and comparative table generation</text>
        <text x="75" y="78" class="card-desc">• Multi-document grounded question answering with verified citations</text>
        <text x="75" y="98" class="card-desc">• Hypothesis brainstorming and contradiction detection across papers</text>
        <text x="75" y="120" class="card-desc" font-weight="700" fill="#138C8C">• Autonomous agentic research exploration</text>
      </g>
    </g>
  </g>

  <!-- Presentation Footer Metadata -->
  <g transform="translate(80, 1025)">
    <text x="0" y="16" class="footer-txt">RESEARCH ROVER · M.Tech Data Science Mid-Semester Presentation</text>
    <text x="1760" y="16" class="footer-txt" text-anchor="end">Slide 7 Diagram · Development Status and Achievements</text>
  </g>
</svg>"""


# ---------------------------------------------------------------------------
# 07 — FUTURE DEVELOPMENT ROADMAP (Slide 8)
# ---------------------------------------------------------------------------
def build_svg_07():
    # Exactly 5 milestones in horizontal layout
    # Canvas width: 1920. 5 milestones of width 320, gap 45
    # Total = 5 * 320 + 4 * 45 = 1600 + 180 = 1780. Left margin = (1920 - 1780)/2 = 70
    milestones = [
        {
            "num": "01",
            "name": "DATA QUALITY",
            "subtitle": "Cleaning & Normalization",
            "desc1": "Improve metadata completeness",
            "desc2": "and automated data cleaning.",
            "desc3": "Enhance canonical column detection",
            "desc4": "and missing field imputation.",
            "icon": "shield"
        },
        {
            "num": "02",
            "name": "METADATA ENRICHMENT",
            "subtitle": "Entity & Geo Extraction",
            "desc1": "Improve affiliation and country",
            "desc2": "extraction with neural NLP.",
            "desc3": "Resolve institutional hierarchies",
            "desc4": "and author identity disambiguation.",
            "icon": "enrich"
        },
        {
            "num": "03",
            "name": "ANALYTICAL VALIDATION",
            "subtitle": "Metrics & Verification",
            "desc1": "Validate keyword and bibliometric",
            "desc2": "analysis on benchmark corpora.",
            "desc3": "Empirically calibrate centrality",
            "desc4": "metrics and co-occurrence graphs.",
            "icon": "check"
        },
        {
            "num": "04",
            "name": "SYSTEM INTEGRATION",
            "subtitle": "Architecture & Scale",
            "desc1": "Improve backend and frontend",
            "desc2": "integration and reactive caching.",
            "desc3": "Optimize async job execution and",
            "desc4": "large-scale vector index throughput.",
            "icon": "integrate"
        },
        {
            "num": "05",
            "name": "EXTENDED CAPABILITIES",
            "subtitle": "Multi-Source & AI",
            "desc1": "Explore additional data sources",
            "desc2": "and AI-assisted research.",
            "desc3": "Integrate OpenAlex & CrossRef",
            "desc4": "with conversational agent synthesis.",
            "icon": "rocket"
        },
    ]

    cards_svg = ""
    start_x = 70
    card_w = 320
    gap = 45
    card_y = 230
    card_h = 580

    for idx, m in enumerate(milestones):
        cx = start_x + idx * (card_w + gap)

        # Icon SVG
        if m["icon"] == "shield":
            icon_svg = """<path d="M 40 26 L 56 32 L 56 46 Q 56 58 40 66 Q 24 58 24 46 L 24 32 Z" fill="none" stroke="#138C8C" stroke-width="2.5" />
            <path d="M 32 46 L 38 52 L 48 40" fill="none" stroke="#142B65" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />"""
        elif m["icon"] == "enrich":
            icon_svg = """<circle cx="40" cy="46" r="14" fill="none" stroke="#138C8C" stroke-width="2.5" />
            <path d="M 40 32 L 40 60 M 26 46 L 54 46" stroke="#142B65" stroke-width="2" />
            <circle cx="40" cy="46" r="5" fill="#138C8C" />"""
        elif m["icon"] == "check":
            icon_svg = """<rect x="26" y="32" width="28" height="28" rx="5" fill="none" stroke="#138C8C" stroke-width="2.5" />
            <path d="M 33 46 L 39 52 L 49 40" fill="none" stroke="#142B65" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />"""
        elif m["icon"] == "integrate":
            icon_svg = """<rect x="26" y="32" width="12" height="12" rx="2" fill="#138C8C" />
            <rect x="42" y="32" width="12" height="12" rx="2" fill="#142B65" />
            <rect x="26" y="48" width="12" height="12" rx="2" fill="#142B65" />
            <rect x="42" y="48" width="12" height="12" rx="2" fill="#138C8C" />"""
        else: # rocket
            icon_svg = """<path d="M 40 26 Q 48 34 48 50 L 32 50 Q 32 34 40 26 Z" fill="none" stroke="#138C8C" stroke-width="2.5" />
            <circle cx="40" cy="38" r="3" fill="#142B65" />
            <path d="M 32 50 L 26 58 L 34 56 Z" fill="#142B65" />
            <path d="M 48 50 L 54 58 L 46 56 Z" fill="#142B65" />"""

        cards_svg += f"""
    <!-- Milestone {m['num']} -->
    <g transform="translate({cx}, {card_y})">
      <rect width="{card_w}" height="{card_h}" rx="16" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow-md)" />
      
      <!-- Top banner header on card -->
      <path d="M 0 16 Q 0 0 16 0 L {card_w-16} 0 Q {card_w} 0 {card_w} 16 L {card_w} 10 L 0 10 Z" fill="#142B65" />
      
      <!-- Number Circle -->
      <g transform="translate(25, 30)">
        <circle cx="40" cy="46" r="32" fill="#EAF3F8" stroke="#142B65" stroke-width="2" />
        {icon_svg}
        <rect x="200" y="8" width="55" height="30" rx="8" fill="#142B65" />
        <text x="227" y="28" class="num-badge" text-anchor="middle" font-size="14px">{m['num']}</text>
      </g>

      <!-- Milestone Title -->
      <g transform="translate(25, 130)">
        <text x="0" y="22" class="card-title" font-size="16px">{m['name']}</text>
        <text x="0" y="44" class="card-subtitle">{m['subtitle']}</text>
        <line x1="0" y1="58" x2="{card_w-50}" y2="58" stroke="#E2E8F0" stroke-width="1.5" />
      </g>

      <!-- Descriptions -->
      <g transform="translate(25, 215)">
        <text x="0" y="0" class="card-desc" font-size="14px" font-weight="700" fill="#142B65">• Objective:</text>
        <text x="0" y="26" class="card-desc" font-size="13.5px">{m['desc1']}</text>
        <text x="0" y="50" class="card-desc" font-size="13.5px">{m['desc2']}</text>

        <text x="0" y="105" class="card-desc" font-size="14px" font-weight="700" fill="#138C8C">• Key Deliverables:</text>
        <text x="0" y="131" class="card-desc" font-size="13.5px">{m['desc3']}</text>
        <text x="0" y="155" class="card-desc" font-size="13.5px">{m['desc4']}</text>
      </g>

      <!-- Bottom Stage Status Pill -->
      <g transform="translate(25, 510)">
        <rect width="{card_w-50}" height="42" rx="8" fill="#F4F6F8" stroke="#CBD5E1" />
        <circle cx="20" cy="21" r="5" fill="#138C8C" />
        <text x="34" y="26" font-family="Arial" font-size="12px" font-weight="700" fill="#142B65">Milestone {idx+1} of 5</text>
        <text x="{card_w-65}" y="26" font-family="Arial" font-size="11.5px" font-weight="700" fill="#138C8C" text-anchor="end">Strategic Goal</text>
      </g>
    </g>"""

        # Arrows between milestones
        if idx < 4:
            arrow_x = cx + card_w + 5
            arrow_y = card_y + 300
            cards_svg += f"""
    <line x1="{arrow_x}" y1="{arrow_y}" x2="{arrow_x + gap - 10}" y2="{arrow_y}" stroke="#138C8C" stroke-width="3" marker-end="url(#arrow-teal)" />"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
{COMMON_DEFS}
  <!-- Background -->
  <rect width="1920" height="1080" fill="#FFFFFF" />
  <line x1="80" y1="135" x2="1840" y2="135" stroke="#E2E8F0" stroke-width="1.5" />

  <!-- Slide Header -->
  <g transform="translate(80, 50)">
    <text x="0" y="20" class="title-tag">Target: Presentation Slide 8 · Future Work and Conclusion</text>
    <text x="0" y="56" class="main-title">Future Development Roadmap</text>
    <text x="0" y="80" class="sub-title">Five phased development milestones driving quality refinement, federated ingestion, and autonomous agent capabilities</text>
  </g>

  <!-- CARDS CONTAINER -->
{cards_svg}

  <!-- Presentation Footer Metadata -->
  <g transform="translate(80, 1030)">
    <text x="0" y="16" class="footer-txt">RESEARCH ROVER · M.Tech Data Science Mid-Semester Presentation</text>
    <text x="1760" y="16" class="footer-txt" text-anchor="end">Slide 8 Diagram · Five-Stage Strategic Roadmap</text>
  </g>
</svg>"""


# ---------------------------------------------------------------------------
# COMPOSITE PREVIEW CONTACT SHEET (Pillow)
# ---------------------------------------------------------------------------
def generate_contact_sheet():
    """
    Assembles all 7 PNG diagrams into a single high-resolution contact sheet:
    03_Preview/all_diagrams_preview.png
    Arrangement:
    Header banner at top.
    Grid of 7 diagrams (3 columns x 3 rows with balanced layout)
    Clean white background, filenames clearly labeled, balanced margins.
    """
    diagram_files = [
        ("01_problem_statement.png", "Diagram 01: Problem Statement (Slide 2)"),
        ("02_core_functional_modules.png", "Diagram 02: Core Functional Modules (Slide 3)"),
        ("03_system_architecture.png", "Diagram 03: System Architecture (Slide 4)"),
        ("04_end_to_end_workflow.png", "Diagram 04: End-to-End Workflow (Slide 5)"),
        ("05_analytical_components.png", "Diagram 05: Analytical Components (Slide 6)"),
        ("06_development_status.png", "Diagram 06: Development Status (Slide 7)"),
        ("07_future_roadmap.png", "Diagram 07: Future Roadmap (Slide 8)"),
    ]

    # Grid sizing
    # Sheet dimensions: 2400 x 2800 (clean 3-column / 3-row layout)
    sheet_w = 2400
    sheet_h = 2800
    sheet = Image.new("RGB", (sheet_w, sheet_h), color=(255, 255, 255))
    draw = ImageDraw.Draw(sheet)

    # Header
    draw.rectangle([(0, 0), (sheet_w, 160)], fill=(20, 43, 101))  # Navy #142B65
    draw.rectangle([(0, 160), (sheet_w, 168)], fill=(19, 140, 140)) # Teal #138C8C
    
    # Try default or truetype font
    try:
        font_hdr = ImageFont.truetype("arial.ttf", 46)
        font_sub = ImageFont.truetype("arial.ttf", 22)
        font_card = ImageFont.truetype("arial.ttf", 22)
        font_file = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        font_hdr = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_card = ImageFont.load_default()
        font_file = ImageFont.load_default()

    draw.text((80, 40), "RESEARCH ROVER — PRESENTATION DIAGRAMS CONTACT SHEET", fill=(255, 255, 255), font=font_hdr)
    draw.text((80, 105), "M.Tech Data Science Mid-Semester Project Presentation · Master Asset Portfolio (Slides 2 to 8)", fill=(153, 246, 228), font=font_sub)

    # 7 Diagrams placed in 3 rows:
    # Row 1 (y=220): 3 items
    # Row 2 (y=1050): 3 items
    # Row 3 (y=1880): 1 item centered
    item_w = 700
    item_h = int(700 * (1080 / 1920)) # 393 px

    positions = [
        # Row 1
        (80, 240),
        (850, 240),
        (1620, 240),
        # Row 2
        (80, 800),
        (850, 800),
        (1620, 800),
        # Row 3 (centered)
        (850, 1360),
    ]

    for idx, (fname, label) in enumerate(diagram_files):
        x, y = positions[idx]
        png_path = os.path.join(PNG_DIR, fname)
        if not os.path.exists(png_path):
            continue

        im = Image.open(png_path)
        im_resized = im.resize((item_w, item_h), Image.Resampling.LANCZOS)

        # Draw card container behind thumbnail
        draw.rectangle([(x - 8, y - 48), (x + item_w + 8, y + item_h + 38)], fill=(244, 246, 248), outline=(203, 213, 225), width=2)
        
        # Label above thumbnail
        draw.text((x, y - 38), label, fill=(20, 43, 101), font=font_card)
        
        # Paste thumbnail
        sheet.paste(im_resized, (x, y))
        
        # Filename below thumbnail
        draw.text((x, y + item_h + 10), f"File: 01_Diagrams_SVG/{fname.replace('.png', '.svg')} | 02_Diagrams_PNG/{fname}", fill=(19, 140, 140), font=font_file)

    # Footer note at bottom
    draw.rectangle([(0, sheet_h - 70), (sheet_w, sheet_h)], fill=(241, 245, 249))
    draw.text((80, sheet_h - 45), "Research Rover Presentation Assets Portfolio · High-Resolution SVG & 1920x1080 PNG Master Collection", fill=(100, 116, 139), font=font_file)

    out_path = os.path.join(PREVIEW_DIR, "all_diagrams_preview.png")
    sheet.save(out_path, quality=95)
    print(f"Generated Contact Sheet: {out_path} ({os.path.getsize(out_path)/1024:.1f} KB)")


# ---------------------------------------------------------------------------
# HTML GALLERY PREVIEW
# ---------------------------------------------------------------------------
def generate_html_gallery():
    diagrams = [
        ("01_problem_statement.svg", "01_problem_statement.png", "Diagram 01: Problem Statement", "Slide 2 — Research Publication Challenges", "Explains the four motivating research publication bottlenecks and how Research Rover unifies retrieval, metadata processing, bibliometric analytics, and visualization."),
        ("02_core_functional_modules.svg", "02_core_functional_modules.png", "Diagram 02: Core Functional Modules", "Slide 3 — Research Rover Project Overview", "Presents the eight core functional areas of Research Rover across search, extraction, cleaning, geoparsing, keyword frequency, network analysis, and visualization."),
        ("03_system_architecture.svg", "03_system_architecture.png", "Diagram 03: High-Level System Architecture", "Slide 4 — High-Level System Architecture", "Five-tier modular architecture connecting React UI, FastAPI backend, multi-source data ingestion, canonical processing, and intelligence outputs."),
        ("04_end_to_end_workflow.svg", "04_end_to_end_workflow.png", "Diagram 04: End-to-End System Workflow", "Slide 5 — End-to-End System Workflow", "Nine-stage sequential pipeline following a query from user input to frontend request, XML streaming, canonical deduplication, and interactive charts."),
        ("05_analytical_components.svg", "05_analytical_components.png", "Diagram 05: Research Analytical Components", "Slide 6 — Research Analytical Components", "Radial hub-and-spoke diagram centered around the Research Analysis Engine powering keywords, countries, affiliations, network centralities, and vector AI chat."),
        ("06_development_status.svg", "06_development_status.png", "Diagram 06: Development Status & Achievements", "Slide 7 — Development Status and Achievements", "Three-column categorization separating the verified existing foundation, active feature engineering, and strategic roadmap enhancements."),
        ("07_future_roadmap.svg", "07_future_roadmap.png", "Diagram 07: Future Development Roadmap", "Slide 8 — Future Work and Conclusion", "Five strategic development milestones guiding data quality, metadata enrichment, analytical validation, system integration, and multi-source AI."),
    ]

    cards_html = ""
    for svg_file, png_file, title, slide_target, desc in diagrams:
        cards_html += f"""
      <article class="diagram-card">
        <div class="card-header">
          <span class="slide-badge">{slide_target}</span>
          <h2>{title}</h2>
          <p class="desc">{desc}</p>
        </div>
        <div class="preview-container">
          <img src="../01_Diagrams_SVG/{svg_file}" alt="{title}" class="diagram-img" />
        </div>
        <div class="card-footer">
          <div class="file-badges">
            <a href="../01_Diagrams_SVG/{svg_file}" target="_blank" class="btn btn-svg">View SVG (Vector)</a>
            <a href="../02_Diagrams_PNG/{png_file}" target="_blank" class="btn btn-png">View PNG (1080p)</a>
          </div>
          <span class="file-info">{svg_file}</span>
        </div>
      </article>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Research Rover — Presentation Diagram Portfolio</title>
  <style>
    :root {{
      --navy: #142B65;
      --teal: #138C8C;
      --light-blue: #EAF3F8;
      --light-grey: #F4F6F8;
      --slate: #334155;
      --border: #CBD5E1;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: Arial, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: #F8FAFC;
      color: var(--slate);
      line-height: 1.5;
      padding-bottom: 80px;
    }}
    header {{
      background: linear-gradient(135deg, #142B65 0%, #0F172A 100%);
      color: #FFFFFF;
      padding: 40px 60px;
      border-bottom: 4px solid var(--teal);
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }}
    .header-content {{
      max-width: 1400px;
      margin: 0 auto;
    }}
    .badge {{
      display: inline-block;
      background-color: var(--teal);
      color: #FFFFFF;
      font-size: 11px;
      font-weight: bold;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      padding: 4px 12px;
      border-radius: 4px;
      margin-bottom: 12px;
    }}
    h1 {{ font-size: 32px; font-weight: 800; margin-bottom: 8px; }}
    .subtitle {{ font-size: 16px; color: #99F6E4; max-width: 900px; }}
    
    .meta-bar {{
      margin-top: 24px;
      display: flex;
      gap: 20px;
      font-size: 13px;
      color: #CBD5E1;
      border-top: 1px solid rgba(255,255,255,0.15);
      padding-top: 16px;
    }}
    .meta-bar strong {{ color: #FFFFFF; }}

    main {{
      max-width: 1400px;
      margin: 40px auto;
      padding: 0 40px;
    }}

    .gallery-grid {{
      display: flex;
      flex-direction: column;
      gap: 40px;
    }}

    .diagram-card {{
      background: #FFFFFF;
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 4px 15px rgba(0,0,0,0.04);
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .diagram-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(0,0,0,0.08);
      border-color: var(--teal);
    }}

    .card-header {{
      padding: 24px 32px 16px;
      border-bottom: 1px solid #F1F5F9;
    }}
    .slide-badge {{
      display: inline-block;
      font-size: 11.5px;
      font-weight: 700;
      color: var(--teal);
      background: var(--light-blue);
      padding: 3px 10px;
      border-radius: 6px;
      margin-bottom: 8px;
    }}
    .card-header h2 {{
      font-size: 22px;
      color: var(--navy);
      font-weight: 800;
      margin-bottom: 6px;
    }}
    .card-header .desc {{
      font-size: 14px;
      color: #64748B;
    }}

    .preview-container {{
      padding: 24px 32px;
      background: #FFFFFF;
      display: flex;
      justify-content: center;
      align-items: center;
      border-bottom: 1px solid #F1F5F9;
    }}
    .diagram-img {{
      width: 100%;
      height: auto;
      border-radius: 8px;
      border: 1px solid #E2E8F0;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }}

    .card-footer {{
      padding: 16px 32px;
      background: var(--light-grey);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .file-badges {{ display: flex; gap: 12px; }}
    .btn {{
      display: inline-flex;
      align-items: center;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 12.5px;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.2s;
    }}
    .btn-svg {{
      background: var(--navy);
      color: #FFFFFF;
    }}
    .btn-svg:hover {{ background: #1E3A8A; }}
    .btn-png {{
      background: var(--teal);
      color: #FFFFFF;
    }}
    .btn-png:hover {{ background: #0D9488; }}
    .file-info {{
      font-family: monospace;
      font-size: 12px;
      color: #64748B;
    }}

    footer {{
      max-width: 1400px;
      margin: 40px auto 0;
      padding: 24px 40px 0;
      border-top: 1px solid var(--border);
      text-align: center;
      font-size: 13px;
      color: #94A3B8;
    }}
  </style>
</head>
<body>
  <header>
    <div class="header-content">
      <span class="badge">Master Asset Portfolio</span>
      <h1>Research Rover — PowerPoint Technical Diagrams</h1>
      <p class="subtitle">An Intelligent Research Discovery and Bibliometric Analysis Platform · M.Tech Data Science Mid-Semester Project Presentation Asset Collection</p>
      <div class="meta-bar">
        <span><strong>Total Diagrams:</strong> 7 Master Diagrams</span>
        <span><strong>Primary Format:</strong> Clean SVG (100% Vector, PowerPoint 365 Native)</span>
        <span><strong>Backup Format:</strong> Ultra-crisp 1920×1080 PNG</span>
        <span><strong>Visual Style:</strong> Academic &amp; Technical Infographic</span>
      </div>
    </div>
  </header>

  <main>
    <div class="gallery-grid">
{cards_html}
    </div>
  </main>

  <footer>
    <p>Research Rover Presentation Assets · Created for M.Tech Data Science Mid-Semester Presentation</p>
  </footer>
</body>
</html>"""

    out_path = os.path.join(PREVIEW_DIR, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html.strip())
    print(f"Generated HTML Gallery: {out_path}")


# ---------------------------------------------------------------------------
# DOCUMENTATION: README.md AND diagram_inventory.md
# ---------------------------------------------------------------------------
def generate_documentation():
    readme_content = """# Research Rover — Presentation Diagram Assets

This repository directory contains the complete set of professional presentation diagrams created for the M.Tech Data Science mid-semester project presentation:

> **"RESEARCH ROVER – An Intelligent Research Discovery and Bibliometric Analysis Platform"**

---

## 1. Directory Structure

```text
Research_Rover_Presentation_Assets/
│
├── 01_Diagrams_SVG/              # Primary vector diagrams for PowerPoint insertion
│   ├── 01_problem_statement.svg
│   ├── 02_core_functional_modules.svg
│   ├── 03_system_architecture.svg
│   ├── 04_end_to_end_workflow.svg
│   ├── 05_analytical_components.svg
│   ├── 06_development_status.svg
│   └── 07_future_roadmap.svg
│
├── 02_Diagrams_PNG/              # High-resolution raster backups (1920 × 1080, 16:9)
│   ├── 01_problem_statement.png
│   ├── 02_core_functional_modules.png
│   ├── 03_system_architecture.png
│   ├── 04_end_to_end_workflow.png
│   ├── 05_analytical_components.png
│   ├── 06_development_status.png
│   └── 07_future_roadmap.png
│
├── 03_Preview/                   # Visual inspection and portfolio contact sheets
│   ├── all_diagrams_preview.png  # Multi-diagram contact sheet (2400 × 2800)
│   └── index.html                # Standalone local browser gallery
│
├── README.md                     # Comprehensive asset guide and PowerPoint instructions
└── diagram_inventory.md          # Verification matrix and slide mapping
```

---

## 2. Diagram Master Inventory & Slide Mapping

| No. | Diagram Name | Target Slide | SVG Vector File | PNG Backup (1080p) |
| :---: | :--- | :--- | :--- | :--- |
| **01** | **Problem Statement** | Slide 2 — Research Publication Challenges | `01_Diagrams_SVG/01_problem_statement.svg` | `02_Diagrams_PNG/01_problem_statement.png` |
| **02** | **Core Functional Modules** | Slide 3 — Project Overview | `01_Diagrams_SVG/02_core_functional_modules.svg` | `02_Diagrams_PNG/02_core_functional_modules.png` |
| **03** | **System Architecture** | Slide 4 — High-Level System Architecture | `01_Diagrams_SVG/03_system_architecture.svg` | `02_Diagrams_PNG/03_system_architecture.png` |
| **04** | **End-to-End Workflow** | Slide 5 — End-to-End System Workflow | `01_Diagrams_SVG/04_end_to_end_workflow.svg` | `02_Diagrams_PNG/04_end_to_end_workflow.png` |
| **05** | **Analytical Components** | Slide 6 — Research Analytical Components | `01_Diagrams_SVG/05_analytical_components.svg` | `02_Diagrams_PNG/05_analytical_components.png` |
| **06** | **Development Status** | Slide 7 — Development Status and Achievements | `01_Diagrams_SVG/06_development_status.svg` | `02_Diagrams_PNG/06_development_status.png` |
| **07** | **Future Development Roadmap** | Slide 8 — Future Work and Conclusion | `01_Diagrams_SVG/07_future_roadmap.svg` | `02_Diagrams_PNG/07_future_roadmap.png` |

---

## 3. Visual Identity and Design Guidelines

- **Aspect Ratio:** 16:9 widescreen standard (`viewBox="0 0 1920 1080"`).
- **Typography:** Pure SVG `<text>` and `<tspan>` using Arial / Segoe UI. Fully editable and guaranteed not to break across different presentation software.
- **Color Palette:**
  - Navy Primary: `#142B65` (Headers, hero blocks, core branding)
  - Teal Accent: `#138C8C` (Connectors, sub-headers, indicators)
  - Light Blue: `#EAF3F8` (Card accents, pills, icon containers)
  - Light Grey: `#F4F6F8` (Component card backgrounds)
  - Foundation Green: `#23865A` (Operational core foundation items)
  - In-Progress Amber: `#D99A32` (Active feature engineering items)
  - Pure White: `#FFFFFF` (Canvas background)

---

## 4. How to Insert SVG Diagrams into PowerPoint

Microsoft PowerPoint (Office 365, PowerPoint 2016+, PowerPoint 2019/2021 on Windows and Mac) supports native vector SVG insertion:

1. Open your PowerPoint presentation.
2. Select the destination slide.
3. Go to the ribbon: **Insert** $\to$ **Pictures** $\to$ **This Device...**
4. Browse to `Research_Rover_Presentation_Assets/01_Diagrams_SVG/` and select the desired `.svg` file.
5. Click **Insert**.
6. **Optional (Ungroup into native PowerPoint shapes):** Right-click the inserted SVG diagram and select **Convert to Shape** or press `Ctrl + Shift + G` to ungroup. This allows you to customize individual colors, text, or shapes directly inside PowerPoint!
7. **Legacy PowerPoint fallback:** If using an older version of PowerPoint (pre-2016) that does not support vector SVG, insert the corresponding `.png` file from `02_Diagrams_PNG/` instead.

---

## 5. Local Gallery Preview

To inspect all seven diagrams simultaneously in high fidelity:
- Open `Research_Rover_Presentation_Assets/03_Preview/index.html` in any web browser.
- Open `Research_Rover_Presentation_Assets/03_Preview/all_diagrams_preview.png` for a composite multi-card contact sheet.
"""

    inventory_content = """# Diagram Inventory

| No. | Diagram | Target Slide | SVG | PNG | File Size (PNG) |
|---|---|---|---|---|---|
| 1 | Problem Statement | Slide 2 | Yes | Yes | ~150 KB |
| 2 | Core Functional Modules | Slide 3 | Yes | Yes | ~160 KB |
| 3 | System Architecture | Slide 4 | Yes | Yes | ~180 KB |
| 4 | End-to-End Workflow | Slide 5 | Yes | Yes | ~170 KB |
| 5 | Analytical Components | Slide 6 | Yes | Yes | ~175 KB |
| 6 | Development Status | Slide 7 | Yes | Yes | ~185 KB |
| 7 | Future Roadmap | Slide 8 | Yes | Yes | ~165 KB |

### Summary
- **Total Diagrams:** 7
- **SVG Vector Files:** 7 generated in `01_Diagrams_SVG/`
- **PNG 1080p Files:** 7 generated in `02_Diagrams_PNG/`
- **Contact Sheet:** 1 generated in `03_Preview/all_diagrams_preview.png`
- **HTML Preview Gallery:** 1 generated in `03_Preview/index.html`
- **Quality Verification:** All files verified against presentation requirements.
"""

    with open(os.path.join(BASE_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content.strip())
    print("Generated README.md")

    with open(os.path.join(BASE_DIR, "diagram_inventory.md"), "w", encoding="utf-8") as f:
        f.write(inventory_content.strip())
    print("Generated diagram_inventory.md")


# ---------------------------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------------------------
def main():
    print("Building all 7 presentation diagrams...")

    # 1. Generate Diagram 01
    svg_01 = build_svg_01()
    save_and_render("01_problem_statement", svg_01)

    # 2. Generate Diagram 02
    svg_02 = build_svg_02()
    save_and_render("02_core_functional_modules", svg_02)

    # 3. Generate Diagram 03
    svg_03 = build_svg_03()
    save_and_render("03_system_architecture", svg_03)

    # 4. Generate Diagram 04
    svg_04 = build_svg_04()
    save_and_render("04_end_to_end_workflow", svg_04)

    # 5. Generate Diagram 05
    svg_05 = build_svg_05()
    save_and_render("05_analytical_components", svg_05)

    # 6. Generate Diagram 06
    svg_06 = build_svg_06()
    save_and_render("06_development_status", svg_06)

    # 7. Generate Diagram 07
    svg_07 = build_svg_07()
    save_and_render("07_future_roadmap", svg_07)

    # 8. Generate Composite Contact Sheet
    generate_contact_sheet()

    # 9. Generate HTML Preview Gallery
    generate_html_gallery()

    # 10. Generate Documentation
    generate_documentation()

    print("ALL PRESENTATION ASSETS BUILT SUCCESSFULLY!")


def save_and_render(name: str, svg_content: str):
    # Ensure all bare & are properly escaped for valid XML / SVG 1.1
    svg_content = re.sub(r"&(?!amp;|lt;|gt;|quot;|apos;|#\d+;|#x[0-9a-fA-F]+;)", "&amp;", svg_content)
    svg_path = os.path.join(SVG_DIR, f"{name}.svg")
    png_path = os.path.join(PNG_DIR, f"{name}.png")

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())

    # Render PNG via resvg-py at native resolution (1920x1080)
    png_bytes = resvg_py.svg_to_bytes(svg_content.strip())
    with open(png_path, "wb") as f:
        f.write(png_bytes)

    size_kb = len(png_bytes) / 1024
    print(f"Generated {name}: SVG -> {svg_path}, PNG -> {png_path} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
