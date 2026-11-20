"""
Generate publication-quality, presentation-ready standalone SVG files for
Research Rover UML Use Case Diagram and 5 Activity Diagrams.
Designed for M.Tech project presentation, thesis report, and demonstration.
"""

import os
from pathlib import Path

OUT_DIR = Path(__file__).parent

def create_use_case_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1150" width="1600" height="1150" style="background:#ffffff; font-family:'Segoe UI', Inter, -apple-system, sans-serif;">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="2" dy="3" stdDeviation="3" flood-opacity="0.12"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb" />
    </marker>
    <marker id="arrow-dash" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#475569" />
    </marker>
    <marker id="gen-arrow" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 11 6 L 0 11 z" fill="#ffffff" stroke="#2563eb" stroke-width="1.5"/>
    </marker>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="ucGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
    <linearGradient id="actorGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#eff6ff"/>
      <stop offset="100%" stop-color="#dbeafe"/>
    </linearGradient>
  </defs>

  <!-- Title Banner -->
  <rect x="30" y="20" width="1540" height="70" rx="12" fill="url(#headerGrad)" filter="url(#shadow)"/>
  <text x="50" y="52" fill="#38bdf8" font-size="13" font-weight="700" letter-spacing="2">UML 2.5 USE CASE MODEL</text>
  <text x="50" y="74" fill="#ffffff" font-size="20" font-weight="bold">Research Rover: Comprehensive System Functional Capabilities</text>
  <text x="1350" y="60" fill="#94a3b8" font-size="13" font-weight="500">M.Tech Software Architecture</text>

  <!-- Left: Primary Actor -->
  <g transform="translate(40, 480)">
    <rect x="0" y="0" width="170" height="230" rx="14" fill="url(#actorGrad)" stroke="#3b82f6" stroke-width="2" filter="url(#shadow)"/>
    <circle cx="85" cy="45" r="20" fill="#1e40af" stroke="#1d4ed8" stroke-width="2"/>
    <line x1="85" y1="65" x2="85" y2="120" stroke="#1d4ed8" stroke-width="4"/>
    <line x1="45" y1="85" x2="125" y2="85" stroke="#1d4ed8" stroke-width="4" stroke-linecap="round"/>
    <line x1="85" y1="120" x2="55" y2="175" stroke="#1d4ed8" stroke-width="4" stroke-linecap="round"/>
    <line x1="85" y1="120" x2="115" y2="175" stroke="#1d4ed8" stroke-width="4" stroke-linecap="round"/>
    <text x="85" y="198" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">&lt;&lt;human actor&gt;&gt;</text>
    <text x="85" y="216" text-anchor="middle" font-size="13" font-weight="600" fill="#2563eb">Researcher / Student</text>
  </g>

  <!-- System Boundary Box -->
  <rect x="250" y="110" width="1070" height="1000" rx="16" fill="#fafafa" stroke="#cbd5e1" stroke-width="2.5" stroke-dasharray="8 6"/>
  <rect x="270" y="98" width="310" height="26" rx="6" fill="#2563eb"/>
  <text x="280" y="116" fill="#ffffff" font-size="13" font-weight="bold" letter-spacing="1">SYSTEM: RESEARCH ROVER (v2.0)</text>

  <!-- Subgroup A: Research Search -->
  <rect x="270" y="140" width="1030" height="210" rx="12" fill="#ffffff" stroke="#93c5fd" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="290" y="165" font-size="13" font-weight="700" fill="#1e40af">A. RESEARCH PAPER SEARCH MODULE</text>

  <g transform="translate(290, 180)">
    <rect id="uc1" x="0" y="0" width="200" height="48" rx="24" fill="url(#ucGrad)" stroke="#2563eb" stroke-width="1.8"/>
    <text x="100" y="22" text-anchor="middle" font-size="12" font-weight="bold" fill="#0f172a">Search Research Papers</text>
    <text x="100" y="38" text-anchor="middle" font-size="10" fill="#64748b">(Base Use Case)</text>

    <rect id="uc1_1" x="270" y="-30" width="180" height="40" rx="20" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="360" y="-10" text-anchor="middle" font-size="11" font-weight="600" fill="#1e3a8a">Unified Search</text>
    <text x="360" y="4" text-anchor="middle" font-size="9" fill="#64748b">(PubMed + OpenAlex)</text>

    <rect id="uc1_2" x="270" y="20" width="180" height="40" rx="20" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="360" y="38" text-anchor="middle" font-size="11" font-weight="600" fill="#1e3a8a">PubMed Search</text>
    <text x="360" y="50" text-anchor="middle" font-size="9" fill="#64748b">(NCBI E-Utilities)</text>

    <rect id="uc1_3" x="270" y="70" width="180" height="40" rx="20" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="360" y="88" text-anchor="middle" font-size="11" font-weight="600" fill="#1e3a8a">OpenAlex Search</text>
    <text x="360" y="100" text-anchor="middle" font-size="9" fill="#64748b">(Academic Works API)</text>

    <rect id="uc_opt" x="510" y="-30" width="220" height="40" rx="20" fill="#f8fafc" stroke="#64748b" stroke-width="1.5"/>
    <text x="620" y="-12" text-anchor="middle" font-size="11" font-weight="600" fill="#0f172a">Optimize Query &amp; Synonyms</text>
    <text x="620" y="2" text-anchor="middle" font-size="9" fill="#64748b">(ml, dl, iiot abbreviation expand)</text>

    <rect id="uc_rerank" x="510" y="20" width="220" height="40" rx="20" fill="#fdf4ff" stroke="#a855f7" stroke-width="1.5"/>
    <text x="620" y="38" text-anchor="middle" font-size="11" font-weight="600" fill="#581c87">Re-Rank by MedCPT Score</text>
    <text x="620" y="50" text-anchor="middle" font-size="9" fill="#7e22ce">(Semantic Relevance Bi-Encoder)</text>

    <rect id="uc_browse" x="780" y="-10" width="200" height="46" rx="23" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
    <text x="880" y="12" text-anchor="middle" font-size="11" font-weight="700" fill="#14532d">Browse Paginated Results</text>
    <text x="880" y="28" text-anchor="middle" font-size="9" fill="#15803d">(PMID, DOI, Match %, Citations)</text>

    <rect id="uc_pdf" x="780" y="65" width="200" height="44" rx="22" fill="#fff1f2" stroke="#e11d48" stroke-width="1.5"/>
    <text x="880" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="#881337">Download Full-Text PDF</text>
    <text x="880" y="100" text-anchor="middle" font-size="9" fill="#9f1239">(SSRF-Safe Proxy Stream)</text>
  </g>

  <!-- Connectors in Search -->
  <path d="M 490 204 L 560 170" fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#gen-arrow)"/>
  <path d="M 490 204 L 560 220" fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#gen-arrow)"/>
  <path d="M 490 204 L 560 270" fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#gen-arrow)"/>

  <path d="M 490 195 L 795 165" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <text x="650" y="174" fill="#475569" font-size="9" font-weight="600">&lt;&lt;include&gt;&gt;</text>

  <path d="M 795 220 L 490 215" fill="none" stroke="#9333ea" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <text x="650" y="213" fill="#9333ea" font-size="9" font-weight="600">&lt;&lt;extend&gt;&gt;</text>

  <path d="M 490 225 L 1070 195" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <text x="910" y="200" fill="#475569" font-size="9" font-weight="600">&lt;&lt;include&gt;&gt;</text>

  <path d="M 1170 245 L 1170 215" fill="none" stroke="#be123c" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <text x="1178" y="235" fill="#be123c" font-size="9" font-weight="600">&lt;&lt;extend&gt;&gt;</text>

  <!-- Subgroup B: Dataset Management -->
  <rect x="270" y="365" width="1030" height="135" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="290" y="388" font-size="13" font-weight="700" fill="#334155">B. DATASET MANAGEMENT MODULE</text>

  <g transform="translate(290, 400)">
    <rect x="0" y="15" width="220" height="42" rx="21" fill="url(#ucGrad)" stroke="#0284c7" stroke-width="1.6"/>
    <text x="110" y="34" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">Upload Research Dataset</text>
    <text x="110" y="48" text-anchor="middle" font-size="9" fill="#64748b">(CSV Validation &amp; Encoding Detect)</text>

    <rect x="260" y="15" width="220" height="42" rx="21" fill="url(#ucGrad)" stroke="#0284c7" stroke-width="1.6"/>
    <text x="370" y="34" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">List &amp; Switch Datasets</text>
    <text x="370" y="48" text-anchor="middle" font-size="9" fill="#64748b">(Auto-Discovered from data/)</text>

    <rect x="520" y="15" width="220" height="42" rx="21" fill="url(#ucGrad)" stroke="#0284c7" stroke-width="1.6"/>
    <text x="630" y="34" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">Export Clean Dataset CSV</text>
    <text x="630" y="48" text-anchor="middle" font-size="9" fill="#64748b">(Unpolluted Metadata Export)</text>

    <rect x="780" y="15" width="220" height="42" rx="21" fill="url(#ucGrad)" stroke="#dc2626" stroke-width="1.5"/>
    <text x="890" y="34" text-anchor="middle" font-size="11" font-weight="bold" fill="#991b1b">Delete Dataset &amp; Index</text>
    <text x="890" y="48" text-anchor="middle" font-size="9" fill="#b91c1c">(Disk Cleanup)</text>
  </g>

  <!-- Subgroup C: Keyword Analytics -->
  <rect x="270" y="515" width="1030" height="195" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="290" y="538" font-size="13" font-weight="700" fill="#0369a1">C. KEYWORD BIBLIOMETRIC ANALYTICS MODULE</text>

  <g transform="translate(290, 550)">
    <rect x="0" y="40" width="200" height="46" rx="23" fill="url(#ucGrad)" stroke="#0284c7" stroke-width="1.8"/>
    <text x="100" y="62" text-anchor="middle" font-size="12" font-weight="bold" fill="#0f172a">Generate Keyword Analytics</text>
    <text x="100" y="76" text-anchor="middle" font-size="9" fill="#64748b">(5-Phase Computation Pipeline)</text>

    <rect x="250" y="0" width="230" height="38" rx="19" fill="#f8fafc" stroke="#64748b" stroke-width="1.4"/>
    <text x="365" y="18" text-anchor="middle" font-size="11" font-weight="600" fill="#0f172a">Normalize Keywords &amp; Synonyms</text>
    <text x="365" y="30" text-anchor="middle" font-size="9" fill="#64748b">(ast parsing, alias replacement)</text>

    <rect x="250" y="48" width="230" height="38" rx="19" fill="#f8fafc" stroke="#64748b" stroke-width="1.4"/>
    <text x="365" y="66" text-anchor="middle" font-size="11" font-weight="600" fill="#0f172a">Inspect Frequency Distributions</text>
    <text x="365" y="78" text-anchor="middle" font-size="9" fill="#64748b">(Top-N Limit, Min Frequency)</text>

    <rect x="250" y="96" width="230" height="38" rx="19" fill="#f8fafc" stroke="#64748b" stroke-width="1.4"/>
    <text x="365" y="114" text-anchor="middle" font-size="11" font-weight="600" fill="#0f172a">Compute NetworkX Centralities</text>
    <text x="365" y="126" text-anchor="middle" font-size="9" fill="#64748b">(Degree, Betweenness, Eigenvector)</text>

    <rect x="520" y="10" width="220" height="40" rx="20" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="630" y="28" text-anchor="middle" font-size="11" font-weight="600" fill="#1e3a8a">Explore Interactive Word Cloud</text>
    <text x="630" y="42" text-anchor="middle" font-size="9" fill="#64748b">(Zoom / Pan / SVG &amp; PNG Export)</text>

    <rect x="520" y="60" width="220" height="40" rx="20" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="630" y="78" text-anchor="middle" font-size="11" font-weight="600" fill="#1e3a8a">Explore Co-Occurrence Graph</text>
    <text x="630" y="92" text-anchor="middle" font-size="9" fill="#64748b">(Pairwise Weighted Graph)</text>

    <rect x="780" y="20" width="220" height="40" rx="20" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
    <text x="890" y="38" text-anchor="middle" font-size="11" font-weight="600" fill="#14532d">Binary Presence Matrix</text>
    <text x="890" y="52" text-anchor="middle" font-size="9" fill="#15803d">(Paper vs Keyword 0/1 Matrix)</text>

    <rect x="780" y="70" width="220" height="40" rx="20" fill="#f8fafc" stroke="#475569" stroke-width="1.5"/>
    <text x="890" y="88" text-anchor="middle" font-size="11" font-weight="600" fill="#0f172a">Export Analytics Artifacts</text>
    <text x="890" y="102" text-anchor="middle" font-size="9" fill="#64748b">(CSVs &amp; JSON Summary)</text>
  </g>

  <!-- Connectors in Keyword -->
  <path d="M 490 610 L 540 575" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <path d="M 490 613 L 540 615" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <path d="M 490 618 L 540 660" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>

  <path d="M 810 578 L 490 605" fill="none" stroke="#2563eb" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <path d="M 810 630 L 490 620" fill="none" stroke="#2563eb" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>

  <!-- Subgroup D: Country Analysis -->
  <rect x="270" y="725" width="1030" height="190" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="290" y="748" font-size="13" font-weight="700" fill="#047857">D. COUNTRY &amp; INTERNATIONAL COLLABORATION MODULE</text>

  <g transform="translate(290, 760)">
    <rect x="0" y="35" width="200" height="46" rx="23" fill="url(#ucGrad)" stroke="#059669" stroke-width="1.8"/>
    <text x="100" y="56" text-anchor="middle" font-size="12" font-weight="bold" fill="#0f172a">Analyze Country Output</text>
    <text x="100" y="70" text-anchor="middle" font-size="9" fill="#64748b">(Geographic Bibliometrics)</text>

    <rect x="250" y="0" width="230" height="38" rx="19" fill="#f8fafc" stroke="#64748b" stroke-width="1.4"/>
    <text x="365" y="18" text-anchor="middle" font-size="11" font-weight="600" fill="#0f172a">Extract Affiliation Countries</text>
    <text x="365" y="30" text-anchor="middle" font-size="9" fill="#64748b">(Regex &amp; ISO-3166-1 Map)</text>

    <rect x="250" y="48" width="230" height="38" rx="19" fill="#fff7ed" stroke="#f97316" stroke-width="1.4"/>
    <text x="365" y="66" text-anchor="middle" font-size="11" font-weight="600" fill="#c2410c">Track Unassigned Papers</text>
    <text x="365" y="78" text-anchor="middle" font-size="9" fill="#ea580c">(No Speculation / Inspection Modal)</text>

    <rect x="250" y="96" width="230" height="38" rx="19" fill="#f8fafc" stroke="#64748b" stroke-width="1.4"/>
    <text x="365" y="114" text-anchor="middle" font-size="11" font-weight="600" fill="#0f172a">Inspect Country Ranking Table</text>
    <text x="365" y="126" text-anchor="middle" font-size="9" fill="#64748b">(Searchable, Volume &amp; %)</text>

    <rect x="520" y="15" width="220" height="42" rx="21" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
    <text x="630" y="34" text-anchor="middle" font-size="11" font-weight="600" fill="#065f46">Explore TopoJSON World Map</text>
    <text x="630" y="48" text-anchor="middle" font-size="9" fill="#047857">(Choropleth Shading &amp; Tooltips)</text>

    <rect x="520" y="68" width="220" height="42" rx="21" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
    <text x="630" y="87" text-anchor="middle" font-size="11" font-weight="600" fill="#065f46">Explore 2D/3D Collaboration</text>
    <text x="630" y="101" text-anchor="middle" font-size="9" fill="#047857">(D3 Force &amp; Three.js Space)</text>

    <rect x="780" y="42" width="220" height="42" rx="21" fill="#f8fafc" stroke="#475569" stroke-width="1.5"/>
    <text x="890" y="61" text-anchor="middle" font-size="11" font-weight="600" fill="#0f172a">Export Country Data</text>
    <text x="890" y="75" text-anchor="middle" font-size="9" fill="#64748b">(Rankings &amp; Partnerships CSV)</text>
  </g>

  <!-- Connectors in Country -->
  <path d="M 490 810 L 540 780" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <path d="M 490 818 L 540 825" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <path d="M 490 825 L 540 870" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>

  <path d="M 810 790 L 490 812" fill="none" stroke="#059669" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <path d="M 810 845 L 490 820" fill="none" stroke="#059669" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>

  <!-- Subgroup E: AI Assistant -->
  <rect x="270" y="930" width="1030" height="165" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="290" y="953" font-size="13" font-weight="700" fill="#6d28d9">E. AI RESEARCH ASSISTANT (RAG) MODULE</text>

  <g transform="translate(290, 965)">
    <rect x="0" y="25" width="200" height="46" rx="23" fill="url(#ucGrad)" stroke="#7c3aed" stroke-width="1.8"/>
    <text x="100" y="46" text-anchor="middle" font-size="12" font-weight="bold" fill="#0f172a">Ask Research Question</text>
    <text x="100" y="60" text-anchor="middle" font-size="9" fill="#64748b">(Conversational RAG Q&amp;A)</text>

    <rect x="250" y="5" width="230" height="40" rx="20" fill="#f8fafc" stroke="#64748b" stroke-width="1.4"/>
    <text x="365" y="23" text-anchor="middle" font-size="11" font-weight="600" fill="#0f172a">Generate Vector Embeddings</text>
    <text x="365" y="37" text-anchor="middle" font-size="9" fill="#64748b">(SentenceTransformer: mpnet, 768-d)</text>

    <rect x="250" y="55" width="230" height="40" rx="20" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="1.4"/>
    <text x="365" y="73" text-anchor="middle" font-size="11" font-weight="600" fill="#4c1d95">Decompose Query to Sub-queries</text>
    <text x="365" y="87" text-anchor="middle" font-size="9" fill="#6d28d9">(Multi-Angle Search Strategy)</text>

    <rect x="520" y="5" width="220" height="40" rx="20" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="1.4"/>
    <text x="630" y="23" text-anchor="middle" font-size="11" font-weight="600" fill="#4c1d95">Retrieve FAISS Chunks</text>
    <text x="630" y="37" text-anchor="middle" font-size="9" fill="#6d28d9">(Nearest Neighbor Search &amp; Dedup)</text>

    <rect x="520" y="55" width="220" height="40" rx="20" fill="#faf5ff" stroke="#c084fc" stroke-width="1.4"/>
    <text x="630" y="73" text-anchor="middle" font-size="11" font-weight="600" fill="#581c87">Scrape Full Text from URLs</text>
    <text x="630" y="87" text-anchor="middle" font-size="9" fill="#7e22ce">(Toggle for Deep Content Index)</text>

    <rect x="780" y="30" width="220" height="46" rx="23" fill="#fdf2f8" stroke="#db2777" stroke-width="1.6"/>
    <text x="890" y="51" text-anchor="middle" font-size="11" font-weight="700" fill="#831843">Synthesize Grounded Answer</text>
    <text x="890" y="65" text-anchor="middle" font-size="9" fill="#9d174d">(Streamed Response + Paper Citations)</text>
  </g>

  <!-- Connectors in AI -->
  <path d="M 490 1005 L 540 985" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <path d="M 490 1015 L 540 1030" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <path d="M 740 1035 L 810 1000" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <path d="M 770 1035 L 1070 1025" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <path d="M 810 1040 L 740 990" fill="none" stroke="#9333ea" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>

  <!-- Right: External System Actors -->
  <g transform="translate(1360, 160)">
    <rect x="0" y="0" width="200" height="90" rx="12" fill="#f8fafc" stroke="#0284c7" stroke-width="1.8" filter="url(#shadow)"/>
    <text x="100" y="30" text-anchor="middle" font-size="11" font-weight="bold" fill="#0369a1">&lt;&lt;external system&gt;&gt;</text>
    <text x="100" y="52" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">NCBI Entrez E-Utilities</text>
    <text x="100" y="70" text-anchor="middle" font-size="10" fill="#64748b">esearch / efetch / espell</text>

    <rect x="0" y="115" width="200" height="90" rx="12" fill="#f8fafc" stroke="#0d9488" stroke-width="1.8" filter="url(#shadow)"/>
    <text x="100" y="145" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f766e">&lt;&lt;external system&gt;&gt;</text>
    <text x="100" y="167" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">OpenAlex Academic API</text>
    <text x="100" y="185" text-anchor="middle" font-size="10" fill="#64748b">Works, Citations &amp; OA URLs</text>

    <rect x="0" y="230" width="200" height="90" rx="12" fill="#f8fafc" stroke="#e11d48" stroke-width="1.8" filter="url(#shadow)"/>
    <text x="100" y="260" text-anchor="middle" font-size="11" font-weight="bold" fill="#be123c">&lt;&lt;external system&gt;&gt;</text>
    <text x="100" y="282" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Publishers &amp; PMC</text>
    <text x="100" y="300" text-anchor="middle" font-size="10" fill="#64748b">Direct Open-Access PDFs</text>

    <rect x="0" y="790" width="200" height="90" rx="12" fill="#f8fafc" stroke="#9333ea" stroke-width="1.8" filter="url(#shadow)"/>
    <text x="100" y="820" text-anchor="middle" font-size="11" font-weight="bold" fill="#7e22ce">&lt;&lt;external system&gt;&gt;</text>
    <text x="100" y="842" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Google Gemini AI</text>
    <text x="100" y="860" text-anchor="middle" font-size="10" fill="#64748b">LLM Synthesis &amp; RAG Chat</text>
  </g>

  <!-- External Actor Associations -->
  <line x1="740" y1="210" x2="1360" y2="205" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="2 2"/>
  <line x1="740" y1="260" x2="1360" y2="320" stroke="#0d9488" stroke-width="1.5" stroke-dasharray="2 2"/>
  <line x1="1270" y1="270" x2="1360" y2="435" stroke="#e11d48" stroke-width="1.5" stroke-dasharray="2 2"/>
  <line x1="1290" y1="1025" x2="1360" y2="995" stroke="#9333ea" stroke-width="1.5" stroke-dasharray="2 2"/>

  <!-- Primary User Associations -->
  <line x1="210" y1="520" x2="290" y2="204" stroke="#2563eb" stroke-width="1.8"/>
  <line x1="210" y1="550" x2="290" y2="430" stroke="#0284c7" stroke-width="1.8"/>
  <line x1="210" y1="580" x2="290" y2="615" stroke="#0284c7" stroke-width="1.8"/>
  <line x1="210" y1="620" x2="290" y2="815" stroke="#059669" stroke-width="1.8"/>
  <line x1="210" y1="660" x2="290" y2="1015" stroke="#7c3aed" stroke-width="1.8"/>

  <!-- Legend Bottom Bar -->
  <rect x="30" y="1115" width="1540" height="28" rx="6" fill="#f1f5f9" stroke="#e2e8f0"/>
  <text x="50" y="1133" font-size="11" font-weight="bold" fill="#334155">LEGEND:</text>
  <line x1="120" y1="1130" x2="160" y2="1130" stroke="#2563eb" stroke-width="2"/>
  <text x="170" y="1134" font-size="11" fill="#475569">Actor Association</text>

  <line x1="300" y1="1130" x2="340" y2="1130" stroke="#475569" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <text x="350" y="1134" font-size="11" fill="#475569">&lt;&lt;include&gt;&gt; (Mandatory Reused)</text>

  <line x1="560" y1="1130" x2="600" y2="1130" stroke="#9333ea" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <text x="610" y="1134" font-size="11" fill="#475569">&lt;&lt;extend&gt;&gt; (Conditional / Optional)</text>

  <line x1="840" y1="1130" x2="880" y2="1130" stroke="#2563eb" stroke-width="1.5" marker-end="url(#gen-arrow)"/>
  <text x="890" y="1134" font-size="11" fill="#475569">Generalization (Specialized Variant)</text>
</svg>'''

def create_activity_1_search_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1200" width="1600" height="1200" style="background:#ffffff; font-family:'Segoe UI', Inter, -apple-system, sans-serif;">
  <defs>
    <filter id="shadow1" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="1" dy="2" stdDeviation="2.5" flood-opacity="0.1"/>
    </filter>
    <marker id="arr1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#3b82f6"/>
    </marker>
    <linearGradient id="headerGrad1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
  </defs>

  <rect x="30" y="20" width="1540" height="70" rx="12" fill="url(#headerGrad1)" filter="url(#shadow1)"/>
  <text x="50" y="50" fill="#38bdf8" font-size="12" font-weight="700" letter-spacing="2">UML 2.5 ACTIVITY DIAGRAM</text>
  <text x="50" y="74" fill="#ffffff" font-size="20" font-weight="bold">Activity Diagram 1: Research Paper Search &amp; Retrieval Workflow</text>
  <text x="1350" y="60" fill="#94a3b8" font-size="13">Verified Source: search.py &amp; services/</text>

  <!-- Swimlane Headers -->
  <rect x="30" y="105" width="370" height="1040" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="30" y="105" width="370" height="40" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
  <text x="215" y="130" text-anchor="middle" font-size="14" font-weight="bold" fill="#1e40af">Researcher / Student (User)</text>

  <rect x="400" y="105" width="410" height="1040" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="400" y="105" width="410" height="40" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5"/>
  <text x="605" y="130" text-anchor="middle" font-size="14" font-weight="bold" fill="#166534">Frontend UI (SearchPage.tsx &amp; Context)</text>

  <rect x="810" y="105" width="440" height="1040" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="810" y="105" width="440" height="40" fill="#faf5ff" stroke="#d8b4fe" stroke-width="1.5"/>
  <text x="1030" y="130" text-anchor="middle" font-size="14" font-weight="bold" fill="#6b21a8">Backend Services (FastAPI &amp; MedCPT)</text>

  <rect x="1250" y="105" width="320" height="1040" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="1250" y="105" width="320" height="40" fill="#fff1f2" stroke="#fecdd3" stroke-width="1.5"/>
  <text x="1410" y="130" text-anchor="middle" font-size="14" font-weight="bold" fill="#9f1239">External Academic APIs &amp; Hosts</text>

  <!-- Nodes -->
  <circle cx="215" cy="180" r="14" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <path d="M 215 194 L 215 220" fill="none" stroke="#3b82f6" stroke-width="2" marker-end="url(#arr1)"/>

  <rect x="105" y="220" width="220" height="50" rx="10" fill="#ffffff" stroke="#3b82f6" stroke-width="1.8" filter="url(#shadow1)"/>
  <text x="215" y="242" text-anchor="middle" font-size="12" font-weight="600" fill="#1e293b">Open Research Rover</text>
  <text x="215" y="258" text-anchor="middle" font-size="11" fill="#64748b">&amp; Enter Research Query</text>

  <path d="M 215 270 L 215 300" fill="none" stroke="#3b82f6" stroke-width="2" marker-end="url(#arr1)"/>

  <!-- Decision: Filters? -->
  <polygon points="215,300 295,330 215,360 135,330" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
  <text x="215" y="334" text-anchor="middle" font-size="11" font-weight="bold" fill="#92400e">Configure Filters?</text>

  <path d="M 295 330 L 340 330 L 340 400 L 295 400" fill="none" stroke="#d97706" stroke-width="1.8" marker-end="url(#arr1)"/>
  <text x="345" y="360" font-size="10" font-weight="bold" fill="#b45309">[Yes]</text>
  <rect x="105" y="380" width="190" height="44" rx="8" fill="#ffffff" stroke="#d97706" stroke-width="1.5" filter="url(#shadow1)"/>
  <text x="200" y="399" text-anchor="middle" font-size="11" font-weight="600" fill="#1e293b">Set Slider Year Bounds,</text>
  <text x="200" y="413" text-anchor="middle" font-size="10" fill="#64748b">Max Results &amp; Sort Mode</text>

  <path d="M 215 360 L 215 440" fill="none" stroke="#3b82f6" stroke-width="2" marker-end="url(#arr1)"/>
  <text x="220" y="375" font-size="10" font-weight="bold" fill="#64748b">[No]</text>
  <path d="M 200 424 L 200 440" fill="none" stroke="#3b82f6" stroke-width="1.5"/>

  <rect x="105" y="440" width="220" height="46" rx="10" fill="#ffffff" stroke="#3b82f6" stroke-width="1.8" filter="url(#shadow1)"/>
  <text x="215" y="462" text-anchor="middle" font-size="12" font-weight="bold" fill="#1e293b">Submit Search Request</text>
  <text x="215" y="476" text-anchor="middle" font-size="10" fill="#64748b">(Click Search Button)</text>

  <path d="M 325 463 L 470 463" fill="none" stroke="#3b82f6" stroke-width="2" marker-end="url(#arr1)"/>

  <polygon points="560,440 640,465 560,490 480,465" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
  <text x="560" y="469" text-anchor="middle" font-size="11" font-weight="bold" fill="#92400e">Is Query Valid?</text>

  <path d="M 560 440 L 560 250 L 325 250" fill="none" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#arr1)"/>
  <text x="568" y="350" font-size="10" font-weight="bold" fill="#dc2626">[Invalid: Display Alert &amp; Re-prompt]</text>

  <path d="M 640 465 L 700 465 L 700 520 L 500 520 L 500 540" fill="none" stroke="#3b82f6" stroke-width="2" marker-end="url(#arr1)"/>
  <text x="645" y="460" font-size="10" font-weight="bold" fill="#16a34a">[Valid]</text>

  <rect x="440" y="540" width="240" height="46" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="1.5" filter="url(#shadow1)"/>
  <text x="560" y="560" text-anchor="middle" font-size="11" font-weight="600" fill="#14532d">Dispatch POST /api/v1/search/</text>
  <text x="560" y="574" text-anchor="middle" font-size="10" fill="#15803d">&amp; Initialize Stepper Progress Panel</text>

  <path d="M 680 563 L 880 563" fill="none" stroke="#3b82f6" stroke-width="2" marker-end="url(#arr1)"/>

  <rect x="880" y="540" width="250" height="48" rx="8" fill="#ffffff" stroke="#7c3aed" stroke-width="1.6" filter="url(#shadow1)"/>
  <text x="1005" y="560" text-anchor="middle" font-size="11" font-weight="bold" fill="#4c1d95">Spawn Background Worker Task</text>
  <text x="1005" y="574" text-anchor="middle" font-size="10" fill="#6d28d9">(Return immediate response &amp; poll flag)</text>

  <path d="M 1005 588 L 1005 615" fill="none" stroke="#3b82f6" stroke-width="2" marker-end="url(#arr1)"/>

  <rect x="880" y="615" width="250" height="46" rx="8" fill="#ffffff" stroke="#7c3aed" stroke-width="1.5" filter="url(#shadow1)"/>
  <text x="1005" y="634" text-anchor="middle" font-size="11" font-weight="600" fill="#1e293b">Normalize Query &amp; Synonyms</text>
  <text x="1005" y="648" text-anchor="middle" font-size="10" fill="#64748b">(Expand abbreviations + ESpell check)</text>

  <path d="M 1005 661 L 1005 690" fill="none" stroke="#3b82f6" stroke-width="2" marker-end="url(#arr1)"/>

  <polygon points="1005,690 1090,720 1005,750 920,720" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
  <text x="1005" y="724" text-anchor="middle" font-size="11" font-weight="bold" fill="#92400e">Select Source</text>

  <path d="M 1090 720 L 1320 720 L 1320 660" fill="none" stroke="#2563eb" stroke-width="1.8" marker-end="url(#arr1)"/>
  <text x="1150" y="712" font-size="10" font-weight="bold" fill="#1e40af">[Unified / PubMed / OpenAlex]</text>

  <rect x="1270" y="590" width="270" height="70" rx="10" fill="#ffffff" stroke="#e11d48" stroke-width="1.8" filter="url(#shadow1)"/>
  <text x="1405" y="615" text-anchor="middle" font-size="12" font-weight="bold" fill="#9f1239">NCBI Entrez / OpenAlex</text>
  <text x="1405" y="632" text-anchor="middle" font-size="10" fill="#64748b">Concurrent API Queries +</text>
  <text x="1405" y="648" text-anchor="middle" font-size="10" fill="#64748b">Affiliation Extraction &amp; Fallback</text>

  <path d="M 1405 660 L 1405 780 L 1150 780" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arr1)"/>

  <rect x="880" y="760" width="270" height="46" rx="8" fill="#ffffff" stroke="#7c3aed" stroke-width="1.5" filter="url(#shadow1)"/>
  <text x="1015" y="779" text-anchor="middle" font-size="11" font-weight="600" fill="#1e293b">Deduplicate Paper Candidates</text>
  <text x="1015" y="793" text-anchor="middle" font-size="10" fill="#64748b">(Match on PMID, DOI &amp; Normalized Title)</text>

  <path d="M 1015 806 L 1015 830" fill="none" stroke="#3b82f6" stroke-width="2" marker-end="url(#arr1)"/>

  <polygon points="1015,830 1090,855 1015,880 940,855" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
  <text x="1015" y="859" text-anchor="middle" font-size="11" font-weight="bold" fill="#92400e">Results &gt; 0?</text>

  <path d="M 940 855 L 750 855 L 750 880" fill="none" stroke="#ef4444" stroke-width="1.8" marker-end="url(#arr1)"/>
  <text x="830" y="848" font-size="10" font-weight="bold" fill="#dc2626">[No: Zero Results]</text>

  <rect x="650" y="880" width="200" height="44" rx="8" fill="#fff1f2" stroke="#e11d48" stroke-width="1.5" filter="url(#shadow1)"/>
  <text x="750" y="900" text-anchor="middle" font-size="11" font-weight="bold" fill="#9f1239">Show 'No Results Found'</text>
  <text x="750" y="914" text-anchor="middle" font-size="10" fill="#be123c">Provide Query Tips</text>

  <path d="M 1015 880 L 1015 910" fill="none" stroke="#3b82f6" stroke-width="2" marker-end="url(#arr1)"/>
  <text x="1025" y="895" font-size="10" font-weight="bold" fill="#16a34a">[Yes]</text>

  <polygon points="1015,910 1090,935 1015,960 940,935" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
  <text x="1015" y="939" text-anchor="middle" font-size="10" font-weight="bold" fill="#92400e">Re-Rank Mode?</text>

  <path d="M 1090 935 L 1290 935" fill="none" stroke="#a855f7" stroke-width="1.8" marker-end="url(#arr1)"/>
  <text x="1130" y="928" font-size="10" font-weight="bold" fill="#7e22ce">[Relevance]</text>

  <rect x="1290" y="915" width="240" height="44" rx="8" fill="#faf5ff" stroke="#a855f7" stroke-width="1.5" filter="url(#shadow1)"/>
  <text x="1410" y="933" text-anchor="middle" font-size="11" font-weight="bold" fill="#581c87">MedCPT Semantic Bi-Encoder</text>
  <text x="1410" y="947" text-anchor="middle" font-size="10" fill="#7e22ce">Cross-attention Cosine Scores</text>

  <path d="M 1410 959 L 1410 990 L 1150 990" fill="none" stroke="#a855f7" stroke-width="1.5" marker-end="url(#arr1)"/>

  <path d="M 1015 960 L 1015 990" fill="none" stroke="#64748b" stroke-width="1.8" marker-end="url(#arr1)"/>
  <text x="1025" y="975" font-size="10" font-weight="bold" fill="#64748b">[Recency]</text>

  <rect x="880" y="990" width="270" height="48" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="1.8" filter="url(#shadow1)"/>
  <text x="1015" y="1010" text-anchor="middle" font-size="11" font-weight="bold" fill="#14532d">Write Clean CSV &amp; Update State</text>
  <text x="1015" y="1024" text-anchor="middle" font-size="10" fill="#15803d">(Save to data/{query}.csv; Progress 100%)</text>

  <path d="M 880 1014 L 690 1014" fill="none" stroke="#16a34a" stroke-width="2" marker-end="url(#arr1)"/>

  <rect x="460" y="990" width="230" height="48" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="1.8" filter="url(#shadow1)"/>
  <text x="575" y="1010" text-anchor="middle" font-size="11" font-weight="bold" fill="#14532d">Fetch GET /search/results</text>
  <text x="575" y="1024" text-anchor="middle" font-size="10" fill="#15803d">&amp; Render Paginated Cards</text>

  <path d="M 460 1014 L 325 1014" fill="none" stroke="#3b82f6" stroke-width="2" marker-end="url(#arr1)"/>

  <rect x="105" y="990" width="220" height="50" rx="10" fill="#ffffff" stroke="#2563eb" stroke-width="1.8" filter="url(#shadow1)"/>
  <text x="215" y="1010" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e293b">Browse Ranked Papers</text>
  <text x="215" y="1024" text-anchor="middle" font-size="10" fill="#64748b">Download PDF or View Online</text>

  <path d="M 215 1040 L 215 1070" fill="none" stroke="#3b82f6" stroke-width="2" marker-end="url(#arr1)"/>

  <circle cx="215" cy="1090" r="14" fill="#ffffff" stroke="#0f172a" stroke-width="3"/>
  <circle cx="215" cy="1090" r="8" fill="#0f172a"/>
  <text x="215" y="1120" text-anchor="middle" font-size="12" font-weight="bold" fill="#334155">End: Exploration Complete</text>
</svg>'''

def create_activity_2_upload_analysis_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1150" width="1600" height="1150" style="background:#ffffff; font-family:'Segoe UI', Inter, -apple-system, sans-serif;">
  <defs>
    <filter id="shadow2" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="1" dy="2" stdDeviation="2.5" flood-opacity="0.1"/>
    </filter>
    <marker id="arr2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#0284c7"/>
    </marker>
    <linearGradient id="headerGrad2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
  </defs>

  <rect x="30" y="20" width="1540" height="70" rx="12" fill="url(#headerGrad2)" filter="url(#shadow2)"/>
  <text x="50" y="50" fill="#38bdf8" font-size="12" font-weight="700" letter-spacing="2">UML 2.5 ACTIVITY DIAGRAM</text>
  <text x="50" y="74" fill="#ffffff" font-size="20" font-weight="bold">Activity Diagram 2: Dataset Upload &amp; Multi-Perspective Analysis Workflow</text>
  <text x="1350" y="60" fill="#94a3b8" font-size="13">Verified: files.py &amp; analysis.py</text>

  <!-- Swimlane Headers -->
  <rect x="30" y="105" width="370" height="990" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="30" y="105" width="370" height="40" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
  <text x="215" y="130" text-anchor="middle" font-size="14" font-weight="bold" fill="#1e40af">Researcher / Student (User)</text>

  <rect x="400" y="105" width="410" height="990" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="400" y="105" width="410" height="40" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5"/>
  <text x="605" y="130" text-anchor="middle" font-size="14" font-weight="bold" fill="#166534">Frontend UI (AnalyticsPage.tsx &amp; Views)</text>

  <rect x="810" y="105" width="370" height="990" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="810" y="105" width="370" height="40" fill="#fefce8" stroke="#fde047" stroke-width="1.5"/>
  <text x="995" y="130" text-anchor="middle" font-size="14" font-weight="bold" fill="#854d0e">File Ingestion &amp; Storage (csv_loader.py)</text>

  <rect x="1180" y="105" width="390" height="990" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="1180" y="105" width="390" height="40" fill="#faf5ff" stroke="#d8b4fe" stroke-width="1.5"/>
  <text x="1375" y="130" text-anchor="middle" font-size="14" font-weight="bold" fill="#6b21a8">Analysis Engine (NetworkX &amp; Country)</text>

  <!-- Nodes -->
  <circle cx="215" cy="180" r="14" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <path d="M 215 194 L 215 220" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arr2)"/>

  <rect x="105" y="220" width="220" height="46" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="1.8" filter="url(#shadow2)"/>
  <text x="215" y="240" text-anchor="middle" font-size="12" font-weight="bold" fill="#1e293b">Open Analytics Module</text>
  <text x="215" y="254" text-anchor="middle" font-size="10" fill="#64748b">Navigate to '/analytics'</text>

  <path d="M 325 243 L 490 243" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arr2)"/>

  <rect x="490" y="220" width="230" height="46" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="1.6" filter="url(#shadow2)"/>
  <text x="605" y="239" text-anchor="middle" font-size="11" font-weight="bold" fill="#14532d">Fetch Available CSV Files</text>
  <text x="605" y="253" text-anchor="middle" font-size="10" fill="#15803d">(GET /api/v1/analysis/files)</text>

  <path d="M 605 266 L 605 300 L 325 300" fill="none" stroke="#0284c7" stroke-width="1.8" marker-end="url(#arr2)"/>

  <polygon points="215,280 295,305 215,330 135,305" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
  <text x="215" y="309" text-anchor="middle" font-size="11" font-weight="bold" fill="#92400e">Select or Upload?</text>

  <path d="M 295 305 L 360 305 L 360 370 L 295 370" fill="none" stroke="#d97706" stroke-width="1.8" marker-end="url(#arr2)"/>
  <text x="365" y="335" font-size="10" font-weight="bold" fill="#b45309">[Upload New]</text>

  <rect x="105" y="350" width="190" height="44" rx="8" fill="#ffffff" stroke="#d97706" stroke-width="1.5" filter="url(#shadow2)"/>
  <text x="200" y="369" text-anchor="middle" font-size="11" font-weight="600" fill="#1e293b">Upload Custom CSV</text>
  <text x="200" y="383" text-anchor="middle" font-size="10" fill="#64748b">(Choose local dataset)</text>

  <path d="M 295 370 L 890 370" fill="none" stroke="#d97706" stroke-width="1.8" marker-end="url(#arr2)"/>

  <rect x="890" y="350" width="220" height="44" rx="8" fill="#ffffff" stroke="#ca8a04" stroke-width="1.5" filter="url(#shadow2)"/>
  <text x="1000" y="369" text-anchor="middle" font-size="11" font-weight="bold" fill="#854d0e">Detect Encoding &amp; Save</text>
  <text x="1000" y="383" text-anchor="middle" font-size="10" fill="#a16207">(UTF-8-BOM, Latin-1 to data/)</text>

  <path d="M 215 330 L 215 440" fill="none" stroke="#0284c7" stroke-width="1.8" marker-end="url(#arr2)"/>
  <text x="220" y="345" font-size="10" font-weight="bold" fill="#64748b">[Select Existing]</text>
  <path d="M 1000 394 L 1000 460 L 325 460" fill="none" stroke="#ca8a04" stroke-width="1.5" marker-end="url(#arr2)"/>

  <rect x="105" y="440" width="220" height="46" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="1.8" filter="url(#shadow2)"/>
  <text x="215" y="460" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e293b">Select Dataset &amp; Config</text>
  <text x="215" y="474" text-anchor="middle" font-size="10" fill="#64748b">(Set Top-N keywords &amp; Min Freq)</text>

  <path d="M 325 463 L 490 463" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arr2)"/>

  <rect x="490" y="440" width="230" height="46" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="1.6" filter="url(#shadow2)"/>
  <text x="605" y="459" text-anchor="middle" font-size="11" font-weight="bold" fill="#14532d">Dispatch POST /analysis/generate</text>
  <text x="605" y="473" text-anchor="middle" font-size="10" fill="#15803d">&amp; Show ResearchRoverLoader</text>

  <path d="M 720 463 L 1240 463" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arr2)"/>

  <rect x="1240" y="430" width="270" height="66" rx="10" fill="#ffffff" stroke="#7c3aed" stroke-width="1.8" filter="url(#shadow2)"/>
  <text x="1375" y="452" text-anchor="middle" font-size="12" font-weight="bold" fill="#4c1d95">5-Phase Pipeline &amp; Country Engine</text>
  <text x="1375" y="468" text-anchor="middle" font-size="10" fill="#6d28d9">1. Normalize Metadata 2. Frequency</text>
  <text x="1375" y="484" text-anchor="middle" font-size="10" fill="#6d28d9">3. Centrality Matrix 4. Country Graph</text>

  <path d="M 1375 496 L 1375 540" fill="none" stroke="#7c3aed" stroke-width="2" marker-end="url(#arr2)"/>

  <rect x="1240" y="540" width="270" height="46" rx="8" fill="#faf5ff" stroke="#a855f7" stroke-width="1.5" filter="url(#shadow2)"/>
  <text x="1375" y="559" text-anchor="middle" font-size="11" font-weight="bold" fill="#581c87">Persist JSON Summary &amp; CSVs</text>
  <text x="1375" y="573" text-anchor="middle" font-size="10" fill="#7e22ce">Cache results in data/ folder</text>

  <path d="M 1240 563 L 720 563" fill="none" stroke="#16a34a" stroke-width="2" marker-end="url(#arr2)"/>

  <rect x="490" y="540" width="230" height="46" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="1.8" filter="url(#shadow2)"/>
  <text x="605" y="560" text-anchor="middle" font-size="11" font-weight="bold" fill="#14532d">Receive Analysis Payloads</text>
  <text x="605" y="574" text-anchor="middle" font-size="10" fill="#15803d">Activate Interactive Tabs</text>

  <path d="M 605 586 L 605 630 L 325 630" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arr2)"/>

  <polygon points="215,605 295,630 215,655 135,630" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
  <text x="215" y="634" text-anchor="middle" font-size="11" font-weight="bold" fill="#92400e">Select Tab View</text>

  <path d="M 295 630 L 490 630" fill="none" stroke="#2563eb" stroke-width="1.8" marker-end="url(#arr2)"/>
  <text x="350" y="622" font-size="10" font-weight="bold" fill="#1e40af">[Keyword Tab]</text>

  <rect x="490" y="610" width="240" height="70" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="1.5" filter="url(#shadow2)"/>
  <text x="610" y="630" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e3a8a">Keyword Analytics View</text>
  <text x="610" y="646" text-anchor="middle" font-size="10" fill="#64748b">• Frequency Bars &amp; Word Cloud</text>
  <text x="610" y="662" text-anchor="middle" font-size="10" fill="#64748b">• Centrality Table &amp; Presence Matrix</text>

  <path d="M 215 655 L 215 730 L 490 730" fill="none" stroke="#059669" stroke-width="1.8" marker-end="url(#arr2)"/>
  <text x="220" y="690" font-size="10" font-weight="bold" fill="#047857">[Country Tab]</text>

  <rect x="490" y="700" width="240" height="70" rx="8" fill="#ffffff" stroke="#059669" stroke-width="1.5" filter="url(#shadow2)"/>
  <text x="610" y="720" text-anchor="middle" font-size="11" font-weight="bold" fill="#065f46">Country Analysis View</text>
  <text x="610" y="736" text-anchor="middle" font-size="10" fill="#64748b">• TopoJSON World Map &amp; Ranking</text>
  <text x="610" y="752" text-anchor="middle" font-size="10" fill="#64748b">• 2D/3D Force Collaboration Networks</text>

  <path d="M 730 645 L 780 645 L 780 820 L 325 820" fill="none" stroke="#2563eb" stroke-width="1.5"/>
  <path d="M 730 735 L 780 735 L 780 820" fill="none" stroke="#059669" stroke-width="1.5"/>

  <rect x="105" y="800" width="220" height="50" rx="10" fill="#ffffff" stroke="#0284c7" stroke-width="1.8" filter="url(#shadow2)"/>
  <text x="215" y="820" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e293b">Interact with Visuals</text>
  <text x="215" y="834" text-anchor="middle" font-size="10" fill="#64748b">(Filter, Search, Zoom, Rotate)</text>

  <path d="M 215 850 L 215 880" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arr2)"/>

  <rect x="105" y="880" width="220" height="46" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.6" filter="url(#shadow2)"/>
  <text x="215" y="900" text-anchor="middle" font-size="11" font-weight="bold" fill="#14532d">Export Selected Artifacts</text>
  <text x="215" y="914" text-anchor="middle" font-size="10" fill="#15803d">(Download CSV, JSON or PNG)</text>

  <path d="M 215 926 L 215 960" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arr2)"/>

  <circle cx="215" cy="980" r="14" fill="#ffffff" stroke="#0f172a" stroke-width="3"/>
  <circle cx="215" cy="980" r="8" fill="#0f172a"/>
  <text x="215" y="1010" text-anchor="middle" font-size="12" font-weight="bold" fill="#334155">End: Analysis Completed</text>
</svg>'''

def create_activity_3_keyword_analytics_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1150" width="1600" height="1150" style="background:#ffffff; font-family:'Segoe UI', Inter, -apple-system, sans-serif;">
  <defs>
    <filter id="shadow3" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="1" dy="2" stdDeviation="2.5" flood-opacity="0.1"/>
    </filter>
    <marker id="arr3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#0284c7"/>
    </marker>
    <linearGradient id="headerGrad3" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
  </defs>

  <rect x="30" y="20" width="1540" height="70" rx="12" fill="url(#headerGrad3)" filter="url(#shadow3)"/>
  <text x="50" y="50" fill="#38bdf8" font-size="12" font-weight="700" letter-spacing="2">UML 2.5 ACTIVITY DIAGRAM</text>
  <text x="50" y="74" fill="#ffffff" font-size="20" font-weight="bold">Activity Diagram 3: Keyword Bibliometrics &amp; NetworkX Analytics Algorithm</text>
  <text x="1350" y="60" fill="#94a3b8" font-size="13">Verified: analysis_service.py</text>

  <!-- 5 Horizontal Processing Phases -->
  <rect x="30" y="110" width="300" height="980" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="30" y="110" width="300" height="40" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
  <text x="180" y="135" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">1. INGESTION &amp; EXTRACTION</text>

  <rect x="330" y="110" width="330" height="980" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="330" y="110" width="330" height="40" fill="#fefce8" stroke="#fde047" stroke-width="1.5"/>
  <text x="495" y="135" text-anchor="middle" font-size="13" font-weight="bold" fill="#854d0e">2. PARSING &amp; ALIAS NORMALIZATION</text>

  <rect x="660" y="110" width="340" height="980" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="660" y="110" width="340" height="40" fill="#faf5ff" stroke="#d8b4fe" stroke-width="1.5"/>
  <text x="830" y="135" text-anchor="middle" font-size="13" font-weight="bold" fill="#6b21a8">3. NETWORKX &amp; CO-OCCURRENCE</text>

  <rect x="1000" y="110" width="270" height="980" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="1000" y="110" width="270" height="40" fill="#fff7ed" stroke="#fed7aa" stroke-width="1.5"/>
  <text x="1135" y="135" text-anchor="middle" font-size="13" font-weight="bold" fill="#9a3412">4. ARTIFACT PERSISTENCE</text>

  <rect x="1270" y="110" width="300" height="980" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="1270" y="110" width="300" height="40" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5"/>
  <text x="1420" y="135" text-anchor="middle" font-size="13" font-weight="bold" fill="#166534">5. INTERACTIVE DASHBOARD</text>

  <!-- Start Node -->
  <circle cx="180" cy="180" r="14" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <path d="M 180 194 L 180 230" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arr3)"/>

  <rect x="60" y="230" width="240" height="56" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="1.6" filter="url(#shadow3)"/>
  <text x="180" y="252" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e293b">Load CSV via Centralized Loader</text>
  <text x="180" y="268" text-anchor="middle" font-size="10" fill="#64748b">(read_csv_to_dataframe)</text>

  <path d="M 180 286 L 180 320" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arr3)"/>

  <rect x="60" y="320" width="240" height="56" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="1.6" filter="url(#shadow3)"/>
  <text x="180" y="342" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e293b">Normalize Schema Headers</text>
  <text x="180" y="358" text-anchor="middle" font-size="10" fill="#64748b">Title, Keywords, DOI, Authors</text>

  <path d="M 180 376 L 180 410" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arr3)"/>

  <rect x="60" y="410" width="240" height="56" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="1.6" filter="url(#shadow3)"/>
  <text x="180" y="432" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e293b">Iterate Paper Records</text>
  <text x="180" y="448" text-anchor="middle" font-size="10" fill="#64748b">Extract Raw 'Keywords' Field</text>

  <path d="M 300 438 L 360 438" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arr3)"/>

  <rect x="360" y="410" width="270" height="56" rx="8" fill="#ffffff" stroke="#ca8a04" stroke-width="1.6" filter="url(#shadow3)"/>
  <text x="495" y="432" text-anchor="middle" font-size="11" font-weight="bold" fill="#854d0e">Detect Format &amp; Parse String</text>
  <text x="495" y="448" text-anchor="middle" font-size="10" fill="#a16207">ast.literal_eval() or ; / , Split</text>

  <path d="M 495 466 L 495 500" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arr3)"/>

  <rect x="360" y="500" width="270" height="56" rx="8" fill="#ffffff" stroke="#ca8a04" stroke-width="1.6" filter="url(#shadow3)"/>
  <text x="495" y="522" text-anchor="middle" font-size="11" font-weight="bold" fill="#854d0e">Strip Parenthetical Expressions</text>
  <text x="495" y="538" text-anchor="middle" font-size="10" fill="#a16207">re.sub(r'\(.*?\)', '', word)</text>

  <path d="M 495 556 L 495 590" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arr3)"/>

  <rect x="360" y="590" width="270" height="70" rx="8" fill="#ffffff" stroke="#ca8a04" stroke-width="1.8" filter="url(#shadow3)"/>
  <text x="495" y="612" text-anchor="middle" font-size="11" font-weight="bold" fill="#854d0e">Domain Alias &amp; Synonym Map</text>
  <text x="495" y="628" text-anchor="middle" font-size="10" fill="#a16207">• iot -&gt; internet of things • ml -&gt; machine learning</text>
  <text x="495" y="644" text-anchor="middle" font-size="10" fill="#a16207">• block chain -&gt; blockchain • dl -&gt; deep learning</text>

  <path d="M 495 660 L 495 690" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arr3)"/>

  <rect x="360" y="690" width="270" height="56" rx="8" fill="#ffffff" stroke="#ca8a04" stroke-width="1.6" filter="url(#shadow3)"/>
  <text x="495" y="712" text-anchor="middle" font-size="11" font-weight="bold" fill="#854d0e">Deduplicate within Paper</text>
  <text x="495" y="728" text-anchor="middle" font-size="10" fill="#a16207">Prevent self-co-occurrence bias</text>

  <path d="M 630 718 L 690 718" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arr3)"/>

  <rect x="690" y="690" width="280" height="56" rx="8" fill="#ffffff" stroke="#7c3aed" stroke-width="1.6" filter="url(#shadow3)"/>
  <text x="830" y="712" text-anchor="middle" font-size="11" font-weight="bold" fill="#4c1d95">Count Frequencies &amp; Percentages</text>
  <text x="830" y="728" text-anchor="middle" font-size="10" fill="#6d28d9">Filter Top-N (100) &amp; Min Freq (1)</text>

  <path d="M 830 746 L 830 780" fill="none" stroke="#7c3aed" stroke-width="2" marker-end="url(#arr3)"/>

  <rect x="690" y="780" width="280" height="56" rx="8" fill="#ffffff" stroke="#7c3aed" stroke-width="1.6" filter="url(#shadow3)"/>
  <text x="830" y="802" text-anchor="middle" font-size="11" font-weight="bold" fill="#4c1d95">Pairwise Combinations for Edges</text>
  <text x="830" y="818" text-anchor="middle" font-size="10" fill="#6d28d9">itertools.combinations(keywords, 2)</text>

  <path d="M 830 836 L 830 870" fill="none" stroke="#7c3aed" stroke-width="2" marker-end="url(#arr3)"/>

  <rect x="690" y="870" width="280" height="85" rx="10" fill="#ffffff" stroke="#7c3aed" stroke-width="1.8" filter="url(#shadow3)"/>
  <text x="830" y="892" text-anchor="middle" font-size="11" font-weight="bold" fill="#4c1d95">NetworkX Centrality Measures</text>
  <text x="830" y="908" text-anchor="middle" font-size="10" fill="#6d28d9">• Degree: nx.degree_centrality</text>
  <text x="830" y="922" text-anchor="middle" font-size="10" fill="#6d28d9">• Closeness: nx.closeness_centrality</text>
  <text x="830" y="936" text-anchor="middle" font-size="10" fill="#6d28d9">• Betweenness, Eigenvector, Clustering</text>

  <path d="M 970 912 L 1030 912" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arr3)"/>

  <rect x="1030" y="880" width="210" height="66" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="1.6" filter="url(#shadow3)"/>
  <text x="1135" y="902" text-anchor="middle" font-size="11" font-weight="bold" fill="#9a3412">Persist Artifacts</text>
  <text x="1135" y="918" text-anchor="middle" font-size="10" fill="#c2410c">• summary.json</text>
  <text x="1135" y="932" text-anchor="middle" font-size="10" fill="#c2410c">• frequency.csv &amp; matrix.csv</text>

  <path d="M 1240 912 L 1300 912" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arr3)"/>

  <rect x="1300" y="860" width="240" height="110" rx="10" fill="#ffffff" stroke="#16a34a" stroke-width="1.8" filter="url(#shadow3)"/>
  <text x="1420" y="882" text-anchor="middle" font-size="12" font-weight="bold" fill="#14532d">Render Keyword Dashboard</text>
  <text x="1420" y="900" text-anchor="middle" font-size="10" fill="#15803d">1. Summary KPI Cards</text>
  <text x="1420" y="914" text-anchor="middle" font-size="10" fill="#15803d">2. Frequency Progress Bars</text>
  <text x="1420" y="928" text-anchor="middle" font-size="10" fill="#15803d">3. Interactive SVG Word Cloud</text>
  <text x="1420" y="942" text-anchor="middle" font-size="10" fill="#15803d">4. Co-occurrence Network Graph</text>
  <text x="1420" y="956" text-anchor="middle" font-size="10" fill="#15803d">5. Centrality Table &amp; Presence Matrix</text>

  <path d="M 1420 970 L 1420 1010" fill="none" stroke="#16a34a" stroke-width="2" marker-end="url(#arr3)"/>

  <circle cx="1420" cy="1030" r="14" fill="#ffffff" stroke="#0f172a" stroke-width="3"/>
  <circle cx="1420" cy="1030" r="8" fill="#0f172a"/>
  <text x="1420" y="1060" text-anchor="middle" font-size="12" font-weight="bold" fill="#334155">End: Visual Analytics Ready</text>
</svg>'''

def create_activity_4_country_analysis_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1150" width="1600" height="1150" style="background:#ffffff; font-family:'Segoe UI', Inter, -apple-system, sans-serif;">
  <defs>
    <filter id="shadow4" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="1" dy="2" stdDeviation="2.5" flood-opacity="0.1"/>
    </filter>
    <marker id="arr4" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#059669"/>
    </marker>
    <linearGradient id="headerGrad4" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
  </defs>

  <rect x="30" y="20" width="1540" height="70" rx="12" fill="url(#headerGrad4)" filter="url(#shadow4)"/>
  <text x="50" y="50" fill="#34d399" font-size="12" font-weight="700" letter-spacing="2">UML 2.5 ACTIVITY DIAGRAM</text>
  <text x="50" y="74" fill="#ffffff" font-size="20" font-weight="bold">Activity Diagram 4: Bibliometric Country Analysis &amp; Co-Authorship Network</text>
  <text x="1350" y="60" fill="#94a3b8" font-size="13">Verified: country_service.py</text>

  <!-- 4 Swimlanes -->
  <rect x="30" y="105" width="370" height="990" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="30" y="105" width="370" height="40" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
  <text x="215" y="130" text-anchor="middle" font-size="14" font-weight="bold" fill="#1e40af">1. INGESTION &amp; CACHE INVALIDATION</text>

  <rect x="400" y="105" width="410" height="990" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="400" y="105" width="410" height="40" fill="#fefce8" stroke="#fde047" stroke-width="1.5"/>
  <text x="605" y="130" text-anchor="middle" font-size="14" font-weight="bold" fill="#854d0e">2. AFFILIATION &amp; CANONICAL EXTRACTION</text>

  <rect x="810" y="105" width="380" height="990" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="810" y="105" width="380" height="40" fill="#faf5ff" stroke="#d8b4fe" stroke-width="1.5"/>
  <text x="1000" y="130" text-anchor="middle" font-size="14" font-weight="bold" fill="#6b21a8">3. CO-AUTHORSHIP COLLABORATION GRAPH</text>

  <rect x="1190" y="105" width="380" height="990" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="1190" y="105" width="380" height="40" fill="#ecfdf5" stroke="#a7f3d0" stroke-width="1.5"/>
  <text x="1380" y="130" text-anchor="middle" font-size="14" font-weight="bold" fill="#065f46">4. DASHBOARD &amp; 2D/3D NETWORKS</text>

  <!-- Start Node -->
  <circle cx="215" cy="180" r="14" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <path d="M 215 194 L 215 230" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#arr4)"/>

  <rect x="105" y="230" width="220" height="50" rx="8" fill="#ffffff" stroke="#059669" stroke-width="1.6" filter="url(#shadow4)"/>
  <text x="215" y="250" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e293b">Receive CSV Path</text>
  <text x="215" y="266" text-anchor="middle" font-size="10" fill="#64748b">Check _CACHE (abs_path, mtime, size)</text>

  <path d="M 215 280 L 215 315" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#arr4)"/>

  <polygon points="215,315 295,340 215,365 135,340" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
  <text x="215" y="344" text-anchor="middle" font-size="11" font-weight="bold" fill="#92400e">Is Cached?</text>

  <path d="M 295 340 L 1380 340 L 1380 430" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#arr4)"/>
  <text x="350" y="330" font-size="10" font-weight="bold" fill="#047857">[Yes: Return Cache Instant]</text>

  <path d="M 215 365 L 215 410" fill="none" stroke="#d97706" stroke-width="2" marker-end="url(#arr4)"/>
  <text x="220" y="385" font-size="10" font-weight="bold" fill="#64748b">[No]</text>

  <rect x="105" y="410" width="220" height="56" rx="8" fill="#ffffff" stroke="#059669" stroke-width="1.6" filter="url(#shadow4)"/>
  <text x="215" y="430" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e293b">Read CSV Records</text>
  <text x="215" y="446" text-anchor="middle" font-size="10" fill="#64748b">Init Counters &amp; Unassigned List</text>

  <path d="M 325 438 L 460 438" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#arr4)"/>

  <rect x="460" y="410" width="290" height="56" rx="8" fill="#ffffff" stroke="#ca8a04" stroke-width="1.6" filter="url(#shadow4)"/>
  <text x="605" y="430" text-anchor="middle" font-size="11" font-weight="bold" fill="#854d0e">Inspect Explicit Affiliation Keys</text>
  <text x="605" y="446" text-anchor="middle" font-size="10" fill="#a16207">Affiliations, affiliation, Address</text>

  <path d="M 605 466 L 605 500" fill="none" stroke="#ca8a04" stroke-width="2" marker-end="url(#arr4)"/>

  <polygon points="605,500 685,525 605,550 525,525" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
  <text x="605" y="529" text-anchor="middle" font-size="10" font-weight="bold" fill="#92400e">Affiliation Found?</text>

  <path d="M 685 525 L 750 525 L 750 600 L 690 600" fill="none" stroke="#16a34a" stroke-width="1.6" marker-end="url(#arr4)"/>
  <text x="700" y="515" font-size="10" font-weight="bold" fill="#15803d">[Yes]</text>

  <path d="M 525 525 L 450 525 L 450 600 L 520 600" fill="none" stroke="#dc2626" stroke-width="1.6" marker-end="url(#arr4)"/>
  <text x="440" y="515" font-size="10" font-weight="bold" fill="#b91c1c">[No: Author Fallback]</text>

  <rect x="460" y="580" width="290" height="60" rx="8" fill="#ffffff" stroke="#ca8a04" stroke-width="1.8" filter="url(#shadow4)"/>
  <text x="605" y="602" text-anchor="middle" font-size="11" font-weight="bold" fill="#854d0e">Regex &amp; ISO-3166-1 Canonical Map</text>
  <text x="605" y="618" text-anchor="middle" font-size="10" fill="#a16207">Deduplicate Countries per Paper</text>

  <path d="M 605 640 L 605 680" fill="none" stroke="#ca8a04" stroke-width="2" marker-end="url(#arr4)"/>

  <polygon points="605,680 685,705 605,730 525,705" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
  <text x="605" y="709" text-anchor="middle" font-size="10" font-weight="bold" fill="#92400e">Country Detected?</text>

  <path d="M 525 705 L 440 705 L 440 770 L 460 770" fill="none" stroke="#dc2626" stroke-width="1.8" marker-end="url(#arr4)"/>
  <text x="430" y="690" font-size="10" font-weight="bold" fill="#dc2626">[No Country]</text>

  <rect x="460" y="750" width="290" height="60" rx="8" fill="#fff7ed" stroke="#f97316" stroke-width="1.6" filter="url(#shadow4)"/>
  <text x="605" y="772" text-anchor="middle" font-size="11" font-weight="bold" fill="#c2410c">Append to unassigned_papers List</text>
  <text x="605" y="788" text-anchor="middle" font-size="10" fill="#ea580c">Preserve PMID, Title (NO Guesswork)</text>

  <path d="M 685 705 L 850 705" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#arr4)"/>
  <text x="730" y="695" font-size="10" font-weight="bold" fill="#047857">[Yes]</text>

  <rect x="850" y="680" width="300" height="56" rx="8" fill="#ffffff" stroke="#7c3aed" stroke-width="1.6" filter="url(#shadow4)"/>
  <text x="1000" y="702" text-anchor="middle" font-size="11" font-weight="bold" fill="#4c1d95">Increment Country Publication Counts</text>
  <text x="1000" y="718" text-anchor="middle" font-size="10" fill="#6d28d9">Track Papers with Country Data</text>

  <path d="M 1000 736 L 1000 770" fill="none" stroke="#7c3aed" stroke-width="2" marker-end="url(#arr4)"/>

  <polygon points="1000,770 1080,795 1000,820 920,795" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
  <text x="1000" y="799" text-anchor="middle" font-size="10" font-weight="bold" fill="#92400e">&gt;= 2 Countries?</text>

  <path d="M 1080 795 L 1140 795 L 1140 860 L 1080 860" fill="none" stroke="#059669" stroke-width="1.8" marker-end="url(#arr4)"/>
  <text x="1100" y="785" font-size="10" font-weight="bold" fill="#047857">[International]</text>

  <rect x="850" y="840" width="300" height="60" rx="8" fill="#ffffff" stroke="#7c3aed" stroke-width="1.8" filter="url(#shadow4)"/>
  <text x="1000" y="862" text-anchor="middle" font-size="11" font-weight="bold" fill="#4c1d95">Build Co-Authorship Partnerships</text>
  <text x="1000" y="878" text-anchor="middle" font-size="10" fill="#6d28d9">combinations(unique_countries, 2)</text>

  <path d="M 1000 900 L 1000 930" fill="none" stroke="#7c3aed" stroke-width="2" marker-end="url(#arr4)"/>

  <rect x="850" y="930" width="300" height="60" rx="8" fill="#faf5ff" stroke="#a855f7" stroke-width="1.6" filter="url(#shadow4)"/>
  <text x="1000" y="952" text-anchor="middle" font-size="11" font-weight="bold" fill="#581c87">Calculate Coverage % &amp; Graph JSON</text>
  <text x="1000" y="968" text-anchor="middle" font-size="10" fill="#7e22ce">Nodes: {id, paperCount}; Links: {weight}</text>

  <path d="M 1150 960 L 1230 960" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#arr4)"/>

  <rect x="1230" y="430" width="300" height="560" rx="12" fill="#ffffff" stroke="#059669" stroke-width="2" filter="url(#shadow4)"/>
  <text x="1380" y="460" text-anchor="middle" font-size="13" font-weight="bold" fill="#065f46">Render Country Analysis Views</text>

  <text x="1260" y="495" font-size="11" font-weight="bold" fill="#1e293b">1. Coverage KPI Cards</text>
  <text x="1260" y="515" font-size="10" fill="#64748b">Total Papers, Coverage %, International</text>

  <text x="1260" y="550" font-size="11" font-weight="bold" fill="#1e293b">2. Coverage Split Bar</text>
  <text x="1260" y="570" font-size="10" fill="#64748b">Papers With vs Without Country</text>

  <text x="1260" y="605" font-size="11" font-weight="bold" fill="#c2410c">3. Unassigned Papers Modal</text>
  <text x="1260" y="625" font-size="10" fill="#ea580c">Interactive inspection of unassigned papers</text>

  <text x="1260" y="660" font-size="11" font-weight="bold" fill="#1e293b">4. TopoJSON World Map</text>
  <text x="1260" y="680" font-size="10" fill="#64748b">Choropleth density shading &amp; tooltips</text>

  <text x="1260" y="715" font-size="11" font-weight="bold" fill="#1e293b">5. Country Ranking Table</text>
  <text x="1260" y="735" font-size="10" fill="#64748b">Searchable, paper volumes &amp; percentages</text>

  <text x="1260" y="770" font-size="11" font-weight="bold" fill="#1e293b">6. 2D D3 Force Network</text>
  <text x="1260" y="790" font-size="10" fill="#64748b">Strength filters (All/Med/Strong), zoom/pan</text>

  <text x="1260" y="825" font-size="11" font-weight="bold" fill="#1e293b">7. 3D Three.js Force Network</text>
  <text x="1260" y="845" font-size="10" fill="#64748b">Rotating orbit space, particle pulses</text>

  <text x="1260" y="880" font-size="11" font-weight="bold" fill="#1e293b">8. CSV &amp; Image Export</text>
  <text x="1260" y="900" font-size="10" fill="#64748b">Download rankings &amp; collaborations CSV</text>

  <path d="M 1380 990 L 1380 1020" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#arr4)"/>

  <circle cx="1380" cy="1040" r="14" fill="#ffffff" stroke="#0f172a" stroke-width="3"/>
  <circle cx="1380" cy="1040" r="8" fill="#0f172a"/>
  <text x="1380" y="1070" text-anchor="middle" font-size="12" font-weight="bold" fill="#334155">End: Country Analytics Complete</text>
</svg>'''

def create_activity_5_ai_assistant_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1150" width="1600" height="1150" style="background:#ffffff; font-family:'Segoe UI', Inter, -apple-system, sans-serif;">
  <defs>
    <filter id="shadow5" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="1" dy="2" stdDeviation="2.5" flood-opacity="0.1"/>
    </filter>
    <marker id="arr5" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#7c3aed"/>
    </marker>
    <linearGradient id="headerGrad5" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
  </defs>

  <rect x="30" y="20" width="1540" height="70" rx="12" fill="url(#headerGrad5)" filter="url(#shadow5)"/>
  <text x="50" y="50" fill="#a78bfa" font-size="12" font-weight="700" letter-spacing="2">UML 2.5 ACTIVITY DIAGRAM</text>
  <text x="50" y="74" fill="#ffffff" font-size="20" font-weight="bold">Activity Diagram 5: AI Research Assistant (Conversational RAG Workflow)</text>
  <text x="1350" y="60" fill="#94a3b8" font-size="13">Verified: chat_service.py &amp; FAISS</text>

  <!-- 4 Swimlanes -->
  <rect x="30" y="105" width="360" height="990" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="30" y="105" width="360" height="40" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
  <text x="210" y="130" text-anchor="middle" font-size="14" font-weight="bold" fill="#1e40af">Researcher / Student (User)</text>

  <rect x="390" y="105" width="390" height="990" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="390" y="105" width="390" height="40" fill="#f5f3ff" stroke="#c4b5fd" stroke-width="1.5"/>
  <text x="585" y="130" text-anchor="middle" font-size="14" font-weight="bold" fill="#6d28d9">Frontend Chat UI (ChatPage.tsx &amp; Modal)</text>

  <rect x="780" y="105" width="410" height="990" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="780" y="105" width="410" height="40" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5"/>
  <text x="985" y="130" text-anchor="middle" font-size="14" font-weight="bold" fill="#166534">Embedding &amp; Vector Index (FAISS Service)</text>

  <rect x="1190" y="105" width="380" height="990" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <rect x="1190" y="105" width="380" height="40" fill="#fdf2f8" stroke="#fbcfe8" stroke-width="1.5"/>
  <text x="1380" y="130" text-anchor="middle" font-size="14" font-weight="bold" fill="#9d174d">LLM Synthesis Gateway (Gemini API)</text>

  <!-- Start Node -->
  <circle cx="210" cy="180" r="14" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <path d="M 210 194 L 210 230" fill="none" stroke="#7c3aed" stroke-width="2" marker-end="url(#arr5)"/>

  <rect x="100" y="230" width="220" height="46" rx="8" fill="#ffffff" stroke="#7c3aed" stroke-width="1.6" filter="url(#shadow5)"/>
  <text x="210" y="250" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e293b">Open AI Assistant</text>
  <text x="210" y="264" text-anchor="middle" font-size="10" fill="#64748b">Navigate to '/chat' &amp; Pick CSV</text>

  <path d="M 320 253 L 450 253" fill="none" stroke="#7c3aed" stroke-width="2" marker-end="url(#arr5)"/>

  <rect x="450" y="230" width="260" height="46" rx="8" fill="#ffffff" stroke="#8b5cf6" stroke-width="1.6" filter="url(#shadow5)"/>
  <text x="580" y="249" text-anchor="middle" font-size="11" font-weight="bold" fill="#4c1d95">Check Embedding Status</text>
  <text x="580" y="263" text-anchor="middle" font-size="10" fill="#6d28d9">(GET /api/v1/embeddings/{file}/status)</text>

  <path d="M 580 276 L 580 310" fill="none" stroke="#7c3aed" stroke-width="2" marker-end="url(#arr5)"/>

  <polygon points="580,310 660,335 580,360 500,335" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
  <text x="580" y="339" text-anchor="middle" font-size="10" font-weight="bold" fill="#92400e">Index Built?</text>

  <path d="M 660 335 L 850 335" fill="none" stroke="#d97706" stroke-width="1.8" marker-end="url(#arr5)"/>
  <text x="700" y="325" font-size="10" font-weight="bold" fill="#b45309">[No: Create Embeddings]</text>

  <rect x="850" y="310" width="270" height="66" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="1.8" filter="url(#shadow5)"/>
  <text x="985" y="330" text-anchor="middle" font-size="11" font-weight="bold" fill="#14532d">Execute Embedding Pipeline</text>
  <text x="985" y="346" text-anchor="middle" font-size="10" fill="#15803d">• Scrape URLs or use Abstracts</text>
  <text x="985" y="360" text-anchor="middle" font-size="10" fill="#15803d">• all-mpnet-base-v2 (768-dim) -&gt; FAISS</text>

  <path d="M 985 376 L 985 410 L 710 410" fill="none" stroke="#16a34a" stroke-width="1.8" marker-end="url(#arr5)"/>

  <path d="M 580 360 L 580 440 L 320 440" fill="none" stroke="#7c3aed" stroke-width="2" marker-end="url(#arr5)"/>
  <text x="590" y="390" font-size="10" font-weight="bold" fill="#16a34a">[Yes: Active]</text>

  <rect x="100" y="420" width="220" height="50" rx="8" fill="#ffffff" stroke="#7c3aed" stroke-width="1.8" filter="url(#shadow5)"/>
  <text x="210" y="440" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e293b">Enter Research Question</text>
  <text x="210" y="454" text-anchor="middle" font-size="10" fill="#64748b">(e.g., 'Compare deep learning models')</text>

  <path d="M 210 470 L 210 500" fill="none" stroke="#7c3aed" stroke-width="2" marker-end="url(#arr5)"/>

  <rect x="100" y="500" width="220" height="46" rx="8" fill="#ffffff" stroke="#7c3aed" stroke-width="1.6" filter="url(#shadow5)"/>
  <text x="210" y="520" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e293b">Submit Chat Prompt</text>
  <text x="210" y="534" text-anchor="middle" font-size="10" fill="#64748b">(Click Send or Enter)</text>

  <path d="M 320 523 L 450 523" fill="none" stroke="#7c3aed" stroke-width="2" marker-end="url(#arr5)"/>

  <rect x="450" y="500" width="260" height="46" rx="8" fill="#ffffff" stroke="#8b5cf6" stroke-width="1.6" filter="url(#shadow5)"/>
  <text x="580" y="520" text-anchor="middle" font-size="11" font-weight="bold" fill="#4c1d95">Validate &amp; Show Loading</text>
  <text x="580" y="534" text-anchor="middle" font-size="10" fill="#6d28d9">POST /api/v1/chat/ request</text>

  <path d="M 710 523 L 850 523" fill="none" stroke="#7c3aed" stroke-width="2" marker-end="url(#arr5)"/>

  <rect x="850" y="500" width="270" height="56" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="1.6" filter="url(#shadow5)"/>
  <text x="985" y="520" text-anchor="middle" font-size="11" font-weight="bold" fill="#14532d">Decompose Query into Sub-Queries</text>
  <text x="985" y="536" text-anchor="middle" font-size="10" fill="#15803d">Multi-angle semantic expansion</text>

  <path d="M 985 556 L 985 590" fill="none" stroke="#16a34a" stroke-width="2" marker-end="url(#arr5)"/>

  <rect x="850" y="590" width="270" height="60" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="1.8" filter="url(#shadow5)"/>
  <text x="985" y="610" text-anchor="middle" font-size="11" font-weight="bold" fill="#14532d">Search FAISS Index (k=5 each)</text>
  <text x="985" y="626" text-anchor="middle" font-size="10" fill="#15803d">Deduplicate Chunks by ID / Hash</text>

  <path d="M 985 650 L 985 680" fill="none" stroke="#16a34a" stroke-width="2" marker-end="url(#arr5)"/>

  <polygon points="985,680 1065,705 985,730 905,705" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
  <text x="985" y="709" text-anchor="middle" font-size="10" font-weight="bold" fill="#92400e">Chunks Found?</text>

  <path d="M 1065 705 L 1240 705" fill="none" stroke="#16a34a" stroke-width="2" marker-end="url(#arr5)"/>
  <text x="1100" y="695" font-size="10" font-weight="bold" fill="#15803d">[Relevant Context]</text>

  <rect x="1240" y="680" width="280" height="66" rx="8" fill="#ffffff" stroke="#db2777" stroke-width="1.8" filter="url(#shadow5)"/>
  <text x="1380" y="702" text-anchor="middle" font-size="11" font-weight="bold" fill="#831843">Assemble Grounded Prompt</text>
  <text x="1380" y="718" text-anchor="middle" font-size="10" fill="#9d174d">Map paper titles, DOIs, URLs</text>
  <text x="1380" y="732" text-anchor="middle" font-size="10" fill="#9d174d">Call Google Gemini API</text>

  <path d="M 1380 746 L 1380 780" fill="none" stroke="#db2777" stroke-width="2" marker-end="url(#arr5)"/>

  <rect x="1240" y="780" width="280" height="56" rx="8" fill="#fdf2f8" stroke="#db2777" stroke-width="1.6" filter="url(#shadow5)"/>
  <text x="1380" y="802" text-anchor="middle" font-size="11" font-weight="bold" fill="#831843">Stream AI Synthesis &amp; Citations</text>
  <text x="1380" y="818" text-anchor="middle" font-size="10" fill="#9d174d">Attach structured paper source drawer</text>

  <path d="M 1240 808 L 710 808" fill="none" stroke="#7c3aed" stroke-width="2" marker-end="url(#arr5)"/>

  <rect x="450" y="780" width="260" height="56" rx="8" fill="#ffffff" stroke="#8b5cf6" stroke-width="1.8" filter="url(#shadow5)"/>
  <text x="580" y="802" text-anchor="middle" font-size="11" font-weight="bold" fill="#4c1d95">Render Markdown &amp; Source Links</text>
  <text x="580" y="818" text-anchor="middle" font-size="10" fill="#6d28d9">Collapsible verified paper cards</text>

  <path d="M 450 808 L 320 808" fill="none" stroke="#7c3aed" stroke-width="2" marker-end="url(#arr5)"/>

  <rect x="100" y="780" width="220" height="56" rx="8" fill="#ffffff" stroke="#7c3aed" stroke-width="1.8" filter="url(#shadow5)"/>
  <text x="210" y="802" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e293b">Inspect Answer &amp; Citations</text>
  <text x="210" y="818" text-anchor="middle" font-size="10" fill="#64748b">Verify claims via paper links</text>

  <path d="M 210 836 L 210 880" fill="none" stroke="#7c3aed" stroke-width="2" marker-end="url(#arr5)"/>

  <polygon points="210,880 280,905 210,930 140,905" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
  <text x="210" y="909" text-anchor="middle" font-size="10" font-weight="bold" fill="#92400e">Ask Follow-up?</text>

  <path d="M 280 905 L 340 905 L 340 440 L 320 440" fill="none" stroke="#7c3aed" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#arr5)"/>
  <text x="345" y="650" font-size="10" font-weight="bold" fill="#7c3aed">[Yes: Loop]</text>

  <path d="M 210 930 L 210 970" fill="none" stroke="#0f172a" stroke-width="2" marker-end="url(#arr5)"/>
  <text x="215" y="950" font-size="10" font-weight="bold" fill="#64748b">[No]</text>

  <circle cx="210" cy="990" r="14" fill="#ffffff" stroke="#0f172a" stroke-width="3"/>
  <circle cx="210" cy="990" r="8" fill="#0f172a"/>
  <text x="210" y="1020" text-anchor="middle" font-size="12" font-weight="bold" fill="#334155">End: Research Q&amp;A Complete</text>
</svg>'''

def main():
    print("Generating diagrams in:", OUT_DIR)
    
    with open(OUT_DIR / "use_case_diagram.svg", "w", encoding="utf-8") as f:
        f.write(create_use_case_svg())
    print("  -> use_case_diagram.svg")
    
    with open(OUT_DIR / "activity_diagram_1_search.svg", "w", encoding="utf-8") as f:
        f.write(create_activity_1_search_svg())
    print("  -> activity_diagram_1_search.svg")
    
    with open(OUT_DIR / "activity_diagram_2_upload_analysis.svg", "w", encoding="utf-8") as f:
        f.write(create_activity_2_upload_analysis_svg())
    print("  -> activity_diagram_2_upload_analysis.svg")
    
    with open(OUT_DIR / "activity_diagram_3_keyword_analytics.svg", "w", encoding="utf-8") as f:
        f.write(create_activity_3_keyword_analytics_svg())
    print("  -> activity_diagram_3_keyword_analytics.svg")
    
    with open(OUT_DIR / "activity_diagram_4_country_analysis.svg", "w", encoding="utf-8") as f:
        f.write(create_activity_4_country_analysis_svg())
    print("  -> activity_diagram_4_country_analysis.svg")
    
    with open(OUT_DIR / "activity_diagram_5_ai_assistant.svg", "w", encoding="utf-8") as f:
        f.write(create_activity_5_ai_assistant_svg())
    print("  -> activity_diagram_5_ai_assistant.svg")
    
    print("All 6 SVG diagrams generated successfully!")

if __name__ == "__main__":
    main()
