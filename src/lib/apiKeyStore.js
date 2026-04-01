const STORAGE_KEY = 'cp_ak'
const SALT = 'civicpulse2024xk'

function xorWithSalt(str) {
  let result = ''
  for (let i = 0; i < str.length; i++) {
    result += String.fromCharCode(str.charCodeAt(i) ^ SALT.charCodeAt(i % SALT.length))
  }
  return result
}

export function saveApiKey(key) {
  if (!key) return clearApiKey()
  const obfuscated = btoa(xorWithSalt(key))
  localStorage.setItem(STORAGE_KEY, obfuscated)
}

export function getApiKey() {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (!stored) return null
  try {
    return xorWithSalt(atob(stored))
  } catch {
    return null
  }
}

export function clearApiKey() {
  localStorage.removeItem(STORAGE_KEY)
}
