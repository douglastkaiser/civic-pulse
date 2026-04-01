import { useState, useEffect } from 'react'
import { getUserProfile, saveUserProfile } from '../../lib/userStore'
import { saveApiKey, getApiKey, clearApiKey } from '../../lib/apiKeyStore'
import { generateProfile } from '../../lib/profileGenerator'
import { VALUE_DIMENSIONS, ISSUE_DOMAINS, ENGAGEMENT_QUESTIONS } from './QuizQuestions'

function initValues() {
  const v = {}
  VALUE_DIMENSIONS.forEach(d => { v[d.key] = 0 })
  return v
}

function initSalience() {
  const s = {}
  ISSUE_DOMAINS.forEach(d => { s[d] = 50 })
  return s
}

function initEngagement() {
  const e = {}
  ENGAGEMENT_QUESTIONS.forEach(q => { e[q.key] = q.options[0] })
  return e
}

export default function PoliticalQuizSection({ user }) {
  const [apiKey, setApiKey] = useState('')
  const [showKey, setShowKey] = useState(false)
  const [freeformText, setFreeformText] = useState('')
  const [values, setValues] = useState(initValues)
  const [issueSalience, setIssueSalience] = useState(initSalience)
  const [engagement, setEngagement] = useState(initEngagement)
  const [generating, setGenerating] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)
  const [loaded, setLoaded] = useState(false)

  // Load existing quiz answers and API key on mount
  useEffect(() => {
    const stored = getApiKey()
    if (stored) setApiKey(stored)

    getUserProfile(user.uid).then(profile => {
      if (profile?.quiz_answers) {
        const qa = profile.quiz_answers
        if (qa.freeformText) setFreeformText(qa.freeformText)
        if (qa.values) setValues(v => ({ ...v, ...qa.values }))
        if (qa.issueSalience) setIssueSalience(s => ({ ...s, ...qa.issueSalience }))
        if (qa.engagement) setEngagement(e => ({ ...e, ...qa.engagement }))
      }
      setLoaded(true)
    }).catch(() => setLoaded(true))
  }, [user.uid])

  const handleApiKeySave = () => {
    saveApiKey(apiKey)
  }

  const handleApiKeyClear = () => {
    setApiKey('')
    clearApiKey()
  }

  const isValidKey = apiKey.startsWith('sk-ant-')

  const handleRegenerate = async () => {
    if (!isValidKey) {
      setError('Please enter a valid Anthropic API key (starts with sk-ant-).')
      return
    }

    setGenerating(true)
    setError(null)
    setSuccess(false)

    const quizAnswers = { freeformText, values, issueSalience, engagement }

    try {
      // Save API key
      saveApiKey(apiKey)

      // Generate profile via Claude
      const generated = await generateProfile(quizAnswers, apiKey)

      // Save to Firestore
      await saveUserProfile(user.uid, {
        ...generated,
        engagement_appetite: engagement,
        quiz_answers: quizAnswers,
        manifesto_inputs_complete: true,
      })

      setSuccess(true)
      setTimeout(() => setSuccess(false), 5000)
    } catch (err) {
      setError(err.message || 'An unexpected error occurred. Please try again.')
    } finally {
      setGenerating(false)
    }
  }

  if (!loaded) {
    return (
      <section className="mb-10">
        <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide mb-1">
          POLITICAL ALIGNMENT
        </h2>
        <div className="animate-pulse text-xs text-text-tertiary font-mono">Loading...</div>
      </section>
    )
  }

  return (
    <section className="mb-10">
      <h2 className="font-mono text-sm font-bold text-text-primary tracking-wide mb-1">
        POLITICAL ALIGNMENT
      </h2>
      <p className="text-xs text-text-secondary mb-6">
        Describe your political views and priorities. Click "Regenerate Profile" to create your personalized dashboard using AI.
      </p>

      {/* API Key */}
      <div className="mb-8 bg-bg-panel border border-border rounded-lg p-4">
        <h3 className="font-mono text-xs font-bold text-text-primary tracking-wide mb-2">
          ANTHROPIC API KEY
        </h3>
        <p className="text-xs text-text-tertiary mb-3">
          Your key is stored locally in your browser and used only to generate your profile. It is never sent to our servers.
        </p>
        <div className="flex gap-2 items-center">
          <div className="relative flex-1">
            <input
              type={showKey ? 'text' : 'password'}
              value={apiKey}
              onChange={e => setApiKey(e.target.value)}
              placeholder="sk-ant-..."
              disabled={generating}
              className="w-full px-3 py-2 text-sm font-mono bg-bg-elevated border border-border rounded text-text-primary placeholder:text-text-tertiary focus:outline-none focus:border-accent-blue/50 disabled:opacity-50"
            />
            <button
              type="button"
              onClick={() => setShowKey(!showKey)}
              className="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-text-tertiary hover:text-text-secondary font-mono"
            >
              {showKey ? 'HIDE' : 'SHOW'}
            </button>
          </div>
          <button
            onClick={handleApiKeySave}
            disabled={!apiKey || generating}
            className="px-3 py-2 text-xs font-mono rounded border border-border text-text-secondary hover:text-accent-blue hover:border-accent-blue/30 transition-colors disabled:opacity-50"
          >
            Save
          </button>
          <button
            onClick={handleApiKeyClear}
            disabled={generating}
            className="px-3 py-2 text-xs font-mono rounded border border-border text-text-secondary hover:text-accent-red hover:border-accent-red/30 transition-colors disabled:opacity-50"
          >
            Clear
          </button>
        </div>
        {apiKey && !isValidKey && (
          <p className="text-xs text-accent-red mt-2 font-mono">
            Key should start with "sk-ant-"
          </p>
        )}
      </div>

      {/* Freeform Write-Up */}
      <div className="mb-8 bg-bg-panel border border-border rounded-lg p-4">
        <h3 className="font-mono text-xs font-bold text-text-primary tracking-wide mb-2">
          YOUR POLITICAL VIEWS
        </h3>
        <p className="text-xs text-text-tertiary mb-3">
          Describe your political views, priorities, and what matters to you in local government. There are no right answers — write as much or as little as you'd like.
        </p>
        <textarea
          value={freeformText}
          onChange={e => setFreeformText(e.target.value)}
          disabled={generating}
          rows={8}
          placeholder="What political issues matter most to you? How would you describe your political philosophy? What do you want from your local government?"
          className="w-full px-3 py-2 text-sm font-mono bg-bg-elevated border border-border rounded text-text-primary placeholder:text-text-tertiary focus:outline-none focus:border-accent-blue/50 resize-y disabled:opacity-50"
        />
      </div>

      {/* Value Dimension Sliders */}
      <div className="mb-8 bg-bg-panel border border-border rounded-lg p-4">
        <h3 className="font-mono text-xs font-bold text-text-primary tracking-wide mb-2">
          VALUE DIMENSIONS
        </h3>
        <p className="text-xs text-text-tertiary mb-4">
          Where do you fall on each spectrum? Slide to indicate your preference. Center means no strong preference.
        </p>
        <div className="space-y-4">
          {VALUE_DIMENSIONS.map(dim => (
            <div key={dim.key}>
              <div className="flex justify-between text-xs text-text-secondary mb-1">
                <span>{dim.left}</span>
                <span>{dim.right}</span>
              </div>
              <div className="flex items-center gap-2">
                <input
                  type="range"
                  min="-100"
                  max="100"
                  value={Math.round(values[dim.key] * 100)}
                  onChange={e => setValues(v => ({ ...v, [dim.key]: parseInt(e.target.value) / 100 }))}
                  disabled={generating}
                  className="flex-1 accent-accent-blue disabled:opacity-50"
                />
                <span className="text-xs font-mono text-text-tertiary w-10 text-right">
                  {values[dim.key] > 0 ? '+' : ''}{values[dim.key].toFixed(1)}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Issue Salience */}
      <div className="mb-8 bg-bg-panel border border-border rounded-lg p-4">
        <h3 className="font-mono text-xs font-bold text-text-primary tracking-wide mb-2">
          ISSUE PRIORITIES
        </h3>
        <p className="text-xs text-text-tertiary mb-4">
          How important is each issue to you personally? (0 = not a priority, 100 = top priority)
        </p>
        <div className="space-y-3">
          {ISSUE_DOMAINS.map(domain => (
            <div key={domain} className="flex items-center gap-3">
              <span className="text-xs text-text-secondary w-48 flex-shrink-0 truncate" title={domain}>
                {domain}
              </span>
              <input
                type="range"
                min="0"
                max="100"
                value={issueSalience[domain]}
                onChange={e => setIssueSalience(s => ({ ...s, [domain]: parseInt(e.target.value) }))}
                disabled={generating}
                className="flex-1 accent-accent-blue disabled:opacity-50"
              />
              <span className="text-xs font-mono text-text-tertiary w-8 text-right">
                {issueSalience[domain]}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Engagement Appetite */}
      <div className="mb-8 bg-bg-panel border border-border rounded-lg p-4">
        <h3 className="font-mono text-xs font-bold text-text-primary tracking-wide mb-2">
          ENGAGEMENT APPETITE
        </h3>
        <p className="text-xs text-text-tertiary mb-4">
          How willing are you to engage in different forms of civic participation?
        </p>
        <div className="space-y-3">
          {ENGAGEMENT_QUESTIONS.map(q => (
            <div key={q.key} className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-3">
              <span className="text-xs text-text-secondary sm:w-64 flex-shrink-0">
                {q.label}
              </span>
              <div className="flex gap-1">
                {q.options.map(opt => (
                  <button
                    key={opt}
                    onClick={() => setEngagement(e => ({ ...e, [q.key]: opt }))}
                    disabled={generating}
                    className={`px-3 py-1 text-xs font-mono rounded border transition-colors ${
                      engagement[q.key] === opt
                        ? 'bg-accent-blue/15 text-accent-blue border-accent-blue/30'
                        : 'text-text-tertiary border-border hover:text-text-secondary hover:border-accent-blue/20'
                    } disabled:opacity-50`}
                  >
                    {opt}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Error / Success Messages */}
      {error && (
        <div className="mb-4 px-4 py-3 bg-accent-red/10 border border-accent-red/30 rounded-lg text-sm text-accent-red font-mono">
          {error}
        </div>
      )}
      {success && (
        <div className="mb-4 px-4 py-3 bg-accent-green/10 border border-accent-green/30 rounded-lg text-sm text-accent-green font-mono">
          Profile generated and saved. Visit your Dashboard to see the results.
        </div>
      )}

      {/* Regenerate Button */}
      <button
        onClick={handleRegenerate}
        disabled={generating || !isValidKey}
        className={`w-full py-3 px-4 font-mono text-sm font-bold rounded-lg border-2 transition-all duration-150 ${
          generating
            ? 'bg-accent-blue/10 text-accent-blue border-accent-blue/30 cursor-wait'
            : !isValidKey
              ? 'bg-bg-elevated text-text-tertiary border-border cursor-not-allowed'
              : 'bg-accent-blue/15 text-accent-blue border-accent-blue/40 hover:bg-accent-blue/25 hover:border-accent-blue/60'
        }`}
      >
        {generating ? (
          <span className="flex items-center justify-center gap-2">
            <span className="animate-spin inline-block w-4 h-4 border-2 border-accent-blue/30 border-t-accent-blue rounded-full" />
            GENERATING PROFILE...
          </span>
        ) : (
          'REGENERATE PROFILE'
        )}
      </button>
      {!isValidKey && !error && (
        <p className="text-xs text-text-tertiary font-mono mt-2 text-center">
          Enter a valid API key above to enable profile generation.
        </p>
      )}
    </section>
  )
}
