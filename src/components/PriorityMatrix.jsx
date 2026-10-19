import { useState } from 'react'
import ContextTooltip from './shared/ContextTooltip'
import DetailModal from './shared/DetailModal'

function MatrixPlot({ issues, selectedIssueId, onSelectIssue }) {
  const scored = (issues || []).filter(i => Number.isFinite(i.importance_score) && Number.isFinite(i.impact_score))
  return <div className="w-full h-full overflow-auto">
    <svg viewBox="0 0 400 280" className="w-full max-h-96" role="img" aria-label="Archived importance and impact scores; use the issue list below to select a record.">
      <rect x="40" y="10" width="340" height="230" fill="rgb(var(--bg-elevated))" rx="8" />
      <path d="M210 10V240M40 125H380" stroke="rgb(var(--border))" strokeDasharray="4" />
      <text x="210" y="270" textAnchor="middle" fill="rgb(var(--text-secondary))" fontSize="12">Recorded importance</text>
      <text x="15" y="125" transform="rotate(-90, 15, 125)" textAnchor="middle" fill="rgb(var(--text-secondary))" fontSize="12">Recorded impact estimate</text>
      {scored.map(issue => <circle key={issue.id} cx={40 + Math.max(0, Math.min(100, issue.importance_score)) * 3.4} cy={240 - Math.max(0, Math.min(100, issue.impact_score)) * 2.3} r={issue.id === selectedIssueId ? 7 : 5} fill="rgb(var(--accent-blue))" opacity=".75"><title>{issue.title}: importance {issue.importance_score}, impact {issue.impact_score}</title></circle>)}
    </svg>
    <ul className="text-sm space-y-1">{scored.map(issue => <li key={issue.id}><button className={`text-left px-2 py-1 rounded ${issue.id === selectedIssueId ? 'bg-accent-blue/10' : ''}`} onClick={() => onSelectIssue?.(issue.id)}>{issue.title} · {issue.importance_score} / {issue.impact_score}</button></li>)}</ul>
    {!scored.length && <p className="text-sm text-text-secondary p-3">No archived scores are available. Explore the source records to choose an action.</p>}
  </div>
}

export default function PriorityMatrix({ issues, onSelectIssue, selectedIssueId }) {
  const [modalOpen, setModalOpen] = useState(false)

  return (
    <>
      <div className="bg-bg-panel border border-border rounded-lg p-3 flex flex-col h-full panel-hover">
        <div className="flex items-center gap-2 mb-2">
          <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide">
            PRIORITY MATRIX
          </h2>
          <ContextTooltip text="These archived estimates are not personalized to your current profile. They are unverified analysis, not measured influence." />
          <button
            onClick={() => setModalOpen(true)}
            className="ml-auto text-xs text-text-tertiary hover:text-accent-blue font-mono transition-colors px-1.5 py-0.5 rounded hover:bg-bg-elevated"
            title="Expand to full view"
          >
            ⤢
          </button>
        </div>
        {issues?.length > 0 ? (
          <div className="flex-1 min-h-0">
            <MatrixPlot
              issues={issues}
              selectedIssueId={selectedIssueId}
              onSelectIssue={onSelectIssue}
            />
          </div>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <div className="text-text-tertiary text-sm font-mono mb-2">No issues data</div>
              <div className="text-text-tertiary text-xs">
                Coverage is still being established for this area.
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Expanded modal view */}
      <DetailModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title="PRIORITY MATRIX"
      >
        <div className="flex items-center gap-2 mb-4">
          <ContextTooltip text="These archived estimates are not personalized to your current profile. They are unverified analysis, not measured influence." />
        </div>
        {issues?.length > 0 ? (
          <div style={{ height: '70vh' }}>
            <MatrixPlot
              issues={issues}
              selectedIssueId={selectedIssueId}
              onSelectIssue={onSelectIssue}
            />
          </div>
        ) : (
          <div className="flex items-center justify-center h-64">
            <div className="text-text-tertiary text-sm font-mono">No issues data</div>
          </div>
        )}
      </DetailModal>
    </>
  )
}
