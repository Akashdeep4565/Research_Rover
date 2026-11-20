import { useMemo, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  GlobeAltIcon,
  DocumentTextIcon,
  ChartBarIcon,
  UserGroupIcon,
  ArrowDownTrayIcon,
  XMarkIcon,
  MapIcon,
  ShareIcon,
  Square2StackIcon,
  ExclamationTriangleIcon,
  MagnifyingGlassIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  InformationCircleIcon,
} from '@heroicons/react/24/outline'
import { toast } from 'sonner'
import type { CountryCollaborationGraphResponse, CountryStatisticsResponse, UnassignedPaperInfo } from '@/types'
import { WorldMap } from './WorldMap'
import { CountryCollaboration2D } from './CountryCollaboration2D'
import { ResearchRoverLoader } from './ResearchRoverLoader'
import { ErrorBoundary } from './ErrorBoundary'

// Theme colors matching Research-Rover design tokens
const COUNTRY_BAR_COLORS = [
  '#38bdf8', '#34d399', '#fb923c', '#a78bfa', '#f472b6',
  '#2dd4bf', '#facc15', '#06b6d4', '#818cf8', '#a3e635',
]

interface CountryAnalysisViewProps {
  countryStats: CountryStatisticsResponse | null
  countryData: CountryCollaborationGraphResponse | null
  loading: boolean
  error: string
  downloadBase: string
}

type ViewMode = 'all' | 'map' | 'network'

export function CountryAnalysisView({
  countryStats,
  countryData,
  loading,
  error,
  downloadBase,
}: CountryAnalysisViewProps) {
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null)
  const [viewMode, setViewMode] = useState<ViewMode>('all')
  const [countrySearch, setCountrySearch] = useState('')
  const [showUnassignedModal, setShowUnassignedModal] = useState(false)

  const hasData = useMemo(() => {
    return Boolean(
      countryStats &&
      (countryStats.total_papers > 0 || (Array.isArray(countryStats.countries) && countryStats.countries.length > 0))
    )
  }, [countryStats])

  // Primary stats values coming directly from countryStats API
  const totalPapers = countryStats?.total_papers || countryData?.total_papers || 0
  const papersWithCountry = countryStats?.papers_with_country_data ?? countryData?.papers_with_country_data ?? 0
  const papersWithoutCountry = countryStats?.papers_without_country_data ?? (totalPapers - papersWithCountry)
  const uniqueCountriesCount = countryStats?.unique_countries || (Array.isArray(countryStats?.countries) ? countryStats.countries.length : 0) || (Array.isArray(countryData?.nodes) ? countryData.nodes.length : 0)
  const internationalPapers = countryStats?.international_papers ?? countryData?.international_papers ?? 0
  const countryCoveragePercentage = countryStats?.country_coverage_percentage ?? (totalPapers > 0 ? parseFloat(((papersWithCountry / totalPapers) * 100).toFixed(1)) : 0.0)

  // Filtered countries for the scrollable/searchable ranking table
  const filteredCountries = useMemo(() => {
    if (!Array.isArray(countryStats?.countries)) return []
    if (!countrySearch.trim()) return countryStats.countries
    const q = countrySearch.toLowerCase().trim()
    return countryStats.countries.filter((c) => c?.country && c.country.toLowerCase().includes(q))
  }, [countryStats, countrySearch])

  // Download helpers using primary statistics API
  const handleDownloadRanking = () => {
    if (!countryStats?.countries.length) {
      toast.error('No country data available to export.')
      return
    }
    const headers = ['Rank', 'Country', 'ISO_A3', 'Papers', 'Percentage']
    const rows = countryStats.countries.map((c, idx) => [
      idx + 1,
      c.country,
      c.iso_a3 || '',
      c.frequency,
      `${c.percentage}%`,
    ])
    const csvContent = [headers.join(','), ...rows.map((r) => r.join(','))].join('\n')
    
    const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${downloadBase}_country_ranking.csv`
    a.click()
    URL.revokeObjectURL(url)
    toast.success('Country ranking CSV downloaded')
  }

  const handleDownloadCollaborations = () => {
    if (!countryData?.links.length) {
      toast.error('No collaboration data available to export.')
      return
    }
    const headers = ['Source Country', 'Target Country', 'Collaboration Weight']
    const rows = countryData.links.map((l) => [l.source, l.target, l.weight])
    const csvContent = [headers.join(','), ...rows.map((r) => r.join(','))].join('\n')

    const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${downloadBase}_country_collaborations.csv`
    a.click()
    URL.revokeObjectURL(url)
    toast.success('Country collaborations CSV downloaded')
  }

  return (
    <div className="space-y-6">
      {/* Loading State */}
      {loading && (
        <div className="py-16 flex justify-center items-center w-full bg-white/50 dark:bg-slate-900/50 rounded-2xl border border-gray-200 dark:border-slate-800">
          <ResearchRoverLoader
            message="Analyzing paper countries & international collaboration networks..."
            size="lg"
          />
        </div>
      )}

      {/* Error state */}
      {!loading && error && (
        <div className="flex items-start gap-3 rounded-2xl border border-rose-500/25 bg-rose-500/8 p-5 text-sm text-rose-400">
          <XMarkIcon className="mt-0.5 h-5 w-5 shrink-0 text-rose-400" />
          <div>
            <p className="font-bold">Error loading country analysis</p>
            <p className="mt-1 text-xs opacity-90">{error}</p>
          </div>
        </div>
      )}

      {/* Empty state: No country/affiliation data in dataset */}
      {!loading && !error && !hasData && (
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col items-center justify-center rounded-2xl border border-amber-500/30 bg-amber-500/5 p-12 text-center"
        >
          <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl border border-amber-500/20 bg-amber-500/10 text-amber-500 shadow-lg shadow-amber-500/10">
            <GlobeAltIcon className="h-8 w-8" />
          </div>
          <h3 className="text-lg font-bold text-gray-900 dark:text-slate-100">
            Country Information Unavailable
          </h3>
          <p className="mt-2 max-w-md text-sm leading-relaxed text-gray-600 dark:text-slate-400">
            Country information is not available in this dataset because author affiliation data was not found.
          </p>
          <p className="mt-4 rounded-xl border border-gray-200 dark:border-slate-800 bg-white/60 dark:bg-slate-900/60 px-4 py-2 text-xs text-gray-500 dark:text-slate-500">
            Note: PubMed searches performed in Research-Rover automatically extract full author affiliation and country metadata.
          </p>
        </motion.div>
      )}

      {/* Active Country Data View */}
      {!loading && !error && hasData && countryStats && (
        <>
          {/* Header Controls & View Toggle Bar */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-white/60 dark:bg-slate-900/60 p-4 rounded-2xl border border-gray-200 dark:border-slate-800 backdrop-blur-md">
            <div>
              <h2 className="text-lg font-bold text-gray-900 dark:text-slate-100 flex items-center gap-2">
                <GlobeAltIcon className="h-5 w-5 text-blue-500" />
                Paper-Level Bibliometric Country Analysis
              </h2>
              <p className="text-xs text-gray-500 dark:text-slate-400">
                Author affiliation geographic mapping & international collaboration network across {totalPapers.toLocaleString()} papers
              </p>
            </div>

            {/* View Switcher */}
            <div className="flex items-center gap-1 bg-gray-100 dark:bg-slate-800 p-1 rounded-xl border border-gray-200 dark:border-slate-700 text-xs font-medium">
              <button
                type="button"
                onClick={() => setViewMode('all')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-all ${
                  viewMode === 'all'
                    ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-blue-400 shadow-sm font-bold'
                    : 'text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-200'
                }`}
              >
                <Square2StackIcon className="h-4 w-4" />
                All Views
              </button>
              <button
                type="button"
                onClick={() => setViewMode('map')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-all ${
                  viewMode === 'map'
                    ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-blue-400 shadow-sm font-bold'
                    : 'text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-200'
                }`}
              >
                <MapIcon className="h-4 w-4" />
                World Map
              </button>
              <button
                type="button"
                onClick={() => setViewMode('network')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-all ${
                  viewMode === 'network'
                    ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-blue-400 shadow-sm font-bold'
                    : 'text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-200'
                }`}
              >
                <ShareIcon className="h-4 w-4" />
                Collaboration Network
              </button>
            </div>
          </div>

          {/* Requirement 9: Clear Coverage Summary Cards */}
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6"
          >
            {[
              {
                title: 'Total Papers',
                value: totalPapers,
                sub: 'Records in CSV',
                icon: DocumentTextIcon,
                accent: '#38bdf8',
              },
              {
                title: 'With Country Data',
                value: papersWithCountry,
                sub: 'Extracted affiliations',
                icon: ChartBarIcon,
                accent: '#34d399',
              },
              {
                title: 'Without Country Data',
                value: papersWithoutCountry,
                sub: 'Missing / unassigned',
                icon: ExclamationTriangleIcon,
                accent: '#f43f5e',
              },
              {
                title: 'Countries Detected',
                value: uniqueCountriesCount,
                sub: 'Unique nations',
                icon: GlobeAltIcon,
                accent: '#a78bfa',
              },
              {
                title: 'International Papers',
                value: internationalPapers,
                sub: '≥ 2 countries',
                icon: UserGroupIcon,
                accent: '#fb923c',
              },
              {
                title: 'Country Coverage',
                value: `${countryCoveragePercentage}%`,
                sub: `${papersWithCountry} / ${totalPapers}`,
                icon: ChartBarIcon,
                accent: '#2dd4bf',
                isString: true,
              },
            ].map(({ title, value, sub, icon: Icon, accent, isString }, i) => (
              <motion.div
                key={title}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.03 }}
                className="rounded-2xl border border-gray-200 dark:border-slate-800/60 bg-white dark:bg-slate-900 p-4 shadow-sm"
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="min-w-0 flex-1">
                    <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-gray-500 dark:text-slate-500 truncate" title={title}>
                      {title}
                    </p>
                    <p className="mt-1.5 text-2xl font-bold tabular-nums text-gray-900 dark:text-slate-50">
                      {isString ? value : (value as number).toLocaleString()}
                    </p>
                    <p className="mt-0.5 truncate text-[11px] text-gray-400 dark:text-slate-500" title={sub}>
                      {sub}
                    </p>
                  </div>
                  <div
                    className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg"
                    style={{ background: `${accent}18`, border: `1px solid ${accent}30` }}
                  >
                    <Icon className="h-4 w-4" style={{ color: accent }} />
                  </div>
                </div>
                <div
                  className="mt-3 h-0.5 w-full rounded-full"
                  style={{ background: `linear-gradient(90deg, ${accent}60 0%, transparent 100%)` }}
                />
              </motion.div>
            ))}
          </motion.div>

          {/* Requirement 10: Paper Coverage Visualization */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-2xl border border-gray-200 dark:border-slate-800/60 bg-white dark:bg-slate-900 p-5 shadow-sm"
          >
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 mb-3">
              <div>
                <h3 className="text-sm font-bold text-gray-900 dark:text-slate-100 flex items-center gap-2">
                  <ChartBarIcon className="h-4 w-4 text-sky-500" />
                  Paper Country Metadata Coverage
                </h3>
                <p className="text-xs text-gray-500 dark:text-slate-400">
                  Calculated coverage breakdown across all {totalPapers.toLocaleString()} records in the active dataset
                </p>
              </div>
              <div className="flex items-center gap-4 text-xs font-medium">
                <div className="flex items-center gap-1.5">
                  <span className="h-3 w-3 rounded-full bg-emerald-500" />
                  <span className="text-gray-700 dark:text-slate-300">With Country: <strong>{papersWithCountry.toLocaleString()}</strong> ({countryCoveragePercentage}%)</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <span className="h-3 w-3 rounded-full bg-slate-400 dark:bg-slate-600" />
                  <span className="text-gray-700 dark:text-slate-300">Without Country: <strong>{papersWithoutCountry.toLocaleString()}</strong> ({(100 - countryCoveragePercentage).toFixed(1)}%)</span>
                </div>
              </div>
            </div>

            {/* Split Bar */}
            <div className="h-4 w-full overflow-hidden rounded-full bg-gray-100 dark:bg-slate-800 p-0.5 flex">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${countryCoveragePercentage}%` }}
                transition={{ duration: 0.6 }}
                className="h-full rounded-l-full bg-gradient-to-r from-emerald-500 to-sky-500"
                title={`Papers With Country Info: ${papersWithCountry} (${countryCoveragePercentage}%)`}
              />
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${100 - countryCoveragePercentage}%` }}
                transition={{ duration: 0.6 }}
                className="h-full rounded-r-full bg-gradient-to-r from-slate-400 to-slate-500 dark:from-slate-600 dark:to-slate-700"
                title={`Papers Without Country Info: ${papersWithoutCountry} (${(100 - countryCoveragePercentage).toFixed(1)}%)`}
              />
            </div>
          </motion.div>

          {/* Requirement 11: Unassigned Papers Section */}
          {papersWithoutCountry > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/80 p-4"
            >
              <div className="flex items-center gap-3">
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-amber-500/20 bg-amber-500/10 text-amber-500">
                  <InformationCircleIcon className="h-5 w-5" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-900 dark:text-slate-200">
                    Country information unavailable for {papersWithoutCountry.toLocaleString()} papers.
                  </p>
                  <p className="text-xs text-gray-500 dark:text-slate-400">
                    These papers lacked usable affiliation metadata in the source dataset. They are preserved without geographic speculation.
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setShowUnassignedModal(true)}
                className="shrink-0 flex items-center gap-1.5 rounded-xl border border-gray-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2 text-xs font-semibold text-gray-700 dark:text-slate-200 shadow-sm transition hover:bg-gray-50 dark:hover:bg-slate-700"
              >
                View papers without country information ({papersWithoutCountry.toLocaleString()})
              </button>
            </motion.div>
          )}

          {/* Interactive World Map Section */}
          {(viewMode === 'all' || viewMode === 'map') && (
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <ErrorBoundary
                fallbackTitle="World Map Unavailable"
                fallbackMessage="The World Map visualization encountered an error and could not be rendered."
              >
                <WorldMap
                  countries={Array.isArray(countryStats.countries) ? countryStats.countries : []}
                  totalPapers={countryStats.total_papers || 0}
                  selectedCountry={selectedNodeId}
                  onSelectCountry={(name) => setSelectedNodeId(name)}
                />
              </ErrorBoundary>
            </motion.div>
          )}

          {/* Country Collaboration Network Section */}
          {(viewMode === 'all' || viewMode === 'network') && (
            <div className="w-full max-w-full">
              <ErrorBoundary
                fallbackTitle="Collaboration Network Unavailable"
                fallbackMessage="Country Collaboration Network encountered an error and is currently unavailable."
              >
                <CountryCollaboration2D
                  countryData={countryData}
                  countryStats={countryStats}
                  selectedCountry={selectedNodeId}
                  onSelectCountry={(name) => setSelectedNodeId(name)}
                  downloadBase={downloadBase}
                />
              </ErrorBoundary>
            </div>
          )}

          {/* Row 1: Top Countries Bar Chart + Requirement 8: ALL Country Ranking Table */}
          {(viewMode === 'all' || viewMode === 'map') && (
            <div className="grid grid-cols-1 gap-4 xl:grid-cols-2">
              {/* Top Countries Bar Chart Card */}
              <div className="flex flex-col overflow-hidden rounded-2xl border border-gray-200 dark:border-slate-800/60 bg-white dark:bg-slate-900 shadow-sm">
                <div className="flex items-center justify-between gap-3 border-b border-gray-200 dark:border-slate-800/60 px-5 py-3.5">
                  <div>
                    <h3 className="text-sm font-bold text-gray-900 dark:text-slate-100">
                      Top Countries by Publication Count
                    </h3>
                    <p className="mt-0.5 text-xs text-gray-400 dark:text-slate-600">
                      Distribution of research outputs across top detected countries
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={handleDownloadRanking}
                    className="flex shrink-0 items-center gap-1.5 rounded-lg border border-gray-200 dark:border-slate-700/60 bg-gray-50 dark:bg-slate-900/60 px-3 py-1.5 text-xs font-medium text-gray-500 dark:text-slate-400 transition hover:bg-gray-100 dark:hover:bg-slate-800 hover:text-gray-900 dark:hover:text-slate-100"
                  >
                    <ArrowDownTrayIcon className="h-3.5 w-3.5" />
                    CSV
                  </button>
                </div>

                <div className="flex-1 p-5">
                  <div className="space-y-3">
                    {countryStats.countries.slice(0, 10).map((item, i) => {
                      const max = countryStats.countries[0]?.frequency || 1
                      const color = COUNTRY_BAR_COLORS[i % COUNTRY_BAR_COLORS.length]

                      return (
                        <div
                          key={item.country}
                          className="cursor-pointer transition-opacity hover:opacity-90"
                          onClick={() => setSelectedNodeId(item.country)}
                        >
                          <div className="mb-1 flex items-center justify-between gap-2 text-xs">
                            <span className="font-semibold text-gray-800 dark:text-slate-200">
                              {item.country}
                            </span>
                            <span className="tabular-nums text-gray-400 dark:text-slate-500">
                              {item.frequency.toLocaleString()} papers · {item.percentage}%
                            </span>
                          </div>
                          <div className="h-2.5 overflow-hidden rounded-full bg-gray-100 dark:bg-slate-800">
                            <motion.div
                              initial={{ width: 0 }}
                              animate={{ width: `${(item.frequency / max) * 100}%` }}
                              transition={{ duration: 0.5, delay: i * 0.04 }}
                              className="h-full rounded-full"
                              style={{
                                background: `linear-gradient(90deg, ${color}cc, ${color}88)`,
                              }}
                            />
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </div>
              </div>

              {/* Requirement 8: Complete Country Ranking Table Card */}
              <div className="flex flex-col overflow-hidden rounded-2xl border border-gray-200 dark:border-slate-800/60 bg-white dark:bg-slate-900 shadow-sm">
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-gray-200 dark:border-slate-800/60 px-5 py-3.5">
                  <div>
                    <h3 className="text-sm font-bold text-gray-900 dark:text-slate-100 flex items-center gap-2">
                      Country Publication Ranking
                      <span className="rounded-md bg-sky-500/10 px-2 py-0.5 text-[10px] font-bold text-sky-600 dark:text-sky-400 border border-sky-500/20">
                        {countryStats.countries.length} Countries
                      </span>
                    </h3>
                    <p className="mt-0.5 text-xs text-gray-400 dark:text-slate-600">
                      All {uniqueCountriesCount} detected countries sorted by paper count
                    </p>
                  </div>
                  <div className="flex items-center gap-2 w-full sm:w-auto">
                    {/* Search Input for Ranking Table */}
                    <div className="relative flex-1 sm:w-44">
                      <input
                        type="text"
                        placeholder="Search country..."
                        value={countrySearch}
                        onChange={(e) => setCountrySearch(e.target.value)}
                        className="w-full rounded-lg border border-gray-300 dark:border-slate-700 bg-gray-50 dark:bg-slate-800/80 px-3 py-1.5 pl-8 text-xs text-gray-800 dark:text-slate-200 outline-none focus:border-sky-500"
                      />
                      <MagnifyingGlassIcon className="absolute left-2.5 top-2 h-3.5 w-3.5 text-gray-400 dark:text-slate-500" />
                      {countrySearch && (
                        <button
                          type="button"
                          onClick={() => setCountrySearch('')}
                          className="absolute right-2 top-2 text-gray-400 hover:text-gray-600 dark:hover:text-slate-200"
                        >
                          <XMarkIcon className="h-3.5 w-3.5" />
                        </button>
                      )}
                    </div>
                    <button
                      type="button"
                      onClick={handleDownloadRanking}
                      className="flex shrink-0 items-center gap-1.5 rounded-lg border border-gray-200 dark:border-slate-700/60 bg-gray-50 dark:bg-slate-900/60 px-3 py-1.5 text-xs font-medium text-gray-500 dark:text-slate-400 transition hover:bg-gray-100 dark:hover:bg-slate-800 hover:text-gray-900 dark:hover:text-slate-100"
                    >
                      <ArrowDownTrayIcon className="h-3.5 w-3.5" />
                      CSV
                    </button>
                  </div>
                </div>

                <div className="flex-1 p-5">
                  <div
                    className="overflow-auto rounded-xl border border-gray-200 dark:border-slate-800/50"
                    style={{ maxHeight: '360px' }}
                  >
                    <table className="min-w-full border-collapse text-xs">
                      <thead className="sticky top-0 bg-gray-50 dark:bg-slate-900 z-10">
                        <tr className="border-b border-gray-200 dark:border-slate-800">
                          <th className="px-3 py-2.5 text-left font-semibold uppercase tracking-[0.18em] text-gray-400 dark:text-slate-500 w-12">
                            Rank
                          </th>
                          <th className="px-3 py-2.5 text-left font-semibold uppercase tracking-[0.18em] text-gray-400 dark:text-slate-500">
                            Country
                          </th>
                          <th className="px-3 py-2.5 text-right font-semibold uppercase tracking-[0.18em] text-gray-400 dark:text-slate-500">
                            Papers
                          </th>
                          <th className="px-3 py-2.5 text-right font-semibold uppercase tracking-[0.18em] text-gray-400 dark:text-slate-500">
                            Percentage
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {filteredCountries.length > 0 ? (
                          filteredCountries.map((item) => {
                            const isSelected = selectedNodeId === item.country
                            const rank = countryStats.countries.findIndex((c) => c.country === item.country) + 1

                            return (
                              <tr
                                key={item.country}
                                onClick={() => setSelectedNodeId(item.country)}
                                className={`border-b border-gray-100 dark:border-slate-800/50 cursor-pointer transition-colors ${
                                  isSelected
                                    ? 'bg-sky-500/10 dark:bg-sky-500/15 font-bold'
                                    : 'hover:bg-gray-50 dark:hover:bg-slate-900/50'
                                }`}
                              >
                                <td className="px-3 py-2.5 text-gray-400 dark:text-slate-500 font-mono">
                                  #{rank}
                                </td>
                                <td className="px-3 py-2.5 font-medium text-gray-800 dark:text-slate-200">
                                  {item.country} {item.iso_a3 ? `(${item.iso_a3})` : ''}
                                </td>
                                <td className="px-3 py-2.5 text-right font-semibold text-gray-900 dark:text-slate-100 font-mono">
                                  {item.frequency.toLocaleString()}
                                </td>
                                <td className="px-3 py-2.5 text-right text-gray-500 dark:text-slate-400 font-mono">
                                  {item.percentage}%
                                </td>
                              </tr>
                            )
                          })
                        ) : (
                          <tr>
                            <td colSpan={4} className="py-6 text-center text-xs text-gray-400 dark:text-slate-500">
                              No country matching &quot;{countrySearch}&quot;
                            </td>
                          </tr>
                        )}
                      </tbody>
                    </table>
                  </div>
                  <p className="mt-2 text-[11px] text-gray-400 dark:text-slate-500 text-center">
                    Note: Percentages represent share of total papers ({totalPapers.toLocaleString()}) and may sum to &gt;100% due to multi-country co-authorships.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Row 2: Top Country Collaborations Table */}
          {(viewMode === 'all' || viewMode === 'network') && countryData && (
            <div className="flex flex-col overflow-hidden rounded-2xl border border-gray-200 dark:border-slate-800/60 bg-white dark:bg-slate-900 shadow-sm">
              <div className="flex items-center justify-between gap-3 border-b border-gray-200 dark:border-slate-800/60 px-5 py-3.5">
                <div>
                  <h3 className="text-sm font-bold text-gray-900 dark:text-slate-100">
                    International Co-Authorship Partnerships
                  </h3>
                  <p className="mt-0.5 text-xs text-gray-400 dark:text-slate-600">
                    Pairs of countries co-authoring papers ({countryData.links.length} total collaboration edges)
                  </p>
                </div>
                <button
                  type="button"
                  onClick={handleDownloadCollaborations}
                  disabled={!countryData.links.length}
                  className="flex shrink-0 items-center gap-1.5 rounded-lg border border-gray-200 dark:border-slate-700/60 bg-gray-50 dark:bg-slate-900/60 px-3 py-1.5 text-xs font-medium text-gray-500 dark:text-slate-400 transition hover:bg-gray-100 dark:hover:bg-slate-800 hover:text-gray-900 dark:hover:text-slate-100 disabled:opacity-40"
                >
                  <ArrowDownTrayIcon className="h-3.5 w-3.5" />
                  CSV
                </button>
              </div>

              <div className="p-5">
                {countryData.links.length > 0 ? (
                  <div
                    className="overflow-auto rounded-xl border border-gray-200 dark:border-slate-800/50"
                    style={{ maxHeight: '340px' }}
                  >
                    <table className="min-w-full border-collapse text-xs">
                      <thead className="sticky top-0 bg-gray-50 dark:bg-slate-900 z-10">
                        <tr className="border-b border-gray-200 dark:border-slate-800">
                          <th className="px-4 py-2.5 text-left font-semibold uppercase tracking-[0.18em] text-gray-400 dark:text-slate-500">
                            Country 1
                          </th>
                          <th className="px-4 py-2.5 text-center font-semibold uppercase tracking-[0.18em] text-gray-400 dark:text-slate-500">
                            Relationship
                          </th>
                          <th className="px-4 py-2.5 text-left font-semibold uppercase tracking-[0.18em] text-gray-400 dark:text-slate-500">
                            Country 2
                          </th>
                          <th className="px-4 py-2.5 text-right font-semibold uppercase tracking-[0.18em] text-gray-400 dark:text-slate-500">
                            Joint Papers (Strength)
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {countryData.links.map((link) => (
                          <tr
                            key={`${link.source}-${link.target}`}
                            className="border-b border-gray-100 dark:border-slate-800/50 hover:bg-gray-50 dark:hover:bg-slate-900/50"
                          >
                            <td className="px-4 py-2.5 font-semibold text-gray-900 dark:text-slate-100">
                              {link.source}
                            </td>
                            <td className="px-4 py-2.5 text-center text-sky-500 dark:text-sky-400 font-bold">
                              ↔
                            </td>
                            <td className="px-4 py-2.5 font-semibold text-gray-900 dark:text-slate-100">
                              {link.target}
                            </td>
                            <td className="px-4 py-2.5 text-right font-mono font-bold text-gray-900 dark:text-slate-50">
                              <span className="rounded-md border border-sky-500/20 bg-sky-500/10 px-2 py-0.5 text-xs text-sky-600 dark:text-sky-400">
                                {link.weight} {link.weight === 1 ? 'paper' : 'papers'}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <div className="py-8 text-center text-xs text-gray-400 dark:text-slate-500">
                    No international co-authorships detected among the papers in this dataset.
                  </div>
                )}
              </div>
            </div>
          )}
        </>
      )}

      {/* Requirement 11: Unassigned Papers Inspection Modal */}
      <AnimatePresence>
        {showUnassignedModal && countryStats?.unassigned_papers && (
          <UnassignedPapersModal
            unassignedList={countryStats.unassigned_papers}
            totalUnassigned={papersWithoutCountry}
            onClose={() => setShowUnassignedModal(false)}
          />
        )}
      </AnimatePresence>
    </div>
  )
}

// Sub-component for inspecting papers without country information
function UnassignedPapersModal({
  unassignedList,
  totalUnassigned,
  onClose,
}: {
  unassignedList: UnassignedPaperInfo[]
  totalUnassigned: number
  onClose: () => void
}) {
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  const pageSize = 15

  const filtered = useMemo(() => {
    if (!search.trim()) return unassignedList
    const q = search.toLowerCase().trim()
    return unassignedList.filter(
      (p) =>
        p.title.toLowerCase().includes(q) ||
        (p.source && p.source.toLowerCase().includes(q)) ||
        (p.paper_id && p.paper_id.toLowerCase().includes(q))
    )
  }, [unassignedList, search])

  const totalPages = Math.ceil(filtered.length / pageSize) || 1
  const paginated = useMemo(() => {
    const start = (page - 1) * pageSize
    return filtered.slice(start, start + pageSize)
  }, [filtered, page])

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/50 p-4 dark:bg-slate-950/90 backdrop-blur-md"
      onClick={(e) => { if (e.target === e.currentTarget) onClose() }}
    >
      <motion.div
        initial={{ scale: 0.95, opacity: 0, y: 12 }}
        animate={{ scale: 1, opacity: 1, y: 0 }}
        exit={{ scale: 0.96, opacity: 0 }}
        className="flex flex-col overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900"
        style={{ width: 'min(94vw, 1000px)', maxHeight: '85vh' }}
      >
        {/* Header */}
        <div className="flex shrink-0 items-center justify-between gap-4 border-b border-gray-200 dark:border-slate-800 px-6 py-4">
          <div>
            <h3 className="text-base font-bold text-gray-900 dark:text-slate-100 flex items-center gap-2">
              <ExclamationTriangleIcon className="h-5 w-5 text-amber-500" />
              Papers Without Country Information ({totalUnassigned.toLocaleString()})
            </h3>
            <p className="text-xs text-gray-500 dark:text-slate-400">
              Showing records for which country affiliation metadata could not be extracted
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="flex items-center gap-1.5 rounded-xl border border-gray-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-1.5 text-xs font-semibold text-gray-700 dark:text-slate-300 hover:bg-gray-100 dark:hover:bg-slate-700"
          >
            <XMarkIcon className="h-4 w-4" />
            Close
          </button>
        </div>

        {/* Filter bar */}
        <div className="flex shrink-0 items-center justify-between gap-4 border-b border-gray-200 dark:border-slate-800/60 bg-gray-50 dark:bg-slate-950/40 px-6 py-3">
          <div className="relative flex-1 max-w-md">
            <input
              type="text"
              placeholder="Search title, journal, or paper ID..."
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(1) }}
              className="w-full rounded-lg border border-gray-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-1.5 pl-8 text-xs text-gray-800 dark:text-slate-200 outline-none focus:border-sky-500"
            />
            <MagnifyingGlassIcon className="absolute left-2.5 top-2 h-3.5 w-3.5 text-gray-400 dark:text-slate-500" />
            {search && (
              <button
                type="button"
                onClick={() => setSearch('')}
                className="absolute right-2 top-2 text-gray-400 hover:text-gray-600 dark:hover:text-slate-200"
              >
                <XMarkIcon className="h-3.5 w-3.5" />
              </button>
            )}
          </div>
          <div className="text-xs text-gray-500 dark:text-slate-400">
            Showing {filtered.length} of {unassignedList.length} loaded records
          </div>
        </div>

        {/* Table */}
        <div className="flex-1 overflow-auto p-6">
          <div className="overflow-hidden rounded-xl border border-gray-200 dark:border-slate-800">
            <table className="min-w-full border-collapse text-xs">
              <thead className="bg-gray-50 dark:bg-slate-900 sticky top-0 z-10">
                <tr className="border-b border-gray-200 dark:border-slate-800">
                  <th className="px-3 py-2.5 text-left font-semibold uppercase tracking-[0.16em] text-gray-400 dark:text-slate-500 w-12">#</th>
                  <th className="px-3 py-2.5 text-left font-semibold uppercase tracking-[0.16em] text-gray-400 dark:text-slate-500">ID</th>
                  <th className="px-4 py-2.5 text-left font-semibold uppercase tracking-[0.16em] text-gray-400 dark:text-slate-500">Title</th>
                  <th className="px-3 py-2.5 text-left font-semibold uppercase tracking-[0.16em] text-gray-400 dark:text-slate-500">Journal / Source</th>
                  <th className="px-3 py-2.5 text-center font-semibold uppercase tracking-[0.16em] text-gray-400 dark:text-slate-500 w-16">Year</th>
                </tr>
              </thead>
              <tbody>
                {paginated.length > 0 ? (
                  paginated.map((paper, idx) => (
                    <tr key={paper.paper_id + idx} className="border-b border-gray-100 dark:border-slate-800/50 hover:bg-gray-50 dark:hover:bg-slate-900/50">
                      <td className="px-3 py-2.5 text-gray-400 dark:text-slate-500 font-mono">{(page - 1) * pageSize + idx + 1}</td>
                      <td className="px-3 py-2.5 font-mono text-gray-600 dark:text-slate-400 font-medium truncate max-w-[100px]" title={paper.paper_id}>{paper.paper_id}</td>
                      <td className="px-4 py-2.5 font-semibold text-gray-900 dark:text-slate-100 max-w-[360px] truncate" title={paper.title}>{paper.title}</td>
                      <td className="px-3 py-2.5 text-gray-500 dark:text-slate-400 truncate max-w-[180px]" title={String(paper.source || '—')}>{paper.source || '—'}</td>
                      <td className="px-3 py-2.5 text-center font-mono text-gray-500 dark:text-slate-400">{paper.year || '—'}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={5} className="py-8 text-center text-xs text-gray-400 dark:text-slate-500">
                      No unassigned papers match your search.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Footer Pagination */}
        <div className="flex shrink-0 items-center justify-between border-t border-gray-200 dark:border-slate-800 bg-gray-50 dark:bg-slate-950/40 px-6 py-3 text-xs text-gray-500 dark:text-slate-400">
          <div>
            Page {page} of {totalPages}
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              disabled={page <= 1}
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              className="flex items-center gap-1 rounded-lg border border-gray-300 dark:border-slate-700 px-2.5 py-1 text-xs disabled:opacity-40"
            >
              <ChevronLeftIcon className="h-3.5 w-3.5" /> Previous
            </button>
            <button
              type="button"
              disabled={page >= totalPages}
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              className="flex items-center gap-1 rounded-lg border border-gray-300 dark:border-slate-700 px-2.5 py-1 text-xs disabled:opacity-40"
            >
              Next <ChevronRightIcon className="h-3.5 w-3.5" />
            </button>
          </div>
        </div>
      </motion.div>
    </motion.div>
  )
}
