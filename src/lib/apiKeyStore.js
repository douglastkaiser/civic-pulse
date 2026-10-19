// Remove credentials saved by older versions. Generation uses authenticated server calls.
export function clearApiKey() { try { localStorage.removeItem('cp_ak') } catch { /* Storage may be disabled. */ } }
