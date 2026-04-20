function toBulletList(items = []) {
  if (!Array.isArray(items) || items.length === 0) return ''
  return items.map((item) => `- ${item}`).join('\n')
}

export function buildBridgeConversationStarterPrompt({ appeal, bridge } = {}) {
  if (!appeal || typeof appeal !== 'object') return null

  const sections = [
    'You are helping write a respectful, persuasive conversation opener for bridge-building outreach.',
    '',
    'Use the context below to draft one short conversation starter (2-4 sentences) that:',
    '- Leads with shared values, not partisan labels.',
    '- Uses plain language and avoids jargon.',
    '- Invites dialogue instead of trying to "win" the exchange.',
  ]

  if (appeal.audience) {
    sections.push('', `Audience: ${appeal.audience}`)
  }

  if (appeal.framing) {
    sections.push('', `Core framing to include: ${appeal.framing}`)
  }

  if (appeal.evidence) {
    sections.push('', `Supporting evidence: ${appeal.evidence}`)
  }

  if (appeal.example_dialogue) {
    sections.push('', `Optional style example: ${appeal.example_dialogue}`)
  }

  const commonGround = toBulletList(bridge?.common_ground)
  if (commonGround) {
    sections.push('', 'Common ground signals to weave in if helpful:', commonGround)
  }

  const traps = toBulletList(bridge?.conversation_traps_to_avoid)
  if (traps) {
    sections.push('', 'Avoid these traps:', traps)
  }

  sections.push('', 'Output only the drafted conversation starter text.')

  return sections.join('\n').trim()
}
