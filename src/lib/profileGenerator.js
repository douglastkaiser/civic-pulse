const API_URL = 'https://api.anthropic.com/v1/messages'
const MODEL = 'claude-haiku-4-5-20251001'

const SYSTEM_PROMPT = `You are a political profiling analyst for Civic Pulse, a local government monitoring dashboard.

Given a user's self-described political views, value dimension ratings, issue priorities, and engagement preferences, generate a comprehensive political profile.

You MUST return ONLY valid JSON (no markdown, no code blocks, no explanation) with exactly these top-level keys:

{
  "manifesto": {
    "manifesto_summary": "1-2 sentence summary of their political identity",
    "narrative": "3-5 paragraph detailed political manifesto in first person",
    "identity_tags": ["array", "of", "5-8", "short", "identity", "labels"],
    "issue_positions": [
      {
        "domain": "Issue Domain Name",
        "stance": "Concise stance description",
        "local_implication": "How this plays out locally",
        "likely_allies": "Groups/people who'd agree",
        "likely_friction": "Groups/people who'd disagree"
      }
    ]
  },
  "political_compass": {
    "user": {
      "economic": <number -1 to 1, negative=left/interventionist, positive=right/free-market>,
      "social": <number -1 to 1, negative=libertarian, positive=authoritarian>,
      "spread": <number 0.1 to 0.4, how broad/uncertain their positions are>
    }
  },
  "political_positions": [
    {
      "id": "kebab-case-id",
      "question": "The policy question this position addresses",
      "short_label": "Short Label",
      "domain": "Issue Domain",
      "position": <number -1 to 1, against to for>,
      "importance": <integer 1 to 5>,
      "rationale": "Brief explanation of why they hold this view",
      "source": "quiz"
    }
  ],
  "values": {
    "growth_vs_preservation": <number -1 to 1>,
    "local_vs_central": <number -1 to 1>,
    "market_vs_regulation": <number -1 to 1>,
    "individual_vs_collective": <number -1 to 1>,
    "fiscal_prudence_vs_investment": <number -1 to 1>,
    "process_vs_speed": <number -1 to 1>,
    "expertise_vs_democracy": <number -1 to 1>,
    "safety_vs_liberty": <number -1 to 1>,
    "present_vs_future": <number -1 to 1>,
    "universal_vs_targeted": <number -1 to 1>
  },
  "issue_salience": {
    "Domain Name": <number 0 to 100>
  },
  "political_context": {
    "party_lean": "e.g. moderate Democrat, conservative Republican, independent, etc.",
    "key_descriptors": ["array", "of", "4-6", "descriptors"]
  }
}

Rules:
- Generate 15-30 political_positions covering diverse policy areas
- The manifesto narrative should be written in first person, reflecting the user's actual stated views
- Do NOT lead or editorialize — reflect what the user expressed, not what you think they should believe
- issue_positions in manifesto should cover the user's top 5-7 priority domains
- political_compass values should be derived from their stated positions, not assumed from party affiliation
- If the user's freeform text is sparse, rely more heavily on the slider values
- values in the output should reflect the slider inputs but may be adjusted slightly based on freeform text
- issue_salience should reflect the priority sliders but may be adjusted based on freeform text emphasis`

function extractJSON(text) {
  // Handle markdown code blocks
  if (text.includes('```json')) {
    text = text.split('```json')[1].split('```')[0]
  } else if (text.includes('```')) {
    text = text.split('```')[1].split('```')[0]
  }
  return JSON.parse(text.trim())
}

function validateProfile(data) {
  const required = ['manifesto', 'political_compass', 'political_positions', 'values', 'issue_salience', 'political_context']
  for (const key of required) {
    if (!(key in data)) throw new Error(`Missing required field: ${key}`)
  }
  const compass = data.political_compass?.user
  if (!compass || typeof compass.economic !== 'number' || typeof compass.social !== 'number') {
    throw new Error('Invalid political_compass format')
  }
  if (!Array.isArray(data.political_positions) || data.political_positions.length === 0) {
    throw new Error('political_positions must be a non-empty array')
  }
  if (!data.manifesto?.manifesto_summary || !data.manifesto?.narrative) {
    throw new Error('manifesto must include manifesto_summary and narrative')
  }
}

export async function generateProfile(quizAnswers, apiKey) {
  const userContent = [
    'Here are my political quiz responses:',
    '',
    '## My Political Views (freeform)',
    quizAnswers.freeformText || '(No freeform text provided)',
    '',
    '## Value Dimension Ratings (-1 to 1 scale)',
    JSON.stringify(quizAnswers.values, null, 2),
    '',
    '## Issue Priority Ratings (0-100 scale)',
    JSON.stringify(quizAnswers.issueSalience, null, 2),
    '',
    '## Engagement Appetite',
    JSON.stringify(quizAnswers.engagement, null, 2),
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

  const profile = extractJSON(text)
  validateProfile(profile)
  return profile
}
