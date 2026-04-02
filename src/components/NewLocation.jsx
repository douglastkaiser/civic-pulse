import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { getApiKey } from '../lib/apiKeyStore'
import { generateLocation } from '../lib/locationGenerator'
import { saveLocation, saveLocationIssues, registerLocation } from '../lib/locationStore'
import { LOCATION_LABELS } from '../lib/data'

export default function NewLocation() {
  const navigate = useNavigate()
  const [city, setCity] = useState('')
  const [state, setState] = useState('')
  const [zip, setZip] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const apiKey = getApiKey()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)

    const trimmedCity = city.trim()
    const trimmedState = state.trim()
    const trimmedZip = zip.trim()

    if (!trimmedCity || !trimmedState || !trimmedZip) {
      setError('All fields are required.')
      return
    }

    if (!/^\d{5}$/.test(trimmedZip)) {
      setError('Please enter a valid 5-digit zip code.')
      return
    }

    const slug = `${trimmedCity.toLowerCase().replace(/\s+/g, '-')}-${trimmedZip}`

    if (LOCATION_LABELS[slug]) {
      setError(`${trimmedCity}, ${trimmedState} (${trimmedZip}) already exists.`)
      return
    }

    setLoading(true)
    try {
      const data = await generateLocation(trimmedCity, trimmedState, trimmedZip, apiKey)

      // Ensure the location ID matches our slug
      data.location.id = slug

      await saveLocation(slug, data.location)
      await saveLocationIssues(slug, data.issues)
      await registerLocation(slug, `${trimmedCity}, ${trimmedState.toUpperCase()}`)

      navigate(`/location/${slug}`)
    } catch (err) {
      console.error('Failed to generate location:', err)
      setError(err.message || 'Failed to generate location. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-full overflow-auto p-4 animate-fade-in">
      <Link to="/dashboard" className="text-xs text-text-tertiary hover:text-accent-blue font-mono transition-colors">
        &larr; Back to Dashboard
      </Link>

      <div className="max-w-xl mx-auto mt-8">
        <h1 className="font-mono text-lg font-bold text-text-primary tracking-wide mb-2">
          + NEW LOCATION
        </h1>
        <p className="text-sm text-text-secondary leading-relaxed mb-6">
          Add a new location to your Civic Pulse dashboard. We'll use AI to generate
          a comprehensive political landscape — governing bodies, active issues,
          upcoming elections, and civic engagement opportunities.
        </p>

        <div className="bg-bg-panel border border-border rounded-lg p-4 space-y-4">
          {!apiKey && (
            <div className="px-3 py-2 bg-accent-amber/10 border border-accent-amber/30 rounded text-xs text-accent-amber font-mono text-center">
              API key required &mdash;{' '}
              <Link to="/settings" className="underline hover:text-accent-amber/80">
                add your Anthropic API key in Settings
              </Link>
            </div>
          )}

          {error && (
            <div className="px-3 py-2 bg-accent-red/10 border border-accent-red/30 rounded text-xs text-accent-red font-mono">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-3">
            <div>
              <label className="block text-xs font-mono text-text-tertiary mb-1">CITY / AREA NAME</label>
              <input
                type="text"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                disabled={loading}
                placeholder="e.g., Denver"
                className="w-full bg-bg-elevated border border-border rounded px-3 py-2 text-sm text-text-primary placeholder-text-tertiary disabled:opacity-50"
              />
            </div>
            <div>
              <label className="block text-xs font-mono text-text-tertiary mb-1">STATE</label>
              <input
                type="text"
                value={state}
                onChange={(e) => setState(e.target.value)}
                disabled={loading}
                placeholder="e.g., CO"
                className="w-full bg-bg-elevated border border-border rounded px-3 py-2 text-sm text-text-primary placeholder-text-tertiary disabled:opacity-50"
              />
            </div>
            <div>
              <label className="block text-xs font-mono text-text-tertiary mb-1">ZIP CODE</label>
              <input
                type="text"
                value={zip}
                onChange={(e) => setZip(e.target.value)}
                disabled={loading}
                placeholder="e.g., 80202"
                maxLength={5}
                className="w-full bg-bg-elevated border border-border rounded px-3 py-2 text-sm text-text-primary placeholder-text-tertiary disabled:opacity-50"
              />
            </div>
            <button
              type="submit"
              disabled={!apiKey || loading}
              className="w-full bg-accent-blue/20 text-accent-blue font-mono text-sm py-2 rounded border border-accent-blue/30 hover:bg-accent-blue/30 transition-colors disabled:opacity-50 disabled:pointer-events-none"
            >
              {loading ? 'GENERATING LANDSCAPE...' : 'GENERATE LOCATION'}
            </button>
          </form>

          {loading && (
            <div className="text-xs text-text-tertiary font-mono text-center animate-pulse">
              Researching political landscape, governing bodies, and local issues...
              <br />
              This may take 30-60 seconds.
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
