import { useTheme, THEMES } from '../lib/theme'
import { useZoom, ZOOM_LEVELS } from '../lib/zoom'

const THEME_PREVIEWS = {
  civic: {
    bg: '#faf8f5',
    panel: '#ffffff',
    border: '#d4d0c8',
    accent: '#1a3a5c',
    green: '#2d6a4f',
    red: '#9b2226',
    text: '#1a1a1a',
  },
  retro90s: {
    bg: '#c0c0c0',
    panel: '#ffffff',
    border: '#808080',
    accent: '#0000ff',
    green: '#008000',
    red: '#ff0000',
    text: '#000000',
  },
  midnight: {
    bg: '#0d0d0d',
    panel: '#161616',
    border: '#2a2a2a',
    accent: '#d4a853',
    green: '#7daa6d',
    red: '#d47766',
    text: '#ede8e0',
  },
  roman: {
    bg: '#e8e0d4',
    panel: '#f5f2ed',
    border: '#b8a898',
    accent: '#2e4a6e',
    green: '#4a6741',
    red: '#8b1a1a',
    text: '#2c2416',
  },
}

function ThemeCard({ themeId, label, description, isActive, onClick }) {
  const p = THEME_PREVIEWS[themeId]
  return (
    <button
      onClick={onClick}
      className={`text-left rounded-lg border-2 p-4 transition-all duration-150 ${
        isActive
          ? 'border-accent-blue ring-2 ring-accent-blue/20'
          : 'border-border hover:border-accent-blue/40'
      }`}
    >
      {/* Mini preview */}
      <div
        className="rounded overflow-hidden mb-3 border"
        style={{ borderColor: p.border }}
      >
        <div
          className="p-2 space-y-1.5"
          style={{ backgroundColor: p.bg }}
        >
          {/* Mini header bar */}
          <div className="flex items-center gap-1.5">
            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: p.red }} />
            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: p.green }} />
            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: p.accent }} />
            <div className="flex-1 h-1.5 rounded-sm ml-1" style={{ backgroundColor: p.border }} />
          </div>
          {/* Mini panel */}
          <div
            className="rounded-sm p-1.5"
            style={{ backgroundColor: p.panel, border: `1px solid ${p.border}` }}
          >
            <div className="h-1 w-12 rounded-sm mb-1" style={{ backgroundColor: p.text, opacity: 0.6 }} />
            <div className="h-1 w-20 rounded-sm mb-1" style={{ backgroundColor: p.text, opacity: 0.3 }} />
            <div className="flex gap-1">
              <div className="h-3 flex-1 rounded-sm" style={{ backgroundColor: p.accent + '30' }} />
              <div className="h-3 flex-1 rounded-sm" style={{ backgroundColor: p.green + '30' }} />
            </div>
          </div>
          {/* Mini second panel */}
          <div className="flex gap-1">
            <div
              className="flex-1 h-4 rounded-sm"
              style={{ backgroundColor: p.panel, border: `1px solid ${p.border}` }}
            />
            <div
              className="flex-1 h-4 rounded-sm"
              style={{ backgroundColor: p.panel, border: `1px solid ${p.border}` }}
            />
          </div>
        </div>
      </div>

      <div className="font-mono text-sm font-bold text-text-primary tracking-wide">
        {label}
      </div>
      <div className="text-xs text-text-secondary mt-0.5">
        {description}
      </div>
      {isActive && (
        <div className="text-xs text-accent-blue font-mono mt-1.5">
          ACTIVE
        </div>
      )}
    </button>
  )
}

export default function SettingsPage() {
  const { theme, setTheme } = useTheme()
  const { zoom, setZoom } = useZoom()

  return (
    <div className="min-h-full bg-bg-primary p-6 animate-fade-in">
      <div className="max-w-3xl mx-auto">
        <h1 className="font-mono text-2xl font-bold text-text-primary tracking-wide mb-1">
          SETTINGS
        </h1>
        <p className="text-sm text-text-secondary mb-8">
          Customize your dashboard appearance.
        </p>

        {/* Theme Selection */}
        <section className="mb-10">
          <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide mb-1">
            THEME
          </h2>
          <p className="text-xs text-text-secondary mb-4">
            Choose a visual style for your dashboard.
          </p>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
            {THEMES.map((t) => (
              <ThemeCard
                key={t.id}
                themeId={t.id}
                label={t.label}
                description={t.description}
                isActive={theme === t.id}
                onClick={() => setTheme(t.id)}
              />
            ))}
          </div>
        </section>

        {/* Zoom Controls */}
        <section>
          <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide mb-1">
            ZOOM
          </h2>
          <p className="text-xs text-text-secondary mb-4">
            Adjust the overall size of the interface.
          </p>
          <div className="flex items-center gap-1">
            {ZOOM_LEVELS.map((level) => (
              <button
                key={level.label}
                onClick={() => setZoom(level.value)}
                className={`px-3 py-1.5 text-xs font-mono rounded border transition-colors ${
                  zoom === level.value
                    ? 'bg-accent-blue/15 text-accent-blue border-accent-blue/30'
                    : 'text-text-tertiary border-border hover:text-text-secondary hover:border-accent-blue/20'
                }`}
              >
                {level.label}
              </button>
            ))}
            <span className="text-xs text-text-tertiary ml-2 font-mono">
              {Math.round(zoom * 100)}%
            </span>
          </div>
        </section>
      </div>
    </div>
  )
}
