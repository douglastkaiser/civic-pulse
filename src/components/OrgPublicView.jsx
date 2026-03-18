import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { loadOrg } from '../lib/data'

const priorityColor = {
  high: 'text-accent-red',
  medium: 'text-accent-amber',
  low: 'text-accent-green',
}

const statusDot = {
  active: 'bg-accent-green',
  planning: 'bg-accent-blue',
  completed: 'bg-text-tertiary',
}

export default function OrgPublicView() {
  const { orgId } = useParams()
  const [org, setOrg] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    loadOrg(orgId)
      .then((data) => { setOrg(data); setLoading(false) })
      .catch(() => { setError('Organization not found'); setLoading(false) })
  }, [orgId])

  if (loading) {
    return (
      <div className="min-h-screen bg-bg-primary flex items-center justify-center">
        <div className="font-mono text-text-secondary text-sm animate-pulse">Loading...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-bg-primary flex items-center justify-center">
        <p className="text-text-secondary font-mono">{error}</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-bg-primary">
      <div className="max-w-2xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="font-mono text-2xl font-bold text-text-primary tracking-wide">
            {org.name}
          </h1>
          <p className="text-base text-text-secondary italic mt-1">{org.tagline}</p>
          <div className="flex items-center justify-center gap-2 mt-2 text-xs text-text-tertiary font-mono">
            <span>{org.geographic_scope?.city}, {org.geographic_scope?.state}</span>
            {org.founded && <span>· Est. {org.founded}</span>}
          </div>
        </div>

        {/* Mission */}
        <div className="bg-bg-panel border border-border rounded-lg p-6 mb-6">
          <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide mb-3">OUR MISSION</h2>
          <p className="text-sm text-text-secondary leading-relaxed">{org.mission}</p>
        </div>

        {/* Key Positions */}
        <div className="bg-bg-panel border border-border rounded-lg p-6 mb-6">
          <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide mb-3">WHAT WE STAND FOR</h2>
          <ul className="space-y-2">
            {org.key_policy_positions?.map((pos, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-text-secondary">
                <span className="text-accent-purple mt-0.5">▸</span>
                <span>{pos}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Active Campaigns */}
        <div className="bg-bg-panel border border-border rounded-lg p-6 mb-6">
          <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide mb-3">ACTIVE CAMPAIGNS</h2>
          <div className="space-y-4">
            {org.active_campaigns?.map((campaign) => (
              <div key={campaign.id} className="border border-border rounded p-4 bg-bg-elevated">
                <div className="flex items-center gap-2 mb-2">
                  <span className={`w-2 h-2 rounded-full ${statusDot[campaign.status] || 'bg-text-tertiary'}`} />
                  <span className="text-sm font-medium text-text-primary">{campaign.title}</span>
                  <span className={`text-xs font-mono ml-auto ${priorityColor[campaign.priority]}`}>
                    {campaign.priority?.toUpperCase()}
                  </span>
                </div>
                <p className="text-xs text-text-secondary leading-relaxed">{campaign.summary}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Get Involved */}
        <div className="bg-bg-panel border border-border rounded-lg p-6 mb-6">
          <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide mb-3">GET INVOLVED</h2>
          {org.engagement_pipeline && (
            <div className="space-y-3">
              <div>
                <span className="font-mono text-xs text-accent-blue">LEARN</span>
                <p className="text-sm text-text-secondary mt-0.5">{org.engagement_pipeline.awareness}</p>
              </div>
              <div>
                <span className="font-mono text-xs text-accent-green">ENGAGE</span>
                <p className="text-sm text-text-secondary mt-0.5">{org.engagement_pipeline.interest}</p>
              </div>
              <div>
                <span className="font-mono text-xs text-accent-amber">ACT</span>
                <p className="text-sm text-text-secondary mt-0.5">{org.engagement_pipeline.action}</p>
              </div>
              <div>
                <span className="font-mono text-xs text-accent-purple">LEAD</span>
                <p className="text-sm text-text-secondary mt-0.5">{org.engagement_pipeline.leadership}</p>
              </div>
            </div>
          )}
        </div>

        {/* Allies */}
        {org.aligned_organizations?.length > 0 && (
          <div className="bg-bg-panel border border-border rounded-lg p-6 mb-6">
            <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide mb-3">OUR ALLIES</h2>
            <div className="space-y-2">
              {org.aligned_organizations.map((ally, i) => (
                <div key={i} className="text-sm text-text-secondary">
                  <span className="text-text-primary font-medium">{ally.name}</span>
                  <span className="text-text-tertiary"> — {ally.relationship}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center text-xs text-text-tertiary font-mono mt-8">
          Powered by <span className="text-text-secondary">CIVIC PULSE</span>
        </div>
      </div>
    </div>
  )
}
