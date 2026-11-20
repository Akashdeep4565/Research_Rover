import { useState, useEffect } from 'react'
import {
  ShieldCheckIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ChevronRightIcon,
  SparklesIcon,
} from '@heroicons/react/24/outline'
import type { DatasetQualityReport } from '@/types'
import { filesApi } from '@/services/api'

interface DatasetFeatureReadinessBannerProps {
  filename?: string | null
  onOpenModal: () => void
  className?: string
}

export function DatasetFeatureReadinessBanner({
  filename,
  onOpenModal,
  className = '',
}: DatasetFeatureReadinessBannerProps) {
  const [report, setReport] = useState<DatasetQualityReport | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!filename) {
      setReport(null)
      return
    }

    let cancelled = false
    setLoading(true)

    filesApi
      .getQuality(filename)
      .then((data) => {
        if (!cancelled) setReport(data)
      })
      .catch(() => {
        if (!cancelled) setReport(null)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [filename])

  if (!filename || loading || !report) return null

  const readyCount = Object.values(report.feature_readiness || {}).filter(
    (f) => f.status === 'ready'
  ).length
  const partialCount = Object.values(report.feature_readiness || {}).filter(
    (f) => f.status === 'partially_ready'
  ).length

  const gradeColor =
    report.quality_grade === 'Excellent' || report.quality_grade === 'Good'
      ? 'text-emerald-600 dark:text-emerald-400'
      : report.quality_grade === 'Fair'
      ? 'text-amber-600 dark:text-amber-400'
      : 'text-rose-600 dark:text-rose-400'

  return (
    <div
      onClick={onOpenModal}
      className={`group cursor-pointer flex flex-wrap items-center justify-between gap-3 px-4 py-2.5 rounded-xl border border-sky-100 dark:border-slate-800/80 bg-gradient-to-r from-sky-50/60 via-indigo-50/40 to-white dark:from-slate-900/80 dark:via-slate-900/60 dark:to-slate-900/40 shadow-sm hover:border-sky-300 dark:hover:border-sky-500/50 transition ${className}`}
      title="Click to view full dataset quality report, column mappings & feature readiness"
    >
      <div className="flex flex-wrap items-center gap-2.5 text-xs text-gray-700 dark:text-slate-300">
        <span className="flex items-center gap-1 font-semibold text-gray-900 dark:text-slate-100">
          <ShieldCheckIcon className="h-4 w-4 text-sky-500" />
          Quality:
          <span className={`font-bold ml-1 ${gradeColor}`}>
            {report.quality_grade} ({report.overall_quality_score.toFixed(0)})
          </span>
        </span>

        <span className="text-gray-300 dark:text-slate-700 hidden sm:inline">|</span>

        <span className="flex items-center gap-1 text-emerald-700 dark:text-emerald-400 font-medium">
          <CheckCircleIcon className="h-3.5 w-3.5" />
          {readyCount} Ready
        </span>

        {partialCount > 0 && (
          <span className="flex items-center gap-1 text-amber-700 dark:text-amber-400 font-medium">
            <ExclamationTriangleIcon className="h-3.5 w-3.5" />
            {partialCount} Partial
          </span>
        )}

        <span className="text-gray-400 dark:text-slate-500 text-[11px] hidden md:inline">
          ({report.valid_records.toLocaleString()} unique records
          {report.duplicate_records > 0 ? `, ${report.duplicate_records} duplicates safely excluded` : ''})
        </span>
      </div>

      <div className="flex items-center gap-1 text-xs font-semibold text-sky-600 dark:text-sky-400 group-hover:translate-x-0.5 transition-transform">
        <SparklesIcon className="h-3.5 w-3.5" />
        <span>Schema & Readiness Details</span>
        <ChevronRightIcon className="h-3.5 w-3.5" />
      </div>
    </div>
  )
}
