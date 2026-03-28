import { createContext, useContext, useState, useEffect } from 'react'

const THEME_KEY = 'civic-pulse-theme'

const THEMES = [
  { id: 'civic', label: 'Civic', description: 'Clean, newspaper-inspired light mode' },
  { id: 'retro90s', label: 'Retro \'90s', description: 'GeoCities meets civic duty' },
  { id: 'midnight', label: 'Midnight', description: 'Warm, refined dark mode' },
  { id: 'roman', label: 'Roman Forum', description: 'Stone & marble civic grandeur' },
]

const ThemeContext = createContext({ theme: 'civic', setTheme: () => {} })

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(() => {
    const saved = localStorage.getItem(THEME_KEY)
    return saved && THEMES.some(t => t.id === saved) ? saved : 'civic'
  })

  useEffect(() => {
    localStorage.setItem(THEME_KEY, theme)
    document.documentElement.setAttribute('data-theme', theme)
  }, [theme])

  // Set initial data-theme on mount
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
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
