import { useState } from 'react'
import AiGeneratedBadge from './shared/AiGeneratedBadge'
import ContextTooltip from './shared/ContextTooltip'

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
  // Map -1..1 to padding..size-padding
  const padding = 30
  const usable = size - 2 * padding
  return padding + ((value + 1) / 2) * usable
}

export default function PoliticalCompass({ entities = [], size = 280, collapsible = true }) {
  const [expanded, setExpanded] = useState(!collapsible)
  const [hoveredIdx, setHoveredIdx] = useState(null)

  const center = size / 2
  const padding = 30
  const axisStart = padding
  const axisEnd = size - padding

  const content = (
    <div>
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        className="w-full h-auto"
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
        <text x={axisStart + 2} y={center - 6} fill="#475569" fontSize="7" fontFamily="JetBrains Mono, monospace">Econ Left</text>
        <text x={axisEnd - 40} y={center - 6} fill="#475569" fontSize="7" fontFamily="JetBrains Mono, monospace">Econ Right</text>
        <text x={center + 4} y={axisStart + 8} fill="#475569" fontSize="7" fontFamily="JetBrains Mono, monospace">Auth</text>
        <text x={center + 4} y={axisEnd - 4} fill="#475569" fontSize="7" fontFamily="JetBrains Mono, monospace">Lib</text>

        {/* Quadrant labels */}
        <text x={axisStart + 4} y={axisStart + 14} fill="#475569" fontSize="6" fontFamily="JetBrains Mono, monospace" opacity="0.5">Auth Left</text>
        <text x={axisEnd - 46} y={axisStart + 14} fill="#475569" fontSize="6" fontFamily="JetBrains Mono, monospace" opacity="0.5">Auth Right</text>
        <text x={axisStart + 4} y={axisEnd - 6} fill="#475569" fontSize="6" fontFamily="JetBrains Mono, monospace" opacity="0.5">Lib Left</text>
        <text x={axisEnd - 40} y={axisEnd - 6} fill="#475569" fontSize="6" fontFamily="JetBrains Mono, monospace" opacity="0.5">Lib Right</text>

        {/* Entity clouds */}
        {entities.map((entity, i) => {
          const cx = mapToSvg(entity.economic, size)
          // Social: positive = authoritarian = top, so invert Y
          const cy = mapToSvg(-entity.social, size)
          const rx = entity.spread * (axisEnd - axisStart) / 2
          const ry = rx * 0.85 // Slightly elliptical
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
              {/* Label */}
              {(isHovered || isHighlighted) && (
                <text
                  x={cx}
                  y={cy - Math.max(ry, 7) - 4}
                  textAnchor="middle"
                  fill={color}
                  fontSize="8"
                  fontFamily="JetBrains Mono, monospace"
                  fontWeight={isHighlighted ? 'bold' : 'normal'}
                >
                  {entity.name}
                </text>
              )}
              {/* Hover ring */}
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
    </div>
  )

  if (!collapsible) {
    return (
      <div className="bg-bg-panel border border-border rounded-lg p-4 panel-hover">
        <div className="flex items-center gap-2 mb-2">
          <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide">
            POLITICAL POSITIONING
          </h2>
          <AiGeneratedBadge />
          <ContextTooltip text={COMPASS_TOOLTIP} />
        </div>
        {content}
      </div>
    )
  }

  return (
    <div className="bg-bg-panel border border-border rounded-lg p-4 panel-hover">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-2 w-full text-left"
      >
        <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide">
          POLITICAL POSITIONING
        </h2>
        <AiGeneratedBadge />
        <ContextTooltip text={COMPASS_TOOLTIP} />
        <span className="text-xs text-text-tertiary ml-auto">{expanded ? '▾' : '▸'}</span>
      </button>
      {expanded && (
        <div className="mt-3 section-content">
          {content}
        </div>
      )}
    </div>
  )
}
