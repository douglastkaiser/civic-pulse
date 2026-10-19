const cache = new Map()
export class DataError extends Error {
  constructor(message, status) {
    super(message)
    this.status = status
  }
}
export async function fetchJSON(
  url,
  { signal, validate = (value) => value, cacheMs = 60000 } = {}
) {
  const cached = cache.get(url)
  if (cached && cached.until > Date.now())
    return structuredClone(validate(cached.data))
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const response = await fetch(url, {
        signal: signal
          ? AbortSignal.any([signal, AbortSignal.timeout(15000)])
          : AbortSignal.timeout(15000),
      })
      if (!response.ok)
        throw new DataError(
          'Unable to load this information. Please try again.',
          response.status
        )
      const data = validate(await response.json())
      cache.set(url, { until: Date.now() + cacheMs, data })
      return structuredClone(data)
    } catch (error) {
      if (
        signal?.aborted ||
        error.name === 'AbortError' ||
        error instanceof SyntaxError ||
        (error.status && error.status < 500) ||
        attempt === 1
      )
        throw error
    }
  }
}
