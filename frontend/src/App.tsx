import { Routes, Route } from 'react-router-dom'
import { ThemeProvider } from '@/components/theme-provider'
import { SearchProvider } from '@/context/SearchContext'
import { EmbeddingProvider } from '@/context/EmbeddingContext'
import { ChatProvider } from '@/context/ChatContext'
import { AnalyticsProvider } from '@/context/AnalyticsContext'
import { SystemStatusProvider } from '@/context/SystemStatusContext'
import { SidebarProvider } from '@/context/SidebarContext'
import { Layout } from '@/components/layout/Layout'
import { HomePage } from '@/pages/HomePage'
import { SearchPage } from '@/pages/SearchPage'
import { ChatPage } from '@/pages/ChatPage'
import { AnalyticsPage } from '@/pages/AnalyticsPage'
import { SettingsPage } from '@/pages/SettingsPage'
import { UseCasesPage } from '@/pages/UseCasesPage'

function App() {
  return (
    <ThemeProvider defaultTheme="light" storageKey="research-rover-theme">
      <SystemStatusProvider>
        <SearchProvider>
          <EmbeddingProvider>
            <ChatProvider>
              <AnalyticsProvider>
                <SidebarProvider>
                  <Layout>
                    <Routes>
                      <Route path="/" element={<HomePage />} />
                      <Route path="/search" element={<SearchPage />} />
                      <Route path="/chat" element={<ChatPage />} />
                      <Route path="/analytics" element={<AnalyticsPage />} />
                      <Route path="/use-cases" element={<UseCasesPage />} />
                      <Route path="/settings" element={<SettingsPage />} />
                    </Routes>
                  </Layout>
                </SidebarProvider>
              </AnalyticsProvider>
            </ChatProvider>
          </EmbeddingProvider>
        </SearchProvider>
      </SystemStatusProvider>
    </ThemeProvider>
  )
}

export default App
