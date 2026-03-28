import React from 'react'
import ReactDOM from 'react-dom/client'
import { HashRouter } from 'react-router-dom'
import App from './App.jsx'
import { ZoomProvider } from './lib/zoom.jsx'
import { ThemeProvider } from './lib/theme.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <HashRouter>
      <ThemeProvider>
        <ZoomProvider>
          <App />
        </ZoomProvider>
      </ThemeProvider>
    </HashRouter>
  </React.StrictMode>,
)
