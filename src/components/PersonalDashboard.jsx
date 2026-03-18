import { useState, useEffect } from 'react'
import { loadProfile, loadLocation, loadIssues, loadFreshness } from '../lib/data'
import ManifestoPanel from './ManifestoPanel'
import LocationPanel from './LocationPanel'
import PriorityMatrix from './PriorityMatrix'
import IssueFeed from './IssueFeed'
import IssueDetail from './IssueDetail'
import NextStepsPanel from './NextStepsPanel'
import PoliticalCompass from './PoliticalCompass'

const PROFILE_ID = 'austin-78702'

export default function PersonalDashboard() {
  const [profile, setProfile] = useState(null)
  const [location, setLocation] = useState(null)
  const [issuesData, setIssuesData] = useState(null)
  const [freshness, setFreshness] = useState(null)
  const [loading, setLoading] = useState(true)
  const [selectedIssueId, setSelectedIssueId] = useState(null)

  useEffect(() => {
    Promise.all([
      loadProfile(PROFILE_ID),
      loadLocation(PROFILE_ID),
      loadIssues(PROFILE_ID),
      loadFreshness(),
    ])
      .then(([prof, loc, iss, fresh]) => {
        setProfile(prof)
        setLocation(loc)
        setIssuesData(iss)
        setFreshness(fresh)
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
        {/* Skeleton: Top row */}
        <div className="flex flex-col lg:flex-row gap-3 lg:flex-1 lg:min-h-0" style={{ flex: '1 1 50%' }}>
          <div className="lg:w-2/5 min-w-0 min-h-[300px] lg:min-h-0">
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
          <div className="lg:w-3/5 min-w-0 min-h-[300px] lg:min-h-0">
            <div className="bg-bg-panel border border-border rounded-lg p-4 h-full animate-pulse">
              <div className="h-4 w-40 bg-bg-elevated rounded mb-4" />
              <div className="space-y-3">
                <div className="bg-bg-elevated rounded p-3 h-20" />
                <div className="bg-bg-elevated rounded p-3 h-16" />
              </div>
            </div>
          </div>
        </div>
        {/* Skeleton: Bottom row */}
        <div className="flex flex-col lg:flex-row gap-3 lg:flex-1 lg:min-h-0" style={{ flex: '1 1 50%' }}>
          <div className="lg:w-1/3 min-w-0 min-h-[300px] lg:min-h-0">
            <div className="bg-bg-panel border border-border rounded-lg p-3 h-full animate-pulse">
              <div className="h-4 w-32 bg-bg-elevated rounded mb-3" />
              <div className="h-full bg-bg-elevated rounded opacity-30" />
            </div>
          </div>
          <div className="lg:w-1/3 min-w-0 min-h-[300px] lg:min-h-0">
            <div className="bg-bg-panel border border-border rounded-lg p-3 h-full animate-pulse">
              <div className="h-4 w-16 bg-bg-elevated rounded mb-3" />
              <div className="space-y-2">
                <div className="h-12 bg-bg-elevated rounded" />
                <div className="h-12 bg-bg-elevated rounded" />
              </div>
            </div>
          </div>
          <div className="lg:w-1/3 min-w-0 min-h-[300px] lg:min-h-0">
            <div className="bg-bg-panel border border-border rounded-lg p-3 h-full animate-pulse">
              <div className="h-4 w-24 bg-bg-elevated rounded mb-3" />
              <div className="space-y-2">
                <div className="h-10 bg-bg-elevated rounded" />
                <div className="h-10 bg-bg-elevated rounded" />
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  const issues = issuesData?.issues || []
  const selectedIssue = issues.find((i) => i.id === selectedIssueId)

  // Build compass entities from profile data
  const compassEntities = []
  if (profile?.political_compass) {
    const pc = profile.political_compass
    if (pc.user) compassEntities.push({ name: 'You', ...pc.user, color: '#a855f7', highlighted: true })
    if (pc.city_austin) compassEntities.push({ name: 'Austin', ...pc.city_austin, color: '#3b82f6' })
    if (pc.state_texas) compassEntities.push({ name: 'Texas', ...pc.state_texas, color: '#ef4444' })
    if (pc.democratic_party) compassEntities.push({ name: 'Dem Party', ...pc.democratic_party, color: '#3b82f6' })
    if (pc.republican_party) compassEntities.push({ name: 'GOP', ...pc.republican_party, color: '#ef4444' })
    if (pc.local_orgs) {
      pc.local_orgs.forEach((org) => compassEntities.push({ ...org, color: '#22c55e' }))
    }
  }

  return (
    <div className="h-full p-3 flex flex-col gap-3 overflow-auto lg:overflow-hidden">
      {/* Top row: Manifesto + Location */}
      <div className="flex flex-col lg:flex-row gap-3 lg:flex-1 lg:min-h-0" style={{ flex: '1 1 50%' }}>
        <div className="lg:w-2/5 min-w-0 min-h-[300px] lg:min-h-0">
          <ManifestoPanel profile={profile} />
        </div>
        <div className="lg:w-3/5 min-w-0 min-h-[300px] lg:min-h-0">
          <LocationPanel location={location} />
        </div>
      </div>

      {/* Bottom row: Matrix + Issues + Next Steps */}
      <div className="flex flex-col lg:flex-row gap-3 lg:flex-1 lg:min-h-0" style={{ flex: '1 1 50%' }}>
        <div className="lg:w-1/3 min-w-0 min-h-[300px] lg:min-h-0">
          <PriorityMatrix
            issues={issues}
            onSelectIssue={setSelectedIssueId}
            selectedIssueId={selectedIssueId}
          />
        </div>
        <div className="lg:w-1/3 min-w-0 min-h-[300px] lg:min-h-0">
          {selectedIssue ? (
            <IssueDetail
              issue={selectedIssue}
              onClose={() => setSelectedIssueId(null)}
            />
          ) : (
            <IssueFeed
              issues={issues}
              onSelectIssue={setSelectedIssueId}
              selectedIssueId={selectedIssueId}
            />
          )}
        </div>
        <div className="lg:w-1/3 min-w-0 min-h-[300px] lg:min-h-0">
          <NextStepsPanel profile={profile} />
        </div>
      </div>

      {/* Political Compass */}
      {compassEntities.length > 0 && (
        <div className="lg:max-w-xs">
          <PoliticalCompass entities={compassEntities} size={280} collapsible={true} />
        </div>
      )}
    </div>
  )
}
