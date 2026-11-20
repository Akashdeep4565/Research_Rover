"""
Generate all 5 black-and-white academic technical diagrams using Graphviz dot.
Outputs vector PDF files directly into E:/Research_Rover_Documentation/figures/
"""

import os
import subprocess

OUTPUT_DIR = os.path.abspath("E:/Research_Rover_Documentation/figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)
DOT_EXE = r"C:\Program Files (x86)\Graphviz\bin\dot.exe"

# Diagram 1: Overall System Architecture
DOT_FIGURE_1 = """
digraph OverallArchitecture {
    graph [rankdir=TB, splines=polyline, nodesep=0.4, ranksep=0.5, bgcolor=white, fontname="Times-Roman"];
    node [shape=box, style="solid", color=black, fontcolor=black, fontname="Times-Roman", fontsize=10, margin="0.15,0.08"];
    edge [color=black, fontcolor=black, fontname="Times-Roman", fontsize=9, arrowsize=0.7];

    subgraph cluster_presentation {
        label = "Presentation Layer (React 19 / TypeScript / Vite - Port 3000)";
        style = "dashed";
        color = black;
        
        ui_pages [label="Application Pages\\nSearchPage | AnalyticsPage | ChatPage | UseCasesPage"];
        ui_components [label="Interactive Analytics & Telemetry Components\\nDatasetQualityModal | DatasetFeatureReadinessBanner\\nCountryCollaboration2D / 3D | WorldMap"];
        ui_client [label="API Client Layer (services/api.ts)\\nAxios Instance | Vite Reverse Proxy (/api -> :8000)"];

        ui_pages -> ui_components [dir=both, style=solid];
        ui_components -> ui_client;
    }

    subgraph cluster_backend {
        label = "Backend Application Layer (FastAPI / Uvicorn ASGI - Port 8000)";
        style = "dashed";
        color = black;

        main_app [label="FastAPI Application Entry Point (main.py)\\nLifespan Manager | CORS Middleware | Background Model Init | /health"];
        
        subgraph cluster_routes {
            label = "API Routing Layer (app/api/routes/)";
            style = "dotted";
            color = black;
            
            r_search [label="/api/v1/search\\nSearch & Progress"];
            r_files [label="/api/v1/files\\nUpload, Quality, CSV"];
            r_analysis [label="/api/v1/analysis\\nKeywords & Countries"];
            r_embeddings [label="/api/v1/embeddings\\nFAISS Indexing"];
            r_chat [label="/api/v1/chat\\nGemini RAG Chat"];
        }

        subgraph cluster_services {
            label = "Service & Core Logic Layer (app/services/ & app/core/)";
            style = "dotted";
            color = black;

            s_search [label="Search & Ranking Services\\npubmed_service.py | openalex_service.py\\nunified_search_service.py | reranker_service.py (MedCPT)"];
            s_ingestion [label="Universal Ingestion & Quality Subsystem\\ndataset_normalizer.py (20 Canonical Fields)\\ndataset_quality.py (Quality & 7-Feature Readiness)\\ncanonical_loader.py (Unified Data Dispatch)"];
            s_analysis [label="Bibliometric Analysis Services\\nanalysis_service.py (Keywords & Co-occurrence)\\ncountry_service.py (Collaboration Graphs)"];
            s_ai [label="AI & Vector Services\\nembedding_service.py (Scraping & FAISS Indexing)\\nchat_service.py (Gemini LLM Synthesis)"];
        }

        main_app -> r_search;
        main_app -> r_files;
        main_app -> r_analysis;
        main_app -> r_embeddings;
        main_app -> r_chat;

        r_search -> s_search;
        r_files -> s_ingestion;
        r_analysis -> s_analysis;
        r_embeddings -> s_ai;
        r_chat -> s_ai;

        s_ingestion -> s_analysis [label="feeds normalized data", style=dashed];
        s_ingestion -> s_ai [label="feeds text data", style=dashed];
    }

    subgraph cluster_storage {
        label = "Data & Model Storage Layer (data/ & Models)";
        style = "dashed";
        color = black;

        d_csv [label="Bibliographic CSV Datasets\\nRaw Uploads & PubMed Searches"];
        d_meta [label="Metadata Sidecars\\n{filename}_canonical_metadata.json"];
        d_faiss [label="Dense Vector Indices & Chunks\\n{filename}_paper_chunks_hdbscan.index"];
        d_models [label="Machine Learning Models\\nall-mpnet-base-v2 | MedCPT Query/Article Encoders"];
    }

    subgraph cluster_external {
        label = "External Scientific & AI APIs";
        style = "dashed";
        color = black;

        ext_pubmed [label="NCBI PubMed API\\n(E-utilities: ESearch, EFetch)"];
        ext_openalex [label="OpenAlex REST API\\n(Scholarly Works Catalog)"];
        ext_gemini [label="Google AI Studio\\n(Gemini 2.5 Flash API)"];
    }

    ui_client -> main_app [label="REST API & SSE\\nHTTP Requests", dir=both];
    
    s_search -> ext_pubmed [dir=both];
    s_search -> ext_openalex [dir=both];
    s_ai -> ext_gemini [dir=both];

    s_ingestion -> d_csv [dir=both];
    s_ingestion -> d_meta [dir=both];
    s_ai -> d_faiss [dir=both];
    s_search -> d_models;
    s_ai -> d_models;
}
"""

# Diagram 2: Universal Dataset Ingestion Workflow
DOT_FIGURE_2 = """
digraph IngestionWorkflow {
    graph [rankdir=TB, splines=ortho, nodesep=0.4, ranksep=0.45, bgcolor=white, fontname="Times-Roman"];
    node [shape=box, style="solid", color=black, fontcolor=black, fontname="Times-Roman", fontsize=10, margin="0.15,0.08"];
    edge [color=black, fontcolor=black, fontname="Times-Roman", fontsize=9, arrowsize=0.7];

    step1 [label="Step 1: CSV Upload\\nUser uploads research-paper CSV via UI or POST /api/v1/files/upload"];
    step2 [label="Step 2: File Validation & Encoding Detection\\nVerify .csv extension, enforce <=100MB limit, detect UTF-8 / Latin-1"];
    step3 [label="Step 3: Canonical Schema Header Mapping Cascade\\nStage 1: Curated Multi-Database Alias Dictionary Lookup\\nStage 2: Normalized Header Transformation (lowercase, punctuation strip)\\nStage 3: Token Set Containment & Prefix Matching\\nStage 4: SequenceMatcher Fuzzy String Comparison (threshold >= 0.85)"];
    step4 [label="Step 4: Record Normalization & Data Cleaning\\nStrip HTML/tags, cast datatypes, unescape entities\\nNon-destructive preservation of unmapped headers into 'raw_data' dictionary\\nDuplicate record identification via exact DOI & title hash"];
    step5 [label="Step 5: Dataset Quality Assessment Engine (0-100)\\nEvaluate 7 completeness dimensions: Title (25), Abstract (20), Keywords (15),\\nAffiliations (10), Authors (10), Year (10), Identifiers (10)\\nApply duplicate penalty, invalid value penalty, small-sample damping factor\\nAssign categorical quality grade: Excellent, Good, Fair, or Poor"];
    step6 [label="Step 6: Seven-Feature Readiness Evaluation\\nDeterministic verification of minimum data thresholds for:\\nkeyword_analysis, cooccurrence_analysis, country_analysis,\\nauthor_analysis, trend_analysis, semantic_search, ai_chat_rag"];
    step7 [label="Step 7: Sidecar Persistence & Extended API Response\\nSave canonical metadata to data/{filename}_canonical_metadata.json\\nReturn ExtendedFileUploadResponse with complete quality & readiness telemetry"];
    step8 [label="Step 8: Interactive UI Telemetry Presentation\\nFrontend automatically opens DatasetQualityModal (Overview, Mappings, Readiness)\\nMounts DatasetFeatureReadinessBanner across AnalyticsPage and ChatPage"];
    step9 [label="Step 9: Downstream Dispatch & Decoupled FAISS Indexing\\nCanonicalDataLoader loads standardized records for bibliometric analytics\\nDense vector embedding generation remains an explicit separate user action"];

    step1 -> step2;
    step2 -> step3;
    step3 -> step4;
    step4 -> step5;
    step5 -> step6;
    step6 -> step7;
    step7 -> step8;
    step8 -> step9;
}
"""

# Diagram 3: Backend Architecture
DOT_FIGURE_3 = """
digraph BackendArchitecture {
    graph [rankdir=TB, splines=polyline, nodesep=0.4, ranksep=0.45, bgcolor=white, fontname="Times-Roman"];
    node [shape=box, style="solid", color=black, fontcolor=black, fontname="Times-Roman", fontsize=10, margin="0.15,0.08"];
    edge [color=black, fontcolor=black, fontname="Times-Roman", fontsize=9, arrowsize=0.7];

    subgraph cluster_entry {
        label = "FastAPI Application Core (backend/main.py)";
        style = "dashed";
        color = black;
        
        main_py [label="FastAPI Entry Point (main.py)\\nApplication Lifespan Context Manager\\nCORS Middleware Configuration\\nHealth Check Routes: GET / and GET /health"];
        config_py [label="Application Settings (app/core/config.py)\\nPydantic BaseSettings | .env Environment Variable Loader\\nDirectories, Model Names, Concurrency & Politeness Controls"];
        model_mgr [label="Model Manager (app/core/model_manager.py)\\nAsynchronous Background Initialization of Transformers\\nRuntime Status Reporting for Embedding & Re-ranking Models"];
        
        main_py -> config_py;
        main_py -> model_mgr;
    }

    subgraph cluster_routes {
        label = "API Routing Layer (backend/app/api/routes/)";
        style = "dashed";
        color = black;

        r_files [label="files.py\\nPOST /upload\\nGET /{filename}/quality\\nGET /csv/{filename}/data\\nGET /download/{filename}\\nDELETE /{filename}"];
        r_search [label="search.py\\nPOST / (search dispatch)\\nGET /progress (SSE)\\nPOST /cancel\\nGET /results"];
        r_analysis [label="analysis.py\\nPOST /generate\\nGET /{filename}/summary\\nGET /{filename}/matrix\\nGET /{filename}/countries"];
        r_embeddings [label="embeddings.py\\nPOST /{filename}\\nGET /progress\\nPOST /cancel\\nGET /{filename}/status"];
        r_chat [label="chat.py\\nPOST / (RAG query)\\nPOST /{filename}\\nContext synthesis"];
        r_system [label="system.py\\nGET /status\\nRuntime model states"];
    }

    subgraph cluster_services {
        label = "Business Logic & Service Layer (backend/app/services/)";
        style = "dashed";
        color = black;

        s_ingest [label="Ingestion & Normalization\\ndataset_normalizer.py\\ndataset_quality.py\\ncanonical_loader.py"];
        s_search [label="Literature Search Services\\npubmed_service.py\\nopenalex_service.py\\nunified_search_service.py\\nreranker_service.py"];
        s_analytics [label="Bibliometric Analytics\\nanalysis_service.py\\ncountry_service.py\\nutils/country_extractor.py"];
        s_vector [label="Embedding & Chat Services\\nembedding_service.py\\nchat_service.py\\nfeatures/embedding_and_indexing.py"];
    }

    subgraph cluster_data {
        label = "Persistence Layer (data/)";
        style = "dashed";
        color = black;

        csv_files [label="CSV Datasets & Sidecars\\n*.csv | *_canonical_metadata.json"];
        faiss_files [label="Vector Indices & Text Mappings\\n*_paper_chunks_hdbscan.index\\n*_full_text_mapping.json"];
    }

    main_py -> r_files;
    main_py -> r_search;
    main_py -> r_analysis;
    main_py -> r_embeddings;
    main_py -> r_chat;
    main_py -> r_system;

    r_files -> s_ingest;
    r_search -> s_search;
    r_analysis -> s_analytics;
    r_embeddings -> s_vector;
    r_chat -> s_vector;

    s_ingest -> csv_files [dir=both];
    s_search -> csv_files [dir=both];
    s_analytics -> csv_files [dir=both];
    s_vector -> faiss_files [dir=both];
}
"""

# Diagram 4: Installation and Execution Workflow
DOT_FIGURE_4 = """
digraph InstallationWorkflow {
    graph [rankdir=TB, splines=ortho, nodesep=0.4, ranksep=0.45, bgcolor=white, fontname="Times-Roman"];
    node [shape=box, style="solid", color=black, fontcolor=black, fontname="Times-Roman", fontsize=10, margin="0.15,0.08"];
    edge [color=black, fontcolor=black, fontname="Times-Roman", fontsize=9, arrowsize=0.7];

    subgraph cluster_phase1 {
        label = "Phase 1: Repository Retrieval";
        style = "dashed";
        color = black;
        
        step_clone [label="Clone Repository from GitHub\\ngit clone https://github.com/Akashdeep4565/Research_Rover.git\\ncd Research_Rover  (or download and extract ZIP archive)"];
    }

    subgraph cluster_phase2 {
        label = "Phase 2: Backend Setup & Environment Configuration";
        style = "dashed";
        color = black;

        step_b_venv [label="Create Python Virtual Environment (Python 3.11+)\\ncd backend\\npython -m venv .venv"];
        step_b_act [label="Activate Virtual Environment\\nWindows PowerShell: .venv\\Scripts\\Activate.ps1\\nLinux/macOS: source .venv/bin/activate"];
        step_b_req [label="Install Backend Dependencies\\npip install -r requirements.txt (or uv pip install)"];
        step_b_env [label="Configure Environment Variables\\nCopy .env.example to .env\\nSet GOOGLE_GENAI_API_KEY, EMAIL, optional PUBMED_API_KEY"];
        
        step_b_venv -> step_b_act -> step_b_req -> step_b_env;
    }

    subgraph cluster_phase3 {
        label = "Phase 3: Frontend Dependency Installation";
        style = "dashed";
        color = black;

        step_f_cd [label="Navigate to Frontend Directory\\ncd ../frontend"];
        step_f_npm [label="Install Node.js Dependencies (Node.js 18+)\\nnpm install"];
        
        step_f_cd -> step_f_npm;
    }

    subgraph cluster_phase4 {
        label = "Phase 4: Concurrent Application Execution";
        style = "dashed";
        color = black;

        step_run_b [label="Terminal 1: Start FastAPI Backend Server\\ncd backend\\n.venv\\Scripts\\Activate.ps1\\nuvicorn main:app --host 0.0.0.0 --port 8000 --reload"];
        step_run_f [label="Terminal 2: Start Vite Frontend Server\\ncd frontend\\nnpm run dev\\n(Vite dev server starts on http://localhost:3000)"];
    }

    subgraph cluster_phase5 {
        label = "Phase 5: Application Verification & Access";
        style = "dashed";
        color = black;

        step_access [label="Access Application Services in Web Browser\\nFrontend Application: http://localhost:3000\\nBackend REST API & Swagger UI: http://localhost:8000/docs\\nSystem Health Check: http://localhost:8000/health"];
    }

    step_clone -> step_b_venv;
    step_b_env -> step_f_cd;
    step_f_npm -> step_run_b;
    step_f_npm -> step_run_f;
    step_run_b -> step_access;
    step_run_f -> step_access;
}
"""

# Diagram 5: Feature Readiness Workflow
DOT_FIGURE_5 = """
digraph FeatureReadiness {
    graph [rankdir=TB, splines=polyline, nodesep=0.4, ranksep=0.45, bgcolor=white, fontname="Times-Roman"];
    node [shape=box, style="solid", color=black, fontcolor=black, fontname="Times-Roman", fontsize=10, margin="0.15,0.08"];
    edge [color=black, fontcolor=black, fontname="Times-Roman", fontsize=9, arrowsize=0.7];

    input_data [label="Uploaded Research Dataset Records (N) & Mapped Canonical Fields\\ntitle, abstract, keywords, affiliations, authors, year, identifiers (doi/pmid)"];

    subgraph cluster_hygiene {
        label = "Dataset Quality & Completeness Evaluation";
        style = "dashed";
        color = black;

        metric_calc [label="Calculate Field Completeness Metrics (%)\\nCov(Title), Cov(Abstract), Cov(Keywords), Cov(Affil), Cov(Authors), Cov(Year)"];
        index_probe [label="Probe File System for FAISS Dense Vector Index\\nCheck existence of data/{filename}_paper_chunks_hdbscan.index"];
    }

    input_data -> metric_calc;
    input_data -> index_probe;

    subgraph cluster_features {
        label = "Deterministic Seven-Feature Readiness Decision Gates";
        style = "dashed";
        color = black;

        gate_kw [label="keyword_analysis\\nCondition: Cov(Keywords) >= 30% OR Cov(Title) >= 50%"];
        gate_co [label="cooccurrence_analysis\\nCondition: Cov(Keywords) >= 40% AND N >= 3 valid records"];
        gate_country [label="country_analysis\\nCondition: Cov(Affiliations) >= 20%"];
        gate_author [label="author_analysis\\nCondition: Cov(Authors) >= 40%"];
        gate_trend [label="trend_analysis\\nCondition: Cov(Year) >= 50% valid years [1800-2100]"];
        gate_search [label="semantic_search\\nCondition: Cov(Abstract) >= 30% AND FAISS Index Present"];
        gate_rag [label="ai_chat_rag\\nCondition: Cov(Abstract) >= 20% AND FAISS Index Present"];
    }

    metric_calc -> gate_kw;
    metric_calc -> gate_co;
    metric_calc -> gate_country;
    metric_calc -> gate_author;
    metric_calc -> gate_trend;
    metric_calc -> gate_search;
    metric_calc -> gate_rag;
    index_probe -> gate_search;
    index_probe -> gate_rag;

    subgraph cluster_states {
        label = "Tri-State Classification Outputs";
        style = "dashed";
        color = black;

        state_ready [label="State: READY (Status Code: 'ready')\\nAll data completeness thresholds and prerequisite indices satisfied\\nUI: Green checkmark badge; analytical feature fully accessible"];
        state_partial [label="State: PARTIALLY READY (Status Code: 'partially_ready')\\nText data sufficient, but FAISS index missing on disk\\nUI: Amber warning badge with actionable 'Generate Embeddings' button"];
        state_not_ready [label="State: NOT READY (Status Code: 'not_ready')\\nMandatory fields missing or below minimum required coverage threshold\\nUI: Red cross badge with explicit diagnostic failure explanation"];
    }

    gate_kw -> state_ready [label="Pass"];
    gate_kw -> state_not_ready [label="Fail"];

    gate_co -> state_ready [label="Pass"];
    gate_co -> state_not_ready [label="Fail"];

    gate_country -> state_ready [label="Pass"];
    gate_country -> state_not_ready [label="Fail"];

    gate_author -> state_ready [label="Pass"];
    gate_author -> state_not_ready [label="Fail"];

    gate_trend -> state_ready [label="Pass"];
    gate_trend -> state_not_ready [label="Fail"];

    gate_search -> state_ready [label="Abstract & Index OK"];
    gate_search -> state_partial [label="Abstract OK, No Index"];
    gate_search -> state_not_ready [label="Abstract < 30%"];

    gate_rag -> state_ready [label="Abstract & Index OK"];
    gate_rag -> state_partial [label="Abstract OK, No Index"];
    gate_rag -> state_not_ready [label="Abstract < 20%"];
}
"""

DIAGRAMS = [
    ("system_architecture.pdf", DOT_FIGURE_1),
    ("data_ingestion_workflow.pdf", DOT_FIGURE_2),
    ("backend_architecture.pdf", DOT_FIGURE_3),
    ("installation_workflow.pdf", DOT_FIGURE_4),
    ("feature_readiness_workflow.pdf", DOT_FIGURE_5),
]

def generate_diagrams():
    print("Generating monochrome vector PDF diagrams with Graphviz...")
    for filename, dot_src in DIAGRAMS:
        pdf_path = os.path.join(OUTPUT_DIR, filename)
        dot_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".dot"))
        
        # Save .dot source as well for completeness
        with open(dot_path, "w", encoding="utf-8") as f:
            f.write(dot_src.strip())
            
        # Compile directly to PDF using dot -Tpdf
        p = subprocess.run(
            [DOT_EXE, "-Tpdf", "-o", pdf_path],
            input=dot_src.encode("utf-8"),
            capture_output=True
        )
        if p.returncode == 0:
            print(f"  [OK] {filename} ({os.path.getsize(pdf_path):,} bytes)")
        else:
            print(f"  [ERROR] {filename}: {p.stderr.decode('utf-8')}")

if __name__ == "__main__":
    generate_diagrams()
