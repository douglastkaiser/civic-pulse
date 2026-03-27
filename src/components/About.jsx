export default function About() {
  return (
    <div className="h-full overflow-auto p-4 lg:p-6 animate-fade-in">
      <div className="max-w-3xl mx-auto space-y-6">
        {/* Header */}
        <div className="bg-bg-panel border border-border rounded-lg p-5">
          <h1 className="font-mono text-lg font-bold text-text-primary tracking-wider mb-1">
            ABOUT CIVIC PULSE
          </h1>
          <p className="font-mono text-xs text-text-tertiary">
            Political intelligence for local government
          </p>
        </div>

        {/* What it is */}
        <div className="bg-bg-panel border border-border rounded-lg p-5">
          <h2 className="font-mono text-sm font-bold text-accent-blue tracking-wide mb-3">
            WHAT IT IS
          </h2>
          <p className="font-mono text-sm text-text-secondary leading-relaxed">
            A political intelligence dashboard that monitors local government, maps
            it against your priorities, and tells you what to do about it. It is the
            local political infrastructure that should exist but doesn't.
          </p>
        </div>

        {/* The Problem */}
        <div className="bg-bg-panel border border-border rounded-lg p-5">
          <h2 className="font-mono text-sm font-bold text-accent-red tracking-wide mb-3">
            THE PROBLEM
          </h2>
          <p className="font-mono text-sm text-text-secondary leading-relaxed">
            Nobody knows what their local government is doing. Finding out is
            unreasonably hard. The information exists — in scattered PDFs, buried
            agendas, and meetings nobody attends — but the cost of assembling it
            into something useful is prohibitive for any individual.
          </p>
          <p className="font-mono text-sm text-text-secondary leading-relaxed mt-3">
            This means local government operates in a low-information environment
            where organized special interests have outsized power and most residents
            have no idea what's being decided on their behalf.
          </p>
        </div>

        {/* How it works */}
        <div className="bg-bg-panel border border-border rounded-lg p-5">
          <h2 className="font-mono text-sm font-bold text-accent-green tracking-wide mb-3">
            HOW IT WORKS
          </h2>
          <p className="font-mono text-sm text-text-secondary leading-relaxed mb-4">
            AI processes public government data — agendas, votes, candidates,
            organizations — and delivers it through a dashboard calibrated to your
            political values and location. You tell it what you care about. It tells
            you what's happening and what you can do.
          </p>

          {/* Data flow diagram */}
          <div className="bg-bg-primary border border-border rounded p-4 font-mono text-xs text-text-tertiary leading-relaxed">
            <pre className="whitespace-pre overflow-x-auto">{`  ┌─────────────────┐
  │  PUBLIC RECORDS  │  Agendas, votes, candidates,
  │  City councils   │  campaign finance, org data
  │  County boards   │
  │  State agencies  │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  AI PROCESSING  │  Extract, summarize, score,
  │  Claude / LLM   │  match to your values
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │   YOUR VALUES   │  Political compass, issue
  │   + LOCATION    │  salience, engagement appetite
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │   DASHBOARD     │  Priority matrix, next steps,
  │   Personalized  │  issue feed, org tracking
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │     ACTION      │  Public comment, vote,
  │                 │  donate, volunteer, show up
  └─────────────────┘`}</pre>
          </div>
        </div>

        {/* Philosophy */}
        <div className="bg-bg-panel border border-border rounded-lg p-5">
          <h2 className="font-mono text-sm font-bold text-accent-purple tracking-wide mb-3">
            PHILOSOPHY
          </h2>
          <div className="space-y-4">
            <div>
              <h3 className="font-mono text-xs font-bold text-text-primary mb-1">
                1. PRACTICALITY OVER PERFORMANCE
              </h3>
              <p className="font-mono text-sm text-text-secondary leading-relaxed">
                Every recommendation answers "what can I actually do?" not "what
                should I feel?" The goal is to reduce the distance between caring
                about an issue and acting on it.
              </p>
            </div>
            <div>
              <h3 className="font-mono text-xs font-bold text-text-primary mb-1">
                2. LOCATION-SPECIFIC, VALUES-DRIVEN
              </h3>
              <p className="font-mono text-sm text-text-secondary leading-relaxed">
                Your politics are yours. The dashboard adapts to where you live,
                not what party you belong to. The same person can track issues
                across multiple locations with the same underlying values.
              </p>
            </div>
            <div>
              <h3 className="font-mono text-xs font-bold text-text-primary mb-1">
                3. TRANSPARENCY ABOUT AI
              </h3>
              <p className="font-mono text-sm text-text-secondary leading-relaxed">
                All AI-generated content is clearly labeled with the ✦ badge.
                The system shows its reasoning. You decide what to do with it.
                AI is a tool for processing public information, not a substitute
                for your judgment.
              </p>
            </div>
          </div>
        </div>

        {/* Open Source */}
        <div className="bg-bg-panel border border-border rounded-lg p-5">
          <h2 className="font-mono text-sm font-bold text-accent-amber tracking-wide mb-3">
            OPEN SOURCE
          </h2>
          <p className="font-mono text-sm text-text-secondary leading-relaxed">
            The project is open source on{' '}
            <a
              href="https://github.com/douglastkaiser/civic-pulse"
              target="_blank"
              rel="noopener noreferrer"
              className="text-accent-blue hover:underline"
            >
              GitHub
            </a>
            . The aspiration is that anyone could fork it, plug in their own
            location and values, and have a personalized civic intelligence system.
          </p>
          <p className="font-mono text-sm text-text-secondary leading-relaxed mt-3">
            The minimum viable level of civic engagement — knowing what's going
            on and showing up when it matters — should be accessible to anyone.
          </p>
        </div>

        {/* Footer */}
        <div className="text-center py-4">
          <span className="font-mono text-xs text-text-tertiary">
            CIVIC PULSE v0.2
          </span>
        </div>
      </div>
    </div>
  )
}
