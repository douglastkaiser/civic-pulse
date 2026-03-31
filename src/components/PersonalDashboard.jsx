import { useState, useEffect } from 'react'
import { loadProfile, loadFreshness, PROFILE_ID } from '../lib/data'
import { useAuth } from '../lib/auth'
import { getUserProfile } from '../lib/userStore'
import ManifestoPanel from './ManifestoPanel'
import PoliticalCompass from './PoliticalCompass'
import PositionScatterPlot from './PositionScatterPlot'
import ExportButton from './shared/ExportButton'
import BulkExportButton from './shared/BulkExportButton'
import { getCssVar } from '../lib/themeColors'

const VIEW_TABS = [
  { key: 'action', label: 'Action' },
  { key: 'profile', label: 'Profile' },
]

function EmptyDashboard({ user }) {
  return (
    <div className="h-full p-3 flex flex-col gap-3 overflow-auto lg:overflow-hidden animate-fade-in">
      <div className="flex flex-col lg:flex-row gap-3 flex-1 lg:min-h-0">
        {/* Empty manifesto */}
        <div className="lg:w-3/5 min-w-0 min-h-[300px] lg:min-h-0">
          <div className="bg-bg-panel border border-border rounded-lg p-6 h-full flex flex-col items-center justify-center text-center">
            <div className="text-3xl mb-3">▸</div>
            <h2 className="font-mono text-lg font-bold text-text-primary tracking-wide mb-2">
              Welcome, {user.displayName?.split(' ')[0] || 'there'}
            </h2>
            <p className="text-text-secondary text-sm max-w-sm mb-4">
              Your political profile is empty. Once set up, you'll see your manifesto, values, and issue priorities here.
            </p>
            <span className="text-xs text-text-tertiary font-mono px-3 py-1.5 bg-bg-elevated rounded">
              Profile setup coming soon
            </span>
          </div>
        </div>

        {/* Empty compass */}
        <div className="lg:w-2/5 min-w-0 min-h-[300px] lg:min-h-0">
          <div className="bg-bg-panel border border-border rounded-lg p-6 h-full flex flex-col items-center justify-center text-center">
            <div className="text-3xl mb-3">◎</div>
            <h3 className="font-mono text-sm font-bold text-text-primary tracking-wide mb-2">
              POLITICAL COMPASS
            </h3>
            <p className="text-text-secondary text-sm max-w-xs">
              Your position on the political compass will appear here once your profile is configured.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default function PersonalDashboard() {
  const { user } = useAuth()
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isEmpty, setIsEmpty] = useState(false)
  const [view, setView] = useState('action')

  useEffect(() => {
    const load = async () => {
      try {
        // Try loading the user's Firestore profile first
        const userProfile = await getUserProfile(user.uid)
        if (userProfile?.manifesto) {
          setProfile(userProfile)
          setLoading(false)
          return
        }

        // Fall back to static profile data if it exists
        const [prof] = await Promise.all([
          loadProfile(PROFILE_ID),
          loadFreshness(),
        ])
        setProfile(prof)
      } catch {
        // No static data and no Firestore data → empty state
        setIsEmpty(true)
      }
      setLoading(false)
    }
    load()
  }, [user.uid])

  if (loading) {
    return (
      <div className="h-full p-3 flex flex-col gap-3 overflow-auto lg:overflow-hidden">
        <div className="flex flex-col lg:flex-row gap-3 flex-1 lg:min-h-0">
          <div className="lg:w-3/5 min-w-0 min-h-[300px] lg:min-h-0">
            <div className="bg-bg-panel border border-border rounded-lg p-4 h-full animate-pulse">
              <div className="h-4 w-28 bg-bg-elevated rounded mb-4" />
              <div className="flex gap-2 mb-4">
                <div className="h-5 w-20 bg-bg-elevated rounded-full" />
                <div className="h-5 w-16 bg-bg-elevated rounded-full" />
                <div className="h-5 w-24 bg-bg-elevated rounded-full" />
              </div>
              <div className="space-y-2">
                <div className="h-3 bg-bg-elevated rounded w-full" />
                <div className="h-3 bg-bg-elevated rounded w-5/6" />
                <div className="h-3 bg-bg-elevated rounded w-4/6" />
              </div>
            </div>
          </div>
          <div className="lg:w-2/5 min-w-0 min-h-[300px] lg:min-h-0">
            <div className="bg-bg-panel border border-border rounded-lg p-4 h-full animate-pulse">
              <div className="h-4 w-32 bg-bg-elevated rounded mb-4" />
              <div className="h-48 bg-bg-elevated rounded opacity-30" />
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (isEmpty || !profile) {
    return <EmptyDashboard user={user} />
  }

  // Political compass: user position only (no location entities)
  const compassEntities = []
  const purple = getCssVar('--accent-purple')

  if (profile?.political_compass?.user) {
    compassEntities.push({ name: 'You', ...profile.political_compass.user, color: purple, highlighted: true })
  }

  const getExportData = () => ({
    export_type: 'personal_political_profile',
    exported_at: new Date().toISOString(),
    profile_id: PROFILE_ID,
    display_name: profile.display_name,
    political_context: profile.political_context,
    values: profile.values,
    issue_salience: profile.issue_salience,
    manifesto: profile.manifesto,
    political_compass: profile.political_compass,
    political_positions: profile.political_positions,
    engagement_appetite: profile.engagement_appetite,
  })

  const profilePanels = (
    <div className="flex flex-col lg:flex-row gap-3 lg:min-h-0" style={{ flex: '2 1 0%' }}>
      <div className="lg:w-3/5 min-w-0 min-h-[300px] lg:min-h-0">
        <ManifestoPanel profile={profile} />
      </div>
      {compassEntities.length > 0 && (
        <div className="lg:w-2/5 min-w-0 min-h-[300px] lg:min-h-0">
          <PoliticalCompass entities={compassEntities} size={280} collapsible={false} />
        </div>
      )}
    </div>
  )

  return (
    <div className="h-full p-3 flex flex-col gap-3 overflow-auto lg:overflow-hidden animate-fade-in">
      {/* Utility bar with view tabs */}
      <div className="flex items-center gap-2 flex-shrink-0">
        <div className="flex gap-1">
          {VIEW_TABS.map(tab => (
            <button
              key={tab.key}
              onClick={() => setView(tab.key)}
              className={`text-xs font-mono px-2.5 py-1 rounded transition-colors ${
                view === tab.key
                  ? 'bg-accent-blue/20 text-accent-blue'
                  : 'text-text-tertiary hover:text-text-secondary'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-2 ml-auto">
          <BulkExportButton />
          <ExportButton getData={getExportData} filename="civic-pulse-profile.json" />
        </div>
      </div>

      {/* Action view: current layout */}
      {view === 'action' && (
        <div className="flex flex-col lg:flex-row gap-3 flex-1 lg:min-h-0">
          <div className="lg:w-3/5 min-w-0 min-h-[300px] lg:min-h-0">
            <ManifestoPanel profile={profile} />
          </div>
          {compassEntities.length > 0 && (
            <div className="lg:w-2/5 min-w-0 min-h-[300px] lg:min-h-0">
              <PoliticalCompass entities={compassEntities} size={280} collapsible={false} />
            </div>
          )}
        </div>
      )}

      {/* Profile view: manifesto + compass + scatter plot */}
      {view === 'profile' && (
        <div className="flex flex-col gap-3 flex-1 lg:min-h-0">
          {profilePanels}
          {profile?.political_positions?.length > 0 && (
            <div className="min-h-[400px]" style={{ flex: '3 1 0%' }}>
              <PositionScatterPlot positions={profile.political_positions} />
            </div>
          )}
        </div>
      )}
    </div>
  )
}
