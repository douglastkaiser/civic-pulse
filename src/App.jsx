import { lazy, Suspense, useEffect } from 'react'
import { Routes, Route, Navigate, Link, useLocation } from 'react-router-dom'
import AppNavigation from './components/AppNavigation'
import SplashPage from './components/SplashPage'
import ErrorBoundary from './components/shared/ErrorBoundary'
import DataState from './components/shared/DataState'
import { useAuth } from './lib/auth'
import { useZoom } from './lib/zoom.jsx'
import { clearApiKey } from './lib/apiKeyStore'
const ResidentHome = lazy(() => import('./components/ResidentHome'))
const ExplorePage = lazy(() => import('./components/ExplorePage'))
const ResidentIssuePage = lazy(() => import('./components/ResidentIssuePage'))
const SavedPage = lazy(() => import('./components/SavedPage'))
const AppearancePage = lazy(() => import('./components/AppearancePage'))
const SettingsPage = lazy(() => import('./components/SettingsPage'))
const PersonalDashboard = lazy(() => import('./components/PersonalDashboard'))
const LocationPage = lazy(() => import('./components/LocationPage'))
const OfficialsPage = lazy(() => import('./components/OfficialsPage'))
const ElectionsPage = lazy(() => import('./components/ElectionsPage'))
const OrgDashboard = lazy(() => import('./components/OrgDashboard'))
const OrgPublicView = lazy(() => import('./components/OrgPublicView'))
const OrganizationsPage = lazy(() => import('./components/OrganizationsPage'))
const NewOrg = lazy(() => import('./components/NewOrg'))
const NewLocation = lazy(() => import('./components/NewLocation'))
const About = lazy(() => import('./components/About'))
function Private({ children }) {
  const { user } = useAuth()
  const location = useLocation()
  return user ? (
    children
  ) : (
    <Navigate
      to="/signin"
      state={{ returnTo: location.pathname + location.search }}
      replace
    />
  )
}
export default function App() {
  const { user, loading, error } = useAuth()
  const location = useLocation()
  const { zoom } = useZoom()
  useEffect(() => {
    clearApiKey()
  }, [])
  useEffect(() => {
    document.querySelector('main')?.focus()
    window.scrollTo(0, 0)
  }, [location.pathname])
  if (loading)
    return (
      <div className="page-wrap">
        <DataState loading />
      </div>
    )
  if (error)
    return (
      <div className="page-wrap">
        <DataState error={error} onRetry={() => window.location.reload()} />
      </div>
    )
  return (
    <div className="app-shell bg-bg-primary text-text-primary">
      <a
        className="skip-link"
        href="#main"
        onClick={(event) => {
          event.preventDefault()
          document.getElementById('main')?.focus()
        }}
      >
        Skip to content
      </a>
      <AppNavigation />
      <main
        id="main"
        className="app-main"
        tabIndex={-1}
        style={zoom !== 1 ? { zoom } : undefined}
      >
        <ErrorBoundary key={location.pathname}>
          <Suspense
            fallback={
              <div className="page-wrap">
                <DataState loading />
              </div>
            }
          >
            <Routes>
              <Route
                path="/"
                element={
                  user ? <Navigate to="/dashboard" replace /> : <SplashPage />
                }
              />
              <Route
                path="/signin"
                element={
                  user ? (
                    <Navigate
                      to={location.state?.returnTo || '/dashboard'}
                      replace
                    />
                  ) : (
                    <SplashPage />
                  )
                }
              />
              <Route
                path="/dashboard"
                element={
                  <Private>
                    <ResidentHome />
                  </Private>
                }
              />
              <Route path="/demo" element={<ResidentHome demo />} />
              <Route path="/appearance" element={<AppearancePage />} />
              <Route path="/explore" element={<ExplorePage />} />
              <Route
                path="/issues/:locationId/:issueId"
                element={<ResidentIssuePage />}
              />
              <Route
                path="/saved"
                element={
                  <Private>
                    <SavedPage />
                  </Private>
                }
              />
              <Route
                path="/settings"
                element={
                  <Private>
                    <SettingsPage />
                  </Private>
                }
              />
              <Route
                path="/profile/analysis"
                element={
                  <Private>
                    <PersonalDashboard />
                  </Private>
                }
              />
              <Route
                path="/organizations"
                element={
                  <Private>
                    <OrganizationsPage />
                  </Private>
                }
              />
              <Route
                path="/location/new"
                element={
                  <Private>
                    <NewLocation />
                  </Private>
                }
              />
              <Route path="/location/:locationId" element={<LocationPage />} />
              <Route
                path="/location"
                element={<Navigate to="/explore" replace />}
              />
              <Route
                path="/officials/:locationId"
                element={<OfficialsPage />}
              />
              <Route
                path="/officials"
                element={<Navigate to="/officials/austin-78702" replace />}
              />
              <Route
                path="/elections/:locationId"
                element={<ElectionsPage />}
              />
              <Route
                path="/elections"
                element={<Navigate to="/elections/austin-78702" replace />}
              />
              <Route
                path="/org/new"
                element={
                  <Private>
                    <NewOrg />
                  </Private>
                }
              />
              <Route path="/org/:orgId/public" element={<OrgPublicView />} />
              <Route
                path="/org/:orgId"
                element={
                  <Private>
                    <OrgDashboard />
                  </Private>
                }
              />
              <Route path="/about" element={<About />} />
              <Route
                path="*"
                element={
                  <div className="page-wrap">
                    <h1 className="text-3xl font-semibold">Page not found</h1>
                    <Link
                      className="civic-button inline-block mt-4"
                      to="/explore"
                    >
                      Explore local issues
                    </Link>
                  </div>
                }
              />
            </Routes>
          </Suspense>
        </ErrorBoundary>
      </main>
      <footer className="app-statusbar">
        Local knowledge. Thoughtful participation.{' '}
        <Link className="underline ml-2" to="/about">
          About Civic Pulse
        </Link>
      </footer>
    </div>
  )
}
