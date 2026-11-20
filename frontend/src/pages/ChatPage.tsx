import React, { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import {
  PaperAirplaneIcon,
  CpuChipIcon,
  DocumentTextIcon,
  ArrowUpTrayIcon,
  ChevronDownIcon,
  XMarkIcon,
  ShieldCheckIcon,
  StopIcon,
  TrashIcon,
  ArrowDownCircleIcon,
  LightBulbIcon,
} from '@heroicons/react/24/outline'
import type { ExtendedFileUploadResponse, DatasetQualityReport } from '@/types'
import { filesApi } from '@/services/api'
import { useChat } from '@/context/ChatContext'
import { useEmbedding } from '@/context/EmbeddingContext'
import { useTheme } from '@/components/theme-provider'
import { EmbeddingProgressModal } from '@/components/EmbeddingProgressModal'
import { DatasetQualityModal } from '@/components/DatasetQualityModal'
import { DatasetFeatureReadinessBanner } from '@/components/DatasetFeatureReadinessBanner'
import { ChatMessageItem } from '@/components/chat/ChatMessageItem'
import { ChatLoadingIndicator } from '@/components/chat/ChatLoadingIndicator'

const QUICK_PROMPTS = [
  'Summarize the core methodologies across these papers',
  'What key limitations or open challenges are discussed?',
  'Explain any mathematical models or formulas used',
  'Compare key findings between the most cited works',
]

export function ChatPage() {
  const { theme } = useTheme()
  const {
    messages,
    inputMessage,
    setInputMessage,
    isLoading,
    selectedFile,
    setSelectedFile,
    availableFiles,
    addAvailableFile,
    error,
    setError,
    hasEmbeddings,
    sendMessage,
    stopGeneration,
    regenerateResponse,
    clearConversation,
  } = useChat()

  const {
    isCreating: isCreatingEmbeddings,
    startEmbeddings,
    scrapeFullText,
    setScrapeFullText,
  } = useEmbedding()

  const scrollContainerRef = useRef<HTMLDivElement>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const [uploading, setUploading] = useState(false)
  const [isQualityModalOpen, setIsQualityModalOpen] = useState(false)
  const [selectedQualityData, setSelectedQualityData] = useState<
    ExtendedFileUploadResponse | DatasetQualityReport | null
  >(null)
  const [isScrolledUp, setIsScrolledUp] = useState(false)

  // Upload handler
  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    e.target.value = ''
    if (!file) return
    if (!file.name.toLowerCase().endsWith('.csv')) {
      setError('Please upload a .csv file')
      return
    }
    setError('')
    setUploading(true)
    try {
      const res = await filesApi.upload(file)
      addAvailableFile(res.filename)
      setSelectedQualityData(res)
      setIsQualityModalOpen(true)
    } catch (err: any) {
      setError(err?.error || err?.detail || 'Failed to upload file')
    } finally {
      setUploading(false)
    }
  }

  // Auto-scroll when new messages arrive, unless user has scrolled up to inspect earlier content
  useEffect(() => {
    if (!isScrolledUp) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, isLoading, isScrolledUp])

  // Track scroll position to prevent forcing scroll when user is reading history
  const handleScroll = () => {
    if (!scrollContainerRef.current) return
    const { scrollTop, scrollHeight, clientHeight } = scrollContainerRef.current
    const distanceFromBottom = scrollHeight - scrollTop - clientHeight
    setIsScrolledUp(distanceFromBottom > 140)
  }

  const scrollToBottom = () => {
    setIsScrolledUp(false)
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${Math.min(
        textareaRef.current.scrollHeight,
        180
      )}px`
    }
  }, [inputMessage])

  // Key down for textarea: Enter sends, Shift+Enter adds newline
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      if (!sendDisabled) {
        sendMessage()
      }
    }
  }

  const inputDisabled = !selectedFile || isLoading || isCreatingEmbeddings
  const sendDisabled = !inputMessage.trim() || inputDisabled

  const inputPlaceholder = isCreatingEmbeddings
    ? 'Building embeddings, please wait…'
    : !selectedFile
    ? 'Select a collection to begin, or ask a general query…'
    : !hasEmbeddings
    ? 'Ask away — create embeddings for paper-grounded answers…'
    : 'Ask about your research papers (Markdown, LaTeX, & Diagrams supported)…'

  // Identify last assistant message index for regenerate button
  let lastAssistantIndex = -1
  for (let i = messages.length - 1; i >= 0; i--) {
    if (messages[i].type === 'assistant') {
      lastAssistantIndex = i
      break
    }
  }

  return (
    <div className="space-y-6 pb-12">
      {/* ── Hero Banner ── */}
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative overflow-hidden rounded-2xl border border-gray-200 dark:border-slate-800/60 px-8 py-9 shadow-sm dark:shadow-2xl"
        style={{
          background:
            theme === 'dark'
              ? 'linear-gradient(135deg, #020617 0%, #0f172a 50%, #0c1830 100%)'
              : 'linear-gradient(135deg, #f8fafc 0%, #eef2ff 50%, #e0f2fe 100%)',
          boxShadow:
            theme === 'dark'
              ? '0 0 0 1px rgba(148,163,184,0.07), 0 24px 80px rgba(2,6,23,0.6)'
              : '0 0 0 1px rgba(148,163,184,0.12), 0 12px 40px rgba(15,23,42,0.08)',
        }}
      >
        <div
          className="pointer-events-none absolute inset-0"
          style={{
            background:
              'radial-gradient(ellipse 60% 50% at 80% 20%, rgba(56,189,248,0.10) 0%, transparent 60%), radial-gradient(ellipse 50% 60% at 20% 80%, rgba(167,139,250,0.08) 0%, transparent 60%)',
          }}
        />
        <div
          className="pointer-events-none absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage:
              'linear-gradient(rgba(148,163,184,1) 1px, transparent 1px), linear-gradient(90deg, rgba(148,163,184,1) 1px, transparent 1px)',
            backgroundSize: '40px 40px',
          }}
        />
        <div className="relative z-10 text-center">
          <span className="inline-flex items-center gap-2 rounded-full border border-sky-500/20 bg-sky-500/10 px-3.5 py-1 text-[11px] font-bold uppercase tracking-[0.3em] text-sky-400">
            <span className="h-1.5 w-1.5 rounded-full bg-sky-400 animate-pulse" />
            AI Research Assistant
          </span>
          <h1 className="mt-3 text-3xl font-bold tracking-tight text-gray-900 dark:text-slate-50 md:text-5xl">
            Chat with Your Papers
          </h1>
          <p className="mx-auto mt-2.5 max-w-2xl text-sm leading-relaxed text-gray-600 dark:text-slate-400">
            Deep academic exploration grounded in your indexed literature. Features full Markdown formatting, KaTeX mathematical equations, syntax-highlighted code blocks, and visual Mermaid diagrams.
          </p>
        </div>
      </motion.div>

      {/* ── Collection & Setup Panel ── */}
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <div className="rounded-2xl border border-gray-200 dark:border-slate-800/60 bg-white dark:bg-slate-900 p-5 shadow-sm">
          <div className="mb-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="h-1 w-5 rounded-full bg-sky-500" />
              <span className="text-xs font-bold uppercase tracking-[0.22em] text-gray-500 dark:text-slate-500">
                Active Research Collection
              </span>
            </div>
            {selectedFile && (
              <span
                className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                  hasEmbeddings
                    ? 'border border-emerald-500/30 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300'
                    : 'border border-amber-500/30 bg-amber-500/10 text-amber-700 dark:text-amber-300'
                }`}
              >
                <span
                  className={`h-1.5 w-1.5 rounded-full ${
                    hasEmbeddings ? 'bg-emerald-500' : 'bg-amber-500'
                  } ${isCreatingEmbeddings ? 'animate-pulse' : ''}`}
                />
                {isCreatingEmbeddings
                  ? 'Indexing…'
                  : hasEmbeddings
                  ? 'Embeddings active'
                  : 'Needs embeddings'}
              </span>
            )}
          </div>

          {/* File Row */}
          <div className="flex flex-col gap-1.5">
            <div className="flex flex-wrap items-stretch gap-2.5">
              <div className="group relative min-w-[220px] flex-1">
                <select
                  value={selectedFile || ''}
                  onChange={(e) => setSelectedFile(e.target.value)}
                  disabled={isCreatingEmbeddings}
                  className="relative w-full appearance-none rounded-xl border border-gray-300 bg-gradient-to-b from-white to-gray-50/70 px-4 py-2.5 pr-12 text-sm font-medium text-gray-800 shadow-sm outline-none transition-all duration-200 hover:border-sky-400/70 hover:shadow-md hover:shadow-sky-500/5 focus:border-sky-500 focus:shadow-[0_0_0_3px_rgba(56,189,248,0.18)] disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-700/80 dark:from-slate-900 dark:to-slate-900/40 dark:text-slate-100 dark:hover:border-sky-500/50"
                >
                  <option value="">Choose a research collection…</option>
                  {availableFiles.map((f) => (
                    <option key={f} value={f}>
                      {f}
                    </option>
                  ))}
                </select>
                <span className="pointer-events-none absolute right-2 top-1/2 flex h-7 w-7 -translate-y-1/2 items-center justify-center rounded-lg bg-gray-100/80 text-gray-500 transition-colors duration-150 group-hover:bg-sky-500/10 group-hover:text-sky-600 dark:bg-slate-800/80 dark:text-slate-400 dark:group-hover:bg-sky-500/15 dark:group-hover:text-sky-300">
                  <ChevronDownIcon className="h-4 w-4" />
                </span>
              </div>

              <input
                ref={fileInputRef}
                type="file"
                accept=".csv"
                onChange={handleUpload}
                className="hidden"
              />
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                disabled={uploading || isCreatingEmbeddings}
                title="Upload a CSV"
                className="flex shrink-0 items-center gap-1.5 rounded-xl border border-gray-300 bg-gradient-to-b from-white to-gray-50/70 px-3.5 py-2.5 text-sm font-medium text-gray-700 shadow-sm transition hover:border-sky-400/70 hover:text-gray-900 hover:shadow-md hover:shadow-sky-500/5 disabled:cursor-not-allowed disabled:opacity-60 dark:border-slate-700/80 dark:from-slate-900 dark:to-slate-900/40 dark:text-slate-300 dark:hover:border-sky-500/50 dark:hover:text-slate-100"
              >
                <ArrowUpTrayIcon className={`h-4 w-4 ${uploading ? 'animate-pulse' : ''}`} />
                <span className="hidden sm:inline">{uploading ? 'Uploading…' : 'Upload'}</span>
              </button>

              <button
                type="button"
                onClick={() => {
                  setSelectedQualityData(null)
                  setIsQualityModalOpen(true)
                }}
                disabled={!selectedFile}
                title="View dataset quality, column mappings and feature readiness"
                className="flex shrink-0 items-center gap-1.5 rounded-xl border border-sky-300 dark:border-sky-700/80 bg-sky-50/70 dark:bg-sky-950/40 px-3.5 py-2.5 text-sm font-semibold text-sky-700 dark:text-sky-300 shadow-sm transition hover:bg-sky-100 hover:border-sky-400 dark:hover:bg-sky-900/50 disabled:cursor-not-allowed disabled:opacity-50"
              >
                <ShieldCheckIcon className="h-4 w-4" />
                <span className="hidden sm:inline">Quality & Schema</span>
              </button>

              {selectedFile && (
                <button
                  type="button"
                  onClick={() => startEmbeddings(selectedFile, hasEmbeddings)}
                  disabled={isCreatingEmbeddings}
                  title={
                    hasEmbeddings
                      ? 'Rebuild this index with current settings'
                      : 'Build the semantic FAISS index for this collection'
                  }
                  className="flex shrink-0 items-center gap-1.5 rounded-xl bg-gradient-to-br from-sky-500 to-indigo-500 px-3.5 py-2.5 text-sm font-semibold text-white shadow-md shadow-sky-500/25 transition hover:from-sky-400 hover:to-indigo-400 hover:shadow-lg hover:shadow-sky-500/30 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  <CpuChipIcon className={`h-4 w-4 ${isCreatingEmbeddings ? 'animate-spin' : ''}`} />
                  <span className="hidden sm:inline">
                    {isCreatingEmbeddings
                      ? 'Building…'
                      : hasEmbeddings
                      ? 'Recreate embeddings'
                      : 'Create embeddings'}
                  </span>
                </button>
              )}
            </div>
          </div>

          {selectedFile && (
            <DatasetFeatureReadinessBanner
              filename={selectedFile}
              onOpenModal={() => {
                setSelectedQualityData(null)
                setIsQualityModalOpen(true)
              }}
              className="mt-3.5"
            />
          )}

          {/* Settings Row */}
          <div className="mt-3 flex flex-col gap-2.5 sm:flex-row sm:items-center sm:justify-between text-xs text-gray-500 dark:text-slate-400">
            <label className="flex cursor-pointer items-center gap-2">
              <input
                type="checkbox"
                checked={scrapeFullText}
                onChange={(e) => setScrapeFullText(e.target.checked)}
                disabled={isCreatingEmbeddings}
                className="h-3.5 w-3.5 rounded border-gray-300 text-sky-600 focus:ring-sky-500 dark:border-slate-700 dark:bg-slate-900"
              />
              <span>Scrape full text from paper URLs</span>
              <span className="text-[11px] text-gray-400 dark:text-slate-500">
                {scrapeFullText ? '(richer full-text context)' : '(abstracts only, faster)'}
              </span>
            </label>

            {selectedFile && (
              <span className="text-[11px]">
                {hasEmbeddings ? (
                  <span className="text-emerald-600 dark:text-emerald-400 font-medium">
                    ✓ Document chunks indexed in FAISS
                  </span>
                ) : (
                  <span className="text-amber-600 dark:text-amber-400">
                    Embeddings not built — queries will fallback to general AI knowledge
                  </span>
                )}
              </span>
            )}
          </div>

          {/* Error Banner */}
          {error && (
            <div className="mt-3.5 flex items-start gap-2.5 rounded-xl border border-rose-500/25 bg-rose-50 p-3 text-xs text-rose-700 dark:bg-rose-500/10 dark:text-rose-300">
              <XMarkIcon className="mt-0.5 h-4 w-4 shrink-0 text-rose-500" />
              <span className="flex-1 font-medium">{error}</span>
              <button
                onClick={() => setError('')}
                className="text-rose-400 hover:text-rose-600 dark:hover:text-rose-200"
              >
                <XMarkIcon className="h-4 w-4" />
              </button>
            </div>
          )}
        </div>
      </motion.div>

      {/* ── Main Chat Conversation Panel ── */}
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <div className="relative flex flex-col rounded-2xl border border-gray-200 dark:border-slate-800/60 bg-white dark:bg-slate-900 shadow-sm overflow-hidden">
          {/* Header */}
          <div className="flex items-center justify-between border-b border-gray-100 dark:border-slate-800/80 px-6 py-3.5 bg-gray-50/60 dark:bg-slate-950/40">
            <div className="flex items-center gap-2">
              <div className="h-1 w-5 rounded-full bg-sky-500" />
              <span className="text-xs font-bold uppercase tracking-[0.2em] text-gray-600 dark:text-slate-400">
                Conversation
              </span>
              {selectedFile && (
                <span className="ml-2 hidden sm:inline-flex items-center gap-1 rounded-md bg-gray-200/60 dark:bg-slate-800 px-2 py-0.5 text-[11px] font-medium text-gray-700 dark:text-slate-300 font-mono">
                  <DocumentTextIcon className="h-3 w-3 text-sky-500" />
                  {selectedFile}
                </span>
              )}
            </div>

            <div className="flex items-center gap-2">
              {messages.length > 1 && (
                <button
                  type="button"
                  onClick={clearConversation}
                  disabled={isLoading}
                  title="Clear conversation history"
                  className="flex items-center gap-1 rounded-lg px-2.5 py-1 text-xs font-medium text-gray-500 hover:bg-gray-200/60 dark:hover:bg-slate-800 hover:text-rose-600 dark:hover:text-rose-400 transition"
                >
                  <TrashIcon className="h-3.5 w-3.5" />
                  <span className="hidden sm:inline">Clear chat</span>
                </button>
              )}
            </div>
          </div>

          {/* Messages Scroll Area */}
          <div
            ref={scrollContainerRef}
            onScroll={handleScroll}
            className="flex flex-col min-h-[460px] max-h-[640px] overflow-y-auto p-6 space-y-4"
          >
            {/* Messages list */}
            {messages.map((msg, index) => (
              <ChatMessageItem
                key={msg.id || index}
                message={msg}
                isLastAssistantMessage={index === lastAssistantIndex}
                onRegenerate={regenerateResponse}
                disabled={isLoading}
              />
            ))}

            {/* Quick prompt suggestions when only the initial greeting is present */}
            {messages.length <= 1 && (
              <div className="my-6 rounded-2xl border border-sky-100 dark:border-slate-800/80 bg-sky-50/40 dark:bg-slate-950/40 p-5">
                <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-sky-600 dark:text-sky-400 mb-3">
                  <LightBulbIcon className="h-4 w-4" />
                  <span>Suggested Research Inquiries</span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {QUICK_PROMPTS.map((promptText, i) => (
                    <button
                      key={i}
                      type="button"
                      onClick={() => sendMessage(promptText)}
                      disabled={inputDisabled}
                      className="text-left rounded-xl border border-gray-200/80 dark:border-slate-800 bg-white dark:bg-slate-900 p-3 text-xs text-gray-700 dark:text-slate-300 hover:border-sky-400 hover:text-sky-600 dark:hover:text-sky-300 hover:shadow-sm transition disabled:opacity-50"
                    >
                      {promptText} →
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Live Loading Indicator */}
            {isLoading && (
              <ChatLoadingIndicator
                onStop={stopGeneration}
                statusMessage="Research Rover is searching paper embeddings & generating answer…"
              />
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Floating Scroll To Bottom Button */}
          {isScrolledUp && (
            <button
              type="button"
              onClick={scrollToBottom}
              className="absolute bottom-24 right-8 z-20 flex items-center gap-1 rounded-full bg-sky-600 text-white px-3 py-1.5 text-xs font-semibold shadow-lg hover:bg-sky-500 transition animate-bounce"
            >
              <ArrowDownCircleIcon className="h-4 w-4" />
              <span>Scroll to latest</span>
            </button>
          )}

          {/* Composer / Input Area */}
          <div className="border-t border-gray-100 dark:border-slate-800/80 bg-gray-50/50 dark:bg-slate-950/40 p-4">
            <div className="relative flex items-end gap-2.5 rounded-2xl border border-gray-300 dark:border-slate-700/80 bg-white dark:bg-slate-900 p-2 shadow-sm focus-within:border-sky-500 focus-within:ring-2 focus-within:ring-sky-500/20 transition">
              <textarea
                ref={textareaRef}
                rows={1}
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={inputDisabled}
                placeholder={inputPlaceholder}
                className="flex-1 max-h-[180px] min-h-[44px] resize-none border-0 bg-transparent px-3 py-2 text-sm leading-relaxed text-gray-800 placeholder:text-gray-400 outline-none dark:text-slate-100 dark:placeholder:text-slate-500 disabled:cursor-not-allowed disabled:opacity-50"
              />

              {/* Action Button: Send or Stop */}
              {isLoading ? (
                <button
                  type="button"
                  onClick={stopGeneration}
                  title="Stop generating response"
                  className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-rose-600 hover:bg-rose-500 text-white shadow-md shadow-rose-500/25 transition active:scale-95"
                >
                  <StopIcon className="h-5 w-5 stroke-[2.5]" />
                </button>
              ) : (
                <button
                  type="button"
                  onClick={() => sendMessage()}
                  disabled={sendDisabled}
                  title="Send message (Enter)"
                  className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-sky-500 to-indigo-600 text-white shadow-md shadow-sky-500/25 transition hover:from-sky-400 hover:to-indigo-500 hover:shadow-lg disabled:cursor-not-allowed disabled:opacity-40 active:scale-95"
                >
                  <PaperAirplaneIcon className="h-4 w-4 -rotate-45 -translate-y-0.5 translate-x-0.5" />
                </button>
              )}
            </div>

            {/* Hint row */}
            <div className="mt-2 flex items-center justify-between px-2 text-[11px] text-gray-400 dark:text-slate-500">
              <span>
                Tip: Press <kbd className="font-mono font-semibold">Enter</kbd> to send,{' '}
                <kbd className="font-mono font-semibold">Shift + Enter</kbd> for a new line
              </span>
              <span>RAG Knowledge Grounding</span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Modals */}
      <EmbeddingProgressModal />
      <DatasetQualityModal
        isOpen={isQualityModalOpen}
        onClose={() => setIsQualityModalOpen(false)}
        filename={selectedFile}
        initialData={selectedQualityData}
      />
    </div>
  )
}
