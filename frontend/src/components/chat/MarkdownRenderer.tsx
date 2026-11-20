import { useMemo } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'
import { CodeBlock } from './CodeBlock'
import { MermaidDiagram } from './MermaidDiagram'

interface MarkdownRendererProps {
  content: string
  onCitationClick?: (sourceId: number) => void
}

/**
 * Preprocess content to ensure robust KaTeX LaTeX rendering:
 * 1. Convert display math \[ ... \] to $$ ... $$
 * 2. Convert inline math \( ... \) to $ ... $
 * Leaves content inside code blocks intact.
 */
function preprocessMathAndFormatting(raw: string): string {
  if (!raw) return ''

  // Split content by fenced code blocks and inline code spans to avoid altering code syntax
  const segments = raw.split(/(```[\s\S]*?```|`[^`\n]+`)/g)

  for (let i = 0; i < segments.length; i += 2) {
    let text = segments[i]

    // Convert display math \[ ... \] into $$ ... $$
    text = text.replace(/\\\[([\s\S]*?)\\\]/g, (_match, math) => {
      return `\n$$\n${math.trim()}\n$$\n`
    })

    // Convert inline math \( ... \) into $ ... $
    text = text.replace(/\\\(([\s\S]*?)\\\)/g, (_match, math) => {
      return `$${math.trim()}$`
    })

    segments[i] = text
  }

  return segments.join('')
}

/**
 * Check if a code snippet is a Mermaid diagram even if language tag is omitted
 */
function isMermaidCode(lang: string, codeText: string): boolean {
  if (lang.toLowerCase() === 'mermaid') return true
  const trimmed = codeText.trim()
  return /^(graph|flowchart|sequenceDiagram|classDiagram|stateDiagram(-v2)?|erDiagram|gantt|pie|gitGraph|journey|mindmap|timeline)\b/m.test(
    trimmed
  )
}

export function MarkdownRenderer({ content, onCitationClick: _onCitationClick }: MarkdownRendererProps) {
  const processedContent = useMemo(() => {
    return preprocessMathAndFormatting(content)
  }, [content])

  return (
    <div className="research-rover-markdown w-full text-sm md:text-[15px] leading-relaxed text-gray-800 dark:text-slate-200 break-words">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeKatex]}
        components={{
          // Code block and inline code
          code({ className, children, ...props }) {
            const match = /language-(\w+)/.exec(className || '')
            const lang = match ? match[1] : ''
            const rawCode = String(children).replace(/\n$/, '')
            const isInline = !match && !rawCode.includes('\n') && !className

            if (isInline) {
              return (
                <code
                  className="rounded-md bg-gray-100 dark:bg-slate-800/90 px-1.5 py-0.5 font-mono text-[13px] font-medium text-sky-600 dark:text-sky-300 border border-gray-200/80 dark:border-slate-700/80"
                  {...props}
                >
                  {children}
                </code>
              )
            }

            // Check if this is a Mermaid diagram
            if (isMermaidCode(lang, rawCode)) {
              return <MermaidDiagram code={rawCode} />
            }

            return <CodeBlock language={lang} value={rawCode} />
          },

          // Paragraphs
          p({ children }) {
            return (
              <p className="mb-4 leading-relaxed text-gray-800 dark:text-slate-200 last:mb-0">
                {children}
              </p>
            )
          },

          // Headings H1 - H6
          h1({ children }) {
            return (
              <h1 className="mt-7 mb-4 text-2xl font-bold tracking-tight text-gray-900 dark:text-slate-50 border-b border-gray-200/80 dark:border-slate-800 pb-2.5">
                {children}
              </h1>
            )
          },
          h2({ children }) {
            return (
              <h2 className="mt-6 mb-3 text-xl font-bold tracking-tight text-gray-900 dark:text-slate-100 border-b border-gray-100 dark:border-slate-800/60 pb-2">
                {children}
              </h2>
            )
          },
          h3({ children }) {
            return (
              <h3 className="mt-5 mb-2.5 text-lg font-bold tracking-tight text-gray-900 dark:text-slate-200">
                {children}
              </h3>
            )
          },
          h4({ children }) {
            return (
              <h4 className="mt-4 mb-2 text-base font-semibold text-gray-800 dark:text-slate-200">
                {children}
              </h4>
            )
          },
          h5({ children }) {
            return (
              <h5 className="mt-3.5 mb-1.5 text-sm font-semibold uppercase tracking-wider text-gray-700 dark:text-slate-400">
                {children}
              </h5>
            )
          },
          h6({ children }) {
            return (
              <h6 className="mt-3 mb-1 text-xs font-semibold uppercase tracking-wider text-gray-600 dark:text-slate-500">
                {children}
              </h6>
            )
          },

          // Lists
          ul({ children }) {
            return (
              <ul className="my-3.5 ml-4 list-disc space-y-1.5 pl-2 text-gray-800 dark:text-slate-200">
                {children}
              </ul>
            )
          },
          ol({ children }) {
            return (
              <ol className="my-3.5 ml-4 list-decimal space-y-1.5 pl-2 text-gray-800 dark:text-slate-200">
                {children}
              </ol>
            )
          },
          li({ children }) {
            return <li className="leading-relaxed pl-1">{children}</li>
          },

          // Blockquotes
          blockquote({ children }) {
            return (
              <blockquote className="my-4 border-l-4 border-sky-500 bg-sky-50/60 dark:bg-sky-950/30 px-4 py-3 rounded-r-xl italic text-gray-700 dark:text-slate-300">
                {children}
              </blockquote>
            )
          },

          // Horizontal rule
          hr() {
            return <hr className="my-6 border-t border-gray-200 dark:border-slate-800" />
          },

          // Tables
          table({ children }) {
            return (
              <div className="my-4 overflow-x-auto rounded-xl border border-gray-200 dark:border-slate-800 shadow-sm">
                <table className="min-w-full divide-y divide-gray-200 dark:divide-slate-800 text-sm">
                  {children}
                </table>
              </div>
            )
          },
          thead({ children }) {
            return (
              <thead className="bg-gray-50/90 dark:bg-slate-900/90 text-xs font-bold uppercase tracking-wider text-gray-700 dark:text-slate-300 border-b border-gray-200 dark:border-slate-800">
                {children}
              </thead>
            )
          },
          tbody({ children }) {
            return (
              <tbody className="divide-y divide-gray-100 dark:divide-slate-800/60 bg-white dark:bg-slate-950/40">
                {children}
              </tbody>
            )
          },
          tr({ children }) {
            return (
              <tr className="transition-colors hover:bg-gray-50/70 dark:hover:bg-slate-900/40">
                {children}
              </tr>
            )
          },
          th({ children }) {
            return (
              <th className="px-4 py-3 text-left font-bold text-gray-900 dark:text-slate-100">
                {children}
              </th>
            )
          },
          td({ children }) {
            return (
              <td className="px-4 py-2.5 text-gray-800 dark:text-slate-200 leading-relaxed">
                {children}
              </td>
            )
          },

          // Links
          a({ href, children }) {
            return (
              <a
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sky-600 dark:text-sky-400 font-semibold underline decoration-sky-400/40 underline-offset-2 hover:text-sky-700 dark:hover:text-sky-300 transition-colors"
              >
                {children}
              </a>
            )
          },

          // Strong / Bold
          strong({ children }) {
            return <strong className="font-bold text-gray-900 dark:text-white">{children}</strong>
          },

          // Emphasis / Italic
          em({ children }) {
            return <em className="italic text-gray-800 dark:text-slate-200">{children}</em>
          },
        }}
      >
        {processedContent}
      </ReactMarkdown>
    </div>
  )
}
