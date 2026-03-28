export default function OfficialCard({ official, selected, onClick }) {
  const score = official.alignment?.score ?? 0
  const borderColor =
    score > 0.3
      ? 'border-l-accent-green'
      : score < -0.3
        ? 'border-l-accent-red'
        : 'border-l-accent-amber'

  const partyColor =
    official.party === 'Democrat'
      ? 'bg-blue-500/20 text-blue-400'
      : official.party === 'Republican'
        ? 'bg-red-500/20 text-red-400'
        : 'bg-gray-500/20 text-gray-400'

  const priorityDot =
    official.alignment?.priority === 'high'
      ? 'bg-accent-green'
      : official.alignment?.priority === 'medium'
        ? 'bg-accent-amber'
        : 'bg-text-tertiary'

  return (
    <button
      onClick={() => onClick(official.id)}
      className={`w-full text-left rounded-lg border-l-2 border border-border p-2.5 transition-all duration-150 cursor-pointer group ${borderColor} ${
        selected
          ? 'bg-accent-blue/10 border-r-accent-blue/30 border-t-accent-blue/30 border-b-accent-blue/30 shadow-lg shadow-accent-blue/5'
          : 'bg-bg-elevated hover:bg-bg-elevated/80 hover:border-r-border hover:shadow-md hover:shadow-black/20'
      }`}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-1.5">
            <span className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${priorityDot}`} />
            <span className="text-sm font-medium text-text-primary truncate group-hover:text-accent-blue transition-colors">
              {official.name}
            </span>
          </div>
          <div className="text-[11px] text-text-tertiary mt-0.5 truncate pl-3">
            {official.title}
          </div>
        </div>
        <span className={`text-[9px] font-mono px-1.5 py-0.5 rounded-full flex-shrink-0 ${partyColor}`}>
          {official.party === 'Democrat' ? 'D' : official.party === 'Republican' ? 'R' : official.party === 'Nonpartisan' ? 'NP' : '?'}
        </span>
      </div>
      {official.alignment?.label && (
        <div className="mt-1.5 flex items-center gap-2 pl-3">
          <div className="flex-1 h-1 rounded-full bg-bg-primary overflow-hidden">
            <div
              className="h-full rounded-full transition-all duration-300"
              style={{
                width: `${((score + 1) / 2) * 100}%`,
                background:
                  score > 0.3
                    ? '#22c55e'
                    : score < -0.3
                      ? '#ef4444'
                      : '#f59e0b',
              }}
            />
          </div>
          <span className="text-[9px] font-mono text-text-tertiary whitespace-nowrap">
            {official.alignment.label}
          </span>
        </div>
      )}
    </button>
  )
}
