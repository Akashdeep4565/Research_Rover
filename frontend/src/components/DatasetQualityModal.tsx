import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  XMarkIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon,
  InformationCircleIcon,
  DocumentTextIcon,
  TableCellsIcon,
  SparklesIcon,
  ShieldCheckIcon,
  ArrowPathIcon,
  CpuChipIcon,
} from '@heroicons/react/24/outline'
import type {
  DatasetQualityReport,
  ExtendedFileUploadResponse,
  FeatureReadiness,
  ColumnMapping,
} from '@/types'
import { filesApi } from '@/services/api'
import { Badge } from '@/components/ui/badge'

interface DatasetQualityModalProps {
  isOpen: boolean
  onClose: () => void
  filename?: string | null
  initialData?: ExtendedFileUploadResponse | DatasetQualityReport | null
}

const GRADE_STYLES: Record<string, { bg: string; text: string; border: string }> = {
  Excellent: {
    bg: 'bg-emerald-50 dark:bg-emerald-950/40',
    text: 'text-emerald-700 dark:text-emerald-400',
    border: 'border-emerald-200 dark:border-emerald-800/60',
  },
  Good: {
    bg: 'bg-sky-50 dark:bg-sky-950/40',
    text: 'text-sky-700 dark:text-sky-400',
    border: 'border-sky-200 dark:border-sky-800/60',
  },
  Fair: {
    bg: 'bg-amber-50 dark:bg-amber-950/40',
    text: 'text-amber-700 dark:text-amber-400',
    border: 'border-amber-200 dark:border-amber-800/60',
  },
  Poor: {
    bg: 'bg-orange-50 dark:bg-orange-950/40',
    text: 'text-orange-700 dark:text-orange-400',
    border: 'border-orange-200 dark:border-orange-800/60',
  },
  Critical: {
    bg: 'bg-rose-50 dark:bg-rose-950/40',
    text: 'text-rose-700 dark:text-rose-400',
    border: 'border-rose-200 dark:border-rose-800/60',
  },
}

const STATUS_ICONS: Record<string, any> = {
  ready: CheckCircleIcon,
  partially_ready: ExclamationTriangleIcon,
  not_ready: XCircleIcon,
}

const STATUS_LABELS: Record<string, string> = {
  ready: 'Ready',
  partially_ready: 'Partially Ready',
  not_ready: 'Not Ready',
}

const STATUS_COLORS: Record<string, { badge: string; text: string; bg: string }> = {
  ready: {
    badge: 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border-emerald-300 dark:border-emerald-800',
    text: 'text-emerald-600 dark:text-emerald-400',
    bg: 'bg-emerald-500',
  },
  partially_ready: {
    badge: 'bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 border-amber-300 dark:border-amber-800',
    text: 'text-amber-600 dark:text-amber-400',
    bg: 'bg-amber-500',
  },
  not_ready: {
    badge: 'bg-rose-100 dark:bg-rose-950/60 text-rose-800 dark:text-rose-300 border-rose-300 dark:border-rose-800',
    text: 'text-rose-600 dark:text-rose-400',
    bg: 'bg-rose-500',
  },
}

export function DatasetQualityModal({
  isOpen,
  onClose,
  filename,
  initialData,
}: DatasetQualityModalProps) {
  const [activeTab, setActiveTab] = useState<'overview' | 'mappings' | 'readiness'>('overview')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [report, setReport] = useState<DatasetQualityReport | null>(null)
  const [uploadMeta, setUploadMeta] = useState<ExtendedFileUploadResponse | null>(null)

  useEffect(() => {
    if (!isOpen) return

    // If initialData is provided as ExtendedFileUploadResponse
    if (initialData && 'canonical_fields_detected' in initialData) {
      const uploadResp = initialData as ExtendedFileUploadResponse
      setUploadMeta(uploadResp)
      setReport({
        overall_quality_score: uploadResp.overall_quality_score,
        quality_grade: uploadResp.quality_grade,
        total_records: uploadResp.total_records,
        valid_records: uploadResp.valid_records,
        duplicate_records: uploadResp.duplicate_records,
        field_statistics: {},
        unmapped_columns: uploadResp.unmapped_columns,
        feature_readiness: uploadResp.feature_readiness,
        recommendations: uploadResp.recommendations,
        normalization_report: {
          total_columns: Object.keys(uploadResp.column_mappings || {}).length + uploadResp.unmapped_columns.length,
          mapped_columns: Object.keys(uploadResp.column_mappings || {}).length,
          unmapped_columns: uploadResp.unmapped_columns.length,
          uncertain_columns: Object.values(uploadResp.column_mappings || {}).filter(m => m.status === 'uncertain').length,
          conflicts: uploadResp.conflicting_mappings || [],
          mappings: uploadResp.column_mappings || {},
          total_records: uploadResp.total_records,
          valid_records: uploadResp.valid_records,
          duplicate_records: uploadResp.duplicate_records,
        },
      })
      // Also fetch the full quality report if filename is available so field_statistics are populated
      if (uploadResp.filename) {
        filesApi
          .getQuality(uploadResp.filename)
          .then((fullRep) => {
            setReport((prev) => ({
              ...fullRep,
              normalization_report: fullRep.normalization_report || prev?.normalization_report,
            }))
          })
          .catch(() => {
            // Non-critical: keep upload metadata
          })
      }
      return
    }

    // If initialData is already a DatasetQualityReport
    if (initialData && 'field_statistics' in initialData) {
      setReport(initialData as DatasetQualityReport)
      setUploadMeta(null)
      return
    }

    // If filename is passed, fetch from backend API
    if (filename) {
      setLoading(true)
      setError(null)
      filesApi
        .getQuality(filename)
        .then((data) => {
          setReport(data)
          setUploadMeta(null)
        })
        .catch((err) => {
          setError(err?.detail || err?.error || err?.message || 'Failed to load dataset quality report')
        })
        .finally(() => {
          setLoading(false)
        })
    }
  }, [isOpen, filename, initialData])

  if (!isOpen) return null

  const displayFilename = uploadMeta?.filename || filename || 'Dataset'
  const qualityScore = report?.overall_quality_score ?? uploadMeta?.overall_quality_score ?? 0
  const qualityGrade = report?.quality_grade ?? uploadMeta?.quality_grade ?? 'Critical'
  const totalRecords = report?.total_records ?? uploadMeta?.total_records ?? 0
  const validRecords = report?.valid_records ?? uploadMeta?.valid_records ?? 0
  const duplicateRecords = report?.duplicate_records ?? uploadMeta?.duplicate_records ?? 0
  const unmappedCols = report?.unmapped_columns ?? uploadMeta?.unmapped_columns ?? []
  const featureReadiness = report?.feature_readiness ?? uploadMeta?.feature_readiness ?? {}
  const recommendations = report?.recommendations ?? uploadMeta?.recommendations ?? []
  const normReport = report?.normalization_report
  const mappings = normReport?.mappings ?? uploadMeta?.column_mappings ?? {}
  const conflicts = normReport?.conflicts ?? uploadMeta?.conflicting_mappings ?? []
  const fieldStats = report?.field_statistics || {}

  const gradeStyle = GRADE_STYLES[qualityGrade] || GRADE_STYLES.Critical

  // Check index status for semantic search / RAG
  const hasIndexWarning =
    uploadMeta?.index_status === 'not_indexed' ||
    featureReadiness?.semantic_search?.warnings?.some(w => w.toLowerCase().includes('faiss') || w.toLowerCase().includes('index')) ||
    featureReadiness?.ai_chat_rag?.warnings?.some(w => w.toLowerCase().includes('faiss') || w.toLowerCase().includes('index')) ||
    featureReadiness?.rag_chat?.warnings?.some(w => w.toLowerCase().includes('faiss') || w.toLowerCase().includes('index'))

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 overflow-y-auto bg-slate-900/60 dark:bg-slate-950/80 backdrop-blur-sm">
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 12 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 12 }}
          transition={{ duration: 0.2 }}
          className="relative w-full max-w-4xl max-h-[90vh] flex flex-col rounded-2xl border border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-2xl overflow-hidden"
        >
          {/* Header */}
          <div className="flex items-center justify-between border-b border-gray-200 dark:border-slate-800 px-6 py-4 bg-gray-50/70 dark:bg-slate-900/80">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-sky-500/10 text-sky-600 dark:text-sky-400">
                <ShieldCheckIcon className="h-6 w-6" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-900 dark:text-slate-100 flex items-center gap-2">
                  Dataset Ingestion & Quality Analysis
                </h3>
                <p className="text-xs text-gray-500 dark:text-slate-400 font-mono truncate max-w-md">
                  {displayFilename} {uploadMeta?.encoding ? `(${uploadMeta.encoding})` : ''}
                </p>
              </div>
            </div>

            <button
              onClick={onClose}
              className="rounded-lg p-1.5 text-gray-400 hover:text-gray-700 dark:text-slate-400 dark:hover:text-slate-200 hover:bg-gray-100 dark:hover:bg-slate-800 transition"
              aria-label="Close dialog"
            >
              <XMarkIcon className="h-5 w-5" />
            </button>
          </div>

          {/* Top Metric Strip */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 px-6 py-4 bg-white dark:bg-slate-900 border-b border-gray-100 dark:border-slate-800/80">
            {/* Score & Grade */}
            <div className={`p-3 rounded-xl border ${gradeStyle.border} ${gradeStyle.bg} flex flex-col justify-between`}>
              <span className="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-slate-400">Quality Score</span>
              <div className="flex items-baseline gap-2 mt-1">
                <span className={`text-2xl font-black ${gradeStyle.text}`}>{qualityScore.toFixed(1)}</span>
                <span className="text-xs text-gray-500 dark:text-slate-400">/ 100</span>
              </div>
              <span className={`text-xs font-bold mt-1 ${gradeStyle.text}`}>Grade: {qualityGrade}</span>
            </div>

            {/* Total Records */}
            <div className="p-3 rounded-xl border border-gray-200 dark:border-slate-800 bg-gray-50/50 dark:bg-slate-800/40 flex flex-col justify-between">
              <span className="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-slate-400">Total Records</span>
              <span className="text-2xl font-black text-gray-900 dark:text-slate-100 mt-1">{totalRecords.toLocaleString()}</span>
              <span className="text-xs text-gray-500 dark:text-slate-400">In CSV dataset</span>
            </div>

            {/* Unique Valid Records */}
            <div className="p-3 rounded-xl border border-gray-200 dark:border-slate-800 bg-gray-50/50 dark:bg-slate-800/40 flex flex-col justify-between">
              <span className="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-slate-400">Unique Valid</span>
              <span className="text-2xl font-black text-emerald-600 dark:text-emerald-400 mt-1">{validRecords.toLocaleString()}</span>
              <span className="text-xs text-emerald-600/80 dark:text-emerald-400/80">
                {totalRecords > 0 ? `${((validRecords / totalRecords) * 100).toFixed(0)}% retention` : 'No records'}
              </span>
            </div>

            {/* Duplicates */}
            <div className="p-3 rounded-xl border border-gray-200 dark:border-slate-800 bg-gray-50/50 dark:bg-slate-800/40 flex flex-col justify-between">
              <span className="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-slate-400">Duplicates</span>
              <span className={`text-2xl font-black mt-1 ${duplicateRecords > 0 ? 'text-amber-600 dark:text-amber-400' : 'text-gray-900 dark:text-slate-100'}`}>
                {duplicateRecords.toLocaleString()}
              </span>
              <span className="text-xs text-gray-500 dark:text-slate-400">
                {duplicateRecords > 0 ? 'Safe deduplication' : 'No duplicates'}
              </span>
            </div>
          </div>

          {/* Navigation Tabs */}
          <div className="flex border-b border-gray-200 dark:border-slate-800 px-6 bg-gray-50/30 dark:bg-slate-900/50">
            <button
              onClick={() => setActiveTab('overview')}
              className={`py-3 px-4 text-sm font-semibold border-b-2 flex items-center gap-2 transition ${
                activeTab === 'overview'
                  ? 'border-sky-500 text-sky-600 dark:text-sky-400'
                  : 'border-transparent text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-200'
              }`}
            >
              <DocumentTextIcon className="h-4 w-4" />
              Quality & Hygiene
            </button>
            <button
              onClick={() => setActiveTab('mappings')}
              className={`py-3 px-4 text-sm font-semibold border-b-2 flex items-center gap-2 transition ${
                activeTab === 'mappings'
                  ? 'border-sky-500 text-sky-600 dark:text-sky-400'
                  : 'border-transparent text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-200'
              }`}
            >
              <TableCellsIcon className="h-4 w-4" />
              Column Mappings
              {conflicts.length > 0 && (
                <span className="ml-1 px-1.5 py-0.5 rounded-full text-[10px] font-bold bg-rose-500 text-white">
                  {conflicts.length}
                </span>
              )}
            </button>
            <button
              onClick={() => setActiveTab('readiness')}
              className={`py-3 px-4 text-sm font-semibold border-b-2 flex items-center gap-2 transition ${
                activeTab === 'readiness'
                  ? 'border-sky-500 text-sky-600 dark:text-sky-400'
                  : 'border-transparent text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-200'
              }`}
            >
              <SparklesIcon className="h-4 w-4" />
              Feature Readiness
              {hasIndexWarning && (
                <span className="ml-1 px-1.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-500 text-white">
                  Notice
                </span>
              )}
            </button>
          </div>

          {/* Body Content */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {loading && (
              <div className="flex flex-col items-center justify-center py-16 text-gray-500 dark:text-slate-400">
                <ArrowPathIcon className="h-8 w-8 animate-spin text-sky-500 mb-3" />
                <p className="text-sm font-medium">Evaluating dataset quality & feature readiness…</p>
              </div>
            )}

            {error && (
              <div className="p-4 rounded-xl border border-rose-200 dark:border-rose-900/60 bg-rose-50 dark:bg-rose-950/40 text-rose-800 dark:text-rose-300 text-sm flex items-start gap-3">
                <XCircleIcon className="h-5 w-5 shrink-0 text-rose-500 mt-0.5" />
                <div>
                  <h4 className="font-semibold">Unable to load quality report</h4>
                  <p className="mt-1 text-xs opacity-90">{error}</p>
                </div>
              </div>
            )}

            {!loading && !error && (
              <>
                {/* ── TAB 1: OVERVIEW & HYGIENE ── */}
                {activeTab === 'overview' && (
                  <div className="space-y-6">
                    {/* Recommendations & Actionable Steps */}
                    {recommendations.length > 0 && (
                      <div className="p-4 rounded-xl border border-sky-200 dark:border-sky-900/60 bg-sky-50/50 dark:bg-sky-950/30">
                        <h4 className="text-sm font-bold text-sky-900 dark:text-sky-300 flex items-center gap-2 mb-2">
                          <InformationCircleIcon className="h-4 w-4 text-sky-600 dark:text-sky-400" />
                          Ingestion Recommendations
                        </h4>
                        <ul className="space-y-1.5">
                          {recommendations.map((rec, idx) => (
                            <li key={idx} className="text-xs text-sky-800 dark:text-sky-300/90 flex items-start gap-2">
                              <span className="font-bold text-sky-600 dark:text-sky-400">•</span>
                              <span>{rec}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Field Completeness Statistics */}
                    <div>
                      <h4 className="text-sm font-bold text-gray-900 dark:text-slate-100 mb-3">
                        Canonical Field Completeness
                      </h4>
                      {Object.keys(fieldStats).length > 0 ? (
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                          {Object.entries(fieldStats).map(([fieldName, stats]) => (
                            <div
                              key={fieldName}
                              className="p-3 rounded-xl border border-gray-200 dark:border-slate-800 bg-gray-50/40 dark:bg-slate-800/30"
                            >
                              <div className="flex items-center justify-between mb-1.5">
                                <span className="text-xs font-semibold text-gray-800 dark:text-slate-200 font-mono">
                                  {fieldName}
                                </span>
                                <span className="text-xs font-bold text-gray-900 dark:text-slate-100">
                                  {stats.coverage_percentage.toFixed(1)}%
                                </span>
                              </div>
                              <div className="h-2 w-full rounded-full bg-gray-200 dark:bg-slate-700 overflow-hidden">
                                <div
                                  className={`h-full rounded-full transition-all duration-500 ${
                                    stats.coverage_percentage >= 80
                                      ? 'bg-emerald-500'
                                      : stats.coverage_percentage >= 50
                                      ? 'bg-sky-500'
                                      : stats.coverage_percentage > 0
                                      ? 'bg-amber-500'
                                      : 'bg-rose-500'
                                  }`}
                                  style={{ width: `${Math.min(100, stats.coverage_percentage)}%` }}
                                />
                              </div>
                              <div className="flex items-center justify-between mt-2 text-[11px] text-gray-500 dark:text-slate-400">
                                <span>{stats.populated_records} / {stats.total_records} populated</span>
                                {stats.invalid_records > 0 && (
                                  <span className="text-rose-500 font-medium">
                                    {stats.invalid_records} invalid
                                  </span>
                                )}
                              </div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p className="text-xs text-gray-500 dark:text-slate-400 italic">
                          Field-level completeness statistics are being computed or not available for this file.
                        </p>
                      )}
                    </div>

                    {/* Unmapped Columns */}
                    <div>
                      <h4 className="text-sm font-bold text-gray-900 dark:text-slate-100 mb-2">
                        Unmapped Custom Columns
                      </h4>
                      {unmappedCols.length > 0 ? (
                        <div className="flex flex-wrap gap-2">
                          {unmappedCols.map((col) => (
                            <span
                              key={col}
                              className="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-mono bg-gray-100 dark:bg-slate-800 text-gray-700 dark:text-slate-300 border border-gray-200 dark:border-slate-700"
                            >
                              {col}
                            </span>
                          ))}
                        </div>
                      ) : (
                        <p className="text-xs text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5 font-medium">
                          <CheckCircleIcon className="h-4 w-4" />
                          All detected source columns were successfully mapped to canonical fields!
                        </p>
                      )}
                    </div>
                  </div>
                )}

                {/* ── TAB 2: COLUMN MAPPINGS ── */}
                {activeTab === 'mappings' && (
                  <div className="space-y-4">
                    {/* Conflict Banner if any */}
                    {conflicts.length > 0 && (
                      <div className="p-3.5 rounded-xl border border-rose-200 dark:border-rose-900/60 bg-rose-50 dark:bg-rose-950/30 text-rose-800 dark:text-rose-300 text-xs">
                        <div className="font-bold flex items-center gap-1.5 text-rose-900 dark:text-rose-200">
                          <ExclamationTriangleIcon className="h-4 w-4 text-rose-600 dark:text-rose-400" />
                          Column Mapping Conflicts Detected ({conflicts.length})
                        </div>
                        <p className="mt-1">
                          Multiple source columns competed for the same canonical field. All original values are safely preserved in the dataset record.
                        </p>
                        <ul className="mt-2 space-y-1 font-mono">
                          {conflicts.map((c, i) => (
                            <li key={i}>• {c}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    <div className="border border-gray-200 dark:border-slate-800 rounded-xl overflow-hidden shadow-sm">
                      <table className="w-full text-left text-xs">
                        <thead className="bg-gray-50 dark:bg-slate-800/80 text-gray-600 dark:text-slate-400 font-semibold uppercase tracking-wider border-b border-gray-200 dark:border-slate-800">
                          <tr>
                            <th className="px-4 py-3">Original CSV Column</th>
                            <th className="px-4 py-3">Canonical Field</th>
                            <th className="px-4 py-3">Confidence</th>
                            <th className="px-4 py-3">Matching Method</th>
                            <th className="px-4 py-3">Status</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-100 dark:divide-slate-800/60">
                          {Object.entries(mappings).map(([origCol, mapInfo]: [string, ColumnMapping]) => {
                            const isConflict = mapInfo.status === 'conflict'
                            const isUncertain = mapInfo.status === 'uncertain'
                            const isMatched = mapInfo.status === 'matched'

                            return (
                              <tr key={origCol} className="hover:bg-gray-50/50 dark:hover:bg-slate-800/40 transition">
                                <td className="px-4 py-3 font-mono font-medium text-gray-900 dark:text-slate-100">
                                  {origCol}
                                </td>
                                <td className="px-4 py-3">
                                  {mapInfo.canonical_field ? (
                                    <span className="font-mono text-sky-600 dark:text-sky-400 font-semibold bg-sky-50 dark:bg-sky-950/50 px-2 py-0.5 rounded border border-sky-200 dark:border-sky-800/50">
                                      {mapInfo.canonical_field}
                                    </span>
                                  ) : (
                                    <span className="text-gray-400 italic">Unmapped</span>
                                  )}
                                </td>
                                <td className="px-4 py-3">
                                  <div className="flex items-center gap-1.5">
                                    <div className="w-12 h-1.5 rounded-full bg-gray-200 dark:bg-slate-700 overflow-hidden">
                                      <div
                                        className="h-full bg-sky-500 rounded-full"
                                        style={{ width: `${mapInfo.confidence * 100}%` }}
                                      />
                                    </div>
                                    <span className="font-semibold text-gray-700 dark:text-slate-300">
                                      {(mapInfo.confidence * 100).toFixed(0)}%
                                    </span>
                                  </div>
                                </td>
                                <td className="px-4 py-3 capitalize text-gray-600 dark:text-slate-400">
                                  {mapInfo.matching_method.replace(/_/g, ' ')}
                                </td>
                                <td className="px-4 py-3">
                                  {isMatched && (
                                    <Badge className="bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border-emerald-300 dark:border-emerald-800">
                                      Matched
                                    </Badge>
                                  )}
                                  {isConflict && (
                                    <Badge className="bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300 border-rose-300 dark:border-rose-800">
                                      Conflict
                                    </Badge>
                                  )}
                                  {isUncertain && (
                                    <Badge className="bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border-amber-300 dark:border-amber-800">
                                      Needs Review
                                    </Badge>
                                  )}
                                  {!isMatched && !isConflict && !isUncertain && (
                                    <Badge variant="outline" className="text-gray-500">
                                      Unmapped
                                    </Badge>
                                  )}
                                </td>
                              </tr>
                            )
                          })}
                        </tbody>
                      </table>
                    </div>

                    <p className="text-[11px] text-gray-500 dark:text-slate-500 italic">
                      Note: Column mappings are generated using Research Rover's canonical alias dictionary and intelligent normalizer.
                    </p>
                  </div>
                )}

                {/* ── TAB 3: FEATURE READINESS ── */}
                {activeTab === 'readiness' && (
                  <div className="space-y-4">
                    {/* Index Status Warning Banner */}
                    {hasIndexWarning && (
                      <div className="p-4 rounded-xl border border-amber-200 dark:border-amber-800/80 bg-amber-50 dark:bg-amber-950/40 text-amber-900 dark:text-amber-200 text-xs flex items-start gap-3">
                        <CpuChipIcon className="h-5 w-5 shrink-0 text-amber-600 dark:text-amber-400 mt-0.5" />
                        <div>
                          <div className="font-bold text-sm text-amber-900 dark:text-amber-100">
                            FAISS Vector Index Not Built
                          </div>
                          <p className="mt-1 opacity-90 leading-relaxed">
                            While the dataset has sufficient abstracts for analysis, semantic vector search and AI RAG chat require vector embeddings to be computed before retrieval can function. Keyword and country analyses remain fully available.
                          </p>
                        </div>
                      </div>
                    )}

                    <div className="grid grid-cols-1 gap-3">
                      {Object.entries(featureReadiness).map(([featureKey, feat]: [string, FeatureReadiness]) => {
                        const Icon = STATUS_ICONS[feat.status] || InformationCircleIcon
                        const colors = STATUS_COLORS[feat.status] || STATUS_COLORS.not_ready

                        return (
                          <div
                            key={featureKey}
                            className="p-4 rounded-xl border border-gray-200 dark:border-slate-800 bg-gray-50/40 dark:bg-slate-800/30 flex flex-col gap-3"
                          >
                            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                              <div className="flex items-center gap-2.5">
                                <Icon className={`h-5 w-5 shrink-0 ${colors.text}`} />
                                <h4 className="text-sm font-bold text-gray-900 dark:text-slate-100 capitalize">
                                  {feat.feature_name.replace(/_/g, ' ')}
                                </h4>
                              </div>
                              <span
                                className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold border ${colors.badge}`}
                              >
                                {STATUS_LABELS[feat.status] || feat.status}
                              </span>
                            </div>

                            <p className="text-xs text-gray-600 dark:text-slate-400 leading-relaxed">
                              {feat.explanation}
                            </p>

                            {/* Coverage Bar */}
                            <div className="space-y-1">
                              <div className="flex justify-between text-[11px] text-gray-500 dark:text-slate-400">
                                <span>Data Coverage</span>
                                <span className="font-semibold">{feat.coverage_percentage.toFixed(0)}%</span>
                              </div>
                              <div className="h-1.5 w-full bg-gray-200 dark:bg-slate-700 rounded-full overflow-hidden">
                                <div
                                  className={`h-full rounded-full transition-all ${colors.bg}`}
                                  style={{ width: `${feat.coverage_percentage}%` }}
                                />
                              </div>
                            </div>

                            {/* Required / Available / Missing Fields */}
                            <div className="flex flex-wrap items-center gap-2 pt-1 text-[11px]">
                              <span className="font-semibold text-gray-500 dark:text-slate-500 uppercase tracking-wider text-[10px]">
                                Available:
                              </span>
                              {feat.available_fields.map((f) => (
                                <span
                                  key={f}
                                  className="px-2 py-0.5 rounded bg-emerald-50 dark:bg-emerald-950/50 text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800/50 font-mono text-[10px]"
                                >
                                  {f}
                                </span>
                              ))}

                              {feat.missing_fields.length > 0 && (
                                <>
                                  <span className="font-semibold text-rose-500 uppercase tracking-wider text-[10px] ml-2">
                                    Missing:
                                  </span>
                                  {feat.missing_fields.map((f) => (
                                    <span
                                      key={f}
                                      className="px-2 py-0.5 rounded bg-rose-50 dark:bg-rose-950/50 text-rose-700 dark:text-rose-400 border border-rose-200 dark:border-rose-800/50 font-mono text-[10px]"
                                    >
                                      {f}
                                    </span>
                                  ))}
                                </>
                              )}
                            </div>

                            {/* Feature Warnings */}
                            {feat.warnings && feat.warnings.length > 0 && (
                              <div className="mt-1 p-2.5 rounded-lg bg-amber-50/80 dark:bg-amber-950/30 border border-amber-200/60 dark:border-amber-900/40 text-[11px] text-amber-800 dark:text-amber-300">
                                {feat.warnings.map((w, wi) => (
                                  <div key={wi} className="flex items-start gap-1.5">
                                    <span className="font-bold">•</span>
                                    <span>{w}</span>
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>
                        )
                      })}
                    </div>
                  </div>
                )}
              </>
            )}
          </div>

          {/* Footer */}
          <div className="flex items-center justify-between border-t border-gray-200 dark:border-slate-800 px-6 py-3.5 bg-gray-50/80 dark:bg-slate-900/90">
            <span className="text-xs text-gray-500 dark:text-slate-400">
              Universal Dataset Ingestion Engine (Phases 1–4)
            </span>
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-sm font-semibold text-white bg-slate-900 dark:bg-slate-100 dark:text-slate-900 hover:bg-slate-800 dark:hover:bg-white transition shadow-sm"
            >
              Done
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  )
}
