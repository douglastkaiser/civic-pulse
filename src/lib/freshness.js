export function getFreshnessColor(isoTimestamp) {
  if (!isoTimestamp) return 'gray'
  const age = Date.now() - new Date(isoTimestamp).getTime()
  const hours = age / (1000 * 60 * 60)
  if (hours < 24) return 'green'
  if (hours < 24 * 7) return 'yellow'
  return 'red'
}

export function getFreshnessLabel(isoTimestamp) {
  if (!isoTimestamp) return 'Never'
  const age = Date.now() - new Date(isoTimestamp).getTime()
  const minutes = Math.floor(age / (1000 * 60))
  if (minutes < 60) return `${minutes}m ago`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}h ago`
  const days = Math.floor(hours / 24)
  if (days < 30) return `${days}d ago`
  const months = Math.floor(days / 30)
  return `${months}mo ago`
}

const DOT_COLORS = {
  green: '#22c55e',
  yellow: '#f59e0b',
  red: '#ef4444',
  gray: '#475569',
}

export function getFreshnessDotColor(isoTimestamp) {
  return DOT_COLORS[getFreshnessColor(isoTimestamp)]
}
