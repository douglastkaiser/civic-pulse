import {
  createContext,
  useContext,
  useState,
  useCallback,
  useLayoutEffect,
} from 'react'

const THEME_KEY = 'civic-pulse-theme'
const FONT_KEY = 'civic-pulse-font'
export const THEMES = [
  {
    id: 'retro90s',
    label: 'Neo Retro',
    description: 'Warm gray, ink blue, flat borders',
    colors: ['#e8e8e4', '#f8f8f5', '#243e58', '#242424'],
  },
  {
    id: 'lightplus',
    label: 'Light+',
    description: 'Paper white with blue accents',
    colors: ['#f3f3f3', '#ffffff', '#005a9e', '#202020'],
  },
  {
    id: 'darkplus',
    label: 'Dark+',
    description: 'Charcoal with editor blue accents',
    colors: ['#1e1e1e', '#252526', '#569cd6', '#d4d4d4'],
  },
  {
    id: 'solarizedlight',
    label: 'Solarized Light',
    description: 'Cream, slate, and muted teal',
    colors: ['#eee8d5', '#fdf6e3', '#006b91', '#465b63'],
  },
  {
    id: 'solarizeddark',
    label: 'Solarized Dark',
    description: 'Deep teal with quiet cyan accents',
    colors: ['#002b36', '#073642', '#62b9cd', '#c1d0cd'],
  },
  {
    id: 'civic',
    label: 'Civic',
    description: 'Newspaper white and navy',
    colors: ['#faf8f5', '#ffffff', '#1a3a5c', '#1a1a1a'],
  },
  {
    id: 'midnight',
    label: 'Midnight',
    description: 'Warm black and soft blue',
    colors: ['#0d0d0d', '#161616', '#89a9c9', '#ede8e0'],
  },
  {
    id: 'roman',
    label: 'Roman Forum',
    description: 'Stone, cream, and burgundy',
    colors: ['#e8e0d4', '#f5f2ed', '#2e4a6e', '#2c2416'],
  },
]
export const FONTS = [
  {
    id: 'mono',
    label: 'System Mono',
    family: 'Consolas, "Liberation Mono", "Courier New", monospace',
  },
  {
    id: 'courier',
    label: 'Courier',
    family: '"Courier New", Courier, monospace',
  },
  {
    id: 'system',
    label: 'System Sans',
    family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif',
  },
  {
    id: 'serif',
    label: 'Book Serif',
    family: 'Georgia, "Times New Roman", serif',
  },
]
function readPreference(key, choices, fallback) {
  try {
    const saved = localStorage.getItem(key)
    return choices.some((item) => item.id === saved) ? saved : fallback
  } catch {
    return fallback
  }
}
function savePreference(key, value) {
  try {
    localStorage.setItem(key, value)
  } catch {
    /* Preferences still work for this session when storage is disabled. */
  }
}
function applyAppearance(theme, font) {
  document.documentElement.dataset.theme = theme
  document.documentElement.style.setProperty(
    '--ui-font',
    FONTS.find((item) => item.id === font).family
  )
  document.documentElement.style.colorScheme = [
    'darkplus',
    'solarizeddark',
    'midnight',
  ].includes(theme)
    ? 'dark'
    : 'light'
}
const ThemeContext = createContext(null)
export function ThemeProvider({ children }) {
  const [theme, setThemeState] = useState(() =>
    readPreference(THEME_KEY, THEMES, 'retro90s')
  )
  const [font, setFontState] = useState(() =>
    readPreference(FONT_KEY, FONTS, 'mono')
  )
  const setTheme = useCallback((value) => {
    if (!THEMES.some((item) => item.id === value)) return
    savePreference(THEME_KEY, value)
    setThemeState(value)
  }, [])
  const setFont = useCallback((value) => {
    if (!FONTS.some((item) => item.id === value)) return
    savePreference(FONT_KEY, value)
    setFontState(value)
  }, [])
  useLayoutEffect(() => {
    applyAppearance(theme, font)
  }, [theme, font])
  return (
    <ThemeContext.Provider value={{ theme, setTheme, font, setFont }}>
      {children}
    </ThemeContext.Provider>
  )
}
export function useTheme() {
  return useContext(ThemeContext)
}
