import { useState, useEffect, useMemo } from 'react'
import { loadProfile, loadFreshness, loadLocation, PROFILE_ID } from '../lib/data'
import { useAuth } from '../lib/auth'
import { getUserProfile } from '../lib/userStore'
import ManifestoPanel from './ManifestoPanel'
import PoliticalCompass from './PoliticalCompass'
import PositionScatterPlot from './PositionScatterPlot'
import ExportButton from './shared/ExportButton'
import BulkExportButton from './shared/BulkExportButton'
import { getCssVar } from '../lib/themeColors'

const VIEW_TABS = [
  { key: 'action', label: 'Action' },
  { key: 'profile', label: 'Profile' },
]

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value))
}

function toSlug(text) {
  return String(text || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '')
}

function buildBridgeOpportunities(profile) {
  const positions = Array.isArray(profile?.political_positions) ? profile.political_positions : []
  const issuePositions = Array.isArray(profile?.manifesto?.issue_positions)
    ? profile.manifesto.issue_positions
    : []

  const issueByDomain = new Map()
  issuePositions.forEach((issue) => {
    if (!issue?.domain) return
    issueByDomain.set(issue.domain, issue)
  })

  const ranked = positions
    .map((pos) => {
      const issue = issueByDomain.get(pos.domain) || null
      const intensity = clamp(Math.abs(pos.position || 0), 0, 1)
      const importance = clamp(Number(pos.importance) || 1, 1, 5)
      const bridgePressure = issue?.likely_friction ? 1 : 0
      const score = (importance / 5) * 0.5 + intensity * 0.35 + bridgePressure * 0.15
      return { ...pos, issue, intensity, importance, score }
    })
    .sort((a, b) => b.score - a.score)

  const makeGuide = (item, categoryLabel) => {
    const issue = item.issue
    const topic = item.short_label || item.question || item.domain
    const id = `guide-${categoryLabel}-${toSlug(item.id || topic)}`
    return {
      id,
      title: `${topic}: ${categoryLabel}`,
      opener:
        issue?.local_implication ||
        item.rationale ||
        'Lead with shared local outcomes and acknowledge tradeoffs before advocating your position.',
      bridge:
        issue?.likely_allies
          ? `Start with shared values from: ${issue.likely_allies}.`
          : 'Find one overlapping value first (cost, fairness, safety, stability, or trust).',
      objection:
        issue?.likely_friction
          ? `Common pushback likely from: ${issue.likely_friction}.`
          : 'Likely objection: concerns about unintended consequences, cost, or implementation capacity.',
      close:
        item.rationale
          ? `Close with your rationale: ${item.rationale}`
          : 'Close with one concrete local action and invite edits instead of forcing agreement.',
    }
  }

  const highFitNeedsBridging = ranked
    .filter(item => item.intensity >= 0.35 && item.intensity <= 0.8 && item.importance >= 4 && item.issue?.likely_friction)
    .slice(0, 4)
    .map((item) => ({
      id: `high-fit-${item.id}`,
      title: item.short_label || item.question,
      rationale: `${item.domain}: You care a lot here and already have likely allies (${item.issue?.likely_allies || 'cross-cutting groups'}), but you may need bridging with ${item.issue?.likely_friction || 'skeptical audiences'}.`,
      guide: makeGuide(item, 'high-fit-needs-bridging'),
    }))

  const strongPositionCommonObjections = ranked
    .filter(item => item.intensity >= 0.75 && item.importance >= 3)
    .slice(0, 4)
    .map((item) => ({
      id: `common-objection-${item.id}`,
      title: item.short_label || item.question,
      rationale: `${item.domain}: Your stance is strong (${item.position > 0 ? 'for' : 'against'}) and likely to trigger predictable objections. Prepare responses before persuasion attempts.`,
      guide: makeGuide(item, 'strong-position-common-objections'),
    }))

  const ownSidePotentialFriction = ranked
    .filter(item => item.importance >= 3 && item.issue?.likely_allies)
    .slice(0, 4)
    .map((item) => ({
      id: `own-side-${item.id}`,
      title: item.short_label || item.question,
      rationale: `${item.domain}: Potential friction may come from your own coalition (${item.issue?.likely_allies}) over tactics, sequencing, or scope.`,
      guide: makeGuide(item, 'own-side-potential-friction'),
    }))

  return {
    categories: [
      { key: 'high-fit', title: 'High fit, needs bridging', items: highFitNeedsBridging },
      { key: 'objections', title: 'Strong position, common objections', items: strongPositionCommonObjections },
      { key: 'own-side', title: 'Your own side, potential friction', items: ownSidePotentialFriction },
    ],
    guides: [...highFitNeedsBridging, ...strongPositionCommonObjections, ...ownSidePotentialFriction].map(item => item.guide),
  }
}

function MyBridgesSection({ profile }) {
  const bridgeData = useMemo(() => buildBridgeOpportunities(profile), [profile])
  const [activeGuideId, setActiveGuideId] = useState(null)

  const activeGuide = bridgeData.guides.find(g => g.id === activeGuideId) || bridgeData.guides[0] || null

  return (
    <section className="bg-bg-panel border border-border rounded-lg p-3 space-y-3">
      <div className="flex items-center justify-between gap-2">
        <h3 className="font-mono text-sm font-bold text-text-primary tracking-wide">MY BRIDGES</h3>
        <span className="text-[11px] text-text-tertiary font-mono uppercase">From your positions + issue mapping</span>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-3">
        {bridgeData.categories.map((category) => (
          <div key={category.key} className="border border-border rounded bg-bg-elevated/50 p-3">
            <h4 className="font-mono text-xs font-bold text-text-secondary tracking-wide mb-2 uppercase">{category.title}</h4>
            {category.items.length === 0 ? (
              <p className="text-xs text-text-tertiary leading-relaxed">
                Add more political positions and issue mapping details to generate opportunities in this category.
              </p>
            ) : (
              <ul className="space-y-2">
                {category.items.map((item) => (
                  <li key={item.id} className="border border-border rounded p-2 bg-bg-panel/60">
                    <p className="text-xs font-medium text-text-primary">{item.title}</p>
                    <p className="text-xs text-text-secondary leading-relaxed mt-1">{item.rationale}</p>
                    <a
                      href={`#${item.guide.id}`}
                      onClick={() => setActiveGuideId(item.guide.id)}
                      className="inline-flex mt-2 text-[11px] font-mono text-accent-blue hover:text-accent-blue/80"
                    >
                      Open framing guide →
                    </a>
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>

      {activeGuide && (
        <div id={activeGuide.id} className="border border-border rounded p-3 bg-bg-elevated/50">
          <div className="flex items-center justify-between gap-2 mb-2">
            <h4 className="font-mono text-xs font-bold text-text-primary tracking-wide uppercase">Framing Guide</h4>
            <span className="text-[11px] text-text-tertiary">{activeGuide.title}</span>
          </div>
          <div className="space-y-1.5 text-xs text-text-secondary leading-relaxed">
            <p><span className="text-text-primary font-medium">Opener:</span> {activeGuide.opener}</p>
            <p><span className="text-text-primary font-medium">Bridge:</span> {activeGuide.bridge}</p>
            <p><span className="text-text-primary font-medium">Objection:</span> {activeGuide.objection}</p>
            <p><span className="text-text-primary font-medium">Close:</span> {activeGuide.close}</p>
          </div>
        </div>
      )}
    </section>
  )
}

function EmptyDashboard({ user }) {
  return (
    <div className="h-full p-3 flex flex-col gap-3 overflow-auto lg:overflow-hidden animate-fade-in">
      <div className="flex flex-col lg:flex-row gap-3 flex-1 lg:min-h-0">
        {/* Empty manifesto */}
        <div className="lg:w-3/5 min-w-0 min-h-[300px] lg:min-h-0">
          <div className="bg-bg-panel border border-border rounded-lg p-6 h-full flex flex-col items-center justify-center text-center">
            <div className="text-3xl mb-3">▸</div>
            <h2 className="font-mono text-lg font-bold text-text-primary tracking-wide mb-2">
              Welcome, {user.displayName?.split(' ')[0] || 'there'}
            </h2>
            <p className="text-text-secondary text-sm max-w-sm mb-4">
              Your political profile is empty. Once set up, you'll see your manifesto, values, and issue priorities here.
            </p>
            <span className="text-xs text-text-tertiary font-mono px-3 py-1.5 bg-bg-elevated rounded">
              Profile setup coming soon
            </span>
          </div>
        </div>

        {/* Empty compass */}
        <div className="lg:w-2/5 min-w-0 min-h-[300px] lg:min-h-0">
          <div className="bg-bg-panel border border-border rounded-lg p-6 h-full flex flex-col items-center justify-center text-center">
            <div className="text-3xl mb-3">◎</div>
            <h3 className="font-mono text-sm font-bold text-text-primary tracking-wide mb-2">
              POLITICAL COMPASS
            </h3>
            <p className="text-text-secondary text-sm max-w-xs">
              Your position on the political compass will appear here once your profile is configured.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default function PersonalDashboard() {
  const { user } = useAuth()
  const [profile, setProfile] = useState(null)
  const [location, setLocation] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isEmpty, setIsEmpty] = useState(false)
  const [view, setView] = useState('action')

  useEffect(() => {
    const load = async () => {
      let loadedProfile = null
      try {
        // Try loading the user's Firestore profile first
        const userProfile = await getUserProfile(user.uid)
        if (userProfile?.manifesto) {
          loadedProfile = userProfile
          setProfile(userProfile)
        } else {
          // Fall back to static profile data if it exists
          const [prof] = await Promise.all([
            loadProfile(PROFILE_ID),
            loadFreshness(),
          ])
          loadedProfile = prof
          setProfile(prof)
        }
      } catch {
        // No static data and no Firestore data → empty state
        setIsEmpty(true)
      }

      // Load primary location's landscape so the compass has reference groups
      const primaryLoc =
        loadedProfile?.locations?.find((l) => l.primary) ||
        loadedProfile?.locations?.[0]
      if (primaryLoc?.id) {
        try {
          const loc = await loadLocation(primaryLoc.id)
          setLocation(loc)
        } catch {
          // Missing landscape — fall back to "You only" compass
        }
      }

      setLoading(false)
    }
    load()
  }, [user.uid])

  if (loading) {
    return (
      <div className="h-full p-3 flex flex-col gap-3 overflow-auto lg:overflow-hidden">
        <div className="flex flex-col lg:flex-row gap-3 flex-1 lg:min-h-0">
          <div className="lg:w-3/5 min-w-0 min-h-[300px] lg:min-h-0">
            <div className="bg-bg-panel border border-border rounded-lg p-4 h-full animate-pulse">
              <div className="h-4 w-28 bg-bg-elevated rounded mb-4" />
              <div className="flex gap-2 mb-4">
                <div className="h-5 w-20 bg-bg-elevated rounded-full" />
                <div className="h-5 w-16 bg-bg-elevated rounded-full" />
                <div className="h-5 w-24 bg-bg-elevated rounded-full" />
              </div>
              <div className="space-y-2">
                <div className="h-3 bg-bg-elevated rounded w-full" />
                <div className="h-3 bg-bg-elevated rounded w-5/6" />
                <div className="h-3 bg-bg-elevated rounded w-4/6" />
              </div>
            </div>
          </div>
          <div className="lg:w-2/5 min-w-0 min-h-[300px] lg:min-h-0">
            <div className="bg-bg-panel border border-border rounded-lg p-4 h-full animate-pulse">
              <div className="h-4 w-32 bg-bg-elevated rounded mb-4" />
              <div className="h-48 bg-bg-elevated rounded opacity-30" />
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (isEmpty || !profile) {
    return <EmptyDashboard user={user} />
  }

  // Political compass: user position + a few reference groups from primary location
  const compassEntities = []
  const purple = getCssVar('--accent-purple')
  const blue = getCssVar('--accent-blue')
  const red = getCssVar('--accent-red')
  const amber = getCssVar('--accent-amber')
  const green = getCssVar('--accent-green')

  if (profile?.political_compass?.user) {
    compassEntities.push({ name: 'You', ...profile.political_compass.user, color: purple, highlighted: true })
  }

  if (location?.political_compass_entities) {
    const pce = location.political_compass_entities
    if (pce.city_austin) compassEntities.push({ name: 'Austin', ...pce.city_austin, color: blue })
    if (pce.state_texas) compassEntities.push({ name: 'Texas', ...pce.state_texas, color: red })
    if (pce.orange_county) compassEntities.push({ name: 'Orange Co', ...pce.orange_county, color: amber })
    if (pce.california_democratic_party) compassEntities.push({ name: 'CA Dems', ...pce.california_democratic_party, color: blue })
    if (pce.democratic_party) compassEntities.push({ name: 'Dem Party', ...pce.democratic_party, color: blue })
    if (pce.republican_party) compassEntities.push({ name: 'GOP', ...pce.republican_party, color: red })
    if (pce.local_orgs) {
      pce.local_orgs.slice(0, 2).forEach((org) => {
        compassEntities.push({ name: org.name, ...org, color: green })
      })
    }
  }

  const getExportData = () => ({
    export_type: 'personal_political_profile',
    exported_at: new Date().toISOString(),
    profile_id: PROFILE_ID,
    display_name: profile.display_name,
    political_context: profile.political_context,
    values: profile.values,
    issue_salience: profile.issue_salience,
    manifesto: profile.manifesto,
    political_compass: profile.political_compass,
    political_positions: profile.political_positions,
    engagement_appetite: profile.engagement_appetite,
  })

  const profilePanels = (
    <div className="flex flex-col lg:flex-row gap-3 lg:min-h-0" style={{ flex: '2 1 0%' }}>
      <div className="lg:w-3/5 min-w-0 min-h-[300px] lg:min-h-0">
        <ManifestoPanel profile={profile} />
      </div>
      {compassEntities.length > 0 && (
        <div className="lg:w-2/5 min-w-0 min-h-[300px] lg:min-h-0">
          <PoliticalCompass entities={compassEntities} size={280} collapsible={false} />
        </div>
      )}
    </div>
  )

  return (
    <div className="h-full p-3 flex flex-col gap-3 overflow-auto lg:overflow-hidden animate-fade-in">
      {/* Utility bar with view tabs */}
      <div className="flex items-center gap-2 flex-shrink-0">
        <div className="flex gap-1">
          {VIEW_TABS.map(tab => (
            <button
              key={tab.key}
              onClick={() => setView(tab.key)}
              className={`text-xs font-mono px-2.5 py-1 rounded transition-colors ${
                view === tab.key
                  ? 'bg-accent-blue/20 text-accent-blue'
                  : 'text-text-tertiary hover:text-text-secondary'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-2 ml-auto">
          <BulkExportButton />
          <ExportButton getData={getExportData} filename="civic-pulse-profile.json" />
        </div>
      </div>

      {/* Action view: current layout */}
      {view === 'action' && (
        <div className="flex flex-col gap-3 flex-1 lg:min-h-0">
          <div className="flex flex-col lg:flex-row gap-3" style={{ flex: '1 1 0%' }}>
            <div className="lg:w-3/5 min-w-0 min-h-[300px] lg:min-h-0">
              <ManifestoPanel profile={profile} />
            </div>
            {compassEntities.length > 0 && (
              <div className="lg:w-2/5 min-w-0 min-h-[300px] lg:min-h-0">
                <PoliticalCompass entities={compassEntities} size={280} collapsible={false} />
              </div>
            )}
          </div>
          <MyBridgesSection profile={profile} />
        </div>
      )}

      {/* Profile view: manifesto + compass + scatter plot */}
      {view === 'profile' && (
        <div className="flex flex-col gap-3 flex-1 lg:min-h-0">
          {profilePanels}
          {profile?.political_positions?.length > 0 && (
            <div className="min-h-[400px]" style={{ flex: '3 1 0%' }}>
              <PositionScatterPlot positions={profile.political_positions} />
            </div>
          )}
        </div>
      )}
    </div>
  )
}
