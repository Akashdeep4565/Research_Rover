import { Link, useLocation, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { useTheme } from '@/components/theme-provider'
import { useSidebar } from '@/context/SidebarContext'
import { useSystemStatus } from '@/context/SystemStatusContext'
import { useSearch } from '@/context/SearchContext'
import { useChat } from '@/context/ChatContext'
import { 
  Bars3Icon,
  MoonIcon, 
  SunIcon, 
  CogIcon,
  BellIcon,
  UserCircleIcon,
  MagnifyingGlassIcon,
  DocumentTextIcon,
} from '@heroicons/react/24/outline'
import { motion } from 'framer-motion'

export function Navbar() {
  const { theme, setTheme } = useTheme()
  const location = useLocation()
  const navigate = useNavigate()
  const { isCollapsed, toggleCollapse, isMobileOpen, toggleMobileOpen } = useSidebar()
  const { apiStatus } = useSystemStatus()
  const { csvFilename } = useSearch()
  const { selectedFile } = useChat()

  const currentDataset = csvFilename || selectedFile

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark')
  }

  const handleToggle = () => {
    if (window.innerWidth < 768) {
      toggleMobileOpen()
    } else {
      toggleCollapse()
    }
  }

  const isNavActive = typeof window !== 'undefined' && window.innerWidth < 768 ? isMobileOpen : !isCollapsed

  return (
    <motion.header 
      initial={{ y: -80, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      className="fixed top-0 inset-x-0 z-50 h-16 bg-surface/85 dark:bg-slate-900/85 backdrop-blur-xl border-b border-outline-variant/30 shadow-[0_1px_12px_rgba(67,56,202,0.04)] transition-colors duration-200"
    >
      <div className="h-full px-4 sm:px-6 flex items-center justify-between gap-4">
        {/* Left Section: Drawer Toggle, Logo & Brand */}
        <div className="flex items-center gap-3 shrink-0">
          <button
            type="button"
            onClick={handleToggle}
            className="p-2 -ml-1 rounded-full text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high/60 transition-colors focus:outline-none focus:ring-2 focus:ring-primary/40"
            aria-label={isNavActive ? 'Collapse navigation' : 'Expand navigation'}
            title={isNavActive ? 'Collapse navigation' : 'Expand navigation'}
          >
            <Bars3Icon className="h-5 w-5" />
          </button>

          <Link to="/" className="flex items-center gap-2.5 group">
            <img
              src="/assets/research-rover-logo.png"
              alt="Research ROVER"
              className="h-8 w-auto object-contain transition-transform duration-200 group-hover:scale-105"
            />
            <div className="flex items-center gap-2">
              <span className="font-display font-bold text-lg md:text-xl text-on-surface tracking-tight">
                Research Rover
              </span>
              <span className="hidden sm:inline-flex px-2 py-0.5 rounded-full bg-primary-fixed text-primary dark:bg-primary-container dark:text-white text-[10px] font-mono font-semibold tracking-wider uppercase">
                v2.4
              </span>
            </div>
          </Link>
        </div>

        {/* Center Section: Pill-style Route Navigation (Desktop) */}
        <nav className="hidden lg:flex items-center gap-1 bg-surface-container-low/80 dark:bg-slate-800/80 p-1 rounded-full border border-outline-variant/30 shadow-inner-sm">
          <NavLink to="/" active={location.pathname === '/'}>
            Home
          </NavLink>
          <NavLink to="/search" active={location.pathname === '/search'}>
            Search
          </NavLink>
          <NavLink to="/analytics" active={location.pathname === '/analytics'}>
            Analysis
          </NavLink>
          <NavLink to="/chat" active={location.pathname === '/chat'}>
            AI Chat
          </NavLink>
        </nav>

        {/* Right Section: Active Dataset, System Indicator & Actions */}
        <div className="flex items-center gap-2 sm:gap-3 shrink-0">
          {/* Quick Search Shortcut Trigger */}
          <button
            type="button"
            onClick={() => navigate('/search')}
            className="hidden xl:flex items-center gap-2 px-3 py-1.5 rounded-full bg-surface-container-lowest/80 dark:bg-slate-800/60 border border-outline-variant/40 text-on-surface-variant hover:text-on-surface hover:border-outline-variant transition-all text-xs font-medium shadow-sm"
            title="Search papers (⌘K)"
          >
            <MagnifyingGlassIcon className="h-4 w-4 text-outline" />
            <span>Search corpus</span>
            <kbd className="font-mono text-[10px] bg-surface-container px-1.5 py-0.5 rounded text-on-surface-variant border border-outline-variant/30">
              ⌘K
            </kbd>
          </button>

          {/* Active Dataset Pill (Real value from context) */}
          {currentDataset && (
            <div 
              className="hidden md:flex items-center gap-1.5 px-3 py-1 rounded-full bg-secondary-container/30 text-on-secondary-container dark:text-teal-200 border border-secondary/20 text-xs font-mono font-medium max-w-[200px] truncate"
              title={`Active Dataset: ${currentDataset}`}
            >
              <DocumentTextIcon className="h-3.5 w-3.5 shrink-0 text-secondary" />
              <span className="truncate">{currentDataset}</span>
            </div>
          )}

          {/* Real System Status Pulse Indicator */}
          <div 
            className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-surface-container-low/80 dark:bg-slate-800/60 border border-outline-variant/30 text-xs font-medium cursor-help"
            title={`API Status: ${apiStatus}`}
          >
            <span className="relative flex h-2 w-2">
              {apiStatus === 'online' && (
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
              )}
              <span
                className={`relative inline-flex rounded-full h-2 w-2 ${
                  apiStatus === 'online'
                    ? 'bg-emerald-500'
                    : apiStatus === 'offline'
                    ? 'bg-rose-500'
                    : 'bg-amber-500 animate-pulse'
                }`}
              />
            </span>
            <span className="hidden sm:inline text-on-surface-variant text-[11px]">
              {apiStatus === 'online' ? 'Online' : apiStatus === 'offline' ? 'Offline' : 'Connecting'}
            </span>
          </div>

          {/* Notifications */}
          <Button 
            variant="ghost" 
            size="icon" 
            className="rounded-full relative text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high/60"
            title="Notifications"
            aria-label="Notifications"
          >
            <BellIcon className="h-5 w-5" />
            <span className="absolute top-2 right-2 flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-secondary-container opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-secondary" />
            </span>
          </Button>

          {/* Theme Toggle */}
          <Button 
            variant="ghost" 
            size="icon" 
            onClick={toggleTheme}
            className="rounded-full text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high/60"
            title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
            aria-label="Toggle color theme"
          >
            {theme === 'dark' ? (
              <SunIcon className="h-5 w-5 text-amber-400" />
            ) : (
              <MoonIcon className="h-5 w-5 text-indigo-700" />
            )}
          </Button>

          {/* Settings Link */}
          <Link to="/settings">
            <Button 
              variant="ghost" 
              size="icon" 
              className="rounded-full text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high/60"
              title="Settings & Diagnostics"
              aria-label="Settings"
            >
              <CogIcon className="h-5 w-5" />
            </Button>
          </Link>

          {/* User Profile */}
          <Button 
            variant="ghost" 
            size="icon" 
            className="rounded-full text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high/60"
            title="User Profile"
            aria-label="User Profile"
          >
            <UserCircleIcon className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </motion.header>
  )
}

interface NavLinkProps {
  to: string
  children: React.ReactNode
  active?: boolean
}

function NavLink({ to, children, active }: NavLinkProps) {
  return (
    <Link
      to={to}
      className={`relative px-4 py-1.5 rounded-full text-sm font-medium transition-all duration-200 ${
        active
          ? 'bg-primary-container text-white shadow-sm font-semibold'
          : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high/60'
      }`}
    >
      {children}
    </Link>
  )
}
