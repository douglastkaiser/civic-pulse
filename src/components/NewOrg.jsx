import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../lib/auth'
import { getApiKey } from '../lib/apiKeyStore'
import { generateOrg } from '../lib/orgGenerator'
import { saveOrg } from '../lib/orgStore'

export default function NewOrg() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [hasApiKey, setHasApiKey] = useState(false)
  const [name, setName] = useState('')
  const [geographicScope, setGeographicScope] = useState('')
  const [coreIssues, setCoreIssues] = useState('')
  const [mission, setMission] = useState('')
  const [generating, setGenerating] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    setHasApiKey(!!getApiKey())
  }, [])

  const canSubmit = name.trim() && geographicScope.trim() && coreIssues.trim() && mission.trim().length >= 20

  const handleSubmit = async () => {
    if (!canSubmit || generating) return

    setGenerating(true)
    setError(null)

    try {
      const apiKey = getApiKey()
      if (!apiKey) {
        setError('API key not found. Please set your Anthropic API key in Settings.')
        setHasApiKey(false)
        return
      }

      const org = await generateOrg(
        { name: name.trim(), geographicScope: geographicScope.trim(), coreIssues: coreIssues.trim(), mission: mission.trim() },
        apiKey,
      )

      await saveOrg(user.uid, org)
      navigate(`/org/${org.id}`)
    } catch (err) {
      setError(err.message || 'An unexpected error occurred. Please try again.')
    } finally {
      setGenerating(false)
    }
  }

  return (
    <div className="h-full overflow-auto p-4 animate-fade-in">
      <Link to="/dashboard" className="text-xs text-text-tertiary hover:text-accent-blue font-mono transition-colors">
        ← Back to Dashboard
      </Link>

      <div className="max-w-xl mx-auto mt-8">
        <h1 className="font-mono text-lg font-bold text-text-primary tracking-wide mb-2">
          + NEW ORGANIZATION
        </h1>
        <p className="text-sm text-text-secondary leading-relaxed mb-6">
          An organization is any group working toward political goals — from a 3-person
          YIMBY squad to a 500-member advocacy coalition. Civic Pulse handles the research,
          tracking, and logistics so you can focus on action.
        </p>

        <div className="bg-bg-panel border border-border rounded-lg p-4 space-y-4">
          {!hasApiKey ? (
            <div className="px-3 py-4 bg-accent-amber/10 border border-accent-amber/30 rounded text-center space-y-2">
              <p className="text-sm text-text-secondary">
                You need an Anthropic API key to create organizations.
              </p>
              <Link
                to="/settings"
                className="inline-block text-sm text-accent-blue font-mono hover:underline"
              >
                Set API key in Settings →
              </Link>
            </div>
          ) : (
            <>
              {error && (
                <div className="px-3 py-2 bg-accent-red/10 border border-accent-red/30 rounded text-sm text-accent-red font-mono">
                  {error}
                </div>
              )}

              {generating && (
                <div className="px-3 py-2 bg-accent-blue/10 border border-accent-blue/30 rounded text-xs text-accent-blue font-mono text-center">
                  Generating organization profile — this may take 15-30 seconds...
                </div>
              )}

              <div className={`space-y-3 ${generating ? 'opacity-50 pointer-events-none' : ''}`}>
                <div>
                  <label className="block text-xs font-mono text-text-tertiary mb-1">ORGANIZATION NAME</label>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="e.g., Austin YIMBY Action"
                    className="w-full bg-bg-elevated border border-border rounded px-3 py-2 text-sm text-text-primary placeholder-text-tertiary focus:outline-none focus:border-accent-blue/50"
                  />
                </div>
                <div>
                  <label className="block text-xs font-mono text-text-tertiary mb-1">GEOGRAPHIC SCOPE</label>
                  <input
                    type="text"
                    value={geographicScope}
                    onChange={(e) => setGeographicScope(e.target.value)}
                    placeholder="e.g., Austin, TX"
                    className="w-full bg-bg-elevated border border-border rounded px-3 py-2 text-sm text-text-primary placeholder-text-tertiary focus:outline-none focus:border-accent-blue/50"
                  />
                </div>
                <div>
                  <label className="block text-xs font-mono text-text-tertiary mb-1">CORE ISSUE AREAS</label>
                  <input
                    type="text"
                    value={coreIssues}
                    onChange={(e) => setCoreIssues(e.target.value)}
                    placeholder="e.g., Housing, Transportation, Land Use"
                    className="w-full bg-bg-elevated border border-border rounded px-3 py-2 text-sm text-text-primary placeholder-text-tertiary focus:outline-none focus:border-accent-blue/50"
                  />
                  <span className="text-[10px] text-text-tertiary font-mono mt-0.5 block">Comma-separated list of issue areas</span>
                </div>
                <div>
                  <label className="block text-xs font-mono text-text-tertiary mb-1">MISSION (1-2 SENTENCES)</label>
                  <textarea
                    value={mission}
                    onChange={(e) => setMission(e.target.value)}
                    rows={3}
                    placeholder="What does your organization do and why?"
                    className="w-full bg-bg-elevated border border-border rounded px-3 py-2 text-sm text-text-primary placeholder-text-tertiary resize-none focus:outline-none focus:border-accent-blue/50"
                  />
                  <span className="text-[10px] text-text-tertiary font-mono mt-0.5 block">
                    {mission.trim().length < 20 && mission.trim().length > 0
                      ? `${20 - mission.trim().length} more characters needed`
                      : 'Minimum 20 characters'}
                  </span>
                </div>
                <button
                  onClick={handleSubmit}
                  disabled={!canSubmit || generating}
                  className={`w-full font-mono text-sm py-2.5 rounded border transition-colors ${
                    canSubmit && !generating
                      ? 'bg-accent-blue/20 text-accent-blue border-accent-blue/30 hover:bg-accent-blue/30 cursor-pointer'
                      : 'bg-bg-elevated text-text-tertiary border-border cursor-not-allowed'
                  }`}
                >
                  {generating ? 'GENERATING...' : 'CREATE ORGANIZATION'}
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
