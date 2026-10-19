import ResidentSettings from './settings/ResidentSettings'
import AppearanceSettings from './settings/AppearanceSettings'
import { useAuth } from '../lib/auth'
import PoliticalQuizSection from './settings/PoliticalQuizSection'
export default function SettingsPage() {
  const { user } = useAuth()
  return (
    <div className="page-wrap max-w-4xl space-y-4">
      <header className="page-heading">
        <p className="eyebrow">Preferences / profile</p>
        <h1>Your profile and preferences</h1>
        <p className="text-text-secondary">
          Manage your appearance, interests, and information.
        </p>
      </header>
      <AppearanceSettings />
      <ResidentSettings user={user} />
      <PoliticalQuizSection user={user} />
      <p className="text-xs text-text-tertiary border-t border-border pt-2">
        build: {__COMMIT_HASH__}
      </p>
    </div>
  )
}
