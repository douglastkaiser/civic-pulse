import { createContext, useContext, useState, useEffect } from 'react'

const ZOOM_KEY = 'civic-pulse-zoom'
const ZOOM_LEVELS = [
  { label: 'S', value: 0.85 },
  { label: 'M', value: 1 },
  { label: 'L', value: 1.15 },
  { label: 'XL', value: 1.3 },
]

const ZoomContext = createContext({ zoom: 1, setZoom: () => {} })

export function ZoomProvider({ children }) {
  const [zoom, setZoom] = useState(() => {
    const saved = localStorage.getItem(ZOOM_KEY)
    return saved ? parseFloat(saved) : 1
  })

  useEffect(() => {
    localStorage.setItem(ZOOM_KEY, String(zoom))
  }, [zoom])

  return (
    <ZoomContext.Provider value={{ zoom, setZoom }}>
      {children}
    </ZoomContext.Provider>
  )
}

export function useZoom() {
  return useContext(ZoomContext)
}

export { ZOOM_LEVELS }
