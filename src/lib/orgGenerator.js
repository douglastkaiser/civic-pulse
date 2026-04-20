const API_URL = 'https://api.anthropic.com/v1/messages'
const MODEL = 'claude-haiku-4-5-20251001'

const SYSTEM_PROMPT = `You are an organization strategy analyst for Civic Pulse, a local government monitoring dashboard.

Given basic information about a civic organization (name, geographic scope, core issue areas, and mission), generate a comprehensive organization profile.

You MUST return ONLY valid JSON (no markdown, no code blocks, no explanation) with exactly this structure:

{
  "id": "custom-kebab-case-slug-from-name",
  "name": "Organization Name",
  "tagline": "One compelling sentence that captures the org's essence",
  "mission": "Multi-paragraph mission statement. Be specific about the local context, the problems being addressed, and why this organization exists. Include concrete local data points and statistics where plausible. 3-5 paragraphs.",
  "theory_of_change": "A paragraph explaining how this organization creates impact — what levers it pulls, what mechanisms drive change, and why the strategy is realistic.",
  "geographic_scope": {
    "city": "City Name",
    "county": "County Name",
    "state": "State"
  },
  "founded": "YYYY-MM-DD",
  "political_positioning": {
    "description": "A paragraph describing where the org sits politically — its coalition, its allies, who it is NOT aligned with, and its ideological approach.",
    "compass_cloud": {
      "economic_center": <number -1 to 1, negative=left/interventionist, positive=right/free-market>,
      "economic_spread": <number 0.1 to 0.5>,
      "social_center": <number -1 to 1, negative=libertarian, positive=authoritarian>,
      "social_spread": <number 0.1 to 0.5>
    }
  },
  "key_policy_positions": [
    "Specific policy position 1 — actionable and local",
    "Specific policy position 2",
    "... (5-10 positions)"
  ],
  "active_campaigns": [
    {
      "id": "kebab-case-campaign-id",
      "title": "Campaign Title",
      "status": "active" or "planning",
      "priority": "high" or "medium" or "low",
      "importance_score": <integer 0-100>,
      "impact_score": <integer 0-100>,
      "summary": "Detailed 2-3 paragraph summary of the campaign — what it does, why it matters, what specific actions are involved. Be concrete and specific to the local context.",
      "theory_of_change": "How this specific campaign creates change — what lever, what decision-maker, what realistic path to impact.",
      "next_actions": [
        "Specific actionable next step 1",
        "Specific actionable next step 2",
        "... (4-7 actions)"
      ],
      "bridge_building": {
        "opposition_steelman": "Strongest good-faith argument from skeptics",
        "cross_partisan_appeals": [
          {
            "audience": "Who this framing is for",
            "framing": "Respectful framing that meets their values",
            "evidence": "One concise supporting fact",
            "example_dialogue": "Optional one-line conversation opener"
          }
        ],
        "common_ground": ["Shared values or goals"],
        "conversation_traps_to_avoid": ["Polarizing framing to avoid"],
        "when_to_acknowledge_uncertainty": ["Where confidence should be limited"],
        "honest_limits": ["What this campaign cannot promise"],
        "provenance": {
          "status": "ai_generated",
          "updated_at": "ISO timestamp or omit",
          "updated_by": "user id/name or omit"
        },
        "subsection_provenance": {
          "opposition_steelman": { "status": "ai_generated" },
          "cross_partisan_appeals": { "status": "ai_generated" },
          "common_ground": { "status": "ai_generated" },
          "conversation_traps_to_avoid": { "status": "ai_generated" },
          "when_to_acknowledge_uncertainty": { "status": "ai_generated" },
          "honest_limits": { "status": "ai_generated" }
        }
      }
    }
  ],
  "aligned_organizations": [
    {
      "name": "Allied Org Name",
      "relationship": "Description of the relationship and shared interests. Be specific about what connects these orgs.",
      "url": "https://example.org (if plausible, otherwise omit this field)"
    }
  ],
  "engagement_pipeline": {
    "awareness": "How people first learn about the org — channels, content, distribution.",
    "interest": "How curious people deepen engagement — events, content, entry points.",
    "action": "How interested people take concrete action — specific activities and opportunities.",
    "leadership": "How active members become leaders — roles, responsibilities, growth paths."
  },
  "bridge_building": {
    "opposition_steelman": "Strongest good-faith argument from people who disagree",
    "cross_partisan_appeals": [
      {
        "audience": "Who this framing is for",
        "framing": "Respectful framing that meets their values",
        "evidence": "One concise supporting fact",
        "example_dialogue": "Optional one-line conversation opener"
      }
    ],
    "common_ground": ["Shared values or goals"],
    "conversation_traps_to_avoid": ["Polarizing framing to avoid"],
    "when_to_acknowledge_uncertainty": ["Where confidence should be limited"],
    "honest_limits": ["What this effort cannot promise"],
    "provenance": {
      "status": "ai_generated",
      "updated_at": "ISO timestamp or omit",
      "updated_by": "user id/name or omit"
    },
    "subsection_provenance": {
      "opposition_steelman": { "status": "ai_generated" },
      "cross_partisan_appeals": { "status": "ai_generated" },
      "common_ground": { "status": "ai_generated" },
      "conversation_traps_to_avoid": { "status": "ai_generated" },
      "when_to_acknowledge_uncertainty": { "status": "ai_generated" },
      "honest_limits": { "status": "ai_generated" }
    }
  },
  "practical_next_steps_for_org": {
    "immediate": [
      {
        "action": "Specific immediate action",
        "owner": "Team or role responsible",
        "deadline": "YYYY-MM-DD (within 2-4 weeks)",
        "effort": "Time estimate (e.g., '4 hours')",
        "impact": "high" or "medium" or "low"
      }
    ],
    "medium_term": [
      {
        "action": "Specific medium-term action",
        "deadline": "YYYY-MM-DD (1-3 months out)",
        "effort": "Time estimate",
        "impact": "high" or "medium" or "low" or "very high"
      }
    ],
    "strategic": [
      {
        "action": "Strategic long-term action",
        "timeframe": "Q designation or date range",
        "impact": "high" or "very high",
        "notes": "Context and strategic rationale"
      }
    ]
  }
}

Rules:
- The "id" field MUST start with "custom-" followed by a kebab-case slug derived from the org name
- Generate 3-5 active_campaigns with realistic, locally-specific next actions
- Generate 5-10 key_policy_positions that are concrete and actionable
- Generate 5-8 aligned_organizations that are plausible local or regional partners
- The "founded" field should use today's date provided in the user message
- The mission should be substantive (3-5 paragraphs) with local context and specifics
- Campaign summaries should be 2-3 paragraphs each with concrete details
- All content should be grounded in the specific geographic location provided
- Political positioning should be nuanced — describe the actual coalition, not a caricature
- Engagement pipeline should have concrete, actionable content at each tier
- Practical next steps should have realistic deadlines relative to the founding date
- Generate 3-4 immediate steps, 3-4 medium-term steps, and 2-3 strategic steps
- Do NOT generate generic boilerplate — every field should be specific to this org's mission and location
- For every bridge_building.provenance or subsection_provenance status, use one of: ai_generated | user_reviewed | user_edited`

function extractJSON(text) {
  if (text.includes('```json')) {
    text = text.split('```json')[1].split('```')[0]
  } else if (text.includes('```')) {
    text = text.split('```')[1].split('```')[0]
  }
  return JSON.parse(text.trim())
}

function validateOrg(data) {
  const required = ['id', 'name', 'tagline', 'mission', 'theory_of_change', 'geographic_scope', 'political_positioning', 'key_policy_positions', 'active_campaigns', 'aligned_organizations', 'engagement_pipeline', 'bridge_building', 'practical_next_steps_for_org']
  for (const key of required) {
    if (!(key in data)) throw new Error(`Missing required field: ${key}`)
  }

  if (!data.id.startsWith('custom-')) {
    data.id = 'custom-' + data.id
  }

  const cc = data.political_positioning?.compass_cloud
  if (!cc || typeof cc.economic_center !== 'number' || typeof cc.social_center !== 'number') {
    throw new Error('Invalid political_positioning.compass_cloud format')
  }

  if (!Array.isArray(data.active_campaigns) || data.active_campaigns.length === 0) {
    throw new Error('active_campaigns must be a non-empty array')
  }

  if (!Array.isArray(data.key_policy_positions) || data.key_policy_positions.length === 0) {
    throw new Error('key_policy_positions must be a non-empty array')
  }

  const pipeline = data.engagement_pipeline
  if (!pipeline?.awareness || !pipeline?.interest || !pipeline?.action || !pipeline?.leadership) {
    throw new Error('engagement_pipeline must include awareness, interest, action, and leadership')
  }

  const steps = data.practical_next_steps_for_org
  if (!steps?.immediate || !steps?.medium_term || !steps?.strategic) {
    throw new Error('practical_next_steps_for_org must include immediate, medium_term, and strategic')
  }
}

export async function generateOrg(formData, apiKey) {
  const today = new Date().toISOString().split('T')[0]

  const userContent = [
    'Please generate a comprehensive organization profile for the following civic organization:',
    '',
    `## Organization Name`,
    formData.name,
    '',
    `## Geographic Scope`,
    formData.geographicScope,
    '',
    `## Core Issue Areas`,
    formData.coreIssues,
    '',
    `## Mission / Purpose (user-provided summary)`,
    formData.mission,
    '',
    `## Today's Date (use for "founded" field and as basis for deadlines)`,
    today,
  ].join('\n')

  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      'anthropic-dangerous-direct-browser-access': 'true',
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: 8192,
      system: SYSTEM_PROMPT,
      messages: [{ role: 'user', content: userContent }],
    }),
  })

  if (!response.ok) {
    const status = response.status
    if (status === 401) throw new Error('Invalid API key. Please check your key and try again.')
    if (status === 429) throw new Error('Rate limited. Please wait a moment and try again.')
    if (status === 400) throw new Error('Bad request. Please try again.')
    if (status === 529) throw new Error('Anthropic API is overloaded. Please try again in a few minutes.')
    throw new Error(`API request failed (${status}). Please try again.`)
  }

  const result = await response.json()
  const text = result.content?.[0]?.text
  if (!text) throw new Error('Empty response from API. Please try again.')

  const org = extractJSON(text)
  validateOrg(org)
  return org
}
