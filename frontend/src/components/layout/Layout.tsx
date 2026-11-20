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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 flex flex-col">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <main
          className={`flex-1 pt-16 flex flex-col min-w-0 transition-all duration-300 ease-in-out ml-0 ${
            isCollapsed ? 'md:ml-20' : 'md:ml-64'
          }`}
        >
          <div className="container mx-auto px-6 py-8 flex-1 min-w-0 max-w-full">
            {children}
          </div>
          <Footer />
        </main>
      </div>
    </div>
  )
}