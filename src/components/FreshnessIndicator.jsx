import { getFreshnessColor, getFreshnessLabel, getFreshnessDotColor } from '../lib/freshness'

export default function FreshnessIndicator({ timestamp, label, size = 8 }) {
  const color = getFreshnessDotColor(timestamp)
  const text = getFreshnessLabel(timestamp)

  return (
    <span className="inline-flex items-center gap-1.5" title={`${label ? label + ': ' : ''}${text}`}>
      <span
        className="rounded-full flex-shrink-0"
        style={{ width: size, height: size, backgroundColor: color }}
      />
      {label && <span className="text-xs text-text-secondary">{text}</span>}
    </span>
  )
}
