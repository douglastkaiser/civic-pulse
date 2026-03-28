import { getCssVar } from '../../lib/themeColors'

const STAGE_DEFS = [
  { key: 'awareness', label: 'AWARENESS', colorVar: '--accent-blue', width: '100%' },
  { key: 'interest', label: 'INTEREST', colorVar: '--accent-green', width: '80%' },
  { key: 'action', label: 'ACTION', colorVar: '--accent-amber', width: '55%' },
  { key: 'leadership', label: 'LEADERSHIP', colorVar: '--accent-purple', width: '30%' },
]

export default function EngagementPipeline({ pipeline }) {
  if (!pipeline) return null

  return (
    <div className="space-y-2">
      {STAGE_DEFS.map((stage) => {
        const description = pipeline[stage.key]
        if (!description) return null
        const color = getCssVar(stage.colorVar)

        return (
          <div key={stage.key} className="flex items-start gap-2">
            <div className="flex-shrink-0 w-20">
              <div
                className="h-5 rounded-r-sm flex items-center justify-start px-1.5"
                style={{ width: stage.width, backgroundColor: color + '25', borderLeft: `2px solid ${color}` }}
              >
                <span className="font-mono text-xs" style={{ color, fontSize: '9px' }}>
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
