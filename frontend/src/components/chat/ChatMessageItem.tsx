import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  UserIcon,
  CpuChipIcon,
  ClipboardDocumentIcon,
  ClipboardDocumentCheckIcon,
  ArrowPathIcon,
  DocumentTextIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  ArrowTopRightOnSquareIcon,
} from '@heroicons/react/24/outline'
import type { ChatMessage } from '@/types'
import { MarkdownRenderer } from './MarkdownRenderer'

interface ChatMessageItemProps {
  message: ChatMessage
  isLastAssistantMessage?: boolean
  onRegenerate?: () => void
  disabled?: boolean
}

export function ChatMessageItem({
  message,
  isLastAssistantMessage = false,
  onRegenerate,
  disabled = false,
}: ChatMessageItemProps) {
  const isUser = message.type === 'user'
  const [copied, setCopied] = useState(false)
  const [sourcesOpen, setSourcesOpen] = useState(false)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message.content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy response:', err)
    }
  }

  if (isUser) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.2 }}
        className="flex items-start justify-end gap-3 my-2"
      >
        <div className="flex max-w-[85%] sm:max-w-[75%] flex-col items-end gap-1.5">
          <div className="rounded-2xl rounded-tr-sm bg-gradient-to-br from-sky-600 via-sky-600 to-indigo-600 px-4 py-3 text-sm font-medium leading-relaxed text-white shadow-md shadow-sky-500/15 whitespace-pre-wrap break-words">
            {message.content}
          </div>
          <span className="text-[11px] tabular-nums text-gray-400 dark:text-slate-500 px-1">
            {new Date(message.timestamp).toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </span>
        </div>

        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-sky-500 to-indigo-600 text-white shadow-md shadow-sky-500/20">
          <UserIcon className="h-4 w-4" />
        </div>
      </motion.div>
    )
  }

  // Assistant Message
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2 }}
      className="flex items-start gap-3.5 my-3"
    >
      {/* AI Avatar */}
      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-sky-400/40 bg-sky-500/10 text-sky-600 shadow-sm dark:border-sky-500/30 dark:bg-sky-950/40 dark:text-sky-400">
        <CpuChipIcon className="h-5 w-5" />
      </div>

      {/* Main Response Container */}
      <div className="flex flex-1 min-w-0 max-w-full flex-col gap-2">
        <div className="rounded-2xl rounded-tl-sm border border-gray-200/90 dark:border-slate-800/80 bg-white dark:bg-slate-900/90 p-5 shadow-sm transition-shadow hover:shadow-md">
          {/* Markdown & LaTeX Rendered Body */}
          <MarkdownRenderer content={message.content} />

          {/* Sources Section */}
          {message.sources && message.sources.length > 0 && (
            <div className="mt-5 border-t border-gray-100 dark:border-slate-800/80 pt-4">
              <button
                type="button"
                onClick={() => setSourcesOpen(!sourcesOpen)}
                className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-slate-400 hover:text-sky-600 dark:hover:text-sky-400 transition-colors"
              >
                <DocumentTextIcon className="h-3.5 w-3.5 text-sky-500" />
                <span>
                  {message.sources.length} Cited Research Paper
                  {message.sources.length > 1 ? 's' : ''}
                </span>
                {sourcesOpen ? (
                  <ChevronUpIcon className="h-3.5 w-3.5" />
                ) : (
                  <ChevronDownIcon className="h-3.5 w-3.5" />
                )}
              </button>

              <AnimatePresence>
                {sourcesOpen && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    transition={{ duration: 0.2 }}
                    className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2.5 overflow-hidden"
                  >
                    {message.sources.map((source, index) => {
                      const url = source.url || (source.doi ? `https://doi.org/${source.doi}` : null)
                      return (
                        <div
                          key={source.id || index}
                          className="flex flex-col justify-between rounded-xl border border-gray-200/80 dark:border-slate-800 bg-gray-50/70 dark:bg-slate-950/50 p-3 text-xs transition hover:border-sky-400/50 hover:bg-sky-50/20 dark:hover:bg-sky-950/20"
                        >
                          <div className="space-y-1.5">
                            <div className="flex items-center gap-1.5">
                              <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-md border border-sky-500/30 bg-sky-500/10 text-[10px] font-bold text-sky-600 dark:text-sky-400">
                                {index + 1}
                              </span>
                              <span className="font-semibold text-gray-500 dark:text-slate-400 text-[10px] uppercase tracking-wider">
                                Source Reference
                              </span>
                            </div>

                            {source.title && (
                              <h4 className="font-semibold text-gray-900 dark:text-slate-100 line-clamp-2 leading-snug">
                                {source.title}
                              </h4>
                            )}

                            {source.content_preview && (
                              <p className="text-gray-500 dark:text-slate-400 line-clamp-2 text-[11px] leading-relaxed">
                                {source.content_preview}
                              </p>
                            )}
                          </div>

                          {url && (
                            <div className="mt-2.5 pt-2 border-t border-gray-200/60 dark:border-slate-800/60">
                              <a
                                href={url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-1 text-[11px] font-semibold text-sky-600 hover:text-sky-700 dark:text-sky-400 dark:hover:text-sky-300 transition"
                              >
                                <ArrowTopRightOnSquareIcon className="h-3 w-3" />
                                <span>View paper</span>
                              </a>
                            </div>
                          )}
                        </div>
                      )
                    })}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          )}
        </div>

        {/* Action Controls Bar */}
        <div className="flex items-center justify-between px-2 text-xs text-gray-400 dark:text-slate-500">
          <div className="flex items-center gap-2">
            {/* Copy Response Button */}
            <button
              type="button"
              onClick={handleCopy}
              className="flex items-center gap-1 rounded-md px-2 py-1 hover:bg-gray-100 dark:hover:bg-slate-800 hover:text-gray-700 dark:hover:text-slate-300 transition"
              title="Copy entire answer"
            >
              {copied ? (
                <>
                  <ClipboardDocumentCheckIcon className="h-3.5 w-3.5 text-emerald-500" />
                  <span className="text-emerald-500 font-medium">Copied</span>
                </>
              ) : (
                <>
                  <ClipboardDocumentIcon className="h-3.5 w-3.5" />
                  <span>Copy</span>
                </>
              )}
            </button>

            {/* Regenerate Response Button */}
            {isLastAssistantMessage && onRegenerate && (
              <button
                type="button"
                onClick={onRegenerate}
                disabled={disabled}
                className="flex items-center gap-1 rounded-md px-2 py-1 hover:bg-gray-100 dark:hover:bg-slate-800 hover:text-gray-700 dark:hover:text-slate-300 disabled:opacity-40 transition"
                title="Regenerate this response"
              >
                <ArrowPathIcon className="h-3.5 w-3.5" />
                <span>Regenerate</span>
              </button>
            )}
          </div>

          {/* Timestamp */}
          <span className="text-[11px] tabular-nums">
            {new Date(message.timestamp).toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </span>
        </div>
      </div>
    </motion.div>
  )
}
