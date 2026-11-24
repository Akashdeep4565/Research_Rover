import React, { useState, useEffect, useMemo, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  PlusIcon,
  ChatBubbleLeftRightIcon,
  ChevronLeftIcon,
  XMarkIcon,
  DocumentTextIcon,
  SparklesIcon,
  PencilSquareIcon,
  TrashIcon,
  CheckIcon,
  ArrowPathIcon,
  ExclamationTriangleIcon,
  ChatBubbleBottomCenterTextIcon,
} from '@heroicons/react/24/outline'
import { useChat } from '@/context/ChatContext'
import type { ConversationSummary } from '@/types'

// ─── Date Grouping Logic ───────────────────────────────────────────────────────

export interface GroupedConversations {
  today: ConversationSummary[]
  yesterday: ConversationSummary[]
  previous7Days: ConversationSummary[]
  older: ConversationSummary[]
}

export function groupConversationsByDate(conversations: ConversationSummary[]): GroupedConversations {
  const now = new Date()
  const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime()
  const yesterdayStart = todayStart - 86400000
  const sevenDaysAgoStart = todayStart - 6 * 86400000

  const groups: GroupedConversations = {
    today: [],
    yesterday: [],
    previous7Days: [],
    older: [],
  }

  for (const convo of conversations) {
    const updatedAtTime = new Date(convo.updated_at).getTime()
    if (isNaN(updatedAtTime)) {
      groups.older.push(convo)
    } else if (updatedAtTime >= todayStart) {
      groups.today.push(convo)
    } else if (updatedAtTime >= yesterdayStart) {
      groups.yesterday.push(convo)
    } else if (updatedAtTime >= sevenDaysAgoStart) {
      groups.previous7Days.push(convo)
    } else {
      groups.older.push(convo)
    }
  }

  return groups
}

function formatRelativeTimestamp(isoDate: string): string {
  const date = new Date(isoDate)
  if (isNaN(date.getTime())) return ''
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()

  // Less than 1 minute
  if (diffMs < 60000) return 'Just now'
  // Less than 1 hour
  if (diffMs < 3600000) {
    const mins = Math.floor(diffMs / 60000)
    return `${mins}m ago`
  }
  // Less than 24 hours
  if (diffMs < 86400000 && date.getDate() === now.getDate()) {
    return date.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })
  }
  // This year
  if (date.getFullYear() === now.getFullYear()) {
    return date.toLocaleDateString([], { month: 'short', day: 'numeric' })
  }
  return date.toLocaleDateString([], { year: 'numeric', month: 'short', day: 'numeric' })
}

// ─── Sidebar Component Props ──────────────────────────────────────────────────

export interface ChatHistorySidebarProps {
  isOpen: boolean
  onToggle: () => void
  onNewChat?: () => void
}

export function ChatHistorySidebar({ isOpen, onToggle, onNewChat }: ChatHistorySidebarProps) {
  const {
    activeConversationId,
    conversations,
    isLoadingConversations,
    conversationError,
    selectedFile,
    loadConversations,
    createNewConversation,
    selectConversation,
    renameConversation,
    deleteConversation,
    refreshConversations,
  } = useChat()

  const [filterMode, setFilterMode] = useState<'all' | 'collection'>('all')
  const [isCreatingNew, setIsCreatingNew] = useState(false)

  // Inline Rename State
  const [renamingId, setRenamingId] = useState<string | null>(null)
  const [renameTitle, setRenameTitle] = useState('')
  const [isSavingRename, setIsSavingRename] = useState(false)
  const [renameError, setRenameError] = useState<string | null>(null)
  const renameInputRef = useRef<HTMLInputElement>(null)

  // Delete Confirmation State
  const [deletingConvo, setDeletingConvo] = useState<ConversationSummary | null>(null)
  const [isDeleting, setIsDeleting] = useState(false)
  const [deleteError, setDeleteError] = useState<string | null>(null)

  // Focus rename input on entering edit mode
  useEffect(() => {
    if (renamingId && renameInputRef.current) {
      renameInputRef.current.focus()
      renameInputRef.current.select()
    }
  }, [renamingId])

  // Synchronize filter when switching mode or when selectedFile changes under 'collection' mode
  useEffect(() => {
    if (filterMode === 'all') {
      loadConversations(undefined)
    } else {
      loadConversations(selectedFile || '__general__')
    }
  }, [filterMode, selectedFile, loadConversations])

  // Filter conversations for the view
  const filteredConversations = useMemo(() => {
    if (filterMode === 'all') {
      return conversations
    }
    if (selectedFile) {
      return conversations.filter((c) => c.dataset_filename === selectedFile)
    }
    // General chat filter: conversations without dataset
    return conversations.filter((c) => !c.dataset_filename)
  }, [conversations, filterMode, selectedFile])

  // Date groups
  const grouped = useMemo(() => {
    return groupConversationsByDate(filteredConversations)
  }, [filteredConversations])

  // ─── Actions ────────────────────────────────────────────────────────────────

  const handleNewChat = async () => {
    if (isCreatingNew || isLoadingConversations) return
    setIsCreatingNew(true)
    try {
      const convo = await createNewConversation(undefined, selectedFile)
      if (convo && onNewChat) {
        onNewChat()
      }
      // On small screens, close the drawer after creating
      if (typeof window !== 'undefined' && window.innerWidth < 1024) {
        onToggle()
      }
    } catch (err) {
      console.error('Failed to create new conversation:', err)
    } finally {
      setIsCreatingNew(false)
    }
  }

  const handleSelectConversation = async (id: string) => {
    if (activeConversationId === id) return
    try {
      await selectConversation(id)
      if (typeof window !== 'undefined' && window.innerWidth < 1024) {
        onToggle()
      }
    } catch (err) {
      console.error('Failed to select conversation:', err)
    }
  }

  const handleStartRename = (convo: ConversationSummary, e: React.MouseEvent) => {
    e.stopPropagation()
    setRenamingId(convo.id)
    setRenameTitle(convo.title)
    setRenameError(null)
  }

  const handleCancelRename = () => {
    setRenamingId(null)
    setRenameTitle('')
    setRenameError(null)
  }

  const handleSaveRename = async (id: string) => {
    const trimmed = renameTitle.trim()
    if (!trimmed) {
      setRenameError('Title cannot be empty')
      return
    }
    if (trimmed.length > 255) {
      setRenameError('Title must be at most 255 characters')
      return
    }

    setIsSavingRename(true)
    setRenameError(null)
    try {
      await renameConversation(id, trimmed)
      setRenamingId(null)
      setRenameTitle('')
    } catch (err: any) {
      setRenameError(err?.message || 'Failed to save title')
    } finally {
      setIsSavingRename(false)
    }
  }

  const handleRenameKeyDown = (e: React.KeyboardEvent<HTMLInputElement>, id: string) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      handleSaveRename(id)
    } else if (e.key === 'Escape') {
      e.preventDefault()
      handleCancelRename()
    }
  }

  const handleOpenDelete = (convo: ConversationSummary, e: React.MouseEvent) => {
    e.stopPropagation()
    setDeletingConvo(convo)
    setDeleteError(null)
  }

  const handleCancelDelete = () => {
    setDeletingConvo(null)
    setDeleteError(null)
  }

  const handleConfirmDelete = async () => {
    if (!deletingConvo) return
    setIsDeleting(true)
    setDeleteError(null)
    try {
      await deleteConversation(deletingConvo.id)
      setDeletingConvo(null)
    } catch (err: any) {
      setDeleteError(err?.message || 'Failed to delete conversation')
    } finally {
      setIsDeleting(false)
    }
  }

  // ─── Render Helper: Conversation Item ────────────────────────────────────────

  const renderConversationItem = (convo: ConversationSummary) => {
    const isActive = convo.id === activeConversationId
    const isRenaming = convo.id === renamingId

    if (isRenaming) {
      return (
        <div
          key={convo.id}
          className="rounded-xl border border-sky-400 bg-sky-50/80 p-2.5 shadow-sm dark:border-sky-500/50 dark:bg-sky-950/40"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex items-center gap-1.5">
            <input
              ref={renameInputRef}
              type="text"
              value={renameTitle}
              maxLength={255}
              onChange={(e) => setRenameTitle(e.target.value)}
              onKeyDown={(e) => handleRenameKeyDown(e, convo.id)}
              disabled={isSavingRename}
              placeholder="Conversation title..."
              className="flex-1 rounded-lg border border-gray-300 bg-white px-2.5 py-1 text-xs text-gray-800 outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100"
            />
            <button
              type="button"
              onClick={() => handleSaveRename(convo.id)}
              disabled={isSavingRename || !renameTitle.trim()}
              title="Save rename"
              className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-sky-600 text-white hover:bg-sky-500 disabled:opacity-40 transition"
            >
              {isSavingRename ? (
                <ArrowPathIcon className="h-3.5 w-3.5 animate-spin" />
              ) : (
                <CheckIcon className="h-3.5 w-3.5 stroke-[2.5]" />
              )}
            </button>
            <button
              type="button"
              onClick={handleCancelRename}
              disabled={isSavingRename}
              title="Cancel rename"
              className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg border border-gray-300 text-gray-500 hover:bg-gray-100 dark:border-slate-700 dark:text-slate-400 dark:hover:bg-slate-800 transition"
            >
              <XMarkIcon className="h-3.5 w-3.5" />
            </button>
          </div>
          {renameError && (
            <div className="mt-1.5 text-[11px] text-rose-600 dark:text-rose-400 font-medium">
              {renameError}
            </div>
          )}
        </div>
      )
    }

    return (
      <div
        key={convo.id}
        onClick={() => handleSelectConversation(convo.id)}
        className={`group relative flex cursor-pointer flex-col gap-1 rounded-xl p-2.5 transition-all duration-150 ${
          isActive
            ? 'border border-sky-400/80 bg-sky-50/90 shadow-sm dark:border-sky-500/50 dark:bg-sky-950/40'
            : 'border border-transparent hover:border-gray-200 hover:bg-gray-50 dark:hover:border-slate-800/80 dark:hover:bg-slate-800/40'
        }`}
      >
        <div className="flex items-start justify-between gap-2">
          {/* Title */}
          <span
            className={`truncate text-xs font-medium leading-snug ${
              isActive
                ? 'text-sky-900 dark:text-sky-200 font-semibold'
                : 'text-gray-800 dark:text-slate-200 group-hover:text-gray-900 dark:group-hover:text-white'
            }`}
            title={convo.title}
          >
            {convo.title || 'Untitled Chat'}
          </span>

          {/* Action buttons (rename & delete) */}
          <div className="flex shrink-0 items-center gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity">
            <button
              type="button"
              onClick={(e) => handleStartRename(convo, e)}
              title="Rename conversation"
              className="rounded p-1 text-gray-400 hover:bg-gray-200/80 hover:text-gray-700 dark:hover:bg-slate-700 dark:hover:text-slate-200 transition"
            >
              <PencilSquareIcon className="h-3.5 w-3.5" />
            </button>
            <button
              type="button"
              onClick={(e) => handleOpenDelete(convo, e)}
              title="Delete conversation"
              className="rounded p-1 text-gray-400 hover:bg-rose-100 hover:text-rose-600 dark:hover:bg-rose-950/40 dark:hover:text-rose-400 transition"
            >
              <TrashIcon className="h-3.5 w-3.5" />
            </button>
          </div>
        </div>

        {/* Metadata row: Dataset badge + timestamp */}
        <div className="flex items-center justify-between text-[10px] text-gray-400 dark:text-slate-500">
          {convo.dataset_filename ? (
            <span
              className="inline-flex max-w-[150px] items-center gap-1 truncate rounded bg-gray-100 px-1.5 py-0.5 font-mono text-[10px] text-gray-600 dark:bg-slate-800 dark:text-slate-400"
              title={`Collection: ${convo.dataset_filename}`}
            >
              <DocumentTextIcon className="h-2.5 w-2.5 shrink-0 text-sky-500" />
              <span className="truncate">{convo.dataset_filename}</span>
            </span>
          ) : (
            <span
              className="inline-flex items-center gap-1 rounded bg-indigo-50 px-1.5 py-0.5 text-[10px] text-indigo-600 dark:bg-indigo-950/40 dark:text-indigo-400"
              title="General AI research query"
            >
              <SparklesIcon className="h-2.5 w-2.5 shrink-0" />
              <span>General Chat</span>
            </span>
          )}

          <span>{formatRelativeTimestamp(convo.updated_at)}</span>
        </div>
      </div>
    )
  }

  // ─── Group Rendering ─────────────────────────────────────────────────────────

  const renderGroup = (title: string, items: ConversationSummary[]) => {
    if (items.length === 0) return null
    return (
      <div key={title} className="space-y-1">
        <div className="px-2 pt-2 pb-1 text-[11px] font-bold uppercase tracking-wider text-gray-400 dark:text-slate-500">
          {title}
        </div>
        <div className="space-y-1">
          {items.map(renderConversationItem)}
        </div>
      </div>
    )
  }

  // ─── Main Sidebar Content ───────────────────────────────────────────────────

  const sidebarContent = (
    <div className="flex h-full flex-col bg-white dark:bg-slate-900 border-r border-gray-200 dark:border-slate-800/80">
      {/* ── Header ── */}
      <div className="p-4 border-b border-gray-100 dark:border-slate-800/80">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-sky-500/10 text-sky-600 dark:text-sky-400">
              <ChatBubbleLeftRightIcon className="h-4 w-4" />
            </div>
            <h2 className="text-sm font-bold text-gray-900 dark:text-slate-100">
              Research Chat
            </h2>
          </div>

          <div className="flex items-center gap-1">
            <button
              type="button"
              onClick={refreshConversations}
              disabled={isLoadingConversations}
              title="Refresh conversation list"
              className="rounded-lg p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-600 dark:hover:bg-slate-800 dark:hover:text-slate-300 transition"
            >
              <ArrowPathIcon className={`h-4 w-4 ${isLoadingConversations ? 'animate-spin' : ''}`} />
            </button>
            <button
              type="button"
              onClick={onToggle}
              title="Collapse sidebar"
              className="rounded-lg p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-600 dark:hover:bg-slate-800 dark:hover:text-slate-300 transition"
            >
              <ChevronLeftIcon className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* New Chat Button */}
        <button
          type="button"
          onClick={handleNewChat}
          disabled={isCreatingNew || isLoadingConversations}
          className="flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 px-3.5 py-2.5 text-xs font-semibold text-white shadow-sm shadow-sky-500/20 transition hover:from-sky-400 hover:to-indigo-500 hover:shadow-md disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isCreatingNew ? (
            <ArrowPathIcon className="h-4 w-4 animate-spin" />
          ) : (
            <PlusIcon className="h-4 w-4 stroke-[2.5]" />
          )}
          <span>New Research Chat</span>
        </button>

        {/* Filter Tabs: All vs Collection */}
        <div className="mt-3 flex rounded-xl bg-gray-100 dark:bg-slate-800/80 p-0.5 text-xs">
          <button
            type="button"
            onClick={() => setFilterMode('all')}
            className={`flex-1 py-1.5 rounded-lg text-xs font-semibold transition text-center ${
              filterMode === 'all'
                ? 'bg-white text-sky-600 shadow-sm dark:bg-slate-900 dark:text-sky-400'
                : 'text-gray-500 hover:text-gray-800 dark:text-slate-400 dark:hover:text-slate-200'
            }`}
          >
            All Chats
          </button>
          <button
            type="button"
            onClick={() => setFilterMode('collection')}
            className={`flex-1 py-1.5 rounded-lg text-xs font-semibold transition text-center truncate px-1 ${
              filterMode === 'collection'
                ? 'bg-white text-sky-600 shadow-sm dark:bg-slate-900 dark:text-sky-400'
                : 'text-gray-500 hover:text-gray-800 dark:text-slate-400 dark:hover:text-slate-200'
            }`}
            title={selectedFile ? `Collection: ${selectedFile}` : 'General Chat collection'}
          >
            {selectedFile ? 'Collection' : 'General Chat'}
          </button>
        </div>
      </div>

      {/* ── Conversation History List ── */}
      <div className="flex-1 overflow-y-auto p-3 space-y-3">
        {/* Error message */}
        {conversationError && (
          <div className="flex items-start gap-2 rounded-xl border border-rose-500/25 bg-rose-50 p-2.5 text-xs text-rose-700 dark:bg-rose-500/10 dark:text-rose-300">
            <ExclamationTriangleIcon className="h-4 w-4 shrink-0 text-rose-500" />
            <div className="flex-1 text-[11px] leading-tight font-medium">
              {conversationError}
            </div>
            <button
              type="button"
              onClick={refreshConversations}
              className="text-rose-600 dark:text-rose-400 underline text-[10px]"
            >
              Retry
            </button>
          </div>
        )}

        {/* Loading state */}
        {isLoadingConversations && filteredConversations.length === 0 ? (
          <div className="space-y-2 py-4 px-2">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="animate-pulse space-y-1.5 p-2">
                <div className="h-3.5 bg-gray-200 dark:bg-slate-800 rounded w-3/4" />
                <div className="h-2.5 bg-gray-100 dark:bg-slate-800/60 rounded w-1/2" />
              </div>
            ))}
          </div>
        ) : filteredConversations.length === 0 ? (
          /* Empty state */
          <div className="flex flex-col items-center justify-center py-10 px-4 text-center">
            <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gray-100 dark:bg-slate-800 text-gray-400 dark:text-slate-500 mb-2.5">
              <ChatBubbleBottomCenterTextIcon className="h-5 w-5" />
            </div>
            <p className="text-xs font-semibold text-gray-700 dark:text-slate-300">
              {filterMode === 'collection'
                ? selectedFile
                  ? `No chats for ${selectedFile}`
                  : 'No General Chat sessions yet'
                : 'No conversation history'}
            </p>
            <p className="mt-1 text-[11px] text-gray-400 dark:text-slate-500 max-w-[190px]">
              Click New Research Chat above to begin exploring your papers.
            </p>
          </div>
        ) : (
          /* Date-grouped lists */
          <div className="space-y-3">
            {renderGroup('Today', grouped.today)}
            {renderGroup('Yesterday', grouped.yesterday)}
            {renderGroup('Previous 7 Days', grouped.previous7Days)}
            {renderGroup('Older', grouped.older)}
          </div>
        )}
      </div>

      {/* ── Footer Info ── */}
      <div className="border-t border-gray-100 dark:border-slate-800/80 p-3 bg-gray-50/50 dark:bg-slate-950/30 text-center">
        <span className="text-[11px] text-gray-400 dark:text-slate-500">
          {filteredConversations.length} {filteredConversations.length === 1 ? 'chat session' : 'chat sessions'}
          {filterMode === 'collection' && (selectedFile ? ` in collection` : ' in general chat')}
        </span>
      </div>
    </div>
  )

  return (
    <>
      {/* ── Desktop Sidebar Container (lg and above) ── */}
      <div
        className={`hidden lg:flex flex-col shrink-0 transition-all duration-300 ease-in-out ${
          isOpen ? 'w-72 xl:w-80 opacity-100' : 'w-0 opacity-0 overflow-hidden pointer-events-none'
        }`}
      >
        <div className="w-72 xl:w-80 h-[calc(100vh-160px)] min-h-[640px] sticky top-24 rounded-2xl overflow-hidden border border-gray-200 dark:border-slate-800/80 shadow-sm">
          {sidebarContent}
        </div>
      </div>

      {/* ── Mobile / Tablet Slide-over Drawer (below lg) ── */}
      <AnimatePresence>
        {isOpen && (
          <div className="lg:hidden fixed inset-0 z-50 flex">
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={onToggle}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm"
            />

            {/* Off-canvas panel */}
            <motion.div
              initial={{ x: '-100%' }}
              animate={{ x: 0 }}
              exit={{ x: '-100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 300 }}
              className="relative w-80 max-w-[85vw] h-full shadow-2xl z-10"
            >
              {sidebarContent}
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      {/* ── Delete Confirmation Dialog Modal ── */}
      <AnimatePresence>
        {deletingConvo && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="w-full max-w-sm rounded-2xl border border-gray-200 bg-white p-5 shadow-2xl dark:border-slate-800 dark:bg-slate-900"
            >
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-rose-500/10 text-rose-600 dark:bg-rose-950/50 dark:text-rose-400">
                  <TrashIcon className="h-5 w-5" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-gray-900 dark:text-slate-100">
                    Delete Conversation?
                  </h3>
                  <p className="mt-0.5 text-xs text-gray-500 dark:text-slate-400">
                    This action cannot be undone.
                  </p>
                </div>
              </div>

              <div className="mt-3 rounded-xl bg-gray-50 p-3 text-xs text-gray-700 dark:bg-slate-950/60 dark:text-slate-300">
                <p className="font-semibold text-gray-900 dark:text-slate-100 truncate">
                  "{deletingConvo.title || 'Untitled Chat'}"
                </p>
                <p className="mt-1 text-[11px] text-gray-500 dark:text-slate-400">
                  All messages ({deletingConvo.message_count} turns) in this conversation will be permanently removed. Associated research CSV datasets and FAISS embeddings will remain intact.
                </p>
              </div>

              {deleteError && (
                <div className="mt-3 text-xs text-rose-600 dark:text-rose-400 font-medium">
                  {deleteError}
                </div>
              )}

              <div className="mt-5 flex items-center justify-end gap-2.5">
                <button
                  type="button"
                  onClick={handleCancelDelete}
                  disabled={isDeleting}
                  className="rounded-xl border border-gray-300 dark:border-slate-700 px-3.5 py-2 text-xs font-semibold text-gray-700 dark:text-slate-300 hover:bg-gray-100 dark:hover:bg-slate-800 transition"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={handleConfirmDelete}
                  disabled={isDeleting}
                  className="flex items-center gap-1.5 rounded-xl bg-rose-600 px-4 py-2 text-xs font-semibold text-white shadow-sm hover:bg-rose-500 disabled:opacity-50 transition"
                >
                  {isDeleting ? (
                    <ArrowPathIcon className="h-3.5 w-3.5 animate-spin" />
                  ) : (
                    <TrashIcon className="h-3.5 w-3.5" />
                  )}
                  <span>Delete Chat</span>
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </>
  )
}
