import { createContext, useContext, useState, useEffect, type ReactNode } from 'react'
import { useLocation } from 'react-router-dom'

interface SidebarContextValue {
  isCollapsed: boolean
  toggleCollapse: () => void
  setIsCollapsed: (collapsed: boolean) => void
  isMobileOpen: boolean
  setIsMobileOpen: (open: boolean) => void
  toggleMobileOpen: () => void
  closeMobile: () => void
}

const SidebarContext = createContext<SidebarContextValue | undefined>(undefined)

const STORAGE_KEY = 'research-rover-sidebar-collapsed'

export function SidebarProvider({ children }: { children: ReactNode }) {
  const [isCollapsed, setIsCollapsed] = useState<boolean>(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      return stored ? JSON.parse(stored) : false
    } catch {
      return false
    }
  })

  const [isMobileOpen, setIsMobileOpen] = useState(false)
  const location = useLocation()

  // Save collapsed state to localStorage
  const toggleCollapse = () => {
    setIsCollapsed((prev) => {
      const next = !prev
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(next))
      } catch {}
      return next
    })
  }

  const toggleMobileOpen = () => {
    setIsMobileOpen((prev) => !prev)
  }

  const closeMobile = () => {
    setIsMobileOpen(false)
  }

  // Automatically close mobile drawer when navigating to a new route
  useEffect(() => {
    setIsMobileOpen(false)
  }, [location.pathname])

  // Close mobile drawer on Escape key and prevent background scroll
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isMobileOpen) {
        setIsMobileOpen(false)
      }
    }

    if (isMobileOpen) {
      document.body.style.overflow = 'hidden'
      window.addEventListener('keydown', handleKeyDown)
    } else {
      document.body.style.overflow = ''
    }

    return () => {
      document.body.style.overflow = ''
      window.removeEventListener('keydown', handleKeyDown)
    }
  }, [isMobileOpen])

  return (
    <SidebarContext.Provider
      value={{
        isCollapsed,
        toggleCollapse,
        setIsCollapsed,
        isMobileOpen,
        setIsMobileOpen,
        toggleMobileOpen,
        closeMobile,
      }}
    >
      {children}
    </SidebarContext.Provider>
  )
}

export function useSidebar() {
  const context = useContext(SidebarContext)
  if (!context) {
    throw new Error('useSidebar must be used within a SidebarProvider')
  }
  return context
}
