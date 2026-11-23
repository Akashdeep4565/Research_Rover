import { useState, useEffect, useRef } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
  MagnifyingGlassIcon,
  DocumentArrowDownIcon,
  EyeIcon,
  CalendarIcon,
  TagIcon,
  LinkIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  ArrowTopRightOnSquareIcon,
  CpuChipIcon,
  UserGroupIcon,
  XCircleIcon,
  CheckCircleIcon,
  FunnelIcon,
  ChartBarIcon,
  SparklesIcon,
  ClockIcon,
  ArrowDownTrayIcon,
  DocumentTextIcon,
  ArrowPathIcon,
  ExclamationCircleIcon,
  GlobeAltIcon,
} from '@heroicons/react/24/outline'
import type { Paper } from '@/types'
import { filesApi, type SearchProgress } from '@/services/api'
import { useSearch } from '@/context/SearchContext'
import { ResearchRoverLoader } from '@/components/ResearchRoverLoader'
import { useEmbedding } from '@/context/EmbeddingContext'
import { EmbeddingProgressModal } from '@/components/EmbeddingProgressModal'

// ─── Dual-handle publication-year range slider ──────────────────────────────
const SLIDER_MIN_YEAR = 1950
const SLIDER_MAX_YEAR = new Date().getFullYear()

function YearRangeSlider({
  startDate,
  endDate,
  onChange,
}: {
  startDate?: string
  endDate?: string
  onChange: (range: { startDate?: string; endDate?: string }) => void
}) {
  const startYear = startDate ? Number(startDate.slice(0, 4)) : SLIDER_MIN_YEAR
  const endYear = endDate ? Number(endDate.slice(0, 4)) : SLIDER_MAX_YEAR
  const span = SLIDER_MAX_YEAR - SLIDER_MIN_YEAR
  const lowPct = ((startYear - SLIDER_MIN_YEAR) / span) * 100
  const highPct = ((endYear - SLIDER_MIN_YEAR) / span) * 100
  const isFullRange = startYear <= SLIDER_MIN_YEAR && endYear >= SLIDER_MAX_YEAR

  const emit = (lo: number, hi: number) =>
    onChange({
      startDate: lo <= SLIDER_MIN_YEAR ? undefined : `${lo}-01-01`,
      endDate: hi >= SLIDER_MAX_YEAR ? undefined : `${hi}-12-31`,
    })

  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center justify-between">
        <label className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
          Publication Years
        </label>
        <span className="flex items-center gap-2">
          <span className="text-xs font-semibold tabular-nums text-indigo-600 dark:text-indigo-400">
            {isFullRange ? 'All Years' : `${startYear} — ${endYear}`}
          </span>
          {!isFullRange && (
            <button
              type="button"
              onClick={() => onChange({ startDate: undefined, endDate: undefined })}
              className="text-xs font-medium text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400"
            >
              Reset
            </button>
          )}
        </span>
      </div>

      {/* Waveform visual density curve */}
      <div className="flex h-12 items-end gap-[1px] px-0.5">
        {Array.from({ length: span + 1 }, (_, i) => {
          const year = SLIDER_MIN_YEAR + i
          const t = i / span
          const base = Math.pow(t, 1.5) * 0.85 + 0.12
          const wave = Math.sin(t * Math.PI * 9) * 0.07
          const h = Math.max(0.1, Math.min(1, base + wave))
          const inRange = year >= startYear && year <= endYear
          return (
            <div
              key={year}
              className={`flex-1 rounded-t-sm transition-colors duration-200 ${
                inRange
                  ? 'bg-gradient-to-t from-indigo-500 to-teal-400'
                  : 'bg-slate-200 dark:bg-slate-700/60'
              }`}
              style={{ height: `${h * 100}%` }}
            />
          )
        })}
      </div>

      <div className="relative flex h-9 items-center">
        {/* Base track */}
        <div className="absolute h-1.5 w-full rounded-full bg-slate-200 dark:bg-slate-700" />
        {/* Selected span */}
        <div
          className="absolute h-1.5 rounded-full bg-gradient-to-r from-indigo-500 to-teal-500"
          style={{ left: `${lowPct}%`, right: `${100 - highPct}%` }}
        />
        {/* Lower handle */}
        <input
          type="range"
          min={SLIDER_MIN_YEAR}
          max={SLIDER_MAX_YEAR}
          value={startYear}
          aria-label="Earliest publication year"
          onChange={(e) => emit(Math.min(Number(e.target.value), endYear), endYear)}
          className="year-range"
          style={{ zIndex: lowPct > 50 ? 5 : 3 }}
        />
        {/* Upper handle */}
        <input
          type="range"
          min={SLIDER_MIN_YEAR}
          max={SLIDER_MAX_YEAR}
          value={endYear}
          aria-label="Latest publication year"
          onChange={(e) => emit(startYear, Math.max(Number(e.target.value), startYear))}
          className="year-range"
          style={{ zIndex: 4 }}
        />
      </div>

      <div className="flex justify-between text-[10px] font-mono text-slate-400 dark:text-slate-500">
        <span>{SLIDER_MIN_YEAR}</span>
        <span>{SLIDER_MAX_YEAR}</span>
      </div>
    </div>
  )
}

// ─── Spinner SVG ─────────────────────────────────────────────────────────────
function Spinner({ className = 'w-4 h-4' }: { className?: string }) {
  return (
    <svg className={`animate-spin ${className}`} fill="none" viewBox="0 0 24 24">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
      <path className="opacity-75" fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
    </svg>
  )
}

// ─── 5-Stage Progress Stepper ────────────────────────────────────────────────
const STEPS = [
  { stage: 0, label: 'Init', desc: 'Initialize' },
  { stage: 1, label: 'Query', desc: 'Federated Search' },
  { stage: 2, label: 'Process', desc: 'Deduplicate & Rank' },
  { stage: 3, label: 'Save', desc: 'Assemble Corpus' },
  { stage: 4, label: 'Done', desc: 'Results Ready' },
]

function SearchProgressPanel({
  progress,
  onCancel,
}: {
  progress: SearchProgress
  onCancel?: () => void
}) {
  const pct = Math.min(100, Math.max(0, progress.progress || 0))
  const currentStage = progress.stage || 0

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -16 }}
      className="w-full"
    >
      <div className="relative overflow-hidden rounded-3xl border border-slate-200/80 dark:border-slate-800 bg-white/90 dark:bg-slate-900/90 backdrop-blur-xl p-6 sm:p-7 shadow-lg shadow-indigo-500/5 space-y-6">
        {/* Ambient top glow */}
        <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/[0.04] via-teal-500/[0.04] to-transparent pointer-events-none" />

        {/* Top Header */}
        <div className="relative flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="relative flex items-center justify-center w-11 h-11 rounded-2xl bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200/60 dark:border-indigo-800/60 text-indigo-600 dark:text-indigo-400 shrink-0 shadow-xs">
              <SparklesIcon className="w-5 h-5 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">
                  Federated Retrieval in Progress
                </h3>
                <span className="flex h-2 w-2 relative">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-teal-400 opacity-75" />
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-teal-500" />
                </span>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                Querying PubMed Central &amp; OpenAlex with MedCPT semantic re-ranking
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3 self-end sm:self-auto">
            <span className="text-xl font-mono font-extrabold text-indigo-600 dark:text-indigo-400 tabular-nums">
              {Math.round(pct)}%
            </span>
            {onCancel && (
              <button
                type="button"
                onClick={onCancel}
                className="inline-flex items-center gap-1.5 h-8 px-3.5 rounded-xl text-xs font-semibold text-rose-600 dark:text-rose-400 bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 hover:bg-rose-100 dark:hover:bg-rose-900/50 active:scale-95 transition-all shadow-xs"
              >
                <XCircleIcon className="w-4 h-4" />
                <span>Cancel Search</span>
              </button>
            )}
          </div>
        </div>

        {/* Animated Progress Bar */}
        <div className="relative h-2.5 w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden p-0.5 shadow-inner">
          <motion.div
            className="h-full rounded-full bg-gradient-to-r from-indigo-500 via-teal-400 to-indigo-600 shadow-sm"
            animate={{ width: `${pct}%` }}
            transition={{ duration: 0.4, ease: 'easeOut' }}
          />
        </div>

        {/* 5-Stage Stepper Tracker */}
        <div className="grid grid-cols-5 gap-2 pt-1">
          {STEPS.map((step, idx) => {
            const isDone = currentStage > step.stage || progress.status === 'completed'
            const isActive = currentStage === step.stage && progress.status !== 'completed'

            return (
              <div key={step.stage} className="flex flex-col items-center text-center gap-2 relative">
                {/* Connector line between steps */}
                {idx < STEPS.length - 1 && (
                  <div
                    className={`hidden sm:block absolute top-4 left-1/2 w-full h-[2px] -z-0 transition-colors duration-300 ${
                      isDone
                        ? 'bg-emerald-500/80 dark:bg-emerald-500/60'
                        : isActive
                        ? 'bg-indigo-300 dark:bg-indigo-700'
                        : 'bg-slate-200 dark:bg-slate-700'
                    }`}
                  />
                )}

                {/* Step indicator circle */}
                <div
                  className={`relative z-10 w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all duration-300 ${
                    isDone
                      ? 'bg-emerald-500 text-white shadow-sm shadow-emerald-500/25 ring-2 ring-emerald-100 dark:ring-emerald-950/60'
                      : isActive
                      ? 'bg-indigo-600 text-white ring-4 ring-indigo-100 dark:ring-indigo-950/80 shadow-md shadow-indigo-500/25 scale-105'
                      : 'bg-slate-100 dark:bg-slate-800 text-slate-400 dark:text-slate-500 border border-slate-200/80 dark:border-slate-700'
                  }`}
                >
                  {isDone ? (
                    <CheckCircleIcon className="w-4 h-4" />
                  ) : isActive ? (
                    <span className="flex h-2 w-2 rounded-full bg-white animate-ping" />
                  ) : (
                    step.stage + 1
                  )}
                </div>

                {/* Labels */}
                <div className="space-y-0.5">
                  <span
                    className={`block text-xs font-bold transition-colors ${
                      isActive
                        ? 'text-indigo-600 dark:text-indigo-400'
                        : isDone
                        ? 'text-slate-800 dark:text-slate-200'
                        : 'text-slate-400 dark:text-slate-500'
                    }`}
                  >
                    {step.label}
                  </span>
                  <span className="hidden sm:block text-[10px] text-slate-400 dark:text-slate-500 font-medium">
                    {step.desc}
                  </span>
                </div>
              </div>
            )
          })}
        </div>

        {/* Backend Status Message */}
        <div className="flex items-center justify-center gap-2.5 p-3 rounded-2xl bg-slate-50/90 dark:bg-slate-800/60 border border-slate-200/60 dark:border-slate-700/60 text-center">
          <Spinner className="w-4 h-4 text-indigo-500 shrink-0" />
          <p className="text-xs sm:text-sm font-medium text-slate-700 dark:text-slate-300 truncate">
            {progress.message || 'Processing research papers…'}
          </p>
        </div>
      </div>
    </motion.div>
  )
}

// ─── Paper card ───────────────────────────────────────────────────────────────
function PaperCard({ paper, index }: { paper: Paper; index: number }) {
  const [expanded, setExpanded] = useState(false)
  const [isDownloading, setIsDownloading] = useState(false)
  const [notice, setNotice] = useState<string | null>(null)

  const handleDownloadPdf = async () => {
    if (!paper.pdf_url || isDownloading) return
    setIsDownloading(true)
    setNotice(null)

    try {
      const { blob, filename } = await filesApi.downloadPdf(
        paper.pdf_url,
        paper.title,
        paper.doi,
        paper.pmid
      )
      const blobUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = blobUrl
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(blobUrl)
    } catch (err: any) {
      const code = err?.code
      const msg = err?.error || err?.detail || ''
      if (paper.pdf_url) {
        window.open(paper.pdf_url, '_blank')
        if (code === '422' || msg.toLowerCase().includes('pmc')) {
          setNotice('Opening direct PDF in new tab (verification required)')
        } else if (code === '403') {
          setNotice('Opening link in new tab (publisher subscription required)')
        } else {
          setNotice('Opening direct link in new tab…')
        }
      } else {
        setNotice(msg || 'Download failed')
      }
    } finally {
      setIsDownloading(false)
    }
  }

  // Rank badge
  const rankLabel = `#${index + 1}`

  // Source badge styling
  const getSourceBadge = () => {
    const s = (paper.source || '').toLowerCase()
    if (s.includes('pubmed') && s.includes('openalex')) {
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-purple-50 text-purple-700 dark:bg-purple-950/60 dark:text-purple-300 border border-purple-200/80 dark:border-purple-800">
          PubMed + OpenAlex
        </span>
      )
    } else if (s.includes('openalex')) {
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-teal-50 text-teal-700 dark:bg-teal-950/60 dark:text-teal-300 border border-teal-200/80 dark:border-teal-800">
          OpenAlex
        </span>
      )
    } else if (s.includes('pubmed')) {
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-700 dark:bg-indigo-950/60 dark:text-indigo-300 border border-indigo-200/80 dark:border-indigo-800">
          PubMed
        </span>
      )
    }
    return (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
        {paper.source}
      </span>
    )
  }

  return (
    <motion.article
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: Math.min(index * 0.03, 0.3) }}
      className="group relative rounded-3xl border border-slate-200/80 dark:border-slate-800 bg-white/90 dark:bg-slate-900/90 backdrop-blur-xl p-5 sm:p-7 shadow-sm hover:shadow-xl hover:border-indigo-400/60 dark:hover:border-indigo-500/60 transition-all duration-300"
    >
      {/* Ambient hover glow */}
      <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-indigo-500/[0.03] via-teal-500/[0.03] to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />

      <div className="relative flex flex-col gap-4">
        {/* Top Badges Row: Rank, Source, Open Access, Relevance Score */}
        <div className="flex flex-wrap items-center justify-between gap-2.5">
          <div className="flex flex-wrap items-center gap-2">
            {/* Rank badge */}
            <span
              title={`Rank #${index + 1}`}
              className="inline-flex items-center justify-center h-6 min-w-7 px-2 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200/80 dark:border-slate-700 font-mono text-xs font-bold"
            >
              {rankLabel}
            </span>

            {/* Source badge */}
            {getSourceBadge()}

            {/* Open Access badge */}
            {paper.is_oa && (
              <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-200/80 dark:border-emerald-800">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                Open Access
              </span>
            )}
          </div>

          {/* Relevance score (only when present in data) */}
          {paper.relevance_score != null && (
            <div className="flex items-center">
              <span
                title="Semantic relevance to your query (MedCPT cross-encoder), relative within this result set"
                className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-teal-50 text-teal-700 dark:bg-teal-950/60 dark:text-teal-300 border border-teal-200/80 dark:border-teal-800 shadow-xs"
              >
                <SparklesIcon className="w-3.5 h-3.5 text-teal-600 dark:text-teal-400" />
                <span>{Math.round(paper.relevance_score)}% Match</span>
              </span>
            </div>
          )}
        </div>

        {/* Publication Title */}
        <div>
          {paper.download_url ? (
            <a
              href={paper.download_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-base sm:text-lg font-bold text-slate-900 dark:text-slate-100 hover:text-indigo-600 dark:hover:text-indigo-400 leading-snug tracking-tight transition-colors inline-flex items-start gap-1.5"
            >
              <span>{paper.title}</span>
              <ArrowTopRightOnSquareIcon className="w-4 h-4 mt-1 shrink-0 opacity-60 group-hover:opacity-100 transition-opacity" />
            </a>
          ) : (
            <h3 className="text-base sm:text-lg font-bold text-slate-900 dark:text-slate-100 leading-snug tracking-tight">
              {paper.title}
            </h3>
          )}
        </div>

        {/* Bibliographic Metadata Row */}
        <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-slate-500 dark:text-slate-400">
          {/* Authors */}
          {paper.authors && paper.authors.length > 0 && (
            <span className="flex items-center gap-1.5 font-medium">
              <UserGroupIcon className="w-3.5 h-3.5 text-slate-400 shrink-0" />
              <span>
                {paper.authors.slice(0, 3).join(', ')}
                {paper.authors.length > 3 && ` +${paper.authors.length - 3}`}
              </span>
            </span>
          )}

          {/* Publication Year */}
          {paper.year && (
            <span className="flex items-center gap-1.5 font-medium">
              <CalendarIcon className="w-3.5 h-3.5 text-slate-400 shrink-0" />
              <span>{paper.year}</span>
            </span>
          )}

          {/* Citations */}
          {paper.citation_count != null && (
            <span className="flex items-center gap-1.5 font-semibold text-indigo-600 dark:text-indigo-400">
              <ChartBarIcon className="w-3.5 h-3.5 shrink-0" />
              <span>{paper.citation_count.toLocaleString()} citations</span>
            </span>
          )}

          {/* DOI */}
          {paper.doi && (
            <a
              href={`https://doi.org/${paper.doi}`}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1.5 text-slate-500 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
            >
              <LinkIcon className="w-3.5 h-3.5 shrink-0" />
              <span className="font-mono text-[11px]">DOI: {paper.doi}</span>
            </a>
          )}

          {/* PMID */}
          {paper.pmid && (
            <a
              href={`https://pubmed.ncbi.nlm.nih.gov/${paper.pmid}`}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1.5 text-slate-500 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
            >
              <DocumentTextIcon className="w-3.5 h-3.5 shrink-0" />
              <span className="font-mono text-[11px]">PMID: {paper.pmid}</span>
            </a>
          )}

          {/* Countries */}
          {paper.countries && paper.countries.length > 0 && (
            <span className="flex items-center gap-1.5">
              <GlobeAltIcon className="w-3.5 h-3.5 text-slate-400 shrink-0" />
              <span>{paper.countries.slice(0, 2).join(', ')}</span>
            </span>
          )}
        </div>

        {/* Abstract */}
        {paper.abstract && (
          <div className="pt-1">
            <p className={`text-sm text-slate-600 dark:text-slate-300 leading-relaxed font-normal ${expanded ? '' : 'line-clamp-3'}`}>
              {paper.abstract}
            </p>
            <button
              type="button"
              onClick={() => setExpanded(!expanded)}
              className="inline-flex items-center gap-1 text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 mt-2 transition-colors"
            >
              <span>{expanded ? 'Show less' : 'Read full abstract'}</span>
              {expanded ? (
                <ChevronUpIcon className="w-3.5 h-3.5" />
              ) : (
                <ChevronDownIcon className="w-3.5 h-3.5" />
              )}
            </button>
          </div>
        )}

        {/* Keyword Chips */}
        {paper.keywords && paper.keywords.length > 0 && (
          <div className="flex flex-wrap items-center gap-1.5 pt-1">
            <TagIcon className="w-3.5 h-3.5 text-slate-400 shrink-0" />
            {paper.keywords.slice(0, 6).map((kw, i) => (
              <span
                key={i}
                className="inline-flex items-center px-2.5 py-0.5 rounded-lg text-xs font-medium bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 border border-slate-200/60 dark:border-slate-700/60"
              >
                {kw}
              </span>
            ))}
            {paper.keywords.length > 6 && (
              <span className="text-xs text-slate-400 dark:text-slate-500 font-medium">
                +{paper.keywords.length - 6} more
              </span>
            )}
          </div>
        )}

        {/* Action Buttons Row */}
        <div className="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-100 dark:border-slate-800/80">
          <div className="flex flex-wrap items-center gap-2.5">
            {/* PDF Download Button */}
            {paper.pdf_url ? (
              <button
                type="button"
                onClick={handleDownloadPdf}
                disabled={isDownloading}
                className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-700 text-white shadow-md shadow-indigo-500/20 disabled:opacity-60 disabled:cursor-not-allowed transition-all active:scale-95"
                title="Download full-text PDF directly"
              >
                {isDownloading ? (
                  <>
                    <Spinner className="w-3.5 h-3.5 text-white" />
                    <span>Downloading…</span>
                  </>
                ) : (
                  <>
                    <ArrowDownTrayIcon className="w-3.5 h-3.5 text-white stroke-[2.2]" />
                    <span>Download PDF</span>
                  </>
                )}
              </button>
            ) : (
              <span
                className="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-medium text-slate-400 dark:text-slate-500 bg-slate-100/70 dark:bg-slate-800/50 border border-slate-200/60 dark:border-slate-700/40"
                title="No direct open-access PDF download found for this paper"
              >
                <DocumentTextIcon className="w-3.5 h-3.5 opacity-70" />
                <span>PDF not available</span>
              </span>
            )}

            {/* View Paper Button */}
            {paper.download_url && (
              <button
                type="button"
                onClick={() => window.open(paper.download_url!, '_blank')}
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold text-slate-700 dark:text-slate-200 hover:text-indigo-600 dark:hover:text-indigo-400 border border-slate-200/80 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-750 transition-all shadow-xs"
                title="Open paper source in new tab"
              >
                <EyeIcon className="w-3.5 h-3.5" />
                <span>View Paper</span>
              </button>
            )}
          </div>

          {/* Notice Feedback */}
          {notice && (
            <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs text-amber-600 dark:text-amber-400 font-medium bg-amber-50 dark:bg-amber-950/40 border border-amber-200/60 dark:border-amber-800/60">
              <ExclamationCircleIcon className="w-3.5 h-3.5 shrink-0" />
              <span>{notice}</span>
            </div>
          )}
        </div>
      </div>
    </motion.article>
  )
}

// ─── Main page ────────────────────────────────────────────────────────────────
export function SearchPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const searchInputRef = useRef<HTMLInputElement>(null)

  const {
    query, setQuery,
    filters, setFilters,
    isLoading,
    allResults,
    displayedResults,
    csvFilename,
    searchProgress,
    error, setError,
    currentPage, setCurrentPage,
    totalResults,
    totalPages,
    perPage, setPerPage,
    handleSearch,
    handleCancel,
    handlePageChange,
  } = useSearch()

  const { startEmbeddings } = useEmbedding()

  // Mobile/Tablet filter panel toggle
  const [showFiltersMobile, setShowFiltersMobile] = useState(false)

  // Handle navigation directives (e.g. from Discover Quick Actions)
  useEffect(() => {
    const state = location.state as {
      focusSearch?: boolean
      openAdvancedFilters?: boolean
      showEmbeddings?: boolean
    } | null

    if (state?.openAdvancedFilters) {
      setShowFiltersMobile(true)
    }
    if (state?.focusSearch) {
      setTimeout(() => {
        searchInputRef.current?.focus()
      }, 150)
    }
    if (state?.showEmbeddings && csvFilename) {
      setError('')
      startEmbeddings(csvFilename)
    }
  }, [location.state, csvFilename])

  // Keyboard shortcut ⌘K / Ctrl+K
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        searchInputRef.current?.focus()
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  // Pending query ref for instant search on example click
  const pendingSearchRef = useRef<string | null>(null)

  const handleExampleClick = (exampleQuery: string) => {
    setQuery(exampleQuery)
    pendingSearchRef.current = exampleQuery
  }

  useEffect(() => {
    if (pendingSearchRef.current && query === pendingSearchRef.current && !isLoading) {
      pendingSearchRef.current = null
      handleSearch()
    }
  }, [query, isLoading, handleSearch])

  const handleDownload = async () => {
    if (!csvFilename) return
    try {
      const blob = await filesApi.download(csvFilename)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = csvFilename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err: any) {
      setError(err.error || 'Failed to download file')
    }
  }

  const handleCreateEmbeddings = async () => {
    if (!csvFilename) return
    setError('')
    await startEmbeddings(csvFilename)
  }

  // Active filter count for mobile badge
  const activeFilterCount =
    (filters.source !== 'unified' ? 1 : 0) +
    (filters.startDate || filters.endDate ? 1 : 0) +
    (filters.maxResults && filters.maxResults !== 100 ? 1 : 0) +
    (filters.sortMode && filters.sortMode !== 'relevance' ? 1 : 0)

  // Reset filters while preserving query
  const handleResetFilters = () => {
    setFilters({
      source: 'unified',
      maxResults: 100,
      startDate: undefined,
      endDate: undefined,
      sortMode: 'relevance',
    })
  }

  return (
    <div className="relative w-full max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-8">
      {/* ─── Ambient Glow Blobs ──────────────────────────────────────────────── */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden -z-10 select-none">
        <div className="absolute -top-32 -left-32 w-96 h-96 rounded-full bg-teal-500/10 dark:bg-teal-500/5 blur-3xl" />
        <div className="absolute top-1/4 -right-20 w-80 h-80 rounded-full bg-indigo-500/10 dark:bg-indigo-500/5 blur-3xl" />
      </div>

      {/* ─── A. Literature Explorer Header ───────────────────────────────────── */}
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-2"
      >
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-indigo-50 dark:bg-indigo-950/40 text-indigo-700 dark:text-indigo-300 border border-indigo-200/60 dark:border-indigo-800 text-xs font-semibold">
          <SparklesIcon className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400" />
          <span>Literature Explorer</span>
          <span className="text-slate-300 dark:text-slate-700">•</span>
          <span>Federated Multi-Source Discovery</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900 dark:text-slate-100">
          Scholarly Literature Search
        </h1>
        <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 max-w-3xl leading-relaxed">
          Query peer-reviewed publications across NIH PubMed Central and OpenAlex with automatic deduplication, MedCPT semantic match scoring, and direct PDF downloads.
        </p>
      </motion.div>

      {/* ─── Search Input Bar Centerpiece ─────────────────────────────────────── */}
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <Card className="border border-slate-200/80 dark:border-slate-800 bg-white/85 dark:bg-slate-900/85 backdrop-blur-xl shadow-lg shadow-indigo-500/5 rounded-3xl">
          <CardContent className="p-5 sm:p-6 space-y-4">
            {/* Input + Action row */}
            <div className="flex flex-col sm:flex-row gap-3">
              <div className="flex-1 relative">
                <MagnifyingGlassIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" />
                <input
                  ref={searchInputRef}
                  placeholder="Search research questions, topics, hypotheses, PMIDs, or DOIs…"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && !isLoading && handleSearch()}
                  disabled={isLoading}
                  className="w-full h-12 pl-12 pr-12 rounded-2xl border border-slate-200/80 dark:border-slate-700
                             bg-slate-50/80 dark:bg-slate-800/60 text-sm text-slate-900 dark:text-slate-100
                             placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white dark:focus:bg-slate-900 disabled:opacity-50 transition"
                />
                {query && !isLoading && (
                  <button
                    type="button"
                    onClick={() => {
                      setQuery('')
                      searchInputRef.current?.focus()
                    }}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 p-1 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
                  >
                    <XCircleIcon className="w-4 h-4" />
                  </button>
                )}
              </div>

              <div className="flex items-center gap-2">
                <Button
                  onClick={handleSearch}
                  disabled={isLoading || !query.trim()}
                  className="h-12 px-7 rounded-2xl font-semibold text-sm text-white bg-indigo-600 hover:bg-indigo-700 shadow-md shadow-indigo-500/20 active:scale-95 transition-all flex items-center gap-2"
                >
                  {isLoading ? (
                    <>
                      <Spinner className="w-4 h-4" />
                      <span>Searching…</span>
                    </>
                  ) : (
                    <>
                      <MagnifyingGlassIcon className="w-4 h-4" />
                      <span>Search</span>
                    </>
                  )}
                </Button>

                {isLoading && (
                  <Button
                    onClick={handleCancel}
                    variant="outline"
                    className="h-12 px-5 rounded-2xl font-semibold text-sm text-rose-600 dark:text-rose-400 border-rose-200 dark:border-rose-800 hover:bg-rose-50 dark:hover:bg-rose-950/30 transition-all flex items-center gap-2"
                  >
                    <XCircleIcon className="w-4 h-4" />
                    <span>Cancel</span>
                  </Button>
                )}
              </div>
            </div>

            {/* Query syntax tip */}
            <div className="flex flex-wrap items-center justify-between gap-2 text-xs text-slate-500 dark:text-slate-400 pt-1">
              <p>
                <span className="font-semibold text-slate-700 dark:text-slate-300">Tip:</span> Separate distinct concepts with commas to AND them together (e.g.{' '}
                <span className="font-mono text-indigo-600 dark:text-indigo-400">smart healthcare, machine learning</span>).
              </p>
              <span className="inline-flex items-center gap-1 font-mono text-[11px] text-slate-400">
                <SparklesIcon className="w-3.5 h-3.5 text-indigo-500" />
                Synonym &amp; MeSH expansion active
              </span>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* ─── Mobile / Tablet Filter Toggle Bar (< xl) ─────────────────────────── */}
      <div className="xl:hidden flex items-center justify-between p-4 rounded-2xl bg-white/80 dark:bg-slate-900/80 border border-slate-200/80 dark:border-slate-800 shadow-sm">
        <button
          type="button"
          onClick={() => setShowFiltersMobile(!showFiltersMobile)}
          className="inline-flex items-center gap-2 text-sm font-semibold text-slate-800 dark:text-slate-200"
        >
          <FunnelIcon className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
          <span>{showFiltersMobile ? 'Hide Filters' : 'Filter Search Results'}</span>
          {activeFilterCount > 0 && (
            <span className="px-2 py-0.5 rounded-full bg-indigo-100 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 text-xs font-bold">
              {activeFilterCount} active
            </span>
          )}
        </button>
        <button
          type="button"
          onClick={handleResetFilters}
          className="text-xs font-medium text-slate-500 hover:text-indigo-600 dark:hover:text-indigo-400"
        >
          Reset Filters
        </button>
      </div>

      {/* ─── B. 12-Column Search Workspace ────────────────────────────────────── */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-8 items-start">

        {/* ─── LEFT RAIL: Precision Filters (4 Cols on xl) ────────────────────── */}
        <aside className={`xl:col-span-4 ${showFiltersMobile ? 'block' : 'hidden xl:block'} space-y-6`}>
          <div className="bg-white/85 dark:bg-slate-900/85 backdrop-blur-xl rounded-3xl p-6 border border-slate-200/70 dark:border-slate-800 shadow-md space-y-6">
            {/* Filter Header */}
            <div className="flex items-center justify-between pb-2 border-b border-slate-100 dark:border-slate-800">
              <div className="flex items-center gap-2">
                <FunnelIcon className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                <h2 className="font-bold text-sm text-slate-900 dark:text-slate-100 uppercase tracking-wider">
                  Precision Filters
                </h2>
              </div>
              <button
                type="button"
                onClick={handleResetFilters}
                className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1"
              >
                <ArrowPathIcon className="w-3 h-3" />
                <span>Reset All</span>
              </button>
            </div>

            {/* ─── C. Repository Source Selector ─── */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                  Repository Source
                </label>
                <span className="text-[11px] font-mono text-indigo-600 dark:text-indigo-400 font-medium">
                  Single Select
                </span>
              </div>

              <div className="space-y-2">
                {[
                  {
                    id: 'unified' as const,
                    title: 'Unified Search',
                    subtitle: 'Cross-query PubMed Central & OpenAlex',
                    tag: 'Default',
                  },
                  {
                    id: 'pubmed' as const,
                    title: 'PubMed Central',
                    subtitle: 'NIH / NLM biomedical research papers',
                    tag: 'NIH PubMed',
                  },
                  {
                    id: 'openalex' as const,
                    title: 'OpenAlex Global Catalog',
                    subtitle: 'Comprehensive cross-disciplinary index',
                    tag: 'OpenAlex',
                  },
                ].map((sourceOption) => {
                  const isSelected = filters.source === sourceOption.id
                  return (
                    <button
                      key={sourceOption.id}
                      type="button"
                      onClick={() => setFilters({ ...filters, source: sourceOption.id })}
                      className={`w-full text-left p-3 rounded-2xl border transition-all flex items-start justify-between gap-3 ${
                        isSelected
                          ? 'bg-indigo-50/80 dark:bg-indigo-950/40 border-indigo-400/80 dark:border-indigo-600/80 shadow-sm'
                          : 'bg-slate-50/60 dark:bg-slate-800/40 border-slate-200/80 dark:border-slate-800 hover:bg-slate-100/70 dark:hover:bg-slate-800/70'
                      }`}
                    >
                      <div className="flex items-start gap-2.5">
                        <div className="mt-0.5">
                          <span
                            className={`flex h-4 w-4 rounded-full border items-center justify-center ${
                              isSelected
                                ? 'border-indigo-600 bg-indigo-600'
                                : 'border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900'
                            }`}
                          >
                            {isSelected && <span className="h-1.5 w-1.5 rounded-full bg-white" />}
                          </span>
                        </div>
                        <div>
                          <span
                            className={`text-xs font-bold block ${
                              isSelected
                                ? 'text-indigo-900 dark:text-indigo-100'
                                : 'text-slate-800 dark:text-slate-200'
                            }`}
                          >
                            {sourceOption.title}
                          </span>
                          <span className="text-[11px] text-slate-500 dark:text-slate-400 block leading-tight mt-0.5">
                            {sourceOption.subtitle}
                          </span>
                        </div>
                      </div>
                      <span
                        className={`text-[10px] font-mono px-2 py-0.5 rounded-full shrink-0 ${
                          isSelected
                            ? 'bg-indigo-200/60 dark:bg-indigo-900/60 text-indigo-800 dark:text-indigo-200 font-semibold'
                            : 'bg-slate-200/60 dark:bg-slate-800 text-slate-500 dark:text-slate-400'
                        }`}
                      >
                        {sourceOption.tag}
                      </span>
                    </button>
                  )
                })}
              </div>
            </div>

            {/* ─── D. Publication Year Range Slider ─── */}
            <div className="pt-2 border-t border-slate-100 dark:border-slate-800">
              <YearRangeSlider
                startDate={filters.startDate}
                endDate={filters.endDate}
                onChange={({ startDate, endDate }) =>
                  setFilters({ ...filters, startDate, endDate })
                }
              />
            </div>

            {/* ─── E. Maximum Results Filter ─── */}
            <div className="pt-2 border-t border-slate-100 dark:border-slate-800 space-y-2">
              <div className="flex items-center justify-between">
                <label className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                  Maximum Results
                </label>
                <span className="text-xs font-mono text-slate-400">
                  {filters.maxResults ?? 100} papers
                </span>
              </div>
              <input
                type="number"
                min="1"
                placeholder="100"
                value={filters.maxResults ?? ''}
                onChange={(e) => {
                  const v = parseInt(e.target.value)
                  setFilters({ ...filters, maxResults: isNaN(v) || v < 1 ? undefined : v })
                }}
                className="w-full h-10 px-3 rounded-xl border border-slate-200 dark:border-slate-700
                           bg-slate-50/80 dark:bg-slate-800/60 text-sm text-slate-900 dark:text-slate-100
                           focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
              <div className="flex items-center gap-1.5 pt-1">
                {[50, 100, 200, 500].map((n) => (
                  <button
                    key={n}
                    type="button"
                    onClick={() => setFilters({ ...filters, maxResults: n })}
                    className={`flex-1 py-1 rounded-lg text-xs font-medium border transition-colors ${
                      (filters.maxResults ?? 100) === n
                        ? 'bg-indigo-50 dark:bg-indigo-950/60 border-indigo-300 dark:border-indigo-700 text-indigo-700 dark:text-indigo-300 font-semibold'
                        : 'bg-slate-50 dark:bg-slate-800/40 border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                    }`}
                  >
                    {n}
                  </button>
                ))}
              </div>
            </div>

            {/* ─── Reset Button ─── */}
            <div className="pt-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleResetFilters}
                className="w-full rounded-xl text-xs font-semibold"
              >
                Reset All Filters
              </Button>
            </div>
          </div>
        </aside>

        {/* ─── RIGHT RAIL: Results Stream (8 Cols on xl) ───────────────────── */}
        <main className="xl:col-span-8 space-y-6">

          {/* ── Error Display ── */}
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                className="w-full"
              >
                <div className="flex items-start justify-between gap-3 p-5 rounded-3xl bg-rose-50/90 dark:bg-rose-950/40 backdrop-blur-xl border border-rose-200/80 dark:border-rose-800/80 shadow-md shadow-rose-500/5">
                  <div className="flex items-start gap-3">
                    <div className="w-9 h-9 rounded-2xl bg-rose-100 dark:bg-rose-900/60 text-rose-600 dark:text-rose-400 flex items-center justify-center shrink-0 shadow-xs">
                      <ExclamationCircleIcon className="w-5 h-5" />
                    </div>
                    <div className="space-y-1">
                      <h4 className="text-sm font-bold text-rose-900 dark:text-rose-100">
                        Search Error Occurred
                      </h4>
                      <p className="text-xs sm:text-sm font-medium text-rose-700 dark:text-rose-300 leading-relaxed">
                        {error}
                      </p>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => setError('')}
                    className="p-1.5 rounded-xl text-rose-400 hover:text-rose-700 dark:hover:text-rose-200 hover:bg-rose-100/60 dark:hover:bg-rose-900/40 transition-colors shrink-0"
                    title="Dismiss error"
                  >
                    <XCircleIcon className="w-5 h-5" />
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* ── Progress / Loading State ── */}
          {isLoading && searchProgress && (
            <SearchProgressPanel progress={searchProgress} onCancel={handleCancel} />
          )}
          {isLoading && !searchProgress && (
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              className="py-16 flex flex-col justify-center items-center w-full rounded-3xl bg-white/85 dark:bg-slate-900/85 backdrop-blur-xl border border-slate-200/80 dark:border-slate-800 shadow-md space-y-4"
            >
              <ResearchRoverLoader message="Initiating federated literature search..." size="lg" />
              <p className="text-xs text-slate-400 dark:text-slate-500 font-mono">
                Connecting to PubMed Central and OpenAlex APIs…
              </p>
            </motion.div>
          )}

          {/* ── Results Stream ── */}
          {displayedResults.length > 0 && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-5">

              {/* Stream Header & Controls */}
              <div className="p-5 sm:p-6 rounded-3xl bg-white/85 dark:bg-slate-900/85 backdrop-blur-xl border border-slate-200/80 dark:border-slate-800 shadow-md space-y-4">
                <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                  {/* Left: Result Count & Search Context */}
                  <div className="flex items-start sm:items-center gap-3">
                    <div className="w-10 h-10 rounded-2xl bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200/60 dark:border-indigo-800/60 text-indigo-600 dark:text-indigo-400 flex items-center justify-center shrink-0 shadow-xs">
                      <CheckCircleIcon className="w-5 h-5" />
                    </div>
                    <div>
                      <div className="flex flex-wrap items-center gap-2.5">
                        <h2 className="text-lg font-extrabold tracking-tight text-slate-900 dark:text-slate-100">
                          {totalResults.toLocaleString()} Publications Found
                        </h2>
                        {totalResults > 0 && (
                          <span className="text-xs font-mono font-semibold px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200/60 dark:border-slate-700/60">
                            Page {currentPage} of {totalPages}
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                        {(filters.sortMode || 'relevance') === 'relevance'
                          ? 'Ranked by MedCPT cross-encoder semantic relevance'
                          : 'Ranked in chronological publication order'}
                      </p>
                    </div>
                  </div>

                  {/* Right: Sort Mode Controls */}
                  <div className="flex items-center gap-2 self-start lg:self-auto">
                    <span className="text-xs font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider hidden sm:inline">
                      Sort:
                    </span>
                    <div className="inline-flex rounded-2xl border border-slate-200/80 dark:border-slate-700 p-1 bg-slate-100/80 dark:bg-slate-800/80 shadow-inner">
                      <button
                        type="button"
                        onClick={() => setFilters({ ...filters, sortMode: 'relevance' })}
                        disabled={isLoading}
                        className={`inline-flex items-center gap-1.5 h-8 px-3.5 rounded-xl text-xs font-bold transition-all ${
                          (filters.sortMode || 'relevance') === 'relevance'
                            ? 'bg-white dark:bg-slate-900 text-indigo-600 dark:text-indigo-400 shadow-sm'
                            : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100'
                        }`}
                      >
                        <SparklesIcon className="w-3.5 h-3.5" />
                        <span>Relevance</span>
                      </button>
                      <button
                        type="button"
                        onClick={() => setFilters({ ...filters, sortMode: 'recency' })}
                        disabled={isLoading}
                        className={`inline-flex items-center gap-1.5 h-8 px-3.5 rounded-xl text-xs font-bold transition-all ${
                          (filters.sortMode || 'relevance') === 'recency'
                            ? 'bg-white dark:bg-slate-900 text-indigo-600 dark:text-indigo-400 shadow-sm'
                            : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100'
                        }`}
                      >
                        <ClockIcon className="w-3.5 h-3.5" />
                        <span>Recent</span>
                      </button>
                    </div>
                  </div>
                </div>

                {/* Bottom Row: Active Context & Batch Action Toolbar */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-3 border-t border-slate-100 dark:border-slate-800">
                  {/* Context Pill */}
                  <div className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400 truncate">
                    {query && (
                      <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-xl bg-slate-100 dark:bg-slate-800/80 border border-slate-200/60 dark:border-slate-700/60 font-medium text-slate-700 dark:text-slate-300 max-w-sm truncate">
                        <MagnifyingGlassIcon className="w-3.5 h-3.5 text-indigo-500 shrink-0" />
                        <span className="truncate">"{query}"</span>
                      </span>
                    )}
                  </div>

                  {/* Batch Action Buttons */}
                  <div className="flex flex-wrap items-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handleDownload}
                      disabled={!csvFilename}
                      className="h-9 px-3.5 rounded-xl text-xs font-semibold border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 disabled:opacity-50 transition-all flex items-center gap-1.5"
                      title={csvFilename ? 'Export retrieved metadata as CSV' : 'No retrieved corpus ready to export'}
                    >
                      <DocumentArrowDownIcon className="w-4 h-4 text-slate-600 dark:text-slate-300" />
                      <span>Export CSV</span>
                    </Button>
                    <Button
                      size="sm"
                      onClick={handleCreateEmbeddings}
                      disabled={!csvFilename}
                      className="h-9 px-3.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold shadow-sm shadow-indigo-500/20 disabled:opacity-50 transition-all flex items-center gap-1.5"
                      title={csvFilename ? 'Generate semantic vector embeddings for AI Chat' : 'Run a search to generate corpus embeddings'}
                    >
                      <CpuChipIcon className="w-4 h-4" />
                      <span>Embeddings</span>
                    </Button>
                    <Button
                      size="sm"
                      onClick={() => navigate('/analytics', { state: { filename: csvFilename, query } })}
                      disabled={!csvFilename}
                      className="h-9 px-3.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold shadow-sm shadow-emerald-500/20 disabled:opacity-50 transition-all flex items-center gap-1.5"
                      title={csvFilename ? 'Open corpus in bibliometric analytics workspace' : 'Run a search to explore corpus analytics'}
                    >
                      <ChartBarIcon className="w-4 h-4" />
                      <span>Analytics</span>
                    </Button>
                  </div>
                </div>
              </div>

              {/* Cards List */}
              <div className="space-y-4">
                {displayedResults.map((paper, i) => (
                  <PaperCard
                    key={i}
                    paper={paper}
                    index={(currentPage - 1) * perPage + i}
                  />
                ))}
              </div>

              {/* Pagination Footer */}
              <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 sm:p-5 rounded-3xl bg-white/85 dark:bg-slate-900/85 backdrop-blur-xl border border-slate-200/80 dark:border-slate-800 shadow-sm mt-6">
                {/* Left: Per page & summary */}
                <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500 dark:text-slate-400">
                  <div className="flex items-center gap-2">
                    <span className="font-medium">Per page:</span>
                    <select
                      value={perPage}
                      onChange={(e) => {
                        setPerPage(parseInt(e.target.value))
                        setCurrentPage(1)
                      }}
                      disabled={isLoading}
                      className="h-8 px-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-semibold cursor-pointer focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    >
                      {[5, 10, 20, 50, 100, 200, 500, 1000].map((n) => (
                        <option key={n} value={n}>
                          {n}
                        </option>
                      ))}
                    </select>
                  </div>
                  <span className="hidden sm:inline text-slate-300 dark:text-slate-700">•</span>
                  <span className="font-mono text-[11px]">
                    Showing {((currentPage - 1) * perPage) + 1}–{Math.min(currentPage * perPage, totalResults)} of {totalResults.toLocaleString()} papers
                  </span>
                </div>

                {/* Right: Numeric Sliding Page Controls */}
                {totalPages > 1 && (
                  <div className="flex items-center gap-1.5">
                    {/* Previous Button */}
                    <button
                      type="button"
                      onClick={() => handlePageChange(currentPage - 1)}
                      disabled={currentPage <= 1 || isLoading}
                      aria-label="Previous page"
                      className="h-8 w-8 rounded-xl flex items-center justify-center border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
                    >
                      <ChevronLeftIcon className="w-4 h-4" />
                    </button>

                    {/* Sliding Numeric Page Window (max 7) */}
                    {Array.from({ length: Math.min(totalPages, 7) }, (_, i) => {
                      let p: number
                      if (totalPages <= 7) p = i + 1
                      else if (currentPage <= 4) p = i + 1
                      else if (currentPage >= totalPages - 3) p = totalPages - 6 + i
                      else p = currentPage - 3 + i
                      return (
                        <button
                          key={p}
                          type="button"
                          onClick={() => handlePageChange(p)}
                          disabled={isLoading}
                          aria-label={`Page ${p}`}
                          aria-current={currentPage === p ? 'page' : undefined}
                          className={`h-8 min-w-8 px-2 rounded-xl text-xs font-bold transition-all ${
                            currentPage === p
                              ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/25'
                              : 'border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
                          }`}
                        >
                          {p}
                        </button>
                      )
                    })}

                    {/* Next Button */}
                    <button
                      type="button"
                      onClick={() => handlePageChange(currentPage + 1)}
                      disabled={currentPage >= totalPages || isLoading}
                      aria-label="Next page"
                      className="h-8 w-8 rounded-xl flex items-center justify-center border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
                    >
                      <ChevronRightIcon className="w-4 h-4" />
                    </button>
                  </div>
                )}
              </div>
            </motion.div>
          )}

          {/* ── Empty State: No Results Found ── */}
          {!isLoading && displayedResults.length === 0 && allResults.length === 0 && query && !error && (
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              className="rounded-3xl border border-slate-200/80 dark:border-slate-800 bg-white/90 dark:bg-slate-900/90 backdrop-blur-xl p-8 sm:p-12 text-center shadow-sm space-y-6"
            >
              <div className="w-16 h-16 rounded-3xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-center justify-center mx-auto text-slate-400">
                <MagnifyingGlassIcon className="w-8 h-8" />
              </div>
              <div className="space-y-2 max-w-md mx-auto">
                <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                  No publications found for "{query}"
                </h3>
                <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
                  We couldn't find any papers matching your specific query or filter constraints in PubMed Central or OpenAlex.
                </p>
              </div>

              {/* Suggestions Box */}
              <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200/60 dark:border-slate-700/60 max-w-lg mx-auto text-left space-y-2 text-xs text-slate-600 dark:text-slate-300">
                <p className="font-semibold text-slate-700 dark:text-slate-200">Recommended adjustments:</p>
                <ul className="list-disc list-inside space-y-1 text-slate-500 dark:text-slate-400">
                  <li>Broaden your query keywords or check for typos.</li>
                  <li>Expand or reset the publication year range in the Precision Filters rail.</li>
                  <li>Switch the Repository Source to <strong>Unified Search</strong> to query both PubMed and OpenAlex.</li>
                </ul>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
                <Button
                  variant="outline"
                  onClick={handleResetFilters}
                  className="rounded-xl text-xs font-semibold"
                >
                  <ArrowPathIcon className="w-3.5 h-3.5 mr-1.5" />
                  Reset All Filters
                </Button>
                <Button
                  onClick={() => {
                    setQuery('')
                    searchInputRef.current?.focus()
                  }}
                  className="rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-700 text-white"
                >
                  Clear Search Query
                </Button>
              </div>
            </motion.div>
          )}

          {/* ── Initial Exploration Landing State ── */}
          {!isLoading && !query && displayedResults.length === 0 && (
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.15 }}
              className="space-y-8 py-4"
            >
              {/* Hero Banner */}
              <div className="relative overflow-hidden rounded-3xl border border-slate-200/80 dark:border-slate-800 bg-white/90 dark:bg-slate-900/90 backdrop-blur-xl p-8 sm:p-10 text-center shadow-sm">
                <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/[0.04] via-teal-500/[0.04] to-transparent pointer-events-none" />
                <div className="relative max-w-2xl mx-auto space-y-4">
                  <div className="w-14 h-14 rounded-3xl bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200/60 dark:border-indigo-800/60 text-indigo-600 dark:text-indigo-400 flex items-center justify-center mx-auto shadow-xs">
                    <SparklesIcon className="w-7 h-7" />
                  </div>
                  <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-900 dark:text-slate-100">
                    Explore Global Scholarly Literature
                  </h2>
                  <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 leading-relaxed">
                    Query hundreds of millions of peer-reviewed articles, clinical trials, and preprints from NIH PubMed Central and OpenAlex with MedCPT semantic ranking.
                  </p>
                </div>
              </div>

              {/* Curated Research Prompt Suggestions */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                    <TagIcon className="w-4 h-4 text-indigo-500" />
                    <span>Suggested Research Inquiries</span>
                  </div>
                  <span className="text-xs text-slate-400">Click any query to search instantly</span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {[
                    {
                      topic: 'CRISPR-Cas9 gene editing in sickle cell disease',
                      category: 'Genomics & Gene Therapy',
                      badge: 'Clinical',
                    },
                    {
                      topic: 'mRNA vaccine immunogenicity and long-term efficacy',
                      category: 'Immunology & Infectious Disease',
                      badge: 'Biomedical',
                    },
                    {
                      topic: 'CAR-T cell therapy solid tumors clinical trials',
                      category: 'Oncology & Immunotherapy',
                      badge: 'Oncology',
                    },
                    {
                      topic: 'Deep learning for early Alzheimer disease detection',
                      category: 'Neuroscience & AI Medicine',
                      badge: 'Neuro / AI',
                    },
                  ].map((item) => (
                    <button
                      key={item.topic}
                      type="button"
                      onClick={() => handleExampleClick(item.topic)}
                      className="group p-4 rounded-2xl border border-slate-200/80 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 hover:border-indigo-400/80 dark:hover:border-indigo-600/80 hover:bg-indigo-50/40 dark:hover:bg-indigo-950/20 hover:shadow-md transition-all text-left flex items-start justify-between gap-3"
                    >
                      <div className="space-y-1">
                        <span className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 block">
                          {item.category}
                        </span>
                        <p className="text-sm font-semibold text-slate-800 dark:text-slate-200 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                          "{item.topic}"
                        </p>
                      </div>
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 shrink-0">
                        {item.badge}
                      </span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Three-Column Platform Capabilities */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
                {[
                  {
                    icon: SparklesIcon,
                    title: 'Semantic MedCPT Ranking',
                    desc: 'Cross-encoder scoring re-ranks retrieved literature by relevance to your research hypothesis.',
                  },
                  {
                    icon: DocumentArrowDownIcon,
                    title: 'Structured CSV Export',
                    desc: 'Download all retrieved publication metadata, PMIDs, DOIs, and abstracts in one click.',
                  },
                  {
                    icon: CpuChipIcon,
                    title: 'Grounded AI Assistant',
                    desc: 'Convert retrieved corpora into vector embeddings to ask synthesis questions in AI Chat.',
                  },
                ].map(({ icon: Icon, title, desc }) => (
                  <div
                    key={title}
                    className="p-5 rounded-3xl bg-white/60 dark:bg-slate-900/60 border border-slate-200/60 dark:border-slate-800 space-y-2.5 shadow-xs"
                  >
                    <div className="w-10 h-10 rounded-2xl bg-indigo-50 dark:bg-indigo-950/50 border border-indigo-200/60 dark:border-indigo-800/60 text-indigo-600 dark:text-indigo-400 flex items-center justify-center">
                      <Icon className="w-5 h-5" />
                    </div>
                    <p className="text-sm font-bold text-slate-800 dark:text-slate-200">{title}</p>
                    <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">{desc}</p>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </main>
      </div>

      {/* App-wide shared embedding modal */}
      <EmbeddingProgressModal />
    </div>
  )
}
