import { useState, useRef, useEffect, useCallback } from 'react'
import AiGeneratedBadge from './shared/AiGeneratedBadge'
import ContextTooltip from './shared/ContextTooltip'
import DetailModal from './shared/DetailModal'
import { getCssVar } from '../lib/themeColors'

const SCATTER_TOOLTIP = "Each dot represents a political position. The horizontal axis shows where you stand (against to for). The vertical axis shows how much you care (barely think about it to defining issue). Positions in the top-right are your strongest held beliefs. Positions in the bottom half are opinions you hold but wouldn't organize around. This matters for coalition building: you can work with someone who disagrees with you on a bottom-half issue because neither of you cares enough to fight about it. Dots marked ✦ are inferred from conversations and have not been explicitly confirmed through the questionnaire."

const DOMAIN_COLORS = {
  'Housing & Land Use': '#22c55e',
  'Transportation': '#3b82f6',
  'Taxation & Finance': '#f59e0b',
  'Public Safety': '#ef4444',
  'Climate & Energy': '#06b6d4',
  'Family & Abundance': '#ec4899',
  'Democracy & Governance': '#a855f7',
  'Technology': '#6366f1',
  'Reproductive Rights': '#f97316',
  'Civil Rights': '#f97316',
  'Immigration': '#14b8a6',
  'Guns': '#78716c',
  'Foreign Policy': '#64748b',
  'Criminal Justice': '#d946ef',
  'Economics': '#eab308',
  'Education': '#84cc16',
  'Healthcare': '#e11d48',
  'Government Transparency': '#a855f7',
}

const FALLBACK_COLOR = '#94a3b8'

function getDomainColor(domain) {
  return DOMAIN_COLORS[domain] || FALLBACK_COLOR
}

function getUniqueDomains(positions) {
  const seen = new Set()
  const domains = []
  for (const p of positions) {
    if (!seen.has(p.domain)) {
      seen.add(p.domain)
      domains.push(p.domain)
    }
  }
  return domains
}

function formatPosition(value) {
  const abs = Math.abs(value)
  if (abs >= 0.8) return value > 0 ? 'Strongly For' : 'Strongly Against'
  if (abs >= 0.5) return value > 0 ? 'For' : 'Against'
  if (abs >= 0.2) return value > 0 ? 'Leaning For' : 'Leaning Against'
  return 'Neutral'
}

function formatImportance(value) {
  const labels = { 1: "Don't Care", 2: 'Low Priority', 3: 'Moderate', 4: 'High Priority', 5: 'Defining Issue' }
  return labels[value] || `${value}/5`
}

// SVG coordinate mapping
function mapX(position, width, padding) {
  return padding + ((position + 1) / 2) * (width - 2 * padding)
}

function mapY(importance, height, padding) {
  // importance 1 = bottom, 5 = top
  return height - padding - ((importance - 1) / 4) * (height - 2 * padding)
}

function ScatterSvg({ positions, activeDomains, hoveredId, setHoveredId, onMouseMove, width, height }) {
  const padding = { top: 40, right: 30, bottom: 50, left: 45 }
  const plotW = width - padding.left - padding.right
  const plotH = height - padding.top - padding.bottom

  const borderColor = getCssVar('--border')
  const hoverBorder = getCssVar('--hover-border')
  const labelColor = getCssVar('--text-tertiary')
  const fontMono = getCssVar('--font-mono') + ', monospace'

  function px(position) {
    return padding.left + ((position + 1) / 2) * plotW
  }

  function py(importance) {
    return padding.top + plotH - ((importance - 1) / 4) * plotH
  }

  // Quadrant dividers: x=0 and y=3
  const divX = px(0)
  const divY = py(3)

  const filtered = positions.filter(p => activeDomains.has(p.domain))

  return (
    <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-auto" style={{ display: 'block' }}>
      <rect width={width} height={height} fill="transparent" />

      {/* Grid lines - horizontal at each importance level */}
      {[1, 2, 3, 4, 5].map(imp => (
        <line
          key={`grid-h-${imp}`}
          x1={padding.left} y1={py(imp)}
          x2={width - padding.right} y2={py(imp)}
          stroke={borderColor} strokeWidth="0.5" opacity="0.4"
        />
      ))}

      {/* Grid lines - vertical at position markers */}
      {[-1, -0.5, 0, 0.5, 1].map(pos => (
        <line
          key={`grid-v-${pos}`}
          x1={px(pos)} y1={padding.top}
          x2={px(pos)} y2={height - padding.bottom}
          stroke={borderColor} strokeWidth="0.5" opacity="0.4"
        />
      ))}

      {/* Quadrant dividers - dashed, more prominent */}
      <line
        x1={divX} y1={padding.top} x2={divX} y2={height - padding.bottom}
        stroke={hoverBorder} strokeWidth="1" strokeDasharray="6 4" opacity="0.6"
      />
      <line
        x1={padding.left} y1={divY} x2={width - padding.right} y2={divY}
        stroke={hoverBorder} strokeWidth="1" strokeDasharray="6 4" opacity="0.6"
      />

      {/* Quadrant labels */}
      <text x={padding.left + 6} y={padding.top + 14} fill={labelColor} fontSize="8" fontFamily={fontMono} opacity="0.4">
        DEFINING OPPOSITION
      </text>
      <text x={width - padding.right - 6} y={padding.top + 14} fill={labelColor} fontSize="8" fontFamily={fontMono} opacity="0.4" textAnchor="end">
        HILLS I'LL DIE ON
      </text>
      <text x={padding.left + 6} y={height - padding.bottom - 8} fill={labelColor} fontSize="8" fontFamily={fontMono} opacity="0.4">
        MEH
      </text>
      <text x={width - padding.right - 6} y={height - padding.bottom - 8} fill={labelColor} fontSize="8" fontFamily={fontMono} opacity="0.4" textAnchor="end">
        SURE, WHATEVER
      </text>

      {/* Y-axis labels (importance) */}
      {[1, 2, 3, 4, 5].map(imp => (
        <text
          key={`y-${imp}`}
          x={padding.left - 8} y={py(imp) + 3}
          fill={labelColor} fontSize="9" fontFamily={fontMono} textAnchor="end"
        >
          {imp}
        </text>
      ))}
      <text
        x={12} y={padding.top + plotH / 2}
        fill={labelColor} fontSize="8" fontFamily={fontMono}
        textAnchor="middle"
        transform={`rotate(-90, 12, ${padding.top + plotH / 2})`}
      >
        IMPORTANCE
      </text>

      {/* X-axis labels (position) */}
      {[
        [-1, '-1'], [-0.5, '-0.5'], [0, '0'], [0.5, '+0.5'], [1, '+1']
      ].map(([pos, label]) => (
        <text
          key={`x-${pos}`}
          x={px(pos)} y={height - padding.bottom + 16}
          fill={labelColor} fontSize="9" fontFamily={fontMono} textAnchor="middle"
        >
          {label}
        </text>
      ))}
      <text
        x={padding.left} y={height - padding.bottom + 30}
        fill={labelColor} fontSize="8" fontFamily={fontMono}
      >
        AGAINST
      </text>
      <text
        x={px(0)} y={height - padding.bottom + 30}
        fill={labelColor} fontSize="8" fontFamily={fontMono} textAnchor="middle"
      >
        NEUTRAL
      </text>
      <text
        x={width - padding.right} y={height - padding.bottom + 30}
        fill={labelColor} fontSize="8" fontFamily={fontMono} textAnchor="end"
      >
        FOR
      </text>

      {/* Dots */}
      {filtered.map(p => {
        const cx = px(p.position)
        const cy = py(p.importance)
        const color = getDomainColor(p.domain)
        const isHovered = hoveredId === p.id
        const r = isHovered ? 6 : 5

        return (
          <g
            key={p.id}
            onMouseEnter={(e) => { setHoveredId(p.id); onMouseMove(e) }}
            onMouseMove={onMouseMove}
            onMouseLeave={() => setHoveredId(null)}
            style={{ cursor: 'pointer' }}
          >
            {/* Glow on hover */}
            {isHovered && (
              <circle cx={cx} cy={cy} r={12} fill={color} opacity="0.15" />
            )}
            <circle
              cx={cx} cy={cy} r={r}
              fill={color}
              stroke={isHovered ? '#ffffff' : 'none'}
              strokeWidth={isHovered ? 1.5 : 0}
              opacity={isHovered ? 1 : 0.85}
            />
            {/* Label for high-importance dots, or on hover */}
            {(p.importance >= 4 || isHovered) && (
              <text
                x={cx}
                y={cy - r - 4}
                textAnchor="middle"
                fill={color}
                fontSize="8"
                fontFamily={fontMono}
                fontWeight={isHovered ? 'bold' : 'normal'}
              >
                {p.short_label}
              </text>
            )}
          </g>
        )
      })}
    </svg>
  )
}

function HoverTooltip({ position, mousePos, containerRef }) {
  const [visible, setVisible] = useState(false)
  const timerRef = useRef(null)

  useEffect(() => {
    if (position) {
      timerRef.current = setTimeout(() => setVisible(true), 150)
    } else {
      setVisible(false)
    }
    return () => { if (timerRef.current) clearTimeout(timerRef.current) }
  }, [position?.id])

  if (!visible || !position || !containerRef.current) return null

  const rect = containerRef.current.getBoundingClientRect()
  const maxW = 320
  let left = mousePos.x - rect.left + 12
  let top = mousePos.y - rect.top - 10

  // Flip if near right edge
  if (left + maxW > rect.width) {
    left = mousePos.x - rect.left - maxW - 12
  }
  // Flip if near bottom
  if (top + 200 > rect.height) {
    top = Math.max(10, top - 200)
  }
  if (left < 0) left = 10

  const color = getDomainColor(position.domain)

  return (
    <div
      className="absolute z-50 pointer-events-none"
      style={{ left, top, maxWidth: maxW }}
    >
      <div className="bg-bg-elevated border border-border rounded-lg p-3 shadow-lg text-xs">
        <div className="flex items-center justify-between mb-1.5">
          <span className="font-mono font-bold text-text-primary text-sm">{position.short_label}</span>
          <span className="font-mono text-text-tertiary" style={{ color }}>{position.domain}</span>
        </div>
        <div className="border-t border-border mb-2" />
        <p className="text-text-secondary italic mb-2 leading-relaxed">"{position.question}"</p>
        <div className="flex gap-4 mb-2 font-mono">
          <span className="text-text-tertiary">
            Position: <span className="text-text-primary">{formatPosition(position.position)} ({position.position > 0 ? '+' : ''}{position.position.toFixed(2)})</span>
          </span>
        </div>
        <div className="mb-2 font-mono">
          <span className="text-text-tertiary">
            Importance: <span className="text-text-primary">{formatImportance(position.importance)} ({position.importance}/5)</span>
          </span>
        </div>
        <p className="text-text-secondary leading-relaxed mb-2">"{position.rationale}"</p>
        {position.source === 'inferred' && (
          <div className="text-text-tertiary font-mono flex items-center gap-1">
            <span className="text-accent-purple">✦</span> Inferred from conversations
          </div>
        )}
      </div>
    </div>
  )
}

function DomainLegend({ domains, activeDomains, onToggle }) {
  return (
    <div className="flex flex-wrap gap-x-3 gap-y-1.5 mt-2">
      {domains.map(domain => {
        const active = activeDomains.has(domain)
        const color = getDomainColor(domain)
        return (
          <button
            key={domain}
            onClick={() => onToggle(domain)}
            className="flex items-center gap-1.5 text-xs font-mono transition-opacity"
            style={{ opacity: active ? 1 : 0.3 }}
          >
            <span
              className="w-2.5 h-2.5 rounded-full flex-shrink-0"
              style={{ backgroundColor: color }}
            />
            <span className={`${active ? 'text-text-secondary' : 'text-text-tertiary line-through'}`}>
              {domain}
            </span>
          </button>
        )
      })}
    </div>
  )
}

export default function PositionScatterPlot({ positions = [], overlayPositions }) {
  const [activeDomains, setActiveDomains] = useState(() => new Set(getUniqueDomains(positions)))
  const [hoveredId, setHoveredId] = useState(null)
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 })
  const [modalOpen, setModalOpen] = useState(false)
  const containerRef = useRef(null)

  const domains = getUniqueDomains(positions)

  const handleToggle = useCallback((domain) => {
    setActiveDomains(prev => {
      const next = new Set(prev)
      if (next.has(domain)) {
        next.delete(domain)
      } else {
        next.add(domain)
      }
      return next
    })
  }, [])

  const handleMouseMove = useCallback((e) => {
    setMousePos({ x: e.clientX, y: e.clientY })
  }, [])

  const hoveredPosition = positions.find(p => p.id === hoveredId) || null

  const hasInferred = positions.some(p => p.source === 'inferred')

  if (!positions.length) return null

  return (
    <>
      <div className="bg-bg-panel border border-border rounded-lg p-3 panel-hover h-full flex flex-col">
        {/* Header */}
        <div className="flex items-center gap-2 mb-2 flex-shrink-0">
          <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide">
            POLITICAL POSITIONS
          </h2>
          <span className="text-text-tertiary text-xs font-mono">Position × Importance</span>
          <ContextTooltip text={SCATTER_TOOLTIP} />
          {hasInferred && <AiGeneratedBadge />}
          <button
            onClick={() => setModalOpen(true)}
            className="ml-auto text-xs text-text-tertiary hover:text-accent-blue font-mono transition-colors px-1.5 py-0.5 rounded hover:bg-bg-elevated"
            title="Expand to full view"
          >
            ⤢
          </button>
        </div>

        {/* Chart area */}
        <div className="flex-1 min-h-0 relative" ref={containerRef}>
          <ScatterSvg
            positions={positions}
            activeDomains={activeDomains}
            hoveredId={hoveredId}
            setHoveredId={setHoveredId}
            onMouseMove={handleMouseMove}
            width={600}
            height={400}
          />
          <HoverTooltip
            position={hoveredPosition}
            mousePos={mousePos}
            containerRef={containerRef}
          />
        </div>

        {/* Legend */}
        <div className="flex-shrink-0">
          <DomainLegend
            domains={domains}
            activeDomains={activeDomains}
            onToggle={handleToggle}
          />
        </div>
      </div>

      {/* Detail modal */}
      <DetailModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title="POLITICAL POSITIONS"
      >
        <div className="flex items-center gap-2 mb-4">
          <span className="text-text-tertiary text-xs font-mono">Position × Importance</span>
          <ContextTooltip text={SCATTER_TOOLTIP} />
          {hasInferred && <AiGeneratedBadge />}
        </div>
        <div className="relative" ref={modalOpen ? undefined : undefined}>
          <ScatterSvg
            positions={positions}
            activeDomains={activeDomains}
            hoveredId={hoveredId}
            setHoveredId={setHoveredId}
            onMouseMove={handleMouseMove}
            width={900}
            height={600}
          />
        </div>
        <DomainLegend
          domains={domains}
          activeDomains={activeDomains}
          onToggle={handleToggle}
        />
      </DetailModal>
    </>
  )
}
