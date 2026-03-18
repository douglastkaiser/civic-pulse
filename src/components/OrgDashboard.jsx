import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { loadOrg } from '../lib/data'
import AiGeneratedBadge from './shared/AiGeneratedBadge'
import ContextTooltip from './shared/ContextTooltip'
import PoliticalCompass from './PoliticalCompass'
import CampaignList from './org/CampaignList'
import CampaignDetail from './org/CampaignDetail'
import EngagementPipeline from './org/EngagementPipeline'
import OrgNextSteps from './org/OrgNextSteps'

export default function OrgDashboard() {
  const { orgId } = useParams()
  const [org, setOrg] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedCampaignId, setSelectedCampaignId] = useState(null)
  const [missionExpanded, setMissionExpanded] = useState(false)

  useEffect(() => {
    setLoading(true)
    setError(null)
    setSelectedCampaignId(null)
    loadOrg(orgId)
      .then((data) => {
        setOrg(data)
        // Auto-select first campaign
        if (data.active_campaigns?.length > 0) {
          setSelectedCampaignId(data.active_campaigns[0].id)
        }
        setLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load org:', err)
        setError('Organization not found')
        setLoading(false)
      })
  }, [orgId])

  if (loading) {
    return (
      <div className="h-full p-4 overflow-auto">
        <div className="animate-pulse space-y-4">
          <div className="h-6 w-64 bg-bg-elevated rounded" />
          <div className="h-4 w-96 bg-bg-elevated rounded" />
          <div className="flex gap-4">
            <div className="w-1/3 space-y-3">
              <div className="h-32 bg-bg-elevated rounded" />
              <div className="h-48 bg-bg-elevated rounded" />
            </div>
            <div className="w-2/3 space-y-3">
              <div className="h-24 bg-bg-elevated rounded" />
              <div className="h-64 bg-bg-elevated rounded" />
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="h-full p-4 flex items-center justify-center">
        <div className="text-center">
          <p className="text-text-secondary font-mono text-sm mb-2">{error}</p>
          <Link to="/dashboard" className="text-accent-blue text-sm font-mono hover:underline">
            ← Back to Dashboard
          </Link>
        </div>
      </div>
    )
  }

  const selectedCampaign = org.active_campaigns?.find((c) => c.id === selectedCampaignId)

  // Build compass entities from org data
  const compassEntities = []
  if (org.political_positioning?.compass_cloud) {
    const cc = org.political_positioning.compass_cloud
    compassEntities.push({
      name: org.name,
      economic: cc.economic_center,
      social: cc.social_center,
      spread: Math.max(cc.economic_spread, cc.social_spread),
      color: '#a855f7',
      highlighted: true,
    })
  }
  const orgPositions = {
    'AURA': { economic: -0.1, social: -0.4, spread: 0.1 },
    'Transit Forward': { economic: -0.15, social: -0.3, spread: 0.1 },
    'Austin Habitat for Humanity': { economic: -0.05, social: -0.2, spread: 0.12 },
  }
  org.aligned_organizations?.forEach((ally) => {
    const pos = orgPositions[ally.name]
    if (pos) compassEntities.push({ name: ally.name, ...pos, color: '#22c55e' })
  })

  return (
    <div className="h-full overflow-auto">
      {/* Header */}
      <div className="px-4 py-3 border-b border-border bg-bg-panel">
        <div className="flex items-center justify-between">
          <Link to="/dashboard" className="text-xs text-text-tertiary hover:text-accent-blue font-mono transition-colors">
            ← Back to Dashboard
          </Link>
          <Link
            to={`/org/${orgId}/public`}
            className="text-xs text-text-tertiary hover:text-accent-blue font-mono transition-colors px-2 py-1 rounded border border-border hover:border-accent-blue/30"
          >
            Share ↗
          </Link>
        </div>
        <h1 className="font-mono text-lg font-bold text-text-primary tracking-wide mt-2">
          {org.name}
        </h1>
        <p className="text-sm text-text-secondary italic">{org.tagline}</p>
      </div>

      {/* Two-column layout */}
      <div className="flex flex-col lg:flex-row gap-4 p-4">
        {/* Left column */}
        <div className="lg:w-2/5 space-y-4 flex-shrink-0">
          {/* Mission & Positioning */}
          <div className="bg-bg-panel border border-border rounded-lg p-4 panel-hover">
            <div className="flex items-center gap-2 mb-2">
              <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide">
                MISSION & POSITIONING
              </h2>
              <AiGeneratedBadge />
            </div>

            {/* Mission - collapsible */}
            <p className="text-sm text-text-secondary leading-relaxed">
              {missionExpanded ? org.mission : (org.mission?.slice(0, 120) + '...')}
            </p>
            {org.mission?.length > 120 && (
              <button
                onClick={() => setMissionExpanded(!missionExpanded)}
                className="text-xs text-accent-blue font-mono mt-1"
              >
                {missionExpanded ? 'Less ▴' : 'More ▾'}
              </button>
            )}

            {/* Key Positions as badges */}
            <div className="mt-3 flex flex-wrap gap-1.5">
              {org.key_policy_positions?.slice(0, 4).map((pos, i) => (
                <span
                  key={i}
                  className="px-2 py-0.5 text-xs rounded-full bg-accent-purple/15 text-accent-purple border border-accent-purple/30"
                >
                  {pos}
                </span>
              ))}
              {org.key_policy_positions?.length > 4 && (
                <span className="px-2 py-0.5 text-xs rounded-full bg-bg-elevated text-text-tertiary border border-border">
                  +{org.key_policy_positions.length - 4} more
                </span>
              )}
            </div>
          </div>

          {/* Political Compass */}
          {compassEntities.length > 0 && (
            <PoliticalCompass entities={compassEntities} size={280} collapsible={false} />
          )}

          {/* Allied Organizations */}
          <div className="bg-bg-panel border border-border rounded-lg p-4 panel-hover">
            <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide mb-2">
              ALLIED ORGANIZATIONS
            </h2>
            <div className="space-y-2">
              {org.aligned_organizations?.map((ally, i) => (
                <div key={i} className="flex items-start gap-2 text-sm">
                  <span className="text-accent-green mt-0.5">●</span>
                  <div>
                    <span className="text-text-primary font-medium">{ally.name}</span>
                    <span className="text-text-tertiary"> — {ally.relationship}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Engagement Pipeline */}
          <div className="bg-bg-panel border border-border rounded-lg p-4 panel-hover">
            <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide mb-3">
              ENGAGEMENT PIPELINE
            </h2>
            <EngagementPipeline pipeline={org.engagement_pipeline} />
          </div>
        </div>

        {/* Right column */}
        <div className="lg:w-3/5 space-y-4">
          {/* Active Campaigns */}
          <div className="bg-bg-panel border border-border rounded-lg p-4 panel-hover">
            <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide mb-3">
              ACTIVE CAMPAIGNS
            </h2>
            <CampaignList
              campaigns={org.active_campaigns}
              selectedId={selectedCampaignId}
              onSelect={setSelectedCampaignId}
            />
          </div>

          {/* Campaign Detail */}
          <div className="bg-bg-panel border border-border rounded-lg p-4 panel-hover min-h-[200px]">
            <CampaignDetail campaign={selectedCampaign} />
          </div>

          {/* Org Next Steps */}
          <OrgNextSteps steps={org.practical_next_steps_for_org} />
        </div>
      </div>
    </div>
  )
}
