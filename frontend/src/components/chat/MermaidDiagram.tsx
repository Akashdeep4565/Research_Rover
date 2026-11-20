import { useState, useEffect, useRef } from 'react'
import mermaid from 'mermaid'
import {
  MagnifyingGlassPlusIcon,
  MagnifyingGlassMinusIcon,
  ArrowPathIcon,
  ClipboardDocumentIcon,
  ClipboardDocumentCheckIcon,
  ExclamationTriangleIcon,
} from '@heroicons/react/24/outline'
import { CodeBlock } from './CodeBlock'
import { useTheme } from '@/components/theme-provider'

interface MermaidDiagramProps {
  code: string
}

function initMermaid(isDark: boolean) {
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: 'strict',
    theme: isDark ? 'dark' : 'default',
    fontFamily: 'ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    flowchart: {
      htmlLabels: false,
      useMaxWidth: false,
    },
  })
}

export function MermaidDiagram({ code }: MermaidDiagramProps) {
  const { theme } = useTheme()
  const isDark = theme === 'dark'
  const containerRef = useRef<HTMLDivElement>(null)
  const [svgHtml, setSvgHtml] = useState<string>('')
  const [renderError, setRenderError] = useState<string | null>(null)
  const [zoom, setZoom] = useState<number>(1)
  const [copied, setCopied] = useState<boolean>(false)
  const [isRendering, setIsRendering] = useState<boolean>(true)

  useEffect(() => {
    let isCancelled = false
    setIsRendering(true)
    setRenderError(null)

    // Re-initialize mermaid with current theme
    initMermaid(isDark)

    const renderDiagram = async () => {
      try {
        const cleanCode = code.trim()
        if (!cleanCode) {
          throw new Error('Diagram source is empty')
        }

        // Generate unique ID for this diagram render pass
        const id = `mermaid-${Date.now()}-${Math.random().toString(36).substring(2, 8)}`
        
        // Render diagram to SVG string
        const { svg } = await mermaid.render(id, cleanCode)
        
        if (!isCancelled) {
          setSvgHtml(svg)
          setRenderError(null)
          setIsRendering(false)
        }
      } catch (err: any) {
        if (!isCancelled) {
          console.warn('Mermaid render error:', err)
          setRenderError(err?.message || 'Failed to parse Mermaid diagram syntax')
          setIsRendering(false)
        }
      }
    }

    renderDiagram()

    return () => {
      isCancelled = true
    }
  }, [code, isDark])

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy mermaid code:', err)
    }
  }

  // If diagram failed to render, gracefully display error notice and raw source code
  if (renderError) {
    return (
      <div className="my-4 rounded-xl border border-amber-300 dark:border-amber-700/60 bg-amber-50/60 dark:bg-amber-950/20 p-4">
        <div className="flex items-center gap-2 text-xs font-semibold text-amber-800 dark:text-amber-300 mb-2">
          <ExclamationTriangleIcon className="h-4 w-4 text-amber-600 dark:text-amber-400" />
          <span>Diagram could not be rendered visually — showing source code:</span>
        </div>
        <CodeBlock language="mermaid" value={code} />
      </div>
    )
  }

  return (
    <div className="my-4 overflow-hidden rounded-xl border border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm">
      {/* Header toolbar */}
      <div className="flex items-center justify-between border-b border-gray-100 dark:border-slate-800/80 bg-gray-50/80 dark:bg-slate-950/50 px-4 py-2 text-xs text-gray-600 dark:text-slate-400">
        <div className="flex items-center gap-2">
          <span className="flex h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
          <span className="font-semibold text-gray-700 dark:text-slate-300">
            Diagram / Flowchart
          </span>
        </div>

        <div className="flex items-center gap-1.5">
          {/* Zoom controls */}
          <button
            type="button"
            onClick={() => setZoom((z) => Math.max(0.5, z - 0.15))}
            title="Zoom out"
            className="rounded p-1 text-gray-500 hover:bg-gray-200/60 hover:text-gray-800 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-slate-200 transition"
          >
            <MagnifyingGlassMinusIcon className="h-3.5 w-3.5" />
          </button>
          <span className="text-[11px] font-mono tabular-nums text-gray-500 dark:text-slate-400 min-w-[3rem] text-center">
            {Math.round(zoom * 100)}%
          </span>
          <button
            type="button"
            onClick={() => setZoom((z) => Math.min(2.5, z + 0.15))}
            title="Zoom in"
            className="rounded p-1 text-gray-500 hover:bg-gray-200/60 hover:text-gray-800 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-slate-200 transition"
          >
            <MagnifyingGlassPlusIcon className="h-3.5 w-3.5" />
          </button>
          <button
            type="button"
            onClick={() => setZoom(1)}
            title="Reset zoom"
            className="rounded p-1 text-gray-500 hover:bg-gray-200/60 hover:text-gray-800 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-slate-200 transition"
          >
            <ArrowPathIcon className="h-3.5 w-3.5" />
          </button>

          <div className="h-3.5 w-[1px] bg-gray-200 dark:bg-slate-700 mx-1" />

          {/* Copy diagram source */}
          <button
            type="button"
            onClick={handleCopy}
            className="flex items-center gap-1 rounded bg-gray-100 dark:bg-slate-800 px-2 py-1 text-xs font-medium text-gray-700 dark:text-slate-300 hover:bg-gray-200 dark:hover:bg-slate-700 transition"
          >
            {copied ? (
              <>
                <ClipboardDocumentCheckIcon className="h-3.5 w-3.5 text-emerald-600 dark:text-emerald-400" />
                <span className="text-emerald-600 dark:text-emerald-400">Copied</span>
              </>
            ) : (
              <>
                <ClipboardDocumentIcon className="h-3.5 w-3.5" />
                <span>Copy source</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Diagram Canvas */}
      <div
        ref={containerRef}
        className="relative overflow-x-auto overflow-y-hidden p-6 flex items-center justify-center min-h-[160px] bg-slate-50/40 dark:bg-slate-950/20"
      >
        {isRendering ? (
          <div className="flex items-center gap-2 text-xs text-gray-400 dark:text-slate-500 py-6">
            <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-sky-500 border-t-transparent" />
            <span>Rendering diagram…</span>
          </div>
        ) : (
          <div
            className="transition-transform duration-150 origin-center flex justify-center"
            style={{ transform: `scale(${zoom})`, transformOrigin: 'top center' }}
            dangerouslySetInnerHTML={{ __html: svgHtml }}
          />
        )}
      </div>
    </div>
  )
}
