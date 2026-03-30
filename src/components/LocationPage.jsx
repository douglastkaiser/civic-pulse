import { useState, useEffect } from 'react'
import { loadProfile, loadLocation, loadIssues, PROFILE_ID } from '../lib/data'
import LocationPanel from './LocationPanel'
import PriorityMatrix from './PriorityMatrix'
import IssueFeed from './IssueFeed'
import IssueDetail from './IssueDetail'
import NextStepsPanel from './NextStepsPanel'
import PoliticalCompass from './PoliticalCompass'
import LocationSwitcher from './LocationSwitcher'
import ExportButton from './shared/ExportButton'
import DetailModal from './shared/DetailModal'
import { getCssVar } from '../lib/themeColors'

export default function LocationPage() {
  const [profile, setProfile] = useState(null)
  const [location, setLocation] = useState(null)
  const [issuesData, setIssuesData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [locationLoading, setLocationLoading] = useState(false)
  const [selectedIssueId, setSelectedIssueId] = useState(null)
  const [issueModalOpen, setIssueModalOpen] = useState(false)
  const [activeLocationId, setActiveLocationId] = useState(null)

  // Phase 1: Load profile on mount
  useEffect(() => {
    loadProfile(PROFILE_ID)
      .then((prof) => {
        setProfile(prof)
        const defaultLoc = prof.locations?.find((l) => l.status === 'active') || prof.locations?.[0]
        if (defaultLoc) {
          setActiveLocationId(defaultLoc.id)
        } else {
          setLoading(false)
        }
      })
      .catch((err) => {
        console.error('Failed to load profile:', err)
        setLoading(false)
      })
  }, [])

  // Phase 2: Load location-specific data when activeLocationId changes
  useEffect(() => {
    if (!activeLocationId) return

    setLocationLoading(true)
    setSelectedIssueId(null)

    Promise.all([
      loadLocation(activeLocationId),
      loadIssues(activeLocationId),
    ])
      .then(([loc, iss]) => {
        setLocation(loc)
        setIssuesData(iss)
        setLoading(false)
        setLocationLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load location data:', err)
        setLoading(false)
        setLocationLoading(false)
      })
  }, [activeLocationId])

  const handleLocationSwitch = (locationId) => {
    if (locationId !== activeLocationId) {
      setActiveLocationId(locationId)
    }
  }

  if (loading) {
    return (
      <div className="h-full p-3 flex flex-col gap-3 overflow-auto lg:overflow-hidden">
        {/* Skeleton: Top row */}
        <div className="flex flex-col lg:flex-row gap-3 lg:flex-1 lg:min-h-0" style={{ flex: '1 1 50%' }}>
          <div className="lg:w-2/5 min-w-0 min-h-[300px] lg:min-h-0">
            <div className="bg-bg-panel border border-border rounded-lg p-4 h-full animate-pulse">
              <div className="h-4 w-40 bg-bg-elevated rounded mb-4" />
              <div className="space-y-3">
                <div className="bg-bg-elevated rounded p-3 h-20" />
                <div className="bg-bg-elevated rounded p-3 h-16" />
              </div>
            </div>
          </div>
          <div className="lg:w-[35%] min-w-0 min-h-[300px] lg:min-h-0">
            <div className="bg-bg-panel border border-border rounded-lg p-3 h-full animate-pulse">
              <div className="h-4 w-32 bg-bg-elevated rounded mb-3" />
              <div className="h-full bg-bg-elevated rounded opacity-30" />
            </div>
          </div>
          <div className="lg:w-1/4 min-w-0 min-h-[300px] lg:min-h-0">
            <div className="bg-bg-panel border border-border rounded-lg p-4 h-full animate-pulse">
              <div className="h-4 w-32 bg-bg-elevated rounded mb-4" />
              <div className="h-48 bg-bg-elevated rounded opacity-30" />
            </div>
          </div>
        </div>
        {/* Skeleton: Bottom row */}
        <div className="flex flex-col lg:flex-row gap-3 lg:flex-1 lg:min-h-0" style={{ flex: '1 1 50%' }}>
          <div className="lg:w-1/2 min-w-0 min-h-[300px] lg:min-h-0">
            <div className="bg-bg-panel border border-border rounded-lg p-3 h-full animate-pulse">
              <div className="h-4 w-16 bg-bg-elevated rounded mb-3" />
              <div className="space-y-2">
                <div className="h-12 bg-bg-elevated rounded" />
                <div className="h-12 bg-bg-elevated rounded" />
              </div>
            </div>
          </div>
          <div className="lg:w-1/2 min-w-0 min-h-[300px] lg:min-h-0">
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

  const handleSelectIssue = (issueId) => {
    setSelectedIssueId(issueId)
    setIssueModalOpen(true)
  }

  // Build compass entities: user position + location-specific entities
  const compassEntities = []
  const purple = getCssVar('--accent-purple')
  const blue = getCssVar('--accent-blue')
  const red = getCssVar('--accent-red')
  const amber = getCssVar('--accent-amber')
  const green = getCssVar('--accent-green')

  if (profile?.political_compass?.user) {
    compassEntities.push({ name: 'You', ...profile.political_compass.user, color: purple, highlighted: true })
  }

  if (location?.political_compass_entities) {
    const pce = location.political_compass_entities
    if (pce.city_austin) compassEntities.push({ name: 'Austin', ...pce.city_austin, color: blue })
    if (pce.state_texas) compassEntities.push({ name: 'Texas', ...pce.state_texas, color: red })
    if (pce.orange_county) compassEntities.push({ name: 'Orange Co', ...pce.orange_county, color: amber })
    if (pce.california_democratic_party) compassEntities.push({ name: 'CA Dems', ...pce.california_democratic_party, color: blue })
    if (pce.democratic_party) compassEntities.push({ name: 'Dem Party', ...pce.democratic_party, color: blue })
    if (pce.republican_party) compassEntities.push({ name: 'GOP', ...pce.republican_party, color: red })
    if (pce.local_orgs) {
      pce.local_orgs.forEach((org) => {
        compassEntities.push({ name: org.name, ...org, color: green })
      })
    }
  }

  const activeLocation = profile?.locations?.find((l) => l.id === activeLocationId)

  const getExportData = () => ({
    export_type: 'location_landscape',
    exported_at: new Date().toISOString(),
    profile_id: PROFILE_ID,
    active_location: activeLocation,
    location_data: location,
    issues: issuesData,
    political_compass_entities: compassEntities,
  })

  const issueTabs = issues.map((i) => ({
    id: i.id,
    label: i.title.length > 30 ? i.title.slice(0, 28) + '...' : i.title,
  }))

  const locationOverlay = locationLoading ? (
    <div className="absolute inset-0 bg-bg-primary/50 z-10 flex items-center justify-center rounded-lg">
      <span className="font-mono text-xs text-text-tertiary animate-pulse">Loading location data...</span>
    </div>
  ) : null

  return (
    <div className="h-full p-3 flex flex-col gap-3 overflow-auto lg:overflow-hidden animate-fade-in">
      {/* Utility bar with location switcher */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 flex-shrink-0">
        <LocationSwitcher
          locations={profile?.locations}
          activeLocationId={activeLocationId}
          onSwitch={handleLocationSwitch}
        />
        <ExportButton getData={getExportData} filename={`civic-pulse-location-${activeLocationId || 'all'}.json`} />
      </div>

      {/* Top row: Location + Priority Matrix + Political Compass */}
      <div className="flex flex-col lg:flex-row gap-3 lg:flex-1 lg:min-h-0" style={{ flex: '1 1 50%' }}>
        <div className="lg:w-2/5 min-w-0 min-h-[300px] lg:min-h-0 relative">
          {locationOverlay}
          <LocationPanel location={location} />
        </div>
        <div className="lg:w-[35%] min-w-0 min-h-[300px] lg:min-h-0 relative">
          {locationOverlay}
          <PriorityMatrix
            issues={issues}
            onSelectIssue={handleSelectIssue}
            selectedIssueId={selectedIssueId}
          />
        </div>
        {compassEntities.length > 0 && (
          <div className="lg:w-1/4 min-w-0 min-h-[300px] lg:min-h-0">
            <PoliticalCompass entities={compassEntities} size={280} collapsible={false} />
          </div>
        )}
      </div>

      {/* Bottom row: Issues + Next Steps */}
      <div className="flex flex-col lg:flex-row gap-3 lg:flex-1 lg:min-h-0" style={{ flex: '1 1 50%' }}>
        <div className="lg:w-1/2 min-w-0 min-h-[300px] lg:min-h-0 relative">
          {locationOverlay}
          <IssueFeed
            issues={issues}
            onSelectIssue={handleSelectIssue}
            selectedIssueId={selectedIssueId}
          />
        </div>
        <div className="lg:w-1/2 min-w-0 min-h-[300px] lg:min-h-0 relative">
          {locationOverlay}
          <NextStepsPanel nextSteps={location?.next_steps} />
        </div>
      </div>

      {/* Issue Detail Modal */}
      <DetailModal
        open={issueModalOpen}
        onClose={() => setIssueModalOpen(false)}
        title="ISSUES"
        tabs={issueTabs}
        activeTab={selectedIssueId}
        onTabChange={setSelectedIssueId}
      >
        <IssueDetail
          issue={selectedIssue}
          onClose={() => setIssueModalOpen(false)}
        />
      </DetailModal>
    </div>
  )
}
