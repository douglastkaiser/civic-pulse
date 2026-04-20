import CopyConversationStarterButton from '../shared/CopyConversationStarterButton'
import ContentProvenanceBadge from '../shared/ContentProvenanceBadge'

function SectionList({ title, items, provenance }) {
  if (!items || items.length === 0) return null

  return (
    <div>
      <div className="flex items-center justify-between gap-2 mb-1.5">
        <h5 className="font-mono text-[11px] font-bold text-text-tertiary tracking-wide uppercase">
          {title}
        </h5>
        {provenance && <ContentProvenanceBadge provenance={provenance} />}
      </div>
      <ul className="space-y-1.5">
        {items.map((item, idx) => (
          <li key={idx} className="flex items-start gap-2 text-xs text-text-secondary leading-relaxed">
            <span className="text-accent-blue mt-0.5">•</span>
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}



function getSubsectionProvenance(bridge, key) {
  const sectionProvenance = bridge?.subsection_provenance
  if (!sectionProvenance || typeof sectionProvenance !== 'object') return null
  return sectionProvenance[key] || null
}

export default function BridgeBuildingPanel({
  bridge,
  header = 'BRIDGE BUILDING',
  sectionTitle,
  className = '',
}) {
  if (!bridge) return null

  const bridgeProvenance = bridge.provenance || null
  const oppositionProvenance = getSubsectionProvenance(bridge, 'opposition_steelman')
  const appealsProvenance = getSubsectionProvenance(bridge, 'cross_partisan_appeals')
  const commonGroundProvenance = getSubsectionProvenance(bridge, 'common_ground')
  const trapsProvenance = getSubsectionProvenance(bridge, 'conversation_traps_to_avoid')
  const uncertaintyProvenance = getSubsectionProvenance(bridge, 'when_to_acknowledge_uncertainty')
  const limitsProvenance = getSubsectionProvenance(bridge, 'honest_limits')

  const crossPartisanAppeals = Array.isArray(bridge.cross_partisan_appeals)
    ? bridge.cross_partisan_appeals
    : []

  return (
    <div className={`border border-border rounded bg-bg-elevated ${className}`.trim()}>
      <details>
        <summary className="px-3 py-2 text-left hover:bg-bg-panel transition-colors cursor-pointer font-mono text-xs font-bold text-text-tertiary tracking-wide">
          {header}
        </summary>
        <div className="px-3 pb-3 pt-1 space-y-3 section-content">
          <div className="flex items-center justify-between gap-2">
            {sectionTitle ? (
              <h4 className="font-mono text-xs font-bold text-text-primary tracking-wide">{sectionTitle}</h4>
            ) : (
              <span />
            )}
            <ContentProvenanceBadge provenance={bridgeProvenance} />
          </div>

          {bridge.opposition_steelman && (
            <div>
              <div className="flex items-center justify-between gap-2 mb-1.5">
                <h5 className="font-mono text-[11px] font-bold text-text-tertiary tracking-wide uppercase">
                  Steelman
                </h5>
                {oppositionProvenance && <ContentProvenanceBadge provenance={oppositionProvenance} />}
              </div>
              <p className="text-xs text-text-secondary leading-relaxed">{bridge.opposition_steelman}</p>
            </div>
          )}

          {crossPartisanAppeals.length > 0 && (
            <div>
              <div className="flex items-center justify-between gap-2 mb-1.5">
                <h5 className="font-mono text-[11px] font-bold text-text-tertiary tracking-wide uppercase">
                  Cross-Partisan Appeals
                </h5>
                {appealsProvenance && <ContentProvenanceBadge provenance={appealsProvenance} />}
              </div>
              <div className="space-y-2">
                {crossPartisanAppeals.map((appeal, idx) => (
                  <div key={idx} className="border border-border rounded p-2 bg-bg-panel/60">
                    <div className="flex items-start justify-between gap-2 mb-1">
                      {appeal.audience && (
                        <p className="text-[11px] font-mono text-accent-purple">{appeal.audience}</p>
                      )}
                      <CopyConversationStarterButton appeal={appeal} bridge={bridge} />
                    </div>
                    {appeal.framing && <p className="text-xs text-text-secondary leading-relaxed">{appeal.framing}</p>}
                    {appeal.evidence && (
                      <p className="text-[11px] text-text-tertiary leading-relaxed mt-1">Evidence: {appeal.evidence}</p>
                    )}
                    {appeal.example_dialogue && (
                      <p className="text-[11px] text-text-tertiary italic leading-relaxed mt-1">{appeal.example_dialogue}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          <SectionList title="Common Ground" items={bridge.common_ground} provenance={commonGroundProvenance} />
          <SectionList title="Traps" items={bridge.conversation_traps_to_avoid} provenance={trapsProvenance} />
          <SectionList title="Uncertainty" items={bridge.when_to_acknowledge_uncertainty} provenance={uncertaintyProvenance} />
          <SectionList title="Limits" items={bridge.honest_limits} provenance={limitsProvenance} />
        </div>
      </details>
    </div>
  )
}
