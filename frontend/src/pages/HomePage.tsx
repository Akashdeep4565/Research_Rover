import { useState, useEffect, useRef } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import {
  MagnifyingGlassIcon,
  ChatBubbleLeftRightIcon,
  DocumentTextIcon,
  CloudArrowDownIcon,
  CpuChipIcon,
  SparklesIcon,
  RocketLaunchIcon,
  ChartBarIcon,
  GlobeAltIcon,
  ArrowUpTrayIcon,
  FunnelIcon,
  ArrowRightIcon,
  ArrowDownTrayIcon,
  CheckCircleIcon,
  ClockIcon,
  XMarkIcon,
} from '@heroicons/react/24/outline'
import { useSystemStatus } from '@/context/SystemStatusContext'
import { useSearch } from '@/context/SearchContext'
import { filesApi, type FileInfo } from '@/services/api'
import { toast } from 'sonner'

// ─── Format Helpers ─────────────────────────────────────────────────────────
function formatFileSize(bytes?: number): string {
  if (!bytes || isNaN(bytes)) return 'Unknown size'
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

function formatDate(dateVal?: string | number): string {
  if (!dateVal) return 'Recently'
  try {
    const d = typeof dateVal === 'number'
      ? (dateVal < 1e12 ? new Date(dateVal * 1000) : new Date(dateVal))
      : new Date(dateVal)
    if (isNaN(d.getTime())) return String(dateVal)
    return d.toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })
  } catch {
    return String(dateVal)
  }
}

// ─── Verified Trending Research Inquiries ────────────────────────────────────
const trendingQueries = [
  { label: 'CRISPR prime editing in vivo', query: 'CRISPR prime editing in vivo', icon: '⚡' },
  { label: 'Glioblastoma microenvironment resistance', query: 'Glioblastoma microenvironment resistance', icon: '🧬' },
  { label: 'Perovskite solar cell degradation', query: 'Perovskite solar cell degradation', icon: '🔬' },
  { label: 'Amyloid-beta clearance pathways', query: 'Amyloid-beta clearance pathways', icon: '🧠' },
  { label: 'CAR-T cell exhaustion mechanisms', query: 'CAR-T cell exhaustion mechanisms', icon: '🛡️' },
]

export function HomePage() {
  const navigate = useNavigate()
  const { apiStatus } = useSystemStatus()
  const { query: contextQuery, setQuery } = useSearch()

  const [localQuery, setLocalQuery] = useState(contextQuery || '')
  const [recentFiles, setRecentFiles] = useState<FileInfo[]>([])
  const [isLoadingFiles, setIsLoadingFiles] = useState(false)
  const searchInputRef = useRef<HTMLInputElement>(null)

  // Sync local query if contextQuery changes externally
  useEffect(() => {
    if (contextQuery && !localQuery) {
      setLocalQuery(contextQuery)
    }
  }, [contextQuery])

  // Fetch real datasets on mount
  const loadRecentFiles = async () => {
    try {
      setIsLoadingFiles(true)
      const list = await filesApi.list()
      const csvFiles = list.filter((f) => f.filename.endsWith('.csv'))
      setRecentFiles(csvFiles)
    } catch {
      // Graceful degradation when offline
    } finally {
      setIsLoadingFiles(false)
    }
  }

  useEffect(() => {
    loadRecentFiles()
  }, [])

  // Keyboard shortcut ⌘K / Ctrl+K
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        searchInputRef.current?.focus()
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  // Download a single file
  const handleDownloadFile = async (filename: string) => {
    try {
      toast.info(`Downloading ${filename}...`)
      const blob = await filesApi.download(filename)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      toast.success(`Downloaded ${filename}`)
    } catch {
      toast.error(`Failed to download ${filename}`)
    }
  }

  // Download latest CSV
  const handleDownloadLatest = async () => {
    try {
      toast.info('Checking available datasets for download...')
      const files = await filesApi.list()
      const csvFiles = files.filter((f) => f.filename.endsWith('.csv'))
      if (csvFiles.length > 0) {
        const latest = csvFiles[0]
        await handleDownloadFile(latest.filename)
      } else {
        toast.info('No dataset files available to download. Search papers or upload a CSV first.')
        navigate('/search')
      }
    } catch {
      toast.error('Failed to download dataset. Navigating to search...')
      navigate('/search')
    }
  }

  // Handle Search Submission
  const handleSearchSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault()
    const q = localQuery.trim()
    if (!q) {
      navigate('/search', { state: { focusSearch: true } })
      return
    }
    setQuery(q)
    navigate('/search', { state: { focusSearch: true } })
  }

  // Handle Trending Query Click
  const handleTrendingClick = (searchQuery: string) => {
    setLocalQuery(searchQuery)
    setQuery(searchQuery)
    navigate('/search', { state: { focusSearch: true } })
  }

  // Preserved Quick Actions
  const quickActions = [
    {
      name: 'New Search',
      description: 'Start a fresh search across PubMed & OpenAlex',
      icon: MagnifyingGlassIcon,
      action: () => navigate('/search', { state: { focusSearch: true } }),
    },
    {
      name: 'Advanced Search',
      description: 'Filter by date range, research sources, and sorting',
      icon: FunnelIcon,
      action: () => navigate('/search', { state: { openAdvancedFilters: true, focusSearch: true } }),
    },
    {
      name: 'Research Analytics',
      description: 'Analyze keyword co-occurrences and frequency trends',
      icon: ChartBarIcon,
      action: () => navigate('/analytics', { state: { tab: 'keywords' } }),
    },
    {
      name: 'Country Analysis',
      description: 'Explore global research collaborations and rankings',
      icon: GlobeAltIcon,
      action: () => navigate('/analytics', { state: { tab: 'country' } }),
    },
    {
      name: 'Upload Dataset',
      description: 'Upload a custom CSV dataset for instant analysis',
      icon: ArrowUpTrayIcon,
      action: () => navigate('/analytics', { state: { triggerUpload: true } }),
    },
    {
      name: 'AI Research Chat',
      description: 'Ask questions and get intelligent answers about papers',
      icon: ChatBubbleLeftRightIcon,
      action: () => navigate('/chat'),
    },
    {
      name: 'Recent Papers',
      description: 'View and select your recently accessed paper datasets',
      icon: DocumentTextIcon,
      action: () => {
        toast.info('Viewing recent datasets & papers...')
        navigate('/analytics', { state: { focusFiles: true } })
      },
    },
    {
      name: 'Download Manager',
      description: 'Export and download research results as CSV',
      icon: CloudArrowDownIcon,
      action: handleDownloadLatest,
    },
    {
      name: 'Vector Embeddings',
      description: 'Create semantic vector embeddings for AI Chat',
      icon: CpuChipIcon,
      action: () => {
        toast.info('Opening Vector Embeddings...')
        navigate('/search', { state: { showEmbeddings: true } })
      },
    },
  ]

  return (
    <div className="relative w-full max-w-7xl mx-auto space-y-16 pb-12">
      {/* ─── Ambient Glow Blobs ──────────────────────────────────────────────── */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden -z-10">
        <div className="absolute -top-32 -left-32 w-96 h-96 rounded-full bg-teal-500/10 dark:bg-teal-500/5 blur-3xl" />
        <div className="absolute top-1/4 -right-24 w-96 h-96 rounded-full bg-indigo-500/10 dark:bg-indigo-500/5 blur-3xl" />
        <div className="absolute bottom-20 left-1/3 w-96 h-96 rounded-full bg-rose-500/5 dark:bg-rose-500/5 blur-3xl" />
      </div>

      {/* ─── 1. HERO SECTION ─────────────────────────────────────────────────── */}
      <motion.section
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="text-center pt-6 sm:pt-10 pb-4 max-w-4xl mx-auto"
      >
        {/* Live Eyebrow Pill */}
        <div className="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl border border-slate-200/80 dark:border-slate-800 shadow-sm text-xs font-medium text-slate-700 dark:text-slate-300 mb-6">
          <span className="relative flex h-2 w-2">
            <span
              className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
                apiStatus === 'online' ? 'bg-emerald-400' : apiStatus === 'offline' ? 'bg-rose-400' : 'bg-amber-400'
              }`}
            />
            <span
              className={`relative inline-flex rounded-full h-2 w-2 ${
                apiStatus === 'online' ? 'bg-emerald-500' : apiStatus === 'offline' ? 'bg-rose-500' : 'bg-amber-500'
              }`}
            />
          </span>
          <span className="font-semibold text-slate-900 dark:text-slate-100">
            {apiStatus === 'online' ? 'API Online' : apiStatus === 'offline' ? 'API Offline' : 'Checking API…'}
          </span>
          <span className="text-slate-300 dark:text-slate-700">•</span>
          <span className="flex items-center gap-1 text-slate-600 dark:text-slate-400">
            <SparklesIcon className="w-3.5 h-3.5 text-indigo-500" />
            Unified PubMed &amp; OpenAlex
          </span>
        </div>

        {/* Flagship Headline */}
        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-slate-900 dark:text-slate-50 leading-[1.12] mb-5">
          Discover, analyze, and synthesize research with{' '}
          <span className="bg-gradient-to-r from-indigo-600 via-indigo-500 to-teal-500 dark:from-indigo-400 dark:via-indigo-300 dark:to-teal-300 bg-clip-text text-transparent">
            AI &amp; MedCPT
          </span>
        </h1>

        {/* Subtitle */}
        <p className="text-base sm:text-lg text-slate-600 dark:text-slate-300 max-w-2xl mx-auto leading-relaxed">
          Federated academic literature search across NIH PubMed and OpenAlex, coupled with keyword co-occurrence analytics and grounded conversational AI.
        </p>
      </motion.section>

      {/* ─── 2. DUAL-MODAL ENTRY DOCK (Search + Upload) ──────────────────────── */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1, duration: 0.4 }}
        className="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-5 items-stretch"
      >
        {/* Left: Omni-Search Bar (8 Cols) */}
        <div className="lg:col-span-8 bg-white/85 dark:bg-slate-900/85 backdrop-blur-2xl p-6 sm:p-7 rounded-3xl border border-slate-200/70 dark:border-slate-800/80 shadow-xl shadow-indigo-500/5 flex flex-col justify-between transition-all duration-300 hover:shadow-2xl">
          <div>
            <div className="flex items-center justify-between pb-3 mb-2">
              <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                <MagnifyingGlassIcon className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                Semantic Query Matrix
              </span>
              <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
                MedCPT Semantic Re-ranking
              </span>
            </div>

            {/* Interactive Search Input Form */}
            <form onSubmit={handleSearchSubmit} className="relative group mt-1">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400 group-focus-within:text-indigo-600 transition-colors">
                <MagnifyingGlassIcon className="w-5 h-5" />
              </div>
              <input
                ref={searchInputRef}
                type="text"
                value={localQuery}
                onChange={(e) => setLocalQuery(e.target.value)}
                placeholder="Search topics, hypotheses, PMIDs, or DOIs…"
                className="w-full pl-11 pr-28 py-3.5 bg-slate-50/80 dark:bg-slate-800/60 hover:bg-slate-100/80 dark:hover:bg-slate-800 text-slate-900 dark:text-slate-100 text-sm sm:text-base rounded-2xl border border-slate-200/80 dark:border-slate-700/80 outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white dark:focus:bg-slate-900 transition-all placeholder:text-slate-400"
              />
              <div className="absolute inset-y-0 right-2 flex items-center gap-1.5">
                {localQuery && (
                  <button
                    type="button"
                    onClick={() => {
                      setLocalQuery('')
                      searchInputRef.current?.focus()
                    }}
                    className="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors"
                  >
                    <XMarkIcon className="w-4 h-4" />
                  </button>
                )}
                <kbd className="hidden sm:inline-flex items-center px-2 py-1 bg-slate-200/60 dark:bg-slate-700/60 text-slate-500 dark:text-slate-400 text-xs font-mono rounded-lg">
                  ⌘K
                </kbd>
                <Button
                  type="submit"
                  size="sm"
                  className="h-9 px-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl shadow-md text-xs font-semibold"
                >
                  Explore
                  <ArrowRightIcon className="w-3.5 h-3.5 ml-1" />
                </Button>
              </div>
            </form>

            {/* Trending Inquiries Presets */}
            <div className="mt-4 flex flex-wrap items-center gap-1.5 pt-1">
              <span className="text-xs text-slate-400 dark:text-slate-500 mr-1 font-medium">
                Trending inquiries:
              </span>
              {trendingQueries.map((t) => (
                <button
                  key={t.label}
                  type="button"
                  onClick={() => handleTrendingClick(t.query)}
                  className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium bg-slate-100 hover:bg-indigo-50 hover:text-indigo-600 dark:bg-slate-800/70 dark:hover:bg-indigo-950/40 dark:hover:text-indigo-300 text-slate-600 dark:text-slate-300 border border-slate-200/60 dark:border-slate-700/60 transition-all"
                >
                  <span>{t.icon}</span>
                  <span>{t.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Micro Status Bar */}
          <div className="pt-4 mt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
            <span className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              Unified Deduplication &amp; Semantic Ranking
            </span>
            <span className="hidden sm:inline text-slate-400 dark:text-slate-500">
              PubMed Central + OpenAlex Ingestion
            </span>
          </div>
        </div>

        {/* Right: Drop Research Corpus Card (4 Cols) */}
        <div
          onClick={() => navigate('/analytics', { state: { triggerUpload: true } })}
          className="lg:col-span-4 bg-gradient-to-br from-white/95 via-slate-50/80 to-indigo-50/40 dark:from-slate-900/95 dark:via-slate-900/80 dark:to-indigo-950/30 backdrop-blur-2xl p-6 sm:p-7 rounded-3xl border border-slate-200/70 dark:border-slate-800/80 shadow-xl shadow-indigo-500/5 flex flex-col justify-between group cursor-pointer hover:border-indigo-400/50 hover:shadow-2xl transition-all duration-300"
        >
          <div className="flex flex-col items-center text-center p-4 rounded-2xl bg-white/60 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-800/60 group-hover:bg-white/90 dark:group-hover:bg-slate-800/70 transition-colors">
            <div className="w-14 h-14 rounded-2xl bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400 flex items-center justify-center group-hover:scale-105 group-hover:bg-indigo-600 group-hover:text-white transition-all shadow-sm">
              <ArrowUpTrayIcon className="w-7 h-7" />
            </div>
            <h3 className="mt-4 font-bold text-base text-slate-900 dark:text-slate-100">
              Import Research Corpus
            </h3>
            <p className="mt-1 text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              Upload custom <strong className="font-semibold text-slate-800 dark:text-slate-200">CSV datasets</strong> for immediate keyword co-occurrence, country analysis, and AI chat.
            </p>
            <span className="mt-3 inline-flex items-center gap-1 px-3 py-1 rounded-full bg-teal-50 dark:bg-teal-950/40 text-teal-700 dark:text-teal-300 border border-teal-200/60 dark:border-teal-800/50 text-xs font-semibold">
              <CheckCircleIcon className="w-3.5 h-3.5" />
              Automated Analysis Ingest
            </span>
          </div>

          <div className="pt-4 flex items-center justify-center gap-1.5 text-xs font-semibold text-indigo-600 dark:text-indigo-400 group-hover:translate-x-0.5 transition-transform">
            <span>Upload CSV Dataset</span>
            <ArrowRightIcon className="w-3.5 h-3.5" />
          </div>
        </div>
      </motion.section>

      {/* ─── 3. THREE-COLUMN PLATFORM CAPABILITY SHOWCASE ───────────────────── */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.4 }}
        className="space-y-6"
      >
        <div className="text-center max-w-2xl mx-auto">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-300 text-xs font-semibold mb-2">
            <CpuChipIcon className="w-3.5 h-3.5" />
            Scholarly Intelligence Suite
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-slate-100 tracking-tight">
            Engineered for Scholarly Discovery
          </h2>
          <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
            Replace manual literature parsing with federated discovery, keyword co-occurrence networks, and grounded conversational analysis.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Capability 1: Federated Literature Search */}
          <Card className="rounded-3xl border border-slate-200/70 dark:border-slate-800 shadow-md hover:shadow-xl transition-all duration-300 flex flex-col justify-between bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl">
            <CardContent className="p-6 flex flex-col justify-between h-full space-y-4">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 rounded-2xl bg-teal-100 dark:bg-teal-900/40 text-teal-600 dark:text-teal-300 flex items-center justify-center">
                    <MagnifyingGlassIcon className="w-6 h-6" />
                  </div>
                  <span className="px-3 py-1 rounded-full bg-teal-50 dark:bg-teal-950/50 text-teal-700 dark:text-teal-300 border border-teal-200/50 dark:border-teal-800 text-xs font-semibold">
                    PubMed + OpenAlex
                  </span>
                </div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                  Cross-Repository Federation
                </h3>
                <p className="mt-1.5 text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
                  Unified multi-source search across NIH PubMed Central and OpenAlex with automatic deduplication, MedCPT semantic match ranking, and direct PDF downloads.
                </p>

                {/* Sub-feature chips */}
                <div className="mt-4 flex flex-wrap gap-1.5">
                  <span className="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-medium">
                    Unified Search
                  </span>
                  <span className="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-medium">
                    MedCPT Re-ranking
                  </span>
                  <span className="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-medium">
                    PDF Downloads
                  </span>
                </div>
              </div>

              <div className="pt-2">
                <Link to="/search">
                  <Button variant="outline" size="sm" className="w-full justify-between rounded-xl">
                    <span>Start Searching</span>
                    <ArrowRightIcon className="w-3.5 h-3.5" />
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>

          {/* Capability 2: Topological & Keyword Analytics */}
          <Card className="rounded-3xl border border-slate-200/70 dark:border-slate-800 shadow-md hover:shadow-xl transition-all duration-300 flex flex-col justify-between bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl">
            <CardContent className="p-6 flex flex-col justify-between h-full space-y-4">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 rounded-2xl bg-indigo-100 dark:bg-indigo-900/40 text-indigo-600 dark:text-indigo-300 flex items-center justify-center">
                    <ChartBarIcon className="w-6 h-6" />
                  </div>
                  <span className="px-3 py-1 rounded-full bg-indigo-50 dark:bg-indigo-950/50 text-indigo-700 dark:text-indigo-300 border border-indigo-200/50 dark:border-indigo-800 text-xs font-semibold">
                    Network Science
                  </span>
                </div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                  Keyword &amp; Author Analytics
                </h3>
                <p className="mt-1.5 text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
                  Compute co-occurrence matrices, author affiliation clusters, and interactive global country collaboration choropleth maps from structured literature datasets.
                </p>

                {/* Sub-feature chips */}
                <div className="mt-4 flex flex-wrap gap-1.5">
                  <span className="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-medium">
                    Co-Occurrence Matrix
                  </span>
                  <span className="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-medium">
                    Country Rankings
                  </span>
                  <span className="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-medium">
                    CSV Export
                  </span>
                </div>
              </div>

              <div className="pt-2">
                <Link to="/analytics">
                  <Button variant="outline" size="sm" className="w-full justify-between rounded-xl">
                    <span>Explore Analytics</span>
                    <ArrowRightIcon className="w-3.5 h-3.5" />
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>

          {/* Capability 3: Grounded Literature Chat */}
          <Card className="rounded-3xl border border-slate-200/70 dark:border-slate-800 shadow-md hover:shadow-xl transition-all duration-300 flex flex-col justify-between bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl">
            <CardContent className="p-6 flex flex-col justify-between h-full space-y-4">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 rounded-2xl bg-rose-100 dark:bg-rose-900/40 text-rose-600 dark:text-rose-300 flex items-center justify-center">
                    <ChatBubbleLeftRightIcon className="w-6 h-6" />
                  </div>
                  <span className="px-3 py-1 rounded-full bg-rose-50 dark:bg-rose-950/50 text-rose-700 dark:text-rose-300 border border-rose-200/50 dark:border-rose-800 text-xs font-semibold">
                    Grounded RAG
                  </span>
                </div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                  Dataset-Grounded AI Chat
                </h3>
                <p className="mt-1.5 text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
                  Engage in multi-turn dialogues grounded in your selected research corpora, backed by semantic vector embeddings and verifiable inline source citations.
                </p>

                {/* Sub-feature chips */}
                <div className="mt-4 flex flex-wrap gap-1.5">
                  <span className="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-medium">
                    Vector Indexing
                  </span>
                  <span className="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-medium">
                    Real-time Streaming
                  </span>
                  <span className="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-medium">
                    Verified Citations
                  </span>
                </div>
              </div>

              <div className="pt-2">
                <Link to="/chat">
                  <Button variant="outline" size="sm" className="w-full justify-between rounded-xl">
                    <span>Try AI Chat</span>
                    <ArrowRightIcon className="w-3.5 h-3.5" />
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>
      </motion.section>

      {/* ─── 4. RECENT DATASETS SECTION (Real filesApi.list Data) ────────────── */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.4 }}
        className="space-y-5"
      >
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
              <DocumentTextIcon className="w-3.5 h-3.5 text-indigo-500" />
              Stateful Research Memory
            </div>
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-slate-100">
              Recent Research Datasets
            </h2>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleDownloadLatest}
              className="rounded-xl text-xs"
            >
              <ArrowDownTrayIcon className="w-3.5 h-3.5 mr-1" />
              Download Latest CSV
            </Button>
            <Button
              size="sm"
              onClick={() => navigate('/analytics', { state: { triggerUpload: true } })}
              className="rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs"
            >
              <ArrowUpTrayIcon className="w-3.5 h-3.5 mr-1" />
              Upload Dataset
            </Button>
          </div>
        </div>

        {/* Real Dataset Cards Grid */}
        {recentFiles.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {recentFiles.slice(0, 6).map((file) => (
              <Card
                key={file.filename}
                className="rounded-2xl border border-slate-200/70 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl shadow-sm hover:shadow-md transition-all group flex flex-col justify-between"
              >
                <CardContent className="p-5 space-y-3">
                  <div className="flex items-start justify-between gap-2">
                    <div className="w-9 h-9 rounded-xl bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 flex items-center justify-center shrink-0">
                      <DocumentTextIcon className="w-5 h-5" />
                    </div>
                    <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
                      {formatFileSize(file.size)}
                    </span>
                  </div>

                  <div>
                    <h3
                      className="font-semibold text-sm text-slate-900 dark:text-slate-100 truncate group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors"
                      title={file.filename}
                    >
                      {file.filename}
                    </h3>
                    <div className="flex items-center gap-1.5 text-xs text-slate-500 mt-1">
                      <ClockIcon className="w-3.5 h-3.5" />
                      <span>{formatDate(file.created_at)}</span>
                    </div>
                  </div>

                  <div className="pt-2 flex items-center justify-between border-t border-slate-100 dark:border-slate-800">
                    <button
                      type="button"
                      onClick={() => navigate('/analytics', { state: { filename: file.filename } })}
                      className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1"
                    >
                      <span>Analyze</span>
                      <ArrowRightIcon className="w-3 h-3" />
                    </button>
                    <button
                      type="button"
                      onClick={() => handleDownloadFile(file.filename)}
                      className="inline-flex items-center gap-1 text-xs text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 transition-colors"
                      title="Download CSV"
                    >
                      <ArrowDownTrayIcon className="w-3.5 h-3.5" />
                      <span>Download</span>
                    </button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <div className="p-8 text-center rounded-2xl border border-dashed border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/30">
            <DocumentTextIcon className="w-10 h-10 text-slate-300 dark:text-slate-600 mx-auto mb-2" />
            <h3 className="font-semibold text-sm text-slate-700 dark:text-slate-300">
              {isLoadingFiles ? 'Loading saved datasets…' : 'No datasets saved yet'}
            </h3>
            <p className="text-xs text-slate-500 max-w-md mx-auto mt-1">
              Datasets are automatically saved when you perform a research search or upload a CSV file.
            </p>
            <div className="mt-4 flex items-center justify-center gap-2">
              <Button
                size="sm"
                variant="outline"
                onClick={() => navigate('/search')}
                className="rounded-xl text-xs"
              >
                <RocketLaunchIcon className="w-3.5 h-3.5 mr-1" />
                Start a Search
              </Button>
            </div>
          </div>
        )}
      </motion.section>

      {/* ─── 5. QUICK ACTIONS GRID ───────────────────────────────────────────── */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.4 }}
        className="space-y-5"
      >
        <div className="text-center sm:text-left">
          <div className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
            <RocketLaunchIcon className="w-3.5 h-3.5 text-indigo-500" />
            Productivity Shortcuts
          </div>
          <h2 className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-slate-100">
            Platform Quick Actions
          </h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {quickActions.map((action) => (
            <Card
              key={action.name}
              onClick={action.action}
              className="cursor-pointer hover:shadow-md hover:border-indigo-300/50 dark:hover:border-indigo-700/50 transition-all duration-200 rounded-2xl border border-slate-200/70 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl group"
            >
              <CardContent className="p-4 sm:p-5 flex items-center space-x-4">
                <div className="w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-800/80 flex items-center justify-center text-slate-600 dark:text-slate-300 group-hover:bg-indigo-50 dark:group-hover:bg-indigo-950/60 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors shrink-0">
                  <action.icon className="w-5 h-5" />
                </div>
                <div className="min-w-0 flex-1">
                  <h3 className="font-semibold text-sm text-slate-900 dark:text-slate-100 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                    {action.name}
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400 line-clamp-1">
                    {action.description}
                  </p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </motion.section>
    </div>
  )
}
