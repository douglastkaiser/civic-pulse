import OfficialCard from './OfficialCard'

const LEVEL_ORDER = ['federal', 'state', 'county', 'city', 'special_district']

function LevelGroup({ level, officials, selectedOfficialId, onSelectOfficial, isLast, useWeighted }) {
  return (
    <div className="relative">
      {/* Level label */}
      <div className="flex items-center gap-2 mb-2">
        <span className="text-[9px] font-mono font-bold text-text-tertiary tracking-widest uppercase">
          {level.label}
        </span>
        <div className="flex-1 h-px bg-border opacity-50" />
      </div>

      {/* Officials in this level */}
      <div className="space-y-2 mb-1">
        {officials.map((official) => (
          <OfficialCard
            key={official.id}
            official={official}
            selected={selectedOfficialId === official.id}
            onClick={onSelectOfficial}
            useWeighted={useWeighted}
          />
        ))}
      </div>

      {/* Connector to next level */}
      {!isLast && (
        <div className="flex justify-center py-1">
          <div className="hierarchy-flow-line" />
        </div>
      )}
    </div>
  )
}

function BranchColumn({ branch, selectedOfficialId, onSelectOfficial, useWeighted }) {
  const sortedLevels = [...branch.levels].sort(
    (a, b) => LEVEL_ORDER.indexOf(a.level) - LEVEL_ORDER.indexOf(b.level)
  )

  // Filter out levels with no officials
  const activeLevels = sortedLevels.filter((l) => l.officials?.length > 0)

  return (
    <div className="flex-1 min-w-[220px]">
      {/* Branch header */}
      <div className="flex items-center gap-2 mb-4 pb-2 border-b border-border">
        <span className="text-accent-blue text-sm">{branch.icon || '◆'}</span>
        <h3 className="font-mono text-xs font-bold text-text-primary tracking-wide">
          {branch.name.toUpperCase()}
        </h3>
        <span className="text-[9px] font-mono text-text-tertiary">
          {activeLevels.reduce((sum, l) => sum + l.officials.length, 0)}
        </span>
      </div>

      {/* Levels */}
      <div className="space-y-1">
        {activeLevels.map((level, i) => (
          <LevelGroup
            key={level.level}
            level={level}
            officials={level.officials}
            selectedOfficialId={selectedOfficialId}
            onSelectOfficial={onSelectOfficial}
            isLast={i === activeLevels.length - 1}
            useWeighted={useWeighted}
          />
        ))}
      </div>
    </div>
  )
}

export default function HierarchyTree({ officials, selectedOfficialId, onSelectOfficial, useWeighted }) {
  if (!officials?.branches?.length) {
    return (
      <div className="h-full flex items-center justify-center text-sm text-text-tertiary font-mono">
        No officials data available
      </div>
    )
  }

  return (
    <div className="h-full flex flex-col overflow-hidden">
      {/* Summary bar */}
      <div className="flex items-center gap-4 mb-4 flex-shrink-0">
        <div className="flex items-center gap-3 text-[9px] font-mono text-text-tertiary">
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-accent-green" /> Ally
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-accent-amber" /> Mixed
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-accent-red" /> Opposed
          </span>
          <span className="text-text-tertiary/50">│</span>
          <span className="flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-accent-green" /> High Priority
          </span>
          <span className="flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-accent-amber" /> Medium
          </span>
          <span className="flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-text-tertiary" /> Low
          </span>
        </div>
      </div>

      {/* Branch columns */}
      <div className="flex-1 overflow-auto min-h-0">
        <div className="flex gap-4 min-w-0 pb-4 hierarchy-columns">
          {officials.branches.map((branch) => (
            <BranchColumn
              key={branch.name}
              branch={branch}
              selectedOfficialId={selectedOfficialId}
              onSelectOfficial={onSelectOfficial}
              useWeighted={useWeighted}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
