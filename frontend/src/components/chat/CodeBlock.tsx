import { useState } from 'react'
import hljs from 'highlight.js'
import {
  ClipboardDocumentIcon,
  ClipboardDocumentCheckIcon,
  CommandLineIcon,
  ArrowsPointingOutIcon,
  ArrowsPointingInIcon,
} from '@heroicons/react/24/outline'

interface CodeBlockProps {
  language?: string
  value: string
}

export function CodeBlock({ language = '', value = '' }: CodeBlockProps) {
  const [copied, setCopied] = useState(false)
  const [wrapLines, setWrapLines] = useState(false)

  const normalizedLang = language.trim().toLowerCase()
  const displayLang = normalizedLang || 'plaintext'

  // Syntax highlight with fallback to auto-detection
  let highlightedCode = ''
  try {
    if (normalizedLang && hljs.getLanguage(normalizedLang)) {
      highlightedCode = hljs.highlight(value, { language: normalizedLang, ignoreIllegals: true }).value
    } else {
      highlightedCode = hljs.highlightAuto(value).value
    }
  } catch {
    highlightedCode = value
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
  }

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(value)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy code:', err)
    }
  }

  return (
    <div className="my-4 overflow-hidden rounded-xl border border-gray-700/60 bg-[#1e1e2e] shadow-lg">
      {/* Header Bar */}
      <div className="flex items-center justify-between border-b border-gray-700/50 bg-[#181825] px-4 py-2 text-xs text-gray-300">
        <div className="flex items-center gap-2">
          <CommandLineIcon className="h-4 w-4 text-sky-400" />
          <span className="font-mono text-xs font-semibold uppercase tracking-wider text-sky-400">
            {displayLang}
          </span>
        </div>

        <div className="flex items-center gap-2">
          {/* Toggle Wrap Lines */}
          <button
            type="button"
            onClick={() => setWrapLines(!wrapLines)}
            title={wrapLines ? 'Enable horizontal scrolling' : 'Wrap lines'}
            className="flex items-center gap-1 rounded-md px-2 py-1 text-gray-400 transition hover:bg-white/5 hover:text-gray-200"
          >
            {wrapLines ? (
              <>
                <ArrowsPointingInIcon className="h-3.5 w-3.5" />
                <span className="text-[11px] hidden sm:inline">Unwrap</span>
              </>
            ) : (
              <>
                <ArrowsPointingOutIcon className="h-3.5 w-3.5" />
                <span className="text-[11px] hidden sm:inline">Wrap</span>
              </>
            )}
          </button>

          {/* Copy Code */}
          <button
            type="button"
            onClick={handleCopy}
            className="flex items-center gap-1.5 rounded-md bg-white/5 px-2.5 py-1 text-xs font-medium text-gray-200 transition hover:bg-white/10 hover:text-white"
          >
            {copied ? (
              <>
                <ClipboardDocumentCheckIcon className="h-3.5 w-3.5 text-emerald-400" />
                <span className="text-emerald-400">Copied!</span>
              </>
            ) : (
              <>
                <ClipboardDocumentIcon className="h-3.5 w-3.5 text-gray-300" />
                <span>Copy code</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Code Body */}
      <div className={`p-4 font-mono text-xs leading-relaxed text-gray-200 ${wrapLines ? 'whitespace-pre-wrap break-words' : 'overflow-x-auto whitespace-pre'}`}>
        <code
          className="hljs block font-mono"
          dangerouslySetInnerHTML={{ __html: highlightedCode }}
        />
      </div>
    </div>
  )
}
