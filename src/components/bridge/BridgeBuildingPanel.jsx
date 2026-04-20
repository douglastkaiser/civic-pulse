function SectionList({ title, items }) {
  if (!items || items.length === 0) return null

  return (
    <div>
      <h5 className="font-mono text-[11px] font-bold text-text-tertiary tracking-wide uppercase mb-1.5">
        {title}
      </h5>
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

export default function BridgeBuildingPanel({
  bridge,
  header = 'BRIDGE BUILDING',
  sectionTitle,
  className = '',
}) {
  if (!bridge) return null

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
          {sectionTitle && (
            <h4 className="font-mono text-xs font-bold text-text-primary tracking-wide">{sectionTitle}</h4>
          )}

          {bridge.opposition_steelman && (
            <div>
              <h5 className="font-mono text-[11px] font-bold text-text-tertiary tracking-wide uppercase mb-1.5">
                Steelman
              </h5>
              <p className="text-xs text-text-secondary leading-relaxed">{bridge.opposition_steelman}</p>
            </div>
          )}

          {crossPartisanAppeals.length > 0 && (
            <div>
              <h5 className="font-mono text-[11px] font-bold text-text-tertiary tracking-wide uppercase mb-1.5">
                Cross-Partisan Appeals
              </h5>
              <div className="space-y-2">
                {crossPartisanAppeals.map((appeal, idx) => (
                  <div key={idx} className="border border-border rounded p-2 bg-bg-panel/60">
                    {appeal.audience && (
                      <p className="text-[11px] font-mono text-accent-purple mb-1">{appeal.audience}</p>
                    )}
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

          <SectionList title="Common Ground" items={bridge.common_ground} />
          <SectionList title="Traps" items={bridge.conversation_traps_to_avoid} />
          <SectionList title="Uncertainty" items={bridge.when_to_acknowledge_uncertainty} />
          <SectionList title="Limits" items={bridge.honest_limits} />
        </div>
      </details>
    </div>
  )
}
