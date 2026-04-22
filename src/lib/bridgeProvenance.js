const VALID_PROVENANCE_STATUSES = new Set(['ai_generated', 'user_reviewed', 'user_edited'])

const BRIDGE_SUBSECTIONS = [
  'opposition_steelman',
  'cross_partisan_appeals',
  'common_ground',
  'conversation_traps_to_avoid',
  'when_to_acknowledge_uncertainty',
  'honest_limits',
]

function normalizeProvenanceRecord(record) {
  if (!record || typeof record !== 'object') {
    return { status: 'ai_generated' }
  }

  const status = VALID_PROVENANCE_STATUSES.has(record.status) ? record.status : 'ai_generated'
  const normalized = { status }

  if (record.updated_at) normalized.updated_at = record.updated_at
  if (record.updated_by) normalized.updated_by = record.updated_by

  return normalized
}

function normalizeSubsectionProvenance(subsectionProvenance) {
  const input = subsectionProvenance && typeof subsectionProvenance === 'object'
    ? subsectionProvenance
    : {}

  return BRIDGE_SUBSECTIONS.reduce((acc, key) => {
    acc[key] = normalizeProvenanceRecord(input[key])
    return acc
  }, {})
}

export function normalizeBridgeBlockProvenance(bridgeBlock) {
  if (!bridgeBlock || typeof bridgeBlock !== 'object') return bridgeBlock

  return {
    ...bridgeBlock,
    provenance: normalizeProvenanceRecord(bridgeBlock.provenance),
    subsection_provenance: normalizeSubsectionProvenance(bridgeBlock.subsection_provenance),
  }
}

export function normalizeOrgBridgeProvenance(org) {
  if (!org || typeof org !== 'object') return org

  return {
    ...org,
    bridge_building: normalizeBridgeBlockProvenance(org.bridge_building),
    active_campaigns: Array.isArray(org.active_campaigns)
      ? org.active_campaigns.map((campaign) => ({
        ...campaign,
        bridge_building: normalizeBridgeBlockProvenance(campaign.bridge_building),
      }))
      : org.active_campaigns,
  }
}

export function normalizeLocationBridgeProvenance(location) {
  if (!location || typeof location !== 'object') return location

  return {
    ...location,
    upcoming_elections: Array.isArray(location.upcoming_elections)
      ? location.upcoming_elections.map((election) => ({
        ...election,
        bridge_building: normalizeBridgeBlockProvenance(election.bridge_building),
      }))
      : location.upcoming_elections,
  }
}
