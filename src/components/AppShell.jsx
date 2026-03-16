import { useState, useEffect } from 'react'
import { loadAllProfiles, loadFreshness, PROFILE_IDS } from '../lib/data'
import TabBar from './TabBar'
import ProfileDashboard from './ProfileDashboard'

export default function AppShell() {
  const [profiles, setProfiles] = useState([])
  const [freshness, setFreshness] = useState(null)
  const [activeId, setActiveId] = useState(PROFILE_IDS[0])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([loadAllProfiles(), loadFreshness()])
      .then(([profs, fresh]) => {
        setProfiles(profs)
        setFreshness(fresh)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load data:', err)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-bg-primary flex items-center justify-center">
        <div className="font-mono text-text-secondary text-sm animate-pulse">
          CIVIC PULSE — Loading...
        </div>
      </div>
    )
  }

  return (
    <div className="h-screen bg-bg-primary flex flex-col overflow-hidden">
      <header className="flex items-center justify-between px-4 py-2 bg-bg-panel border-b border-border">
        <div className="flex items-center gap-3">
          <h1 className="font-mono text-base font-bold text-text-primary tracking-wider">
            CIVIC PULSE
          </h1>
          <span className="text-xs text-text-tertiary font-mono">v0.1</span>
        </div>
        <a
          href="https://github.com/douglastkaiser/civic-pulse/actions/workflows/pipeline.yml"
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs text-text-tertiary hover:text-accent-blue font-mono transition-colors px-2 py-1 rounded hover:bg-accent-blue/10"
          title="Trigger data refresh via GitHub Actions"
        >
          ↻ Refresh
        </a>
      </header>
      <TabBar
        profiles={profiles}
        freshness={freshness}
        activeId={activeId}
        onSelect={setActiveId}
      />
      <main className="flex-1 overflow-auto lg:overflow-hidden">
        <div key={activeId} className="h-full animate-fade-in">
          <ProfileDashboard profileId={activeId} freshness={freshness} />
        </div>
      </main>
    </div>
  )
}
