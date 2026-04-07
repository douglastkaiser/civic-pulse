import { useState, useEffect } from 'react'

// Deterministic color from a string (hash → HSL)
function colorFromName(name) {
  let h = 0
  for (let i = 0; i < name.length; i++) {
    h = (h * 31 + name.charCodeAt(i)) | 0
  }
  const hue = Math.abs(h) % 360
  return `hsl(${hue}, 45%, 35%)`
}

function initialsOf(name) {
  if (!name) return '?'
  const parts = name.trim().split(/\s+/).filter(Boolean)
  if (parts.length === 0) return '?'
  if (parts.length === 1) return parts[0][0].toUpperCase()
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
}

const SIZES = {
  sm: { box: 'w-9 h-9', text: 'text-[11px]' },
  md: { box: 'w-12 h-12', text: 'text-sm' },
  lg: { box: 'w-16 h-16', text: 'text-lg' },
}

export default function OfficialAvatar({ official, size = 'sm', className = '' }) {
  const [errored, setErrored] = useState(false)

  // Reset error state if the underlying official changes
  useEffect(() => {
    setErrored(false)
  }, [official?.id, official?.photoUrl])

  const sz = SIZES[size] || SIZES.sm
  const name = official?.name || ''
  const initials = initialsOf(name)
  const bg = colorFromName(name)
  const url = official?.photoUrl

  const showImage = url && !errored

  return (
    <div
      className={`${sz.box} flex-shrink-0 rounded-full overflow-hidden border border-border flex items-center justify-center font-mono font-bold text-white ${className}`}
      style={showImage ? undefined : { background: bg }}
      aria-label={name}
    >
      {showImage ? (
        <img
          src={url}
          alt={name}
          loading="lazy"
          referrerPolicy="no-referrer"
          onError={() => setErrored(true)}
          className="w-full h-full object-cover"
        />
      ) : (
        <span className={sz.text}>{initials}</span>
      )}
    </div>
  )
}
