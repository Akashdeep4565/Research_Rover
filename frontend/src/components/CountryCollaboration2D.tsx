import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import ForceGraph2D from 'react-force-graph-2d'
import {
  MagnifyingGlassIcon,
  ArrowPathIcon,
  FunnelIcon,
  PlusIcon,
  MinusIcon,
  ArrowsPointingOutIcon,
  ArrowsPointingInIcon,
  ArrowDownTrayIcon,
  GlobeAltIcon,
  ShareIcon,
  XMarkIcon,
} from '@heroicons/react/24/outline'
import { toast } from 'sonner'
import type {
  CountryCollaborationGraphResponse,
  CountryStatisticsResponse,
} from '@/types'

export interface CountryCollaboration2DProps {
  countryData: CountryCollaborationGraphResponse | null
  countryStats: CountryStatisticsResponse | null
  selectedCountry?: string | null
  onSelectCountry?: (countryName: string | null) => void
  downloadBase?: string
}

interface GraphNode {
  id: string
  label: string
  paperCount: number
  collabCount: number
  iso_a3?: string
  x?: number
  y?: number
  vx?: number
  vy?: number
}

interface GraphLink {
  source: string | GraphNode
  target: string | GraphNode
  weight: number
}

type FilterMode = 'all' | 'medium' | 'strong'

export function CountryCollaboration2D({
  countryData,
  countryStats,
  selectedCountry,
  onSelectCountry,
  downloadBase,
}: CountryCollaboration2DProps) {
  const fgRef = useRef<any>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  const [dimensions, setDimensions] = useState({ width: 800, height: 520 })
  const [activeNodeId, setActiveNodeId] = useState<string | null>(selectedCountry || null)
  const [hoveredNodeId, setHoveredNodeId] = useState<string | null>(null)
  const [hoveredLink, setHoveredLink] = useState<{ source: string; target: string; weight: number } | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [filterMode, setFilterMode] = useState<FilterMode>('all')
  const [isFullscreen, setIsFullscreen] = useState(false)

  // Track the natural in-card dimensions so we can restore them cleanly upon exiting fullscreen
  const normalDimensionsRef = useRef<{ width: number; height: number }>({ width: 800, height: 520 })
  const originalBodyOverflow = useRef('')
  const originalHtmlOverflow = useRef('')

  // Sync internal activeNodeId state when external selectedCountry changes
  useEffect(() => {
    setActiveNodeId(selectedCountry || null)
  }, [selectedCountry])

  // Measure container dimensions cleanly
  const updateSize = useCallback(() => {
    if (!containerRef.current) return
    const rect = containerRef.current.getBoundingClientRect()
    const w = Math.floor(rect.width) || containerRef.current.clientWidth || 800
    const h = Math.floor(rect.height) || containerRef.current.clientHeight || 520
    const finalW = Math.max(300, w)
    const finalH = Math.max(300, h)

    if (!isFullscreen) {
      normalDimensionsRef.current = { width: finalW, height: finalH }
    }

    setDimensions({
      width: finalW,
      height: finalH,
    })
  }, [isFullscreen])

  // Container resize observer to keep graph responsive
  useEffect(() => {
    if (!containerRef.current) return
    updateSize()
    const observer = new ResizeObserver(() => {
      updateSize()
    })
    observer.observe(containerRef.current)
    return () => observer.disconnect()
  }, [updateSize])

  // Fullscreen open & close lifecycle with body scroll lock and robust restoration
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isFullscreen) {
        setIsFullscreen(false)
      }
    }

    if (isFullscreen) {
      // 1. Record existing overflow styles
      originalBodyOverflow.current = document.body.style.overflow
      originalHtmlOverflow.current = document.documentElement.style.overflow

      // 2. Lock scroll on both body and html
      document.body.style.overflow = 'hidden'
      document.documentElement.style.overflow = 'hidden'
      window.addEventListener('keydown', handleKeyDown)

      // 3. Allow fullscreen container to mount and resize to viewport
      const timer = setTimeout(() => {
        updateSize()
        if (fgRef.current) {
          fgRef.current.zoomToFit(400, 45)
        }
      }, 80)

      return () => {
        clearTimeout(timer)
        window.removeEventListener('keydown', handleKeyDown)
      }
    } else {
      // Exiting Fullscreen:
      // 1. Restore body and HTML overflow
      document.body.style.overflow = originalBodyOverflow.current
      document.documentElement.style.overflow = originalHtmlOverflow.current

      // 2. Prevent horizontal scroll displacement
      window.scrollTo({ left: 0 })

      // 3. Immediately restore dimensions to last known normal dimensions to avoid canvas stretch
      const fallback = normalDimensionsRef.current
      setDimensions({ width: fallback.width || 800, height: fallback.height || 520 })

      // 4. Wait for normal card container to re-render in DOM and measure actual natural bounds
      let rafId: number
      const timer = setTimeout(() => {
        rafId = requestAnimationFrame(() => {
          if (containerRef.current) {
            const rect = containerRef.current.getBoundingClientRect()
            const w = Math.floor(rect.width) || containerRef.current.clientWidth || fallback.width || 800
            const h = Math.floor(rect.height) || containerRef.current.clientHeight || fallback.height || 520
            setDimensions({ width: w, height: h })
            normalDimensionsRef.current = { width: w, height: h }

            // Recenter and fit graph inside normal card
            setTimeout(() => {
              if (fgRef.current) {
                fgRef.current.zoomToFit(350, 40)
              }
            }, 60)
          }
        })
      }, 50)

      return () => {
        clearTimeout(timer)
        cancelAnimationFrame(rafId)
      }
    }
  }, [isFullscreen, updateSize])

  // Component unmount cleanup ensures scroll is never permanently locked
  useEffect(() => {
    return () => {
      document.body.style.overflow = originalBodyOverflow.current
      document.documentElement.style.overflow = originalHtmlOverflow.current
    }
  }, [])

  // Lookup paper counts from countryStats API
  const paperCountMap = useMemo(() => {
    const map: Record<string, number> = {}
    if (countryStats?.countries) {
      countryStats.countries.forEach((c) => {
        map[c.country] = c.frequency
      })
    } else if (countryData?.nodes) {
      countryData.nodes.forEach((n) => {
        map[n.id] = n.paper_count
      })
    }
    return map
  }, [countryStats, countryData])

  // Max paper count for node sizing scale
  const maxPaperCount = useMemo(() => {
    const vals = Object.values(paperCountMap)
    return vals.length ? Math.max(...vals, 1) : 1
  }, [paperCountMap])

  // Helper to compute node radius smoothly
  const getNodeRadius = useCallback(
    (node: any) => {
      const count = paperCountMap[node.id] || node.paperCount || 1
      const normCount = Math.log(count + 1) / Math.log(maxPaperCount + 1)
      return Math.max(6, Math.min(22, 6 + normCount * 16))
    },
    [paperCountMap, maxPaperCount]
  )

  // Calculate collaboration thresholds for filter modes
  const { mediumThreshold, strongThreshold } = useMemo(() => {
    if (!countryData?.links || !countryData.links.length) {
      return { mediumThreshold: 2, strongThreshold: 5 }
    }
    const weights = countryData.links.map((l) => l.weight).sort((a, b) => a - b)
    const maxW = weights[weights.length - 1]
    if (maxW <= 2) {
      return { mediumThreshold: 2, strongThreshold: 2 }
    }
    const p50 = weights[Math.floor(weights.length * 0.5)] || 2
    const p75 = weights[Math.floor(weights.length * 0.75)] || 4
    return {
      mediumThreshold: Math.max(2, p50),
      strongThreshold: Math.max(3, p75),
    }
  }, [countryData])

  // Process raw links & nodes according to active filterMode
  const { processedNodes, processedLinks, topCollaborations, neighborMap, nodeDegreeMap } = useMemo(() => {
    if (!countryData?.nodes || !countryData.nodes.length) {
      return {
        processedNodes: [],
        processedLinks: [],
        topCollaborations: [],
        neighborMap: new Map<string, Set<string>>(),
        nodeDegreeMap: new Map<string, number>(),
      }
    }

    // Filter links based on current strength filter
    let cutoff = 1
    if (filterMode === 'medium') cutoff = mediumThreshold
    if (filterMode === 'strong') cutoff = strongThreshold

    const validLinks = countryData.links.filter((l) => l.weight >= cutoff)

    // Build degree map and neighbor sets
    const neighbors = new Map<string, Set<string>>()
    const degrees = new Map<string, number>()

    validLinks.forEach((link) => {
      const s = typeof link.source === 'object' ? (link.source as any).id : link.source
      const t = typeof link.target === 'object' ? (link.target as any).id : link.target

      if (!neighbors.has(s)) neighbors.set(s, new Set())
      if (!neighbors.has(t)) neighbors.set(t, new Set())
      neighbors.get(s)!.add(t)
      neighbors.get(t)!.add(s)

      degrees.set(s, (degrees.get(s) || 0) + 1)
      degrees.set(t, (degrees.get(t) || 0) + 1)
    })

    // Filter nodes to include only connected nodes in medium/strong modes, or all nodes if 'all'
    const connectedNodeIds = new Set<string>()
    validLinks.forEach((l) => {
      connectedNodeIds.add(typeof l.source === 'object' ? (l.source as any).id : l.source)
      connectedNodeIds.add(typeof l.target === 'object' ? (l.target as any).id : l.target)
    })

    const rawNodes = countryData.nodes.filter((n) => filterMode === 'all' || connectedNodeIds.has(n.id))

    const nodes: GraphNode[] = rawNodes.map((n) => ({
      id: n.id,
      label: n.label || n.id,
      paperCount: paperCountMap[n.id] || n.paper_count || 1,
      collabCount: degrees.get(n.id) || 0,
      iso_a3: n.iso_a3,
    }))

    const links: GraphLink[] = validLinks.map((l) => ({
      source: typeof l.source === 'object' ? (l.source as any).id : l.source,
      target: typeof l.target === 'object' ? (l.target as any).id : l.target,
      weight: l.weight,
    }))

    // Top collaborations sorted by weight
    const sortedCollabs = [...countryData.links]
      .sort((a, b) => b.weight - a.weight)
      .slice(0, 10)
      .map((l) => ({
        source: typeof l.source === 'object' ? (l.source as any).id : l.source,
        target: typeof l.target === 'object' ? (l.target as any).id : l.target,
        weight: l.weight,
      }))

    return {
      processedNodes: nodes,
      processedLinks: links,
      topCollaborations: sortedCollabs,
      neighborMap: neighbors,
      nodeDegreeMap: degrees,
    }
  }, [countryData, paperCountMap, filterMode, mediumThreshold, strongThreshold])

  // Top 5 publication countries for permanent clean labels
  const topCountryIds = useMemo(() => {
    const sorted = [...processedNodes].sort((a, b) => b.paperCount - a.paperCount)
    return new Set(sorted.slice(0, 5).map((n) => n.id))
  }, [processedNodes])

  // Configure D3 force physics to keep nodes bounded and gracefully stabilized
  useEffect(() => {
    if (!fgRef.current) return
    const fg = fgRef.current

    // 1. Distance-capped many-body repulsion
    const maxRepulsionDist = Math.max(180, Math.min(dimensions.width, dimensions.height) * 0.45)
    fg.d3Force('charge')
      ?.strength((node: any) => {
        const deg = nodeDegreeMap.get(node.id) || 0
        return deg === 0 ? -40 : -140
      })
      ?.distanceMax(maxRepulsionDist)

    // 2. Link force with dynamic distance inversely related to collaboration weight
    fg.d3Force('link')
      ?.distance((link: any) => {
        const w = link.weight || 1
        return Math.max(50, 110 - Math.min(50, w * 6))
      })
      ?.strength((link: any) => {
        const w = link.weight || 1
        return Math.min(1, 0.3 + (w / 10) * 0.4)
      })

    // 3. Center gravity force
    fg.d3Force('center')?.strength(0.6)

    // 4. Custom collision force to prevent overlapping nodes
    const collisionForce = (extraPadding = 8) => {
      let nodes: any[] = []
      const force = () => {
        for (let i = 0; i < nodes.length; i++) {
          const a = nodes[i]
          if (!Number.isFinite(a.x) || !Number.isFinite(a.y)) continue
          const rA = getNodeRadius(a) + extraPadding
          for (let j = i + 1; j < nodes.length; j++) {
            const b = nodes[j]
            if (!Number.isFinite(b.x) || !Number.isFinite(b.y)) continue
            const rB = getNodeRadius(b) + extraPadding
            const dx = b.x - a.x
            const dy = b.y - a.y
            const dist = Math.hypot(dx, dy)
            const minDist = rA + rB
            if (dist < minDist && dist > 0) {
              const overlap = ((minDist - dist) / dist) * 0.4
              a.x -= dx * overlap
              a.y -= dy * overlap
              b.x += dx * overlap
              b.y += dy * overlap
            }
          }
        }
      }
      force.initialize = (_nodes: any[]) => {
        nodes = _nodes
      }
      return force
    }
    fg.d3Force('collide', collisionForce())

    // 5. Container boundary constraint force to stop endless drifting
    const boundaryForce = () => {
      let nodes: any[] = []
      const force = () => {
        const padding = 36
        const maxRx = Math.max(120, dimensions.width / 2 - padding)
        const maxRy = Math.max(120, dimensions.height / 2 - padding)
        for (const n of nodes) {
          if (!Number.isFinite(n.x) || !Number.isFinite(n.y)) continue
          const normX = n.x / maxRx
          const normY = n.y / maxRy
          const distSq = normX * normX + normY * normY
          if (distSq > 1) {
            const dist = Math.sqrt(distSq)
            n.x = (normX / dist) * maxRx
            n.y = (normY / dist) * maxRy
            if (n.vx) n.vx *= 0.2
            if (n.vy) n.vy *= 0.2
          }
        }
      }
      force.initialize = (_nodes: any[]) => {
        nodes = _nodes
      }
      return force
    }
    fg.d3Force('boundary', boundaryForce())

    fg.d3ReheatSimulation()
  }, [processedNodes, processedLinks, dimensions.width, dimensions.height, nodeDegreeMap, getNodeRadius])

  // Engine stop handler to ensure cleanly framed layout
  const handleEngineStop = useCallback(() => {
    if (fgRef.current && processedNodes.length > 0 && !activeNodeId) {
      fgRef.current.zoomToFit(400, 45)
    }
  }, [processedNodes.length, activeNodeId])

  // Selection & focus helper
  const handleSelectNode = useCallback(
    (nodeId: string | null) => {
      setActiveNodeId(nodeId)
      if (onSelectCountry) onSelectCountry(nodeId)

      if (nodeId && fgRef.current) {
        const node = processedNodes.find((n) => n.id === nodeId)
        if (node && node.x !== undefined && node.y !== undefined) {
          fgRef.current.centerAt(node.x, node.y, 500)
          fgRef.current.zoom(2.0, 500)
        }
      }
    },
    [onSelectCountry, processedNodes]
  )

  // Search submit handler
  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!searchQuery.trim()) return
    const q = searchQuery.toLowerCase().trim()
    const match = processedNodes.find(
      (n) => n.id.toLowerCase().includes(q) || n.label.toLowerCase().includes(q)
    )
    if (match) {
      handleSelectNode(match.id)
    } else {
      toast.error(`No country matching "${searchQuery}" found in active graph.`)
    }
  }

  // Reset view handler
  const handleReset = useCallback(() => {
    setActiveNodeId(null)
    setSearchQuery('')
    setFilterMode('all')
    if (onSelectCountry) onSelectCountry(null)
    if (fgRef.current && processedNodes.length > 0) {
      fgRef.current.zoomToFit(500, 45)
    }
  }, [onSelectCountry, processedNodes.length])

  // Zoom controls
  const handleZoomIn = () => {
    if (fgRef.current) {
      fgRef.current.zoom(fgRef.current.zoom() * 1.3, 300)
    }
  }
  const handleZoomOut = () => {
    if (fgRef.current) {
      fgRef.current.zoom(fgRef.current.zoom() / 1.3, 300)
    }
  }

  // Export CSV Handler
  const handleDownloadCSV = () => {
    if (!countryData?.links || countryData.links.length === 0) {
      toast.error('No country collaboration data available to export.')
      return
    }

    const headers = [
      'Source Country',
      'Source ISO_A3',
      'Source Paper Count',
      'Target Country',
      'Target ISO_A3',
      'Target Paper Count',
      'Collaboration Weight',
    ]

    const nodeMap = new Map<string, { iso_a3?: string; paperCount: number }>()
    if (countryData.nodes) {
      countryData.nodes.forEach((n) => {
        nodeMap.set(n.id, {
          iso_a3: n.iso_a3,
          paperCount: paperCountMap[n.id] || n.paper_count || 0,
        })
      })
    }

    const escapeCsv = (val: any) => `"${String(val ?? '').replace(/"/g, '""')}"`

    const rows = countryData.links.map((link) => {
      const sId = typeof link.source === 'object' ? (link.source as any).id : link.source
      const tId = typeof link.target === 'object' ? (link.target as any).id : link.target
      const sNode = nodeMap.get(sId)
      const tNode = nodeMap.get(tId)

      return [
        escapeCsv(sId),
        escapeCsv(sNode?.iso_a3 || ''),
        sNode?.paperCount ?? (paperCountMap[sId] || ''),
        escapeCsv(tId),
        escapeCsv(tNode?.iso_a3 || ''),
        tNode?.paperCount ?? (paperCountMap[tId] || ''),
        link.weight || 1,
      ]
    })

    const csvContent = [headers.join(','), ...rows.map((r) => r.join(','))].join('\n')
    const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    const filename = downloadBase
      ? `${downloadBase}_country_collaboration.csv`
      : 'research_rover_country_collaboration.csv'
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    toast.success(`Exported ${rows.length} collaboration links to ${filename}`)
  }

  // Precise pointer hit-test area paint
  const paintNodePointerArea = useCallback(
    (node: any, color: string, ctx: CanvasRenderingContext2D) => {
      if (!node || !Number.isFinite(node.x) || !Number.isFinite(node.y)) return
      const radius = getNodeRadius(node)
      ctx.fillStyle = color
      ctx.beginPath()
      ctx.arc(node.x, node.y, radius + 4, 0, 2 * Math.PI)
      ctx.fill()
    },
    [getNodeRadius]
  )

  // Custom node canvas rendering: clean circles with selective label drawing
  const drawNode = useCallback(
    (node: any, ctx: CanvasRenderingContext2D, globalScale: number) => {
      if (!node || !Number.isFinite(node.x) || !Number.isFinite(node.y)) return

      const isSelected = activeNodeId === node.id
      const isHovered = hoveredNodeId === node.id
      const isNeighbor = activeNodeId ? neighborMap.get(activeNodeId)?.has(node.id) : false
      const isFaded = Boolean(activeNodeId && !isSelected && !isNeighbor)

      const radius = getNodeRadius(node)
      const opacity = isFaded ? 0.18 : 1.0

      ctx.save()
      ctx.globalAlpha = opacity

      // Outer Selection Glow / Highlight Ring
      if (isSelected) {
        ctx.beginPath()
        ctx.arc(node.x, node.y, radius + 6, 0, 2 * Math.PI)
        ctx.fillStyle = 'rgba(56, 189, 248, 0.25)'
        ctx.fill()
        ctx.lineWidth = 2.5 / globalScale
        ctx.strokeStyle = '#38bdf8'
        ctx.stroke()
      } else if (isHovered || isNeighbor) {
        ctx.beginPath()
        ctx.arc(node.x, node.y, radius + 3, 0, 2 * Math.PI)
        ctx.strokeStyle = isHovered ? '#38bdf8' : 'rgba(52, 211, 153, 0.8)'
        ctx.lineWidth = 2 / globalScale
        ctx.stroke()
      }

      // Main Circle Fill with subtle Radial Gradient
      ctx.beginPath()
      ctx.arc(node.x, node.y, radius, 0, 2 * Math.PI)
      const grad = ctx.createRadialGradient(
        node.x - radius * 0.3,
        node.y - radius * 0.3,
        radius * 0.1,
        node.x,
        node.y,
        radius
      )
      if (isSelected) {
        grad.addColorStop(0, '#38bdf8')
        grad.addColorStop(1, '#0284c7')
      } else if (isNeighbor) {
        grad.addColorStop(0, '#34d399')
        grad.addColorStop(1, '#059669')
      } else {
        grad.addColorStop(0, '#60a5fa')
        grad.addColorStop(1, '#2563eb')
      }
      ctx.fillStyle = grad
      ctx.fill()
      ctx.lineWidth = 1.2 / globalScale
      ctx.strokeStyle = '#ffffff'
      ctx.stroke()

      // Selective Label Rendering
      const shouldDrawLabel =
        isSelected ||
        isHovered ||
        isNeighbor ||
        topCountryIds.has(node.id) ||
        globalScale >= 1.5

      if (shouldDrawLabel && !isFaded) {
        const fontSize = Math.max(10, Math.min(13, 11 / globalScale))
        ctx.font = `${isSelected || isHovered ? '600' : '500'} ${fontSize}px Inter, sans-serif`
        const text = node.label || node.id || ''
        const textWidth = ctx.measureText(text).width
        const textY = node.y + radius + fontSize + 2

        // Label background pill for readability
        ctx.fillStyle = isSelected
          ? 'rgba(14, 165, 233, 0.95)'
          : isHovered
          ? 'rgba(15, 23, 42, 0.92)'
          : isNeighbor
          ? 'rgba(5, 150, 105, 0.9)'
          : 'rgba(15, 23, 42, 0.75)'
        ctx.fillRect(
          node.x - textWidth / 2 - 4,
          textY - fontSize + 2,
          textWidth + 8,
          fontSize + 3
        )

        ctx.fillStyle = '#ffffff'
        ctx.textAlign = 'center'
        ctx.textBaseline = 'alphabetic'
        ctx.fillText(text, node.x, textY)
      }

      ctx.restore()
    },
    [activeNodeId, hoveredNodeId, neighborMap, getNodeRadius, topCountryIds]
  )

  // Custom link canvas rendering: thickness by weight, selective fading
  const drawLink = useCallback(
    (link: any, ctx: CanvasRenderingContext2D, globalScale: number) => {
      if (
        !link ||
        !link.source ||
        !link.target ||
        !Number.isFinite(link.source.x) ||
        !Number.isFinite(link.source.y) ||
        !Number.isFinite(link.target.x) ||
        !Number.isFinite(link.target.y)
      ) {
        return
      }

      const sId = typeof link.source === 'object' ? link.source.id : link.source
      const tId = typeof link.target === 'object' ? link.target.id : link.target

      const isConnectedToActive = activeNodeId && (sId === activeNodeId || tId === activeNodeId)
      const isConnectedToHover = hoveredNodeId && (sId === hoveredNodeId || tId === hoveredNodeId)
      const isFaded = activeNodeId ? !isConnectedToActive : false

      const weight = link.weight || 1
      const strokeWidth = Math.max(1, Math.min(5, 1 + Math.log2(weight))) / globalScale

      ctx.save()
      ctx.beginPath()
      ctx.moveTo(link.source.x, link.source.y)
      ctx.lineTo(link.target.x, link.target.y)

      if (isConnectedToActive || isConnectedToHover) {
        ctx.strokeStyle = '#38bdf8'
        ctx.globalAlpha = 0.95
        ctx.lineWidth = strokeWidth * 1.6
      } else if (isFaded) {
        ctx.strokeStyle = '#64748b'
        ctx.globalAlpha = 0.06
        ctx.lineWidth = strokeWidth * 0.7
      } else {
        const alpha = Math.min(0.65, 0.2 + (weight / 20) * 0.4)
        ctx.strokeStyle = '#94a3b8'
        ctx.globalAlpha = alpha
        ctx.lineWidth = strokeWidth
      }

      ctx.stroke()
      ctx.restore()
    },
    [activeNodeId, hoveredNodeId]
  )

  // Selected country details helper for stats display
  const selectedNodeInfo = useMemo(() => {
    if (!activeNodeId) return null
    const node = processedNodes.find((n) => n.id === activeNodeId)
    const neighbors = neighborMap.get(activeNodeId)
    const collabCount = neighbors ? neighbors.size : 0
    return {
      name: activeNodeId,
      papers: node?.paperCount || paperCountMap[activeNodeId] || 0,
      collabCount,
    }
  }, [activeNodeId, processedNodes, neighborMap, paperCountMap])

  // Strongest collaboration pair in entire dataset
  const strongestPair = useMemo(() => {
    if (!topCollaborations.length) return null
    return topCollaborations[0]
  }, [topCollaborations])

  return (
    <div
      className={
        isFullscreen
          ? 'fixed inset-0 z-50 flex flex-col bg-slate-950 text-slate-100 w-full h-full overflow-hidden'
          : 'flex flex-col rounded-2xl border border-gray-200 dark:border-slate-800/60 bg-white dark:bg-slate-900 shadow-sm overflow-hidden w-full max-w-full'
      }
    >
      {/* ── 1. Statistics & Actions Header ── */}
      <div
        className={`flex flex-wrap items-center justify-between gap-4 border-b border-gray-200 dark:border-slate-800/60 px-6 py-4 ${
          isFullscreen ? 'bg-slate-900/90' : 'bg-gray-50/50 dark:bg-slate-900/50'
        }`}
      >
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-sky-500/20 bg-sky-500/10 text-sky-500">
            <GlobeAltIcon className="h-5 w-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-gray-900 dark:text-slate-100">
              International Country Collaboration Network
            </h3>
            <p className="text-xs text-gray-500 dark:text-slate-400">
              Co-authorship frequency graph across research papers
            </p>
          </div>
        </div>

        {/* Compact Metrics Banner & Global Action Controls */}
        <div className="flex flex-wrap items-center gap-3 text-xs">
          <div className="rounded-xl border border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 px-3 py-1.5 shadow-2xs">
            <span className="text-gray-400 dark:text-slate-500">Countries: </span>
            <span className="font-bold text-gray-900 dark:text-slate-100">
              {processedNodes.length}
            </span>
          </div>

          <div className="rounded-xl border border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 px-3 py-1.5 shadow-2xs">
            <span className="text-gray-400 dark:text-slate-500">Visible Links: </span>
            <span className="font-bold text-sky-600 dark:text-sky-400">
              {processedLinks.length}
            </span>
          </div>

          {strongestPair && (
            <div className="rounded-xl border border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 px-3 py-1.5 shadow-2xs hidden md:block">
              <span className="text-gray-400 dark:text-slate-500">Strongest Pair: </span>
              <span className="font-bold text-emerald-600 dark:text-emerald-400">
                {strongestPair.source} ↔ {strongestPair.target} ({strongestPair.weight})
              </span>
            </div>
          )}

          {/* Download CSV Button */}
          <button
            type="button"
            onClick={handleDownloadCSV}
            className="flex items-center gap-1.5 rounded-xl border border-sky-500/30 bg-sky-500/10 hover:bg-sky-500/20 text-sky-600 dark:text-sky-400 px-3 py-1.5 text-xs font-semibold transition"
            title="Download collaboration network as CSV"
          >
            <ArrowDownTrayIcon className="h-3.5 w-3.5" />
            Export CSV
          </button>

          {/* Fullscreen Button */}
          <button
            type="button"
            onClick={() => setIsFullscreen((prev) => !prev)}
            className={`flex items-center gap-1.5 rounded-xl border px-3 py-1.5 text-xs font-semibold transition ${
              isFullscreen
                ? 'border-sky-500 bg-sky-500/20 text-sky-300 hover:bg-sky-500/30'
                : 'border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-800 text-gray-700 dark:text-slate-200 hover:bg-gray-50 dark:hover:bg-slate-700'
            }`}
            title={isFullscreen ? 'Exit Fullscreen (Esc)' : 'Expand Fullscreen'}
          >
            {isFullscreen ? (
              <>
                <ArrowsPointingInIcon className="h-3.5 w-3.5 text-sky-400" />
                Exit Fullscreen
              </>
            ) : (
              <>
                <ArrowsPointingOutIcon className="h-3.5 w-3.5" />
                Fullscreen
              </>
            )}
          </button>
        </div>
      </div>

      {/* ── 2. Controls Row: Search, Filters & Reset ── */}
      <div
        className={`flex flex-wrap items-center justify-between gap-3 border-b border-gray-200 dark:border-slate-800/60 px-6 py-3 ${
          isFullscreen ? 'bg-slate-900' : 'bg-white dark:bg-slate-900'
        }`}
      >
        {/* Search Input Box */}
        <form onSubmit={handleSearchSubmit} className="relative flex-1 min-w-[200px] max-w-md">
          <MagnifyingGlassIcon className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search country (e.g. United States, India, Germany)..."
            className="w-full rounded-xl border border-gray-200 dark:border-slate-800 bg-gray-50 dark:bg-slate-800/50 pl-9 pr-8 py-1.5 text-xs text-gray-900 dark:text-slate-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-sky-500"
          />
          {searchQuery && (
            <button
              type="button"
              onClick={() => setSearchQuery('')}
              className="absolute right-2.5 top-1/2 -translate-y-1/2 text-xs text-gray-400 hover:text-gray-600 dark:hover:text-slate-200"
            >
              ×
            </button>
          )}
        </form>

        {/* Filter & Reset Controls */}
        <div className="flex flex-wrap items-center gap-2">
          <div className="flex items-center gap-1 rounded-xl border border-gray-200 dark:border-slate-800 bg-gray-50 dark:bg-slate-800/50 p-1">
            <span className="px-2 text-[11px] font-semibold text-gray-400 dark:text-slate-500 flex items-center gap-1">
              <FunnelIcon className="h-3 w-3" /> Filter:
            </span>
            {(['all', 'medium', 'strong'] as FilterMode[]).map((mode) => (
              <button
                key={mode}
                type="button"
                onClick={() => setFilterMode(mode)}
                className={`rounded-lg px-2.5 py-1 text-xs font-semibold capitalize transition ${
                  filterMode === mode
                    ? 'bg-white dark:bg-slate-700 text-sky-600 dark:text-sky-400 shadow-2xs'
                    : 'text-gray-500 dark:text-slate-400 hover:text-gray-900 dark:hover:text-slate-200'
                }`}
              >
                {mode === 'all'
                  ? 'All'
                  : mode === 'medium'
                  ? `Medium+ (≥${mediumThreshold})`
                  : `Strong (≥${strongThreshold})`}
              </button>
            ))}
          </div>

          <button
            type="button"
            onClick={handleReset}
            className="flex items-center gap-1.5 rounded-xl border border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-800 px-3 py-1.5 text-xs font-semibold text-gray-600 dark:text-slate-300 hover:bg-gray-50 dark:hover:bg-slate-700 transition"
            title="Reset filters, zoom and selection"
          >
            <ArrowPathIcon className="h-3.5 w-3.5" />
            Reset View
          </button>
        </div>
      </div>

      {/* ── 3. Main Network Canvas & Sidebar Area ── */}
      <div
        className={
          isFullscreen
            ? 'relative flex flex-col lg:flex-row w-full flex-1 min-h-0 overflow-hidden'
            : 'relative flex flex-col xl:flex-row w-full min-h-[520px] max-w-full overflow-hidden'
        }
      >
        {/* Network Canvas Container */}
        <div
          ref={containerRef}
          className={`relative flex-1 min-w-0 bg-slate-950 cursor-grab active:cursor-grabbing overflow-hidden max-w-full ${
            isFullscreen ? 'h-full min-h-0' : 'min-h-[500px] h-[520px] xl:h-[580px]'
          }`}
        >
          {processedNodes.length > 0 ? (
            <div className="absolute inset-0 overflow-hidden">
              <ForceGraph2D
                ref={fgRef}
                width={dimensions.width}
                height={dimensions.height}
                graphData={{ nodes: processedNodes, links: processedLinks }}
                nodeCanvasObject={drawNode}
                linkCanvasObject={drawLink}
                nodePointerAreaPaint={paintNodePointerArea}
                nodeRelSize={6}
                linkWidth={(link: any) => Math.max(1, Math.min(5, link.weight))}
                onNodeClick={(node: any) => handleSelectNode(node.id)}
                onNodeHover={(node: any) => {
                  setHoveredNodeId(node ? node.id : null)
                }}
                onLinkHover={(link: any) => {
                  if (link) {
                    const s = typeof link.source === 'object' ? link.source.id : link.source
                    const t = typeof link.target === 'object' ? link.target.id : link.target
                    setHoveredLink({ source: s, target: t, weight: link.weight })
                  } else {
                    setHoveredLink(null)
                  }
                }}
                warmupTicks={60}
                cooldownTicks={100}
                cooldownTime={2000}
                onEngineStop={handleEngineStop}
                enableZoomInteraction={true}
                enablePanInteraction={true}
                enableNodeDrag={true}
              />
            </div>
          ) : (
            <div className="flex h-full min-h-[400px] flex-col items-center justify-center p-8 text-center text-slate-400">
              <GlobeAltIcon className="mb-3 h-10 w-10 text-slate-600" />
              <p className="text-sm font-semibold">
                No international collaboration data available for this dataset.
              </p>
              <p className="mt-1 text-xs text-slate-500">
                Try selecting another research dataset or adjusting the strength filter.
              </p>
            </div>
          )}

          {/* Floating Zoom & View Controls */}
          <div className="absolute bottom-4 left-4 flex flex-col gap-1 rounded-xl border border-slate-800 bg-slate-900/90 p-1 backdrop-blur-md shadow-lg z-10">
            <button
              type="button"
              onClick={handleZoomIn}
              title="Zoom In"
              className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition"
            >
              <PlusIcon className="h-4 w-4" />
            </button>
            <button
              type="button"
              onClick={handleZoomOut}
              title="Zoom Out"
              className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition"
            >
              <MinusIcon className="h-4 w-4" />
            </button>
            <button
              type="button"
              onClick={handleReset}
              title="Fit View"
              className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition"
            >
              <ArrowPathIcon className="h-4 w-4" />
            </button>
            <button
              type="button"
              onClick={() => setIsFullscreen((prev) => !prev)}
              title={isFullscreen ? 'Exit Fullscreen (Esc)' : 'Open Fullscreen'}
              className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition"
            >
              {isFullscreen ? (
                <ArrowsPointingInIcon className="h-4 w-4 text-sky-400" />
              ) : (
                <ArrowsPointingOutIcon className="h-4 w-4" />
              )}
            </button>
          </div>

          {/* Hover Tooltip Overlay for Nodes */}
          {hoveredNodeId && (
            <div className="absolute top-4 left-4 pointer-events-none z-10 rounded-xl border border-slate-700 bg-slate-900/95 p-3 text-xs text-slate-200 backdrop-blur-md shadow-xl">
              <p className="font-bold text-sky-400 text-sm">{hoveredNodeId}</p>
              <div className="mt-1 space-y-0.5 text-[11px] text-slate-300">
                <p>
                  Publications:{' '}
                  <span className="font-semibold text-white">
                    {(paperCountMap[hoveredNodeId] || 0).toLocaleString()}
                  </span>
                </p>
                <p>
                  Direct Collaborators:{' '}
                  <span className="font-semibold text-emerald-400">
                    {neighborMap.get(hoveredNodeId)?.size || 0} countries
                  </span>
                </p>
              </div>
            </div>
          )}

          {/* Hover Tooltip Overlay for Links */}
          {hoveredLink && !hoveredNodeId && (
            <div className="absolute top-4 left-4 pointer-events-none z-10 rounded-xl border border-slate-700 bg-slate-900/95 p-3 text-xs text-slate-200 backdrop-blur-md shadow-xl">
              <p className="font-bold text-emerald-400">
                {hoveredLink.source} ↔ {hoveredLink.target}
              </p>
              <p className="mt-1 text-[11px] text-slate-300">
                Co-authored Publications:{' '}
                <span className="font-semibold text-white">{hoveredLink.weight}</span>
              </p>
            </div>
          )}
        </div>

        {/* ── 4. Top Collaborations & Country Inspection Sidebar ── */}
        <div
          className={
            isFullscreen
              ? 'w-full lg:w-80 h-full border-t lg:border-t-0 lg:border-l border-slate-800 bg-slate-900/95 p-4 flex flex-col justify-between overflow-y-auto'
              : 'w-full xl:w-72 border-t xl:border-t-0 xl:border-l border-gray-200 dark:border-slate-800/60 bg-gray-50/50 dark:bg-slate-900/50 p-4 flex flex-col justify-between overflow-y-auto max-h-[580px]'
          }
        >
          <div>
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-gray-700 dark:text-slate-300 flex items-center gap-1.5">
                <ShareIcon className="h-4 w-4 text-sky-500" /> Top Collaborations
              </h4>
              <span className="text-[10px] font-semibold text-gray-400 dark:text-slate-500">
                By Weight
              </span>
            </div>

            <div className="space-y-2">
              {topCollaborations.map((collab, idx) => {
                const isPairActive =
                  activeNodeId === collab.source || activeNodeId === collab.target
                return (
                  <button
                    key={`${collab.source}-${collab.target}-${idx}`}
                    type="button"
                    onClick={() => handleSelectNode(collab.source)}
                    className={`w-full text-left p-2.5 rounded-xl border text-xs transition flex items-center justify-between gap-2 ${
                      isPairActive
                        ? 'border-sky-500 bg-sky-50 dark:bg-sky-950/40 text-sky-700 dark:text-sky-300 font-semibold'
                        : 'border-gray-200 dark:border-slate-800/80 bg-white dark:bg-slate-800/60 text-gray-700 dark:text-slate-300 hover:border-sky-300 dark:hover:border-slate-700'
                    }`}
                  >
                    <div className="truncate font-medium">
                      <span>{collab.source}</span>
                      <span className="mx-1 text-gray-400">↔</span>
                      <span>{collab.target}</span>
                    </div>
                    <span className="shrink-0 rounded-md bg-sky-100 dark:bg-sky-900/40 px-2 py-0.5 text-[11px] font-bold text-sky-600 dark:text-sky-400">
                      {collab.weight}
                    </span>
                  </button>
                )
              })}
            </div>
          </div>

          {/* Selected Country Inspection Card */}
          {selectedNodeInfo && (
            <div className="mt-4 rounded-xl border border-sky-500/30 bg-sky-500/10 p-3.5 text-xs text-sky-900 dark:text-sky-100">
              <div className="flex items-center justify-between font-bold mb-1">
                <span>{selectedNodeInfo.name}</span>
                <button
                  type="button"
                  onClick={() => handleSelectNode(null)}
                  className="text-sky-400 hover:text-sky-200 text-sm"
                  title="Clear selection"
                >
                  <XMarkIcon className="h-4 w-4" />
                </button>
              </div>
              <p className="text-[11px] opacity-90">
                Publications:{' '}
                <span className="font-semibold">{selectedNodeInfo.papers.toLocaleString()}</span>
              </p>
              <p className="text-[11px] opacity-90">
                Direct Collaborators:{' '}
                <span className="font-semibold">{selectedNodeInfo.collabCount} countries</span>
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
