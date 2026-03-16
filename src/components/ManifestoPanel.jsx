import { useState } from 'react'

function PositionCard({ position }) {
  const [expanded, setExpanded] = useState(false)

  return (
    <div className="border border-border rounded bg-bg-elevated">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between px-3 py-2 text-left hover:bg-bg-panel transition-colors"
      >
        <span className="text-sm font-medium text-text-primary">{position.domain}</span>
        <span className="text-xs text-text-tertiary">{expanded ? '▾' : '▸'}</span>
      </button>
      {expanded && (
        <div className="px-3 pb-3 space-y-2 text-xs">
          <div>
            <span className="text-text-tertiary">Stance: </span>
            <span className="text-text-primary">{position.stance}</span>
          </div>
          {position.local_implication && (
            <div>
              <span className="text-text-tertiary">Local: </span>
              <span className="text-text-secondary">{position.local_implication}</span>
            </div>
          )}
          {position.likely_allies && (
            <div>
              <span className="text-accent-green">Allies: </span>
              <span className="text-text-secondary">{position.likely_allies}</span>
            </div>
          )}
          {position.likely_friction && (
            <div>
              <span className="text-accent-amber">Friction: </span>
              <span className="text-text-secondary">{position.likely_friction}</span>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default function ManifestoPanel({ profile }) {
  if (!profile) return null

  const { manifesto, manifesto_inputs_complete, political_context } = profile

  return (
    <div className="bg-bg-panel border border-border rounded-lg p-4 flex flex-col h-full overflow-hidden">
      <div className="flex items-center justify-between mb-3">
        <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide">
          MANIFESTO
        </h2>
        {political_context?.party_lean && (
          <span className="text-xs text-text-tertiary font-mono">
            {political_context.party_lean}
          </span>
        )}
      </div>

      {!manifesto_inputs_complete && (
        <div className="mb-3 px-3 py-1.5 bg-accent-amber/10 border border-accent-amber/30 rounded text-xs text-accent-amber font-mono">
          DRAFT — Profile Incomplete
        </div>
      )}

      <div className="flex-1 overflow-y-auto space-y-4 min-h-0">
        {/* Identity Tags */}
        {manifesto?.identity_tags?.length > 0 && (
          <div className="flex flex-wrap gap-1.5">
            {manifesto.identity_tags.map((tag) => (
              <span
                key={tag}
                className="px-2 py-0.5 text-xs rounded-full bg-accent-blue/15 text-accent-blue border border-accent-blue/30"
              >
                {tag}
              </span>
            ))}
          </div>
        )}

        {/* Narrative */}
        {manifesto?.narrative && (
          <div className="text-sm text-text-secondary leading-relaxed whitespace-pre-wrap">
            {manifesto.narrative}
          </div>
        )}

        {/* Issue Positions */}
        {manifesto?.issue_positions?.length > 0 && (
          <div className="space-y-1.5">
            <h3 className="font-mono text-xs font-bold text-text-tertiary tracking-wide">
              POSITIONS
            </h3>
            {manifesto.issue_positions.map((pos) => (
              <PositionCard key={pos.domain} position={pos} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
