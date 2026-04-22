const API_URL = 'https://api.anthropic.com/v1/messages'
const MODEL = 'claude-haiku-4-5-20251001'

const SYSTEM_PROMPT = `You are a local government and political landscape analyst for Civic Pulse, a civic engagement dashboard.

Given a city/area name, state, and zip code, generate a comprehensive local political landscape profile.

You MUST return ONLY valid JSON (no markdown, no code blocks, no explanation) with exactly these top-level keys:

{
  "location": {
    "id": "<slug, e.g. denver-80202>",
    "last_updated": "<current ISO timestamp>",
    "governing_bodies": [
      {
        "name": "City Council / Board of Supervisors / etc.",
        "type": "city_council|county_commission|school_board|transit_authority|state_legislature|federal",
        "url": "official website URL",
        "your_representative": {
          "name": "Representative name",
          "district": "District/ward if applicable",
          "contact_email": "email if known",
          "alignment_notes": "Brief political lean or focus areas"
        },
        "mayor": "Mayor name (if city council)",
        "meeting_schedule": "When and where they meet",
        "agenda_source": "URL for agendas",
        "public_comment_process": "How citizens can participate"
      }
    ],
    "political_organizations": {
      "advocacy_orgs": [
        {
          "name": "Org name",
          "focus": "What they work on",
          "alignment": "General political alignment",
          "url": "website",
          "how_to_engage": "How to get involved"
        }
      ],
      "official_party": [
        {
          "name": "Local party chapter",
          "focus": "What they do",
          "alignment": "Alignment notes",
          "url": "website"
        }
      ],
      "citizen_groups": [
        {
          "name": "Group name",
          "focus": "Focus area",
          "how_to_engage": "How to participate"
        }
      ],
      "media_and_info": [
        {
          "name": "Outlet name",
          "type": "Type of coverage",
          "url": "website"
        }
      ]
    },
    "upcoming_elections": [
      {
        "election_type": "candidate_race|ballot_measure (default candidate_race if omitted)",
        "race": "Race description (or measure title if contest is a ballot measure)",
        "date": "YYYY-MM-DD",
        "candidates": ["Candidate 1", "Candidate 2"],
        "relevance": "Why this matters",
        "action": "What a civic-minded resident should do",
        "measure_bridge_fields": {
          "what_each_side_thinks_measure_does": {
            "supporters": "How supporters describe the measure's practical effect",
            "opponents": "How opponents describe the measure's practical effect"
          },
          "empirical_claims_by_side": {
            "supporters": ["Claim(s) supporters say are factual and testable"],
            "opponents": ["Claim(s) opponents say are factual and testable"]
          },
          "values_vs_facts_disagreement": "Where disagreement is mostly values/priorities vs where it is factual dispute",
          "what_could_change_a_reasonable_opponents_mind": "Specific evidence or safeguard that could move a good-faith skeptic"
        },
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
        }
      }
    ],
    "key_political_dynamics": "2-4 paragraph narrative about the political landscape, key tensions, recent developments, and what to watch",
    "political_compass_entities": {
      "local_government": { "economic": <-1 to 1>, "social": <-1 to 1>, "spread": <0.1 to 0.4> },
      "state_government": { "economic": <-1 to 1>, "social": <-1 to 1>, "spread": <0.1 to 0.4> },
      "democratic_party": { "economic": -0.3, "social": -0.1, "spread": 0.3 },
      "republican_party": { "economic": 0.4, "social": 0.3, "spread": 0.25 },
      "local_orgs": [
        { "name": "Org name", "economic": <-1 to 1>, "social": <-1 to 1>, "spread": <0.1 to 0.3> }
      ]
    },
    "next_steps": {
      "immediate": [
        {
          "action": "Specific action to take now",
          "detail": "More details",
          "time": "Estimated time",
          "impact": "HIGH/MEDIUM/LOW",
          "reason": "Why this matters or null"
        }
      ],
      "this_month": [
        { "action": "...", "detail": "...", "time": "...", "impact": "...", "reason": null }
      ],
      "medium_term": [
        { "action": "...", "detail": "...", "time": "...", "impact": "...", "reason": null }
      ],
      "strategic": [
        { "action": "...", "detail": "...", "impact": "...", "reason": null }
      ]
    }
  },
  "issues": {
    "last_scraped": "<current ISO timestamp>",
    "issues": [
      {
        "id": "kebab-case-id",
        "title": "Issue title",
        "governing_body": "Which body is handling this",
        "governing_body_type": "city_council|county_commission|school_board|etc",
        "meeting_date": "YYYY-MM-DD or null",
        "summary": "Detailed summary of the issue, recent developments, and context",
        "policy_domains": ["Domain 1", "Domain 2"],
        "decision_type": "vote|discussion|election|petition|hearing",
        "geographic_scope": "neighborhood|district|citywide|citywide_impact|county|state",
        "public_comment": {
          "available": true/false,
          "deadline": "date or null",
          "instructions": "How to participate"
        },
        "estimated_contestedness": "high|medium|low",
        "importance_score": <1-100>,
        "impact_score": <1-100>,
        "quadrant": "act_now|monitor|background|delegate",
        "why_it_matters_to_you": "Why a civic-minded resident of this area should care",
        "source_url": "URL or null"
      }
    ]
  }
}

Rules:
- Generate 3-6 governing bodies relevant to the location (city/town council, county, school board, transit if applicable, state rep, US rep)
- Generate 6-10 current local issues with realistic importance and impact scores
- Upcoming elections may include candidate races and ballot measures; each item should include a bridge_building block with provenance metadata
- Ballot measures MUST set "election_type": "ballot_measure" and include all measure_bridge_fields keys with substantive content
- Candidate races should set "election_type": "candidate_race" (or omit election_type) and should not include placeholder-only measure_bridge_fields
- Include real organization names and URLs where you are confident they are correct
- For information you are uncertain about, note it (e.g. "verify current status")
- political_compass values: economic (-1=left/interventionist, 1=right/free-market), social (-1=libertarian, 1=authoritarian)
- next_steps should have 2-3 items per category, focused on actionable civic engagement
- Issues should span multiple policy domains (housing, transportation, education, public safety, budget, etc.)
- quadrant assignment: act_now (high importance + high impact), monitor (high importance + lower impact), background (lower importance), delegate (lower importance but high impact)
- Use current date for timestamps
- For every bridge_building.provenance or subsection_provenance status, use one of: ai_generated | user_reviewed | user_edited`

function extractJSON(text) {
  if (text.includes('```json')) {
    text = text.split('```json')[1].split('```')[0]
  } else if (text.includes('```')) {
    text = text.split('```')[1].split('```')[0]
  }
  return JSON.parse(text.trim())
}

function validateLocation(data) {
  if (!data.location) throw new Error('Missing required field: location')
  if (!data.issues) throw new Error('Missing required field: issues')

  const loc = data.location
  if (!Array.isArray(loc.governing_bodies) || loc.governing_bodies.length === 0) {
    throw new Error('governing_bodies must be a non-empty array')
  }
  if (!loc.political_organizations) {
    throw new Error('Missing political_organizations')
  }
  if (!loc.next_steps) {
    throw new Error('Missing next_steps')
  }

  const iss = data.issues
  if (!Array.isArray(iss.issues) || iss.issues.length === 0) {
    throw new Error('issues.issues must be a non-empty array')
  }
}

export async function generateLocation(city, state, zip, apiKey) {
  const userContent = [
    `Generate a comprehensive local political landscape profile for:`,
    ``,
    `City/Area: ${city}`,
    `State: ${state}`,
    `Zip Code: ${zip}`,
    ``,
    `Please include the most current information you have about local government, active issues, upcoming elections, and civic engagement opportunities for this area.`,
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
      max_tokens: 16384,
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

  const data = extractJSON(text)
  validateLocation(data)
  return data
}
