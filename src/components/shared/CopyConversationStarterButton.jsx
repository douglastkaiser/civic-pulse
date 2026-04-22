import { useMemo, useState } from 'react'
import { buildBridgeConversationStarterPrompt } from '../../lib/bridgePromptBuilder'

export default function CopyConversationStarterButton({ appeal, bridge }) {
  const [copied, setCopied] = useState(false)

  const prompt = useMemo(
    () => buildBridgeConversationStarterPrompt({ appeal, bridge }),
    [appeal, bridge],
  )

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
      className="inline-flex items-center gap-1 px-1.5 py-0.5 text-xs rounded border font-mono transition-colors bg-accent-blue/10 text-accent-blue border-accent-blue/30 hover:bg-accent-blue/20"
      title="Copy a conversation-starter prompt for this appeal"
    >
      {copied ? '✓ Copied' : 'Draft a conversation starter'}
    </button>
  )
}
