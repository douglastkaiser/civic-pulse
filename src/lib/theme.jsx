import { createContext, useContext, useState, useCallback } from 'react'

const THEME_KEY = 'civic-pulse-theme'

const THEMES = [
  { id: 'civic', label: 'Civic', description: 'Clean, newspaper-inspired light mode' },
  { id: 'retro90s', label: 'Retro \'90s', description: 'GeoCities meets civic duty' },
  { id: 'midnight', label: 'Midnight', description: 'Warm, refined dark mode' },
  { id: 'roman', label: 'Roman Forum', description: 'Stone & marble civic grandeur' },
]

const ThemeContext = createContext({ theme: 'civic', setTheme: () => {} })

function applyTheme(themeId) {
  document.documentElement.setAttribute('data-theme', themeId)
}

export function ThemeProvider({ children }) {
  const [theme, setThemeState] = useState(() => {
    const saved = localStorage.getItem(THEME_KEY)
    const initial = saved && THEMES.some(t => t.id === saved) ? saved : 'civic'
    applyTheme(initial)
    return initial
  })

  const setTheme = useCallback((newTheme) => {
    localStorage.setItem(THEME_KEY, newTheme)
    applyTheme(newTheme)
    setThemeState(newTheme)
  }, [])

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  return useContext(ThemeContext)
}

export { THEMES }
