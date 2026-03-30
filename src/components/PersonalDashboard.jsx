import { useState, useEffect } from 'react'
import { loadProfile, loadFreshness, PROFILE_ID } from '../lib/data'
import ManifestoPanel from './ManifestoPanel'
import PoliticalCompass from './PoliticalCompass'
import ExportButton from './shared/ExportButton'
import BulkExportButton from './shared/BulkExportButton'
import { getCssVar } from '../lib/themeColors'

export default function PersonalDashboard() {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      loadProfile(PROFILE_ID),
      loadFreshness(),
    ])
      .then(([prof]) => {
        setProfile(prof)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load profile data:', err)
        setLoading(false)
      })
  }, [])

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
    engagement_appetite: profile.engagement_appetite,
  })

  return (
    <div className="h-full p-3 flex flex-col gap-3 overflow-auto lg:overflow-hidden animate-fade-in">
      {/* Utility bar */}
      <div className="flex items-center justify-end gap-2 flex-shrink-0">
        <BulkExportButton />
        <ExportButton getData={getExportData} filename="civic-pulse-profile.json" />
      </div>

      {/* Profile panels: Manifesto + Political Compass */}
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
    </div>
  )
}
