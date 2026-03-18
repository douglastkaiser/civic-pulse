import { useState, useMemo } from 'react'
import ContextTooltip from './shared/ContextTooltip'

const QUADRANT_COLORS = {
  act_now: '#22c55e',
  know: '#3b82f6',
  watch: '#f59e0b',
  background: '#475569',
}

const SORT_OPTIONS = [
  { key: 'importance', label: 'Importance' },
  { key: 'impact', label: 'Impact' },
  { key: 'date', label: 'Date' },
]

export default function IssueFeed({ issues, onSelectIssue, selectedIssueId }) {
  const [sortBy, setSortBy] = useState('importance')

  const sorted = useMemo(() => {
    if (!issues?.length) return []
    return [...issues].sort((a, b) => {
      if (sortBy === 'importance') return b.importance_score - a.importance_score
      if (sortBy === 'impact') return b.impact_score - a.impact_score
      if (sortBy === 'date') {
        if (!a.meeting_date) return 1
        if (!b.meeting_date) return -1
        return new Date(a.meeting_date) - new Date(b.meeting_date)
      }
      return 0
    })
  }, [issues, sortBy])

  if (!issues?.length) {
    return (
      <div className="bg-bg-panel border border-border rounded-lg p-4 flex flex-col h-full panel-hover">
        <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide mb-3">
          ISSUES
        </h2>
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="text-text-tertiary text-sm font-mono">No issues scraped yet</div>
            <div className="text-text-tertiary text-xs mt-1">Run pipeline to populate.</div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-bg-panel border border-border rounded-lg p-3 flex flex-col h-full overflow-hidden panel-hover">
      <div className="flex items-center justify-between mb-2">
        <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide">
          ISSUES
        </h2>
        <div className="flex gap-1">
          {SORT_OPTIONS.map((opt) => (
            <button
              key={opt.key}
              onClick={() => setSortBy(opt.key)}
              className={`text-xs font-mono px-1.5 py-0.5 rounded transition-colors ${
                sortBy === opt.key
                  ? 'bg-accent-blue/20 text-accent-blue'
                  : 'text-text-tertiary hover:text-text-secondary'
              }`}
            >
              {opt.label}
            </button>
          ))}
        </div>
      </div>
      <div className="flex-1 overflow-y-auto space-y-1 min-h-0">
        {sorted.map((issue) => (
          <button
            key={issue.id}
            onClick={() => onSelectIssue?.(issue.id)}
            className={`w-full text-left px-2.5 py-2 rounded border transition-colors ${
              issue.id === selectedIssueId
                ? 'bg-bg-elevated border-accent-blue/50'
                : 'border-transparent hover:bg-bg-elevated hover:border-border'
            }`}
          >
            <div className="flex items-start gap-2">
              <span
                className="mt-1.5 rounded-full flex-shrink-0"
                style={{
                  width: 8,
                  height: 8,
                  backgroundColor: QUADRANT_COLORS[issue.quadrant] || '#475569',
                }}
              />
              <div className="flex-1 min-w-0">
                <div className="text-sm text-text-primary truncate">{issue.title}</div>
                <div className="flex items-center gap-2 mt-0.5 text-xs text-text-tertiary">
                  <span>{issue.governing_body}</span>
                  {issue.meeting_date && (
                    <>
                      <span>·</span>
                      <span>{issue.meeting_date}</span>
                    </>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-1.5 flex-shrink-0 text-xs font-mono">
                <span className="text-text-secondary">
                  I:{issue.importance_score}
                </span>
                <span className="text-text-tertiary">
                  M:{issue.impact_score}
                </span>
                <ContextTooltip text="I: Importance — how much this issue affects your stated priorities. M: Impact — how much influence you can have on the outcome." />
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}
