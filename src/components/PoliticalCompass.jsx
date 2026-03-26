import { useState } from 'react'
import AiGeneratedBadge from './shared/AiGeneratedBadge'
import ContextTooltip from './shared/ContextTooltip'
import DetailModal from './shared/DetailModal'

const COMPASS_TOOLTIP = "This visualization approximates political positioning on two axes: economic policy (left = more government intervention, right = more free market) and social policy (bottom = more individual liberty, top = more social regulation). Positions are shown as clouds rather than points because political identity is multidimensional and fuzzy. All positions are AI-estimated approximations based on voting patterns, stated positions, and policy analysis. Take them as directional indicators, not precise measurements."

const DEFAULT_COLORS = [
  '#a855f7', // purple - user/primary
  '#3b82f6', // blue
  '#22c55e', // green
  '#f59e0b', // amber
  '#ef4444', // red
  '#06b6d4', // cyan
  '#ec4899', // pink
  '#8b5cf6', // violet
]

function mapToSvg(value, size) {
  const padding = 30
  const usable = size - 2 * padding
  return padding + ((value + 1) / 2) * usable
}

function CompassSvg({ entities, size, hoveredIdx, setHoveredIdx }) {
  const center = size / 2
  const padding = 30
  const axisStart = padding
  const axisEnd = size - padding
  const fontSize = Math.max(7, size / 40)
  const labelFontSize = Math.max(6, size / 47)

  return (
    <svg
      viewBox={`0 0 ${size} ${size}`}
      className="w-full h-auto"
      style={{ maxWidth: size, display: 'block' }}
    >
      {/* Background */}
      <rect width={size} height={size} fill="transparent" />

      {/* Grid lines */}
      <line x1={center} y1={axisStart} x2={center} y2={axisEnd} stroke="#1e2d4a" strokeWidth="1" strokeDasharray="4 4" />
      <line x1={axisStart} y1={center} x2={axisEnd} y2={center} stroke="#1e2d4a" strokeWidth="1" strokeDasharray="4 4" />

      {/* Axes */}
      <line x1={axisStart} y1={center} x2={axisEnd} y2={center} stroke="#2a3f6a" strokeWidth="1" />
      <line x1={center} y1={axisStart} x2={center} y2={axisEnd} stroke="#2a3f6a" strokeWidth="1" />

      {/* Axis labels */}
      <text x={axisStart + 2} y={center - 6} fill="#475569" fontSize={fontSize} fontFamily="JetBrains Mono, monospace">Econ Left</text>
      <text x={axisEnd - 2} y={center - 6} fill="#475569" fontSize={fontSize} fontFamily="JetBrains Mono, monospace" textAnchor="end">Econ Right</text>
      <text x={center + 4} y={axisStart + 8} fill="#475569" fontSize={fontSize} fontFamily="JetBrains Mono, monospace">Auth</text>
      <text x={center + 4} y={axisEnd - 4} fill="#475569" fontSize={fontSize} fontFamily="JetBrains Mono, monospace">Lib</text>

      {/* Quadrant labels */}
      <text x={axisStart + 4} y={axisStart + 14} fill="#475569" fontSize={labelFontSize} fontFamily="JetBrains Mono, monospace" opacity="0.5">Auth Left</text>
      <text x={axisEnd - 4} y={axisStart + 14} fill="#475569" fontSize={labelFontSize} fontFamily="JetBrains Mono, monospace" opacity="0.5" textAnchor="end">Auth Right</text>
      <text x={axisStart + 4} y={axisEnd - 6} fill="#475569" fontSize={labelFontSize} fontFamily="JetBrains Mono, monospace" opacity="0.5">Lib Left</text>
      <text x={axisEnd - 4} y={axisEnd - 6} fill="#475569" fontSize={labelFontSize} fontFamily="JetBrains Mono, monospace" opacity="0.5" textAnchor="end">Lib Right</text>

      {/* Entity clouds */}
      {entities.map((entity, i) => {
        const cx = mapToSvg(entity.economic, size)
        const cy = mapToSvg(-entity.social, size)
        const economicSpread = entity.economic_spread ?? entity.spread
        const socialSpread = entity.social_spread ?? entity.spread
        const rx = economicSpread * (axisEnd - axisStart) / 2
        const ry = socialSpread * (axisEnd - axisStart) / 2
        const color = entity.color || DEFAULT_COLORS[i % DEFAULT_COLORS.length]
        const isHighlighted = entity.highlighted
        const isHovered = hoveredIdx === i

        return (
          <g
            key={i}
            onMouseEnter={() => setHoveredIdx(i)}
            onMouseLeave={() => setHoveredIdx(null)}
            style={{ cursor: 'default' }}
          >
            <ellipse
              cx={cx}
              cy={cy}
              rx={Math.max(rx, 8)}
              ry={Math.max(ry, 7)}
              fill={color}
              fillOpacity={isHighlighted ? 0.3 : 0.15}
              stroke={isHighlighted ? color : 'none'}
              strokeWidth={isHighlighted ? 1.5 : 0}
              strokeOpacity={0.6}
            />
            {(isHovered || isHighlighted) && (
              <text
                x={cx}
                y={cy - Math.max(ry, 7) - 4}
                textAnchor="middle"
                fill={color}
                fontSize={Math.max(8, size / 35)}
                fontFamily="JetBrains Mono, monospace"
                fontWeight={isHighlighted ? 'bold' : 'normal'}
              >
                {entity.name}
              </text>
            )}
            {isHovered && !isHighlighted && (
              <ellipse
                cx={cx}
                cy={cy}
                rx={Math.max(rx, 8) + 2}
                ry={Math.max(ry, 7) + 2}
                fill="none"
                stroke={color}
                strokeWidth="1"
                strokeOpacity="0.4"
                strokeDasharray="3 2"
              />
            )}
          </g>
        )
      })}
    </svg>
  )
}

export default function PoliticalCompass({ entities = [], size = 280, collapsible = true }) {
  const [expanded, setExpanded] = useState(!collapsible)
  const [hoveredIdx, setHoveredIdx] = useState(null)
  const [modalOpen, setModalOpen] = useState(false)

  const header = (
    <div className="flex items-center gap-2">
      <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide">
        POLITICAL POSITIONING
      </h2>
      <AiGeneratedBadge />
      <ContextTooltip text={COMPASS_TOOLTIP} />
      <button
        onClick={(e) => { e.stopPropagation(); setModalOpen(true) }}
        className="ml-auto text-xs text-text-tertiary hover:text-accent-blue font-mono transition-colors px-1.5 py-0.5 rounded hover:bg-bg-elevated"
        title="Expand to full view"
      >
        ⤢
      </button>
    </div>
  )

  const compass = (
    <CompassSvg
      entities={entities}
      size={size}
      hoveredIdx={hoveredIdx}
      setHoveredIdx={setHoveredIdx}
    />
  )

  const modal = (
    <DetailModal
      open={modalOpen}
      onClose={() => setModalOpen(false)}
      title="POLITICAL POSITIONING"
    >
      <div className="flex items-center gap-2 mb-4">
        <AiGeneratedBadge />
        <ContextTooltip text={COMPASS_TOOLTIP} />
      </div>
      <div className="flex justify-center">
        <CompassSvg
          entities={entities}
          size={560}
          hoveredIdx={hoveredIdx}
          setHoveredIdx={setHoveredIdx}
        />
      </div>
      {/* Legend */}
      <div className="mt-4 flex flex-wrap gap-3">
        {entities.map((entity, i) => (
          <div key={i} className="flex items-center gap-1.5 text-xs">
            <span
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: entity.color || DEFAULT_COLORS[i % DEFAULT_COLORS.length], opacity: 0.6 }}
            />
            <span className="text-text-secondary font-mono">{entity.name}</span>
          </div>
        ))}
      </div>
    </DetailModal>
  )

  if (!collapsible) {
    return (
      <>
        <div className="bg-bg-panel border border-border rounded-lg p-4 panel-hover h-full flex flex-col">
          <div className="mb-2">{header}</div>
          <div className="flex-1 min-h-0 flex items-center justify-center overflow-hidden">
            {compass}
          </div>
        </div>
        {modal}
      </>
    )
  }

  return (
    <>
      <div className="bg-bg-panel border border-border rounded-lg p-4 panel-hover">
        <button
          onClick={() => setExpanded(!expanded)}
          className="flex items-center gap-2 w-full text-left"
        >
          {header}
          <span className="text-xs text-text-tertiary ml-auto">{expanded ? '▾' : '▸'}</span>
        </button>
        {expanded && (
          <div className="mt-3 section-content">
            {compass}
          </div>
        )}
      </div>
      {modal}
    </>
  )
}
