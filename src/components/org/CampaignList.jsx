const priorityColor = {
  high: 'text-accent-red',
  medium: 'text-accent-amber',
  low: 'text-accent-green',
}

const statusDot = {
  active: 'bg-accent-green',
  planning: 'bg-accent-blue',
  completed: 'bg-text-tertiary',
}

export default function CampaignList({ campaigns = [], selectedId, onSelect }) {
  return (
    <div className="space-y-1.5">
      {campaigns.map((campaign) => {
        const isSelected = campaign.id === selectedId
        return (
          <button
            key={campaign.id}
            onClick={() => onSelect(campaign.id)}
            className={`w-full text-left px-3 py-2.5 rounded border transition-colors duration-150 ${
              isSelected
                ? 'bg-bg-elevated border-accent-blue/30'
                : 'bg-bg-panel border-border hover:border-accent-blue/20 hover:bg-bg-elevated'
            }`}
          >
            <div className="flex items-center gap-2">
              <span className={`w-2 h-2 rounded-full flex-shrink-0 ${statusDot[campaign.status] || 'bg-text-tertiary'}`} />
              <span className={`text-sm font-medium truncate ${isSelected ? 'text-text-primary' : 'text-text-secondary'}`}>
                {campaign.title}
              </span>
              <span className={`text-xs font-mono ml-auto flex-shrink-0 ${priorityColor[campaign.priority] || 'text-text-tertiary'}`}>
                {campaign.priority?.toUpperCase()}
              </span>
            </div>
          </button>
        )
      })}
    </div>
  )
}
