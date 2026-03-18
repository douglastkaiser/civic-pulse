import { useState } from 'react'
import ContextTooltip from '../shared/ContextTooltip'

const priorityColor = {
  high: 'text-accent-red',
  medium: 'text-accent-amber',
  low: 'text-accent-green',
}

const ACTION_CONTEXT = {
  'Monitor for public hearing schedule announcement': 'Rezoning hearings are where the decision actually gets made. Missing the announcement means missing the opportunity to organize testimony.',
  'Prepare template public comment supporting residential/mixed-use zoning': 'Template comments lower the barrier for supporters to participate. Quantity of comments matters — it signals organized support to council members.',
  'Coordinate with AURA on joint advocacy strategy': 'Coalition testimony carries more weight than individual orgs. AURA has deeper policy expertise; we bring grassroots energy.',
  'Draft housing policy questionnaire for D1 candidates': 'Early engagement locks candidates into positions before they calibrate to the median voter. A public questionnaire creates accountability.',
  'Schedule meet-and-greets with declared candidates': 'Face time with candidates builds relationships that translate to access after the election.',
  'Identify and recruit potential pro-housing candidate if current field is insufficient': 'If no candidate is pro-housing, the entire 8-year council term is a lost opportunity for this district.',
  'Research both candidates\' positions on development': 'Informed endorsement requires understanding both candidates\' actual positions, not assumptions.',
  'Prepare endorsement recommendation': 'A credible endorsement from an organized group carries disproportionate weight in low-turnout runoffs.',
  'Organize precinct-level voter outreach (target: 5-10 volunteers, 4 weekends)': 'In a runoff with 8-12% turnout, a team of 10 doing door-knocking can shift the outcome. This is the highest-leverage volunteer activity.',
}

export default function CampaignDetail({ campaign }) {
  const [contextExpanded, setContextExpanded] = useState(false)

  if (!campaign) {
    return (
      <div className="flex items-center justify-center h-full text-text-tertiary text-sm font-mono">
        Select a campaign to view details
      </div>
    )
  }

  return (
    <div className="space-y-3 animate-fade-in">
      <div>
        <h3 className="text-base font-semibold text-text-primary">{campaign.title}</h3>
        <div className="flex items-center gap-3 mt-1 text-xs font-mono">
          <span className="text-text-tertiary">
            STATUS: <span className="text-text-secondary">{campaign.status?.charAt(0).toUpperCase() + campaign.status?.slice(1)}</span>
          </span>
          <span className="text-text-tertiary">
            PRIORITY: <span className={priorityColor[campaign.priority] || 'text-text-secondary'}>{campaign.priority?.toUpperCase()}</span>
          </span>
        </div>
      </div>

      <p className="text-sm text-text-secondary leading-relaxed">{campaign.summary}</p>

      {/* Theory of Change / Context */}
      <div className="border border-border rounded bg-bg-elevated">
        <button
          onClick={() => setContextExpanded(!contextExpanded)}
          className="w-full flex items-center justify-between px-3 py-2 text-left hover:bg-bg-panel transition-colors"
        >
          <span className="font-mono text-xs font-bold text-text-tertiary">THEORY OF CHANGE</span>
          <span className="text-xs text-text-tertiary">{contextExpanded ? '▾' : '▸'}</span>
        </button>
        {contextExpanded && (
          <div className="px-3 pb-3 text-xs text-text-secondary leading-relaxed section-content">
            {campaign.theory_of_change || `This campaign targets a specific decision point where organized action can shift outcomes. The strategy combines public testimony, coalition building, and voter mobilization to create maximum pressure at the moment of decision.`}
          </div>
        )}
      </div>

      {/* Next Actions */}
      {campaign.next_actions?.length > 0 && (
        <div>
          <h4 className="font-mono text-xs font-bold text-text-tertiary tracking-wide mb-2">NEXT ACTIONS</h4>
          <div className="space-y-2">
            {campaign.next_actions.map((action, i) => (
              <div key={i} className="flex items-start gap-2 p-2 rounded border border-border bg-bg-elevated">
                <span className="text-accent-blue font-mono text-xs mt-0.5 flex-shrink-0">
                  {String.fromCharCode(10122 + i)}
                </span>
                <div className="flex-1">
                  <span className="text-sm text-text-primary">{action}</span>
                  {ACTION_CONTEXT[action] && (
                    <div className="flex items-start gap-1 mt-1">
                      <ContextTooltip text={ACTION_CONTEXT[action]} />
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
