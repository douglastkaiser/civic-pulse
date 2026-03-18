import { useState } from 'react'
import AiGeneratedBadge from './shared/AiGeneratedBadge'

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
  const [manifestoExpanded, setManifestoExpanded] = useState(false)

  if (!profile) return null

  const { manifesto, manifesto_inputs_complete, political_context } = profile

  return (
    <div className="bg-bg-panel border border-border rounded-lg p-4 flex flex-col h-full overflow-hidden panel-hover">
      {/* Header — always visible */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide">
            MANIFESTO
          </h2>
          <AiGeneratedBadge />
        </div>
        {political_context?.party_lean && (
          <span className="text-xs text-text-tertiary font-mono">
            {political_context.party_lean}
          </span>
        )}
      </div>

      {!manifesto_inputs_complete && (
        <div className="mb-2 px-3 py-1.5 bg-accent-amber/10 border border-accent-amber/30 rounded text-xs text-accent-amber font-mono">
          DRAFT — Profile Incomplete
        </div>
      )}

      {/* Always-visible summary + identity tags */}
      {manifesto?.manifesto_summary && (
        <p className="text-sm text-text-primary leading-relaxed font-medium mb-2">
          {manifesto.manifesto_summary}
        </p>
      )}

      {manifesto?.identity_tags?.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mb-3">
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

      {/* Scrollable collapsible sections */}
      <div className="flex-1 overflow-y-auto space-y-2 min-h-0">
        {/* Full Manifesto — collapsible */}
        {manifesto?.narrative && (
          <div className="border border-border rounded bg-bg-elevated">
            <button
              onClick={() => setManifestoExpanded(!manifestoExpanded)}
              className="w-full flex items-center justify-between px-3 py-2 text-left hover:bg-bg-panel transition-colors"
            >
              <span className="font-mono text-xs font-bold text-text-tertiary tracking-wide">FULL MANIFESTO</span>
              <span className="text-xs text-text-tertiary">{manifestoExpanded ? '▾' : '▸'}</span>
            </button>
            {manifestoExpanded && (
              <div className="px-3 pb-3 text-sm text-text-secondary leading-relaxed whitespace-pre-wrap section-content">
                {manifesto.narrative}
              </div>
            )}
          </div>
        )}

        {/* Positions — each independently collapsible */}
        {manifesto?.issue_positions?.length > 0 && (
          <div className="space-y-1.5">
            <h3 className="font-mono text-xs font-bold text-text-tertiary tracking-wide px-1">
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
