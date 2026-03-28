import { NavLink } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { ORG_IDS_BY_LOCATION, LOCATION_LABELS, loadOrg, loadFreshness } from '../lib/data'
import FreshnessIndicator from './FreshnessIndicator'

export default function Sidebar() {
  const [orgsByLocation, setOrgsByLocation] = useState({})
  const [freshness, setFreshness] = useState(null)
  const [orgsExpanded, setOrgsExpanded] = useState(true)
  const [mobileOpen, setMobileOpen] = useState(false)

  useEffect(() => {
    // Load orgs grouped by location
    const loadOrgsByLoc = async () => {
      const result = {}
      for (const [locId, orgIds] of Object.entries(ORG_IDS_BY_LOCATION)) {
        try {
          result[locId] = await Promise.all(orgIds.map((id) => loadOrg(id)))
        } catch (err) {
          console.error(`Failed to load orgs for ${locId}:`, err)
          result[locId] = []
        }
      }
      setOrgsByLocation(result)
    }

    loadOrgsByLoc()

    loadFreshness()
      .then(setFreshness)
      .catch(() => {})
  }, [])

  // Get timestamps for each location
  const getLocationTimestamp = (locId) => {
    const locData = freshness?.locations?.[locId]
    if (!locData) {
      // Fallback to old profiles structure
      const profileData = freshness?.profiles?.[locId]
      if (!profileData) return null
      return [profileData.issues_scraped, profileData.location_scraped, profileData.manifesto_generated]
        .filter(Boolean)
        .sort()
        .pop()
    }
    return [locData.landscape_scraped, locData.issues_scraped, locData.next_steps_generated]
      .filter(Boolean)
      .sort()
      .pop()
  }

  const navLinkClass = ({ isActive }) =>
    `flex items-center gap-2 px-3 py-2 text-sm font-mono rounded transition-colors duration-150 ${
      isActive
        ? 'bg-accent-blue/15 text-accent-blue border-l-2 border-accent-blue'
        : 'text-text-secondary hover:text-text-primary hover:bg-bg-elevated'
    }`

  const handleNavClick = () => {
    setMobileOpen(false)
  }

  const sidebarContent = (
    <>
      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto p-2 space-y-1">
        <NavLink to="/dashboard" className={navLinkClass} onClick={handleNavClick}>
          <span className="text-xs">▸</span>
          MY DASHBOARD
        </NavLink>

        <NavLink to="/officials" className={navLinkClass} onClick={handleNavClick}>
          <span className="text-xs">◆</span>
          OFFICIALS
        </NavLink>

        <div className="mt-4">
          <button
            onClick={() => setOrgsExpanded(!orgsExpanded)}
            className="flex items-center gap-2 px-3 py-1.5 text-xs font-mono font-bold text-text-secondary tracking-wide w-full text-left hover:text-text-primary transition-colors"
          >
            <span>{orgsExpanded ? '▾' : '▸'}</span>
            ORGANIZATIONS
          </button>

          {orgsExpanded && (
            <div className="ml-2 space-y-0.5 mt-1 pl-1 border-l border-border/40">
              {Object.entries(ORG_IDS_BY_LOCATION).map(([locId]) => {
                const orgs = orgsByLocation[locId] || []
                const label = LOCATION_LABELS[locId] || locId
                return (
                  <div key={locId}>
                    <div className="px-3 py-1 text-[10px] font-mono font-bold text-text-secondary tracking-widest uppercase mt-2 first:mt-0">
                      {label}
                    </div>
                    {orgs.map((org) => (
                      <NavLink
                        key={org.id}
                        to={`/org/${org.id}`}
                        className={navLinkClass}
                        onClick={handleNavClick}
                      >
                        <span className="text-xs">├─</span>
                        <span className="truncate text-xs">{org.name}</span>
                      </NavLink>
                    ))}
                  </div>
                )
              })}
              <NavLink to="/org/new" className={navLinkClass} onClick={handleNavClick}>
                <span className="text-xs">├─</span>
                <span className="text-accent-green text-xs">+ New Organization</span>
              </NavLink>
            </div>
          )}
        </div>

        <div className="mt-4">
          <NavLink to="/about" className={navLinkClass} onClick={handleNavClick}>
            <span className="text-xs">▸</span>
            ABOUT
          </NavLink>
          <NavLink to="/settings" className={navLinkClass} onClick={handleNavClick}>
            <span className="text-xs">⚙</span>
            SETTINGS
          </NavLink>
        </div>
      </nav>

      {/* Footer */}
      <div className="p-3 border-t border-border space-y-2">
        {Object.entries(LOCATION_LABELS).map(([locId, label]) => {
          const ts = getLocationTimestamp(locId)
          const shortLabel = locId === 'austin-78702' ? 'ATX' : 'OC'
          return (
            <div key={locId} className="flex items-center gap-2 text-xs text-text-secondary font-mono">
              <span>{shortLabel}:</span>
              {ts ? (
                <FreshnessIndicator timestamp={ts} size={6} />
              ) : (
                <span className="text-text-tertiary">Never</span>
              )}
            </div>
          )
        })}
        <a
          href="https://github.com/douglastkaiser/civic-pulse/actions/workflows/pipeline.yml"
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs text-text-tertiary hover:text-accent-blue font-mono transition-colors flex items-center gap-1"
          title="Opens GitHub Actions where you can trigger a data refresh"
        >
          ↻ Refresh
        </a>
      </div>
    </>
  )

  return (
    <>
      {/* Mobile hamburger button */}
      <button
        onClick={() => setMobileOpen(!mobileOpen)}
        className="lg:hidden fixed top-3 left-3 z-50 p-2.5 bg-bg-elevated border-2 border-border rounded text-text-primary font-mono text-base shadow-lg"
        aria-label="Toggle navigation"
      >
        {mobileOpen ? '✕' : '☰'}
      </button>

      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-30"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Sidebar - desktop */}
      <aside className="hidden lg:flex w-56 h-full bg-bg-panel border-r border-border flex-col flex-shrink-0">
        <div className="px-4 py-3 border-b border-border">
          <h1 className="font-mono text-base font-bold text-text-primary tracking-wider">
            CIVIC PULSE
          </h1>
          <span className="text-xs text-text-tertiary font-mono">v0.2</span>
        </div>
        {sidebarContent}
      </aside>

      {/* Sidebar - mobile */}
      <aside
        className={`lg:hidden fixed top-0 left-0 h-full w-64 bg-bg-panel border-r border-border flex flex-col z-40 transition-transform duration-200 shadow-2xl backdrop-blur-sm ${
          mobileOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="px-4 py-3 border-b border-border">
          <h1 className="font-mono text-base font-bold text-text-primary tracking-wider">
            CIVIC PULSE
          </h1>
          <span className="text-xs text-text-tertiary font-mono">v0.2</span>
        </div>
        {sidebarContent}
      </aside>
    </>
  )
}
