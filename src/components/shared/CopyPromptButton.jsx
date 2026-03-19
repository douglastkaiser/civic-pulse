import { useState } from 'react'

export default function CopyPromptButton({ prompt }) {
  const [copied, setCopied] = useState(false)

  if (!prompt) return null

  const handleCopy = (e) => {
    e.stopPropagation()
    navigator.clipboard.writeText(prompt).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }

  return (
    <button
      onClick={handleCopy}
      className="inline-flex items-center gap-1 px-1.5 py-0.5 text-xs rounded border font-mono transition-colors bg-accent-purple/10 text-accent-purple border-accent-purple/30 hover:bg-accent-purple/20"
      title="Copy an AI prompt for this action to your clipboard"
    >
      {copied ? '✓ Copied' : '✦ Draft with AI'}
    </button>
  )
}
