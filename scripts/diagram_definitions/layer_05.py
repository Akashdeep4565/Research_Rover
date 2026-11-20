"""
Layer 5: Data Cleaning & Enrichment Layer
Covers identifier normalization, 4-priority deduplication, record merging,
affiliation fallback enrichment, ISO 3166-1 country extraction, encoding probing, and CSV storage.
"""

from .common import THEMES, get_svg_header, get_svg_footer
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

def get_mermaid():
    return """flowchart TD
    %% =========================================================================
    %% LAYER 5: DATA CLEANING & ENRICHMENT LAYER
    %% Project: Research Rover
    %% Focus: Identifier Normalization, Deduplication, Record Merging, Country Extraction & CSV Storage
    %% =========================================================================

    classDef startEnd fill:#ECFDF5,stroke:#059669,stroke-width:2.5px,color:#064E3B,font-weight:bold;
    classDef norm fill:#F8FAFC,stroke:#10B981,stroke-width:1.5px,color:#0F172A;
    classDef decision fill:#FEF3C7,stroke:#D97706,stroke-width:2px,color:#78350F,font-weight:bold;
    classDef mergeEngine fill:#EFF6FF,stroke:#2563EB,stroke-width:1.8px,color:#1E3A8A,font-weight:bold;
    classDef geoEngine fill:#FDF4FF,stroke:#C026D3,stroke-width:1.5px,color:#701A75;
    classDef storage fill:#F1F5F9,stroke:#64748B,stroke-width:1.8px,color:#0F172A;
    classDef output fill:#ECFDF5,stroke:#10B981,stroke-width:2px,color:#064E3B;

    DC_ENTRY(["5.0 Entry: Raw Candidate Paper Records<br/>(From Layer 4 APIs or User Uploaded CSV)"]):::startEnd

    %% ─── METADATA NORMALIZATION ──────────────────────────────────────────────
    subgraph SUB_NORM["IDENTIFIER NORMALIZATION & COMPOSITE KEY GENERATION"]
        N_DOI["5.1 normalize_doi(doi)<br/>Strips https://doi.org/ & dx.doi.org/ prefixes, lowercases, trims"]:::norm
        N_PMID["5.2 normalize_pmid(pmid)<br/>Strips URL prefixes, extracts numeric ID"]:::norm
        N_OA["5.3 normalize_openalex_id(id)<br/>Strips URI path, isolates alphanumeric ID"]:::norm
        N_KEY["5.4 compute_title_key(title, year, first_author)<br/>• Alphanumeric regex [^a-z0-9] on title (first 60 chars)<br/>• Normalizes 4-digit publication year<br/>• Normalizes first author surname (first 20 chars)<br/>• Output: title60_year_author20 collision-resistant key"]:::norm
    end

    %% ─── DEDUPLICATION ENGINE ────────────────────────────────────────────────
    subgraph SUB_DEDUP["4-PRIORITY DEDUPLICATION ENGINE (UnifiedSearchService.deduplicate_results)"]
        D_CHECK{"5.5 Check Record Match Across 4 Hash Indices"}:::decision
        
        MATCH_P1["Priority 1 Match: DOI in doi_index"]:::norm
        MATCH_P2["Priority 2 Match: PMID in pmid_index"]:::norm
        MATCH_P3["Priority 3 Match: OpenAlex ID in openalex_index"]:::norm
        MATCH_P4["Priority 4 Match: title_key in title_index"]:::norm
        
        D_MERGE["5.6 Record Merging (merge_paper_records)<br/>• Sources Union: e.g. ['pubmed', 'openalex'] → 'pubmed, openalex'<br/>• Authors Union: deduplicated list preserving original order<br/>• Affiliations Union: semicolon-delimited unique strings<br/>• Title & Abstract: selects longer, more informative text<br/>• Citation Count: max(c1, c2)<br/>• Direct PDF: prioritizes direct .pdf over landing page (_pdf_priority)<br/>• Updates all 4 hash lookup indices with merged record"]:::mergeEngine
        
        D_NEW["5.7 Register New Unique Record<br/>Appends to unique_list, populates normalized source tags, registers in indices"]:::norm
    end

    %% ─── AFFILIATION ENRICHMENT ──────────────────────────────────────────────
    subgraph SUB_AFFILIATION["AFFILIATION FALLBACK ENRICHMENT (pubmed_affiliation_enricher.py)"]
        AFF_CHECK{"5.8 Affiliations Missing in PubMed Records?"}:::decision
        AFF_BATCH["5.9 Batch EFetch XML Enrichment<br/>• Batches PMIDs in chunks of 50<br/>• Queries efetch.fcgi with retmode=xml<br/>• Parses &lt;AffiliationInfo/Affiliation&gt; nodes<br/>• Populates Affiliations column"]:::norm
    end

    %% ─── GEOGRAPHIC RECOGNITION ──────────────────────────────────────────────
    subgraph SUB_GEO["GEOGRAPHIC ENTITY EXTRACTION & NORMALIZATION (country_extractor.py)"]
        GEO_EXTRACT["5.10 extract_countries_from_affiliations(text)<br/>• Checks COUNTRY_ALIASES dictionary (700+ canonical mappings)<br/>• Resolves acronyms (usa, uk, prc, rok, uae) & native names (deutschland, bharat)<br/>• Word boundary regex \\b eliminates false positives (e.g. Iran in Uranium)<br/>• get_country_iso3: resolves canonical name to ISO-3166-1 alpha-3 code<br/>• Emits sorted deduplicated canonical country list per paper"]:::geoEngine
    end

    %% ─── CSV FILE OPERATIONS ─────────────────────────────────────────────────
    subgraph SUB_CSV["CENTRALIZED CSV LOADER & STORAGE ENGINE (utils/csv_loader.py)"]
        CSV_BOM["5.11 Byte-Order Mark Detection (check_bom)<br/>Detects UTF-8-BOM, UTF-16-LE, UTF-16-BE, UTF-32"]:::storage
        CSV_ENC["5.12 Encoding Probing (detect_csv_encoding)<br/>Probes: UTF-8 → UTF-8-SIG → CP1252 → ISO-8859-1 → Latin-1 → chardet"]:::storage
        CSV_STORE[("5.13 Persistent Local CSV Storage<br/>data/<sanitized_query>.csv (UTF-8-SIG)<br/>Standard Schema: Title, DOI, PMID, OpenAlex_ID, Abstract,<br/>Source, Year, Authors, Affiliations, Countries, Citation_Count, PDF_URL")]:::storage
    end

    DC_FINAL(["5.14 Exit: Clean, Structured Dataset Ready for Analysis (Layer 6)"]):::startEnd

    %% Connections
    DC_ENTRY --> N_DOI & N_PMID & N_OA & N_KEY --> D_CHECK
    D_CHECK -->|P1 Match| MATCH_P1 --> D_MERGE
    D_CHECK -->|P2 Match| MATCH_P2 --> D_MERGE
    D_CHECK -->|P3 Match| MATCH_P3 --> D_MERGE
    D_CHECK -->|P4 Match| MATCH_P4 --> D_MERGE
    D_CHECK -->|No Match| D_NEW

    D_MERGE --> AFF_CHECK
    D_NEW --> AFF_CHECK

    AFF_CHECK -->|Missing| AFF_BATCH --> GEO_EXTRACT
    AFF_CHECK -->|Present| GEO_EXTRACT

    GEO_EXTRACT --> CSV_BOM --> CSV_ENC --> CSV_STORE --> DC_FINAL
"""

def get_svg():
    w, h = 1750, 1250
    header = get_svg_header(
        w, h,
        title="Layer 5: Data Cleaning & Enrichment Layer Flowchart",
        subtitle="Identifier Normalization, 4-Priority Deduplication, Record Merging, ISO 3166-1 Country Extraction & CSV Storage",
        layer_badge="LAYER 05",
        theme_key="layer_05"
    )

    content = '''
  <!-- Inter-layer Connectivity Cards -->
  <g transform="translate(45, 115)">
    <rect x="0" y="0" width="380" height="42" rx="8" fill="#ecfeff" stroke="#0891b2" stroke-width="1.5"/>
    <text x="15" y="26" font-size="12" font-weight="bold" fill="#155e75">INPUT SOURCE:</text>
    <text x="120" y="26" font-size="12" fill="#334155">Layer 4: Raw Paper Records or Uploaded CSV</text>
  </g>
  <g transform="translate(1325, 115)">
    <rect x="0" y="0" width="380" height="42" rx="8" fill="#fffbeb" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="15" y="26" font-size="12" font-weight="bold" fill="#92400e">OUTPUT TARGET:</text>
    <text x="130" y="26" font-size="12" fill="#334155">Layer 6 (Analysis &amp; Computation Engines)</text>
  </g>

  <!-- Left: Identifier Normalization & Key Formulation -->
  <g transform="translate(45, 175)">
    <rect x="0" y="0" width="480" height="970" rx="14" fill="#fafafa" stroke="#059669" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="450" height="34" rx="6" fill="#d1fae5"/>
    <text x="240" y="37" font-size="13" font-weight="bold" fill="#065f46" text-anchor="middle">METADATA &amp; IDENTIFIER NORMALIZATION</text>

    <!-- DOI Normalization -->
    <rect x="20" y="65" width="440" height="90" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="90" font-size="11.5" font-weight="bold" fill="#0f172a">5.1 DOI Normalization (normalize_doi)</text>
    <text x="35" y="110" font-size="9.5" fill="#475569">• Strips http://dx.doi.org/ and https://doi.org/ prefixes via regex</text>
    <text x="35" y="126" font-size="9.5" fill="#475569">• Strips whitespace, converts to lowercase string</text>
    <text x="35" y="142" font-size="9.5" fill="#475569">• Output: clean raw DOI string (e.g. 10.1016/j.cell.2023.01.002)</text>

    <!-- PMID Normalization -->
    <rect x="20" y="170" width="440" height="85" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="195" font-size="11.5" font-weight="bold" fill="#0f172a">5.2 PMID Normalization (normalize_pmid)</text>
    <text x="35" y="215" font-size="9.5" fill="#475569">• Strips URL paths (e.g. pubmed.ncbi.nlm.nih.gov/38291024)</text>
    <text x="35" y="231" font-size="9.5" fill="#475569">• Extracts clean numeric string digits</text>
    <text x="35" y="247" font-size="9.5" fill="#475569">• Output: isolated numeric PMID (e.g. 38291024)</text>

    <!-- OpenAlex ID Normalization -->
    <rect x="20" y="270" width="440" height="85" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="295" font-size="11.5" font-weight="bold" fill="#0f172a">5.3 OpenAlex ID Normalization (normalize_openalex_id)</text>
    <text x="35" y="315" font-size="9.5" fill="#475569">• Strips URL prefixes (e.g. https://openalex.org/W2741809807)</text>
    <text x="35" y="331" font-size="9.5" fill="#475569">• Isolates canonical OpenAlex identifier</text>
    <text x="35" y="347" font-size="9.5" fill="#475569">• Output: raw work identifier (e.g. W2741809807)</text>

    <!-- Composite Title Key -->
    <rect x="20" y="370" width="440" height="135" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="395" font-size="11.5" font-weight="bold" fill="#0f172a">5.4 Composite Title Key (compute_title_key)</text>
    <text x="35" y="415" font-size="9.5" fill="#475569">• Serves as fallback matcher when DOIs/PMIDs are missing</text>
    <text x="35" y="431" font-size="9.5" fill="#475569">• Title: strips non-alphanumeric [^a-z0-9], takes first 60 chars</text>
    <text x="35" y="447" font-size="9.5" fill="#475569">• Year: captures normalized 4-digit publication year</text>
    <text x="35" y="463" font-size="9.5" fill="#475569">• Author: cleans first author surname, takes first 20 chars</text>
    <text x="35" y="482" font-size="9.5" font-weight="bold" fill="#065f46">• Output Key: title60_year_author20 (e.g. deeplearningforcancer_2024_smith)</text>

    <!-- Affiliation Fallback -->
    <rect x="20" y="520" width="440" height="160" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="545" font-size="11.5" font-weight="bold" fill="#0f172a">5.5 Affiliation Fallback Enricher (pubmed_affiliation_enricher.py)</text>
    <text x="35" y="565" font-size="9.5" fill="#475569">• Triggered when PubMed CSV records lack institutional affiliations</text>
    <text x="35" y="581" font-size="9.5" fill="#475569">• Detects PMID column in DataFrame</text>
    <text x="35" y="597" font-size="9.5" fill="#475569">• Batches PMIDs into chunks of 50</text>
    <text x="35" y="613" font-size="9.5" fill="#475569">• Queries NCBI efetch.fcgi with retmode=xml</text>
    <text x="35" y="629" font-size="9.5" fill="#475569">• Extracts author affiliations from &lt;AffiliationInfo/Affiliation&gt;</text>
    <text x="35" y="645" font-size="9.5" fill="#475569">• Populates Affiliations column in-place and saves enriched file</text>
  </g>

  <!-- Middle: 4-Priority Deduplication Engine -->
  <g transform="translate(555, 175)">
    <rect x="0" y="0" width="560" height="970" rx="14" fill="#fafafa" stroke="#059669" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="530" height="34" rx="6" fill="#d1fae5"/>
    <text x="280" y="37" font-size="13" font-weight="bold" fill="#065f46" text-anchor="middle">4-PRIORITY DEDUPLICATION &amp; MERGE ENGINE</text>

    <!-- Priority Evaluation -->
    <rect x="20" y="65" width="520" height="230" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="90" font-size="11.5" font-weight="bold" fill="#0f172a">5.6 Priority-Based Matching Logic (deduplicate_results)</text>
    <text x="35" y="110" font-size="9.5" fill="#475569">Maintains 4 hash lookup indices: doi_index, pmid_index, openalex_index, title_index</text>

    <rect x="30" y="125" width="500" height="34" rx="6" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1"/>
    <text x="45" y="146" font-size="10" font-weight="bold" fill="#1e40af">Priority 1 Match: Normalized DOI match in doi_index</text>

    <rect x="30" y="165" width="500" height="34" rx="6" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1"/>
    <text x="45" y="186" font-size="10" font-weight="bold" fill="#1e40af">Priority 2 Match: Normalized PMID match in pmid_index</text>

    <rect x="30" y="205" width="500" height="34" rx="6" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1"/>
    <text x="45" y="226" font-size="10" font-weight="bold" fill="#1e40af">Priority 3 Match: OpenAlex ID match in openalex_index</text>

    <rect x="30" y="245" width="500" height="34" rx="6" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1"/>
    <text x="45" y="266" font-size="10" font-weight="bold" fill="#1e40af">Priority 4 Match: Fallback composite title_key match in title_index</text>

    <!-- Merge Logic -->
    <rect x="20" y="315" width="520" height="320" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="1.5"/>
    <rect x="25" y="322" width="510" height="26" rx="4" fill="#dbeafe"/>
    <text x="280" y="339" font-size="11" font-weight="bold" fill="#1e40af" text-anchor="middle">5.7 Paper Record Merging Engine (merge_paper_records)</text>

    <text x="35" y="370" font-size="9.5" fill="#1e293b">• <b>Source Tags Union:</b> Preserves both origins e.g. ['pubmed', 'openalex'] → 'pubmed, openalex'</text>
    <text x="35" y="395" font-size="9.5" fill="#1e293b">• <b>Title &amp; Abstract:</b> Selects the longer, more informative abstract and title</text>
    <text x="35" y="420" font-size="9.5" fill="#1e293b">• <b>Author Names Union:</b> Merges author lists preserving order, removing duplicates</text>
    <text x="35" y="445" font-size="9.5" fill="#1e293b">• <b>Institutional Affiliations:</b> Semicolon-delimited concatenation of unique affiliations</text>
    <text x="35" y="470" font-size="9.5" fill="#1e293b">• <b>Countries Set:</b> Combines and sorts canonical extracted country lists</text>
    <text x="35" y="495" font-size="9.5" fill="#1e293b">• <b>Citation Counts:</b> Takes highest verified count max(rec1.citations, rec2.citations)</text>
    <text x="35" y="520" font-size="9.5" fill="#1e293b">• <b>Direct PDF URL Priority (_pdf_priority):</b></text>
    <text x="50" y="538" font-size="9" fill="#475569">Priority 3: Verified direct .pdf file link</text>
    <text x="50" y="554" font-size="9" fill="#475569">Priority 2: PMC / repository stream path (/pdf/)</text>
    <text x="50" y="570" font-size="9" fill="#475569">Priority 1: General landing page link</text>
    <text x="35" y="605" font-size="9.5" fill="#1e293b">• <b>Index Map Updates:</b> Updates existing index entry with merged representation</text>
  </g>

  <!-- Right: Country Extraction & CSV Storage -->
  <g transform="translate(1145, 175)">
    <rect x="0" y="0" width="560" height="970" rx="14" fill="#fafafa" stroke="#059669" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="530" height="34" rx="6" fill="#d1fae5"/>
    <text x="280" y="37" font-size="13" font-weight="bold" fill="#065f46" text-anchor="middle">COUNTRY EXTRACTION &amp; CSV STORAGE</text>

    <!-- Country Extractor -->
    <rect x="20" y="65" width="520" height="235" rx="8" fill="#ffffff" stroke="#c026d3" stroke-width="1.5"/>
    <rect x="25" y="70" width="510" height="26" rx="4" fill="#fae8ff"/>
    <text x="280" y="87" font-size="11" font-weight="bold" fill="#86198f" text-anchor="middle">5.8 Geographic Entity Recognition (country_extractor.py)</text>

    <text x="35" y="115" font-size="9.5" fill="#701a75">• <b>COUNTRY_ALIASES Dictionary:</b> 700+ canonical mappings</text>
    <text x="50" y="131" font-size="9" fill="#475569">Acronyms: 'usa', 'uk', 'prc', 'frg', 'rok', 'uae', 'us of a'</text>
    <text x="50" y="147" font-size="9" fill="#475569">Sub-regions: 'england', 'scotland', 'wales' → 'United Kingdom'</text>
    <text x="50" y="163" font-size="9" fill="#475569">Native names: 'deutschland' → 'Germany', 'bharat' → 'India'</text>

    <text x="35" y="185" font-size="9.5" fill="#701a75">• <b>Regex Word Boundary Protection (\\b):</b></text>
    <text x="50" y="201" font-size="9" fill="#475569">Eliminates false-positive substring matches (e.g. 'Iran' in 'Uranium', 'Oman' in 'Woman')</text>

    <text x="35" y="223" font-size="9.5" fill="#701a75">• <b>ISO-3166-1 Alpha-3 Code Resolution (get_country_iso3):</b></text>
    <text x="50" y="239" font-size="9" fill="#475569">Maps canonical names to 3-letter codes ('United States' → 'USA', 'India' → 'IND')</text>
    <text x="50" y="255" font-size="9" fill="#475569">Enables direct matching with TopoJSON world-110m.json map shapes</text>
    <text x="35" y="278" font-size="9.5" font-weight="bold" fill="#701a75">• Output: Sorted deduplicated list of canonical countries per paper</text>

    <!-- Centralized CSV Loader -->
    <rect x="20" y="320" width="520" height="155" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="345" font-size="11.5" font-weight="bold" fill="#0f172a">5.9 Centralized CSV Loader (utils/csv_loader.py)</text>
    <text x="35" y="365" font-size="9.5" fill="#475569">• <b>check_bom:</b> Detects UTF-8-BOM (\\xef\\xbb\\xbf), UTF-16, UTF-32</text>
    <text x="35" y="381" font-size="9.5" fill="#475569">• <b>detect_csv_encoding:</b> Probing sequence:</text>
    <text x="50" y="397" font-size="9" fill="#475569">1. UTF-8 → 2. UTF-8-SIG → 3. CP1252 → 4. ISO-8859-1 → 5. Latin-1 → 6. chardet</text>
    <text x="35" y="417" font-size="9.5" fill="#475569">• <b>read_csv_to_dataframe &amp; read_csv_to_records:</b></text>
    <text x="50" y="433" font-size="9" fill="#475569">Safe error-tolerant parsing with fallback to Latin-1 on encoding failures</text>
    <text x="50" y="449" font-size="9" fill="#475569">Guarantees all standard columns are present with null-safe defaults</text>

    <!-- Storage Cylinder -->
    <rect x="20" y="495" width="520" height="200" rx="8" fill="#f8fafc" stroke="#64748b" stroke-width="1.8"/>
    <rect x="25" y="500" width="510" height="26" rx="4" fill="#e2e8f0"/>
    <text x="280" y="517" font-size="11" font-weight="bold" fill="#1e293b" text-anchor="middle">5.10 Persistent CSV Dataset Storage (data/*.csv)</text>

    <text x="35" y="545" font-size="9.5" fill="#0f172a">• Stored in local directory: <b>data/&lt;sanitized_query&gt;.csv</b></text>
    <text x="35" y="565" font-size="9.5" fill="#0f172a">• Encoded as UTF-8-SIG (preserves international accents in Excel)</text>
    <text x="35" y="585" font-size="9.5" fill="#0f172a">• <b>Standardized 13-Column Schema:</b></text>
    <text x="50" y="605" font-size="9" fill="#475569">1. Title • 2. DOI • 3. PMID • 4. OpenAlex_ID • 5. Abstract</text>
    <text x="50" y="621" font-size="9" fill="#475569">6. Source • 7. Publication Year • 8. Authors • 9. Affiliations</text>
    <text x="50" y="637" font-size="9" fill="#475569">10. Countries • 11. Citation_Count • 12. Is_OA • 13. PDF_URL</text>

    <!-- Hand-off to Layer 6 -->
    <rect x="20" y="715" width="520" height="65" rx="8" fill="#f0fdf4" stroke="#10b981" stroke-width="1.5"/>
    <text x="280" y="742" font-size="11.5" font-weight="bold" fill="#065f46" text-anchor="middle">5.11 Final Structured Dataset Handed Off to Layer 6</text>
    <text x="280" y="760" font-size="9.5" fill="#047857" text-anchor="middle">Enriched, deduplicated, geographic dataset ready for bibliometrics &amp; AI</text>
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
                            facecolor="#059669", edgecolor="#047857", linewidth=1.5, zorder=2)
    ax.add_patch(header)
    ax.text(0.6, 11.45, "LAYER 05: DATA CLEANING & ENRICHMENT LAYER FLOWCHART", fontsize=15, fontweight='bold', color="#FFFFFF", zorder=3)
    ax.text(0.6, 11.08, "Identifier Normalization, 4-Priority Deduplication, Record Merging, ISO 3166-1 Country Extraction & CSV Storage", fontsize=9.5, color="#D1FAE5", zorder=3)
    ax.text(17.4, 11.25, "Research Rover v2.0", fontsize=10, fontweight='bold', color="#6EE7B7", ha='right', zorder=3)

    # Column 1: Normalization & Keys
    col1 = FancyBboxPatch((0.5, 0.5), 5.2, 10.0, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#059669", linewidth=1.5, zorder=2)
    ax.add_patch(col1)
    ax.text(3.1, 10.2, "IDENTIFIER NORMALIZATION", fontsize=11, fontweight='bold', color="#065F46", ha='center', zorder=3)

    ax.text(3.1, 9.4, "5.1 normalize_doi(doi)\nStrips https://doi.org/ & dx.doi.org/\nConverts to lowercase trimmed string", fontsize=8.5, color="#0F172A", ha='center', zorder=3)
    ax.text(3.1, 8.2, "5.2 normalize_pmid(pmid)\nStrips URL prefixes, extracts numeric ID", fontsize=8.5, color="#0F172A", ha='center', zorder=3)
    ax.text(3.1, 7.2, "5.3 normalize_openalex_id(id)\nStrips URI path, isolates alphanumeric ID", fontsize=8.5, color="#0F172A", ha='center', zorder=3)
    ax.text(3.1, 5.8, "5.4 compute_title_key(title, year, author)\nAlphanumeric regex [^a-z0-9] on title (60 chars)\nNormalizes 4-digit publication year\nFirst author surname (20 chars)\nOutput: title60_year_author20 key", fontsize=8.5, color="#1E40AF", ha='center', zorder=3)
    ax.text(3.1, 3.6, "5.5 Affiliation Fallback Enricher\npubmed_affiliation_enricher.py\nBatches PMIDs in chunks of 50\nQueries EFetch XML for AffiliationInfo\nPopulates Affiliations column", fontsize=8.5, color="#047857", ha='center', zorder=3)

    # Column 2: 4-Priority Deduplication
    col2 = FancyBboxPatch((6.0, 0.5), 5.6, 10.0, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#059669", linewidth=1.5, zorder=2)
    ax.add_patch(col2)
    ax.text(8.8, 10.2, "4-PRIORITY DEDUPLICATION ENGINE", fontsize=11, fontweight='bold', color="#065F46", ha='center', zorder=3)

    ax.text(8.8, 9.4, "5.6 Priority-Based Matching Logic\nMaintains 4 hash lookup indices:\n• Priority 1: Match by DOI in doi_index\n• Priority 2: Match by PMID in pmid_index\n• Priority 3: Match by OpenAlex ID in openalex_index\n• Priority 4: Fallback title_key in title_index", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    ax.text(8.8, 6.6, "5.7 Record Merging (merge_paper_records)\n• Sources union: ['pubmed', 'openalex']\n• Authors union: deduplicated, preserves order\n• Affiliations: semicolon-delimited unique strings\n• Title & Abstract: selects longer, richer text\n• Citation Count: max(c1, c2)\n• Direct PDF: prioritizes verified .pdf over viewer\n• Updates all 4 hash indices with merged record", fontsize=8.5, color="#1E3A8A", ha='center', zorder=3)

    # Column 3: Geographic Recognition & Storage
    col3 = FancyBboxPatch((11.9, 0.5), 5.6, 10.0, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#059669", linewidth=1.5, zorder=2)
    ax.add_patch(col3)
    ax.text(14.7, 10.2, "COUNTRY EXTRACTION & STORAGE", fontsize=11, fontweight='bold', color="#065F46", ha='center', zorder=3)

    ax.text(14.7, 9.4, "5.8 Geographic Extraction (country_extractor.py)\nCOUNTRY_ALIASES map (700+ entries)\n• Acronyms: usa, uk, prc, rok, uae\n• Sub-regions: england, scotland → UK\n• Word boundary regex \\b prevents false positives\n• get_country_iso3: resolves to ISO-3 alpha-3\n  ('United States' → 'USA', 'India' → 'IND')", fontsize=8.5, color="#701A75", ha='center', zorder=3)

    ax.text(14.7, 6.8, "5.9 Centralized CSV Loader (csv_loader.py)\ncheck_bom: detects UTF-8-BOM, UTF-16, UTF-32\ndetect_csv_encoding: UTF-8 → UTF-8-SIG →\nCP1252 → ISO-8859-1 → Latin-1 → chardet\nSafe fallback parsing prevents decode crashes", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    ax.text(14.7, 4.4, "5.10 Dataset Storage (data/*.csv)\nSaved in data/<sanitized_query>.csv\nEncoded as UTF-8-SIG (Excel compatible)\nStandardized 13-column schema:\nTitle, DOI, PMID, OpenAlex_ID, Abstract, Source,\nYear, Authors, Affiliations, Countries, Citations, PDF", fontsize=8.5, color="#1E293B", ha='center', zorder=3)

    ax.text(14.7, 1.8, "5.11 Exit: Structured Dataset Ready\nClean deduplicated bibliographic catalog\nHanded off to Layer 6: Analysis & Computation", fontsize=8.5, fontweight='bold', color="#065F46", ha='center', zorder=3)

    plt.tight_layout()
    plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated PNG: {png_path}")
