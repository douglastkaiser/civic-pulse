import { useState } from 'react'
import { addDoc, collection, serverTimestamp } from 'firebase/firestore'
import { db } from '../lib/firebase'
import { useAuth } from '../lib/auth'
import { Link } from 'react-router-dom'
export default function NewLocation() {
  const { user } = useAuth()
  const [city, setCity] = useState(''),
    [state, setState] = useState(''),
    [zip, setZip] = useState(''),
    [busy, setBusy] = useState(false),
    [error, setError] = useState(null),
    [done, setDone] = useState(false)
  async function submit(event) {
    event.preventDefault()
    setBusy(true)
    setError(null)
    try {
      await addDoc(collection(db, 'coverageRequests'), {
        uid: user.uid,
        city: city.trim(),
        state: state.trim(),
        zip,
        createdAt: serverTimestamp(),
      })
      setDone(true)
    } catch {
      setError('Your request could not be saved. Please try again.')
    } finally {
      setBusy(false)
    }
  }
  return (
    <div className="page-wrap max-w-2xl">
      <h1 className="text-3xl font-semibold mb-4">Request local coverage</h1>
      <p className="text-text-secondary mb-6">
        New areas need a working official source before we can show reliable
        decisions. A request does not activate coverage.
      </p>
      {done ? (
        <div className="civic-card" role="status">
          Your coverage request is saved.{' '}
          <Link className="underline" to="/explore">
            Browse existing areas
          </Link>
        </div>
      ) : (
        <form onSubmit={submit} className="civic-card space-y-4">
          <label className="block">
            City or county
            <input
              className="civic-input mt-2"
              required
              maxLength={100}
              value={city}
              onChange={(e) => setCity(e.target.value)}
            />
          </label>
          <label className="block">
            State
            <input
              className="civic-input mt-2"
              required
              maxLength={100}
              value={state}
              onChange={(e) => setState(e.target.value)}
            />
          </label>
          <label className="block">
            ZIP code
            <input
              className="civic-input mt-2"
              required
              pattern="[0-9]{5}"
              inputMode="numeric"
              maxLength={5}
              value={zip}
              onChange={(e) => setZip(e.target.value)}
            />
          </label>
          {error && <p role="alert">{error}</p>}
          <button className="civic-button" disabled={busy}>
            {busy ? 'Saving…' : 'Save request'}
          </button>
        </form>
      )}
    </div>
  )
}
