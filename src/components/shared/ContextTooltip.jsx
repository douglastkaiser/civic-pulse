export default function ContextTooltip({ text }) {
  return (
    <span className="context-tooltip-wrapper">
      <span className="inline-flex items-center justify-center w-4 h-4 rounded-full text-xs text-text-tertiary border border-border hover:border-accent-blue/50 hover:text-accent-blue cursor-help transition-colors duration-150">
        ?
      </span>
      <span className="context-tooltip-content">
        {text}
      </span>
    </span>
  )
}
