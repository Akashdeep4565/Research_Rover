"""
Layer 6: Analysis & Computation Layer
Covers all 8 parallel computational engines: Keyword Frequency, NetworkX Centralities,
Binary Presence Matrix, Country Bibliometrics, Co-authorship Collaboration Graph,
MedCPT Neural Re-ranking, HDBSCAN Semantic Chunking & FAISS Indexing, and RAG Query Synthesis.
"""

from .common import THEMES, get_svg_header, get_svg_footer
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

def get_mermaid():
    return """flowchart TD
    %% =========================================================================
    %% LAYER 6: ANALYSIS & COMPUTATION LAYER
    %% Project: Research Rover
    %% Focus: 8 Parallel Analytical Pipelines, Graph Algorithms, Neural Reranking, Vector Store & RAG
    %% =========================================================================

    classDef startEnd fill:#FFFBEB,stroke:#D97706,stroke-width:2.5px,color:#78350F,font-weight:bold;
    classDef inputDS fill:#F1F5F9,stroke:#64748B,stroke-width:1.5px,color:#0F172A;
    classDef kwBranch fill:#FEF3C7,stroke:#D97706,stroke-width:1.5px,color:#78350F;
    classDef ctryBranch fill:#FDF4FF,stroke:#C026D3,stroke-width:1.5px,color:#701A75;
    classDef aiBranch fill:#EFF6FF,stroke:#2563EB,stroke-width:1.5px,color:#1E3A8A;
    classDef ragBranch fill:#F0FDF4,stroke:#059669,stroke-width:1.5px,color:#064E3B;
    classDef output fill:#ECFDF5,stroke:#10B981,stroke-width:2px,color:#064E3B;

    AN_ENTRY(["6.0 Entry: Clean Structured Dataset (data/*.csv)<br/>(Received from Layer 5: Data Cleaning & Enrichment)"]):::startEnd

    %% ─── PARALLEL COMPUTATION BRANCHES ───────────────────────────────────────
    
    %% BRANCH 1: KEYWORD FREQUENCY
    subgraph B1["BRANCH 1: KEYWORD FREQUENCY & PERCENTAGE (analysis_service.py)"]
        B1_IN["Input: Paper keywords lists"]:::inputDS
        B1_PROC["Processing: _normalize_keyword alias mapping<br/>(ai → artificial intelligence, ml → machine learning)<br/>Collections Counter frequency aggregation"]:::kwBranch
        B1_OUT["Output: Ranked Keyword Frequency List<br/>Frequency count & percentage coverage across corpus"]:::output
    end

    %% BRANCH 2: CO-OCCURRENCE & NETWORKX CENTRALITY
    subgraph B2["BRANCH 2: CO-OCCURRENCE & NETWORKX CENTRALITIES (analysis_service.py)"]
        B2_IN["Input: Top N keywords per paper"]:::inputDS
        B2_PROC["Processing: itertools.combinations(sorted(kw), 2)<br/>Construct undirected graph nx.Graph()<br/>Compute 5 Centrality Algorithms:<br/>1. Degree Centrality (nx.degree_centrality)<br/>2. Closeness Centrality (nx.closeness_centrality)<br/>3. Betweenness Centrality (nx.betweenness_centrality)<br/>4. Eigenvector Centrality (nx.eigenvector_centrality)<br/>5. Clustering Coefficient (nx.clustering)"]:::kwBranch
        B2_OUT["Output: Co-Occurrence Edges & Centrality Rankings Table"]:::output
    end

    %% BRANCH 3: BINARY PRESENCE MATRIX
    subgraph B3["BRANCH 3: BINARY KEYWORD PRESENCE MATRIX (analysis_service.py)"]
        B3_IN["Input: Paper records & Top N matrix keywords"]:::inputDS
        B3_PROC["Processing: One-hot binary indicator mapping<br/>Row = paper, Column = keyword (1 = present, 0 = absent)<br/>Generates preview rows (1-100)"]:::kwBranch
        B3_OUT["Output: _analysis_keyword_presence_matrix.csv<br/>Preview payload & full downloadable CSV matrix"]:::output
    end

    %% BRANCH 4: COUNTRY BIBLIOMETRICS
    subgraph B4["BRANCH 4: COUNTRY PUBLICATION BIBLIOMETRICS (country_service.py)"]
        B4_IN["Input: Extracted country lists from paper affiliations"]:::inputDS
        B4_PROC["Processing: Frequency counter per country<br/>Computes percentage coverage: papers_with_country / total<br/>Tracks international multi-country papers (len >= 2)<br/>Captures unassigned papers lacking geographic data"]:::ctryBranch
        B4_OUT["Output: CountryStatisticsResponse<br/>Ranked publication volume, coverage %, unassigned records"]:::output
    end

    %% BRANCH 5: CO-AUTHORSHIP COLLABORATION GRAPH
    subgraph B5["BRANCH 5: INTERNATIONAL COLLABORATION NETWORK (country_service.py)"]
        B5_IN["Input: Multi-country author teams"]:::inputDS
        B5_PROC["Processing: combinations(unique_countries, 2)<br/>Accumulates co-authorship edge weights<br/>Constructs nodes with paper_count and links with weight"]:::ctryBranch
        B5_OUT["Output: CountryCollaborationGraphResponse<br/>Nodes & links payload for 2D/3D force network renderers"]:::output
    end

    %% BRANCH 6: MEDCPT NEURAL RERANKING
    subgraph B6["BRANCH 6: MEDCPT NEURAL RE-RANKING ENGINE (reranker_service.py)"]
        B6_IN["Input: PubMed candidate papers (up to 300) & search query"]:::inputDS
        B6_PROC["Processing: PyTorch Bi-Encoder Models<br/>• Query: ncbi/MedCPT-Query-Encoder (CLS token)<br/>• Article: ncbi/MedCPT-Article-Encoder (CLS token)<br/>Dot product similarity: (a_emb @ q_emb.T)<br/>Monotonic min-max normalization to 0-100 display scale"]:::aiBranch
        B6_OUT["Output: Re-Ranked Papers with Relevance_Score & Relevance_Rank"]:::output
    end

    %% BRANCH 7: HDBSCAN CHUNKING & FAISS
    subgraph B7["BRANCH 7: HDBSCAN CHUNKING & FAISS VECTOR STORE (embedding_service.py)"]
        B7_IN["Input: Paper abstracts & scraped full text"]:::inputDS
        B7_PROC["Processing:<br/>1. Stage 1: Concurrent full-text scrape (BeautifulSoup)<br/>2. Stage 2: NLTK sentence tokenize<br/>3. Dense embedding via all-mpnet-base-v2 (768-dim)<br/>4. HDBSCAN semantic clustering (min_cluster_size=3)<br/>5. Oversized chunk splitting (max 800 tokens)<br/>6. L2 normalization & FAISS IndexFlatL2 construction"]:::aiBranch
        B7_OUT["Output: Persistent FAISS Index (*.index) & Metadata JSONs"]:::output
    end

    %% BRANCH 8: CONVERSATIONAL RAG ENGINE
    subgraph B8["BRANCH 8: CONVERSATIONAL RAG QUERY ENGINE (chat_service.py)"]
        B8_IN["Input: User question & FAISS vector index"]:::inputDS
        B8_PROC["Processing:<br/>1. Gemini query decomposition (splits into <= 5 sub-queries)<br/>2. Multi-query FAISS vector retrieval (k=5 per sub-query)<br/>3. Deduplication of chunks by ID & distance ranking<br/>4. Numbered context assembly [1], [2] with paper metadata<br/>5. Citation-enforcing prompt synthesis via Google Gemini"]:::ragBranch
        B8_OUT["Output: ChatResponse<br/>Synthesized Markdown answer with superscript citation pills"]:::output
    end

    %% BRANCH 9: CITATION CAPTURE CLARIFICATION
    subgraph B9["BRANCH 9: CITATION METRIC CAPTURE (Bibliographic Metadata)"]
        B9_NOTE["Citation Analysis Status Note:<br/>Paper records capture exact numerical citation counts (cited_by_count)<br/>Explicit paper-to-paper citation network graph is not implemented"]:::inputDS
    end

    AN_OUT(["6.10 Exit: Analytical Datasets & Vector Stores Forwarded to Layer 7 (Visualization Layer)"]):::startEnd

    %% Connections
    AN_ENTRY --> B1_IN & B2_IN & B3_IN & B4_IN & B5_IN & B6_IN & B7_IN & B8_IN & B9_NOTE
    B1_IN --> B1_PROC --> B1_OUT --> AN_OUT
    B2_IN --> B2_PROC --> B2_OUT --> AN_OUT
    B3_IN --> B3_PROC --> B3_OUT --> AN_OUT
    B4_IN --> B4_PROC --> B4_OUT --> AN_OUT
    B5_IN --> B5_PROC --> B5_OUT --> AN_OUT
    B6_IN --> B6_PROC --> B6_OUT --> AN_OUT
    B7_IN --> B7_PROC --> B7_OUT --> AN_OUT
    B8_IN --> B8_PROC --> B8_OUT --> AN_OUT
    B9_NOTE --> AN_OUT
"""

def get_svg():
    w, h = 1850, 1300
    header = get_svg_header(
        w, h,
        title="Layer 6: Analysis & Computation Layer Flowchart",
        subtitle="Parallel Analytical Pipelines: NetworkX Graph Centralities, Binary Presence Matrix, MedCPT Neural Ranking, FAISS Vectors & RAG",
        layer_badge="LAYER 06",
        theme_key="layer_06"
    )

    content = '''
  <!-- Inter-layer Connectivity Cards -->
  <g transform="translate(45, 115)">
    <rect x="0" y="0" width="380" height="42" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
    <text x="15" y="26" font-size="12" font-weight="bold" fill="#065f46">INPUT SOURCE:</text>
    <text x="120" y="26" font-size="12" fill="#334155">Layer 5: Structured, Deduplicated CSV Dataset</text>
  </g>
  <g transform="translate(1425, 115)">
    <rect x="0" y="0" width="380" height="42" rx="8" fill="#fff1f2" stroke="#f43f5e" stroke-width="1.5"/>
    <text x="15" y="26" font-size="12" font-weight="bold" fill="#9f1239">OUTPUT TARGET:</text>
    <text x="130" y="26" font-size="12" fill="#334155">Layer 7 (Visualization &amp; Output Layer)</text>
  </g>

  <!-- 3 Major Parallel Workflow Pillars -->
  <!-- Pillar 1: Bibliometric & Keyword Graph Analytics -->
  <g transform="translate(45, 175)">
    <rect x="0" y="0" width="560" height="1020" rx="14" fill="#fafafa" stroke="#d97706" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="530" height="34" rx="6" fill="#fef3c7"/>
    <text x="280" y="37" font-size="13" font-weight="bold" fill="#92400e" text-anchor="middle">PILLAR 1: KEYWORD BIBLIOMETRICS &amp; GRAPH CENTRALITIES</text>

    <!-- Branch 1: Keyword Frequency -->
    <rect x="20" y="65" width="520" height="175" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="90" font-size="11.5" font-weight="bold" fill="#0f172a">6.1 Keyword Frequency Distribution (analysis_service.py)</text>
    <text x="35" y="110" font-size="9.5" fill="#475569">• Input: Parsed keywords list per paper from CSV</text>
    <text x="35" y="126" font-size="9.5" fill="#475569">• _normalize_keyword: alias dictionary replaces terms ('ai' → 'artificial intelligence')</text>
    <text x="35" y="142" font-size="9.5" fill="#475569">• collections.Counter aggregates term frequencies across all records</text>
    <text x="35" y="158" font-size="9.5" fill="#475569">• Filters by minimum_frequency threshold, sorts descending</text>
    <text x="35" y="174" font-size="9.5" fill="#475569">• Computes exact percentage: round((count / total_papers) * 100, 2)</text>
    <text x="35" y="190" font-size="9.5" font-weight="bold" fill="#92400e">• Emits top N frequency list &amp; saves _analysis_keyword_frequency.csv</text>

    <!-- Branch 2: NetworkX Centralities -->
    <rect x="20" y="255" width="520" height="340" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="280" font-size="11.5" font-weight="bold" fill="#0f172a">6.2 Keyword Co-Occurrence &amp; NetworkX Centrality (nx.Graph)</text>
    <text x="35" y="300" font-size="9.5" fill="#475569">• Pairwise keyword combinations: itertools.combinations(sorted(keywords), 2)</text>
    <text x="35" y="316" font-size="9.5" fill="#475569">• Increments co-occurrence weights across all papers</text>
    <text x="35" y="332" font-size="9.5" fill="#475569">• Builds undirected graph: graph.add_edge(source, target, weight=w)</text>
    <text x="35" y="352" font-size="10" font-weight="bold" fill="#b45309">5 Computed Graph Centrality Algorithms:</text>
    <text x="45" y="372" font-size="9" fill="#1e293b">1. <b>Degree Centrality:</b> nx.degree_centrality(graph) - direct connection volume</text>
    <text x="45" y="392" font-size="9" fill="#1e293b">2. <b>Closeness Centrality:</b> nx.closeness_centrality(graph) - shortest path closeness</text>
    <text x="45" y="412" font-size="9" fill="#1e293b">3. <b>Betweenness Centrality:</b> nx.betweenness_centrality(graph, normalized=True)</text>
    <text x="45" y="432" font-size="9" fill="#1e293b">4. <b>Eigenvector Centrality:</b> nx.eigenvector_centrality(graph, max_iter=1000)</text>
    <text x="45" y="452" font-size="9" fill="#1e293b">5. <b>Clustering Coefficient:</b> nx.clustering(graph) - local neighborhood density</text>
    <text x="35" y="480" font-size="9.5" fill="#475569">• Sorts keywords descending by degree centrality</text>
    <text x="35" y="496" font-size="9.5" font-weight="bold" fill="#92400e">• Emits structured centrality_scores array to _analysis_summary.json</text>

    <!-- Branch 3: Binary Presence Matrix -->
    <rect x="20" y="610" width="520" height="185" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="635" font-size="11.5" font-weight="bold" fill="#0f172a">6.3 Binary Keyword Presence Matrix (analysis_service.py)</text>
    <text x="35" y="655" font-size="9.5" fill="#475569">• Ingests top N matrix keywords and paper records</text>
    <text x="35" y="671" font-size="9.5" fill="#475569">• Encodes each paper as a binary indicator row (1 if keyword present, 0 otherwise)</text>
    <text x="35" y="687" font-size="9.5" fill="#475569">• Metadata columns: paper_id, title, source, year, keywords</text>
    <text x="35" y="703" font-size="9.5" fill="#475569">• Columns: top N keywords (e.g. 100 columns)</text>
    <text x="35" y="719" font-size="9.5" fill="#475569">• Exports full matrix to _analysis_keyword_presence_matrix.csv (UTF-8-SIG)</text>
    <text x="35" y="735" font-size="9.5" font-weight="bold" fill="#92400e">• Emits preview rows (1-100) via /analysis/{fn}/matrix endpoint</text>
  </g>

  <!-- Pillar 2: Geographic & Collaboration Network Analytics -->
  <g transform="translate(645, 175)">
    <rect x="0" y="0" width="560" height="1020" rx="14" fill="#fafafa" stroke="#c026d3" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="530" height="34" rx="6" fill="#fae8ff"/>
    <text x="280" y="37" font-size="13" font-weight="bold" fill="#86198f" text-anchor="middle">PILLAR 2: GEOGRAPHIC &amp; COLLABORATION ANALYTICS</text>

    <!-- Branch 4: Country Publication Statistics -->
    <rect x="20" y="65" width="520" height="235" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="90" font-size="11.5" font-weight="bold" fill="#0f172a">6.4 Country Bibliometric Statistics (country_service.py)</text>
    <text x="35" y="110" font-size="9.5" fill="#475569">• Ingests extracted canonical country names per paper</text>
    <text x="35" y="126" font-size="9.5" fill="#475569">• In-Memory Dataset Cache keyed by (abs_path, mtime, size) prevents re-reads</text>
    <text x="35" y="142" font-size="9.5" fill="#475569">• Computes publication frequency and coverage %: (with_country / total) * 100</text>
    <text x="35" y="158" font-size="9.5" fill="#475569">• Flags international multi-country papers: len(unique_countries) &gt;= 2</text>
    <text x="35" y="174" font-size="9.5" fill="#475569">• Tracks unassigned papers lacking geographic data (title, authors, year, journal)</text>
    <text x="35" y="190" font-size="9.5" fill="#475569">• Resolves ISO 3166-1 alpha-3 code via get_country_iso3</text>
    <text x="35" y="206" font-size="9.5" font-weight="bold" fill="#701a75">• Emits CountryStatisticsResponse payload for ranking table &amp; map</text>

    <!-- Branch 5: Co-Authorship Collaboration Graph -->
    <rect x="20" y="315" width="520" height="260" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="340" font-size="11.5" font-weight="bold" fill="#0f172a">6.5 International Co-Authorship Network (country_service.py)</text>
    <text x="35" y="360" font-size="9.5" fill="#475569">• Detects cross-border scientific co-authorship per paper</text>
    <text x="35" y="376" font-size="9.5" fill="#475569">• Generates pairwise country links: combinations(unique_countries, 2)</text>
    <text x="35" y="392" font-size="9.5" fill="#475569">• Increments collaboration_counts[(source, target)] += 1</text>
    <text x="35" y="408" font-size="9.5" fill="#475569">• Builds Graph Data Structures:</text>
    <text x="45" y="426" font-size="9" fill="#1e293b">• <b>Nodes:</b> [{id, label: country, iso_a3, paper_count: int}]</text>
    <text x="45" y="444" font-size="9" fill="#1e293b">• <b>Links:</b> [{source: countryA, target: countryB, weight: int}]</text>
    <text x="35" y="468" font-size="9.5" fill="#475569">• Sorts links descending by collaboration weight</text>
    <text x="35" y="484" font-size="9.5" font-weight="bold" fill="#701a75">• Emits CountryCollaborationGraphResponse for 2D &amp; 3D force graph viewers</text>

    <!-- Branch 9: Citation Metric Capture Note -->
    <rect x="20" y="590" width="520" height="155" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="6 4"/>
    <text x="35" y="615" font-size="11" font-weight="bold" fill="#475569">6.6 Citation Metric Capture (Verification Clarification)</text>
    <text x="35" y="635" font-size="9.5" fill="#64748b">• Paper records capture raw numerical citation counts from OpenAlex &amp; PubMed</text>
    <text x="35" y="651" font-size="9.5" fill="#64748b">• Stored as Citation_Count and cited_by_count columns in CSV</text>
    <text x="35" y="667" font-size="9.5" font-weight="bold" fill="#b91c1c">• Clarification: Paper-to-paper citation network graph is NOT implemented</text>
    <text x="35" y="683" font-size="9.5" fill="#64748b">• (Only co-authorship networks and keyword co-occurrence graphs exist)</text>
  </g>

  <!-- Pillar 3: AI Neural Reranking, Vector Embeddings & RAG -->
  <g transform="translate(1245, 175)">
    <rect x="0" y="0" width="560" height="1020" rx="14" fill="#fafafa" stroke="#2563eb" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="15" y="15" width="530" height="34" rx="6" fill="#eff6ff"/>
    <text x="280" y="37" font-size="13" font-weight="bold" fill="#1e40af" text-anchor="middle">PILLAR 3: NEURAL RERANKING, VECTOR STORE &amp; RAG</text>

    <!-- Branch 6: MedCPT Neural Reranking -->
    <rect x="20" y="65" width="520" height="235" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="90" font-size="11.5" font-weight="bold" fill="#0f172a">6.7 MedCPT Neural Re-ranking Engine (reranker_service.py)</text>
    <text x="35" y="110" font-size="9.5" fill="#475569">• Addresses PubMed's default chronological ordering issue</text>
    <text x="35" y="126" font-size="9.5" fill="#475569">• Ingests candidate papers (up to 300) &amp; original user query</text>
    <text x="35" y="142" font-size="9.5" fill="#475569">• PyTorch Bi-Encoder Models (NCBI MedCPT):</text>
    <text x="45" y="160" font-size="9" fill="#1e293b">• Query Encoder: ncbi/MedCPT-Query-Encoder (CLS token embedding)</text>
    <text x="45" y="176" font-size="9" fill="#1e293b">• Article Encoder: ncbi/MedCPT-Article-Encoder (CLS token on title+abstract)</text>
    <text x="35" y="196" font-size="9.5" fill="#475569">• Dot Product Relevance: scores = (a_emb @ q_emb.T)</text>
    <text x="35" y="212" font-size="9.5" fill="#475569">• Monotonic Min-Max Transform: scales dot product to 0-100 display score</text>
    <text x="35" y="228" font-size="9.5" font-weight="bold" fill="#1e40af">• Re-orders candidate catalog by intellectual relevance</text>

    <!-- Branch 7: HDBSCAN Chunking & FAISS -->
    <rect x="20" y="315" width="520" height="275" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="340" font-size="11.5" font-weight="bold" fill="#0f172a">6.8 Full-Text Scrape &amp; FAISS Indexing (embedding_service.py)</text>
    <text x="35" y="360" font-size="9.5" fill="#475569">• <b>Stage 1: Concurrent Full-Text Scraping:</b></text>
    <text x="50" y="376" font-size="9" fill="#475569">Fetches papers via BeautifulSoup, bounded by SCRAPE_CONCURRENCY=10</text>
    <text x="50" y="392" font-size="9" fill="#475569">Writes &lt;base&gt;_full_text_mapping.json (fallback: abstract only)</text>
    <text x="35" y="412" font-size="9.5" fill="#475569">• <b>Stage 2: Semantic Chunking &amp; Vector Index:</b></text>
    <text x="50" y="428" font-size="9" fill="#475569">NLTK sent_tokenize splits text into sentences</text>
    <text x="50" y="444" font-size="9" fill="#475569">Sentence Transformer all-mpnet-base-v2 encodes normalized vectors</text>
    <text x="50" y="460" font-size="9" fill="#475569">HDBSCAN semantic clustering (min_cluster_size=3) groups sentences</text>
    <text x="50" y="476" font-size="9" fill="#475569">split_oversized_chunks caps chunks at max 800 tokens</text>
    <text x="50" y="492" font-size="9" fill="#475569">Chunk vector = mean of sentence vectors, L2-normalized</text>
    <text x="50" y="508" font-size="9" fill="#475569">Builds FAISS IndexFlatL2 dense index &amp; metadata JSONs</text>

    <!-- Branch 8: Conversational RAG Engine -->
    <rect x="20" y="605" width="520" height="255" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="35" y="630" font-size="11.5" font-weight="bold" fill="#0f172a">6.9 Conversational RAG Query Engine (chat_service.py)</text>
    <text x="35" y="650" font-size="9.5" fill="#475569">• <b>Step 1: Query Decomposition:</b> Gemini splits question into &lt;= 5 sub-queries</text>
    <text x="35" y="666" font-size="9.5" fill="#475569">• <b>Step 2: FAISS Vector Retrieval:</b> search_faiss(k=5) per sub-query</text>
    <text x="35" y="682" font-size="9.5" fill="#475569">• <b>Step 3: Chunk Deduplication:</b> merges chunks, keeps smallest L2 distance</text>
    <text x="35" y="698" font-size="9.5" fill="#475569">• <b>Step 4: Context Assembly:</b> numbered context [1], [2] with paper metadata</text>
    <text x="35" y="714" font-size="9.5" fill="#475569">• <b>Step 5: LLM Synthesis:</b> Google Gemini Flash synthesizes answer</text>
    <text x="35" y="730" font-size="9.5" font-weight="bold" fill="#065f46">• Emits ChatResponse with cited Markdown answer &amp; source cards</text>
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
                            facecolor="#B45309", edgecolor="#92400E", linewidth=1.5, zorder=2)
    ax.add_patch(header)
    ax.text(0.6, 11.45, "LAYER 06: ANALYSIS & COMPUTATION LAYER FLOWCHART", fontsize=15, fontweight='bold', color="#FFFFFF", zorder=3)
    ax.text(0.6, 11.08, "Parallel Analytical Pipelines: NetworkX Graph Centralities, Binary Presence Matrix, MedCPT Neural Ranking, FAISS Vectors & RAG", fontsize=9.5, color="#FEF3C7", zorder=3)
    ax.text(17.4, 11.25, "Research Rover v2.0", fontsize=10, fontweight='bold', color="#FDE68A", ha='right', zorder=3)

    # Column 1: Keywords & NetworkX
    col1 = FancyBboxPatch((0.5, 0.5), 5.4, 10.0, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#D97706", linewidth=1.5, zorder=2)
    ax.add_patch(col1)
    ax.text(3.2, 10.2, "KEYWORD BIBLIOMETRICS & NETWORKX", fontsize=11, fontweight='bold', color="#92400E", ha='center', zorder=3)

    ax.text(3.2, 9.4, "6.1 Keyword Frequency Distribution\n• _normalize_keyword: alias map ('ai' → 'artificial intelligence')\n• collections.Counter calculates frequencies\n• Computes percentage coverage across total papers\n• Emits frequency list & saves keyword_frequency.csv", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    ax.text(3.2, 7.2, "6.2 NetworkX Graph Centrality (nx.Graph)\n• Pairwise combinations(sorted(kw), 2)\n• Builds weighted co-occurrence edges\n• Computes 5 Graph Centrality Metrics:\n  1. Degree Centrality (nx.degree_centrality)\n  2. Closeness Centrality (nx.closeness_centrality)\n  3. Betweenness Centrality (nx.betweenness_centrality)\n  4. Eigenvector Centrality (nx.eigenvector_centrality)\n  5. Clustering Coefficient (nx.clustering)\n• Saves centrality_scores in _analysis_summary.json", fontsize=8.5, color="#78350F", ha='center', zorder=3)

    ax.text(3.2, 3.8, "6.3 Binary Keyword Presence Matrix\n• Encodes each paper as binary 0/1 row\n• Row = paper, Column = top keyword\n• Exports _analysis_keyword_presence_matrix.csv\n• Returns preview rows (1-100) via /matrix API", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    # Column 2: Geographic Bibliometrics
    col2 = FancyBboxPatch((6.2, 0.5), 5.4, 10.0, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#C026D3", linewidth=1.5, zorder=2)
    ax.add_patch(col2)
    ax.text(8.9, 10.2, "GEOGRAPHIC & COLLABORATION ANALYTICS", fontsize=11, fontweight='bold', color="#701A75", ha='center', zorder=3)

    ax.text(8.9, 9.4, "6.4 Country Bibliometric Statistics\n• In-memory cache keyed by (path, mtime, size)\n• Computes publication volume per country\n• Calculates coverage %: (with_country / total) * 100\n• Flags international papers (len(countries) >= 2)\n• Tracks unassigned papers lacking affiliations\n• Maps to ISO-3166-1 alpha-3 code via get_country_iso3", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    ax.text(8.9, 6.4, "6.5 Co-Authorship Collaboration Network\n• Detects cross-border author teams per paper\n• Generates pairwise country combinations\n• Accumulates edge weights: collaboration_counts\n• Builds Graph Structures for 2D & 3D viewers:\n  Nodes: [{id, label, iso_a3, paper_count}]\n  Links: [{source, target, weight}]", fontsize=8.5, color="#701A75", ha='center', zorder=3)

    ax.text(8.9, 3.6, "6.6 Citation Metric Capture Note\n• Captures numeric citation count (cited_by_count)\n• Attached to paper dictionary and CSV\n• Clarification: Paper citation network graph\n  is NOT implemented (only co-authorship exists)", fontsize=8.5, color="#991B1B", ha='center', zorder=3)

    # Column 3: AI Neural Models & RAG
    col3 = FancyBboxPatch((11.9, 0.5), 5.6, 10.0, boxstyle="round,pad=0,rounding_size=0.15",
                          facecolor="#FAFAFA", edgecolor="#2563EB", linewidth=1.5, zorder=2)
    ax.add_patch(col3)
    ax.text(14.7, 10.2, "NEURAL RANKING, FAISS & RAG CHAT", fontsize=11, fontweight='bold', color="#1E3A8A", ha='center', zorder=3)

    ax.text(14.7, 9.4, "6.7 MedCPT Neural Re-ranking Engine\n• NCBI MedCPT bi-encoder PyTorch models\n• ncbi/MedCPT-Query-Encoder (CLS token)\n• ncbi/MedCPT-Article-Encoder (CLS token)\n• Dot product similarity: scores = (a_emb @ q_emb.T)\n• Monotonic min-max transform to 0-100 display score\n• Ranks candidates by intellectual relevance", fontsize=8.5, color="#0F172A", ha='center', zorder=3)

    ax.text(14.7, 6.4, "6.8 HDBSCAN Chunking & FAISS Vector Store\n• Stage 1: Full-text web scrape (BeautifulSoup)\n• Stage 2: all-mpnet-base-v2 (768-dim vectors)\n• HDBSCAN semantic clustering (min_cluster_size=3)\n• split_oversized_chunks: max 800 tokens\n• Vector = mean of sentence vectors, L2 normalized\n• FAISS IndexFlatL2 index (*.index) & metadata", fontsize=8.5, color="#1E40AF", ha='center', zorder=3)

    ax.text(14.7, 3.6, "6.9 Conversational RAG Query Engine\n• Gemini splits question into <= 5 sub-queries\n• Multi-query FAISS search: search_faiss(k=5)\n• Chunk deduplication & distance ranking\n• Context assembly with [1], [2] citation markers\n• Google Gemini Flash synthesizes Markdown answer\n• Emits ChatResponse with citation source cards", fontsize=8.5, color="#065F46", ha='center', zorder=3)

    plt.tight_layout()
    plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated PNG: {png_path}")
