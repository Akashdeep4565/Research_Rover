import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import ForceGraph3D from 'react-force-graph-3d'
import SpriteText from 'three-spritetext'
import * as THREE from 'three'
import {
  GlobeAltIcon,
  ArrowsPointingOutIcon,
  ArrowPathIcon,
  XMarkIcon,
  UserGroupIcon,
  ExclamationTriangleIcon,
} from '@heroicons/react/24/outline'
import type {
  CountryCollaborationGraphResponse,
  CountryStatisticsResponse,
} from '@/types'

interface CountryCollaboration3DProps {
  countryData: CountryCollaborationGraphResponse | null
  countryStats: CountryStatisticsResponse | null
  selectedCountry?: string | null
  onSelectCountry?: (countryName: string) => void
}

interface GraphNode {
  id: string
  label: string
  paperCount: number
  collabCount: number
  val: number
  color: string
}

interface GraphLink {
  source: string | GraphNode
  target: string | GraphNode
  weight: number
  width: number
}

// Helper to safely extract string ID whether source/target is string or mutated node object
function getLinkId(val: any): string {
  if (val === null || val === undefined) return ''
  if (typeof val === 'object') return String(val.id || '')
  return String(val)
}

// Capability check for WebGL support
function checkWebGLSupport(): boolean {
  try {
    const canvas = document.createElement('canvas')
    return Boolean(
      window.WebGLRenderingContext &&
      (canvas.getContext('webgl') || canvas.getContext('experimental-webgl'))
    )
  } catch (e) {
    return false
  }
}

// Color palette matching Research Rover dark UI
const NODE_COLORS = [
  '#38bdf8', '#34d399', '#fb923c', '#a78bfa', '#f472b6',
  '#2dd4bf', '#facc15', '#06b6d4', '#818cf8', '#a3e635',
]

export function CountryCollaboration3D({
  countryData,
  countryStats,
  selectedCountry,
  onSelectCountry,
}: CountryCollaboration3DProps) {
  const fgRef = useRef<any>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  const [dimensions, setDimensions] = useState({ width: 800, height: 500 })
  const [activeNode, setActiveNode] = useState<string | null>(selectedCountry || null)
  const [enableParticles, setEnableParticles] = useState(true)
  const [webGLAvailable] = useState<boolean>(() => checkWebGLSupport())

  // Sync internal activeNode state when external selectedCountry changes
  useEffect(() => {
    if (selectedCountry) {
      setActiveNode(selectedCountry)
    }
  }, [selectedCountry])

  // ResizeObserver to keep 3D graph responsive to container bounds
  useEffect(() => {
    if (!containerRef.current) return
    const updateSize = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.clientWidth || 800,
          height: Math.max(480, Math.min(650, window.innerHeight * 0.55)),
        })
      }
    }
    updateSize()
    const observer = new ResizeObserver(updateSize)
    observer.observe(containerRef.current)
    return () => observer.disconnect()
  }, [])

  // Build lookup for publication counts from primary countryStats API
  const countryPaperCountMap = useMemo(() => {
    const map: Record<string, number> = {}
    if (Array.isArray(countryStats?.countries)) {
      countryStats.countries.forEach((c) => {
        if (c?.country) map[c.country] = c.frequency || 0
      })
    } else if (Array.isArray(countryData?.nodes)) {
      countryData.nodes.forEach((n) => {
        if (n?.id) map[n.id] = n.paper_count || 0
      })
    }
    return map
  }, [countryStats, countryData])

  // Process and format graph nodes & links
  const { graphData, neighborMap } = useMemo(() => {
    const rawNodes = Array.isArray(countryData?.nodes) ? countryData.nodes : []
    const rawLinks = Array.isArray(countryData?.links) ? countryData.links : []

    if (!rawNodes.length) {
      return {
        graphData: { nodes: [], links: [] },
        maxPaperCount: 1,
        maxLinkWeight: 1,
        neighborMap: new Map<string, Set<string>>(),
      }
    }

    const validNodeIds = new Set(rawNodes.map((n) => n.id))

    // 1. Calculate max paper count & max link weight for dynamic scaling
    let maxPapers = 1
    let maxWeight = 1

    const collabCountMap: Record<string, number> = {}
    const neighbors = new Map<string, Set<string>>()

    rawLinks.forEach((l) => {
      const srcId = getLinkId(l.source)
      const tgtId = getLinkId(l.target)
      if (!srcId || !tgtId || !validNodeIds.has(srcId) || !validNodeIds.has(tgtId)) return

      const w = l.weight || 1
      if (w > maxWeight) maxWeight = w

      // Count collaborations per country
      collabCountMap[srcId] = (collabCountMap[srcId] || 0) + w
      collabCountMap[tgtId] = (collabCountMap[tgtId] || 0) + w

      // Track neighbor nodes for click highlighting
      if (!neighbors.has(srcId)) neighbors.set(srcId, new Set())
      if (!neighbors.has(tgtId)) neighbors.set(tgtId, new Set())
      neighbors.get(srcId)!.add(tgtId)
      neighbors.get(tgtId)!.add(srcId)
    })

    rawNodes.forEach((n) => {
      const count = countryPaperCountMap[n.id] || n.paper_count || 1
      if (count > maxPapers) maxPapers = count
    })

    // 2. Format Nodes
    const nodes: GraphNode[] = rawNodes.map((n, i) => {
      const paperCount = countryPaperCountMap[n.id] || n.paper_count || 1
      // Node size scaled dynamically between 4 and 20
      const radiusVal = 4 + (paperCount / maxPapers) * 16
      const color = NODE_COLORS[i % NODE_COLORS.length]

      return {
        id: n.id,
        label: n.label || n.id,
        paperCount,
        collabCount: collabCountMap[n.id] || 0,
        val: radiusVal,
        color,
      }
    })

    // 3. Format Links
    const links: GraphLink[] = rawLinks
      .filter((l) => {
        const s = getLinkId(l.source)
        const t = getLinkId(l.target)
        return s && t && validNodeIds.has(s) && validNodeIds.has(t)
      })
      .map((l) => {
        const w = l.weight || 1
        // Link thickness scaled dynamically between 1.5 and 8
        const width = 1.5 + (w / maxWeight) * 6.5
        return {
          source: getLinkId(l.source),
          target: getLinkId(l.target),
          weight: w,
          width,
        }
      })

    return {
      graphData: { nodes, links },
      maxPaperCount: maxPapers,
      maxLinkWeight: maxWeight,
      neighborMap: neighbors,
    }
  }, [countryData, countryPaperCountMap])

  // Top 5 countries for permanent 3D labels
  const topCountryIds = useMemo(() => {
    if (!graphData.nodes) return new Set<string>()
    const sorted = [...graphData.nodes].sort((a, b) => b.paperCount - a.paperCount)
    return new Set(sorted.slice(0, 5).map((n) => n.id))
  }, [graphData.nodes])

  // Automatically zoom to fit the graph after initialization
  const handleEngineStop = useCallback(() => {
    try {
      if (fgRef.current && typeof fgRef.current.zoomToFit === 'function') {
        fgRef.current.zoomToFit(400, 40)
      }
    } catch (e) {
      console.warn('3D zoomToFit error:', e)
    }
  }, [])

  const resetCamera = useCallback(() => {
    try {
      if (fgRef.current && typeof fgRef.current.zoomToFit === 'function') {
        fgRef.current.zoomToFit(400, 40)
      }
    } catch (e) {
      console.warn('3D resetCamera error:', e)
    }
  }, [])

  // Node click handler with smooth camera transition
  const handleNodeClick = useCallback(
    (node: any) => {
      if (!node) return
      const nodeName = node.id || node.label || ''
      if (!nodeName) return

      setActiveNode((prev) => (prev === nodeName ? null : nodeName))
      if (onSelectCountry) {
        onSelectCountry(nodeName)
      }

      // Smooth camera focus towards clicked node
      if (fgRef.current && node.x !== undefined && typeof fgRef.current.cameraPosition === 'function') {
        const x = Number(node.x) || 0
        const y = Number(node.y) || 0
        const z = Number(node.z) || 0
        const dist = Math.hypot(x, y, z)
        const distRatio = dist > 0 ? 1 + 140 / dist : 1.5

        try {
          fgRef.current.cameraPosition(
            { x: x * distRatio, y: y * distRatio, z: z * distRatio },
            { x, y, z },
            1000
          )
        } catch (e) {
          console.warn('3D cameraPosition error:', e)
        }
      }
    },
    [onSelectCountry]
  )

  // Determine if a node or link should be highlighted during active click selection
  const isNodeHighlighted = (nodeId: string) => {
    if (!activeNode) return true
    if (nodeId === activeNode) return true
    const activeNeighbors = neighborMap.get(activeNode)
    return Boolean(activeNeighbors && activeNeighbors.has(nodeId))
  }

  const isLinkHighlighted = (sourceId: string, targetId: string) => {
    if (!activeNode) return true
    return sourceId === activeNode || targetId === activeNode
  }

  const hasGraphData = Boolean(
    graphData.nodes.length > 0 && graphData.links.length > 0
  )

  return (
    <div className="relative w-full rounded-2xl border border-gray-200 dark:border-slate-800 bg-white/70 dark:bg-slate-900/70 p-6 backdrop-blur-md shadow-lg">
      {/* Header & Controls */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-4 gap-3">
        <div>
          <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2">
            <GlobeAltIcon className="h-5 w-5 text-indigo-500" />
            3D Country Collaboration Network
          </h3>
          <p className="text-xs text-gray-500 dark:text-slate-400">
            Force-directed 3D co-authorship space — drag, rotate, zoom, and click nodes to explore partnerships
          </p>
        </div>

        {/* Legend & Controls */}
        <div className="flex flex-wrap items-center gap-2.5">
          {/* Dynamic Legend */}
          <div className="flex items-center gap-3 text-xs text-gray-600 dark:text-gray-300 bg-gray-50 dark:bg-slate-800/60 px-3 py-1.5 rounded-xl border border-gray-200 dark:border-slate-700/80 shadow-sm">
            <div className="flex items-center gap-1">
              <span className="w-2.5 h-2.5 rounded-full bg-indigo-500" />
              <span className="text-[11px] text-gray-500 dark:text-slate-400">Sphere size = Papers</span>
            </div>
            <span className="text-gray-300 dark:text-slate-700">|</span>
            <div className="flex items-center gap-1">
              <span className="w-4 h-0.5 bg-sky-400 rounded" />
              <span className="text-[11px] text-gray-500 dark:text-slate-400">Thickness = Joint Papers</span>
            </div>
          </div>

          {/* Reset Camera Button */}
          <button
            type="button"
            onClick={resetCamera}
            disabled={!webGLAvailable}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-gray-200 dark:border-slate-700/80 bg-white dark:bg-slate-800 text-xs font-medium text-gray-700 dark:text-slate-300 hover:bg-gray-100 dark:hover:bg-slate-700 transition disabled:opacity-50"
            title="Reset 3D Camera view"
          >
            <ArrowsPointingOutIcon className="h-3.5 w-3.5 text-indigo-400" />
            Reset Camera
          </button>

          {/* Toggle Particles */}
          <button
            type="button"
            onClick={() => setEnableParticles((p) => !p)}
            disabled={!webGLAvailable}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-medium transition disabled:opacity-50 ${
              enableParticles
                ? 'border-indigo-500/40 bg-indigo-500/10 text-indigo-400 font-bold'
                : 'border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-gray-500 dark:text-slate-400'
            }`}
          >
            <ArrowPathIcon className="h-3.5 w-3.5" />
            Particles
          </button>

          {/* Clear Active Selection */}
          {activeNode && (
            <button
              type="button"
              onClick={() => {
                setActiveNode(null)
                if (onSelectCountry) onSelectCountry('')
              }}
              className="flex items-center gap-1 px-2.5 py-1.5 rounded-xl border border-rose-500/30 bg-rose-500/10 text-xs font-medium text-rose-400 hover:bg-rose-500/20 transition"
            >
              <XMarkIcon className="h-3.5 w-3.5" />
              Clear Selection ({activeNode})
            </button>
          )}
        </div>
      </div>

      {/* 3D Canvas / Empty State / WebGL Unavailable Container */}
      <div
        ref={containerRef}
        className="relative w-full overflow-hidden rounded-2xl bg-slate-950 border border-slate-800/90 shadow-2xl flex items-center justify-center min-h-[480px]"
      >
        {!webGLAvailable ? (
          <div className="flex flex-col items-center justify-center p-12 text-center text-slate-400 space-y-3">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl border border-amber-500/30 bg-amber-500/10 text-amber-400 shadow-lg">
              <ExclamationTriangleIcon className="h-7 w-7" />
            </div>
            <h4 className="text-base font-bold text-slate-200">
              3D Collaboration Network
            </h4>
            <p className="max-w-md text-xs text-slate-300 leading-relaxed">
              WebGL is unavailable in this browser/environment.
            </p>
            <p className="text-xs text-slate-500">
              The other Country Analysis visualizations remain available.
            </p>
          </div>
        ) : !hasGraphData ? (
          <div className="flex flex-col items-center justify-center p-12 text-center text-slate-400 space-y-3">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl border border-indigo-500/30 bg-indigo-500/10 text-indigo-400 shadow-lg">
              <UserGroupIcon className="h-7 w-7" />
            </div>
            <h4 className="text-base font-bold text-slate-200">
              No International Collaboration Data
            </h4>
            <p className="max-w-sm text-xs text-slate-400 leading-relaxed">
              No international co-authorship relationships were detected among the papers in this dataset.
            </p>
          </div>
        ) : (
          <ForceGraph3D
            ref={fgRef}
            width={dimensions.width}
            height={dimensions.height}
            graphData={graphData}
            backgroundColor="#090d16"
            nodeLabel={(node: any) => `
              <div style="background: rgba(15, 23, 42, 0.95); border: 1px solid rgba(56, 189, 248, 0.4); padding: 8px 12px; border-radius: 10px; font-family: sans-serif; font-size: 12px; color: #fff; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
                <div style="font-weight: bold; color: #38bdf8; margin-bottom: 4px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 3px;">
                  ${node.label || node.id || ''}
                </div>
                <div>Publications: <b style="color: #fff;">${node.paperCount || 0}</b></div>
                <div>International collaborations: <b style="color: #34d399;">${node.collabCount || 0}</b></div>
              </div>
            `}
            nodeVal={(node: any) => node.val || 4}
            nodeColor={(node: any) => {
              if (!isNodeHighlighted(node.id)) return '#1e293b'
              if (activeNode === node.id) return '#38bdf8'
              return node.color || '#38bdf8'
            }}
            nodeOpacity={0.95}
            nodeResolution={16}
            nodeThreeObjectExtend={true}
            nodeThreeObject={(node: any) => {
              const isSelected = activeNode === node.id
              const isNeighbor = activeNode ? neighborMap.get(activeNode)?.has(node.id) : false
              const isTopCountry = topCountryIds.has(node.id)

              // Returning a valid empty THREE Object3D instead of null prevents
              // three-forcegraph from crashing on null.position reference!
              if (!isSelected && !isNeighbor && !isTopCountry) {
                return new THREE.Group()
              }

              try {
                const labelText = node.label || node.id || ''
                const sprite = new SpriteText(labelText)
                const isDimmed = !isNodeHighlighted(node.id)

                sprite.color = isSelected ? '#38bdf8' : isDimmed ? '#64748b' : '#ffffff'
                sprite.textHeight = isSelected ? 5.5 : 4
                sprite.backgroundColor = isSelected
                  ? 'rgba(14, 165, 233, 0.25)'
                  : isDimmed
                  ? 'rgba(15, 23, 42, 0.3)'
                  : 'rgba(15, 23, 42, 0.8)'
                sprite.padding = [2, 4]
                sprite.borderWidth = 0.5
                sprite.borderColor = isSelected ? '#38bdf8' : node.color || 'rgba(148, 163, 184, 0.4)'
                sprite.borderRadius = 4

                const sphereRadius = node.val || 6
                sprite.position.set(0, sphereRadius + 3.5, 0)
                return sprite
              } catch (e) {
                console.warn('SpriteText creation failed for node:', node.id, e)
                return new THREE.Group()
              }
            }}
            linkLabel={(link: any) => {
              const srcName = getLinkId(link.source)
              const tgtName = getLinkId(link.target)
              return `
                <div style="background: rgba(15, 23, 42, 0.95); border: 1px solid rgba(168, 85, 247, 0.4); padding: 8px 12px; border-radius: 10px; font-family: sans-serif; font-size: 12px; color: #fff; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
                  <div style="font-weight: bold; color: #c084fc; margin-bottom: 4px;">
                    ${srcName} ↔ ${tgtName}
                  </div>
                  <div>Collaborations: <b style="color: #38bdf8;">${link.weight || 1} joint ${(link.weight || 1) === 1 ? 'paper' : 'papers'}</b></div>
                </div>
              `
            }}
            linkWidth={(link: any) => {
              const srcId = getLinkId(link.source)
              const tgtId = getLinkId(link.target)
              if (!isLinkHighlighted(srcId, tgtId)) return 0.5
              return link.width || 1
            }}
            linkColor={(link: any) => {
              const srcId = getLinkId(link.source)
              const tgtId = getLinkId(link.target)
              if (!isLinkHighlighted(srcId, tgtId)) return '#1e293b'
              return '#38bdf8'
            }}
            linkOpacity={0.6}
            linkDirectionalParticles={enableParticles ? (link: any) => ((link.weight || 1) > 1 ? 2 : 1) : 0}
            linkDirectionalParticleWidth={(link: any) => Math.min((link.width || 1) * 0.6, 4)}
            linkDirectionalParticleSpeed={0.006}
            linkDirectionalParticleColor={() => '#38bdf8'}
            onNodeClick={handleNodeClick}
            onEngineStop={handleEngineStop}
          />
        )}

        {/* Selected Country Active Card Overlay */}
        {activeNode && (
          <div className="absolute top-4 left-4 z-10 px-4 py-3 bg-slate-900/90 border border-sky-500/40 text-white rounded-xl shadow-2xl backdrop-blur-md text-xs space-y-1">
            <div className="font-bold text-sky-400 text-sm flex items-center justify-between gap-3">
              <span>{activeNode}</span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-sky-500/20 text-sky-300 font-mono">
                Active Selection
              </span>
            </div>
            <div className="text-slate-300">
              Publications: <strong className="text-white">{countryPaperCountMap[activeNode] || 0}</strong>
            </div>
            <div className="text-slate-300">
              Partners: <strong className="text-emerald-400">{neighborMap.get(activeNode)?.size || 0} nations</strong>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
