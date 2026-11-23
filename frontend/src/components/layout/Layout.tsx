import React from 'react'
import { Navbar } from './Navbar'
import { Sidebar } from './Sidebar'
import { Footer } from './Footer'
import { useSidebar } from '@/context/SidebarContext'

interface LayoutProps {
  children: React.ReactNode
}

export function Layout({ children }: LayoutProps) {
  const { isCollapsed } = useSidebar()

  return (
    <div className="min-h-screen bg-surface dark:bg-slate-950 text-on-surface dark:text-slate-100 flex flex-col relative antialiased selection:bg-primary-container selection:text-white transition-colors duration-200 overflow-x-hidden">
      {/* ── Radiant Luminary Ambient Background Lights (Non-interactive) ── */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden -z-10 select-none">
        <div className="absolute -top-32 -left-32 w-96 h-96 rounded-full bg-secondary-fixed/20 blur-3xl" />
        <div className="absolute top-1/4 -right-20 w-80 h-80 rounded-full bg-primary-fixed/25 blur-3xl" />
        <div className="absolute -bottom-20 left-1/3 w-96 h-96 rounded-full bg-tertiary-fixed/15 blur-3xl" />
      </div>

      {/* ── Fixed Navbar ── */}
      <Navbar />

      {/* ── Main Layout Body with Sidebar & Content ── */}
      <div className="flex flex-1 relative min-h-0">
        <Sidebar />

        <main
          className={`flex-1 pt-16 flex flex-col min-w-0 transition-all duration-300 ease-in-out ml-0 ${
            isCollapsed ? 'md:ml-20' : 'md:ml-64'
          }`}
        >
          <div className="w-full max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 min-w-0">
            {children}
          </div>
          <Footer />
        </main>
      </div>
    </div>
  )
}
