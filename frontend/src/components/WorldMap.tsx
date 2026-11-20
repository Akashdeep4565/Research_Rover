import { useMemo, useState } from 'react'
import { ComposableMap, Geographies, Geography, ZoomableGroup } from 'react-simple-maps'
import type { CountryFrequencyItem } from '@/types'

// Path to locally bundled TopoJSON world atlas dataset
const GEO_URL = '/world-110m.json'

// Mapping from ISO 3166-1 numeric 3-digit IDs to ISO 3166-1 alpha-3 string codes
const NUMERIC_TO_ISO3: Record<string, string> = {
  '004': 'AFG', '008': 'ALB', '012': 'DZA', '020': 'AND', '024': 'AGO', '028': 'ATG', '031': 'AZE', '032': 'ARG', '036': 'AUS', '040': 'AUT',
  '044': 'BHS', '048': 'BHR', '050': 'BGD', '051': 'ARM', '052': 'BRB', '056': 'BEL', '064': 'BTN', '068': 'BOL', '070': 'BIH', '072': 'BWA',
  '076': 'BRA', '084': 'BLZ', '090': 'SLB', '096': 'BRN', '100': 'BGR', '104': 'MMR', '108': 'BDI', '112': 'BLR', '116': 'KHM', '120': 'CMR',
  '124': 'CAN', '132': 'CPV', '140': 'CAF', '144': 'LKA', '148': 'TCD', '152': 'CHL', '156': 'CHN', '170': 'COL', '174': 'COM', '178': 'COG',
  '180': 'COD', '188': 'CRI', '191': 'HRV', '192': 'CUB', '196': 'CYP', '203': 'CZE', '204': 'BEN', '208': 'DNK', '212': 'DMA', '214': 'DOM',
  '218': 'ECU', '222': 'SLV', '226': 'GNQ', '231': 'ETH', '232': 'ERI', '233': 'EST', '242': 'FJI', '246': 'FIN', '250': 'FRA', '262': 'DJI',
  '266': 'GAB', '268': 'GEO', '270': 'GMB', '275': 'PSE', '276': 'DEU', '288': 'GHA', '292': 'GIB', '300': 'GRC', '304': 'GRL', '308': 'GRD',
  '320': 'GTM', '324': 'GIN', '328': 'GYA', '332': 'HTI', '340': 'HND', '344': 'HKG', '348': 'HUN', '352': 'ISL', '356': 'IND', '360': 'IDN',
  '364': 'IRN', '368': 'IRQ', '372': 'IRL', '376': 'ISR', '380': 'ITA', '384': 'CIV', '388': 'JAM', '392': 'JPN', '398': 'KAZ', '400': 'JOR',
  '404': 'KEN', '408': 'PRK', '410': 'KOR', '414': 'KWT', '417': 'KGZ', '418': 'LAO', '422': 'LBN', '426': 'LSO', '428': 'LVA', '430': 'LBR',
  '434': 'LBY', '438': 'LIE', '440': 'LTU', '442': 'LUX', '446': 'MAC', '450': 'MDG', '454': 'MWI', '458': 'MYS', '462': 'MDV', '466': 'MLI',
  '470': 'MLT', '478': 'MRT', '480': 'MUS', '484': 'MEX', '492': 'MCO', '496': 'MNG', '498': 'MDA', '499': 'MNE', '504': 'MAR', '508': 'MOZ',
  '512': 'OMN', '516': 'NAM', '520': 'NRU', '524': 'NPL', '528': 'NLD', '548': 'VUT', '554': 'NZL', '558': 'NIC', '562': 'NER', '566': 'NGA',
  '578': 'NOR', '586': 'PAK', '591': 'PAN', '598': 'PNG', '600': 'PRY', '604': 'PER', '608': 'PHL', '616': 'POL', '620': 'PRT', '624': 'GNB',
  '626': 'TLS', '634': 'QAT', '642': 'ROU', '646': 'RWA', '682': 'SAU', '686': 'SEN', '688': 'SRB', '694': 'SLE', '702': 'SGP', '703': 'SVK',
  '704': 'VNM', '705': 'SVN', '706': 'SOM', '710': 'ZAF', '716': 'ZWE', '724': 'ESP', '728': 'SSD', '729': 'SDN', '740': 'SUR', '752': 'SWE',
  '756': 'CHE', '760': 'SYR', '762': 'TJK', '764': 'THA', '768': 'TGO', '780': 'TTO', '784': 'ARE', '788': 'TUN', '792': 'TUR', '795': 'TKM',
  '800': 'UGA', '804': 'UKR', '818': 'EGY', '826': 'GBR', '834': 'TZA', '840': 'USA', '858': 'URY', '860': 'UZB', '862': 'VEN', '887': 'YEM',
  '894': 'ZMB', '158': 'TWN', '643': 'RUS'
}

// Fallback lookup dictionary mapping normalized display names to ISO-3 alpha-3 codes
const NAME_TO_ISO3: Record<string, string> = {
  'united states': 'USA',
  'united states of america': 'USA',
  'usa': 'USA',
  'us': 'USA',
  'india': 'IND',
  'united kingdom': 'GBR',
  'uk': 'GBR',
  'great britain': 'GBR',
  'china': 'CHN',
  'people\'s republic of china': 'CHN',
  'prc': 'CHN',
  'germany': 'DEU',
  'france': 'FRA',
  'japan': 'JPN',
  'canada': 'CAN',
  'australia': 'AUS',
  'brazil': 'BRA',
  'south korea': 'KOR',
  'korea': 'KOR',
  'republic of korea': 'KOR',
  'spain': 'ESP',
  'italy': 'ITA',
  'netherlands': 'NLD',
  'switzerland': 'CHE',
  'sweden': 'SWE',
  'singapore': 'SGP',
  'saudi arabia': 'SAU',
  'south africa': 'ZAF',
  'iran': 'IRN',
  'turkey': 'TUR',
  'israel': 'ISR',
  'egypt': 'EGY',
  'mexico': 'MEX',
  'russia': 'RUS',
  'russian federation': 'RUS',
  'belgium': 'BEL',
  'poland': 'POL',
  'norway': 'NOR',
  'denmark': 'DNK',
  'finland': 'FIN',
  'austria': 'AUT',
  'greece': 'GRC',
  'portugal': 'PRT',
  'ireland': 'IRL',
  'new zealand': 'NZL',
  'pakistan': 'PAK',
  'bangladesh': 'BGD',
  'indonesia': 'IDN',
  'malaysia': 'MYS',
  'thailand': 'THA',
  'vietnam': 'VNM',
  'philippines': 'PHL',
  'taiwan': 'TWN',
  'argentina': 'ARG',
  'chile': 'CHL',
  'colombia': 'COL',
  'nigeria': 'NGA',
  'kenya': 'KEN',
  'united arab emirates': 'ARE',
  'uae': 'ARE',
  'qatar': 'QAT',
  'jordan': 'JOR',
}

interface WorldMapProps {
  countries: CountryFrequencyItem[]
  totalPapers: number
  selectedCountry?: string | null
  onSelectCountry?: (countryName: string) => void
}

interface HoverState {
  countryName: string
  paperCount: number
  percentage: number
  x: number
  y: number
}

export function WorldMap({
  countries,
  totalPapers,
  selectedCountry,
  onSelectCountry,
}: WorldMapProps) {
  const [hoverState, setHoverState] = useState<HoverState | null>(null)

  // Memoize ISO-3 indexed country stats and track unmapped entries
  const { isoDataMap, maxFrequency, unmappedCountries } = useMemo(() => {
    const isoMap: Record<string, CountryFrequencyItem> = {}
    const unmapped: CountryFrequencyItem[] = []
    let maxFreq = 1

    countries.forEach((item) => {
      // 1. Check explicit backend iso_a3 code
      let iso = item.iso_a3?.toUpperCase()

      // 2. Fallback to name-based lookup
      if (!iso) {
        const normName = item.country.trim().toLowerCase()
        iso = NAME_TO_ISO3[normName]
      }

      if (iso) {
        isoMap[iso] = item
        if (item.frequency > maxFreq) {
          maxFreq = item.frequency
        }
      } else {
        unmapped.push(item)
        console.warn(`[WorldMap] Unmapped country name: "${item.country}" (frequency: ${item.frequency})`)
      }
    })

    return { isoDataMap: isoMap, maxFrequency: maxFreq, unmappedCountries: unmapped }
  }, [countries])

  // Get color fill based on actual publication frequency ratio
  const getGeographyFill = (iso3Code: string | null, isSelected: boolean) => {
    if (isSelected) return '#38bdf8' // Highlight selected country

    if (!iso3Code || !isoDataMap[iso3Code] || isoDataMap[iso3Code].frequency === 0) {
      return '#1e293b' // Neutral Slate fill for 0 publications
    }

    const freq = isoDataMap[iso3Code].frequency
    const ratio = Math.min(freq / maxFrequency, 1)

    // Smooth gradient scale suitable for Research Rover dark theme
    if (ratio > 0.70) return '#6366f1' // High (Indigo)
    if (ratio > 0.40) return '#3b82f6' // Medium-High (Blue)
    if (ratio > 0.15) return '#0284c7' // Medium (Sky)
    return '#0d9488' // Low (Teal)
  }

  return (
    <div className="relative w-full rounded-2xl border border-gray-200 dark:border-slate-800 bg-white/70 dark:bg-slate-900/70 p-6 backdrop-blur-md shadow-lg">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-4 gap-3">
        <div>
          <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
            Geographic Research Publication Map
          </h3>
          <p className="text-xs text-gray-500 dark:text-slate-400">
            Real TopoJSON geographic boundaries shaded dynamically by API publication volume
          </p>
        </div>

        {/* Dynamic Legend */}
        <div className="flex items-center gap-3 text-xs text-gray-600 dark:text-gray-300 bg-gray-50 dark:bg-slate-800/60 px-3.5 py-2 rounded-xl border border-gray-200 dark:border-slate-700/80 shadow-sm">
          <span className="font-semibold text-gray-700 dark:text-slate-300">Publication Volume:</span>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded bg-slate-800 border border-slate-700" title="None (0)" />
            <span className="text-[10px] text-gray-500 dark:text-slate-400">None</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded bg-teal-600" title="Low" />
            <span className="w-3 h-3 rounded bg-sky-600" title="Medium" />
            <span className="w-3 h-3 rounded bg-blue-600" title="Medium-High" />
            <span className="w-3 h-3 rounded bg-indigo-600" title="High" />
            <span className="text-[10px] font-semibold text-gray-700 dark:text-slate-300">High</span>
          </div>
        </div>
      </div>

      {/* Composable Real TopoJSON World Map */}
      <div className="relative w-full overflow-hidden rounded-2xl bg-slate-950 p-2 border border-slate-800/90 shadow-inner">
        <ComposableMap
          projection="geoEqualEarth"
          projectionConfig={{ scale: 155 }}
          className="w-full h-auto max-h-[520px]"
        >
          <ZoomableGroup center={[0, 10]} zoom={1} minZoom={1} maxZoom={5}>
            <Geographies geography={GEO_URL}>
              {({ geographies }) =>
                geographies.map((geo) => {
                  const numId = String(geo.id).padStart(3, '0')
                  const geoIso3 = NUMERIC_TO_ISO3[numId] || NAME_TO_ISO3[String(geo.properties?.name || '').toLowerCase()]
                  const geoName = geo.properties?.name || 'Unknown'

                  const dataItem = geoIso3 ? isoDataMap[geoIso3] : undefined
                  const paperCount = dataItem ? dataItem.frequency : 0
                  const pct = dataItem
                    ? dataItem.percentage
                    : totalPapers > 0
                    ? parseFloat(((paperCount / totalPapers) * 100).toFixed(2))
                    : 0

                  const isSelected = Boolean(
                    selectedCountry &&
                    (selectedCountry.toLowerCase() === geoName.toLowerCase() ||
                      (dataItem && dataItem.country.toLowerCase() === selectedCountry.toLowerCase()))
                  )

                  const fillColor = getGeographyFill(geoIso3 || null, isSelected)

                  return (
                    <Geography
                      key={geo.rsmKey}
                      geography={geo}
                      fill={fillColor}
                      stroke="#334155"
                      strokeWidth={0.5}
                      style={{
                        default: { outline: 'none', transition: 'fill 300ms ease' },
                        hover: {
                          fill: paperCount > 0 ? '#38bdf8' : '#475569',
                          stroke: '#ffffff',
                          strokeWidth: 1.2,
                          outline: 'none',
                          cursor: 'pointer',
                        },
                        pressed: { fill: '#0284c7', outline: 'none' },
                      } as any}
                      onMouseEnter={(e) => {
                        const rect = (e.target as SVGPathElement).getBoundingClientRect()
                        setHoverState({
                          countryName: dataItem?.country || geoName,
                          paperCount,
                          percentage: pct,
                          x: rect.left + rect.width / 2,
                          y: rect.top - 8,
                        })
                      }}
                      onMouseLeave={() => setHoverState(null)}
                      onClick={() => {
                        const targetName = dataItem?.country || geoName
                        if (onSelectCountry) onSelectCountry(targetName)
                      }}
                    />
                  )
                })
              }
            </Geographies>
          </ZoomableGroup>
        </ComposableMap>
      </div>

      {/* Floating Hover Tooltip */}
      {hoverState && (
        <div
          className="fixed z-50 pointer-events-none transform -translate-x-1/2 -translate-y-full px-3.5 py-2.5 bg-slate-900/95 border border-sky-500/40 text-white rounded-xl shadow-2xl backdrop-blur-md text-xs space-y-1 min-w-[150px]"
          style={{ left: hoverState.x, top: hoverState.y }}
        >
          <div className="font-bold text-sky-300 border-b border-slate-700/60 pb-1">
            {hoverState.countryName}
          </div>
          <div className="space-y-0.5 pt-1">
            <div className="flex justify-between gap-3 text-slate-200">
              <span>Papers:</span>
              <span className="font-bold text-white">{hoverState.paperCount.toLocaleString()}</span>
            </div>
            <div className="flex justify-between gap-3 text-slate-400">
              <span>Share:</span>
              <span className="font-bold text-emerald-400">{hoverState.percentage}%</span>
            </div>
          </div>
        </div>
      )}

      {/* Unmapped Geographic Regions Section */}
      {unmappedCountries.length > 0 && (
        <div className="mt-4 p-4 rounded-xl bg-slate-100 dark:bg-slate-800/40 border border-gray-200 dark:border-slate-700/60">
          <h4 className="text-xs font-semibold text-gray-700 dark:text-gray-300 mb-2 flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-amber-500" />
            Other Detected Geographic Regions ({unmappedCountries.length})
          </h4>
          <div className="flex flex-wrap gap-2">
            {unmappedCountries.map((item) => (
              <span
                key={item.country}
                className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700 text-xs font-medium text-gray-800 dark:text-gray-200 shadow-sm"
              >
                <span>{item.country}</span>
                <span className="px-1.5 py-0.5 rounded-full bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 text-[10px] font-bold">
                  {item.frequency} {item.frequency === 1 ? 'paper' : 'papers'} ({item.percentage}%)
                </span>
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
