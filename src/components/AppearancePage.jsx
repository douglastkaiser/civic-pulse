import AppearanceSettings from './settings/AppearanceSettings'
export default function AppearancePage() {
  return (
    <div className="page-wrap max-w-4xl">
      <header className="page-heading">
        <p className="eyebrow">Preferences / appearance</p>
        <h1>Appearance settings</h1>
        <p className="text-text-secondary">
          Color, font, and size. Changes apply immediately and stay on this
          browser.
        </p>
      </header>
      <AppearanceSettings />
    </div>
  )
}
