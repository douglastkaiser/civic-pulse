import { useState } from 'react'

function Section({ title, children, defaultOpen = false }) {
  const [open, setOpen] = useState(defaultOpen)
  return (
    <div className="border-b border-border last:border-b-0">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between py-2 text-left"
      >
        <span className="font-mono text-xs font-bold text-text-tertiary tracking-wide">
          {title}
        </span>
        <span className="text-xs text-text-tertiary">{open ? '▾' : '▸'}</span>
      </button>
      {open && <div className="pb-3">{children}</div>}
    </div>
  )
}

function GoverningBody({ body }) {
  return (
    <div className="mb-3 last:mb-0 bg-bg-elevated rounded p-2.5 border border-border">
      <div className="flex items-start justify-between gap-2">
        <div className="text-sm font-medium text-text-primary">{body.name}</div>
        <span className="text-xs text-text-tertiary font-mono whitespace-nowrap">{body.type}</span>
      </div>
      {body.your_representative && (
        <div className="mt-1.5 text-xs space-y-0.5">
          <div>
            <span className="text-accent-blue">Rep: </span>
            <span className="text-text-secondary">{body.your_representative.name}</span>
          </div>
          {body.your_representative.note && (
            <div className="text-text-tertiary">{body.your_representative.note}</div>
          )}
          {body.your_representative.contact_email && (
            <div className="text-text-tertiary">
              ✉ {body.your_representative.contact_email}
            </div>
          )}
        </div>
      )}
      {body.meeting_schedule && (
        <div className="mt-1 text-xs text-text-tertiary">
          📅 {body.meeting_schedule}
        </div>
      )}
      {body.public_comment_process && (
        <div className="mt-1 text-xs text-text-secondary">
          💬 {body.public_comment_process}
        </div>
      )}
      {body.note && !body.your_representative && (
        <div className="mt-1 text-xs text-text-tertiary">{body.note}</div>
      )}
    </div>
  )
}

function OrgList({ orgs }) {
  if (!orgs?.length) return <div className="text-xs text-text-tertiary">None listed</div>
  return (
    <div className="space-y-2">
      {orgs.map((org) => (
        <div key={org.name} className="bg-bg-elevated rounded p-2 border border-border text-xs">
          <div className="flex items-start justify-between gap-2">
            <span className="text-text-primary font-medium">{org.name}</span>
            {org.alignment && (
              <span className="text-text-tertiary whitespace-nowrap">{org.alignment}</span>
            )}
          </div>
          <div className="text-text-secondary mt-0.5">{org.focus}</div>
          {org.how_to_engage && (
            <div className="text-accent-green mt-0.5">→ {org.how_to_engage}</div>
          )}
        </div>
      ))}
    </div>
  )
}

function ElectionCard({ election }) {
  const daysUntil = election.date
    ? Math.ceil((new Date(election.date) - Date.now()) / (1000 * 60 * 60 * 24))
    : null

  return (
    <div className="bg-bg-elevated rounded p-2.5 border border-border">
      <div className="flex items-start justify-between gap-2">
        <span className="text-sm font-medium text-text-primary">{election.race}</span>
        {daysUntil !== null && (
          <span
            className={`text-xs font-mono whitespace-nowrap px-1.5 py-0.5 rounded ${
              daysUntil <= 30
                ? 'bg-accent-red/15 text-accent-red'
                : daysUntil <= 90
                  ? 'bg-accent-amber/15 text-accent-amber'
                  : 'bg-accent-blue/15 text-accent-blue'
            }`}
          >
            {daysUntil > 0 ? `${daysUntil}d` : 'Today'}
          </span>
        )}
      </div>
      {election.date && (
        <div className="text-xs text-text-tertiary mt-0.5">
          {new Date(election.date).toLocaleDateString('en-US', {
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            year: 'numeric',
          })}
        </div>
      )}
      {election.candidates && (
        <div className="text-xs text-text-secondary mt-1">
          Candidates: {election.candidates.join(', ')}
        </div>
      )}
      {election.relevance && (
        <div className="text-xs text-accent-amber mt-1">{election.relevance}</div>
      )}
      {election.action && (
        <div className="text-xs text-accent-green mt-1">→ {election.action}</div>
      )}
    </div>
  )
}

export default function LocationPanel({ location }) {
  if (!location) return null

  const orgs = location.political_organizations

  return (
    <div className="bg-bg-panel border border-border rounded-lg p-4 flex flex-col h-full overflow-hidden">
      <div className="flex items-center justify-between mb-3">
        <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide">
          LOCATION LANDSCAPE
        </h2>
        {location.needs_enrichment && (
          <span className="text-xs text-accent-amber font-mono">⚠ INCOMPLETE</span>
        )}
      </div>

      <div className="flex-1 overflow-y-auto space-y-1 min-h-0">
        {/* Upcoming Elections */}
        {location.upcoming_elections?.length > 0 && (
          <Section title="UPCOMING ELECTIONS" defaultOpen={true}>
            <div className="space-y-2">
              {location.upcoming_elections.map((e) => (
                <ElectionCard key={e.race} election={e} />
              ))}
            </div>
          </Section>
        )}

        {/* Governing Bodies */}
        {location.governing_bodies?.length > 0 && (
          <Section title="GOVERNING BODIES" defaultOpen={true}>
            {location.governing_bodies.map((body) => (
              <GoverningBody key={body.name} body={body} />
            ))}
          </Section>
        )}

        {/* Organizations */}
        {orgs && (
          <Section title="ORGANIZATIONS">
            {orgs.advocacy_orgs?.length > 0 && (
              <div className="mb-2">
                <div className="text-xs text-text-tertiary mb-1 font-mono">Advocacy</div>
                <OrgList orgs={orgs.advocacy_orgs} />
              </div>
            )}
            {orgs.official_party?.length > 0 && (
              <div className="mb-2">
                <div className="text-xs text-text-tertiary mb-1 font-mono">Party</div>
                <OrgList orgs={orgs.official_party} />
              </div>
            )}
            {orgs.citizen_groups?.length > 0 && (
              <div className="mb-2">
                <div className="text-xs text-text-tertiary mb-1 font-mono">Citizen Groups</div>
                <OrgList orgs={orgs.citizen_groups} />
              </div>
            )}
            {orgs.media_and_info?.length > 0 && (
              <div>
                <div className="text-xs text-text-tertiary mb-1 font-mono">Media & Info</div>
                <OrgList orgs={orgs.media_and_info} />
              </div>
            )}
          </Section>
        )}

        {/* Key Political Dynamics */}
        {location.key_political_dynamics && (
          <Section title="KEY DYNAMICS" defaultOpen={false}>
            <div className="text-xs text-text-secondary leading-relaxed">
              {location.key_political_dynamics}
            </div>
          </Section>
        )}
      </div>
    </div>
  )
}
