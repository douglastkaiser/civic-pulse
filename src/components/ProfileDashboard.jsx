import { useState, useEffect } from 'react'
import { loadProfile, loadLocation, loadIssues } from '../lib/data'
import ManifestoPanel from './ManifestoPanel'
import LocationPanel from './LocationPanel'
import PriorityMatrix from './PriorityMatrix'
import IssueFeed from './IssueFeed'
import IssueDetail from './IssueDetail'
import NextStepsPanel from './NextStepsPanel'

export default function ProfileDashboard({ profileId, freshness }) {
  const [profile, setProfile] = useState(null)
  const [location, setLocation] = useState(null)
  const [issuesData, setIssuesData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [selectedIssueId, setSelectedIssueId] = useState(null)

  useEffect(() => {
    setLoading(true)
    setSelectedIssueId(null)

    Promise.all([
      loadProfile(profileId),
      loadLocation(profileId),
      loadIssues(profileId),
    ])
      .then(([prof, loc, iss]) => {
        setProfile(prof)
        setLocation(loc)
        setIssuesData(iss)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load profile data:', err)
        setLoading(false)
      })
  }, [profileId])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="font-mono text-text-secondary text-sm animate-pulse">Loading...</div>
      </div>
    )
  }

  const issues = issuesData?.issues || []
  const selectedIssue = issues.find((i) => i.id === selectedIssueId)

  return (
    <div className="h-full p-3 flex flex-col gap-3 overflow-hidden">
      {/* Top row: Manifesto + Location */}
      <div className="flex gap-3 flex-1 min-h-0" style={{ flex: '1 1 50%' }}>
        <div className="w-2/5 min-w-0">
          <ManifestoPanel profile={profile} />
        </div>
        <div className="w-3/5 min-w-0">
          <LocationPanel location={location} />
        </div>
      </div>

      {/* Bottom row: Matrix + Issues + Next Steps */}
      <div className="flex gap-3 flex-1 min-h-0" style={{ flex: '1 1 50%' }}>
        <div className="w-1/3 min-w-0">
          <PriorityMatrix
            issues={issues}
            onSelectIssue={setSelectedIssueId}
            selectedIssueId={selectedIssueId}
          />
        </div>
        <div className="w-1/3 min-w-0">
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
        <div className="w-1/3 min-w-0">
          <NextStepsPanel profile={profile} />
        </div>
      </div>
    </div>
  )
}
