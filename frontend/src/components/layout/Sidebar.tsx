import { Link, useLocation, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { useSystemStatus } from '@/context/SystemStatusContext'
import { useSidebar } from '@/context/SidebarContext'
import { filesApi } from '@/services/api'
import { toast } from 'sonner'
import {
  HomeIcon,
  MagnifyingGlassIcon,
  ChatBubbleLeftRightIcon,
  ChartBarIcon,
  DocumentTextIcon,
  FolderIcon,
  CloudArrowDownIcon,
  CpuChipIcon,
  ArrowUpTrayIcon,
  GlobeAltIcon,
  XMarkIcon,
  Bars3Icon,
} from '@heroicons/react/24/outline'

const sidebarItems = [
  {
    name: 'Home',
    href: '/',
    icon: HomeIcon,
  },
  {
    name: 'Search Papers',
    href: '/search',
    icon: MagnifyingGlassIcon,
  },
  {
    name: 'Analysis',
    href: '/analytics',
    icon: ChartBarIcon,
  },
  {
    name: 'AI Chat',
    href: '/chat',
    icon: ChatBubbleLeftRightIcon,
  },
]

export function Sidebar() {
  const location = useLocation()
  const navigate = useNavigate()
  const { isCollapsed, toggleCollapse, isMobileOpen, closeMobile } = useSidebar()
  const { apiStatus, modelStatus, details } = useSystemStatus()

  const handleDownloadLatest = async () => {
    try {
      toast.info('Checking available datasets for download...')
      const files = await filesApi.list()
      const csvFiles = files.filter((f) => f.filename.endsWith('.csv'))
      if (csvFiles.length > 0) {
        const latest = csvFiles[0]
        const blob = await filesApi.download(latest.filename)
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = latest.filename
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
        toast.success(`Downloaded ${latest.filename}`)
      } else {
        toast.info('No dataset files available to download. Search papers or upload a CSV first.')
        navigate('/search')
      }
    } catch {
      toast.error('Failed to download dataset. Navigating to search...')
      navigate('/search')
    }
  }

  const quickActions = [
    {
      name: 'Recent Files',
      icon: DocumentTextIcon,
      action: () => {
        toast.info('Viewing recent datasets & files...')
        navigate('/analytics', { state: { tab: 'keywords', focusFiles: true } })
      },
    },
    {
      name: 'File Manager',
      icon: FolderIcon,
      action: () => {
        toast.info('Opening Dataset & File Manager...')
        navigate('/analytics', { state: { tab: 'keywords' } })
      },
    },
    {
      name: 'Downloads',
      icon: CloudArrowDownIcon,
      action: handleDownloadLatest,
    },
    {
      name: 'Embeddings',
      icon: CpuChipIcon,
      action: () => {
        toast.info('Opening Vector Embeddings...')
        navigate('/search', { state: { showEmbeddings: true } })
      },
    },
    {
      name: 'Upload CSV',
      icon: ArrowUpTrayIcon,
      action: () => {
        toast.info('Opening dataset upload...')
        navigate('/analytics', { state: { triggerUpload: true } })
      },
    },
    {
      name: 'Country Analysis',
      icon: GlobeAltIcon,
      action: () => {
        navigate('/analytics', { state: { tab: 'country' } })
      },
    },
  ]

  const statusTooltip = (() => {
    if (apiStatus === 'offline') return 'Backend API is unreachable (Offline).'
    if (!details?.models?.components) return 'API is online. Checking model readiness...'
    const comps = details.models.components
    const parts: string[] = []
    if (comps.embedding) parts.push(`Embedding (${comps.embedding.name}): ${comps.embedding.status}`)
    if (comps.reranker && comps.reranker.status !== 'disabled') parts.push(`Re-Ranker: ${comps.reranker.status}`)
    if (comps.llm) parts.push(`LLM (${comps.llm.name}): ${comps.llm.status}`)
    return parts.join(' • ')
  })()

  // Full detailed status card (used in expanded desktop mode and mobile drawer)
  const renderDetailedStatusCard = () => (
    <div
      className="p-3.5 bg-surface-container-low/80 dark:bg-slate-800/60 rounded-2xl border border-outline-variant/30 shadow-sm transition-all"
      title={statusTooltip}
    >
      <div className="flex items-center justify-between mb-2.5">
        <h4 className="text-xs font-semibold text-on-surface uppercase tracking-wider font-mono">
          System Status
        </h4>
        <span className="w-1.5 h-1.5 rounded-full bg-secondary" />
      </div>
      <div className="space-y-2 text-xs">
        {/* API Status Row */}
        <div className="flex items-center justify-between">
          <span className="text-on-surface-variant font-medium">FastAPI Engine</span>
          <div className="flex items-center gap-1.5">
            <span
              className={`w-2 h-2 rounded-full ${
                apiStatus === 'online'
                  ? 'bg-emerald-500'
                  : apiStatus === 'offline'
                  ? 'bg-rose-500'
                  : 'bg-amber-500 animate-pulse'
              }`}
            />
            <span
              className={`text-xs font-medium ${
                apiStatus === 'online'
                  ? 'text-emerald-600 dark:text-emerald-400'
                  : apiStatus === 'offline'
                  ? 'text-rose-600 dark:text-rose-400'
                  : 'text-amber-600 dark:text-amber-400'
              }`}
            >
              {apiStatus === 'online' ? 'Online' : apiStatus === 'offline' ? 'Offline' : 'Checking'}
            </span>
          </div>
        </div>

        {/* Model Status Row */}
        <div className="flex items-center justify-between">
          <span className="text-on-surface-variant font-medium">Model Pipeline</span>
          <div className="flex items-center gap-1.5">
            <span
              className={`w-2 h-2 rounded-full ${
                modelStatus === 'loaded'
                  ? 'bg-emerald-500'
                  : modelStatus === 'loading'
                  ? 'bg-amber-500 animate-pulse'
                  : modelStatus === 'partial'
                  ? 'bg-amber-500'
                  : modelStatus === 'not_loaded' || modelStatus === 'error'
                  ? 'bg-rose-500'
                  : 'bg-amber-500 animate-pulse'
              }`}
            />
            <span
              className={`text-xs font-medium ${
                modelStatus === 'loaded'
                  ? 'text-emerald-600 dark:text-emerald-400'
                  : modelStatus === 'loading' || modelStatus === 'partial'
                  ? 'text-amber-600 dark:text-amber-400'
                  : modelStatus === 'not_loaded' || modelStatus === 'error'
                  ? 'text-rose-600 dark:text-rose-400'
                  : 'text-amber-600 dark:text-amber-400'
              }`}
            >
              {modelStatus === 'loaded'
                ? 'Ready'
                : modelStatus === 'loading'
                ? 'Loading'
                : modelStatus === 'partial'
                ? 'Partial'
                : modelStatus === 'not_loaded' || modelStatus === 'error'
                ? 'Offline'
                : 'Checking'}
            </span>
          </div>
        </div>
      </div>
    </div>
  )

  return (
    <>
      {/* ── Desktop Sidebar (Expanded or Icon-only Rail) ── */}
      <aside
        className={`fixed left-0 top-16 h-[calc(100vh-4rem)] bg-surface-container-lowest/85 dark:bg-slate-900/85 backdrop-blur-xl border-r border-outline-variant/30 shadow-card transition-all duration-300 ease-in-out z-30 hidden md:flex md:flex-col ${
          isCollapsed ? 'w-20' : 'w-64'
        }`}
      >
        {isCollapsed ? (
          /* Collapsed Desktop View (Icon-only Rail) */
          <div className="p-3 flex flex-col items-center h-full overflow-y-auto custom-scrollbar">
            {/* Toggle Button */}
            <button
              type="button"
              onClick={toggleCollapse}
              className="p-2 mb-4 rounded-full text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high/60 transition-colors focus:outline-none focus:ring-2 focus:ring-primary/40"
              title="Expand sidebar"
              aria-label="Expand sidebar"
            >
              <Bars3Icon className="h-5 w-5" />
            </button>

            {/* Navigation Icons */}
            <nav className="space-y-2 w-full flex flex-col items-center">
              {sidebarItems.map((item) => {
                const isActive = location.pathname === item.href
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    title={item.name}
                    className={`relative flex items-center justify-center w-11 h-11 rounded-full transition-all duration-200 ${
                      isActive
                        ? 'bg-primary-fixed text-primary dark:bg-primary-container dark:text-white shadow-sm'
                        : 'text-on-surface-variant hover:bg-surface-container-high/60 hover:text-on-surface'
                    }`}
                  >
                    <item.icon className="h-5 w-5" />
                    {isActive && (
                      <div className="absolute right-1 top-3 bottom-3 w-1 bg-primary rounded-full" />
                    )}
                  </Link>
                )
              })}
            </nav>

            {/* Quick Actions Icons */}
            <div className="mt-6 w-full flex flex-col items-center space-y-2 pt-4 border-t border-outline-variant/30">
              {quickActions.map((action) => (
                <button
                  key={action.name}
                  type="button"
                  onClick={action.action}
                  title={action.name}
                  className="flex items-center justify-center w-11 h-11 rounded-full text-on-surface-variant hover:bg-surface-container-high/60 hover:text-on-surface transition-all duration-200"
                >
                  <action.icon className="h-5 w-5" />
                </button>
              ))}
            </div>

            {/* Compact System Status Indicator */}
            <div
              className="mt-auto w-full flex flex-col items-center pt-4 border-t border-outline-variant/30 pb-2"
              title={`System Status\n• API: ${apiStatus}\n• Models: ${modelStatus}\n${statusTooltip}`}
            >
              <div className="flex flex-col items-center gap-1.5 p-2 rounded-full bg-surface-container-low/80 dark:bg-slate-800/60 border border-outline-variant/30 cursor-help">
                <span
                  className={`w-2.5 h-2.5 rounded-full ${
                    apiStatus === 'online'
                      ? 'bg-emerald-500'
                      : apiStatus === 'offline'
                      ? 'bg-rose-500'
                      : 'bg-amber-500 animate-pulse'
                  }`}
                  title={`API: ${apiStatus}`}
                />
                <span
                  className={`w-2.5 h-2.5 rounded-full ${
                    modelStatus === 'loaded'
                      ? 'bg-emerald-500'
                      : modelStatus === 'loading' || modelStatus === 'partial'
                      ? 'bg-amber-500 animate-pulse'
                      : 'bg-rose-500'
                  }`}
                  title={`Models: ${modelStatus}`}
                />
              </div>
            </div>
          </div>
        ) : (
          /* Expanded Desktop View */
          <div className="p-5 flex flex-col h-full overflow-y-auto custom-scrollbar">
            {/* Header / Collapse Bar */}
            <div className="flex items-center justify-between mb-4 px-1">
              <h3 className="text-xs font-semibold text-on-surface-variant uppercase tracking-wider font-mono">
                Workspace
              </h3>
              <button
                type="button"
                onClick={toggleCollapse}
                className="p-1.5 rounded-full text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high/60 transition-colors focus:outline-none"
                title="Collapse sidebar"
                aria-label="Collapse sidebar"
              >
                <Bars3Icon className="h-4 w-4" />
              </button>
            </div>

            {/* Navigation Links */}
            <nav className="space-y-1">
              {sidebarItems.map((item) => {
                const isActive = location.pathname === item.href
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`flex items-center px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                      isActive
                        ? 'bg-primary-fixed text-primary dark:bg-primary-container dark:text-white font-semibold shadow-sm'
                        : 'text-on-surface-variant hover:bg-surface-container-high/60 hover:text-on-surface'
                    }`}
                  >
                    <item.icon className="mr-3 h-5 w-5 shrink-0" />
                    <span>{item.name}</span>
                    {isActive && (
                      <motion.div
                        layoutId="sidebar-indicator"
                        className="ml-auto w-1 h-5 bg-primary dark:bg-primary-fixed rounded-full"
                      />
                    )}
                  </Link>
                )
              })}
            </nav>

            {/* Quick Actions */}
            <div className="mt-6 pt-5 border-t border-outline-variant/30">
              <h3 className="text-xs font-semibold text-on-surface-variant uppercase tracking-wider font-mono mb-3 px-1">
                Data Tools
              </h3>
              <div className="space-y-1">
                {quickActions.map((action) => (
                  <button
                    key={action.name}
                    type="button"
                    onClick={action.action}
                    className="flex items-center w-full px-3.5 py-2 rounded-xl text-sm font-medium text-on-surface-variant hover:bg-surface-container-high/60 hover:text-on-surface transition-all duration-200 text-left"
                  >
                    <action.icon className="mr-3 h-4 w-4 shrink-0 text-outline" />
                    <span>{action.name}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* System Status Card */}
            <div className="mt-auto pt-6">
              {renderDetailedStatusCard()}
            </div>
          </div>
        )}
      </aside>

      {/* ── Mobile Overlay & Drawer ── */}
      <AnimatePresence>
        {isMobileOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={closeMobile}
              className="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm md:hidden"
              aria-hidden="true"
            />

            {/* Sliding Drawer */}
            <motion.aside
              initial={{ x: -320 }}
              animate={{ x: 0 }}
              exit={{ x: -320 }}
              transition={{ type: 'spring', damping: 25, stiffness: 220 }}
              className="fixed inset-y-0 left-0 z-50 w-72 bg-surface dark:bg-slate-900 border-r border-outline-variant/30 shadow-2xl flex flex-col md:hidden overflow-y-auto custom-scrollbar"
            >
              <div className="p-6 flex flex-col h-full">
                {/* Drawer Header */}
                <div className="flex items-center justify-between pb-4 border-b border-outline-variant/30 mb-6">
                  <div className="flex items-center gap-2.5">
                    <img
                      src="/assets/research-rover-logo.png"
                      alt="Research ROVER"
                      className="h-7 w-auto object-contain"
                    />
                    <span className="font-display font-bold text-lg text-on-surface tracking-tight">
                      Research Rover
                    </span>
                  </div>
                  <button
                    type="button"
                    onClick={closeMobile}
                    className="p-2 rounded-full text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high/60 transition-colors"
                    aria-label="Close navigation"
                  >
                    <XMarkIcon className="h-5 w-5" />
                  </button>
                </div>

                {/* Navigation Links */}
                <nav className="space-y-1.5 mb-6">
                  <h3 className="text-xs font-semibold text-on-surface-variant uppercase tracking-wider font-mono mb-2 px-1">
                    Navigation
                  </h3>
                  {sidebarItems.map((item) => {
                    const isActive = location.pathname === item.href
                    return (
                      <Link
                        key={item.name}
                        to={item.href}
                        onClick={closeMobile}
                        className={`flex items-center px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                          isActive
                            ? 'bg-primary-fixed text-primary dark:bg-primary-container dark:text-white font-semibold shadow-sm'
                            : 'text-on-surface-variant hover:bg-surface-container-high/60 hover:text-on-surface'
                        }`}
                      >
                        <item.icon className="mr-3 h-5 w-5 shrink-0" />
                        <span>{item.name}</span>
                      </Link>
                    )
                  })}
                </nav>

                {/* Quick Actions */}
                <div className="mb-6 pt-4 border-t border-outline-variant/30">
                  <h3 className="text-xs font-semibold text-on-surface-variant uppercase tracking-wider font-mono mb-2 px-1">
                    Data Tools
                  </h3>
                  <div className="space-y-1">
                    {quickActions.map((action) => (
                      <button
                        key={action.name}
                        type="button"
                        onClick={() => {
                          closeMobile()
                          action.action()
                        }}
                        className="flex items-center w-full px-3.5 py-2 rounded-xl text-sm font-medium text-on-surface-variant hover:bg-surface-container-high/60 hover:text-on-surface transition-all text-left"
                      >
                        <action.icon className="mr-3 h-4 w-4 shrink-0 text-outline" />
                        <span>{action.name}</span>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Status Card in Drawer */}
                <div className="mt-auto pt-4 border-t border-outline-variant/30">
                  {renderDetailedStatusCard()}
                </div>
              </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>
    </>
  )
}
