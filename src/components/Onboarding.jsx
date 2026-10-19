import { useState } from 'react'
import { JURISDICTIONS, coverageLabel } from '../lib/civic'
import { savePreferences } from '../lib/residentStore'
export const TOPICS = [
  'Housing',
  'Transportation',
  'Education',
  'Public Safety',
  'Environment',
  'Budget',
  'Land Use',
  'Healthcare',
]
export default function Onboarding({ user, preferences, onDone }) {
  const [locationId, setLocation] = useState(
    preferences?.locationId || JURISDICTIONS[0].id
  )
  const [interests, setInterests] = useState(preferences?.interests || [])
  const [minutes, setMinutes] = useState(preferences?.availableMinutes || 15)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)
  async function submit(event) {
    event.preventDefault()
    setSaving(true)
    setError(null)
    try {
      await savePreferences(user.uid, {
        ...preferences,
        locationId,
        interests,
        availableMinutes: Number(minutes),
        weeklyDigest: preferences?.weeklyDigest === true,
        deadlineReminders: preferences?.deadlineReminders === true,
      })
      onDone?.()
    } catch {
      setError('Your preferences could not be saved. Please try again.')
    } finally {
      setSaving(false)
    }
  }
  return (
    <form onSubmit={submit} className="civic-card max-w-2xl mx-auto space-y-6">
      <div>
        <p className="eyebrow">A little local knowledge goes a long way</p>
        <h1 className="text-3xl font-semibold mt-2">
          Make your community your priority.
        </h1>
        <p className="text-text-secondary mt-3">
          Choose what matters to you. Your political profile is optional, and
          you can change these choices any time.
        </p>
      </div>
      <label className="block">
        Your area
        <select
          value={locationId}
          onChange={(e) => setLocation(e.target.value)}
          className="civic-input mt-2"
        >
          {JURISDICTIONS.map((j) => (
            <option key={j.id} value={j.id}>
              {j.label}
            </option>
          ))}
        </select>
        <span className="block text-sm text-text-secondary mt-2">
          {coverageLabel(locationId)}
        </span>
      </label>
      <fieldset>
        <legend className="mb-3">What would you like to follow?</legend>
        <div className="flex flex-wrap gap-2">
          {TOPICS.map((topic) => (
            <label
              key={topic}
              className="topic-choice flex gap-2 items-center"
            >
              <input
                type="checkbox"
                checked={interests.includes(topic)}
                onChange={() =>
                  setInterests((current) =>
                    current.includes(topic)
                      ? current.filter((t) => t !== topic)
                      : [...current, topic]
                  )
                }
              />
              {topic}
            </label>
          ))}
        </div>
      </fieldset>
      <label className="block">
        Time you have for an action
        <select
          value={minutes}
          onChange={(e) => setMinutes(e.target.value)}
          className="civic-input mt-2"
        >
          {[5, 15, 30, 60].map((m) => (
            <option key={m} value={m}>
              {m} minutes
            </option>
          ))}
        </select>
        <span className="block mt-2 text-sm text-text-secondary">
          We’ll show your time preference alongside actions. Effort estimates
          appear only when available.
        </span>
      </label>
      {error && (
        <p role="alert" className="text-accent-red">
          {error}
        </p>
      )}
      <button className="civic-button" disabled={saving}>
        {saving ? 'Saving…' : 'Save and see local issues'}
      </button>
    </form>
  )
}
