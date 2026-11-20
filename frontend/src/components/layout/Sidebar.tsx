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
      className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-lg border border-blue-200 dark:border-blue-800"
      title={statusTooltip}
    >
      <h4 className="text-sm font-semibold text-blue-900 dark:text-blue-100 mb-2">
        System Status
      </h4>
      <div className="space-y-2 text-xs">
        {/* API Status Row */}
        <div className="flex items-center justify-between">
          <span className="text-blue-700 dark:text-blue-300">API</span>
          <div className="flex items-center">
            <div
              className={`w-2 h-2 rounded-full mr-2 ${
                apiStatus === 'online'
                  ? 'bg-green-500'
                  : apiStatus === 'offline'
                  ? 'bg-red-500'
                  : 'bg-amber-500 animate-pulse'
              }`}
            />
            <span
              className={
                apiStatus === 'online'
                  ? 'text-green-600 dark:text-green-400 font-medium'
                  : apiStatus === 'offline'
                  ? 'text-red-600 dark:text-red-400 font-medium'
                  : 'text-amber-600 dark:text-amber-400 font-medium'
              }
            >
              {apiStatus === 'online' ? 'Online' : apiStatus === 'offline' ? 'Offline' : 'Checking...'}
            </span>
          </div>
        </div>

        {/* Model Status Row */}
        <div className="flex items-center justify-between">
          <span className="text-blue-700 dark:text-blue-300">Models</span>
          <div className="flex items-center">
            <div
              className={`w-2 h-2 rounded-full mr-2 ${
                modelStatus === 'loaded'
                  ? 'bg-green-500'
                  : modelStatus === 'loading'
                  ? 'bg-amber-500 animate-pulse'
                  : modelStatus === 'partial'
                  ? 'bg-amber-500'
                  : modelStatus === 'not_loaded' || modelStatus === 'error'
                  ? 'bg-red-500'
                  : 'bg-amber-500 animate-pulse'
              }`}
            />
            <span
              className={
                modelStatus === 'loaded'
                  ? 'text-green-600 dark:text-green-400 font-medium'
                  : modelStatus === 'loading' || modelStatus === 'partial'
                  ? 'text-amber-600 dark:text-amber-400 font-medium'
                  : modelStatus === 'not_loaded' || modelStatus === 'error'
                  ? 'text-red-600 dark:text-red-400 font-medium'
                  : 'text-amber-600 dark:text-amber-400 font-medium'
              }
            >
              {modelStatus === 'loaded'
                ? 'Loaded'
                : modelStatus === 'loading'
                ? 'Loading...'
                : modelStatus === 'partial'
                ? 'Partial'
                : modelStatus === 'not_loaded' || modelStatus === 'error'
                ? 'Not Loaded'
                : modelStatus === 'checking'
                ? 'Checking...'
                : 'Unknown'}
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
        className={`fixed left-0 top-16 h-[calc(100vh-4rem)] bg-white/60 dark:bg-slate-900/60 backdrop-blur-md border-r border-gray-200 dark:border-gray-800 transition-all duration-300 ease-in-out z-30 hidden md:flex md:flex-col ${
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
              className="p-2 mb-4 rounded-xl text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800/60 transition-colors focus:outline-none"
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
                    className={`relative flex items-center justify-center w-11 h-11 rounded-xl transition-all duration-200 ${
                      isActive
                        ? 'bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 shadow-sm'
                        : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800/50 hover:text-gray-900 dark:hover:text-gray-100'
                    }`}
                  >
                    <item.icon className="h-5 w-5" />
                    {isActive && (
                      <div className="absolute right-1 top-2.5 bottom-2.5 w-1 bg-blue-600 dark:bg-blue-400 rounded-full" />
                    )}
                  </Link>
                )
              })}
            </nav>

            {/* Quick Actions Icons */}
            <div className="mt-6 w-full flex flex-col items-center space-y-2 pt-4 border-t border-gray-200 dark:border-gray-800">
              {quickActions.map((action) => (
                <button
                  key={action.name}
                  type="button"
                  onClick={action.action}
                  title={action.name}
                  className="flex items-center justify-center w-11 h-11 rounded-xl text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800/50 hover:text-gray-900 dark:hover:text-gray-100 transition-all duration-200"
                >
                  <action.icon className="h-5 w-5" />
                </button>
              ))}
            </div>

            {/* Compact System Status Indicator */}
            <div
              className="mt-auto w-full flex flex-col items-center pt-4 border-t border-gray-200 dark:border-gray-800 pb-2"
              title={`System Status\n• API: ${apiStatus}\n• Models: ${modelStatus}\n${statusTooltip}`}
            >
              <div className="flex flex-col items-center gap-1.5 p-2 rounded-xl bg-blue-50/50 dark:bg-blue-900/20 border border-blue-200/50 dark:border-blue-800/50 cursor-help">
                <div
                  className={`w-2.5 h-2.5 rounded-full ${
                    apiStatus === 'online'
                      ? 'bg-green-500'
                      : apiStatus === 'offline'
                      ? 'bg-red-500'
                      : 'bg-amber-500 animate-pulse'
                  }`}
                  title={`API: ${apiStatus}`}
                />
                <div
                  className={`w-2.5 h-2.5 rounded-full ${
                    modelStatus === 'loaded'
                      ? 'bg-green-500'
                      : modelStatus === 'loading' || modelStatus === 'partial'
                      ? 'bg-amber-500 animate-pulse'
                      : 'bg-red-500'
                  }`}
                  title={`Models: ${modelStatus}`}
                />
              </div>
            </div>
          </div>
        ) : (
          /* Expanded Desktop View */
          <div className="p-6 flex flex-col h-full overflow-y-auto custom-scrollbar">
            {/* Header / Collapse Bar */}
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Navigation
              </h3>
              <button
                type="button"
                onClick={toggleCollapse}
                className="p-1.5 rounded-lg text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors focus:outline-none"
                title="Collapse sidebar"
                aria-label="Collapse sidebar"
              >
                <Bars3Icon className="h-4 w-4" />
              </button>
            </div>

            {/* Navigation Links */}
            <nav className="space-y-1.5">
              {sidebarItems.map((item) => {
                const isActive = location.pathname === item.href
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                      isActive
                        ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 shadow-sm'
                        : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800/50 hover:text-gray-900 dark:hover:text-gray-100'
                    }`}
                  >
                    <item.icon className="mr-3 h-5 w-5" />
                    {item.name}
                    {isActive && (
                      <motion.div
                        layoutId="sidebar-indicator"
                        className="ml-auto w-1 h-6 bg-blue-600 dark:bg-blue-400 rounded-full"
                      />
                    )}
                  </Link>
                )
              })}
            </nav>

            {/* Quick Actions */}
            <div className="mt-8">
              <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4">
                Quick Actions
              </h3>
              <div className="space-y-1.5">
                {quickActions.map((action) => (
                  <button
                    key={action.name}
                    type="button"
                    onClick={action.action}
                    className="flex items-center w-full px-3 py-2 rounded-lg text-sm font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800/50 hover:text-gray-900 dark:hover:text-gray-100 transition-all duration-200"
                  >
                    <action.icon className="mr-3 h-5 w-5" />
                    {action.name}
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
              className="fixed inset-y-0 left-0 z-50 w-72 bg-white dark:bg-slate-900 border-r border-gray-200 dark:border-gray-800 shadow-2xl flex flex-col md:hidden overflow-y-auto custom-scrollbar"
            >
              <div className="p-6 flex flex-col h-full">
                {/* Drawer Header */}
                <div className="flex items-center justify-between pb-4 border-b border-gray-200 dark:border-gray-800 mb-6">
                  <div className="flex items-center space-x-3">
                    <img
                      src="/assets/research-rover-logo.png"
                      alt="Research ROVER"
                      className="h-7 w-auto object-contain"
                    />
                    <span className="text-lg font-bold gradient-text">
                      Research Rover
                    </span>
                  </div>
                  <button
                    type="button"
                    onClick={closeMobile}
                    className="p-2 rounded-xl text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                    aria-label="Close navigation"
                  >
                    <XMarkIcon className="h-6 w-6" />
                  </button>
                </div>

                {/* Navigation Links */}
                <nav className="space-y-2 mb-6">
                  <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2">
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
                            ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300'
                            : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                        }`}
                      >
                        <item.icon className="mr-3 h-5 w-5" />
                        {item.name}
                      </Link>
                    )
                  })}
                </nav>

                {/* Quick Actions */}
                <div className="mb-6">
                  <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2">
                    Quick Actions
                  </h3>
                  <div className="space-y-1.5">
                    {quickActions.map((action) => (
                      <button
                        key={action.name}
                        type="button"
                        onClick={() => {
                          closeMobile()
                          action.action()
                        }}
                        className="flex items-center w-full px-3.5 py-2.5 rounded-xl text-sm font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-all"
                      >
                        <action.icon className="mr-3 h-5 w-5" />
                        {action.name}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Status Card in Drawer */}
                <div className="mt-auto pt-4 border-t border-gray-200 dark:border-gray-800">
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