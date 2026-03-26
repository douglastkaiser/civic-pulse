import AiGeneratedBadge from './shared/AiGeneratedBadge'
import ContextTooltip from './shared/ContextTooltip'
import CopyPromptButton from './shared/CopyPromptButton'

const IMPACT_COLORS = {
  HIGH: 'bg-accent-red/15 text-accent-red border-accent-red/30',
  'VERY HIGH': 'bg-accent-red/20 text-accent-red border-accent-red/40',
  MEDIUM: 'bg-accent-amber/15 text-accent-amber border-accent-amber/30',
  'LOW EFFORT, ONGOING VALUE': 'bg-accent-green/15 text-accent-green border-accent-green/30',
}

function getImpactClasses(impact) {
  return IMPACT_COLORS[impact] || 'bg-bg-elevated text-text-secondary border-border'
}

function StepItem({ step, index }) {
  return (
    <div className="flex gap-2.5 py-2 border-b border-border last:border-b-0">
      <span className="text-xs font-mono text-text-tertiary mt-0.5 flex-shrink-0 w-4 text-right">
        {index}
      </span>
      <div className="flex-1 min-w-0">
        <div className="text-sm text-text-primary">{step.action}</div>
        {step.detail && (
          <div className="text-xs text-text-secondary mt-0.5 leading-relaxed">
            {step.detail}
          </div>
        )}
        <div className="flex flex-wrap gap-1.5 mt-1">
          {step.time && (
            <span className="px-1.5 py-0.5 text-xs rounded bg-bg-elevated text-text-tertiary border border-border font-mono">
              {step.time}
            </span>
          )}
          {step.impact && (
            <span
              className={`px-1.5 py-0.5 text-xs rounded border font-mono ${getImpactClasses(step.impact)}`}
            >
              {step.impact}
            </span>
          )}
        </div>
        {step.reason && (
          <div className="text-xs text-text-tertiary mt-1 italic">{step.reason}</div>
        )}
        {step.llm_prompt && (
          <div className="mt-1">
            <CopyPromptButton prompt={step.llm_prompt} />
          </div>
        )}
      </div>
    </div>
  )
}

function StepSection({ title, steps, startIndex }) {
  if (!steps?.length) return null
  return (
    <div className="mb-3 last:mb-0">
      <h3 className="font-mono text-xs font-bold text-text-tertiary tracking-wide mb-1">
        {title}
      </h3>
      {steps.map((step, i) => (
        <StepItem key={i} step={step} index={startIndex + i} />
      ))}
    </div>
  )
}

export default function NextStepsPanel({ profile }) {
  const steps = profile?.next_steps

  return (
    <div className="bg-bg-panel border border-border rounded-lg p-4 flex flex-col h-full overflow-hidden panel-hover">
      <div className="flex items-center gap-2 mb-3">
        <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide">
          NEXT STEPS
        </h2>
        <AiGeneratedBadge />
        <ContextTooltip text="These actions are recommended based on your values, your location, current political opportunities, and effort-to-impact ratio. They are ordered by a combination of urgency and leverage." />
      </div>
      {steps ? (
        <div className="flex-1 overflow-y-auto min-h-0">
          <StepSection
            title="IMMEDIATE (THIS WEEK)"
            steps={steps.immediate}
            startIndex={1}
          />
          <StepSection
            title="THIS MONTH"
            steps={steps.this_month}
            startIndex={(steps.immediate?.length || 0) + 1}
          />
          <StepSection
            title="MEDIUM TERM (NEXT 90 DAYS)"
            steps={steps.medium_term}
            startIndex={
              (steps.immediate?.length || 0) + (steps.this_month?.length || 0) + 1
            }
          />
          <StepSection
            title="STRATEGIC OPPORTUNITIES"
            steps={steps.strategic}
            startIndex={
              (steps.immediate?.length || 0) +
              (steps.this_month?.length || 0) +
              (steps.medium_term?.length || 0) +
              1
            }
          />
        </div>
      ) : (
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="text-text-tertiary text-sm font-mono">
              Next steps not yet generated
            </div>
            <div className="text-text-tertiary text-xs mt-1">
              Complete the profile questionnaire and run the pipeline.
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
