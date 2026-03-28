import { useState } from 'react'
import AiGeneratedBadge from '../shared/AiGeneratedBadge'
import { getCssVar } from '../../lib/themeColors'

function AlignmentGauge({ score }) {
  const pct = ((score + 1) / 2) * 100
  const accentGreen = getCssVar('--accent-green')
  const accentRed = getCssVar('--accent-red')
  const accentAmber = getCssVar('--accent-amber')
  const color =
    score > 0.3 ? accentGreen : score < -0.3 ? accentRed : accentAmber

  return (
    <div className="space-y-1.5">
      <div className="flex justify-between text-[9px] font-mono text-text-tertiary">
        <span>ANTAGONIST</span>
        <span>MIXED</span>
        <span>ALLY</span>
      </div>
      <div className="relative h-2.5 rounded-full overflow-hidden alignment-bar-bg">
        {/* Marker */}
        <div
          className="absolute top-1/2 -translate-y-1/2 w-3.5 h-3.5 rounded-full border-2 border-bg-panel shadow-lg transition-all duration-500 z-10"
          style={{
            left: `calc(${pct}% - 7px)`,
            background: color,
            boxShadow: `0 0 8px ${color}60`,
          }}
        />
        {/* Track */}
        <div className="absolute inset-0 rounded-full opacity-30"
          style={{ background: `linear-gradient(to right, ${accentRed}, ${accentAmber} 50%, ${accentGreen})` }}
        />
        {/* Fill */}
        <div
          className="absolute inset-y-0 left-0 rounded-full transition-all duration-500"
          style={{
            width: `${pct}%`,
            background: `linear-gradient(to right, ${accentRed}80, ${color}80)`,
          }}
        />
      </div>
      <div className="text-center">
        <span
          className="text-sm font-bold font-mono"
          style={{ color }}
        >
          {score > 0 ? '+' : ''}{score.toFixed(1)}
        </span>
      </div>
    </div>
  )
}

function Section({ title, children, defaultOpen = true, accent }) {
  const [open, setOpen] = useState(defaultOpen)
  return (
    <div className="border-b border-border last:border-b-0">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between py-2 text-left hover:text-text-secondary transition-colors"
      >
        <span className={`font-mono text-[10px] font-bold tracking-wide ${accent || 'text-text-tertiary'}`}>
          {title}
        </span>
        <span className="text-xs text-text-tertiary">{open ? '▾' : '▸'}</span>
      </button>
      {open && <div className="pb-3 section-content">{children}</div>}
    </div>
  )
}

export default function OfficialDetail({ official, onClose }) {
  if (!official) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-center p-6">
        <div className="text-3xl mb-3 opacity-30">◆</div>
        <div className="text-sm text-text-tertiary font-mono">
          Select an official to view<br />details and alignment analysis
        </div>
      </div>
    )
  }

  const score = official.alignment?.score ?? 0
  const scoreColor =
    score > 0.3 ? 'text-accent-green' : score < -0.3 ? 'text-accent-red' : 'text-accent-amber'
  const labelColor =
    score > 0.3
      ? 'bg-accent-green/15 text-accent-green border-accent-green/30'
      : score < -0.3
        ? 'bg-accent-red/15 text-accent-red border-accent-red/30'
        : 'bg-accent-amber/15 text-accent-amber border-accent-amber/30'

  const priorityColors = {
    high: 'bg-accent-green/15 text-accent-green',
    medium: 'bg-accent-amber/15 text-accent-amber',
    low: 'bg-text-tertiary/15 text-text-tertiary',
    critical: 'bg-accent-red/15 text-accent-red',
  }

  const partyFull = {
    Democrat: { label: 'Democrat', color: 'bg-accent-blue/20 text-accent-blue border-accent-blue/30' },
    Republican: { label: 'Republican', color: 'bg-accent-red/20 text-accent-red border-accent-red/30' },
    Nonpartisan: { label: 'Nonpartisan', color: 'bg-text-tertiary/20 text-text-tertiary border-text-tertiary/30' },
    Appointed: { label: 'Appointed', color: 'bg-accent-purple/20 text-accent-purple border-accent-purple/30' },
  }

  const partyInfo = partyFull[official.party] || { label: official.party || 'Unknown', color: 'bg-gray-500/20 text-gray-400 border-gray-500/30' }

  return (
    <div className="h-full flex flex-col overflow-hidden animate-fade-in">
      {/* Header */}
      <div className="flex-shrink-0 p-4 border-b border-border">
        <div className="flex items-start justify-between gap-2">
          <div className="min-w-0">
            <h3 className="text-lg font-bold text-text-primary leading-tight">{official.name}</h3>
            <div className="text-xs text-text-secondary mt-0.5">{official.title}</div>
            {official.scope && (
              <div className="text-[10px] text-text-tertiary font-mono mt-0.5">{official.scope}</div>
            )}
          </div>
          {onClose && (
            <button
              onClick={onClose}
              className="lg:hidden text-text-tertiary hover:text-text-primary text-sm p-1 rounded hover:bg-bg-elevated transition-colors flex-shrink-0"
            >
              ✕
            </button>
          )}
        </div>

        <div className="flex flex-wrap items-center gap-1.5 mt-2">
          <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full border ${partyInfo.color}`}>
            {partyInfo.label}
          </span>
          <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full border ${labelColor}`}>
            {official.alignment?.label || 'Unknown'}
          </span>
          {official.alignment?.priority && (
            <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full ${priorityColors[official.alignment.priority]}`}>
              {official.alignment.priority.toUpperCase()} PRIORITY
            </span>
          )}
        </div>

        {official.term && (
          <div className="text-[10px] text-text-tertiary font-mono mt-2">
            Term: {new Date(official.term.start).getFullYear()} – {new Date(official.term.end).getFullYear()}
          </div>
        )}
      </div>

      {/* Scrollable content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-1 min-h-0">
        {/* Alignment Gauge */}
        <Section title="MANIFESTO ALIGNMENT" defaultOpen={true}>
          <AlignmentGauge score={score} />
          {official.alignment?.summary && (
            <p className="text-xs text-text-secondary leading-relaxed mt-3">
              {official.alignment.summary}
            </p>
          )}
        </Section>

        {/* Key Agreements */}
        {official.alignment?.key_agreements?.length > 0 && (
          <Section title="KEY AGREEMENTS" accent="text-accent-green">
            <ul className="space-y-1.5">
              {official.alignment.key_agreements.map((item, i) => (
                <li key={i} className="flex items-start gap-2 text-xs">
                  <span className="text-accent-green flex-shrink-0 mt-0.5">+</span>
                  <span className="text-text-secondary">{item}</span>
                </li>
              ))}
            </ul>
          </Section>
        )}

        {/* Key Disagreements */}
        {official.alignment?.key_disagreements?.length > 0 && (
          <Section title="KEY DISAGREEMENTS" accent="text-accent-red">
            <ul className="space-y-1.5">
              {official.alignment.key_disagreements.map((item, i) => (
                <li key={i} className="flex items-start gap-2 text-xs">
                  <span className="text-accent-red flex-shrink-0 mt-0.5">−</span>
                  <span className="text-text-secondary">{item}</span>
                </li>
              ))}
            </ul>
          </Section>
        )}

        {/* Engagement Strategy */}
        {official.alignment?.engagement_strategy && (
          <Section title="ENGAGEMENT STRATEGY" accent="text-accent-blue">
            <div className="bg-accent-blue/5 border border-accent-blue/20 rounded-lg p-3">
              <p className="text-xs text-text-primary leading-relaxed">
                {official.alignment.engagement_strategy}
              </p>
            </div>
            <div className="flex items-center gap-1.5 mt-2">
              <AiGeneratedBadge />
            </div>
          </Section>
        )}

        {/* Relevant Domains */}
        {official.alignment?.relevant_domains?.length > 0 && (
          <Section title="RELEVANT POLICY DOMAINS" defaultOpen={false}>
            <div className="flex flex-wrap gap-1.5">
              {official.alignment.relevant_domains.map((domain) => (
                <span
                  key={domain}
                  className="px-2 py-0.5 text-[10px] rounded-full bg-accent-purple/15 text-accent-purple border border-accent-purple/30 font-mono"
                >
                  {domain}
                </span>
              ))}
            </div>
          </Section>
        )}

        {/* Contact Info */}
        <Section title="CONTACT INFORMATION" defaultOpen={false}>
          <div className="space-y-2">
            {official.contact?.phone && (
              <ContactRow icon="📞" label="Phone" value={official.contact.phone} href={`tel:${official.contact.phone}`} />
            )}
            {official.contact?.email && (
              <ContactRow
                icon="✉"
                label="Email"
                value={official.contact.email}
                href={official.contact.email.startsWith('http') ? official.contact.email : `mailto:${official.contact.email}`}
              />
            )}
            {official.contact?.office && (
              <ContactRow icon="🏛" label="Office" value={official.contact.office} />
            )}
            {official.contact?.website && (
              <ContactRow icon="🌐" label="Web" value={official.contact.website} href={official.contact.website} />
            )}
          </div>
        </Section>

        {/* Notes */}
        {official.notes && (
          <Section title="NOTES" defaultOpen={false}>
            <p className="text-xs text-text-secondary leading-relaxed">{official.notes}</p>
          </Section>
        )}
      </div>
    </div>
  )
}

function ContactRow({ icon, label, value, href }) {
  const content = (
    <div className="flex items-start gap-2 text-xs">
      <span className="flex-shrink-0 w-4 text-center">{icon}</span>
      <div className="min-w-0">
        <div className="text-[9px] font-mono text-text-tertiary uppercase">{label}</div>
        <div className={`text-text-secondary break-all ${href ? 'hover:text-accent-blue transition-colors' : ''}`}>
          {value}
        </div>
      </div>
    </div>
  )

  if (href) {
    return (
      <a href={href} target="_blank" rel="noopener noreferrer" className="block">
        {content}
      </a>
    )
  }
  return content
}
