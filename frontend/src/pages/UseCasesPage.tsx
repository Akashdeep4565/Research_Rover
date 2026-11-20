import { useState } from 'react'
import { motion } from 'framer-motion'
import {
  DocumentChartBarIcon,
  CheckBadgeIcon,
  ArrowDownTrayIcon,
  CommandLineIcon,
  InformationCircleIcon,
  MagnifyingGlassIcon,
  ArrowsPointingOutIcon,
  ClipboardDocumentCheckIcon,
  ClipboardIcon,
  SparklesIcon,
} from '@heroicons/react/24/outline'
import { toast } from 'sonner'

interface UseCaseItem {
  id: string
  name: string
  group: 'Search' | 'Dataset' | 'Keyword' | 'Country' | 'AI'
  type: 'Base' | '<<include>>' | '<<extend>>' | 'Generalization'
  relatedTo: string
  codeFile: string
  description: string
}

const USE_CASE_DATA: UseCaseItem[] = [
  // Group A: Search
  {
    id: 'UC-S1',
    name: 'Search Research Papers',
    group: 'Search',
    type: 'Base',
    relatedTo: 'Researcher / Student',
    codeFile: 'backend/app/api/routes/search.py',
    description: 'Entry-point search workflow accepting search query string, data source, and query parameters.',
  },
  {
    id: 'UC-S2',
    name: 'Execute Unified Search',
    group: 'Search',
    type: 'Generalization',
    relatedTo: 'Search Research Papers',
    codeFile: 'backend/app/services/unified_search.py',
    description: 'Concurrent asynchronous querying across both PubMed (biomedical) and OpenAlex (multidisciplinary) databases.',
  },
  {
    id: 'UC-S3',
    name: 'Execute PubMed Search',
    group: 'Search',
    type: 'Generalization',
    relatedTo: 'Search Research Papers',
    codeFile: 'backend/app/services/pubmed_service.py',
    description: 'Queries NCBI Entrez E-Utilities (esearch, efetch) with MeSH medical subject terms and boolean operators.',
  },
  {
    id: 'UC-S4',
    name: 'Execute OpenAlex Search',
    group: 'Search',
    type: 'Generalization',
    relatedTo: 'Search Research Papers',
    codeFile: 'backend/app/services/openalex_service.py',
    description: 'Queries OpenAlex API with inverted index abstract reconstruction and open-access PDF URL extraction.',
  },
  {
    id: 'UC-S5',
    name: 'Optimize & Expand Query',
    group: 'Search',
    type: '<<include>>',
    relatedTo: 'Search Research Papers',
    codeFile: 'backend/app/services/query_optimizer.py',
    description: 'Mandatory preprocessing that expands scientific acronyms (e.g. ml -> machine learning, dl -> deep learning, iiot).',
  },
  {
    id: 'UC-S6',
    name: 'Browse Search Results',
    group: 'Search',
    type: '<<include>>',
    relatedTo: 'Search Research Papers',
    codeFile: 'frontend/src/pages/SearchPage.tsx',
    description: 'Mandatory visualization of retrieved paper metadata cards with pagination, match score, citations, and authors.',
  },
  {
    id: 'UC-S7',
    name: 'Apply Advanced Search Filters',
    group: 'Search',
    type: '<<extend>>',
    relatedTo: 'Search Research Papers',
    codeFile: 'frontend/src/context/SearchContext.tsx',
    description: 'Optional filtering by publication year range slider (1990-2026), result limit, and relevance sorting mode.',
  },
  {
    id: 'UC-S8',
    name: 'Re-Rank by Semantic Relevance',
    group: 'Search',
    type: '<<extend>>',
    relatedTo: 'Search Research Papers',
    codeFile: 'backend/app/services/pubmed_service.py',
    description: 'Optional deep semantic re-ranking using MedCPT Bi-Encoder neural model to score title/abstract similarity.',
  },
  {
    id: 'UC-S9',
    name: 'Download Available PDF',
    group: 'Search',
    type: '<<extend>>',
    relatedTo: 'Browse Search Results',
    codeFile: 'backend/app/api/routes/pdf.py',
    description: 'Conditional full-text PDF download piped through an SSRF-protected streaming proxy when open_access_pdf is present.',
  },
  {
    id: 'UC-S10',
    name: 'View Paper on Publisher Site',
    group: 'Search',
    type: '<<extend>>',
    relatedTo: 'Browse Search Results',
    codeFile: 'frontend/src/pages/SearchPage.tsx',
    description: 'External navigation to DOI or publisher web page for licensed paywalled papers.',
  },
  {
    id: 'UC-S11',
    name: 'Cancel In-Flight Search',
    group: 'Search',
    type: 'Base',
    relatedTo: 'Researcher / Student',
    codeFile: 'backend/app/api/routes/search.py',
    description: 'Cooperative cancellation token interrupting thread pools during long API fetches.',
  },

  // Group B: Dataset Management
  {
    id: 'UC-D1',
    name: 'Upload Custom Dataset',
    group: 'Dataset',
    type: 'Base',
    relatedTo: 'Researcher / Student',
    codeFile: 'backend/app/api/routes/files.py',
    description: 'Upload custom bibliographic CSV with automatic charset encoding detection and mandatory column schema validation.',
  },
  {
    id: 'UC-D2',
    name: 'List & Switch Datasets',
    group: 'Dataset',
    type: 'Base',
    relatedTo: 'Researcher / Student',
    codeFile: 'backend/app/api/routes/files.py',
    description: 'Dynamic auto-discovery of all CSV corpora in data/ with active dataset selection for analytics & RAG.',
  },
  {
    id: 'UC-D3',
    name: 'Export Clean Dataset CSV',
    group: 'Dataset',
    type: 'Base',
    relatedTo: 'Researcher / Student',
    codeFile: 'backend/app/api/routes/files.py',
    description: 'Downloads clean curated CSV containing metadata while stripping bloated scraped full-text cache columns.',
  },
  {
    id: 'UC-D4',
    name: 'Delete Dataset & Embeddings',
    group: 'Dataset',
    type: 'Base',
    relatedTo: 'Researcher / Student',
    codeFile: 'backend/app/api/routes/files.py',
    description: 'Permanently removes dataset CSV file, associated FAISS vector indexes, and chunk metadata pickles from disk.',
  },

  // Group C: Keyword Analytics
  {
    id: 'UC-K1',
    name: 'Analyse Keywords',
    group: 'Keyword',
    type: 'Base',
    relatedTo: 'Researcher / Student',
    codeFile: 'backend/app/services/keyword_service.py',
    description: 'Executes comprehensive 5-phase bibliometric pipeline generating keyword co-occurrences and centrality rankings.',
  },
  {
    id: 'UC-K2',
    name: 'Normalize Keywords & Resolve Aliases',
    group: 'Keyword',
    type: '<<include>>',
    relatedTo: 'Analyse Keywords',
    codeFile: 'backend/app/services/keyword_service.py',
    description: 'Mandatory normalization using AST string literal parsing, punctuation cleaning, and domain synonym deduplication.',
  },
  {
    id: 'UC-K3',
    name: 'View Frequency & Distribution Bars',
    group: 'Keyword',
    type: '<<include>>',
    relatedTo: 'Analyse Keywords',
    codeFile: 'frontend/src/pages/AnalyticsPage.tsx',
    description: 'Interactive distribution chart of top-N keyword occurrences with minimum frequency cutoff sliders.',
  },
  {
    id: 'UC-K4',
    name: 'Compute NetworkX Centrality Scores',
    group: 'Keyword',
    type: '<<include>>',
    relatedTo: 'Analyse Keywords',
    codeFile: 'backend/app/services/keyword_service.py',
    description: 'Calculates graph-theoretic metrics: Degree, Closeness, Betweenness, Eigenvector centrality, and Clustering coefficients.',
  },
  {
    id: 'UC-K5',
    name: 'Inspect Binary Presence Matrix',
    group: 'Keyword',
    type: '<<include>>',
    relatedTo: 'Analyse Keywords',
    codeFile: 'backend/app/services/keyword_service.py',
    description: 'Generates boolean 0/1 incidence matrix of papers vs extracted keywords for clustering and verification.',
  },
  {
    id: 'UC-K6',
    name: 'Explore Interactive SVG Word Cloud',
    group: 'Keyword',
    type: '<<extend>>',
    relatedTo: 'Analyse Keywords',
    codeFile: 'frontend/src/pages/AnalyticsPage.tsx',
    description: 'Interactive SVG word cloud with frequency-weighted font sizing, tooltips, pan/zoom, and PNG export.',
  },
  {
    id: 'UC-K7',
    name: 'Explore Co-Occurrence Network Graph',
    group: 'Keyword',
    type: '<<extend>>',
    relatedTo: 'Analyse Keywords',
    codeFile: 'frontend/src/pages/AnalyticsPage.tsx',
    description: 'Force-directed graph of pairwise keyword co-occurrence frequencies with node sizing by centrality.',
  },
  {
    id: 'UC-K8',
    name: 'Export Keyword Analytics Artifacts',
    group: 'Keyword',
    type: '<<extend>>',
    relatedTo: 'Analyse Keywords',
    codeFile: 'frontend/src/pages/AnalyticsPage.tsx',
    description: 'One-click export of keyword frequency CSV, co-occurrence matrix CSV, JSON metrics, and SVG/PNG visuals.',
  },

  // Group D: Country Analysis
  {
    id: 'UC-C1',
    name: 'Perform Country Bibliometric Analysis',
    group: 'Country',
    type: 'Base',
    relatedTo: 'Researcher / Student',
    codeFile: 'backend/app/services/country_service.py',
    description: 'Parses author affiliation metadata to map global publication distribution and bilateral international collaborations.',
  },
  {
    id: 'UC-C2',
    name: 'Extract Affiliations & Resolve ISO Countries',
    group: 'Country',
    type: '<<include>>',
    relatedTo: 'Perform Country Bibliometric Analysis',
    codeFile: 'backend/app/services/country_service.py',
    description: 'Mandatory regex parsing against ISO-3166-1 country names, alpha codes, and major research institutions.',
  },
  {
    id: 'UC-C3',
    name: 'Track & Inspect Unassigned Papers',
    group: 'Country',
    type: '<<include>>',
    relatedTo: 'Perform Country Bibliometric Analysis',
    codeFile: 'frontend/src/components/CountryAnalysisView.tsx',
    description: 'Mandatory audit trail retaining unparseable affiliations without fabricating artificial country labels.',
  },
  {
    id: 'UC-C4',
    name: 'View Country Rankings & Statistics',
    group: 'Country',
    type: '<<include>>',
    relatedTo: 'Perform Country Bibliometric Analysis',
    codeFile: 'frontend/src/components/CountryAnalysisView.tsx',
    description: 'Searchable tabular ranking of countries by paper volume, total affiliations, and global percentage share.',
  },
  {
    id: 'UC-C5',
    name: 'Explore TopoJSON Geographic World Map',
    group: 'Country',
    type: '<<extend>>',
    relatedTo: 'Perform Country Bibliometric Analysis',
    codeFile: 'frontend/src/components/WorldMap.tsx',
    description: 'Choropleth geographic map color-coded by country publication density with hover tooltips.',
  },
  {
    id: 'UC-C6',
    name: 'Explore International Collaboration Networks',
    group: 'Country',
    type: '<<extend>>',
    relatedTo: 'Perform Country Bibliometric Analysis',
    codeFile: 'frontend/src/components/CountryCollaboration2D.tsx',
    description: 'Interactive 2D D3 force-directed and 3D Three.js orbital graphs showing cross-border co-authorship links.',
  },
  {
    id: 'UC-C7',
    name: 'Export Country Data & Partnerships',
    group: 'Country',
    type: '<<extend>>',
    relatedTo: 'Perform Country Bibliometric Analysis',
    codeFile: 'frontend/src/components/CountryAnalysisView.tsx',
    description: 'Downloads CSV exports for country publication rankings and bilateral collaboration dyads.',
  },

  // Group E: AI Research Assistant (RAG)
  {
    id: 'UC-A1',
    name: 'Generate Vector Embeddings',
    group: 'AI',
    type: 'Base',
    relatedTo: 'Researcher / Student',
    codeFile: 'backend/app/services/embedding_service.py',
    description: 'Encodes paper abstracts into 768-dimensional dense vector embeddings using SentenceTransformer all-mpnet-base-v2.',
  },
  {
    id: 'UC-A2',
    name: 'Scrape Full-Text Content from URLs',
    group: 'AI',
    type: '<<extend>>',
    relatedTo: 'Generate Vector Embeddings',
    codeFile: 'backend/app/services/scraper_service.py',
    description: 'Optional deep scraping of publisher HTML/PDF with polite User-Agent headers, falling back gracefully to abstract.',
  },
  {
    id: 'UC-A3',
    name: 'Ask Research Questions (AI Chat)',
    group: 'AI',
    type: 'Base',
    relatedTo: 'Researcher / Student',
    codeFile: 'backend/app/services/chat_service.py',
    description: 'Multi-turn conversational Q&A grounded strictly in the active dataset using Retrieval-Augmented Generation (RAG).',
  },
  {
    id: 'UC-A4',
    name: 'Decompose Complex Query',
    group: 'AI',
    type: '<<include>>',
    relatedTo: 'Ask Research Questions',
    codeFile: 'backend/app/services/chat_service.py',
    description: 'Breaks complex research inquiries into targeted sub-queries to maximize vector retrieval recall across distinct angles.',
  },
  {
    id: 'UC-A5',
    name: 'Retrieve Semantic Context from FAISS',
    group: 'AI',
    type: '<<include>>',
    relatedTo: 'Ask Research Questions',
    codeFile: 'backend/app/services/embedding_service.py',
    description: 'Performs nearest-neighbor vector search in FAISS with deduplication across chunks and distance thresholding.',
  },
  {
    id: 'UC-A6',
    name: 'Synthesize Grounded Response with Citations',
    group: 'AI',
    type: '<<include>>',
    relatedTo: 'Ask Research Questions',
    codeFile: 'backend/app/services/chat_service.py',
    description: 'Prompts Google Gemini with retrieved paper chunks to produce evidence-grounded answers with verifiable citations.',
  },
  {
    id: 'UC-A7',
    name: 'View AI Responses with Cited Sources',
    group: 'AI',
    type: '<<include>>',
    relatedTo: 'Ask Research Questions',
    codeFile: 'frontend/src/pages/ChatPage.tsx',
    description: 'Displays streamed Markdown response alongside interactive citation chips linking back to paper cards.',
  },
]

const SIMPLE_PLANTUML_CODE = `@startuml Research_Rover_Simple_User_Use_Case_Diagram
' ==============================================================================
' Project: Research Rover
' Diagram: Simple User Use Case Diagram
' Reference Style: University Management System Use Case Diagram
' ==============================================================================

skinparam backgroundColor #FFFFFF
skinparam handwritten false
skinparam monochrome false
skinparam shadowing false
skinparam defaultFontName "Segoe UI", Arial, Helvetica, sans-serif
skinparam defaultFontSize 13
skinparam defaultFontColor #0F172A

skinparam actor {
    BackgroundColor #EFF6FF
    BorderColor #1D4ED8
    BorderThickness 2
    FontColor #0F172A
    FontSize 14
    FontStyle bold
}

skinparam rectangle {
    BackgroundColor #FFFFFF
    BorderColor #2563EB
    BorderThickness 2.5
    FontColor #1D4ED8
    FontSize 16
    FontStyle bold
}

skinparam usecase {
    BackgroundColor #F8FAFC
    BorderColor #2563EB
    BorderThickness 1.8
    FontColor #0F172A
    FontSize 12.5
    FontStyle bold
    ArrowColor #3B82F6
    ArrowThickness 1.5
}

left to right direction

actor "Researcher / Student" as User

rectangle "Research Rover" {
    usecase "Search Research Papers" as UC_Search
    usecase "Explore Research Papers" as UC_ExplorePapers
    usecase "View Paper Details" as UC_PaperDetails
    usecase "Download Research Papers" as UC_DownloadPaper
    
    usecase "Upload Dataset" as UC_UploadData
    usecase "View My Datasets" as UC_ViewData
    usecase "Select Dataset" as UC_SelectData
    usecase "Download Dataset" as UC_DownloadData
    
    usecase "Explore Keywords" as UC_Keywords
    usecase "View Popular Keywords" as UC_PopularKW
    usecase "Explore Keyword Connections" as UC_KWConnections
    usecase "View Keyword Networks" as UC_KWNetworks
    
    usecase "Explore Countries" as UC_Countries
    usecase "View Country Rankings" as UC_CountryRank
    usecase "Explore World Map" as UC_WorldMap
    usecase "View International Collaborations" as UC_Collaborations
    
    usecase "Ask Questions" as UC_AskAI
    usecase "Get AI Answers" as UC_AIAnswers
    usecase "Explore Research Information" as UC_ResearchInfo
    
    usecase "Download Charts" as UC_DownloadCharts
    usecase "Export Reports" as UC_ExportReports
}

User -- UC_Search
User -- UC_ExplorePapers
User -- UC_PaperDetails
User -- UC_DownloadPaper

User -- UC_UploadData
User -- UC_ViewData
User -- UC_SelectData
User -- UC_DownloadData

User -- UC_Keywords
User -- UC_PopularKW
User -- UC_KWConnections
User -- UC_KWNetworks

User -- UC_Countries
User -- UC_CountryRank
User -- UC_WorldMap
User -- UC_Collaborations

User -- UC_AskAI
User -- UC_AIAnswers
User -- UC_ResearchInfo

User -- UC_DownloadCharts
User -- UC_ExportReports
@enduml`

const DETAILED_PLANTUML_CODE = `@startuml Research_Rover_Use_Case_Diagram
skinparam backgroundColor #FFFFFF
skinparam defaultFontName "Segoe UI", Arial, sans-serif
left to right direction

actor "Researcher / Student\\n<<Primary Human Actor>>" as User

actor "NCBI Entrez API\\n<<External System>>" as NCBI
actor "OpenAlex API\\n<<External System>>" as OpenAlex
actor "Publisher / PMC Host\\n<<External System>>" as Publisher
actor "Google Gemini AI\\n<<External System>>" as Gemini

rectangle "Research Rover" {
    package "Research Paper Search" {
        usecase "Search Research Papers" as UC_Search
        usecase "Execute Unified Search" as UC_Unified
        usecase "Execute PubMed Search" as UC_PubMed
        usecase "Execute OpenAlex Search" as UC_OpenAlex
        usecase "Optimize & Expand Query" as UC_QueryOpt
        usecase "Apply Search Filters" as UC_Filters
        usecase "Re-Rank by Relevance" as UC_Rerank
        usecase "Browse Search Results" as UC_Browse
        usecase "Download Available PDF" as UC_PDF
        usecase "Cancel In-Flight Search" as UC_Cancel
    }

    package "Dataset Management" {
        usecase "Upload Custom Dataset" as UC_Upload
        usecase "List Available Datasets" as UC_ListDatasets
        usecase "Export Clean Dataset CSV" as UC_ExportCSV
        usecase "Delete Dataset & Embeddings" as UC_DeleteDataset
    }

    package "Keyword Analytics" {
        usecase "Analyse Keywords" as UC_AnalyzeKW
        usecase "Normalize Keywords & Aliases" as UC_NormKW
        usecase "View Frequency & Distribution" as UC_FreqKW
        usecase "Compute NetworkX Centrality" as UC_Centrality
        usecase "Inspect Binary Presence Matrix" as UC_PresenceMatrix
        usecase "Explore SVG Word Cloud" as UC_WordCloud
        usecase "Explore Co-Occurrence Graph" as UC_CooccurGraph
        usecase "Export Keyword Artifacts" as UC_ExportKW
    }

    package "Country Analysis" {
        usecase "Perform Country Analysis" as UC_AnalyzeCountry
        usecase "Extract Affiliations & Countries" as UC_ExtractCountry
        usecase "Track Unassigned Papers" as UC_Unassigned
        usecase "View Country Rankings" as UC_CountryRank
        usecase "Explore TopoJSON World Map" as UC_WorldMap
        usecase "Explore Collaboration Networks" as UC_CollabNet
        usecase "Export Country Data" as UC_ExportCountry
    }

    package "AI Research Assistant" {
        usecase "Generate Vector Embeddings" as UC_Embed
        usecase "Scrape Full-Text Content" as UC_Scrape
        usecase "Ask Research Questions" as UC_AskAI
        usecase "Decompose Complex Query" as UC_Decompose
        usecase "Retrieve Context from FAISS" as UC_FAISS
        usecase "Synthesize Grounded Response" as UC_Synthesize
        usecase "View AI Responses with Sources" as UC_ViewAIResponse
    }
}

' Actor Associations
User -- UC_Search
User -- UC_Cancel
User -- UC_Browse
User -- UC_PDF
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
User -- UC_Embed
User -- UC_AskAI
User -- UC_ViewAIResponse

' Generalization
UC_Unified -up-|> UC_Search
UC_PubMed -up-|> UC_Search
UC_OpenAlex -up-|> UC_Search

' Includes & Extends
UC_Search ..> UC_QueryOpt : <<include>>
UC_Search ..> UC_Browse : <<include>>
UC_Filters ..> UC_Search : <<extend>>
UC_Rerank ..> UC_Search : <<extend>>
UC_PDF ..> UC_Browse : <<extend>>

UC_AnalyzeKW ..> UC_NormKW : <<include>>
UC_AnalyzeKW ..> UC_FreqKW : <<include>>
UC_AnalyzeKW ..> UC_Centrality : <<include>>
UC_AnalyzeKW ..> UC_PresenceMatrix : <<include>>
UC_WordCloud ..> UC_AnalyzeKW : <<extend>>
UC_CooccurGraph ..> UC_AnalyzeKW : <<extend>>
UC_ExportKW ..> UC_AnalyzeKW : <<extend>>

UC_AnalyzeCountry ..> UC_ExtractCountry : <<include>>
UC_AnalyzeCountry ..> UC_Unassigned : <<include>>
UC_CountryRank ..> UC_AnalyzeCountry : <<include>>
UC_WorldMap ..> UC_AnalyzeCountry : <<extend>>
UC_CollabNet ..> UC_AnalyzeCountry : <<extend>>
UC_ExportCountry ..> UC_AnalyzeCountry : <<extend>>

UC_Embed <.. UC_Scrape : <<extend>>
UC_AskAI ..> UC_Decompose : <<include>>
UC_AskAI ..> UC_FAISS : <<include>>
UC_AskAI ..> UC_Synthesize : <<include>>
UC_AskAI ..> UC_ViewAIResponse : <<include>>

' External Actors
UC_Search -- NCBI
UC_Search -- OpenAlex
UC_PDF -- Publisher
UC_Synthesize -- Gemini
@enduml`

export function UseCasesPage() {
  const [activeTab, setActiveTab] = useState<'diagram' | 'inventory' | 'relationships' | 'plantuml'>('diagram')
  const [diagramMode, setDiagramMode] = useState<'simple' | 'detailed'>('simple')
  const [viewFormat, setViewFormat] = useState<'svg' | 'png'>('svg')
  const [searchFilter, setSearchFilter] = useState('')
  const [groupFilter, setGroupFilter] = useState<string>('all')
  const [copied, setCopied] = useState(false)

  const handleCopyPlantUML = async () => {
    try {
      const fileName = diagramMode === 'simple' 
        ? '/assets/uml/Research_Rover_Simple_User_Use_Case_Diagram.puml'
        : '/assets/uml/Research_Rover_Use_Case_Diagram.puml'
      const response = await fetch(fileName)
      const text = await response.text()
      await navigator.clipboard.writeText(text)
      setCopied(true)
      toast.success('PlantUML code copied to clipboard!')
      setTimeout(() => setCopied(false), 2500)
    } catch {
      toast.error('Failed to copy PlantUML code.')
    }
  }

  const filteredUseCases = USE_CASE_DATA.filter((item) => {
    const matchesSearch =
      item.name.toLowerCase().includes(searchFilter.toLowerCase()) ||
      item.description.toLowerCase().includes(searchFilter.toLowerCase()) ||
      item.codeFile.toLowerCase().includes(searchFilter.toLowerCase())
    const matchesGroup = groupFilter === 'all' || item.group === groupFilter
    return matchesSearch && matchesGroup
  })

  return (
    <div className="space-y-10 pb-16 max-w-7xl mx-auto px-4 sm:px-6">
      {/* ── HERO BANNER ── */}
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative overflow-hidden rounded-3xl border border-gray-200 dark:border-slate-800 bg-gradient-to-br from-blue-500/10 via-indigo-500/5 to-cyan-500/10 p-8 sm:p-12 shadow-sm"
      >
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-3 max-w-3xl">
            <div className="flex flex-wrap items-center gap-2">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-blue-100 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300">
                <DocumentChartBarIcon className="h-4 w-4" />
                UML 2.5 Specification
              </span>
              <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300">
                <CheckBadgeIcon className="h-4 w-4" />
                100% Codebase Verified
              </span>
              <span className="px-3 py-1 rounded-full text-xs font-mono bg-white/70 dark:bg-slate-800 text-gray-700 dark:text-gray-300">
                M.Tech Project Specification
              </span>
            </div>

            <h1 className="text-3xl sm:text-5xl font-black tracking-tight text-gray-900 dark:text-white">
              System <span className="gradient-text">Use Cases</span>
            </h1>

            <p className="text-sm sm:text-base text-gray-600 dark:text-gray-300 leading-relaxed">
              Explore the complete, traditional UML Use Case model for Research Rover. Built following strict UML 2.5 conventions: separating the primary human actor (Researcher / Student) on the left, an explicit <strong>Research Rover</strong> system boundary in the centre with oval use cases, and four external interacting systems on the right.
            </p>
          </div>

          {/* Quick Metrics */}
          <div className="grid grid-cols-2 gap-3 shrink-0">
            <div className="p-4 rounded-2xl bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm border border-gray-200 dark:border-slate-800 text-center shadow-xs">
              <div className="text-2xl font-black text-blue-600 dark:text-blue-400">37</div>
              <div className="text-xs text-gray-500 font-medium">Verified Use Cases</div>
            </div>
            <div className="p-4 rounded-2xl bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm border border-gray-200 dark:border-slate-800 text-center shadow-xs">
              <div className="text-2xl font-black text-emerald-600 dark:text-emerald-400">300 DPI</div>
              <div className="text-xs text-gray-500 font-medium">High-Res PNG &amp; SVG</div>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex items-center gap-2 mt-8 pt-6 border-t border-gray-200/60 dark:border-slate-800 overflow-x-auto">
          <button
            type="button"
            onClick={() => setActiveTab('diagram')}
            className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all shrink-0 ${
              activeTab === 'diagram'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-gray-600 dark:text-gray-300 hover:bg-white/60 dark:hover:bg-slate-800'
            }`}
          >
            UML Diagram Viewer
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('inventory')}
            className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all shrink-0 ${
              activeTab === 'inventory'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-gray-600 dark:text-gray-300 hover:bg-white/60 dark:hover:bg-slate-800'
            }`}
          >
            Use Case Inventory (37)
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('relationships')}
            className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all shrink-0 ${
              activeTab === 'relationships'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-gray-600 dark:text-gray-300 hover:bg-white/60 dark:hover:bg-slate-800'
            }`}
          >
            UML Relationships &amp; Defense Notes
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('plantuml')}
            className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all shrink-0 ${
              activeTab === 'plantuml'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-gray-600 dark:text-gray-300 hover:bg-white/60 dark:hover:bg-slate-800'
            }`}
          >
            PlantUML Source Code
          </button>
        </div>
      </motion.div>

      {/* ── TAB 1: DIAGRAM VIEWER ── */}
      {activeTab === 'diagram' && (
        <div className="space-y-6">
          {/* Diagram Mode Switcher Banner */}
          <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-2xl bg-gradient-to-r from-blue-50/80 via-indigo-50/50 to-slate-50 dark:from-slate-900 dark:via-slate-900 dark:to-slate-950 border border-blue-200/80 dark:border-slate-800 shadow-xs">
            <div className="flex items-center gap-3">
              <span className="text-xs font-bold text-blue-900 dark:text-blue-300 uppercase tracking-wider">Diagram Style:</span>
              <div className="inline-flex rounded-xl p-1 bg-white dark:bg-slate-800 border border-blue-200 dark:border-slate-700 shadow-xs">
                <button
                  type="button"
                  onClick={() => setDiagramMode('simple')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    diagramMode === 'simple'
                      ? 'bg-blue-600 text-white shadow-xs'
                      : 'text-gray-600 dark:text-gray-300 hover:text-blue-600'
                  }`}
                >
                  Simple User Model (EdrawMax Style)
                </button>
                <button
                  type="button"
                  onClick={() => setDiagramMode('detailed')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    diagramMode === 'detailed'
                      ? 'bg-blue-600 text-white shadow-xs'
                      : 'text-gray-600 dark:text-gray-300 hover:text-blue-600'
                  }`}
                >
                  Detailed Engineering Model (UML 2.5)
                </button>
              </div>
            </div>
            <div className="text-xs text-slate-600 dark:text-slate-400 font-medium">
              {diagramMode === 'simple' 
                ? '21 Student & Researcher Features • 1 Boundary (Research Rover) • 0 Technical Jargon' 
                : '37 Verified Use Cases • 5 Subsystem Modules • 4 External APIs'}
            </div>
          </div>

          {/* Action Toolbar */}
          <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 shadow-xs">
            <div className="flex items-center gap-3">
              <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Format:</span>
              <div className="inline-flex rounded-xl p-1 bg-gray-100 dark:bg-slate-800">
                <button
                  type="button"
                  onClick={() => setViewFormat('svg')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    viewFormat === 'svg'
                      ? 'bg-white dark:bg-slate-700 text-blue-600 dark:text-blue-400 shadow-xs'
                      : 'text-gray-600 dark:text-gray-300'
                  }`}
                >
                  Interactive Vector (SVG)
                </button>
                <button
                  type="button"
                  onClick={() => setViewFormat('png')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    viewFormat === 'png'
                      ? 'bg-white dark:bg-slate-700 text-blue-600 dark:text-blue-400 shadow-xs'
                      : 'text-gray-600 dark:text-gray-300'
                  }`}
                >
                  High-Resolution (300 DPI PNG)
                </button>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <a
                href={
                  diagramMode === 'simple'
                    ? '/assets/uml/Research_Rover_Simple_User_Use_Case_Diagram.png'
                    : '/assets/uml/Research_Rover_Use_Case_Diagram.png'
                }
                download={
                  diagramMode === 'simple'
                    ? 'Research_Rover_Simple_User_Use_Case_Diagram.png'
                    : 'Research_Rover_Use_Case_Diagram.png'
                }
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold bg-emerald-50 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 hover:bg-emerald-100 transition-colors"
              >
                <ArrowDownTrayIcon className="h-4 w-4" />
                Download 300 DPI PNG
              </a>
              <a
                href={
                  diagramMode === 'simple'
                    ? '/assets/uml/Research_Rover_Simple_User_Use_Case_Diagram.pdf'
                    : '/assets/uml/Research_Rover_Use_Case_Diagram.pdf'
                }
                download={
                  diagramMode === 'simple'
                    ? 'Research_Rover_Simple_User_Use_Case_Diagram.pdf'
                    : 'Research_Rover_Use_Case_Diagram.pdf'
                }
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold bg-purple-50 text-purple-700 dark:bg-purple-950 dark:text-purple-300 border border-purple-200 dark:border-purple-800 hover:bg-purple-100 transition-colors"
              >
                <ArrowDownTrayIcon className="h-4 w-4" />
                Download Vector PDF
              </a>
              <a
                href={
                  diagramMode === 'simple'
                    ? '/assets/uml/Research_Rover_Simple_User_Use_Case_Diagram.svg'
                    : '/assets/uml/Research_Rover_Use_Case_Diagram.svg'
                }
                download={
                  diagramMode === 'simple'
                    ? 'Research_Rover_Simple_User_Use_Case_Diagram.svg'
                    : 'Research_Rover_Use_Case_Diagram.svg'
                }
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold bg-blue-50 text-blue-700 dark:bg-blue-950 dark:text-blue-300 border border-blue-200 dark:border-blue-800 hover:bg-blue-100 transition-colors"
              >
                <ArrowDownTrayIcon className="h-4 w-4" />
                Download SVG
              </a>
              <a
                href={
                  diagramMode === 'simple'
                    ? '/assets/uml/Research_Rover_Simple_User_Use_Case_Diagram.puml'
                    : '/assets/uml/Research_Rover_Use_Case_Diagram.puml'
                }
                download={
                  diagramMode === 'simple'
                    ? 'Research_Rover_Simple_User_Use_Case_Diagram.puml'
                    : 'Research_Rover_Use_Case_Diagram.puml'
                }
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border border-slate-300 dark:border-slate-700 hover:bg-slate-200 transition-colors"
              >
                <CommandLineIcon className="h-4 w-4" />
                PlantUML File
              </a>
            </div>
          </div>

          {/* Diagram Display Box */}
          <div className="overflow-hidden rounded-3xl border border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 sm:p-6 shadow-md">
            <div className="flex items-center justify-between pb-4 mb-4 border-b border-gray-100 dark:border-slate-800 text-xs text-gray-500">
              <span className="flex items-center gap-1.5 font-medium">
                <InformationCircleIcon className="h-4 w-4 text-blue-500" />
                {diagramMode === 'simple'
                  ? 'University Management Reference Style: Single Actor (Left) • Single System Boundary: Research Rover (Centre) • 21 Student Features'
                  : 'Standard UML 2.5: Primary Actor (Left) • System Boundary: Research Rover (Centre) • External Systems (Right)'}
              </span>
              <a
                href={
                  diagramMode === 'simple'
                    ? viewFormat === 'svg'
                      ? '/assets/uml/Research_Rover_Simple_User_Use_Case_Diagram.svg'
                      : '/assets/uml/Research_Rover_Simple_User_Use_Case_Diagram.png'
                    : viewFormat === 'svg'
                    ? '/assets/uml/Research_Rover_Use_Case_Diagram.svg'
                    : '/assets/uml/Research_Rover_Use_Case_Diagram.png'
                }
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1 text-blue-600 dark:text-blue-400 hover:underline font-semibold"
              >
                <ArrowsPointingOutIcon className="h-3.5 w-3.5" />
                Open Fullscreen
              </a>
            </div>

            <div className="w-full overflow-x-auto flex justify-center">
              <img
                src={
                  diagramMode === 'simple'
                    ? viewFormat === 'svg'
                      ? '/assets/uml/Research_Rover_Simple_User_Use_Case_Diagram.svg'
                      : '/assets/uml/Research_Rover_Simple_User_Use_Case_Diagram.png'
                    : viewFormat === 'svg'
                    ? '/assets/uml/Research_Rover_Use_Case_Diagram.svg'
                    : '/assets/uml/Research_Rover_Use_Case_Diagram.png'
                }
                alt={
                  diagramMode === 'simple'
                    ? 'Research Rover Simple User Use Case Diagram'
                    : 'Research Rover UML 2.5 Use Case Diagram'
                }
                className="w-full max-w-6xl h-auto rounded-xl object-contain shadow-xs border border-gray-100 dark:border-slate-800"
              />
            </div>
          </div>
        </div>
      )}

      {/* ── TAB 2: USE CASE INVENTORY ── */}
      {activeTab === 'inventory' && (
        <div className="space-y-6">
          {/* Filter Bar */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 shadow-xs">
            <div className="relative w-full sm:w-80">
              <MagnifyingGlassIcon className="absolute left-3.5 top-3 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search use cases, files, keywords..."
                value={searchFilter}
                onChange={(e) => setSearchFilter(e.target.value)}
                className="w-full pl-9 pr-4 py-2 rounded-xl text-xs bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="flex items-center gap-2 overflow-x-auto w-full sm:w-auto">
              {['all', 'Search', 'Dataset', 'Keyword', 'Country', 'AI'].map((grp) => (
                <button
                  key={grp}
                  type="button"
                  onClick={() => setGroupFilter(grp)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all shrink-0 ${
                    groupFilter === grp
                      ? 'bg-blue-600 text-white shadow-xs'
                      : 'bg-gray-100 dark:bg-slate-800 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-slate-700'
                  }`}
                >
                  {grp === 'all' ? 'All Groups' : grp}
                </button>
              ))}
            </div>
          </div>

          {/* Table */}
          <div className="overflow-hidden rounded-2xl border border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-gray-50 dark:bg-slate-800/80 text-gray-700 dark:text-gray-300 font-bold border-b border-gray-200 dark:border-slate-800 uppercase tracking-wider">
                  <tr>
                    <th className="py-3 px-4">ID</th>
                    <th className="py-3 px-4">Use Case Name</th>
                    <th className="py-3 px-4">Module Group</th>
                    <th className="py-3 px-4">UML Relationship</th>
                    <th className="py-3 px-4">Related Node</th>
                    <th className="py-3 px-4">Verified Source File</th>
                    <th className="py-3 px-4">Description</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100 dark:divide-slate-800">
                  {filteredUseCases.map((item) => (
                    <tr key={item.id} className="hover:bg-gray-50/60 dark:hover:bg-slate-800/50 transition-colors">
                      <td className="py-3 px-4 font-mono font-bold text-gray-500">{item.id}</td>
                      <td className="py-3 px-4 font-bold text-gray-900 dark:text-white">{item.name}</td>
                      <td className="py-3 px-4">
                        <span className={`inline-block px-2 py-0.5 rounded-md text-[11px] font-semibold ${
                          item.group === 'Search' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300' :
                          item.group === 'Dataset' ? 'bg-sky-100 text-sky-800 dark:bg-sky-900/40 dark:text-sky-300' :
                          item.group === 'Keyword' ? 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900/40 dark:text-indigo-300' :
                          item.group === 'Country' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' :
                          'bg-purple-100 text-purple-800 dark:bg-purple-900/40 dark:text-purple-300'
                        }`}>
                          {item.group}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <span className={`inline-block px-2 py-0.5 rounded-md font-mono text-[11px] font-bold ${
                          item.type === 'Base' ? 'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300' :
                          item.type === '<<include>>' ? 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300' :
                          item.type === '<<extend>>' ? 'bg-rose-100 text-rose-800 dark:bg-rose-900/40 dark:text-rose-300' :
                          'bg-cyan-100 text-cyan-800 dark:bg-cyan-900/40 dark:text-cyan-300'
                        }`}>
                          {item.type}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-gray-600 dark:text-gray-300 font-medium">{item.relatedTo}</td>
                      <td className="py-3 px-4 font-mono text-[11px] text-blue-600 dark:text-blue-400">{item.codeFile}</td>
                      <td className="py-3 px-4 text-gray-600 dark:text-gray-300 leading-relaxed max-w-sm">{item.description}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ── TAB 3: RELATIONSHIPS & DEFENSE NOTES ── */}
      {activeTab === 'relationships' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 space-y-4 shadow-xs">
            <div className="flex items-center gap-2 text-blue-600 dark:text-blue-400 font-bold text-base">
              <SparklesIcon className="h-5 w-5" />
              Actors Specification
            </div>
            <div className="space-y-3 text-xs text-gray-600 dark:text-gray-300 leading-relaxed">
              <div className="p-3 rounded-xl bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-900">
                <div className="font-bold text-blue-900 dark:text-blue-200">1. Researcher / Student (Primary Human Actor)</div>
                <div className="mt-1">Placed outside the system boundary on the left. Initiates search queries, uploads CSV datasets, interacts with analytics charts, and questions the RAG AI assistant.</div>
              </div>
              <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700">
                <div className="font-bold text-slate-900 dark:text-slate-200">2. External Systems (Right-side Actors)</div>
                <ul className="list-disc pl-4 mt-1 space-y-1">
                  <li><strong>NCBI Entrez API:</strong> Provides biomedical paper citations, abstracts, and MeSH terms.</li>
                  <li><strong>OpenAlex API:</strong> Multidisciplinary index providing citation counts and open-access URLs.</li>
                  <li><strong>Publishers &amp; PMC:</strong> Direct hosts from which full-text PDFs are streamed.</li>
                  <li><strong>Google Gemini AI:</strong> External generative model providing grounded responses.</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 space-y-4 shadow-xs">
            <div className="flex items-center gap-2 text-indigo-600 dark:text-indigo-400 font-bold text-base">
              <InformationCircleIcon className="h-5 w-5" />
              UML Relationship Rationales
            </div>
            <div className="space-y-3 text-xs text-gray-600 dark:text-gray-300 leading-relaxed">
              <div className="p-3 rounded-xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-900">
                <div className="font-bold text-amber-900 dark:text-amber-200">&lt;&lt;include&gt;&gt; Mandatory Inclusions</div>
                <div className="mt-1">Dashed arrows pointing from base use case to included use case. Used when behaviour is unconditionally executed: query optimization and result browsing are mandatory parts of Search; normalization is mandatory in Keyword Analysis; FAISS retrieval is mandatory in AI Chat.</div>
              </div>
              <div className="p-3 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900">
                <div className="font-bold text-rose-900 dark:text-rose-200">&lt;&lt;extend&gt;&gt; Optional / Conditional Extensions</div>
                <div className="mt-1">Dashed arrows pointing from extending use case back to base use case. Used when behaviour is conditional: PDF download only occurs if an open-access link exists; MedCPT re-ranking occurs only when enabled; Word Cloud is an interactive visual extension.</div>
              </div>
              <div className="p-3 rounded-xl bg-cyan-50 dark:bg-cyan-950/40 border border-cyan-200 dark:border-cyan-900">
                <div className="font-bold text-cyan-900 dark:text-cyan-200">Generalization (Search Specialization)</div>
                <div className="mt-1">Solid line with hollow triangular arrowhead pointing to the base parent. Unified Search, PubMed Search, and OpenAlex Search specialize the abstract Search Research Papers parent use case.</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ── TAB 4: PLANTUML SOURCE CODE ── */}
      {activeTab === 'plantuml' && (
        <div className="space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800">
            <div>
              <div className="text-sm font-bold text-gray-900 dark:text-white">
                {diagramMode === 'simple'
                  ? 'PlantUML Source: Simple User Model (21 Use Cases)'
                  : 'PlantUML Source: Detailed Engineering Model (37 Use Cases)'}
              </div>
              <div className="text-xs text-gray-500">
                {diagramMode === 'simple'
                  ? 'Plain-English student & researcher use cases, single system boundary, clean association lines.'
                  : 'Detailed specification with <<include>>, <<extend>>, generalizations, and external system actors.'}
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="inline-flex rounded-xl p-1 bg-gray-100 dark:bg-slate-800 border border-gray-200 dark:border-slate-700">
                <button
                  type="button"
                  onClick={() => setDiagramMode('simple')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    diagramMode === 'simple'
                      ? 'bg-blue-600 text-white shadow-xs'
                      : 'text-gray-600 dark:text-gray-300 hover:text-blue-600'
                  }`}
                >
                  Simple Model
                </button>
                <button
                  type="button"
                  onClick={() => setDiagramMode('detailed')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    diagramMode === 'detailed'
                      ? 'bg-blue-600 text-white shadow-xs'
                      : 'text-gray-600 dark:text-gray-300 hover:text-blue-600'
                  }`}
                >
                  Engineering Model
                </button>
              </div>

              <button
                type="button"
                onClick={handleCopyPlantUML}
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold bg-blue-600 text-white hover:bg-blue-700 transition-colors shadow-xs"
              >
                {copied ? <ClipboardDocumentCheckIcon className="h-4 w-4" /> : <ClipboardIcon className="h-4 w-4" />}
                {copied ? 'Copied!' : 'Copy PlantUML Code'}
              </button>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-950 text-slate-200 font-mono text-xs overflow-x-auto max-h-[600px] border border-slate-800">
            <pre className="leading-relaxed">
              {diagramMode === 'simple' ? SIMPLE_PLANTUML_CODE : DETAILED_PLANTUML_CODE}
            </pre>
          </div>
        </div>
      )}
    </div>
  )
}
