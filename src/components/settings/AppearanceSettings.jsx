import { THEMES, FONTS, useTheme } from '../../lib/theme'
import { useZoom, ZOOM_LEVELS } from '../../lib/zoom'
export default function AppearanceSettings() {
  const { theme, setTheme, font, setFont } = useTheme()
  const { zoom, setZoom } = useZoom()
  return (
    <section className="appearance-settings" aria-labelledby="appearance-title">
      <header className="panel-heading">
        <h2 id="appearance-title">Appearance</h2>
        <span>Saved on this browser</span>
      </header>
      <div className="setting-row">
        <div>
          <label htmlFor="color-theme">Color theme</label>
          <p id="color-theme-help" className="setting-description">
            Change the palette. The layout stays compact.
          </p>
        </div>
        <select
          id="color-theme"
          aria-describedby="color-theme-help"
          className="civic-input"
          value={theme}
          onChange={(event) => setTheme(event.target.value)}
        >
          {THEMES.map((item) => (
            <option key={item.id} value={item.id}>
              {item.label}
            </option>
          ))}
        </select>
      </div>
      <div className="setting-row">
        <div>
          <label htmlFor="interface-font">Interface font</label>
          <p id="interface-font-help" className="setting-description">
            Choose the typeface used throughout the app.
          </p>
        </div>
        <select
          id="interface-font"
          aria-describedby="interface-font-help"
          className="civic-input"
          value={font}
          onChange={(event) => setFont(event.target.value)}
        >
          {FONTS.map((item) => (
            <option key={item.id} value={item.id}>
              {item.label}
            </option>
          ))}
        </select>
      </div>
      <div className="setting-row">
        <div>
          <label htmlFor="interface-size">Interface size</label>
          <p id="interface-size-help" className="setting-description">
            Adjust text and controls together.
          </p>
        </div>
        <select
          id="interface-size"
          aria-describedby="interface-size-help"
          className="civic-input"
          value={zoom}
          onChange={(event) => setZoom(Number(event.target.value))}
        >
          {ZOOM_LEVELS.map((item) => (
            <option key={item.value} value={item.value}>
              {Math.round(item.value * 100)}%{' '}
              {item.value === 1 ? '(default)' : ''}
            </option>
          ))}
        </select>
      </div>
      <div
        className="theme-presets"
        role="group"
        aria-label="Color theme presets"
      >
        {THEMES.map((item) => (
          <button
            key={item.id}
            type="button"
            className="theme-preset"
            aria-pressed={theme === item.id}
            onClick={() => setTheme(item.id)}
          >
            <span className="theme-swatches" aria-hidden="true">
              {item.colors.map((color, index) => (
                <span key={index} style={{ background: color }} />
              ))}
            </span>
            <span>{item.label}</span>
            <span className="preset-state">
              {theme === item.id ? '[selected]' : '[select]'}
            </span>
          </button>
        ))}
      </div>
      <div className="type-specimen">
        <span className="eyebrow">Preview</span>
        <p>City Council / Meeting agenda</p>
        <p className="text-text-secondary">
          Housing · Transportation · Local government
        </p>
        <p className="text-accent-blue">
          Aa Bb Cc · 0123456789 · {'{} [] / →'}
        </p>
      </div>
    </section>
  )
}
