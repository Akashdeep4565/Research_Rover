"""
Layer 4: Data Collection & External Sources Layer
Covers NCBI PubMed E-Utilities, OpenAlex REST API, CORE planned stub,
query optimization, ESpell correction, batching, rate limiting, and response parsing.
"""

from .common import THEMES, get_svg_header, get_svg_footer
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

def get_mermaid():
    return """flowchart TD
    %% =========================================================================
    %% LAYER 4: DATA COLLECTION & EXTERNAL SOURCES LAYER
    %% Project: Research Rover
    %% Focus: External Scientific APIs, E-Utilities, OpenAlex REST, Parsing & Fault Tolerance
    %% =========================================================================

    classDef startEnd fill:#ECFEFF,stroke:#0891B2,stroke-width:2.5px,color:#155E75,font-weight:bold;
    classDef orchestrator fill:#F8FAFC,stroke:#06B6D4,stroke-width:1.5px,color:#0F172A;
    classDef externalAPI fill:#F0FDFA,stroke:#0D9488,stroke-width:2px,color:#134E4A,font-weight:bold;
    classDef decision fill:#FEF3C7,stroke:#D97706,stroke-width:2px,color:#78350F,font-weight:bold;
    classDef stub fill:#F1F5F9,stroke:#64748B,stroke-width:1.5px,stroke-dasharray: 5 5,color:#475569;
    classDef parser fill:#EEF2FF,stroke:#6366F1,stroke-width:1.5px,color:#312E81;
    classDef output fill:#ECFDF5,stroke:#10B981,stroke-width:2px,color:#064E3B;

    DC_ENTRY(["4.0 Entry: Search Query & Parameters Received<br/>(From Layer 3: Backend Controllers)"]):::startEnd

    %% ─── SEARCH ORCHESTRATION ───────────────────────────────────────────────
    subgraph SUB_ORCH["SEARCH ORCHESTRATION (SearchService & UnifiedSearchService)"]
        SRC_DECIDE{"4.1 Evaluate search_source Option"}:::decision
        RUN_UNIFIED["Unified Search Engine<br/>Launches parallel async tasks across PubMed & OpenAlex"]:::orchestrator
        RUN_PUBMED["PubMed Dedicated Search Engine<br/>Dedicated ThreadPoolExecutor (max_workers=4)"]:::orchestrator
        RUN_OPENALEX["OpenAlex Dedicated Search Engine<br/>Async httpx client with polite pool mailto"]:::orchestrator
        RUN_CORE["CORE Search Stub (Planned)<br/>search_service.py:102 logs warning & returns []"]:::stub
    end

    %% ─── SOURCE 1: NCBI PUBMED E-UTILITIES ───────────────────────────────────
    subgraph SUB_PUBMED["DATA SOURCE 1: NCBI PUBMED (Entrez E-Utilities API)"]
        PM_PREP["4.2 Query Pre-Processing & Expansion<br/>• _improve_pubmed_query: Expands abbreviations (ai, ml, iot)<br/>• _concept_clause: MeSH descriptor & synonym tagging<br/>• _build_date_filter: Formats mindate & maxdate YYYY/MM/DD"]:::orchestrator
        
        PM_ESEARCH["4.3 esearch.fcgi (Search Query & PMIDs Retrieval)<br/>• Rate Limit: 0.10s (with API key) / 0.34s (without API key)<br/>• POST with exponential backoff retry (_post_with_retry)<br/>• Paged retrieval up to min(max_results * 2, 1000)"]:::externalAPI
        
        PM_SPELL_CHECK{"4.4 Check esearch Count"}:::decision
        PM_ESPELL["4.5 espell.fcgi (NCBI Spell Check Fallback)<br/>Query returns 0 hits → fetches corrected spelling<br/>Automatically retries esearch with corrected query"]:::externalAPI
        
        PM_EFETCH["4.6 efetch.fcgi (Full XML Article Retrieval)<br/>• Batching: Chunks PMIDs into batches of 50<br/>• retmode=xml, db=pubmed"]:::externalAPI
        
        PM_ESUMMARY["4.7 esummary.fcgi (Metadata Verification)<br/>Retrieves exact publication year, journal title & citation strings"]:::externalAPI
        
        PM_PARSE["4.8 XML ElementTree Parser (_parse_pubmed_xml)<br/>• Extracts PMID, PMCID, DOI, Title, AbstractText<br/>• Extracts Authors & AffiliationInfo/Affiliation<br/>• Formats Vancouver-style bibliographic reference"]:::parser
    end

    %% ─── SOURCE 2: OPENALEX REST API ─────────────────────────────────────────
    subgraph SUB_OPENALEX["DATA SOURCE 2: OPENALEX (Universal Scientific Works API)"]
        OA_REQ["4.9 OpenAlex HTTP Request Formulation<br/>• URL: https://api.openalex.org/works<br/>• User-Agent: ResearchRover/2.0 (mailto:email)<br/>• Query params: search, filter (dates), per_page (up to 200)"]:::orchestrator
        
        OA_FETCH["4.10 OpenAlex Works REST API<br/>Dispatches async GET via httpx (timeout=30s)"]:::externalAPI
        
        OA_PARSE["4.11 OpenAlex JSON Response Parser (parse_work_item)<br/>• reconstruct_abstract(): Inverts abstract_inverted_index dictionary<br/>• extract_clean_doi() & extract_clean_pmid()<br/>• Authors, raw_affiliation_strings & institution objects<br/>• Resolves Open Access status & direct PDF URLs<br/>• Extracts concepts, topics & cited_by_count"]:::parser
    end

    %% ─── SOURCE 3: CORE REPOSITORY (PLANNED) ─────────────────────────────────
    subgraph SUB_CORE["DATA SOURCE 3: CORE (Open Access Harvester)"]
        CORE_NOTE["CORE API Integration<br/>Status: Planned Stub (schemas.py enum SearchSource.CORE)<br/>Current behavior: logs warning and returns empty list"]:::stub
    end

    %% ─── FAULT TOLERANCE & MERGING ───────────────────────────────────────────
    subgraph SUB_FAULT_TOLERANCE["NON-BLOCKING FAULT TOLERANCE & PARTIAL FAILURES"]
        FT_CHECK{"4.12 Check API Responses"}:::decision
        FT_BOTH_OK["Both PubMed & OpenAlex succeeded<br/>Emits combined candidate set"]:::output
        FT_PARTIAL["Partial Failure Handling<br/>One API unreachable → returns active API results<br/>Attaches user warning flag (last_warning)"]:::orchestrator
        FT_BOTH_FAIL["Both APIs Failed<br/>Raises SearchServiceException to Layer 3 Controller"]:::errorState
    end

    DC_OUT(["4.13 Exit: Transmit Raw Paper Dictionaries to Layer 5 (Data Cleaning & Enrichment)"]):::startEnd

    %% Connections
    DC_ENTRY --> SRC_DECIDE
    SRC_DECIDE -->|unified| RUN_UNIFIED
    SRC_DECIDE -->|pubmed| RUN_PUBMED
    SRC_DECIDE -->|openalex| RUN_OPENALEX
    SRC_DECIDE -->|core| RUN_CORE

    RUN_UNIFIED --> PM_PREP & OA_REQ
    RUN_PUBMED --> PM_PREP
    RUN_OPENALEX --> OA_REQ
    RUN_CORE --> CORE_NOTE --> DC_OUT

    PM_PREP --> PM_ESEARCH --> PM_SPELL_CHECK
    PM_SPELL_CHECK -->|Count == 0| PM_ESPELL --> PM_ESEARCH
    PM_SPELL_CHECK -->|Count > 0| PM_EFETCH & PM_ESUMMARY --> PM_PARSE

    OA_REQ --> OA_FETCH --> OA_PARSE

    PM_PARSE --> FT_CHECK
    OA_PARSE --> FT_CHECK

    FT_CHECK -->|Both Success| FT_BOTH_OK --> DC_OUT
    FT_CHECK -->|One Fails| FT_PARTIAL --> DC_OUT
    FT_CHECK -->|Both Fail| FT_BOTH_FAIL
"""

def get_svg():
    w, h = 1750, 1250
    header = get_svg_header(
        w, h,
        title="Layer 4: Data Collection & External Sources Layer Flowchart",
        subtitle="NCBI Entrez E-Utilities, OpenAlex REST API, Abstract Inversion, Batch Fetching, Rate Limiting & Partial Failures",
        layer_badge="LAYER 04",
        theme_key="layer_04"
    )

    content = '''
  <!-- Inter-layer Connectivity Cards -->
  <g transform="translate(45, 115)">
    <rect x="0" y="0" width="380" height="42" rx="8" fill="#f3e8ff" stroke="#a855f7" stroke-width="1.5"/>
    <text x="15" y="26" font-size="12" font-weight="bold" fill="#6b21a8">INPUT SOURCE:</text>
    <text x="120" y="26" font-size="12" fill="#334155">Layer 3: Search Request Criteria &amp; Parameters</text>
  </g>
  <g transform="translate(1325, 115)">
    <rect x="0" y="0" width="380" height="42" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
    <text x="15" y="26" font-size="12" font-weight="bold" fill="#065f46">OUTPUT TARGET:</text>
    <text x="130" y="26" font-size="12" fill="#334155">Layer 5 (Data Cleaning &amp; Enrichment)</text>
  </g>

  <!-- Left: Source 1 NCBI PubMed E-Utilities -->
  <g transform="translate(45, 175)">
    <rect x="0" y="0" width="540" height="970" rx="14" fill="#fafafa" stroke="#0891b2" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="510" height="34" rx="6" fill="#cffafe"/>
    <text x="270" y="37" font-size="13" font-weight="bold" fill="#155e75" text-anchor="middle">DATA SOURCE 1: NCBI PUBMED (Entrez E-Utilities)</text>

    <!-- Pre-processing -->
    <rect x="20" y="65" width="500" height="95" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="88" font-size="11.5" font-weight="bold" fill="#0f172a">4.1 Query Pre-Processing &amp; Expansion (_improve_pubmed_query)</text>
    <text x="35" y="108" font-size="9.5" fill="#475569">• Word-boundary abbreviation expansion (ml → machine learning, ai, dl, iot)</text>
    <text x="35" y="124" font-size="9.5" fill="#475569">• _concept_clause: tags multi-word phrases with MeSH Terms e.g. ("phrase"[MeSH] OR "phrase")</text>
    <text x="35" y="140" font-size="9.5" fill="#475569">• _build_date_filter: converts start_date/end_date to YYYY/MM/DD [dp] tags</text>

    <!-- esearch.fcgi -->
    <rect x="20" y="175" width="500" height="100" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="200" font-size="11.5" font-weight="bold" fill="#0e7490">4.2 esearch.fcgi (Search Query &amp; PMIDs Retrieval)</text>
    <text x="35" y="220" font-size="9.5" fill="#475569">• Endpoint: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi</text>
    <text x="35" y="236" font-size="9.5" fill="#475569">• Rate Limiter: 0.10s (with API key) / 0.34s (without API key) delay between calls</text>
    <text x="35" y="252" font-size="9.5" fill="#475569">• Paged candidate collection: retstart/retmax up to min(max_results * 2, 1000)</text>

    <!-- Spell check decision -->
    <polygon points="270,290 380,315 270,340 160,315" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>
    <text x="270" y="312" font-size="10" font-weight="bold" fill="#78350f" text-anchor="middle">Count == 0?</text>
    <text x="270" y="324" font-size="8" fill="#92400e" text-anchor="middle">Zero results fallback</text>

    <!-- espell.fcgi -->
    <rect x="20" y="355" width="500" height="75" rx="8" fill="#fffbeb" stroke="#f59e0b" stroke-width="1.2"/>
    <text x="35" y="378" font-size="11" font-weight="bold" fill="#92400e">4.3 espell.fcgi (NCBI Query Correction Engine)</text>
    <text x="35" y="396" font-size="9" fill="#78350f">• Calls espell.fcgi to extract &lt;CorrectedQuery&gt; tag</text>
    <text x="35" y="412" font-size="9" fill="#78350f">• Surfaces last_corrected_query ("Showing results for ...") and retries</text>

    <!-- efetch.fcgi & esummary.fcgi -->
    <rect x="20" y="445" width="500" height="115" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="470" font-size="11.5" font-weight="bold" fill="#0e7490">4.4 efetch.fcgi &amp; esummary.fcgi (Batch Article Retrieval)</text>
    <text x="35" y="490" font-size="9.5" fill="#475569">• efetch.fcgi: Chunks candidate PMIDs into batches of 50 (retmode=xml)</text>
    <text x="35" y="506" font-size="9.5" fill="#475569">• Exponential backoff retry (_post_with_retry: 3 attempts on 429/5xx)</text>
    <text x="35" y="522" font-size="9.5" fill="#475569">• esummary.fcgi: JSON summary verification for exact publication dates</text>
    <text x="35" y="538" font-size="9.5" fill="#475569">• ThreadPoolExecutor: 4 dedicated threads prevent asyncio pool starvation</text>

    <!-- XML Parser -->
    <rect x="20" y="575" width="500" height="145" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="600" font-size="11.5" font-weight="bold" fill="#0e7490">4.5 XML Parser &amp; Metadata Extraction (_parse_pubmed_xml)</text>
    <text x="35" y="620" font-size="9.5" fill="#475569">• Parses &lt;PubmedArticle&gt; tree using Python xml.etree.ElementTree</text>
    <text x="35" y="636" font-size="9.5" fill="#475569">• Extracts Title, AbstractText, Journal Title, PubDate (Year, Month, Day)</text>
    <text x="35" y="652" font-size="9.5" fill="#475569">• AuthorList: Extracts ForeName + LastName into structured string list</text>
    <text x="35" y="668" font-size="9.5" fill="#475569">• AffiliationInfo/Affiliation: Extracts raw author affiliation strings</text>
    <text x="35" y="684" font-size="9.5" fill="#475569">• ArticleIdList: Extracts DOI, PMID, and PMCID for full-text PMC linking</text>
    <text x="35" y="700" font-size="9.5" fill="#475569">• Reference: Formats standard Vancouver-style bibliographic citation</text>
  </g>

  <!-- Middle: Source 2 OpenAlex Universal Scientific Works API -->
  <g transform="translate(615, 175)">
    <rect x="0" y="0" width="540" height="970" rx="14" fill="#fafafa" stroke="#0891b2" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="510" height="34" rx="6" fill="#cffafe"/>
    <text x="270" y="37" font-size="13" font-weight="bold" fill="#155e75" text-anchor="middle">DATA SOURCE 2: OPENALEX (Universal Works API)</text>

    <!-- Request Formulation -->
    <rect x="20" y="65" width="500" height="95" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="88" font-size="11.5" font-weight="bold" fill="#0f172a">4.6 Request Formulation &amp; Polite Pool Protocol</text>
    <text x="35" y="108" font-size="9.5" fill="#475569">• Endpoint: https://api.openalex.org/works</text>
    <text x="35" y="124" font-size="9.5" fill="#475569">• User-Agent: ResearchRover/2.0 (mailto:email) ensures fast Polite Pool priority</text>
    <text x="35" y="140" font-size="9.5" fill="#475569">• Parameters: search, filter (from/to dates), per_page=min(max_results, 200)</text>

    <!-- Inverted Abstract Reconstruction -->
    <rect x="20" y="175" width="500" height="110" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="200" font-size="11.5" font-weight="bold" fill="#0e7490">4.7 Abstract Inversion Engine (reconstruct_abstract)</text>
    <text x="35" y="220" font-size="9.5" fill="#475569">• OpenAlex provides abstracts as compressed abstract_inverted_index objects</text>
    <text x="35" y="236" font-size="9.5" fill="#475569">• Structure: {"word": [position_0, position_12, position_45]}</text>
    <text x="35" y="252" font-size="9.5" fill="#475569">• Reconstructs word positions into chronological array: sorted(pos_map.keys())</text>
    <text x="35" y="268" font-size="9.5" fill="#475569">• Emits full plain-text abstract without loss of formatting</text>

    <!-- Author & Institutional Affiliation -->
    <rect x="20" y="300" width="500" height="135" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="325" font-size="11.5" font-weight="bold" fill="#0e7490">4.8 Author, Institution &amp; Country Extraction</text>
    <text x="35" y="345" font-size="9.5" fill="#475569">• Authorships array: iterates over author.display_name and author.id</text>
    <text x="35" y="361" font-size="9.5" fill="#475569">• raw_affiliation_strings: collects raw institutional strings</text>
    <text x="35" y="377" font-size="9.5" fill="#475569">• institutions: extracts display_name, ROR ID, and country_code</text>
    <text x="35" y="393" font-size="9.5" fill="#475569">• countries: captures explicit 2-letter ISO country codes</text>
    <text x="35" y="409" font-size="9.5" fill="#475569">• Feeds affiliation text into country_extractor.py to populate ISO-3 country sets</text>

    <!-- Open Access & PDF Resolution -->
    <rect x="20" y="450" width="500" height="110" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="475" font-size="11.5" font-weight="bold" fill="#0e7490">4.9 Open Access &amp; Direct PDF Link Resolution</text>
    <text x="35" y="495" font-size="9.5" fill="#475569">• Inspects open_access.is_oa and open_access.oa_url</text>
    <text x="35" y="511" font-size="9.5" fill="#475569">• best_oa_location.pdf_url &amp; primary_location.pdf_url resolution</text>
    <text x="35" y="527" font-size="9.5" fill="#475569">• PMCID Fallback: https://pmc.ncbi.nlm.nih.gov/articles/PMC{id}/pdf/</text>
    <text x="35" y="543" font-size="9.5" fill="#475569">• Prioritizes true .pdf endpoints over repository landing pages</text>

    <!-- Concepts, Topics & Citation Metrics -->
    <rect x="20" y="575" width="500" height="145" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="600" font-size="11.5" font-weight="bold" fill="#0e7490">4.10 Concepts, Topics &amp; Citation Metrics</text>
    <text x="35" y="620" font-size="9.5" fill="#475569">• Concepts list: extracts display_name (e.g. 'Artificial Intelligence')</text>
    <text x="35" y="636" font-size="9.5" fill="#475569">• Topics list: extracts granular sub-disciplinary research tags</text>
    <text x="35" y="652" font-size="9.5" fill="#475569">• cited_by_count: captures exact numerical citation frequency</text>
    <text x="35" y="668" font-size="9.5" fill="#475569">• Standardizes output schema to match Research Rover paper dictionary</text>
  </g>

  <!-- Right: CORE Planned Stub & Non-Blocking Fault Tolerance -->
  <g transform="translate(1185, 175)">
    <rect x="0" y="0" width="520" height="970" rx="14" fill="#fafafa" stroke="#0891b2" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="490" height="34" rx="6" fill="#cffafe"/>
    <text x="260" y="37" font-size="13" font-weight="bold" fill="#155e75" text-anchor="middle">ORCHESTRATION &amp; FAULT TOLERANCE</text>

    <!-- Unified Search Orchestrator -->
    <rect x="20" y="65" width="480" height="115" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="90" font-size="11.5" font-weight="bold" fill="#0f172a">4.11 Unified Multi-Source Engine (UnifiedSearchService)</text>
    <text x="35" y="110" font-size="9.5" fill="#475569">• Ingests query, max_results, date bounds, and cancel_event</text>
    <text x="35" y="126" font-size="9.5" fill="#475569">• Launches parallel async tasks across PubMed and OpenAlex</text>
    <text x="35" y="142" font-size="9.5" fill="#475569">• Eliminates sequential network latency</text>
    <text x="35" y="158" font-size="9.5" fill="#475569">• Checks cooperative cancellation between steps</text>

    <!-- CORE Stub Card -->
    <rect x="20" y="195" width="480" height="95" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="6 4"/>
    <text x="35" y="220" font-size="11.5" font-weight="bold" fill="#475569">4.12 CORE Repository Harvester (Planned Stub)</text>
    <text x="35" y="240" font-size="9.5" fill="#64748b">• Present in schemas.py as SearchSource.CORE enum</text>
    <text x="35" y="256" font-size="9.5" fill="#64748b">• Implemented in search_service.py:102 as _search_core()</text>
    <text x="35" y="272" font-size="9.5" fill="#64748b">• Behavior: Logs warning and returns [] empty result set</text>

    <!-- Non-Blocking Partial Failure Handling -->
    <rect x="20" y="305" width="480" height="230" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="330" font-size="11.5" font-weight="bold" fill="#0f172a">4.13 Non-Blocking Partial Failure Resilience</text>

    <rect x="30" y="345" width="460" height="45" rx="6" fill="#ecfdf5" stroke="#a7f3d0" stroke-width="1"/>
    <text x="45" y="365" font-size="9.5" font-weight="bold" fill="#065f46">Case 1: Both Succeeded</text>
    <text x="45" y="379" font-size="8.5" fill="#047857">PubMed results + OpenAlex results merged and passed to Layer 5</text>

    <rect x="30" y="400" width="460" height="45" rx="6" fill="#fffbeb" stroke="#fde68a" stroke-width="1"/>
    <text x="45" y="420" font-size="9.5" font-weight="bold" fill="#92400e">Case 2: PubMed Fails, OpenAlex Succeeds</text>
    <text x="45" y="434" font-size="8.5" fill="#78350f">Returns OpenAlex results with last_warning: "PubMed could not be reached"</text>

    <rect x="30" y="455" width="460" height="45" rx="6" fill="#fffbeb" stroke="#fde68a" stroke-width="1"/>
    <text x="45" y="475" font-size="9.5" font-weight="bold" fill="#92400e">Case 3: OpenAlex Fails, PubMed Succeeds</text>
    <text x="45" y="489" font-size="8.5" fill="#78350f">Returns PubMed results with last_warning: "OpenAlex could not be reached"</text>

    <!-- Output Box -->
    <rect x="20" y="560" width="480" height="160" rx="8" fill="#f0fdf4" stroke="#10b981" stroke-width="1.8"/>
    <text x="40" y="590" font-size="12" font-weight="bold" fill="#065f46">4.14 Raw Candidate Record Output</text>
    <text x="40" y="612" font-size="9.5" fill="#047857">• Standardized dictionary representations emitted to Layer 5:</text>
    <text x="40" y="630" font-size="9.5" fill="#047857">  Title, DOI, PMID, OpenAlex_ID, Abstract, Publication Year,</text>
    <text x="40" y="648" font-size="9.5" fill="#047857">  Journal, Authors list, raw Affiliations, direct PDF_URL, OA flag</text>
    <text x="40" y="670" font-size="9.5" font-weight="bold" fill="#064e3b">→ Handed off to Layer 5: Data Cleaning &amp; Enrichment</text>
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
                            facecolor="#0E7490", edgecolor="#155E75", linewidth=1.5, zorder=2)
    ax.add_patch(header)
    ax.text(0.6, 11.45, "LAYER 04: DATA COLLECTION & EXTERNAL SOURCES FLOWCHART", fontsize=15, fontweight='bold', color="#FFFFFF", zorder=3)
    ax.text(0.6, 11.08, "NCBI Entrez E-Utilities, OpenAlex REST API, Abstract Inversion, Batch Fetching, Rate Limiting & Partial Failures", fontsize=9.5, color="#CFFAFE", zorder=3)
    ax.text(17.4, 11.25, "Research Rover v2.0", fontsize=10, fontweight='bold', color="#67E8F9", ha='right', zorder=3)

    # Column 1: Source 1 NCBI PubMed E-Utilities
    col1 = FancyBboxPatch((0.5, 0.5), 5.4, 10.0, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#0891B2", linewidth=1.5, zorder=2)
    ax.add_patch(col1)
    ax.text(3.2, 10.2, "NCBI PUBMED (E-UTILITIES API)", fontsize=11, fontweight='bold', color="#155E75", ha='center', zorder=3)

    ax.text(3.2, 9.4, "4.1 Query Pre-Processing\n_improve_pubmed_query (abbreviation expansion)\n_concept_clause (MeSH descriptor tagging)\n_build_date_filter (YYYY/MM/DD [dp] bounds)", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    ax.text(3.2, 7.8, "4.2 esearch.fcgi (PMIDs Collection)\nRate limit: 0.10s (with key) / 0.34s (without key)\nDedicated ThreadPoolExecutor (max_workers=4)\nPaged collection up to min(max*2, 1000)", fontsize=8.5, color="#0E7490", ha='center', zorder=3)

    ax.text(3.2, 6.2, "4.3 espell.fcgi (Zero-Hit Spell Fallback)\nIf count == 0: fetches suggested spelling\nAutomatically retries esearch with corrected query", fontsize=8.5, color="#92400E", ha='center', zorder=3)

    ax.text(3.2, 4.6, "4.4 efetch.fcgi & esummary.fcgi\nBatching: chunks PMIDs into batches of 50\nExponential backoff retry (_post_with_retry)\nRetrieves complete XML records & summaries", fontsize=8.5, color="#0E7490", ha='center', zorder=3)

    ax.text(3.2, 2.8, "4.5 XML ElementTree Parser\nExtracts Title, AbstractText, Journal, PubDate\nExtracts Authors, AffiliationInfo/Affiliation\nExtracts DOI, PMID, PMCID, and Reference", fontsize=8.5, color="#047857", ha='center', zorder=3)

    # Column 2: Source 2 OpenAlex REST API
    col2 = FancyBboxPatch((6.2, 0.5), 5.4, 10.0, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#0891B2", linewidth=1.5, zorder=2)
    ax.add_patch(col2)
    ax.text(8.9, 10.2, "OPENALEX (UNIVERSAL WORKS API)", fontsize=11, fontweight='bold', color="#155E75", ha='center', zorder=3)

    ax.text(8.9, 9.4, "4.6 Request Formulation & Polite Pool\nEndpoint: https://api.openalex.org/works\nUser-Agent: ResearchRover/2.0 (mailto:email)\nFilter params: from/to dates, per_page up to 200", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    ax.text(8.9, 7.8, "4.7 Abstract Inversion Engine\nOpenAlex stores abstract as inverted index\nreconstruct_abstract(): inverts positions map\nSorted position keys reconstruct full text", fontsize=8.5, color="#0E7490", ha='center', zorder=3)

    ax.text(8.9, 6.2, "4.8 Authors & Affiliations Extraction\nIterates over author display names and IDs\nCaptures raw_affiliation_strings\nExtracts institutions & 2-letter country codes", fontsize=8.5, color="#0E7490", ha='center', zorder=3)

    ax.text(8.9, 4.6, "4.9 Open Access & PDF Resolution\nChecks open_access.is_oa and best_oa_location\nResolves verified .pdf URLs and PMC stream paths\nPrioritizes direct PDF endpoints", fontsize=8.5, color="#0E7490", ha='center', zorder=3)

    ax.text(8.9, 2.8, "4.10 Concepts & Citation Metrics\nExtracts display_name concepts and topics\nCaptures exact cited_by_count number\nEmits normalized paper dictionary", fontsize=8.5, color="#047857", ha='center', zorder=3)

    # Column 3: Orchestration & Fault Tolerance
    col3 = FancyBboxPatch((11.9, 0.5), 5.6, 10.0, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#0891B2", linewidth=1.5, zorder=2)
    ax.add_patch(col3)
    ax.text(14.7, 10.2, "ORCHESTRATION & FAULT TOLERANCE", fontsize=11, fontweight='bold', color="#155E75", ha='center', zorder=3)

    ax.text(14.7, 9.4, "4.11 UnifiedSearchService Orchestrator\nLaunches parallel async tasks across\nPubMed and OpenAlex APIs simultaneously\nEliminates sequential roundtrip latency", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    ax.text(14.7, 7.8, "4.12 CORE Repository Stub (Planned)\nSearchSource.CORE enum in schemas.py\nImplemented as _search_core() in search_service.py\nLogs warning and returns [] empty list", fontsize=8.5, color="#64748B", ha='center', zorder=3)

    ax.text(14.7, 5.8, "4.13 Non-Blocking Partial Failure Resilience\n• If both succeed: merges candidate records\n• If PubMed fails: returns OpenAlex + warning\n• If OpenAlex fails: returns PubMed + warning\n• If both fail: raises exception to controller", fontsize=8.5, color="#B45309", ha='center', zorder=3)

    ax.text(14.7, 2.8, "4.14 Raw Candidate Record Output\nStandardized dictionary schema emitted to Layer 5:\nTitle, DOI, PMID, OpenAlex_ID, Abstract, Year,\nAuthors, Affiliations, direct PDF_URL, OA flag\nHanded off to Layer 5: Data Cleaning & Enrichment", fontsize=8.5, fontweight='bold', color="#065F46", ha='center', zorder=3)

    plt.tight_layout()
    plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated PNG: {png_path}")
