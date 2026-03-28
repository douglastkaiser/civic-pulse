// Read CSS custom property values at runtime.
// Used by components that need raw color values (Plotly, SVG, inline styles).
// CSS vars store space-separated RGB channels (e.g. "26 58 92"),
// so we convert to hex for use in inline styles and Plotly configs.

function rgbChannelsToHex(channels) {
  const parts = channels.trim().split(/\s+/)
  if (parts.length !== 3) return channels // fallback if not RGB format
  return '#' + parts.map(n => parseInt(n, 10).toString(16).padStart(2, '0')).join('')
}

export function getCssVar(name) {
  const raw = getComputedStyle(document.documentElement).getPropertyValue(name).trim()
  // If it looks like space-separated RGB channels, convert to hex
  if (/^\d+\s+\d+\s+\d+$/.test(raw)) {
    return rgbChannelsToHex(raw)
  }
  return raw
}

export function getThemeColors() {
  return {
    bgPrimary: getCssVar('--bg-primary'),
    bgPanel: getCssVar('--bg-panel'),
    bgElevated: getCssVar('--bg-elevated'),
    border: getCssVar('--border'),
    textPrimary: getCssVar('--text-primary'),
    textSecondary: getCssVar('--text-secondary'),
    textTertiary: getCssVar('--text-tertiary'),
    accentBlue: getCssVar('--accent-blue'),
    accentGreen: getCssVar('--accent-green'),
    accentAmber: getCssVar('--accent-amber'),
    accentRed: getCssVar('--accent-red'),
    accentPurple: getCssVar('--accent-purple'),
    quadAct: getCssVar('--quad-act'),
    quadKnow: getCssVar('--quad-know'),
    quadWatch: getCssVar('--quad-watch'),
    quadBg: getCssVar('--quad-bg'),
    hoverBorder: getCssVar('--hover-border'),
    fontMono: getCssVar('--font-mono'),
  }
}
