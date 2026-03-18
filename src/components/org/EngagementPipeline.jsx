const STAGES = [
  { key: 'awareness', label: 'AWARENESS', color: '#3b82f6', width: '100%' },
  { key: 'interest', label: 'INTEREST', color: '#22c55e', width: '80%' },
  { key: 'action', label: 'ACTION', color: '#f59e0b', width: '55%' },
  { key: 'leadership', label: 'LEADERSHIP', color: '#a855f7', width: '30%' },
]

export default function EngagementPipeline({ pipeline }) {
  if (!pipeline) return null

  return (
    <div className="space-y-2">
      {STAGES.map((stage) => {
        const description = pipeline[stage.key]
        if (!description) return null

        return (
          <div key={stage.key} className="flex items-start gap-2">
            <div className="flex-shrink-0 w-20">
              <div
                className="h-5 rounded-r-sm flex items-center justify-start px-1.5"
                style={{ width: stage.width, backgroundColor: stage.color + '25', borderLeft: `2px solid ${stage.color}` }}
              >
                <span className="font-mono text-xs" style={{ color: stage.color, fontSize: '9px' }}>
                  {stage.label}
                </span>
              </div>
            </div>
            <p className="text-xs text-text-secondary leading-relaxed flex-1 mt-0.5">
              {description}
            </p>
          </div>
        )
      })}
    </div>
  )
}
