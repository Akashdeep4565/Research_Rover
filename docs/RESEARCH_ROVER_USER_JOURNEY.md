# Research Rover - User Perspective Flowchart & User Journey Document

## 1. Detailed User Journey Flowchart

```mermaid
flowchart TD
    subgraph USER["USER ACTIONS"]
        U1(["Start: User Opens Research Rover"])
        U2["Navigate to Page View<br/>(Home / Search / Analytics / Chat / Settings)"]
        U3["Enter Research Query & Select Filters<br/>(e.g., 'machine learning cancer', Max Results, Date Bounds)"]
        U4["Click 'Search Research Papers'"]
        U5{"Search Results Found?"}
        U6["Refine Search Terms or Date Filters"]
        U7["Browse Ranked Results & Metadata<br/>(PMID, Authors, Affiliations, MedCPT Score)"]
        U8["Click 'Open in Analytics' or Select CSV File"]
        U9{"Select Analysis Perspective"}
        U10_KW["Explore Keyword Analytics Tab"]
        U10_CTRY["Explore Country Analysis Tab"]
        U10_CHAT["Open RAG Chat Interface"]
        U11_INTERACT["Interact with Visualizations<br/>(Hover country map, search ranking, filter 2D/3D graph, rotate 3D space)"]
        U12_EXPORT["Export Results & Assets<br/>(Download CSV data, JSON summary, PNG charts)"]
        U13{"Continue Exploration?"}
        U14(["End: Research Complete"])
    end

    subgraph SYSTEM["RESEARCH ROVER SYSTEM RESPONSES"]
        S1["Display Home Dashboard & Navigation Bar"]
        S2["Display Search Form & Filter Controls"]
        S3["Show Real-time Progress Bar<br/>('Searching research papers...')"]
        S4["Query PubMed API & Re-rank with MedCPT AI"]
        S5_NO["Display 'No Papers Found' Alert & Query Suggestions"]
        S5_YES["Display Ranked Paper Results List & 'Download CSV' Button"]
        S6["Load CSV Dataset & Compute Analytics"]
        S7_KW["Render Keyword Visualizations<br/>(Frequency Bars, Word Cloud, Co-occurrence Graph, Centrality Table, Matrix)"]
        S7_CTRY["Render Country Visualizations<br/>(TopoJSON World Map, Ranking Table, 2D D3 Network, 3D Three.js Network)"]
        S7_CHAT["Generate Vector Index & Stream RAG Answer with Citations"]
        S8["Provide Interactive Highlights, Tooltips & File Downloads"]
    end

    %% Flow Connections
    U1 --> S1 --> U2 --> U3 --> U4 --> S3 --> S4 --> U5
    U5 -->|No| S5_NO --> U6 --> U4
    U5 -->|Yes| S5_YES --> U7 --> U8 --> S6 --> U9

    U9 -->|Keyword Tab| U10_KW --> S7_KW --> U11_INTERACT
    U9 -->|Country Tab| U10_CTRY --> S7_CTRY --> U11_INTERACT
    U9 -->|RAG Chat Tab| U10_CHAT --> S7_CHAT --> U11_INTERACT

    U11_INTERACT --> S8 --> U12_EXPORT --> U13
    U13 -->|Yes| U9
    U13 -->|No| U14
```

---

## 2. Simplified PPT-Friendly User Flowchart

```mermaid
flowchart LR
    A["1. Enter Search Query<br/>(PubMed + MedCPT AI)"] --> B["2. Review Ranked Results<br/>(Title, Authors, Affiliations)"]
    B --> C["3. Select Analytics View<br/>(Keyword or Country)"]
    C --> D["4. Interact with Visuals<br/>(World Map, 2D/3D Graphs)"]
    D --> E["5. RAG Q&A Chat<br/>(Ask Questions on Dataset)"]
    E --> F["6. Export Assets<br/>(CSV, JSON, PNG Downloads)"]
```

---

## 3. Explanation of User Journey Steps

1. **Start & Navigation**: The researcher accesses Research Rover and selects a workflow page from the main navigation header (Home, Search, Analytics, Chat, Settings).
2. **Formulating Search Request**: The user enters a topic query (e.g., `"machine learning cancer"`), adjusts the max result limit (e.g., 10 to 100), and optionally sets publication start/end year bounds.
3. **Executing Search & Feedback**: Clicking **Search** displays a real-time progress indicator ("Searching research papers..."). The system queries PubMed, parses affiliations/metadata, and re-ranks papers using MedCPT AI relevance scoring.
4. **Inspecting Search Results**: If papers are found, they are displayed in a clean list featuring PMID, Title, Authors, Journal, Affiliations, MeSH terms, and MedCPT relevance scores. If no results match, a clean error alert prompts the user to adjust terms.
5. **Selecting Analysis Perspective**: The user clicks **Open in Analytics** or navigates to the **Analytics Page** and picks a dataset CSV:
   - **Keyword Analytics Tab**: Displays total papers, unique keywords, frequency distribution bars, an interactive Word Cloud, a 3D-sphere co-occurrence network, NetworkX centrality scores (degree, closeness, betweenness, eigenvector, clustering), and a binary keyword presence matrix per paper.
   - **Country Analysis Tab**: Displays country publication coverage summary, unassigned paper inspection modal, an interactive TopoJSON World Map (volume shading & hover tooltips), top country publication bar chart, a complete country publication ranking table (with search), an international co-authorship partnerships table, a 2D D3 collaboration network, and a 3D Three.js force-directed space graph.
   - **Chat RAG Tab**: The user picks a dataset and types natural language questions. The system embeds the text into FAISS vector space and streams AI answers with paper citations.
6. **Interacting with Visualizations**: The user hovers over map countries, searches ranking tables, filters collaboration strength (All/Medium/Strong), rotates 3D network spaces, and zooms camera controls.
7. **Exporting Assets & Data**: The user downloads CSV files (keyword frequency, centrality scores, country ranking, co-authorships), JSON summary artifacts, or PNG chart images directly to their local computer.

---

## 4. Actual Research Rover Pages & Features Used in the Flowchart

| UI Page | Feature / View | Exact Visual Elements & Controls Implemented |
| :--- | :--- | :--- |
| **Search Page** (`/search`) | Query Input & Filters | Search bar, Max Results selector (10, 20, 50, 100), Start/End Year inputs, Raw Query mode toggle, Real-time progress panel, MedCPT AI score badges, CSV download button, "Open in Analytics" link |
| **Analytics Page** (`/analytics`) | CSV Dataset Selector | File select dropdown, Refresh button, Custom CSV file upload button, Top-N keyword limit controls (presets + custom N), Matrix preview row selector, Rebuild analysis button |
| **Analytics Page** (`/analytics`) | Keyword Analytics Tab | Summary KPI cards (Total Papers, With Keywords, Unique Keywords, Matrix Columns), Keyword Frequency progress bars, Analysis Summary metadata box, SVG Word Cloud, Co-occurrence network graph, NetworkX Centrality table, Binary Keyword Matrix |
| **Analytics Page** (`/analytics`) | Country Analysis Tab | Summary KPI cards (Total Papers, With Country Data, Without Country Data, Unique Countries, International Papers, Coverage %), Metadata Coverage split bar, Unassigned Papers inspection modal, TopoJSON World Map, Top Country Bar Chart, Complete Country Publication Ranking table (with search), International Co-Authorship Partnerships table, 2D D3 Force Network (strength filter, search, zoom/pan), 3D Three.js Force Network (rotate, zoom, particle toggle, active card overlay) |
| **Chat Page** (`/chat`) | RAG Dataset Q&A | Dataset selector, Model selector dropdown (OpenAI, DeepSeek, Groq), Vector Index generation modal (`EmbeddingProgressModal`), Streaming markdown chat responses with paper source citations |
| **Settings Page** (`/settings`) | System Configuration | API Key input fields (NCBI, OpenAI, DeepSeek, Groq), Model preference select, Dark/Light theme switcher |
