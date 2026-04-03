/**
 * Compute a salience-weighted alignment score for an official.
 *
 * The raw alignment score is adjusted by how much the user cares about the
 * official's relevant policy domains. Officials whose domains match the user's
 * top priorities get amplified scores (further from zero); officials whose
 * domains are low-priority get dampened scores (closer to zero).
 *
 * @param {object} official - Official object with alignment.score and alignment.relevant_domains
 * @param {object} issueSalience - Map of domain name → salience weight (0-100)
 * @returns {{ weightedScore: number, salience: number, domainWeights: Array }}
 */
export function computeWeightedAlignment(official, issueSalience) {
  const score = official.alignment?.score ?? 0
  const domains = official.alignment?.relevant_domains ?? []

  if (!issueSalience || Object.keys(issueSalience).length === 0 || domains.length === 0) {
    return { weightedScore: score, salience: 50, domainWeights: [] }
  }

  // Compute average salience across the official's relevant domains
  const domainWeights = domains.map((domain) => ({
    domain,
    weight: issueSalience[domain] ?? 50, // default to neutral if not in user's list
  }))

  const avgSalience = domainWeights.reduce((sum, d) => sum + d.weight, 0) / domainWeights.length

  // Normalize: 50 = neutral (no change), 100 = max amplification, 0 = max dampening
  // multiplier range: 0.4 (low salience) to 1.6 (high salience)
  const multiplier = 0.4 + (avgSalience / 100) * 1.2

  const weightedScore = Math.max(-1, Math.min(1, score * multiplier))

  return { weightedScore, salience: avgSalience, domainWeights }
}

/**
 * Apply weighted alignment to all officials in a branches structure.
 * Returns a new branches array with weightedAlignment added to each official.
 */
export function applyWeightedAlignments(branches, issueSalience) {
  if (!branches) return branches

  return branches.map((branch) => ({
    ...branch,
    levels: branch.levels.map((level) => ({
      ...level,
      officials: (level.officials || []).map((official) => ({
        ...official,
        weightedAlignment: computeWeightedAlignment(official, issueSalience),
      })),
    })),
  }))
}
