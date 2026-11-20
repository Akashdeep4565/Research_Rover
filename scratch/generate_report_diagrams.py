"""
Generate high-resolution technical diagrams for the Research Rover Academic Progress Report.
Renders SVG to PNG via resvg-py.
"""

import os
import re
import resvg_py

FIGURES_DIR = os.path.abspath("reports/figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# FIGURE 1: OVERALL SYSTEM ARCHITECTURE OF UNIVERSAL DATASET INGESTION
# ---------------------------------------------------------------------------
def build_fig_1_architecture() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 950" width="1600" height="950">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0F172A" flood-opacity="0.1"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1E3A8A"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
    </marker>
    <linearGradient id="hdr" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#142B65"/>
      <stop offset="100%" stop-color="#1E3A8A"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="1600" height="950" fill="#F8FAFC"/>

  <!-- Top Title Bar -->
  <rect x="40" y="25" width="1520" height="55" rx="6" fill="url(#hdr)" />
  <text x="60" y="58" font-family="Arial, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF">
    Figure 4.1: High-Level Architecture of the Universal Dataset Ingestion &amp; Quality System
  </text>
  <text x="1530" y="58" font-family="Arial, sans-serif" font-size="12" font-weight="600" fill="#93C5FD" text-anchor="end">
    RESEARCH ROVER ARCHITECTURE
  </text>

  <!-- ================= TIER 1: FRONTEND UPLOAD & INTERACTION (y: 110) ================= -->
  <g transform="translate(40, 105)">
    <rect x="0" y="0" width="380" height="230" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="0" y="0" width="380" height="32" rx="8" fill="#142B65"/>
    <text x="190" y="21" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">
      1. CLIENT INTERACTION LAYER (React 18 + Vite)
    </text>

    <g transform="translate(15, 45)">
      <rect x="0" y="0" width="350" height="48" rx="6" fill="#F0F9FF" stroke="#BAE6FD" stroke-width="1"/>
      <text x="12" y="20" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#0369A1">CSV File Selector &amp; Dropzone</text>
      <text x="12" y="36" font-family="Arial, sans-serif" font-size="10" fill="#475569">Multipart/form-data upload via Axios client (api.ts)</text>

      <rect x="0" y="58" width="350" height="54" rx="6" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1"/>
      <text x="12" y="20" transform="translate(0, 58)" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#047857">DatasetFeatureReadinessBanner</text>
      <text x="12" y="36" transform="translate(0, 58)" font-family="Arial, sans-serif" font-size="10" fill="#475569">Inline pill in AnalyticsPage &amp; ChatPage (Score, Grade, Ready count)</text>

      <rect x="0" y="122" width="350" height="50" rx="6" fill="#FDF4FF" stroke="#F0ABFC" stroke-width="1"/>
      <text x="12" y="20" transform="translate(0, 122)" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#A21CAF">DatasetQualityModal</text>
      <text x="12" y="36" transform="translate(0, 122)" font-family="Arial, sans-serif" font-size="10" fill="#475569">3 Tabs: Quality &amp; Hygiene, Column Mappings, Feature Readiness</text>
    </g>
  </g>

  <!-- Flow Arrow from Tier 1 to Tier 2 -->
  <path d="M420 220 L470 220" stroke="#1E3A8A" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>
  <text x="445" y="210" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="#1E3A8A" text-anchor="middle">POST /upload</text>

  <!-- ================= TIER 2: FASTAPI BACKEND INGESTION CONTROLLER (y: 105) ================= -->
  <g transform="translate(470, 105)">
    <rect x="0" y="0" width="340" height="230" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="0" y="0" width="340" height="32" rx="8" fill="#1E3A8A"/>
    <text x="170" y="21" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">
      2. INGESTION CONTROLLER (FastAPI)
    </text>

    <g transform="translate(15, 45)">
      <rect x="0" y="0" width="310" height="48" rx="6" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
      <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#1E293B">Extension &amp; Size Guard</text>
      <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="#64748B">Validates .csv suffix, enforces 50 MB payload cap</text>

      <rect x="0" y="58" width="310" height="48" rx="6" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
      <text x="10" y="18" transform="translate(0, 58)" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#1E293B">Original CSV Storage</text>
      <text x="10" y="34" transform="translate(0, 58)" font-family="Arial, sans-serif" font-size="10" fill="#64748B">Writes raw byte stream to data/&lt;filename&gt;.csv (zero loss)</text>

      <rect x="0" y="122" width="310" height="50" rx="6" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
      <text x="10" y="18" transform="translate(0, 122)" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#1E293B">Encoding &amp; Dialect Detection</text>
      <text x="10" y="34" transform="translate(0, 122)" font-family="Arial, sans-serif" font-size="10" fill="#64748B">Multi-encoding fallback (utf-8, utf-8-sig, latin-1, cp1252)</text>
    </g>
  </g>

  <!-- Flow Arrow from Tier 2 to Tier 3 -->
  <path d="M810 220 L860 220" stroke="#1E3A8A" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>

  <!-- ================= TIER 3: CANONICAL NORMALIZER & QUALITY ASSESSOR (y: 105) ================= -->
  <g transform="translate(860, 105)">
    <rect x="0" y="0" width="700" height="230" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="0" y="0" width="700" height="32" rx="8" fill="#142B65"/>
    <text x="350" y="21" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">
      3. CORE NORMALIZATION &amp; QUALITY LAYER (Newly Developed)
    </text>

    <!-- Sub-Box A: DatasetNormalizer -->
    <g transform="translate(15, 45)">
      <rect x="0" y="0" width="325" height="170" rx="6" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1.2"/>
      <rect x="0" y="0" width="325" height="26" rx="6" fill="#059669"/>
      <text x="162" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">
        DatasetNormalizer (dataset_normalizer.py)
      </text>
      <text x="12" y="46" font-family="Arial, sans-serif" font-size="10" font-weight="600" fill="#065F46">• 20-Field Canonical Paper Schema</text>
      <text x="12" y="64" font-family="Arial, sans-serif" font-size="10" fill="#1E293B">• Multi-Source Alias Dictionary (PubMed, Scopus, WoS, OpenAlex)</text>
      <text x="12" y="82" font-family="Arial, sans-serif" font-size="10" fill="#1E293B">• Normalized Token &amp; Levenshtein Fuzzy Match (&gt;0.85)</text>
      <text x="12" y="100" font-family="Arial, sans-serif" font-size="10" fill="#1E293B">• Multi-Pass Paper Deduplication (DOI strip + Title hash)</text>
      <text x="12" y="118" font-family="Arial, sans-serif" font-size="10" fill="#1E293B">• Non-Destructive Raw Data Preservation in raw_data dict</text>
      <text x="12" y="136" font-family="Arial, sans-serif" font-size="10" fill="#1E293B">• Conflicting Scalar Mappings Capture (zero silent data loss)</text>
      <text x="12" y="154" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="#059669">Output: List[CanonicalPaperRecord], NormalizationReport</text>
    </g>

    <!-- Sub-Box B: DatasetQualityAssessor -->
    <g transform="translate(355, 45)">
      <rect x="0" y="0" width="330" height="170" rx="6" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1.2"/>
      <rect x="0" y="0" width="330" height="26" rx="6" fill="#2563EB"/>
      <text x="165" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">
        DatasetQualityAssessor (dataset_quality.py)
      </text>
      <text x="12" y="46" font-family="Arial, sans-serif" font-size="10" font-weight="600" fill="#1E40AF">• Overall Quality Score (0–100 Scale)</text>
      <text x="12" y="64" font-family="Arial, sans-serif" font-size="10" fill="#1E293B">• Weighted Formula: Title 25, Abstract 20, Keywords 15, ...</text>
      <text x="12" y="82" font-family="Arial, sans-serif" font-size="10" fill="#1E293B">• Duplicate Penalty (up to -10) &amp; Malformed Penalty (up to -5)</text>
      <text x="12" y="100" font-family="Arial, sans-serif" font-size="10" fill="#1E293B">• Small Sample Damping (min(1.0, N/5.0))</text>
      <text x="12" y="118" font-family="Arial, sans-serif" font-size="10" fill="#1E293B">• Seven-Feature Readiness Evaluation (Ready / Partial / Not Ready)</text>
      <text x="12" y="136" font-family="Arial, sans-serif" font-size="10" fill="#1E293B">• Field-Level Population Statistics &amp; Hygiene Warnings</text>
      <text x="12" y="154" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="#2563EB">Output: DatasetQualityReport (Score, Grade, Readiness)</text>
    </g>
  </g>

  <!-- Flow Arrow from Tier 3 to Tier 4 -->
  <path d="M1210 335 L1210 380" stroke="#1E3A8A" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>
  <text x="1225" y="360" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="#1E3A8A">Persist Metadata Sidecar</text>

  <!-- ================= TIER 4: PERSISTENCE & CANONICAL LOADER (y: 380) ================= -->
  <g transform="translate(470, 380)">
    <rect x="0" y="0" width="1090" height="190" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="0" y="0" width="1090" height="32" rx="8" fill="#047857"/>
    <text x="545" y="21" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">
      4. CANONICAL DATA LOADER &amp; UNIFIED STORAGE LAYER (canonical_loader.py)
    </text>

    <!-- Sidecar File Info -->
    <g transform="translate(20, 48)">
      <rect x="0" y="0" width="480" height="125" rx="6" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
      <text x="12" y="20" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#0F172A">Metadata Sidecar JSON (data/&lt;name&gt;_canonical_metadata.json)</text>
      <text x="12" y="38" font-family="Arial, sans-serif" font-size="10" fill="#475569">• Stores complete NormalizationReport and DatasetQualityReport</text>
      <text x="12" y="54" font-family="Arial, sans-serif" font-size="10" fill="#475569">• Caches mapped column names, confidence levels, and unmapped columns</text>
      <text x="12" y="70" font-family="Arial, sans-serif" font-size="10" fill="#475569">• Preserves duplicate record flags (is_duplicate: True) for filtering</text>
      <text x="12" y="86" font-family="Arial, sans-serif" font-size="10" fill="#475569">• Enables instantaneous O(1) quality retrieval via GET /files/{filename}/quality</text>
      <text x="12" y="104" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="#059669">✓ Prevents redundant re-normalization on downstream access</text>
    </g>

    <!-- Loader Dispatch Info -->
    <g transform="translate(520, 48)">
      <rect x="0" y="0" width="550" height="125" rx="6" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
      <text x="12" y="20" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#065F46">CanonicalDataLoader Downstream Service Dispatch</text>
      <text x="12" y="38" font-family="Arial, sans-serif" font-size="10" fill="#1E293B">• <tspan font-weight="700">load_canonical_dataframe(exclude_duplicates=True):</tspan> Filtered dataset for analytics</text>
      <text x="12" y="54" font-family="Arial, sans-serif" font-size="10" fill="#1E293B">• <tspan font-weight="700">load_canonical_dataframe(exclude_duplicates=False):</tspan> Complete paper catalogue</text>
      <text x="12" y="70" font-family="Arial, sans-serif" font-size="10" fill="#1E293B">• <tspan font-weight="700">apply_index_status_overlay():</tspan> Dynamic overlay of FAISS runtime availability</text>
      <text x="12" y="86" font-family="Arial, sans-serif" font-size="10" fill="#1E293B">• <tspan font-weight="700">Backward Compatibility:</tspan> Falls back transparently for legacy un-normalized CSVs</text>
      <text x="12" y="104" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="#047857">✓ Single source of truth across all 6 downstream research services</text>
    </g>
  </g>

  <!-- Flow Arrows from Tier 4 to Downstream Services (Tier 5) -->
  <path d="M1015 570 L1015 620" stroke="#059669" stroke-width="2.5" fill="none" marker-end="url(#arrow-green)"/>
  <text x="1025" y="598" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="#059669">Normalized Data Dispatch</text>

  <!-- ================= TIER 5: DOWNSTREAM RESEARCH ROVER SERVICES (y: 620) ================= -->
  <g transform="translate(40, 620)">
    <rect x="0" y="0" width="1520" height="290" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="0" y="0" width="1520" height="32" rx="8" fill="#142B65"/>
    <text x="760" y="21" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">
      5. CONSUMING RESEARCH ROVER SERVICES &amp; ANALYTICAL ENGINES (Refactored for Ingestion)
    </text>

    <!-- 5 Consuming Services Boxes (width: 285 each) -->
    <!-- Service 1: AnalysisService -->
    <g transform="translate(18, 48)">
      <rect x="0" y="0" width="285" height="225" rx="6" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
      <rect x="0" y="0" width="285" height="26" rx="6" fill="#1E3A8A"/>
      <text x="142" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">AnalysisService</text>
      <text x="12" y="44" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="#1E3A8A">Keywords &amp; Centrality</text>
      <text x="12" y="62" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• Calls CanonicalDataLoader</text>
      <text x="12" y="78" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• exclude_duplicates = True</text>
      <text x="12" y="94" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• Keyword frequency tables</text>
      <text x="12" y="110" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• Co-occurrence presence matrix</text>
      <text x="12" y="126" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• NetworkX graph centralities</text>
      <text x="12" y="142" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• Degree, betweenness, closeness</text>
      <text x="12" y="166" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#059669">✓ Operates on canonical 'keywords'</text>
      <text x="12" y="182" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">and deduplicated paper records</text>
    </g>

    <!-- Service 2: SearchService -->
    <g transform="translate(320, 48)">
      <rect x="0" y="0" width="285" height="225" rx="6" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
      <rect x="0" y="0" width="285" height="26" rx="6" fill="#1E3A8A"/>
      <text x="142" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">SearchService &amp; FilesRoute</text>
      <text x="12" y="44" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="#1E3A8A">Paper Listing &amp; Catalog</text>
      <text x="12" y="62" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• GET /files/csv/{name}/data</text>
      <text x="12" y="78" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• GET /files/csv/{name}/paginated</text>
      <text x="12" y="94" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• exclude_duplicates = False</text>
      <text x="12" y="110" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• Preserves full record audit trail</text>
      <text x="12" y="126" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• Injects is_duplicate &amp; paper_id</text>
      <text x="12" y="142" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• Downstream card rendering</text>
      <text x="12" y="166" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#059669">✓ Users see full original rows</text>
      <text x="12" y="182" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">with duplicate badge metadata</text>
    </g>

    <!-- Service 3: CountryService -->
    <g transform="translate(622, 48)">
      <rect x="0" y="0" width="285" height="225" rx="6" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
      <rect x="0" y="0" width="285" height="26" rx="6" fill="#1E3A8A"/>
      <text x="142" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">CountryService</text>
      <text x="12" y="44" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="#1E3A8A">Affiliations &amp; Collaboration</text>
      <text x="12" y="62" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• Reads canonical 'affiliations'</text>
      <text x="12" y="78" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• Uses pre-extracted 'countries'</text>
      <text x="12" y="94" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• exclude_duplicates = True</text>
      <text x="12" y="110" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• Resolves ISO-3 country codes</text>
      <text x="12" y="126" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• Country frequency distribution</text>
      <text x="12" y="142" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• International collaboration links</text>
      <text x="12" y="166" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#059669">✓ Prevents country overcounting</text>
      <text x="12" y="182" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">from duplicate paper entries</text>
    </g>

    <!-- Service 4: EmbeddingService -->
    <g transform="translate(924, 48)">
      <rect x="0" y="0" width="285" height="225" rx="6" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
      <rect x="0" y="0" width="285" height="26" rx="6" fill="#1E3A8A"/>
      <text x="142" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">EmbeddingService &amp; FAISS</text>
      <text x="12" y="44" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="#1E3A8A">Vector Index Construction</text>
      <text x="12" y="62" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• Reads deduplicated records</text>
      <text x="12" y="78" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• Full-text extraction / scrape</text>
      <text x="12" y="94" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• Abstract fallback if paywalled</text>
      <text x="12" y="110" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• HDBSCAN semantic chunking</text>
      <text x="12" y="126" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• Sentence-Transformers 768-d</text>
      <text x="12" y="142" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• FAISS IndexFlatL2 .index</text>
      <text x="12" y="166" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#059669">✓ Embeddings triggered explicitly</text>
      <text x="12" y="182" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">by user (not auto on upload)</text>
    </g>

    <!-- Service 5: ChatService -->
    <g transform="translate(1226, 48)">
      <rect x="0" y="0" width="276" height="225" rx="6" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
      <rect x="0" y="0" width="276" height="26" rx="6" fill="#1E3A8A"/>
      <text x="138" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">ChatService &amp; RAG</text>
      <text x="12" y="44" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="#1E3A8A">Conversational QA Assistant</text>
      <text x="12" y="62" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• Multi-query decomposition</text>
      <text x="12" y="78" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• FAISS cosine search retrieval</text>
      <text x="12" y="94" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• Dynamic index check</text>
      <text x="12" y="110" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• If index missing: fallback to</text>
      <text x="12" y="126" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">  general Gemini response</text>
      <text x="12" y="142" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">• Citations [n] with DOI links</text>
      <text x="12" y="166" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#059669">✓ Consistent readiness warnings</text>
      <text x="12" y="182" font-family="Arial, sans-serif" font-size="9.5" fill="#475569">displayed in Quality Modal</text>
    </g>
  </g>
</svg>"""

# ---------------------------------------------------------------------------
# FIGURE 2: DATASET INGESTION & QUALITY EVALUATION SEQUENCE WORKFLOW
# ---------------------------------------------------------------------------
def build_fig_2_workflow() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" width="1600" height="900">
  <defs>
    <filter id="shadow2" x="-5%" y="-5%" width="110%" height="115%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.12"/>
    </filter>
    <marker id="seq-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1E3A8A"/>
    </marker>
    <marker id="resp-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1600" height="900" fill="#F8FAFC"/>

  <!-- Top Title -->
  <rect x="40" y="25" width="1520" height="50" rx="6" fill="#142B65" />
  <text x="60" y="56" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="#FFFFFF">
    Figure 4.2: End-to-End Dataset Ingestion, Quality Assessment &amp; Downstream Dispatch Workflow
  </text>
  <text x="1530" y="56" font-family="Arial, sans-serif" font-size="12" font-weight="600" fill="#93C5FD" text-anchor="end">
    SEQUENCE &amp; DATAFLOW MODEL
  </text>

  <!-- 5 Sequence Lifelines -->
  <!-- Lifeline 1: User / Browser -->
  <g transform="translate(140, 100)">
    <rect x="-80" y="0" width="160" height="40" rx="6" fill="#1E3A8A"/>
    <text x="0" y="25" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">User / Browser</text>
    <line x1="0" y1="40" x2="0" y2="760" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="4,4"/>
  </g>

  <!-- Lifeline 2: Files Route (FastAPI) -->
  <g transform="translate(440, 100)">
    <rect x="-90" y="0" width="180" height="40" rx="6" fill="#1E3A8A"/>
    <text x="0" y="25" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">POST /files/upload</text>
    <line x1="0" y1="40" x2="0" y2="760" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="4,4"/>
  </g>

  <!-- Lifeline 3: DatasetNormalizer -->
  <g transform="translate(740, 100)">
    <rect x="-100" y="0" width="200" height="40" rx="6" fill="#059669"/>
    <text x="0" y="25" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">DatasetNormalizer</text>
    <line x1="0" y1="40" x2="0" y2="760" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="4,4"/>
  </g>

  <!-- Lifeline 4: QualityAssessor -->
  <g transform="translate(1040, 100)">
    <rect x="-100" y="0" width="200" height="40" rx="6" fill="#2563EB"/>
    <text x="0" y="25" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">QualityAssessor</text>
    <line x1="0" y1="40" x2="0" y2="760" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="4,4"/>
  </g>

  <!-- Lifeline 5: CanonicalDataLoader & Storage -->
  <g transform="translate(1360, 100)">
    <rect x="-110" y="0" width="220" height="40" rx="6" fill="#047857"/>
    <text x="0" y="25" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">CanonicalDataLoader</text>
    <line x1="0" y1="40" x2="0" y2="760" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="4,4"/>
  </g>

  <!-- ================= SEQUENCE INTERACTIONS ================= -->
  <!-- Step 1: Upload Action (y: 170) -->
  <g transform="translate(0, 160)">
    <line x1="140" y1="0" x2="440" y2="0" stroke="#1E3A8A" stroke-width="2" marker-end="url(#seq-arrow)"/>
    <rect x="180" y="-18" width="220" height="24" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
    <text x="290" y="-2" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="#1E3A8A" text-anchor="middle">
      1. Upload CSV file (multipart/form-data)
    </text>
  </g>

  <!-- Step 2: Validate & Store Raw (y: 215) -->
  <g transform="translate(440, 205)">
    <rect x="0" y="0" width="220" height="34" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
    <text x="10" y="15" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#1E293B">2. Validate size &lt;= 50MB &amp; extension</text>
    <text x="10" y="28" font-family="Arial, sans-serif" font-size="9.5" fill="#64748B">Write raw data/&lt;filename&gt;.csv</text>
  </g>

  <!-- Step 3: Trigger Normalization (y: 270) -->
  <g transform="translate(0, 260)">
    <line x1="440" y1="0" x2="740" y2="0" stroke="#1E3A8A" stroke-width="2" marker-end="url(#seq-arrow)"/>
    <rect x="490" y="-18" width="200" height="24" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
    <text x="590" y="-2" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="#1E3A8A" text-anchor="middle">
      3. normalize_dataframe(df)
    </text>
  </g>

  <!-- Step 4: Normalizer Execution Box (y: 300) -->
  <g transform="translate(740, 290)">
    <rect x="-15" y="0" width="240" height="80" rx="4" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1"/>
    <text x="0" y="16" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#065F46">4. Normalizer Processing:</text>
    <text x="0" y="32" font-family="Arial, sans-serif" font-size="9" fill="#1E293B">• Header sanitization &amp; alias lookup</text>
    <text x="0" y="46" font-family="Arial, sans-serif" font-size="9" fill="#1E293B">• Fuzzy matching (&gt;0.85 threshold)</text>
    <text x="0" y="60" font-family="Arial, sans-serif" font-size="9" fill="#1E293B">• DOI clean &amp; duplicate detection</text>
    <text x="0" y="74" font-family="Arial, sans-serif" font-size="9" fill="#1E293B">• Canonical records &amp; mapping report</text>
  </g>

  <!-- Step 5: Trigger Quality Assessment (y: 395) -->
  <g transform="translate(0, 395)">
    <line x1="740" y1="0" x2="1040" y2="0" stroke="#1E3A8A" stroke-width="2" marker-end="url(#seq-arrow)"/>
    <rect x="790" y="-18" width="200" height="24" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
    <text x="890" y="-2" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="#1E3A8A" text-anchor="middle">
      5. assess(records, norm_report)
    </text>
  </g>

  <!-- Step 6: Quality Assessor Processing (y: 425) -->
  <g transform="translate(1040, 420)">
    <rect x="-15" y="0" width="240" height="80" rx="4" fill="#EFF6FF" stroke="#93C5FD" stroke-width="1"/>
    <text x="0" y="16" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#1E40AF">6. Quality Assessor Processing:</text>
    <text x="0" y="32" font-family="Arial, sans-serif" font-size="9" fill="#1E293B">• Weighted completeness score (0–100)</text>
    <text x="0" y="46" font-family="Arial, sans-serif" font-size="9" fill="#1E293B">• Duplicate &amp; invalid value penalties</text>
    <text x="0" y="60" font-family="Arial, sans-serif" font-size="9" fill="#1E293B">• Small-sample damping factor</text>
    <text x="0" y="74" font-family="Arial, sans-serif" font-size="9" fill="#1E293B">• 7-feature readiness status &amp; warnings</text>
  </g>

  <!-- Step 7: Pass to CanonicalLoader & Persist (y: 525) -->
  <g transform="translate(0, 525)">
    <line x1="1040" y1="0" x2="1360" y2="0" stroke="#1E3A8A" stroke-width="2" marker-end="url(#seq-arrow)"/>
    <rect x="1110" y="-18" width="220" height="24" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
    <text x="1220" y="-2" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="#1E3A8A" text-anchor="middle">
      7. process_and_save_canonical()
    </text>
  </g>

  <!-- Step 8: Persistence Box (y: 550) -->
  <g transform="translate(1360, 550)">
    <rect x="-15" y="0" width="240" height="85" rx="4" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1"/>
    <text x="0" y="16" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#047857">8. Storage &amp; Runtime Overlay:</text>
    <text x="0" y="32" font-family="Arial, sans-serif" font-size="9" fill="#1E293B">• Save &lt;name&gt;_canonical_metadata.json</text>
    <text x="0" y="46" font-family="Arial, sans-serif" font-size="9" fill="#1E293B">• Check if FAISS index exists</text>
    <text x="0" y="60" font-family="Arial, sans-serif" font-size="9" fill="#1E293B">• Overlay vector status on RAG features</text>
    <text x="0" y="76" font-family="Arial, sans-serif" font-size="9" font-weight="700" fill="#047857">• Downgrade to partially_ready if no index</text>
  </g>

  <!-- Step 9: Return Extended Upload Response (y: 660) -->
  <g transform="translate(0, 660)">
    <line x1="1360" y1="0" x2="440" y2="0" stroke="#059669" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#resp-arrow)"/>
    <rect x="800" y="-18" width="220" height="24" rx="4" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1"/>
    <text x="910" y="-2" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="#059669" text-anchor="middle">
      9. ExtendedFileUploadResponse
    </text>
  </g>

  <!-- Step 10: Deliver to Client & Open Modal (y: 710) -->
  <g transform="translate(0, 710)">
    <line x1="440" y1="0" x2="140" y2="0" stroke="#059669" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#resp-arrow)"/>
    <rect x="210" y="-18" width="200" height="24" rx="4" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1"/>
    <text x="310" y="-2" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="#059669" text-anchor="middle">
      10. HTTP 200 + Auto-Open Modal
    </text>
  </g>

  <!-- Step 11: Client UI Update Box (y: 745) -->
  <g transform="translate(140, 740)">
    <rect x="-80" y="0" width="260" height="55" rx="4" fill="#FDF4FF" stroke="#F0ABFC" stroke-width="1"/>
    <text x="0" y="16" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#A21CAF">11. Frontend State Resolution:</text>
    <text x="0" y="32" font-family="Arial, sans-serif" font-size="9" fill="#1E293B">• Auto-select uploaded file in dropdowns</text>
    <text x="0" y="46" font-family="Arial, sans-serif" font-size="9" fill="#1E293B">• Display DatasetQualityModal with 3 tabs</text>
  </g>
</svg>"""

# ---------------------------------------------------------------------------
# FIGURE 3: BEFORE-VERSUS-AFTER PARADIGM COMPARISON
# ---------------------------------------------------------------------------
def build_fig_3_comparison() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 850" width="1600" height="850">
  <defs>
    <filter id="shadow3" x="-5%" y="-5%" width="110%" height="115%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#0F172A" flood-opacity="0.1"/>
    </filter>
  </defs>

  <rect width="1600" height="850" fill="#F8FAFC"/>

  <!-- Top Title -->
  <rect x="40" y="25" width="1520" height="50" rx="6" fill="#142B65" />
  <text x="60" y="56" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="#FFFFFF">
    Figure 4.3: Architectural Paradigm Comparison: Pre-existing Ingestion vs. Universal Ingestion System
  </text>
  <text x="1530" y="56" font-family="Arial, sans-serif" font-size="12" font-weight="600" fill="#93C5FD" text-anchor="end">
    BEFORE VS. AFTER ARCHITECTURAL AUDIT
  </text>

  <!-- LEFT BOX: PRE-EXISTING SYSTEM (y: 100, width: 730) -->
  <g transform="translate(40, 100)">
    <rect x="0" y="0" width="730" height="710" rx="8" fill="#FFF1F2" stroke="#FECDD3" stroke-width="1.5" filter="url(#shadow3)"/>
    <rect x="0" y="0" width="730" height="38" rx="8" fill="#BE123C"/>
    <text x="365" y="25" font-family="Arial, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF" text-anchor="middle">
      PRE-EXISTING RESEARCH ROVER INGESTION (Identified Limitations)
    </text>

    <!-- Content Items -->
    <g transform="translate(25, 60)">
      <!-- Item 1 -->
      <rect x="0" y="0" width="680" height="90" rx="6" fill="#FFFFFF" stroke="#FDA4AF" stroke-width="1"/>
      <text x="15" y="22" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#9F1239">
        1. Hardcoded PubMed/Rover Schema Dependency
      </text>
      <text x="15" y="44" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Expected exact headers: 'Title', 'Abstract', 'Authors', 'DOI', 'Keywords', 'Publication Year'.
      </text>
      <text x="15" y="62" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Scopus exports ('Document Title', 'Abstract', 'Author Keywords') failed or lost fields.
      </text>
      <text x="15" y="80" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Web of Science and OpenAlex exports could not be parsed without manual editing.
      </text>

      <!-- Item 2 -->
      <rect x="0" y="105" width="680" height="90" rx="6" fill="#FFFFFF" stroke="#FDA4AF" stroke-width="1"/>
      <text x="15" y="22" transform="translate(0, 105)" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#9F1239">
        2. Silent Data Loss &amp; Header Fragility
      </text>
      <text x="15" y="44" transform="translate(0, 105)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Minor capitalization differences ('Doi' vs 'DOI') caused silent dropped fields.
      </text>
      <text x="15" y="62" transform="translate(0, 105)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Custom metadata columns outside the fixed set were discarded during ingestion.
      </text>
      <text x="15" y="80" transform="translate(0, 105)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • No record was maintained of which columns were recognized vs unmapped.
      </text>

      <!-- Item 3 -->
      <rect x="0" y="210" width="680" height="90" rx="6" fill="#FFFFFF" stroke="#FDA4AF" stroke-width="1"/>
      <text x="15" y="22" transform="translate(0, 210)" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#9F1239">
        3. Undetected Duplicate Paper Records
      </text>
      <text x="15" y="44" transform="translate(0, 210)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Duplicate papers across multi-query merges were double-counted in keyword frequency.
      </text>
      <text x="15" y="62" transform="translate(0, 210)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Skewed NetworkX centrality metrics and country collaboration counts.
      </text>
      <text x="15" y="80" transform="translate(0, 210)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Vector embeddings indexed identical chunks multiple times, wasting FAISS memory.
      </text>

      <!-- Item 4 -->
      <rect x="0" y="315" width="680" height="90" rx="6" fill="#FFFFFF" stroke="#FDA4AF" stroke-width="1"/>
      <text x="15" y="22" transform="translate(0, 315)" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#9F1239">
        4. Complete Absence of Quality Assessment
      </text>
      <text x="15" y="44" transform="translate(0, 315)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • No systematic verification of missing abstracts, malformed years, or empty fields.
      </text>
      <text x="15" y="62" transform="translate(0, 315)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • A dataset with 90% missing abstracts was accepted with HTTP 200 without warning.
      </text>
      <text x="15" y="80" transform="translate(0, 315)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • No metric to inform researchers whether data was suitable for analysis.
      </text>

      <!-- Item 5 -->
      <rect x="0" y="420" width="680" height="90" rx="6" fill="#FFFFFF" stroke="#FDA4AF" stroke-width="1"/>
      <text x="15" y="22" transform="translate(0, 420)" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#9F1239">
        5. Opaque Feature Compatibility &amp; Runtime Failures
      </text>
      <text x="15" y="44" transform="translate(0, 420)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Users navigated to Analytics or Chat without knowing if required columns existed.
      </text>
      <text x="15" y="62" transform="translate(0, 420)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Attempting semantic search on a dataset without an index failed silently.
      </text>
      <text x="15" y="80" transform="translate(0, 420)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • No visual status banner or pre-flight readiness checks.
      </text>

      <!-- Bottom Summary Box -->
      <rect x="0" y="525" width="680" height="95" rx="6" fill="#FFE4E6" stroke="#FDA4AF" stroke-width="1"/>
      <text x="15" y="24" transform="translate(0, 525)" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#9F1239">
        Summary of Consequences:
      </text>
      <text x="15" y="46" transform="translate(0, 525)" font-family="Arial, sans-serif" font-size="10.5" fill="#881337">
        Researchers were forced to write bespoke Python preprocessing scripts for non-PubMed CSVs.
      </text>
      <text x="15" y="64" transform="translate(0, 525)" font-family="Arial, sans-serif" font-size="10.5" fill="#881337">
        Corrupted or incomplete datasets led to unexplained downstream crashes in analytics and chat.
      </text>
    </g>
  </g>

  <!-- RIGHT BOX: NEW PROPOSED UNIVERSAL INGESTION SYSTEM (y: 100, width: 730) -->
  <g transform="translate(830, 100)">
    <rect x="0" y="0" width="730" height="710" rx="8" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1.5" filter="url(#shadow3)"/>
    <rect x="0" y="0" width="730" height="38" rx="8" fill="#047857"/>
    <text x="365" y="25" font-family="Arial, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF" text-anchor="middle">
      PROPOSED UNIVERSAL DATASET INGESTION SYSTEM (Implemented Solution)
    </text>

    <!-- Content Items -->
    <g transform="translate(25, 60)">
      <!-- Item 1 -->
      <rect x="0" y="0" width="680" height="90" rx="6" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1"/>
      <text x="15" y="22" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#065F46">
        1. 20-Field Canonical Representation &amp; Multi-Source Matching
      </text>
      <text x="15" y="44" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Universal schema maps PubMed, Scopus, Web of Science, and OpenAlex.
      </text>
      <text x="15" y="62" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Exact alias matching, normalized tokens, and Levenshtein fuzzy matching (&gt;0.85).
      </text>
      <text x="15" y="80" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Automatic encoding resolution (UTF-8, UTF-8-SIG, Latin-1, CP1252).
      </text>

      <!-- Item 2 -->
      <rect x="0" y="105" width="680" height="90" rx="6" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1"/>
      <text x="15" y="22" transform="translate(0, 105)" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#065F46">
        2. Non-Destructive Ingestion &amp; Metadata Sidecar
      </text>
      <text x="15" y="44" transform="translate(0, 105)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Original CSV preserved byte-for-byte in data/&lt;filename&gt;.csv.
      </text>
      <text x="15" y="62" transform="translate(0, 105)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Unmapped and custom columns preserved in record-level raw_data dictionaries.
      </text>
      <text x="15" y="80" transform="translate(0, 105)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Conflicting column mappings reported and tracked without silent data loss.
      </text>

      <!-- Item 3 -->
      <rect x="0" y="210" width="680" height="90" rx="6" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1"/>
      <text x="15" y="22" transform="translate(0, 210)" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#065F46">
        3. Automated Deduplication &amp; Dual-Mode Consumption
      </text>
      <text x="15" y="44" transform="translate(0, 210)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Multi-pass duplicate identification: normalized DOI strip + normalized title hashing.
      </text>
      <text x="15" y="62" transform="translate(0, 210)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • CanonicalDataLoader allows services to select exclude_duplicates=True or False.
      </text>
      <text x="15" y="80" transform="translate(0, 210)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Analytics &amp; Country graphs filter duplicates; Catalogue listings preserve all records.
      </text>

      <!-- Item 4 -->
      <rect x="0" y="315" width="680" height="90" rx="6" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1"/>
      <text x="15" y="22" transform="translate(0, 315)" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#065F46">
        4. Multi-Attribute Quality Assessor (0–100 Score &amp; Grade)
      </text>
      <text x="15" y="44" transform="translate(0, 315)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Weighted completeness scoring across 7 dimensions (Title 25, Abstract 20, etc.).
      </text>
      <text x="15" y="62" transform="translate(0, 315)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Duplicate penalties (up to -10) and invalid format deductions (up to -5).
      </text>
      <text x="15" y="80" transform="translate(0, 315)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Assigned Grades: Excellent (90–100), Good (80–89), Fair, Poor, Critical.
      </text>

      <!-- Item 5 -->
      <rect x="0" y="420" width="680" height="90" rx="6" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1"/>
      <text x="15" y="22" transform="translate(0, 420)" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#065F46">
        5. Seven-Feature Readiness &amp; Dynamic Runtime Overlay
      </text>
      <text x="15" y="44" transform="translate(0, 420)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Pre-flight readiness checks for all 7 Research Rover features.
      </text>
      <text x="15" y="62" transform="translate(0, 420)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Statuses: Ready (Green), Partially Ready (Amber), Not Ready (Rose).
      </text>
      <text x="15" y="80" transform="translate(0, 420)" font-family="Arial, sans-serif" font-size="11" fill="#1E293B">
        • Dynamic FAISS index verification downgrades RAG chat to partially_ready if unindexed.
      </text>

      <!-- Bottom Summary Box -->
      <rect x="0" y="525" width="680" height="95" rx="6" fill="#D1FAE5" stroke="#86EFAC" stroke-width="1"/>
      <text x="15" y="24" transform="translate(0, 525)" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#065F46">
        Achieved System Impact:
      </text>
      <text x="15" y="46" transform="translate(0, 525)" font-family="Arial, sans-serif" font-size="10.5" fill="#064E3B">
        Seamless ingestion of multi-database CSVs with zero manual code modifications.
      </text>
      <text x="15" y="64" transform="translate(0, 525)" font-family="Arial, sans-serif" font-size="10.5" fill="#064E3B">
        Transparent, actionable quality metrics and feature badges guide researchers immediately upon upload.
      </text>
    </g>
  </g>
</svg>"""

def main():
    print("Building report figures...")
    
    # Figure 1
    svg_1 = build_fig_1_architecture()
    png_1_bytes = resvg_py.svg_to_bytes(svg_1)
    p1 = os.path.join(FIGURES_DIR, "figure_1_system_architecture.png")
    with open(p1, "wb") as f:
        f.write(png_1_bytes)
    print(f"Generated Figure 1 -> {p1} ({len(png_1_bytes)/1024:.1f} KB)")

    # Figure 2
    svg_2 = build_fig_2_workflow()
    png_2_bytes = resvg_py.svg_to_bytes(svg_2)
    p2 = os.path.join(FIGURES_DIR, "figure_2_ingestion_workflow.png")
    with open(p2, "wb") as f:
        f.write(png_2_bytes)
    print(f"Generated Figure 2 -> {p2} ({len(png_2_bytes)/1024:.1f} KB)")

    # Figure 3
    svg_3 = build_fig_3_comparison()
    png_3_bytes = resvg_py.svg_to_bytes(svg_3)
    p3 = os.path.join(FIGURES_DIR, "figure_3_before_after_comparison.png")
    with open(p3, "wb") as f:
        f.write(png_3_bytes)
    print(f"Generated Figure 3 -> {p3} ({len(png_3_bytes)/1024:.1f} KB)")

if __name__ == "__main__":
    main()
