const STATUS_STYLES = {
  active: { dot: '#22c55e', label: 'Active' },
  setting_up: { dot: '#f59e0b', label: 'Setting up' },
}

export default function LocationSwitcher({ locations, activeLocationId, onSwitch }) {
  if (!locations || locations.length < 2) return null

  return (
    <div className="flex items-center gap-1 bg-bg-panel border border-border rounded-lg px-2 py-1.5 font-mono text-xs">
      {locations.map((loc, i) => {
        const isActive = loc.id === activeLocationId
        const status = STATUS_STYLES[loc.status] || STATUS_STYLES.active

        return (
          <div key={loc.id} className="flex items-center">
            {i > 0 && (
              <span className="text-text-tertiary mx-1.5">←→</span>
            )}
            <button
              onClick={() => onSwitch(loc.id)}
              className={`flex items-center gap-1.5 px-2 py-1 rounded transition-colors duration-150 ${
                isActive
                  ? 'bg-accent-blue/15 text-accent-blue border border-accent-blue/30'
                  : 'text-text-secondary hover:text-text-primary hover:bg-bg-elevated border border-transparent'
              }`}
            >
              <span className="truncate">{loc.label}</span>
              <span className="flex items-center gap-1 flex-shrink-0">
                <span
                  className="inline-block w-1.5 h-1.5 rounded-full"
                  style={{ backgroundColor: status.dot }}
                />
                <span className="text-text-tertiary text-[10px]">{status.label}</span>
              </span>
            </button>
          </div>
        )
      })}
    </div>
  )
}
