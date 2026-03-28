import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { loadOrg } from '../lib/data'
import AiGeneratedBadge from './shared/AiGeneratedBadge'
import ContextTooltip from './shared/ContextTooltip'
import DetailModal from './shared/DetailModal'
import PoliticalCompass from './PoliticalCompass'
import PriorityMatrix from './PriorityMatrix'
import CampaignList from './org/CampaignList'
import CampaignDetail from './org/CampaignDetail'
import EngagementPipeline from './org/EngagementPipeline'
import OrgNextSteps from './org/OrgNextSteps'
import ExportButton from './shared/ExportButton'
import { getCssVar } from '../lib/themeColors'

export default function OrgDashboard() {
  const { orgId } = useParams()
  const [org, setOrg] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [missionExpanded, setMissionExpanded] = useState(false)
  // Campaign modal state
  const [campaignModalOpen, setCampaignModalOpen] = useState(false)
  const [selectedCampaignId, setSelectedCampaignId] = useState(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    setSelectedCampaignId(null)
    loadOrg(orgId)
      .then((data) => {
        setOrg(data)
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

  const handleCampaignSelect = (campaignId) => {
    setSelectedCampaignId(campaignId)
    setCampaignModalOpen(true)
  }

  const getExportData = () => ({
    export_type: 'org_political_profile',
    exported_at: new Date().toISOString(),
    org_id: org.id,
    name: org.name,
    tagline: org.tagline,
    mission: org.mission,
    geographic_scope: org.geographic_scope,
    political_positioning: org.political_positioning,
    key_policy_positions: org.key_policy_positions,
    active_campaigns: org.active_campaigns,
    aligned_organizations: org.aligned_organizations,
    engagement_pipeline: org.engagement_pipeline,
    practical_next_steps: org.practical_next_steps_for_org,
  })

  // Build compass entities from org data
  const compassEntities = []
  if (org.political_positioning?.compass_cloud) {
    const cc = org.political_positioning.compass_cloud
    compassEntities.push({
      name: org.name,
      economic: cc.economic_center,
      social: cc.social_center,
      economic_spread: cc.economic_spread,
      social_spread: cc.social_spread,
      color: getCssVar('--accent-purple'),
      highlighted: true,
    })
  }
  compassEntities.push({ name: 'Austin', economic: -0.15, social: -0.2, spread: 0.25, color: getCssVar('--accent-blue') })
  compassEntities.push({ name: 'Texas', economic: 0.3, social: 0.2, spread: 0.35, color: getCssVar('--accent-red') })
  compassEntities.push({ name: 'Dem Party', economic: -0.3, social: -0.1, spread: 0.3, color: getCssVar('--accent-blue') })
  compassEntities.push({ name: 'GOP', economic: 0.4, social: 0.3, spread: 0.25, color: getCssVar('--accent-red') })

  const orgPositions = {
    'AURA': { economic: -0.1, social: -0.4, spread: 0.1 },
    'Transit Forward': { economic: -0.15, social: -0.3, spread: 0.1 },
    'Austin Habitat for Humanity': { economic: -0.05, social: -0.2, spread: 0.12 },
    'Downtown Austin Alliance': { economic: 0.2, social: -0.15, spread: 0.1 },
    'Austin Chamber of Commerce': { economic: 0.3, social: 0.0, spread: 0.15 },
    'League of Women Voters': { economic: -0.1, social: -0.3, spread: 0.1 },
    'Austin Abundance Project': { economic: 0.0, social: -0.1, spread: 0.15 },
    'Austin YIMBY Action': { economic: 0.15, social: -0.2, spread: 0.15 },
    'Austin Tech Alliance': { economic: 0.15, social: -0.2, spread: 0.1 },
    'United Way for Greater Austin': { economic: -0.2, social: -0.25, spread: 0.1 },
    'Integral Care': { economic: -0.2, social: -0.15, spread: 0.1 },
    'Austin Area Urban League': { economic: -0.15, social: -0.2, spread: 0.1 },
    'Family Endeavors': { economic: -0.1, social: -0.1, spread: 0.1 },
    'ECHO': { economic: -0.15, social: -0.2, spread: 0.1 },
    'Austin Safe & Sound': { economic: 0.05, social: 0.0, spread: 0.15 },
  }
  org.aligned_organizations?.forEach((ally) => {
    const pos = orgPositions[ally.name]
    if (pos) compassEntities.push({ name: ally.name, ...pos, color: getCssVar('--accent-green') })
  })

  // Build campaign data for priority matrix
  const campaignIssues = (org.active_campaigns || []).map((c) => ({
    id: c.id,
    title: c.title,
    importance_score: c.importance_score ?? 50,
    impact_score: c.impact_score ?? 50,
    quadrant: (c.importance_score ?? 50) >= 50 && (c.impact_score ?? 50) >= 50 ? 'act_now'
      : (c.importance_score ?? 50) < 50 && (c.impact_score ?? 50) >= 50 ? 'know'
      : (c.importance_score ?? 50) >= 50 && (c.impact_score ?? 50) < 50 ? 'watch'
      : 'background',
  }))

  // Campaign tabs for modal
  const campaignTabs = (org.active_campaigns || []).map((c) => ({
    id: c.id,
    label: c.title.length > 30 ? c.title.slice(0, 28) + '...' : c.title,
  }))

  return (
    <div className="h-full overflow-auto animate-fade-in">
      {/* Header */}
      <div className="px-4 py-3 border-b border-border bg-bg-panel">
        <div className="flex items-center justify-between">
          <Link to="/dashboard" className="text-xs text-text-tertiary hover:text-accent-blue font-mono transition-colors">
            ← Back to Dashboard
          </Link>
          <div className="flex items-center gap-2">
            <ExportButton getData={getExportData} filename={`civic-pulse-org-${orgId}.json`} />
            <Link
              to={`/org/${orgId}/public`}
              className="text-xs text-text-tertiary hover:text-accent-blue font-mono transition-colors px-2 py-1 rounded border border-border hover:border-accent-blue/30"
            >
              Share ↗
            </Link>
          </div>
        </div>
        <h1 className="font-mono text-lg font-bold text-text-primary tracking-wide mt-2">
          {org.name}
        </h1>
        <p className="text-sm text-text-secondary italic">{org.tagline}</p>
      </div>

      {/* Two-row layout mirroring personal dashboard */}
      <div className="p-3 flex flex-col gap-3 lg:h-[calc(100%-88px)]">
        {/* Top row: Mission + Political Compass + Priority Matrix */}
        <div className="flex flex-col lg:flex-row gap-3 lg:flex-1 lg:min-h-0" style={{ flex: '1 1 50%' }}>
          {/* Mission & Positioning (like Manifesto) */}
          <div className="lg:w-2/5 min-w-0 min-h-[300px] lg:min-h-0">
            <div className="bg-bg-panel border border-border rounded-lg p-4 panel-hover h-full flex flex-col overflow-hidden">
              <div className="flex items-center gap-2 mb-2">
                <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide">
                  MISSION & POSITIONING
                </h2>
                <AiGeneratedBadge />
              </div>

              {/* Scrollable content */}
              <div className="flex-1 overflow-y-auto min-h-0">
                {/* Always-visible mission summary */}
                <p className="text-sm text-text-secondary leading-relaxed mb-2">
                  {missionExpanded ? org.mission : (org.mission?.slice(0, 200) + '...')}
                </p>
                {org.mission?.length > 200 && (
                  <button
                    onClick={() => setMissionExpanded(!missionExpanded)}
                    className="text-xs text-accent-blue font-mono mb-3 text-left"
                  >
                    {missionExpanded ? 'Less ▴' : 'More ▾'}
                  </button>
                )}

                {/* Key Positions as badges */}
                <div className="flex flex-wrap gap-1.5 mb-3">
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

                {/* Positioning description — collapsible */}
                {org.political_positioning?.description && (
                  <div className="border border-border rounded bg-bg-elevated">
                    <details>
                      <summary className="px-3 py-2 text-left hover:bg-bg-panel transition-colors cursor-pointer font-mono text-xs font-bold text-text-tertiary tracking-wide">
                        POSITIONING DETAILS
                      </summary>
                      <div className="px-3 pb-3 text-xs text-text-secondary leading-relaxed section-content">
                        {org.political_positioning.description}
                      </div>
                    </details>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Political Compass (center) */}
          {compassEntities.length > 0 && (
            <div className="lg:w-1/4 min-w-0 min-h-[300px] lg:min-h-0">
              <PoliticalCompass entities={compassEntities} size={320} collapsible={false} />
            </div>
          )}

          {/* Priority Matrix (right) */}
          <div className="lg:w-[35%] min-w-0 min-h-[300px] lg:min-h-0">
            <PriorityMatrix
              issues={campaignIssues}
              onSelectIssue={(id) => handleCampaignSelect(id)}
              selectedIssueId={selectedCampaignId}
            />
          </div>
        </div>

        {/* Bottom row: Allied Orgs + Pipeline | Campaigns | Next Steps */}
        <div className="flex flex-col lg:flex-row gap-3 lg:flex-1 lg:min-h-0" style={{ flex: '1 1 50%' }}>
          {/* Allied Orgs + Engagement Pipeline (like Location panel) */}
          <div className="lg:w-2/5 min-w-0 min-h-[300px] lg:min-h-0">
            <div className="bg-bg-panel border border-border rounded-lg p-4 panel-hover h-full flex flex-col overflow-hidden">
              {/* Scrollable content */}
              <div className="flex-1 overflow-y-auto min-h-0">
                {/* Allied Organizations */}
                <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide mb-2">
                  ALLIED ORGANIZATIONS
                </h2>
                <div className="space-y-2 mb-4">
                  {org.aligned_organizations?.map((ally, i) => (
                    <div key={i} className="flex items-start gap-2 text-sm">
                      <span className="text-accent-green mt-0.5">●</span>
                      <div>
                        {ally.internal_id ? (
                          <Link
                            to={`/org/${ally.internal_id}`}
                            className="text-text-primary font-medium hover:text-accent-blue transition-colors"
                          >
                            {ally.name} <span className="text-accent-blue text-xs">&rarr;</span>
                          </Link>
                        ) : ally.url ? (
                          <a
                            href={ally.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-text-primary font-medium hover:text-accent-blue transition-colors"
                          >
                            {ally.name} <span className="text-text-tertiary text-xs">↗</span>
                          </a>
                        ) : (
                          <span className="text-text-primary font-medium">{ally.name}</span>
                        )}
                        <span className="text-text-tertiary"> — {ally.relationship}</span>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Engagement Pipeline */}
                <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide mb-3">
                  ENGAGEMENT PIPELINE
                </h2>
                <EngagementPipeline pipeline={org.engagement_pipeline} />
              </div>
            </div>
          </div>

          {/* Active Campaigns (like Issues feed) */}
          <div className="lg:w-[30%] min-w-0 min-h-[300px] lg:min-h-0">
            <div className="bg-bg-panel border border-border rounded-lg p-3 panel-hover h-full flex flex-col overflow-hidden">
              <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide mb-3">
                ACTIVE CAMPAIGNS
              </h2>
              <div className="flex-1 overflow-y-auto min-h-0">
                <CampaignList
                  campaigns={org.active_campaigns}
                  selectedId={selectedCampaignId}
                  onSelect={handleCampaignSelect}
                />
              </div>
            </div>
          </div>

          {/* Org Next Steps (like Next Steps) */}
          <div className="lg:w-[30%] min-w-0 min-h-[300px] lg:min-h-0">
            <OrgNextSteps steps={org.practical_next_steps_for_org} />
          </div>
        </div>
      </div>

      {/* Campaign Detail Modal */}
      <DetailModal
        open={campaignModalOpen}
        onClose={() => setCampaignModalOpen(false)}
        title="ACTIVE CAMPAIGNS"
        tabs={campaignTabs}
        activeTab={selectedCampaignId}
        onTabChange={setSelectedCampaignId}
      >
        <CampaignDetail campaign={selectedCampaign} />
      </DetailModal>
    </div>
  )
}
