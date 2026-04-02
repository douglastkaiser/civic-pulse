import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import PersonalDashboard from './components/PersonalDashboard'
import OrgDashboard from './components/OrgDashboard'
import OrgPublicView from './components/OrgPublicView'
import NewOrg from './components/NewOrg'
import About from './components/About'
import LocationPage from './components/LocationPage'
import OfficialsPage from './components/OfficialsPage'
import SettingsPage from './components/SettingsPage'
import SplashPage from './components/SplashPage'
import ErrorBoundary from './components/shared/ErrorBoundary'
import { useZoom } from './lib/zoom.jsx'
import { useAuth } from './lib/auth'
import { LOCATION_LABELS } from './lib/data'

const DEFAULT_LOCATION = Object.keys(LOCATION_LABELS)[0]

export default function App() {
  const location = useLocation()
  const isPublicView = location.pathname.endsWith('/public')
  const { zoom } = useZoom()
  const { user, loading } = useAuth()

  // Show loading spinner while auth state resolves
  if (loading) {
    return (
      <div className="h-screen bg-bg-primary flex items-center justify-center">
        <div className="text-text-tertiary font-mono text-sm animate-pulse">Loading...</div>
      </div>
    )
  }

  // Public view renders without sidebar or auth
  if (isPublicView) {
    return (
      <ErrorBoundary>
        <Routes>
          <Route path="/org/:orgId/public" element={<OrgPublicView />} />
        </Routes>
      </ErrorBoundary>
    )
  }

  // Not logged in → splash page
  if (!user) {
    return <SplashPage />
  }

  return (
    <div className="h-screen bg-bg-primary flex overflow-hidden">
      <Sidebar />
      <main className="flex-1 overflow-y-auto" style={zoom !== 1 ? { zoom } : undefined}>
        <ErrorBoundary>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<PersonalDashboard />} />
            <Route path="/location/:locationId" element={<LocationPage />} />
            <Route path="/location" element={<Navigate to={`/location/${DEFAULT_LOCATION}`} replace />} />
            <Route path="/officials/:locationId" element={<OfficialsPage />} />
            <Route path="/officials" element={<Navigate to={`/officials/${DEFAULT_LOCATION}`} replace />} />
            <Route path="/about" element={<About />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="/org/new" element={<NewOrg />} />
            <Route path="/org/:orgId/public" element={<OrgPublicView />} />
            <Route path="/org/:orgId" element={<OrgDashboard />} />
          </Routes>
        </ErrorBoundary>
      </main>
    </div>
  )
}
