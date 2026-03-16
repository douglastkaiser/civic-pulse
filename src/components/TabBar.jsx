import FreshnessIndicator from './FreshnessIndicator'

export default function TabBar({ profiles, freshness, activeId, onSelect }) {
  return (
    <div className="flex border-b border-border bg-bg-panel overflow-x-auto">
      {profiles.map((profile) => {
        const isActive = profile.id === activeId
        const f = freshness?.profiles?.[profile.id]
        const latestTimestamp = f
          ? [f.issues_scraped, f.location_scraped, f.manifesto_generated]
              .filter(Boolean)
              .sort()
              .pop()
          : null

        return (
          <button
            key={profile.id}
            onClick={() => onSelect(profile.id)}
            className={`
              flex items-center gap-2 px-4 py-2.5 font-mono text-sm whitespace-nowrap
              transition-colors border-b-2 hover:bg-bg-elevated
              ${isActive
                ? 'border-accent-blue text-text-primary'
                : 'border-transparent text-text-secondary hover:text-text-primary'
              }
            `}
          >
            <span>{profile.display_name}</span>
            <FreshnessIndicator timestamp={latestTimestamp} size={6} />
          </button>
        )
      })}
    </div>
  )
}
