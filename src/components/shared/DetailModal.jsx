import { useEffect, useRef, useId } from 'react'

export default function DetailModal({ open, onClose, title, tabs, activeTab, onTabChange, children }) {
  const backdropRef = useRef(null)
  const dialogRef = useRef(null)
  const titleId = useId()

  useEffect(() => {
    if (!open) return
    const previous = document.activeElement
    dialogRef.current?.focus()
    const handleKey = (e) => {
      if (e.key === 'Escape') onClose()
      if (e.key === 'Tab') {
        const controls = [...dialogRef.current.querySelectorAll('button, a[href], input, select, textarea, [tabindex="0"]')].filter(el => !el.disabled && el.getClientRects().length)
        const first = controls[0], last = controls.at(-1)
        if (!first) { e.preventDefault(); return }
        if (e.shiftKey && (document.activeElement === first || document.activeElement === dialogRef.current)) { e.preventDefault(); last.focus() }
        else if (!e.shiftKey && (document.activeElement === last || document.activeElement === dialogRef.current)) { e.preventDefault(); first.focus() }
      }
    }
    document.addEventListener('keydown', handleKey)
    return () => { document.removeEventListener('keydown', handleKey); previous?.focus() }
  }, [open, onClose])

  // Prevent body scroll when open
  useEffect(() => {
    if (open) {
      document.body.style.overflow = 'hidden'
      return () => { document.body.style.overflow = '' }
    }
  }, [open])

  if (!open) return null

  return (
    <div
      ref={backdropRef}
      className="fixed inset-0 z-50 flex items-center justify-center animate-fade-in"
      onClick={(e) => { if (e.target === backdropRef.current) onClose() }}
    >
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/70 pointer-events-none" />

      {/* Modal panel */}
      <div ref={dialogRef} role="dialog" aria-modal="true" aria-labelledby={titleId} tabIndex={-1} className="relative w-[95vw] sm:w-[85vw] max-w-6xl h-[85vh] bg-bg-panel border border-border rounded-lg flex flex-col overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-3 border-b border-border flex-shrink-0">
          <div className="flex items-center gap-4 min-w-0 flex-1">
            <h2 id={titleId} className="font-mono text-sm font-bold text-text-primary tracking-wide truncate">
              {title}
            </h2>
            {/* Tabs */}
            {tabs?.length > 0 && (
              <div className="flex gap-1 overflow-x-auto min-w-0">
                {tabs.map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => onTabChange?.(tab.id)}
                    className={`px-3 py-1.5 text-xs font-mono rounded whitespace-nowrap transition-colors ${
                      activeTab === tab.id
                        ? 'bg-accent-blue/20 text-accent-blue border border-accent-blue/30'
                        : 'text-text-tertiary hover:text-text-secondary hover:bg-bg-elevated border border-transparent'
                    }`}
                  >
                    {tab.label}
                  </button>
                ))}
              </div>
            )}
          </div>
          <button
            onClick={onClose}
            aria-label="Close details"
            className="text-text-tertiary hover:text-text-primary text-lg ml-4 flex-shrink-0 w-8 h-8 flex items-center justify-center rounded hover:bg-bg-elevated transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto min-h-0 p-5">
          {children}
        </div>
      </div>
    </div>
  )
}
