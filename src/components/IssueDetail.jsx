const QUADRANT_LABELS = {
  act_now: { label: 'ACT NOW', color: 'text-quad-act' },
  know: { label: 'KNOW', color: 'text-quad-know' },
  watch: { label: 'WATCH', color: 'text-quad-watch' },
  background: { label: 'BACKGROUND', color: 'text-quad-bg' },
}

export default function IssueDetail({ issue, onClose }) {
  if (!issue) return null

  const quadrant = QUADRANT_LABELS[issue.quadrant] || QUADRANT_LABELS.background

  return (
    <div className="bg-bg-panel border border-border rounded-lg p-4 flex flex-col h-full overflow-hidden">
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className={`font-mono text-xs font-bold ${quadrant.color}`}>
              {quadrant.label}
            </span>
            <span className="text-xs text-text-tertiary font-mono">
              I:{issue.importance_score} M:{issue.impact_score}
            </span>
          </div>
          <h3 className="text-base font-semibold text-text-primary">{issue.title}</h3>
        </div>
        <button
          onClick={onClose}
          className="text-text-tertiary hover:text-text-primary text-sm ml-2 flex-shrink-0"
        >
          ✕
        </button>
      </div>

      <div className="flex-1 overflow-y-auto space-y-3 min-h-0">
        {/* Meta row */}
        <div className="flex flex-wrap gap-2 text-xs">
          <span className="px-2 py-0.5 rounded bg-bg-elevated text-text-secondary border border-border">
            {issue.governing_body}
          </span>
          <span className="px-2 py-0.5 rounded bg-bg-elevated text-text-secondary border border-border">
            {issue.decision_type}
          </span>
          <span className="px-2 py-0.5 rounded bg-bg-elevated text-text-secondary border border-border">
            {issue.geographic_scope}
          </span>
          {issue.estimated_contestedness && (
            <span
              className={`px-2 py-0.5 rounded border ${
                issue.estimated_contestedness === 'high'
                  ? 'bg-accent-red/10 text-accent-red border-accent-red/30'
                  : issue.estimated_contestedness === 'medium'
                    ? 'bg-accent-amber/10 text-accent-amber border-accent-amber/30'
                    : 'bg-bg-elevated text-text-secondary border-border'
              }`}
            >
              {issue.estimated_contestedness} contestedness
            </span>
          )}
        </div>

        {/* Policy Domains */}
        {issue.policy_domains?.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {issue.policy_domains.map((d) => (
              <span
                key={d}
                className="px-1.5 py-0.5 text-xs rounded bg-accent-purple/10 text-accent-purple border border-accent-purple/20"
              >
                {d}
              </span>
            ))}
          </div>
        )}

        {/* Summary */}
        <div className="text-sm text-text-secondary leading-relaxed">{issue.summary}</div>

        {/* Why it matters */}
        {issue.why_it_matters_to_you && (
          <div className="bg-bg-elevated rounded p-3 border border-border">
            <div className="font-mono text-xs font-bold text-accent-green mb-1">
              WHY THIS MATTERS TO YOU
            </div>
            <div className="text-xs text-text-secondary leading-relaxed">
              {issue.why_it_matters_to_you}
            </div>
          </div>
        )}

        {/* Public Comment */}
        {issue.public_comment && (
          <div className="bg-bg-elevated rounded p-3 border border-border">
            <div className="font-mono text-xs font-bold text-text-tertiary mb-1">
              PUBLIC COMMENT
            </div>
            <div className="text-xs text-text-secondary">
              {issue.public_comment.available ? (
                <>
                  <span className="text-accent-green">Available</span>
                  {issue.public_comment.deadline && (
                    <span> — Deadline: {issue.public_comment.deadline}</span>
                  )}
                  {issue.public_comment.instructions && (
                    <div className="mt-1">{issue.public_comment.instructions}</div>
                  )}
                </>
              ) : (
                <>
                  <span className="text-text-tertiary">Not applicable</span>
                  {issue.public_comment.instructions && (
                    <div className="mt-1">{issue.public_comment.instructions}</div>
                  )}
                </>
              )}
            </div>
          </div>
        )}

        {/* Meeting Date */}
        {issue.meeting_date && (
          <div className="text-xs text-text-tertiary">
            Meeting/Election date: {new Date(issue.meeting_date).toLocaleDateString('en-US', {
              weekday: 'long',
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </div>
        )}

        {/* Source */}
        {issue.source_url && (
          <a
            href={issue.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs text-accent-blue hover:underline"
          >
            Source →
          </a>
        )}
      </div>
    </div>
  )
}
