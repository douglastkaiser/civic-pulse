import { useState, useEffect, useMemo } from 'react'
import { useParams } from 'react-router-dom'
import { loadProfile, loadOfficials, PROFILE_ID } from '../lib/data'
import { applyWeightedAlignments } from '../lib/alignmentWeighting'
import ExportButton from './shared/ExportButton'
import HierarchyTree from './officials/HierarchyTree'
import OfficialDetail from './officials/OfficialDetail'
import DetailModal from './shared/DetailModal'
import ContextTooltip from './shared/ContextTooltip'

export default function OfficialsPage() {
  const { locationId } = useParams()
  const [profile, setProfile] = useState(null)
  const [officials, setOfficials] = useState(null)
  const [loading, setLoading] = useState(true)
  const [locationLoading, setLocationLoading] = useState(false)
  const [selectedOfficialId, setSelectedOfficialId] = useState(null)
  const [mobileDetailOpen, setMobileDetailOpen] = useState(false)
  const [useWeighted, setUseWeighted] = useState(false)

  // Load profile for manifesto data
  useEffect(() => {
    loadProfile(PROFILE_ID)
      .then(setProfile)
      .catch((err) => console.error('Failed to load profile:', err))
  }, [])

  // Load officials for location from URL
  useEffect(() => {
    if (!locationId) return

    setLoading(true)
    setLocationLoading(true)
    setSelectedOfficialId(null)
    setMobileDetailOpen(false)

    loadOfficials(locationId)
      .then((data) => {
        setOfficials(data)
        setLoading(false)
        setLocationLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load officials:', err)
        setOfficials(null)
        setLoading(false)
        setLocationLoading(false)
      })
  }, [locationId])

  // Apply weighted alignment scores when toggled
  const enrichedOfficials = useMemo(() => {
    if (!officials?.branches || !profile?.issue_salience) return officials
    return {
      ...officials,
      branches: applyWeightedAlignments(officials.branches, profile.issue_salience),
    }
  }, [officials, profile?.issue_salience])

  // Find the selected official across all branches/levels
  const selectedOfficial = useMemo(() => {
    if (!selectedOfficialId || !enrichedOfficials?.branches) return null
    for (const branch of enrichedOfficials.branches) {
      for (const level of branch.levels) {
        const found = level.officials?.find((o) => o.id === selectedOfficialId)
        if (found) return found
      }
    }
    return null
  }, [selectedOfficialId, enrichedOfficials])

  const handleSelectOfficial = (officialId) => {
    setSelectedOfficialId(officialId)
    setMobileDetailOpen(true)
  }

  const getExportData = () => {
    // Collect all officials into a flat list for export
    const allOfficials = []
    if (enrichedOfficials?.branches) {
      for (const branch of officials.branches) {
        for (const level of branch.levels) {
          for (const official of level.officials || []) {
            allOfficials.push(official)
          }
        }
      }
    }

    return {
      export_type: 'officials_hierarchy',
      exported_at: new Date().toISOString(),
      location_id: locationId,
      location_label: profile?.locations?.find((l) => l.id === locationId)?.label,
      manifesto_summary: profile?.manifesto?.manifesto_summary,
      officials_hierarchy: enrichedOfficials?.branches,
      officials_flat: allOfficials,
      total_officials: allOfficials.length,
      alignment_summary: {
        allies: allOfficials.filter((o) => (o.alignment?.score ?? 0) > 0.3).length,
        mixed: allOfficials.filter((o) => {
          const s = o.alignment?.score ?? 0
          return s >= -0.3 && s <= 0.3
        }).length,
        opposed: allOfficials.filter((o) => (o.alignment?.score ?? 0) < -0.3).length,
      },
    }
  }

  if (loading) {
    return (
      <div className="h-full p-3 flex flex-col gap-3 overflow-hidden animate-fade-in">
        <div className="flex items-center justify-between flex-shrink-0">
          <div className="h-6 w-48 bg-bg-elevated rounded animate-pulse" />
          <div className="h-8 w-24 bg-bg-elevated rounded animate-pulse" />
        </div>
        <div className="flex-1 flex gap-3 min-h-0">
          <div className="flex-1 bg-bg-panel border border-border rounded-lg p-4 animate-pulse">
            <div className="flex gap-4">
              {[1, 2, 3].map((i) => (
                <div key={i} className="flex-1 space-y-4">
                  <div className="h-4 w-24 bg-bg-elevated rounded" />
                  <div className="space-y-2">
                    <div className="h-16 bg-bg-elevated rounded" />
                    <div className="h-16 bg-bg-elevated rounded" />
                    <div className="h-16 bg-bg-elevated rounded" />
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div className="hidden lg:block w-80 bg-bg-panel border border-border rounded-lg animate-pulse" />
        </div>
      </div>
    )
  }

  // Count officials
  const officialCount = enrichedOfficials?.branches?.reduce(
    (sum, b) => sum + b.levels.reduce((s, l) => s + (l.officials?.length || 0), 0),
    0
  ) || 0

  const locationOverlay = locationLoading ? (
    <div className="absolute inset-0 bg-bg-primary/50 z-10 flex items-center justify-center rounded-lg">
      <span className="font-mono text-xs text-text-tertiary animate-pulse">Loading officials...</span>
    </div>
  ) : null

  return (
    <div className="h-full p-3 flex flex-col gap-3 overflow-hidden animate-fade-in">
      {/* Utility bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 flex-shrink-0">
        <div className="flex items-center gap-3">
          <h1 className="font-mono text-sm font-bold text-text-primary tracking-wide">
            OFFICIALS
          </h1>
          <ContextTooltip text="Your elected and appointed officials organized by branch of government, from federal down to local. Each official includes manifesto alignment analysis and engagement strategy." />
          {officialCount > 0 && (
            <span className="text-[10px] font-mono text-text-tertiary">
              {officialCount} officials
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          {profile?.issue_salience && Object.keys(profile.issue_salience).length > 0 && (
            <button
              onClick={() => setUseWeighted((w) => !w)}
              className={`text-[10px] font-mono px-2.5 py-1 rounded-full border transition-all duration-200 ${
                useWeighted
                  ? 'bg-accent-purple/15 text-accent-purple border-accent-purple/40 shadow-sm shadow-accent-purple/10'
                  : 'bg-bg-elevated text-text-tertiary border-border hover:text-text-secondary hover:border-border'
              }`}
              title="Weight alignment scores by your issue priorities"
            >
              {useWeighted ? '⚖ WEIGHTED' : '⚖ RAW'}
            </button>
          )}
          <ExportButton
            getData={getExportData}
            filename={`civic-pulse-officials-${locationId || 'all'}.json`}
          />
        </div>
      </div>

      {/* Main content: Tree + Detail Panel */}
      <div className="flex-1 flex gap-3 min-h-0 overflow-hidden">
        {/* Hierarchy Tree */}
        <div className="flex-1 min-w-0 bg-bg-panel border border-border rounded-lg p-4 overflow-hidden relative panel-hover">
          {locationOverlay}
          <HierarchyTree
            officials={enrichedOfficials}
            selectedOfficialId={selectedOfficialId}
            onSelectOfficial={handleSelectOfficial}
            useWeighted={useWeighted}
          />
        </div>

        {/* Detail Panel - Desktop */}
        <div className="hidden lg:flex w-80 flex-shrink-0 bg-bg-panel border border-border rounded-lg overflow-hidden panel-hover">
          <OfficialDetail official={selectedOfficial} useWeighted={useWeighted} />
        </div>

        {/* Detail Panel - Mobile (modal) */}
        <DetailModal
          open={mobileDetailOpen && !!selectedOfficial}
          onClose={() => setMobileDetailOpen(false)}
          title={selectedOfficial?.name || 'Official'}
          tabs={[]}
        >
          <div className="lg:hidden">
            <OfficialDetail
              official={selectedOfficial}
              onClose={() => setMobileDetailOpen(false)}
              useWeighted={useWeighted}
            />
          </div>
        </DetailModal>
      </div>
    </div>
  )
}
