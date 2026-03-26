import AiGeneratedBadge from '../shared/AiGeneratedBadge'
import ContextTooltip from '../shared/ContextTooltip'
import CopyPromptButton from '../shared/CopyPromptButton'

const IMPACT_COLORS = {
  'very high': 'text-accent-red',
  high: 'text-accent-amber',
  medium: 'text-text-secondary',
}

const STEP_CONTEXT = {
  'Set up candidate questionnaire for D1 race': 'Open seat — 8-year opportunity. Field not yet solidified. Early engagement has maximum leverage on candidate positioning.',
  'Draft Pct 4 runoff endorsement analysis': 'Low-turnout runoff. Organized endorsement from a credible group carries disproportionate weight with the small electorate that shows up.',
  'Recruit 10 volunteers for Pct 4 canvassing': 'In an 8-12% turnout election, 10 door-knockers covering key precincts can shift the margin. This is the single highest-leverage volunteer activity available right now.',
  'Prepare testimony toolkit for golf course rezoning hearings': 'Pro-housing testimony at rezoning hearings is where the rubber meets the road. A toolkit lowers the barrier for supporters to show up and speak effectively.',
  'Build coalition with AURA for November council elections': 'Combined endorsement slate across Districts 1, 3, 5, 8, 9 would have significant influence. Coalition-building takes months — starting now is critical.',
}

function StepCard({ step, index }) {
  const impactClass = IMPACT_COLORS[step.impact] || 'text-text-tertiary'
  const context = STEP_CONTEXT[step.action]

  return (
    <div className="border border-border rounded p-2.5 bg-bg-elevated">
      <div className="flex items-start gap-2">
        <span className="text-accent-blue font-mono text-xs mt-0.5 flex-shrink-0">
          {String.fromCharCode(10122 + index)}
        </span>
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <span className="text-sm text-text-primary">{step.action}</span>
            <span className={`text-xs font-mono whitespace-nowrap ${impactClass}`}>
              {step.impact?.toUpperCase()}
            </span>
          </div>
          <div className="flex flex-wrap gap-2 mt-1 text-xs text-text-tertiary">
            {step.owner && <span>{step.owner}</span>}
            {step.deadline && <span>Due: {step.deadline}</span>}
            {step.timeframe && <span>{step.timeframe}</span>}
            {step.effort && <span>{step.effort}</span>}
          </div>
          {step.notes && (
            <p className="text-xs text-text-tertiary mt-1 italic">{step.notes}</p>
          )}
          {context && (
            <div className="mt-1">
              <ContextTooltip text={context} />
            </div>
          )}
          {step.llm_prompt && (
            <div className="mt-1">
              <CopyPromptButton prompt={step.llm_prompt} />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default function OrgNextSteps({ steps }) {
  if (!steps) return null

  let globalIdx = 0

  return (
    <div className="bg-bg-panel border border-border rounded-lg p-4 panel-hover h-full flex flex-col overflow-hidden">
      <div className="flex items-center gap-2 mb-3">
        <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide">
          PRACTICAL NEXT STEPS FOR THE ORGANIZATION
        </h2>
        <AiGeneratedBadge />
      </div>

      <div className="flex-1 overflow-y-auto min-h-0">
      {steps.immediate?.length > 0 && (
        <div className="mb-3">
          <h3 className="font-mono text-xs font-bold text-text-tertiary tracking-wide mb-2">IMMEDIATE</h3>
          <div className="space-y-2">
            {steps.immediate.map((step, i) => (
              <StepCard key={i} step={step} index={globalIdx++} />
            ))}
          </div>
        </div>
      )}

      {steps.medium_term?.length > 0 && (
        <div className="mb-3">
          <h3 className="font-mono text-xs font-bold text-text-tertiary tracking-wide mb-2">MEDIUM TERM</h3>
          <div className="space-y-2">
            {steps.medium_term.map((step, i) => (
              <StepCard key={i} step={step} index={globalIdx++} />
            ))}
          </div>
        </div>
      )}

      {steps.strategic?.length > 0 && (
        <div>
          <h3 className="font-mono text-xs font-bold text-text-tertiary tracking-wide mb-2">STRATEGIC</h3>
          <div className="space-y-2">
            {steps.strategic.map((step, i) => (
              <StepCard key={i} step={step} index={globalIdx++} />
            ))}
          </div>
        </div>
      )}
      </div>
    </div>
  )
}
