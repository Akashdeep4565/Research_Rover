# Research Rover: System Workflow & Block Diagram Documentation

**Document Level:** M.Tech Project Architecture & Presentation Documentation  
**System Name:** Research Rover (Intelligent Literature Review & Bibliometric Discovery Platform)  
**Visual Style:** Miro Clean Board Architecture (Pastel Workflow with Decision Diamonds)  
**Verification Date:** November 2026  

---

## 1. Executive Summary

This document specifies the operational workflow of the **Research Rover** application, corresponding directly to the visual block diagram (`research_rover_block_diagram.png` / `.svg`). 

Unlike complex low-level UML diagrams that expose internal classes, this block diagram focuses on the **end-to-end user-to-system process flow**. It bridges the gap between what the researcher initiates in the user interface and how the backend coordinates external academic APIs, performs data cleaning, calculates bibliometrics, and renders insights.

```
+----------------------------------------------------------------------------------------------------+
|                                    RESEARCH ROVER HIGH-LEVEL FLOW                                  |
|                                                                                                    |
|  [ Open Research Rover ]                                                                           |
|          |                                                                                         |
|          v                                                                                         |
|  [ Enter Research Query ]                                                                          |
|          |                                                                                         |
|          v                                                                                         |
|  [ Select Search Options ] (Unified, PubMed, OpenAlex)                                             |
|          |                                                                                         |
|          v                                                                                         |
|  [ Submit Search Request ]                                                                         |
|          |                                                                                         |
|          v                                                                                         |
|  [ FastAPI Orchestrator ] ----> [ Query Scholarly APIs ] ----> { API Success? }                   |
|                                                                     |                              |
|                                            +--- (No) -------------> [ Display API Error ]          |
|                                            |                                                       |
|                                            v (Yes)                                                 |
|                                 [ Retrieve Papers ]                                                |
|                                            |                                                       |
|                                            v                                                       |
|                                   { Papers Found? }                                                |
|                                      |                                                             |
|             +--- (No) --------------> [ Display No Results ]                                       |
|             |                                                                                      |
|             v (Yes)                                                                                |
|   [ Deduplicate & Merge ] (Match DOI, PMID, Title)                                                 |
|             |                                                                                      |
|             v                                                                                      |
|   [ Extract Affiliations ] (Normalize ISO-3 Countries)                                             |
|             |                                                                                      |
|             v                                                                                      |
|   [ Save Clean Corpus ] (CSV in data/ folder)                                                      |
|             |                                                                                      |
|             v                                                                                      |
|   [ Compute Bibliometrics ] & [ Build Network Models ] ----> { Analysis Success? }                 |
|                                                                  |                                 |
|                                       +--- (No) ---------------> [ Fallback Metadata View ]        |
|                                       |                                                            |
|                                       v (Yes)                                                      |
|                             [ Render Visualizations ]                                              |
|                                       |                                                            |
|                                       +---> [ Explore Paper Cards ]                                |
|                                       |                                                            |
|                                       +---> [ Download OA PDFs ]                                   |
|                                       |                                                            |
|                                       +---> [ AI Research Assistant ]                              |
|                                       |                                                            |
|                                       v                                                            |
|                             [ Explore Insights & Export Data ] (Terminal)                          |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Visual Palette & Miro Design Elements

The diagram utilizes the visual language of the reference Miro workflow board:
- **Terminal Nodes (Gold / Pastel Yellow `#FFDA54`):** Represent the entry point (*Open Research Rover*) and final user achievement (*Explore Insights & Export Data*).
- **Process Blocks (Lavender / Pastel Purple `#B3ACFF`):** Represent atomic operational stages executed either by the user or the underlying backend services.
- **Decision Points (Sky Blue `#82D2FD`):** Prominently shaped diamonds representing critical branching decisions.
- **Exception & Recovery Blocks (Soft Coral / Pastel Red `#FFB3B3`):** Indicate error boundaries, empty result states, or fallback modes that cleanly redirect the user without application crashes.
- **Flow Connectors (Dark Charcoal `#1E1E1E`):** Orthogonal, clean connecting lines with unambiguous directional arrowheads and branch condition badges (`Yes` / `No`).

---

## 3. Detailed Step-by-Step Block Inventory

### Column 1: User Interaction & API Dispatch
1. **Open Research Rover (Start Node):** The user launches the single-page application, served by React/Vite with automatic backend status probing (`GET /api/v1/system/status`).
2. **Enter Research Query:** The researcher provides a scientific topic, author name, or medical condition (e.g., *"Agentic AI in Oncology"*, *"Deep Learning for Genomic Diagnostics"*).
3. **Select Search Options:** The user selects search parameters:
   - **Target Data Source:** Unified Search (Parallel PubMed + OpenAlex), PubMed Only, or OpenAlex Only.
   - **Publication Year Range:** Dual-handle slider filtering between 1950 and current year.
   - **Result Limit:** Desired number of candidate records (e.g., 10, 25, 50, 100).
   - **Sort Mode:** Ordering by algorithmic relevance or recency.
4. **Submit Search Request:** Triggers `POST /api/v1/search/` with JSON payload containing query configuration.
5. **FastAPI Orchestrator:**
   - Immediately returns a fast response to free the HTTP thread.
   - Spawns an asynchronous background task (`asyncio.create_task`) with a cooperative cancellation token (`threading.Event`).
   - Serves real-time execution status via `GET /api/v1/search/progress` for the frontend progress bar.
6. **Query Scholarly APIs:** Dispatches non-blocking HTTP requests:
   - **NCBI Entrez E-Utilities:** Calls `esearch.fcgi`, `efetch.fcgi`, and spelling suggestion via `espell.fcgi`.
   - **OpenAlex REST API:** Calls `/works` endpoint with filter parameters and inverted index reconstruction for abstracts.
7. **Decision Point 1 — API Request Successful?:**
   - **No:** If network failures, rate limiting, or gateway timeouts occur on both external APIs, the system moves to **Display API Error & Retry**, notifying the user with specific failure context.
   - **Yes:** If at least one data source succeeds, execution continues forward. If only one provider succeeds in Unified mode, a non-blocking warning is logged and surviving results are preserved.

---

### Column 2: Data Collection & Normalization
8. **Retrieve Papers & Raw Metadata:** Extracts titles, abstracts, author rosters, raw affiliation strings, publication years, DOIs, PMIDs, citation counts, and open-access PDF URLs.
9. **Decision Point 2 — Research Papers Found?:**
   - **No:** If the query matched 0 papers across all queried APIs, the system moves to **Display No-Results Message**, offering synonym expansions, acronym unwrapping, or broader date bounds.
   - **Yes:** If valid papers are retrieved ($N \ge 1$), the pipeline proceeds.
10. **Deduplicate & Merge:**
    - Resolves cross-database overlaps between PubMed and OpenAlex.
    - Matches candidate duplicates hierarchically:
      1. Normalized DOI matching (ignoring case, whitespace, and URL prefixes).
      2. PubMed ID (PMID) matching.
      3. OpenAlex Work ID matching.
      4. Normalized Title + Year + First Author composite key.
    - Merges complementary fields (e.g., taking MeSH terms from PubMed and citation counts/OA links from OpenAlex).
11. **Extract Affiliations & Normalize Countries:**
    - Parses author and institution strings using heuristic address segmentation.
    - Maps country variations (e.g., *"USA"*, *"US"*, *"U.S.A."*, *"United States of America"*) to canonical country names.
    - Generates ISO-3166 alpha-3 codes (e.g., `USA`, `GBR`, `CHN`, `IND`) for choropleth mapping.
    - Flags unassigned records without country data for transparent bibliometric accounting.
12. **Save Clean Corpus (CSV):**
    - Persists the processed, deduplicated paper records as a standardized CSV file in the `data/` directory.
    - Encodes with UTF-8 BOM (`utf-8-sig`) for Excel and external R/Python compatibility.

---

### Column 3: Bibliometrics & AI Processing
13. **Compute Bibliometrics:**
    - Calculates keyword frequencies from author-supplied keywords and title/abstract tokenization.
    - Normalizes acronyms and aliases (e.g., `ml` $	o$ `machine learning`, `iot` $	o$ `internet of things`).
    - Produces country publication frequencies and relative percentages.
14. **Build Network Models:**
    - Calculates keyword co-occurrence frequencies across all papers.
    - Constructs an undirected co-occurrence graph using NetworkX to compute degree centrality metrics.
    - Computes international co-authorship collaboration links between countries with weighted edge counts.
15. **Decision Point 3 — Analysis Successful?:**
    - **No:** In the event of missing metadata fields or unexpected CSV formatting, the system falls back to **Fallback Metadata View** so raw papers remain accessible.
    - **Yes:** Proceeds with full analytics rendering and downstream AI indexing.
16. **AI Research Assistant:**
    - Builds/loads a local FAISS vector index of paper chunks using `SentenceTransformer` embeddings (`all-MiniLM-L6-v2`).
    - Enables the user to ask plain-English questions in the Chat interface.
    - Synthesizes grounded answers backed by interactive citations that link directly to specific papers in the corpus.

---

### Column 4: Visualization & Output
17. **Render Visualizations:**
    - **Keyword Analytics:** Interactive SVG Word Cloud, top-keyword frequency bar charts, and co-occurrence network graphs.
    - **Geographic Country Analysis:** TopoJSON interactive choropleth world map, country volume ranking tables, and 2D/3D force-directed international collaboration graphs.
    - **Keyword Presence Matrix:** Document-by-keyword binary presence grid.
18. **Explore Paper Cards:** Interactive paginated cards displaying paper titles, author chips, publication year badges, citation counts, and Open Access tags.
19. **Download OA PDFs:**
    - Direct download link when an open-access PDF URL is present.
    - Secure backend streaming proxy (`GET /api/v1/files/download-pdf`) protected against SSRF, verifying public IP ranges and delivering clean PDF binaries with descriptive filenames.
20. **Explore Insights & Export Data (Terminal Node):**
    - Export clean corpus CSV for local thesis and publication use.
    - Download high-resolution PNG / SVG charts.
    - Export keyword frequency tables and country collaboration matrices.

---

## 4. Key Architectural Strengths

1. **Non-Blocking Resilience:** FastAPI background tasks and polling endpoints (`/search/progress`) prevent long external API requests from timing out HTTP connections or freezing the browser.
2. **Cooperative Cancellation:** Both the PubMed fetch loop and background embedding tasks monitor `threading.Event` cancel tokens, allowing the user to halt expensive operations mid-run.
3. **Data Integrity & Fallback Open:** When one API fails in unified search, surviving results from the alternate source are presented with transparent warning badges.
4. **Self-Contained Storage:** All search results, canonical schemas, and analytics summaries reside in structured JSON and CSV formats on disk, ensuring offline durability and reproducibility.
