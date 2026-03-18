import { Link } from 'react-router-dom'

export default function NewOrg() {
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
          <div className="px-3 py-2 bg-accent-amber/10 border border-accent-amber/30 rounded text-xs text-accent-amber font-mono text-center">
            COMING SOON — Organization creation will be available when the pipeline is automated
          </div>

          <div className="space-y-3 opacity-50 pointer-events-none">
            <div>
              <label className="block text-xs font-mono text-text-tertiary mb-1">ORGANIZATION NAME</label>
              <input
                type="text"
                disabled
                placeholder="e.g., Austin YIMBY Action"
                className="w-full bg-bg-elevated border border-border rounded px-3 py-2 text-sm text-text-primary placeholder-text-tertiary"
              />
            </div>
            <div>
              <label className="block text-xs font-mono text-text-tertiary mb-1">GEOGRAPHIC SCOPE</label>
              <input
                type="text"
                disabled
                placeholder="e.g., Austin, TX"
                className="w-full bg-bg-elevated border border-border rounded px-3 py-2 text-sm text-text-primary placeholder-text-tertiary"
              />
            </div>
            <div>
              <label className="block text-xs font-mono text-text-tertiary mb-1">CORE ISSUE AREAS</label>
              <input
                type="text"
                disabled
                placeholder="e.g., Housing, Transportation, Land Use"
                className="w-full bg-bg-elevated border border-border rounded px-3 py-2 text-sm text-text-primary placeholder-text-tertiary"
              />
            </div>
            <div>
              <label className="block text-xs font-mono text-text-tertiary mb-1">MISSION (1-2 SENTENCES)</label>
              <textarea
                disabled
                rows={3}
                placeholder="What does your organization do and why?"
                className="w-full bg-bg-elevated border border-border rounded px-3 py-2 text-sm text-text-primary placeholder-text-tertiary resize-none"
              />
            </div>
            <button
              disabled
              className="w-full bg-accent-blue/20 text-accent-blue font-mono text-sm py-2 rounded border border-accent-blue/30"
            >
              CREATE ORGANIZATION
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
