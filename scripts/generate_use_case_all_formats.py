"""
Generate publication-quality, professional UML 2.5 Use Case Diagram deliverables for Research Rover:
  - Research_Rover_Use_Case_Diagram.puml
  - Research_Rover_Use_Case_Diagram.svg
  - Research_Rover_Use_Case_Diagram.png (300 DPI high-resolution)
  - Research_Rover_Use_Case_Diagram.pdf (Vector PDF for M.Tech thesis / report)

Updated specification:
  - Stereotype labels (<<include>>, <<extend>>, <<human actor>>, <<external system>>) completely removed as requested.
  - All relationship lines, arrows, shapes, colors, use cases, actors, and module groupings are 100% preserved.
"""

import os
import shutil
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle

# ==============================================================================
# 1. PLANTUML SOURCE CODE GENERATOR (NO STEREOTYPES)
# ==============================================================================
def generate_plantuml_source():
    return """@startuml Research_Rover_Use_Case_Diagram
' ==============================================================================
' Project: Research Rover - Intelligent Systematic Literature Review Platform
' Diagram: UML 2.5 Use Case Diagram
' Standard: ISO/IEC 19505:2012 / OMG UML 2.5
' Target: M.Tech Project Defense, Thesis Report, and Technical Documentation
' ==============================================================================

skinparam backgroundColor #FFFFFF
skinparam handwritten false
skinparam monochrome false
skinparam shadowing false
skinparam defaultFontName "Segoe UI", Arial, Helvetica, sans-serif
skinparam defaultFontSize 12
skinparam defaultFontColor #1E293B

' Styling for Human Actors
skinparam actor {
    BackgroundColor #EFF6FF
    BorderColor #2563EB
    BorderThickness 1.5
    FontColor #0F172A
    FontSize 13
    FontStyle bold
}

' Styling for System Boundary
skinparam rectangle {
    BackgroundColor #F8FAFC
    BorderColor #64748B
    BorderThickness 2
    FontColor #0F172A
    FontSize 15
    FontStyle bold
}

' Styling for Modules (Packages)
skinparam package {
    BackgroundColor #FFFFFF
    BorderColor #CBD5E1
    BorderThickness 1.2
    FontColor #1E40AF
    FontSize 12
    FontStyle bold
}

' Styling for Use Cases (Ovals)
skinparam usecase {
    BackgroundColor #F1F5F9
    BorderColor #3B82F6
    BorderThickness 1.5
    FontColor #0F172A
    FontSize 12
    FontStyle normal
    ArrowColor #475569
    ArrowThickness 1.2
    ArrowFontColor #475569
    ArrowFontSize 11
}

left to right direction

' ==============================================================================
' PRIMARY ACTOR (LEFT)
' ==============================================================================
actor "Researcher / Student\\n(Primary User)" as User

' ==============================================================================
' EXTERNAL SYSTEMS (RIGHT)
' ==============================================================================
actor "NCBI Entrez API\\n(PubMed Paper Retrieval)" as NCBI
actor "OpenAlex API\\n(Citations & OA Links)" as OpenAlex
actor "Publishers & PMC\\n(Full-Text PDF Hosts)" as Publisher
actor "Google Gemini AI\\n(Generative Synthesis)" as Gemini

' ==============================================================================
' SYSTEM BOUNDARY: RESEARCH ROVER
' ==============================================================================
rectangle "Research Rover" {

    ' --------------------------------------------------------------------------
    ' A. Research Paper Search Module
    ' --------------------------------------------------------------------------
    package "Research Paper Search" {
        usecase "Search Research Papers\\n(Base Search Query)" as UC_Search
        usecase "Unified Search\\n(PubMed + OpenAlex)" as UC_Unified
        usecase "PubMed Search\\n(Biomedical Focus)" as UC_PubMed
        usecase "OpenAlex Search\\n(Multidisciplinary)" as UC_OpenAlex
        usecase "Optimize & Expand Query\\n(MeSH & Acronyms)" as UC_QueryOpt
        usecase "Browse Search Results\\n(Paginated Cards & Citations)" as UC_Browse
        usecase "Apply Search Filters\\n(Year, Sort, Limit)" as UC_Filters
        usecase "Re-Rank Relevance\\n(MedCPT Bi-Encoder)" as UC_Rerank
        usecase "Download Available PDF\\n(SSRF-Protected Stream)" as UC_PDF
        usecase "View Paper on Publisher Site\\n(Direct DOI Link)" as UC_ViewPub
        usecase "Cancel In-Flight Search\\n(Cooperative Abort)" as UC_Cancel
    }

    ' --------------------------------------------------------------------------
    ' B. Dataset Management Module
    ' --------------------------------------------------------------------------
    package "Dataset Management" {
        usecase "Upload Custom Dataset\\n(CSV Validation & Encoding)" as UC_Upload
        usecase "List & Switch Datasets\\n(Auto-Discovered in data/)" as UC_ListDatasets
        usecase "Export Clean Dataset CSV\\n(Unpolluted Metadata)" as UC_ExportCSV
        usecase "Delete Dataset & Embeddings\\n(Storage Clean-up)" as UC_DeleteDataset
    }

    ' --------------------------------------------------------------------------
    ' C. Keyword Bibliometric Analytics Module
    ' --------------------------------------------------------------------------
    package "Keyword Bibliometric Analytics" {
        usecase "Analyse Keywords\\n(5-Phase Pipeline)" as UC_AnalyzeKW
        usecase "Normalize & Alias Map\\n(AST Parsing & Deduplication)" as UC_NormKW
        usecase "View Frequency & Rank\\n(Distribution Bar Charts)" as UC_FreqKW
        usecase "NetworkX Centralities\\n(Degree, Betweenness, Eigen)" as UC_Centrality
        usecase "Binary Presence Matrix\\n(Paper-Keyword 0/1 Grid)" as UC_PresenceMatrix
        usecase "Explore SVG Word Cloud\\n(Interactive Zoom & Tooltips)" as UC_WordCloud
        usecase "Explore Co-Occurrence Graph\\n(Weighted Pairwise Links)" as UC_CooccurGraph
        usecase "Export Analytics Artifacts\\n(CSV, JSON & PNG Visuals)" as UC_ExportKW
    }

    ' --------------------------------------------------------------------------
    ' D. Country & International Collaboration Module
    ' --------------------------------------------------------------------------
    package "Country & International Collaboration" {
        usecase "Country Analysis\\n(Affiliation Mapping)" as UC_AnalyzeCountry
        usecase "Extract Affiliations\\n(Regex & ISO-3166 Lexicon)" as UC_ExtractCountry
        usecase "Track Unassigned Papers\\n(Data Transparency)" as UC_Unassigned
        usecase "Country Rankings Table\\n(Volume & Percentage Share)" as UC_CountryRank
        usecase "Explore World Map\\n(TopoJSON Choropleth)" as UC_WorldMap
        usecase "Explore 2D/3D Collaboration\\n(Force-Directed & Three.js)" as UC_CollabNet
        usecase "Export Country Data\\n(Rankings & Partnerships CSV)" as UC_ExportCountry
    }

    ' --------------------------------------------------------------------------
    ' E. AI Research Assistant (Conversational RAG) Module
    ' --------------------------------------------------------------------------
    package "AI Research Assistant" {
        usecase "Ask Research Questions\\n(Conversational AI Chat)" as UC_AskAI
        usecase "Decompose Query\\n(Sub-Question Strategy)" as UC_Decompose
        usecase "Retrieve FAISS Context\\n(Top-K Vector Search)" as UC_FAISS
        usecase "Synthesize Answer\\n(Gemini LLM with Citations)" as UC_Synthesize
        usecase "Generate Vector Embeddings\\n(all-mpnet-base-v2, 768-d)" as UC_Embed
        usecase "Scrape Full Text\\n(Polite Scraper with Fallback)" as UC_Scrape
    }
}

' ==============================================================================
' RELATIONSHIPS & ASSOCIATIONS (STEREOTYPE TEXT REMOVED)
' ==============================================================================

' Primary Actor Associations
User -- UC_Search
User -- UC_Cancel
User -- UC_Browse
User -- UC_PDF
User -- UC_ViewPub
User -- UC_Upload
User -- UC_ListDatasets
User -- UC_ExportCSV
User -- UC_DeleteDataset
User -- UC_AnalyzeKW
User -- UC_WordCloud
User -- UC_CooccurGraph
User -- UC_ExportKW
User -- UC_AnalyzeCountry
User -- UC_WorldMap
User -- UC_CountryRank
User -- UC_CollabNet
User -- UC_ExportCountry
User -- UC_AskAI
User -- UC_Embed

' Generalization (Specialized Search Modes inherit Base Search)
UC_Unified -up-|> UC_Search
UC_PubMed -up-|> UC_Search
UC_OpenAlex -up-|> UC_Search

' Research Paper Search: Inclusions & Extensions
UC_Search ..> UC_QueryOpt
UC_Search ..> UC_Browse
UC_Filters ..> UC_Search
UC_Rerank ..> UC_Search
UC_PDF ..> UC_Browse
UC_ViewPub ..> UC_Browse

' Keyword Analytics: Inclusions & Extensions
UC_AnalyzeKW ..> UC_NormKW
UC_AnalyzeKW ..> UC_FreqKW
UC_AnalyzeKW ..> UC_Centrality
UC_AnalyzeKW ..> UC_PresenceMatrix
UC_WordCloud ..> UC_AnalyzeKW
UC_CooccurGraph ..> UC_AnalyzeKW
UC_ExportKW ..> UC_AnalyzeKW

' Country Analysis: Inclusions & Extensions
UC_AnalyzeCountry ..> UC_ExtractCountry
UC_AnalyzeCountry ..> UC_Unassigned
UC_AnalyzeCountry ..> UC_CountryRank
UC_WorldMap ..> UC_AnalyzeCountry
UC_CollabNet ..> UC_AnalyzeCountry
UC_ExportCountry ..> UC_AnalyzeCountry

' AI Assistant: Inclusions & Extensions
UC_AskAI ..> UC_Decompose
UC_AskAI ..> UC_FAISS
UC_AskAI ..> UC_Synthesize
UC_Scrape ..> UC_Embed

' External Actor Interactions
UC_Search -- NCBI
UC_Search -- OpenAlex
UC_PDF -- Publisher
UC_Synthesize -- Gemini

@enduml
"""

# ==============================================================================
# 2. STANDALONE SVG GENERATOR (NO STEREOTYPES)
# ==============================================================================
def generate_svg_source():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1680 1180" width="1680" height="1180" style="background:#ffffff; font-family:'Segoe UI', Inter, -apple-system, sans-serif;">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="2" dy="3" stdDeviation="3" flood-opacity="0.10"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb" />
    </marker>
    <marker id="arrow-dash" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#475569" />
    </marker>
    <marker id="arrow-extend" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#9333ea" />
    </marker>
    <marker id="gen-arrow" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 11 6 L 0 11 z" fill="#ffffff" stroke="#2563eb" stroke-width="1.6"/>
    </marker>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
    <linearGradient id="ucGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f8fafc"/>
    </linearGradient>
    <linearGradient id="actorGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#eff6ff"/>
      <stop offset="100%" stop-color="#dbeafe"/>
    </linearGradient>
  </defs>

  <!-- Title Banner -->
  <rect x="30" y="20" width="1620" height="70" rx="12" fill="url(#headerGrad)" filter="url(#shadow)"/>
  <text x="50" y="48" fill="#38bdf8" font-size="12" font-weight="700" letter-spacing="2">UML 2.5 USE CASE MODEL</text>
  <text x="50" y="72" fill="#ffffff" font-size="20" font-weight="bold">Research Rover: Comprehensive System Functional Capabilities</text>
  <text x="1440" y="60" fill="#94a3b8" font-size="12" font-weight="500">M.Tech Software Architecture Specification</text>

  <!-- Left: Primary Human Actor -->
  <g transform="translate(40, 470)">
    <rect x="0" y="0" width="180" height="250" rx="14" fill="url(#actorGrad)" stroke="#3b82f6" stroke-width="2" filter="url(#shadow)"/>
    <!-- Stick figure -->
    <circle cx="90" cy="50" r="22" fill="#1e40af" stroke="#1d4ed8" stroke-width="2.5"/>
    <line x1="90" y1="72" x2="90" y2="135" stroke="#1d4ed8" stroke-width="4"/>
    <line x1="45" y1="95" x2="135" y2="95" stroke="#1d4ed8" stroke-width="4" stroke-linecap="round"/>
    <line x1="90" y1="135" x2="55" y2="195" stroke="#1d4ed8" stroke-width="4" stroke-linecap="round"/>
    <line x1="90" y1="135" x2="125" y2="195" stroke="#1d4ed8" stroke-width="4" stroke-linecap="round"/>
    <text x="90" y="218" text-anchor="middle" font-size="14" font-weight="bold" fill="#0f172a">Researcher / Student</text>
    <text x="90" y="236" text-anchor="middle" font-size="11" font-weight="500" fill="#64748b">(Primary User)</text>
  </g>

  <!-- System Boundary Box: Research Rover -->
  <rect x="250" y="110" width="1120" height="1020" rx="16" fill="#fafafa" stroke="#3b82f6" stroke-width="2.5" stroke-dasharray="8 6"/>
  <rect x="270" y="98" width="340" height="26" rx="6" fill="#2563eb"/>
  <text x="282" y="116" fill="#ffffff" font-size="12" font-weight="bold" letter-spacing="1">SYSTEM BOUNDARY: RESEARCH ROVER</text>

  <!-- ========================================================================= -->
  <!-- A. Research Paper Search Module -->
  <!-- ========================================================================= -->
  <rect x="270" y="135" width="1080" height="215" rx="12" fill="#ffffff" stroke="#93c5fd" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="290" y="158" font-size="12" font-weight="700" fill="#1e40af">A. RESEARCH PAPER SEARCH MODULE</text>

  <g transform="translate(290, 175)">
    <rect x="0" y="0" width="200" height="48" rx="24" fill="url(#ucGrad)" stroke="#2563eb" stroke-width="2.0"/>
    <text x="100" y="22" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">Search Research Papers</text>
    <text x="100" y="38" text-anchor="middle" font-size="9" fill="#64748b">(Base Search Query)</text>

    <!-- Generalizations -->
    <rect x="260" y="-30" width="170" height="38" rx="19" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.4"/>
    <text x="345" y="-12" text-anchor="middle" font-size="10.5" font-weight="600" fill="#1e3a8a">Unified Search</text>
    <text x="345" y="1" text-anchor="middle" font-size="8.5" fill="#64748b">(PubMed + OpenAlex)</text>

    <rect x="260" y="16" width="170" height="38" rx="19" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.4"/>
    <text x="345" y="34" text-anchor="middle" font-size="10.5" font-weight="600" fill="#1e3a8a">PubMed Search</text>
    <text x="345" y="47" text-anchor="middle" font-size="8.5" fill="#64748b">(Biomedical Focus)</text>

    <rect x="260" y="62" width="170" height="38" rx="19" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.4"/>
    <text x="345" y="80" text-anchor="middle" font-size="10.5" font-weight="600" fill="#1e3a8a">OpenAlex Search</text>
    <text x="345" y="93" text-anchor="middle" font-size="8.5" fill="#64748b">(Multidisciplinary)</text>

    <!-- Sub-use cases -->
    <rect x="490" y="-30" width="220" height="40" rx="20" fill="#f8fafc" stroke="#64748b" stroke-width="1.4"/>
    <text x="600" y="-12" text-anchor="middle" font-size="10.5" font-weight="600" fill="#0f172a">Optimize &amp; Expand Query</text>
    <text x="600" y="1" text-anchor="middle" font-size="8.5" fill="#64748b">(MeSH &amp; Domain Acronyms)</text>

    <rect x="490" y="20" width="220" height="40" rx="20" fill="#faf5ff" stroke="#9333ea" stroke-width="1.4"/>
    <text x="600" y="38" text-anchor="middle" font-size="10.5" font-weight="600" fill="#581c87">Re-Rank Relevance</text>
    <text x="600" y="51" text-anchor="middle" font-size="8.5" fill="#7e22ce">(MedCPT Bi-Encoder)</text>

    <rect x="760" y="-12" width="200" height="46" rx="23" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.8"/>
    <text x="860" y="10" text-anchor="middle" font-size="11" font-weight="bold" fill="#14532d">Browse Search Results</text>
    <text x="860" y="25" text-anchor="middle" font-size="8.5" fill="#15803d">(Paginated Paper Cards)</text>

    <rect x="760" y="60" width="200" height="42" rx="21" fill="#fff1f2" stroke="#e11d48" stroke-width="1.4"/>
    <text x="860" y="80" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#881337">Download Available PDF</text>
    <text x="860" y="93" text-anchor="middle" font-size="8.5" fill="#9f1239">(SSRF-Protected Stream)</text>

    <rect x="990" y="18" width="80" height="36" rx="18" fill="#f8fafc" stroke="#64748b" stroke-width="1.2"/>
    <text x="1030" y="36" text-anchor="middle" font-size="9.5" font-weight="600" fill="#334155">Cancel</text>
    <text x="1030" y="47" text-anchor="middle" font-size="8" fill="#64748b">(Abort)</text>
  </g>

  <!-- Connectors in Search (Arrows preserved, text removed) -->
  <path d="M 550 160 L 490 195" fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#gen-arrow)"/>
  <path d="M 550 210 L 490 200" fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#gen-arrow)"/>
  <path d="M 550 255 L 490 205" fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#gen-arrow)"/>

  <path d="M 490 190 L 780 165" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <path d="M 490 202 L 1050 185" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <path d="M 780 215 L 490 205" fill="none" stroke="#9333ea" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-extend)"/>
  <path d="M 1150 235 L 1150 210" fill="none" stroke="#e11d48" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>

  <!-- ========================================================================= -->
  <!-- B. Dataset Management Module -->
  <!-- ========================================================================= -->
  <rect x="270" y="365" width="1080" height="135" rx="12" fill="#ffffff" stroke="#bae6fd" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="290" y="388" font-size="12" font-weight="700" fill="#0369a1">B. DATASET MANAGEMENT MODULE</text>

  <g transform="translate(290, 405)">
    <rect x="0" y="10" width="230" height="42" rx="21" fill="url(#ucGrad)" stroke="#0284c7" stroke-width="1.8"/>
    <text x="115" y="29" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">Upload Custom Dataset</text>
    <text x="115" y="43" text-anchor="middle" font-size="8.5" fill="#64748b">(CSV Validation &amp; Encoding Check)</text>

    <rect x="280" y="10" width="230" height="42" rx="21" fill="url(#ucGrad)" stroke="#0284c7" stroke-width="1.5"/>
    <text x="395" y="29" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">List &amp; Switch Datasets</text>
    <text x="395" y="43" text-anchor="middle" font-size="8.5" fill="#64748b">(Auto-Discovered from data/)</text>

    <rect x="560" y="10" width="230" height="42" rx="21" fill="url(#ucGrad)" stroke="#0284c7" stroke-width="1.5"/>
    <text x="675" y="29" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">Export Clean Dataset CSV</text>
    <text x="675" y="43" text-anchor="middle" font-size="8.5" fill="#64748b">(Unpolluted Metadata Export)</text>

    <rect x="830" y="10" width="220" height="42" rx="21" fill="url(#ucGrad)" stroke="#dc2626" stroke-width="1.4"/>
    <text x="940" y="29" text-anchor="middle" font-size="11" font-weight="bold" fill="#991b1b">Delete Dataset &amp; Embeddings</text>
    <text x="940" y="43" text-anchor="middle" font-size="8.5" fill="#b91c1c">(Disk Clean-up)</text>
  </g>

  <!-- ========================================================================= -->
  <!-- C. Keyword Bibliometric Analytics Module -->
  <!-- ========================================================================= -->
  <rect x="270" y="515" width="1080" height="200" rx="12" fill="#ffffff" stroke="#bae6fd" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="290" y="538" font-size="12" font-weight="700" fill="#0284c7">C. KEYWORD BIBLIOMETRIC ANALYTICS MODULE</text>

  <g transform="translate(290, 550)">
    <rect x="0" y="40" width="200" height="48" rx="24" fill="url(#ucGrad)" stroke="#0284c7" stroke-width="2.0"/>
    <text x="100" y="62" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#0f172a">Analyse Keywords</text>
    <text x="100" y="77" text-anchor="middle" font-size="8.5" fill="#64748b">(5-Phase Computation Pipeline)</text>

    <rect x="260" y="0" width="230" height="38" rx="19" fill="#f8fafc" stroke="#64748b" stroke-width="1.4"/>
    <text x="375" y="18" text-anchor="middle" font-size="10.5" font-weight="600" fill="#0f172a">Normalize &amp; Alias Map</text>
    <text x="375" y="30" text-anchor="middle" font-size="8.5" fill="#64748b">(AST Parsing &amp; Deduplication)</text>

    <rect x="260" y="48" width="230" height="38" rx="19" fill="#f8fafc" stroke="#64748b" stroke-width="1.4"/>
    <text x="375" y="66" text-anchor="middle" font-size="10.5" font-weight="600" fill="#0f172a">View Frequency &amp; Rank</text>
    <text x="375" y="78" text-anchor="middle" font-size="8.5" fill="#64748b">(Distribution Bar Charts)</text>

    <rect x="260" y="96" width="230" height="38" rx="19" fill="#f8fafc" stroke="#64748b" stroke-width="1.4"/>
    <text x="375" y="114" text-anchor="middle" font-size="10.5" font-weight="600" fill="#0f172a">NetworkX Centralities</text>
    <text x="375" y="126" text-anchor="middle" font-size="8.5" fill="#64748b">(Degree, Betweenness, Eigen)</text>

    <rect x="540" y="12" width="220" height="40" rx="20" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.4"/>
    <text x="650" y="30" text-anchor="middle" font-size="10.5" font-weight="600" fill="#1e3a8a">Explore SVG Word Cloud</text>
    <text x="650" y="43" text-anchor="middle" font-size="8.5" fill="#64748b">(Interactive Zoom &amp; Tooltips)</text>

    <rect x="540" y="66" width="220" height="40" rx="20" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.4"/>
    <text x="650" y="84" text-anchor="middle" font-size="10.5" font-weight="600" fill="#1e3a8a">Explore Co-Occurrence Graph</text>
    <text x="650" y="97" text-anchor="middle" font-size="8.5" fill="#64748b">(Weighted Pairwise Links)</text>

    <rect x="810" y="16" width="220" height="40" rx="20" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.4"/>
    <text x="920" y="34" text-anchor="middle" font-size="10.5" font-weight="600" fill="#14532d">Binary Presence Matrix</text>
    <text x="920" y="47" text-anchor="middle" font-size="8.5" fill="#15803d">(Paper-Keyword 0/1 Grid)</text>

    <rect x="810" y="70" width="220" height="40" rx="20" fill="#f8fafc" stroke="#475569" stroke-width="1.4"/>
    <text x="920" y="88" text-anchor="middle" font-size="10.5" font-weight="600" fill="#0f172a">Export Analytics Artifacts</text>
    <text x="920" y="101" text-anchor="middle" font-size="8.5" fill="#64748b">(CSV, JSON &amp; PNG Visuals)</text>
  </g>

  <!-- Connectors in Keyword (Arrows preserved, text removed) -->
  <path d="M 490 610 L 550 572" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <path d="M 490 614 L 550 618" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <path d="M 490 618 L 550 664" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>

  <path d="M 830 580 L 490 605" fill="none" stroke="#2563eb" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-extend)"/>
  <path d="M 830 635 L 490 618" fill="none" stroke="#2563eb" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-extend)"/>

  <!-- ========================================================================= -->
  <!-- D. Country & International Collaboration Module -->
  <!-- ========================================================================= -->
  <rect x="270" y="730" width="1080" height="195" rx="12" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="290" y="753" font-size="12" font-weight="700" fill="#047857">D. COUNTRY &amp; INTERNATIONAL COLLABORATION MODULE</text>

  <g transform="translate(290, 765)">
    <rect x="0" y="38" width="200" height="48" rx="24" fill="url(#ucGrad)" stroke="#059669" stroke-width="2.0"/>
    <text x="100" y="60" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#0f172a">Country Analysis</text>
    <text x="100" y="74" text-anchor="middle" font-size="8.5" fill="#64748b">(Affiliation Mapping)</text>

    <rect x="260" y="0" width="230" height="38" rx="19" fill="#f8fafc" stroke="#64748b" stroke-width="1.4"/>
    <text x="375" y="18" text-anchor="middle" font-size="10.5" font-weight="600" fill="#0f172a">Extract Affiliations</text>
    <text x="375" y="30" text-anchor="middle" font-size="8.5" fill="#64748b">(Regex &amp; ISO-3166 Lexicon)</text>

    <rect x="260" y="48" width="230" height="38" rx="19" fill="#fff7ed" stroke="#f97316" stroke-width="1.4"/>
    <text x="375" y="66" text-anchor="middle" font-size="10.5" font-weight="600" fill="#c2410c">Track Unassigned Papers</text>
    <text x="375" y="78" text-anchor="middle" font-size="8.5" fill="#ea580c">(Data Transparency)</text>

    <rect x="260" y="96" width="230" height="38" rx="19" fill="#f8fafc" stroke="#64748b" stroke-width="1.4"/>
    <text x="375" y="114" text-anchor="middle" font-size="10.5" font-weight="600" fill="#0f172a">Country Rankings Table</text>
    <text x="375" y="126" text-anchor="middle" font-size="8.5" fill="#64748b">(Volume &amp; Percentage Share)</text>

    <rect x="540" y="15" width="220" height="42" rx="21" fill="#ecfdf5" stroke="#10b981" stroke-width="1.4"/>
    <text x="650" y="34" text-anchor="middle" font-size="10.5" font-weight="600" fill="#065f46">Explore World Map</text>
    <text x="650" y="48" text-anchor="middle" font-size="8.5" fill="#047857">(TopoJSON Choropleth)</text>

    <rect x="540" y="70" width="220" height="42" rx="21" fill="#ecfdf5" stroke="#10b981" stroke-width="1.4"/>
    <text x="650" y="89" text-anchor="middle" font-size="10.5" font-weight="600" fill="#065f46">Explore 2D/3D Collaboration</text>
    <text x="650" y="103" text-anchor="middle" font-size="8.5" fill="#047857">(Force-Directed &amp; Three.js)</text>

    <rect x="810" y="42" width="220" height="42" rx="21" fill="#f8fafc" stroke="#475569" stroke-width="1.4"/>
    <text x="920" y="61" text-anchor="middle" font-size="10.5" font-weight="600" fill="#0f172a">Export Country Data</text>
    <text x="920" y="75" text-anchor="middle" font-size="8.5" fill="#64748b">(Rankings &amp; Partnerships CSV)</text>
  </g>

  <!-- Connectors in Country (Arrows preserved, text removed) -->
  <path d="M 490 815 L 550 786" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <path d="M 490 822 L 550 832" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <path d="M 490 828 L 550 880" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>

  <path d="M 830 795 L 490 818" fill="none" stroke="#059669" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-extend)"/>
  <path d="M 830 852 L 490 825" fill="none" stroke="#059669" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-extend)"/>

  <!-- ========================================================================= -->
  <!-- E. AI Research Assistant Module -->
  <!-- ========================================================================= -->
  <rect x="270" y="940" width="1080" height="170" rx="12" fill="#ffffff" stroke="#ddd6fe" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="290" y="963" font-size="12" font-weight="700" fill="#6d28d9">E. AI RESEARCH ASSISTANT (CONVERSATIONAL RAG) MODULE</text>

  <g transform="translate(290, 975)">
    <rect x="0" y="28" width="200" height="48" rx="24" fill="url(#ucGrad)" stroke="#7c3aed" stroke-width="2.0"/>
    <text x="100" y="50" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#0f172a">Ask Research Questions</text>
    <text x="100" y="64" text-anchor="middle" font-size="8.5" fill="#64748b">(Conversational AI Chat)</text>

    <rect x="260" y="10" width="230" height="40" rx="20" fill="#faf5ff" stroke="#8b5cf6" stroke-width="1.4"/>
    <text x="375" y="28" text-anchor="middle" font-size="10.5" font-weight="600" fill="#4c1d95">Decompose Query</text>
    <text x="375" y="42" text-anchor="middle" font-size="8.5" fill="#6d28d9">(Sub-Question Strategy)</text>

    <rect x="540" y="10" width="230" height="40" rx="20" fill="#faf5ff" stroke="#8b5cf6" stroke-width="1.4"/>
    <text x="655" y="28" text-anchor="middle" font-size="10.5" font-weight="600" fill="#4c1d95">Retrieve FAISS Context</text>
    <text x="655" y="42" text-anchor="middle" font-size="8.5" fill="#6d28d9">(Top-K Vector Search)</text>

    <rect x="810" y="10" width="230" height="40" rx="20" fill="#fdf2f8" stroke="#db2777" stroke-width="1.6"/>
    <text x="925" y="28" text-anchor="middle" font-size="11" font-weight="bold" fill="#831843">Synthesize Answer</text>
    <text x="925" y="42" text-anchor="middle" font-size="8.5" fill="#9d174d">(Gemini LLM with Citations)</text>

    <rect x="260" y="65" width="230" height="40" rx="20" fill="#f8fafc" stroke="#64748b" stroke-width="1.4"/>
    <text x="375" y="83" text-anchor="middle" font-size="10.5" font-weight="600" fill="#0f172a">Generate Vector Embeddings</text>
    <text x="375" y="97" text-anchor="middle" font-size="8.5" fill="#64748b">(all-mpnet-base-v2, 768-d)</text>

    <rect x="540" y="65" width="230" height="40" rx="20" fill="#faf5ff" stroke="#c084fc" stroke-width="1.4"/>
    <text x="655" y="83" text-anchor="middle" font-size="10.5" font-weight="600" fill="#581c87">Scrape Full Text</text>
    <text x="655" y="97" text-anchor="middle" font-size="8.5" fill="#7e22ce">(Polite Scraper with Fallback)</text>
  </g>

  <!-- Connectors in AI (Arrows preserved, text removed) -->
  <path d="M 490 1025 L 550 1005" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <path d="M 720 1005 L 830 1005" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <path d="M 1000 1005 L 1100 1005" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <path d="M 830 1060 L 720 1060" fill="none" stroke="#9333ea" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#arrow-extend)"/>

  <!-- ========================================================================= -->
  <!-- Right: External System Actors -->
  <!-- ========================================================================= -->
  <g transform="translate(1420, 160)">
    <!-- NCBI -->
    <rect x="0" y="0" width="220" height="85" rx="12" fill="#f8fafc" stroke="#0284c7" stroke-width="1.8" filter="url(#shadow)"/>
    <text x="110" y="38" text-anchor="middle" font-size="13" font-weight="bold" fill="#0f172a">NCBI Entrez API</text>
    <text x="110" y="58" text-anchor="middle" font-size="10" fill="#64748b">(PubMed Paper Retrieval)</text>

    <!-- OpenAlex -->
    <rect x="0" y="115" width="220" height="85" rx="12" fill="#f8fafc" stroke="#0d9488" stroke-width="1.8" filter="url(#shadow)"/>
    <text x="110" y="153" text-anchor="middle" font-size="13" font-weight="bold" fill="#0f172a">OpenAlex API</text>
    <text x="110" y="173" text-anchor="middle" font-size="10" fill="#64748b">(Citations &amp; OA Links)</text>

    <!-- Publishers & PMC -->
    <rect x="0" y="235" width="220" height="85" rx="12" fill="#f8fafc" stroke="#e11d48" stroke-width="1.8" filter="url(#shadow)"/>
    <text x="110" y="273" text-anchor="middle" font-size="13" font-weight="bold" fill="#0f172a">Publishers &amp; PMC</text>
    <text x="110" y="293" text-anchor="middle" font-size="10" fill="#64748b">(Full-Text PDF Hosts)</text>

    <!-- Google Gemini AI -->
    <rect x="0" y="805" width="220" height="85" rx="12" fill="#f8fafc" stroke="#9333ea" stroke-width="1.8" filter="url(#shadow)"/>
    <text x="110" y="843" text-anchor="middle" font-size="13" font-weight="bold" fill="#0f172a">Google Gemini AI</text>
    <text x="110" y="863" text-anchor="middle" font-size="10" fill="#64748b">(Generative Synthesis)</text>
  </g>

  <!-- External Actor Associations -->
  <line x1="780" y1="205" x2="1420" y2="202" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="3 3"/>
  <line x1="780" y1="250" x2="1420" y2="318" stroke="#0d9488" stroke-width="1.5" stroke-dasharray="3 3"/>
  <line x1="1250" y1="265" x2="1420" y2="435" stroke="#e11d48" stroke-width="1.5" stroke-dasharray="3 3"/>
  <line x1="1330" y1="1005" x2="1420" y2="1005" stroke="#9333ea" stroke-width="1.5" stroke-dasharray="3 3"/>

  <!-- Primary User Associations -->
  <line x1="220" y1="520" x2="290" y2="200" stroke="#2563eb" stroke-width="2.0"/>
  <line x1="220" y1="550" x2="290" y2="435" stroke="#0284c7" stroke-width="2.0"/>
  <line x1="220" y1="590" x2="290" y2="615" stroke="#0284c7" stroke-width="2.0"/>
  <line x1="220" y1="630" x2="290" y2="825" stroke="#059669" stroke-width="2.0"/>
  <line x1="220" y1="670" x2="290" y2="1025" stroke="#7c3aed" stroke-width="2.0"/>

  <!-- Legend Bottom Bar (No stereotype text) -->
  <rect x="30" y="1142" width="1620" height="30" rx="6" fill="#f1f5f9" stroke="#cbd5e1"/>
  <text x="50" y="1162" font-size="11" font-weight="bold" fill="#334155">UML 2.5 NOTATION LEGEND:</text>
  <line x1="240" y1="1158" x2="280" y2="1158" stroke="#2563eb" stroke-width="2"/>
  <text x="290" y="1162" font-size="11" fill="#475569">Actor Association</text>

  <line x1="450" y1="1158" x2="490" y2="1158" stroke="#475569" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#arrow-dash)"/>
  <text x="500" y="1162" font-size="11" fill="#475569">Mandatory Reused Behaviour</text>

  <line x1="770" y1="1158" x2="810" y2="1158" stroke="#9333ea" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#arrow-extend)"/>
  <text x="820" y="1162" font-size="11" fill="#475569">Conditional / Optional Extension</text>

  <line x1="1130" y1="1158" x2="1170" y2="1158" stroke="#2563eb" stroke-width="1.5" marker-end="url(#gen-arrow)"/>
  <text x="1180" y="1162" font-size="11" fill="#475569">Generalization (Specialized Search Variant)</text>
</svg>'''

# ==============================================================================
# 3. HIGH-RESOLUTION MATPLOTLIB RENDERER (PNG & PDF, NO STEREOTYPES)
# ==============================================================================
def draw_stick_figure(ax, x, y, scale=1.0, color="#1D4ED8"):
    head_radius = 0.18 * scale
    head = Circle((x, y + 0.65 * scale), head_radius, facecolor="#EFF6FF", edgecolor=color, linewidth=2.0, zorder=5)
    ax.add_patch(head)
    ax.plot([x, x], [y + 0.65 * scale - head_radius, y + 0.1 * scale], color=color, linewidth=2.5, solid_capstyle='round', zorder=5)
    ax.plot([x - 0.35 * scale, x + 0.35 * scale], [y + 0.35 * scale, y + 0.35 * scale], color=color, linewidth=2.5, solid_capstyle='round', zorder=5)
    ax.plot([x, x - 0.28 * scale], [y + 0.1 * scale, y - 0.45 * scale], color=color, linewidth=2.5, solid_capstyle='round', zorder=5)
    ax.plot([x, x + 0.28 * scale], [y + 0.1 * scale, y - 0.45 * scale], color=color, linewidth=2.5, solid_capstyle='round', zorder=5)

def draw_usecase_oval(ax, x, y, width, height, title, subtitle=None, fillcolor="#F8FAFC", edgecolor="#2563EB", textcolor="#0F172A", title_fontsize=9, sub_fontsize=7.5, is_base=False):
    lw = 2.0 if is_base else 1.3
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle=f"round,pad=0,rounding_size={height/2}",
        facecolor=fillcolor,
        edgecolor=edgecolor,
        linewidth=lw,
        zorder=4
    )
    ax.add_patch(box)
    
    if subtitle:
        ax.text(x, y + height * 0.12, title, ha='center', va='center', fontsize=title_fontsize, fontweight='bold', color=textcolor, zorder=6)
        ax.text(x, y - height * 0.22, subtitle, ha='center', va='center', fontsize=sub_fontsize, color="#64748B", zorder=6)
    else:
        ax.text(x, y, title, ha='center', va='center', fontsize=title_fontsize, fontweight='bold', color=textcolor, zorder=6)

def draw_external_actor(ax, x, y, width, height, title, subtitle, tag_color="#0284C7"):
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0,rounding_size=0.15",
        facecolor="#F8FAFC",
        edgecolor=tag_color,
        linewidth=1.6,
        zorder=4
    )
    ax.add_patch(box)
    
    # Balanced layout without <<external system>>
    ax.text(x, y + height * 0.12, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color="#0F172A", zorder=6)
    ax.text(x, y - height * 0.18, subtitle, ha='center', va='center', fontsize=8.0, color="#64748B", zorder=6)

def render_figure(png_path, pdf_path):
    fig, ax = plt.subplots(figsize=(20, 13.5), dpi=300)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 13.5)
    ax.axis('off')
    
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Header Banner
    header = FancyBboxPatch((0.5, 12.3), 19.0, 0.9, boxstyle="round,pad=0,rounding_size=0.15",
                            facecolor="#0F172A", edgecolor="#1E293B", linewidth=1.5, zorder=3)
    ax.add_patch(header)
    ax.text(0.8, 12.85, "UML 2.5 USE CASE MODEL", fontsize=9.5, fontweight='bold', color="#38BDF8")
    ax.text(0.8, 12.52, "Research Rover: Comprehensive System Functional Capabilities", fontsize=15, fontweight='bold', color="#FFFFFF")
    ax.text(19.2, 12.65, "M.Tech Software Architecture Specification", ha='right', va='center', fontsize=9.5, color="#94A3B8")

    # System Boundary Box
    boundary = FancyBboxPatch((3.0, 0.7), 13.8, 11.3, boxstyle="round,pad=0,rounding_size=0.25",
                              facecolor="#FAFAFA", edgecolor="#3B82F6", linewidth=2.5, linestyle="--", zorder=2)
    ax.add_patch(boundary)
    
    tag_box = FancyBboxPatch((3.3, 11.65), 4.2, 0.45, boxstyle="round,pad=0,rounding_size=0.1",
                             facecolor="#2563EB", edgecolor="none", zorder=3)
    ax.add_patch(tag_box)
    ax.text(5.4, 11.87, "SYSTEM BOUNDARY: RESEARCH ROVER", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#FFFFFF")

    # Primary Actor (No <<human actor>>)
    actor_card = FancyBboxPatch((0.5, 5.0), 2.2, 3.2, boxstyle="round,pad=0,rounding_size=0.2",
                                facecolor="#EFF6FF", edgecolor="#3B82F6", linewidth=1.8, zorder=3)
    ax.add_patch(actor_card)
    draw_stick_figure(ax, 1.6, 6.7, scale=1.1, color="#1D4ED8")
    ax.text(1.6, 5.5, "Researcher / Student", ha='center', va='center', fontsize=11, fontweight='bold', color="#0F172A")
    ax.text(1.6, 5.2, "(Primary User)", ha='center', va='center', fontsize=8.5, color="#64748B")

    # Module A: Research Paper Search
    grp_search = FancyBboxPatch((3.3, 9.25), 13.2, 2.3, boxstyle="round,pad=0,rounding_size=0.18",
                                facecolor="#FFFFFF", edgecolor="#93C5FD", linewidth=1.4, zorder=3)
    ax.add_patch(grp_search)
    ax.text(3.5, 11.3, "A. RESEARCH PAPER SEARCH MODULE", fontsize=9.5, fontweight='bold', color="#1E40AF")
    
    draw_usecase_oval(ax, 4.8, 10.35, 2.4, 0.65, "Search Research Papers", "(Base Search Query)", fillcolor="#EFF6FF", edgecolor="#2563EB", is_base=True)
    draw_usecase_oval(ax, 7.8, 11.0, 2.1, 0.5, "Unified Search", "(PubMed + OpenAlex)", fillcolor="#F8FAFC", edgecolor="#3B82F6")
    draw_usecase_oval(ax, 7.8, 10.35, 2.1, 0.5, "PubMed Search", "(Biomedical Focus)", fillcolor="#F8FAFC", edgecolor="#3B82F6")
    draw_usecase_oval(ax, 7.8, 9.7, 2.1, 0.5, "OpenAlex Search", "(Multidisciplinary)", fillcolor="#F8FAFC", edgecolor="#3B82F6")
    
    draw_usecase_oval(ax, 10.6, 10.85, 2.2, 0.52, "Optimize & Expand Query", "(MeSH & Domain Acronyms)", fillcolor="#F8FAFC", edgecolor="#64748B")
    draw_usecase_oval(ax, 10.6, 9.85, 2.2, 0.52, "Re-Rank Relevance", "(MedCPT Bi-Encoder)", fillcolor="#FAF5FF", edgecolor="#9333EA")
    draw_usecase_oval(ax, 13.4, 10.85, 2.3, 0.55, "Browse Search Results", "(Paginated Paper Cards)", fillcolor="#F0FDF4", edgecolor="#16A34A", is_base=True)
    draw_usecase_oval(ax, 13.4, 9.85, 2.2, 0.52, "Download Available PDF", "(SSRF-Protected Stream)", fillcolor="#FFF1F2", edgecolor="#E11D48")
    draw_usecase_oval(ax, 15.65, 10.35, 1.8, 0.5, "Cancel In-Flight Search", "(Cooperative Abort)", fillcolor="#F8FAFC", edgecolor="#64748B")

    # Connectors for Search (Arrows preserved, stereotype labels removed)
    ax.annotate("", xy=(6.0, 10.5), xytext=(6.75, 10.9), arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=1.3, mutation_scale=12))
    ax.annotate("", xy=(6.0, 10.35), xytext=(6.75, 10.35), arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=1.3, mutation_scale=12))
    ax.annotate("", xy=(6.0, 10.2), xytext=(6.75, 9.8), arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=1.3, mutation_scale=12))

    ax.annotate("", xy=(9.5, 10.85), xytext=(6.0, 10.5), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.annotate("", xy=(12.25, 10.85), xytext=(6.0, 10.4), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.annotate("", xy=(6.0, 10.15), xytext=(9.5, 9.85), arrowprops=dict(arrowstyle="->", color="#9333EA", lw=1.2, ls="--", mutation_scale=10))
    ax.annotate("", xy=(13.4, 10.57), xytext=(13.4, 10.11), arrowprops=dict(arrowstyle="->", color="#E11D48", lw=1.2, ls="--", mutation_scale=10))

    # Module B: Dataset Management
    grp_dataset = FancyBboxPatch((3.3, 7.65), 13.2, 1.45, boxstyle="round,pad=0,rounding_size=0.18",
                                 facecolor="#FFFFFF", edgecolor="#BAE6FD", linewidth=1.4, zorder=3)
    ax.add_patch(grp_dataset)
    ax.text(3.5, 8.88, "B. DATASET MANAGEMENT MODULE", fontsize=9.5, fontweight='bold', color="#0369A1")

    draw_usecase_oval(ax, 5.0, 8.25, 2.5, 0.58, "Upload Custom Dataset", "(CSV Validation & Encoding)", fillcolor="#F0F9FF", edgecolor="#0284C7", is_base=True)
    draw_usecase_oval(ax, 8.3, 8.25, 2.5, 0.58, "List & Switch Datasets", "(Auto-Discovered from data/)", fillcolor="#F8FAFC", edgecolor="#0284C7")
    draw_usecase_oval(ax, 11.6, 8.25, 2.5, 0.58, "Export Clean Dataset CSV", "(Unpolluted Research Columns)", fillcolor="#F8FAFC", edgecolor="#0284C7")
    draw_usecase_oval(ax, 14.8, 8.25, 2.4, 0.58, "Delete Dataset & Embeddings", "(File Storage Clean-up)", fillcolor="#FEF2F2", edgecolor="#DC2626")

    # Module C: Keyword Analytics
    grp_keyword = FancyBboxPatch((3.3, 5.3), 13.2, 2.2, boxstyle="round,pad=0,rounding_size=0.18",
                                 facecolor="#FFFFFF", edgecolor="#BAE6FD", linewidth=1.4, zorder=3)
    ax.add_patch(grp_keyword)
    ax.text(3.5, 7.28, "C. KEYWORD BIBLIOMETRIC ANALYTICS MODULE", fontsize=9.5, fontweight='bold', color="#0284C7")

    draw_usecase_oval(ax, 4.8, 6.35, 2.4, 0.65, "Analyse Keywords", "(5-Phase Computation Pipeline)", fillcolor="#F0F9FF", edgecolor="#0284C7", is_base=True)

    draw_usecase_oval(ax, 7.9, 6.95, 2.3, 0.48, "Normalize & Alias Map", "(AST Parser & Deduplication)", fillcolor="#F8FAFC", edgecolor="#64748B")
    draw_usecase_oval(ax, 7.9, 6.35, 2.3, 0.48, "View Frequency & Rank", "(Distribution Bar Charts)", fillcolor="#F8FAFC", edgecolor="#64748B")
    draw_usecase_oval(ax, 7.9, 5.75, 2.3, 0.48, "NetworkX Centralities", "(Degree, Betweenness, Eigen)", fillcolor="#F8FAFC", edgecolor="#64748B")

    draw_usecase_oval(ax, 10.9, 6.75, 2.4, 0.52, "Explore SVG Word Cloud", "(Interactive Zoom & Tooltips)", fillcolor="#EFF6FF", edgecolor="#3B82F6")
    draw_usecase_oval(ax, 10.9, 5.95, 2.4, 0.52, "Explore Co-Occurrence Graph", "(Weighted Pairwise Links)", fillcolor="#EFF6FF", edgecolor="#3B82F6")

    draw_usecase_oval(ax, 14.2, 6.75, 2.4, 0.52, "Binary Presence Matrix", "(Paper-Keyword 0/1 Association)", fillcolor="#F0FDF4", edgecolor="#16A34A")
    draw_usecase_oval(ax, 14.2, 5.95, 2.4, 0.52, "Export Analytics Artifacts", "(CSV, JSON & Visual Exports)", fillcolor="#F8FAFC", edgecolor="#64748B")

    # Connectors for Keywords (Arrows preserved, stereotype labels removed)
    ax.annotate("", xy=(6.75, 6.9), xytext=(6.0, 6.5), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.annotate("", xy=(6.75, 6.35), xytext=(6.0, 6.35), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.annotate("", xy=(6.75, 5.8), xytext=(6.0, 6.2), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))

    ax.annotate("", xy=(6.0, 6.45), xytext=(9.7, 6.75), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.2, ls="--", mutation_scale=10))
    ax.annotate("", xy=(6.0, 6.25), xytext=(9.7, 5.95), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.2, ls="--", mutation_scale=10))

    # Module D: Country Analysis
    grp_country = FancyBboxPatch((3.3, 3.0), 13.2, 2.15, boxstyle="round,pad=0,rounding_size=0.18",
                                 facecolor="#FFFFFF", edgecolor="#A7F3D0", linewidth=1.4, zorder=3)
    ax.add_patch(grp_country)
    ax.text(3.5, 4.95, "D. COUNTRY & INTERNATIONAL COLLABORATION MODULE", fontsize=9.5, fontweight='bold', color="#047857")

    draw_usecase_oval(ax, 4.8, 4.05, 2.4, 0.65, "Country Analysis", "(Affiliation Mapping)", fillcolor="#ECFDF5", edgecolor="#059669", is_base=True)

    draw_usecase_oval(ax, 7.9, 4.65, 2.3, 0.48, "Extract Affiliations", "(Regex & ISO-3166 Lexicon)", fillcolor="#F8FAFC", edgecolor="#64748B")
    draw_usecase_oval(ax, 7.9, 4.05, 2.3, 0.48, "Track Unassigned Papers", "(Data Quality & Transparency)", fillcolor="#FFF7ED", edgecolor="#EA580C")
    draw_usecase_oval(ax, 7.9, 3.45, 2.3, 0.48, "Country Rankings Table", "(Volume & Percentage Share)", fillcolor="#F8FAFC", edgecolor="#64748B")

    draw_usecase_oval(ax, 10.9, 4.45, 2.4, 0.52, "Explore World Map", "(TopoJSON Choropleth)", fillcolor="#ECFDF5", edgecolor="#10B981")
    draw_usecase_oval(ax, 10.9, 3.65, 2.4, 0.52, "Explore 2D/3D Collaboration", "(Force-Directed & Three.js Graphs)", fillcolor="#ECFDF5", edgecolor="#10B981")

    draw_usecase_oval(ax, 14.2, 4.05, 2.4, 0.55, "Export Country Data", "(Rankings & Collaboration CSVs)", fillcolor="#F8FAFC", edgecolor="#64748B")

    # Connectors for Country (Arrows preserved, stereotype labels removed)
    ax.annotate("", xy=(6.75, 4.6), xytext=(6.0, 4.2), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.annotate("", xy=(6.75, 4.05), xytext=(6.0, 4.05), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.annotate("", xy=(6.75, 3.5), xytext=(6.0, 3.9), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))

    ax.annotate("", xy=(6.0, 4.15), xytext=(9.7, 4.45), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.2, ls="--", mutation_scale=10))
    ax.annotate("", xy=(6.0, 3.95), xytext=(9.7, 3.65), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.2, ls="--", mutation_scale=10))

    # Module E: AI Research Assistant
    grp_ai = FancyBboxPatch((3.3, 0.95), 13.2, 1.9, boxstyle="round,pad=0,rounding_size=0.18",
                            facecolor="#FFFFFF", edgecolor="#DDD6FE", linewidth=1.4, zorder=3)
    ax.add_patch(grp_ai)
    ax.text(3.5, 2.65, "E. AI RESEARCH ASSISTANT (CONVERSATIONAL RAG) MODULE", fontsize=9.5, fontweight='bold', color="#6D28D9")

    draw_usecase_oval(ax, 4.8, 1.85, 2.4, 0.65, "Ask Research Questions", "(Conversational AI Chat)", fillcolor="#F5F3FF", edgecolor="#7C3AED", is_base=True)

    draw_usecase_oval(ax, 7.9, 2.3, 2.3, 0.48, "Generate Vector Embeddings", "(all-mpnet-base-v2, 768-d)", fillcolor="#F8FAFC", edgecolor="#64748B")
    draw_usecase_oval(ax, 7.9, 1.4, 2.3, 0.48, "Decompose Query", "(Sub-Question Search Strategy)", fillcolor="#FAF5FF", edgecolor="#8B5CF6")

    draw_usecase_oval(ax, 10.9, 2.3, 2.4, 0.48, "Retrieve FAISS Context", "(Top-K Vector Search)", fillcolor="#FAF5FF", edgecolor="#8B5CF6")
    draw_usecase_oval(ax, 10.9, 1.4, 2.4, 0.48, "Scrape Full Text", "(Polite Scraper with Fallback)", fillcolor="#FAF5FF", edgecolor="#8B5CF6")

    draw_usecase_oval(ax, 14.2, 1.85, 2.4, 0.58, "Synthesize Answer", "(Gemini LLM with Citations)", fillcolor="#FDF2F8", edgecolor="#DB2777", is_base=True)

    # Connectors for AI (Arrows preserved, stereotype labels removed)
    ax.annotate("", xy=(6.75, 1.4), xytext=(6.0, 1.75), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.annotate("", xy=(9.7, 2.3), xytext=(6.0, 1.85), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.annotate("", xy=(13.0, 1.85), xytext=(6.0, 1.85), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.annotate("", xy=(7.9, 2.06), xytext=(9.7, 1.55), arrowprops=dict(arrowstyle="->", color="#8B5CF6", lw=1.2, ls="--", mutation_scale=10))

    # Primary User Associations
    ax.annotate("", xy=(3.6, 10.35), xytext=(2.7, 6.8), arrowprops=dict(arrowstyle="-", color="#2563EB", lw=1.8))
    ax.annotate("", xy=(3.75, 8.25), xytext=(2.7, 6.7), arrowprops=dict(arrowstyle="-", color="#0284C7", lw=1.8))
    ax.annotate("", xy=(3.6, 6.35), xytext=(2.7, 6.6), arrowprops=dict(arrowstyle="-", color="#0284C7", lw=1.8))
    ax.annotate("", xy=(3.6, 4.05), xytext=(2.7, 6.4), arrowprops=dict(arrowstyle="-", color="#059669", lw=1.8))
    ax.annotate("", xy=(3.6, 1.85), xytext=(2.7, 6.2), arrowprops=dict(arrowstyle="-", color="#7C3AED", lw=1.8))

    # External System Actors (Right, No <<external system>>)
    draw_external_actor(ax, 18.2, 11.0, 2.4, 0.9, "NCBI Entrez API", "PubMed Paper Retrieval", tag_color="#0284C7")
    draw_external_actor(ax, 18.2, 9.8, 2.4, 0.9, "OpenAlex API", "Citations & OA Links", tag_color="#0D9488")
    draw_external_actor(ax, 18.2, 8.4, 2.4, 0.9, "Publishers & PMC", "Full-Text PDF Hosts", tag_color="#E11D48")
    draw_external_actor(ax, 18.2, 1.85, 2.4, 0.9, "Google Gemini AI", "Generative Synthesis", tag_color="#9333EA")

    # Dotted Associations to External Systems
    ax.annotate("", xy=(17.0, 11.0), xytext=(8.85, 10.35), arrowprops=dict(arrowstyle="-", color="#0284C7", lw=1.3, ls=":"))
    ax.annotate("", xy=(17.0, 9.8), xytext=(8.85, 9.7), arrowprops=dict(arrowstyle="-", color="#0D9488", lw=1.3, ls=":"))
    ax.annotate("", xy=(17.0, 8.4), xytext=(14.5, 9.85), arrowprops=dict(arrowstyle="-", color="#E11D48", lw=1.3, ls=":"))
    ax.annotate("", xy=(17.0, 1.85), xytext=(15.4, 1.85), arrowprops=dict(arrowstyle="-", color="#9333EA", lw=1.3, ls=":"))

    # Legend Bar (No stereotypes in labels)
    legend_bar = FancyBboxPatch((0.5, 0.1), 19.0, 0.45, boxstyle="round,pad=0,rounding_size=0.08",
                                facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=1.0, zorder=3)
    ax.add_patch(legend_bar)
    
    ax.text(0.8, 0.32, "UML 2.5 NOTATION LEGEND:", fontsize=8.5, fontweight='bold', color="#1E293B")
    
    ax.plot([3.5, 4.1], [0.32, 0.32], color="#2563EB", lw=2.0)
    ax.text(4.2, 0.32, "Actor Association", fontsize=8, color="#334155", va='center')
    
    ax.annotate("", xy=(7.2, 0.32), xytext=(6.5, 0.32), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.4, ls="--", mutation_scale=9))
    ax.text(7.3, 0.32, "Mandatory Reused Behaviour", fontsize=8, color="#334155", va='center')
    
    ax.annotate("", xy=(11.5, 0.32), xytext=(10.8, 0.32), arrowprops=dict(arrowstyle="->", color="#9333EA", lw=1.4, ls="--", mutation_scale=9))
    ax.text(11.6, 0.32, "Conditional / Optional Extension", fontsize=8, color="#334155", va='center')
    
    ax.annotate("", xy=(16.2, 0.32), xytext=(15.5, 0.32), arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=1.4, mutation_scale=10))
    ax.text(16.3, 0.32, "Generalization (Specialized Search Variant)", fontsize=8, color="#334155", va='center')

    plt.tight_layout()
    plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.savefig(pdf_path, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated 300 DPI PNG: {png_path}")
    print(f"Generated Vector PDF:  {pdf_path}")

def main():
    base_dir = Path("E:/Research_Rover")
    uml_dir = base_dir / "docs" / "uml"
    pub_dir = base_dir / "frontend" / "public" / "assets" / "uml"
    
    for d in [uml_dir, pub_dir]:
        d.mkdir(parents=True, exist_ok=True)
    
    # 1. PUML
    puml_content = generate_plantuml_source()
    puml_targets = [
        base_dir / "Research_Rover_Use_Case_Diagram.puml",
        uml_dir / "Research_Rover_Use_Case_Diagram.puml",
        uml_dir / "use_case_diagram.puml",
        pub_dir / "Research_Rover_Use_Case_Diagram.puml",
        pub_dir / "use_case_diagram.puml",
    ]
    for p in puml_targets:
        p.write_text(puml_content, encoding='utf-8')
        print(f"Wrote PlantUML file: {p}")
        
    # 2. SVG
    svg_content = generate_svg_source()
    svg_targets = [
        base_dir / "Research_Rover_Use_Case_Diagram.svg",
        uml_dir / "Research_Rover_Use_Case_Diagram.svg",
        uml_dir / "use_case_diagram.svg",
        pub_dir / "Research_Rover_Use_Case_Diagram.svg",
        pub_dir / "use_case_diagram.svg",
    ]
    for s in svg_targets:
        s.write_text(svg_content, encoding='utf-8')
        print(f"Wrote SVG file: {s}")

    # 3. PNG & PDF via Matplotlib
    png_root = base_dir / "Research_Rover_Use_Case_Diagram.png"
    pdf_dest = uml_dir / "Research_Rover_Use_Case_Diagram.pdf"
    render_figure(png_root, pdf_dest)
    
    # Mirror PNG and PDF to docs/uml and public
    for dest_dir in [uml_dir, pub_dir]:
        shutil.copy2(png_root, dest_dir / "Research_Rover_Use_Case_Diagram.png")
        shutil.copy2(png_root, dest_dir / "use_case_diagram.png")
        shutil.copy2(pdf_dest, dest_dir / "use_case_diagram.pdf")
        if dest_dir != uml_dir:
            shutil.copy2(pdf_dest, dest_dir / "Research_Rover_Use_Case_Diagram.pdf")

    # Try copying to root PDF
    try:
        shutil.copy2(pdf_dest, base_dir / "Research_Rover_Use_Case_Diagram.pdf")
        print("Updated root PDF successfully: Research_Rover_Use_Case_Diagram.pdf")
    except PermissionError:
        print("Notice: E:/Research_Rover/Research_Rover_Use_Case_Diagram.pdf is currently open in a PDF viewer.")
        shutil.copy2(pdf_dest, base_dir / "Research_Rover_Use_Case_Diagram_No_Stereotypes.pdf")
        print("Created E:/Research_Rover/Research_Rover_Use_Case_Diagram_No_Stereotypes.pdf without stereotypes.")

    print("\n[SUCCESS] All deliverables generated and synchronized!")

if __name__ == '__main__':
    main()
