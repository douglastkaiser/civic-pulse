import {
  getFunctions,
  httpsCallable,
  connectFunctionsEmulator,
} from 'firebase/functions'
import { app } from './firebase'
const functions = getFunctions(
  app,
  import.meta.env.VITE_FUNCTIONS_REGION || 'us-central1'
)
if (import.meta.env.DEV && import.meta.env.VITE_USE_EMULATORS === 'true')
  connectFunctionsEmulator(functions, '127.0.0.1', 5001)
export async function callService(name, data = {}) {
  try {
    const result = await httpsCallable(functions, name, { timeout: 90000 })(
      data
    )
    return result.data
  } catch (error) {
    const messages = {
      'functions/unavailable':
        'This service is temporarily unavailable. Please try again later.',
      'functions/unauthenticated': 'Please sign in again.',
      'functions/resource-exhausted':
        'Your usage limit has been reached. Please try again later.',
      'functions/not-found': 'This service has not been configured yet.',
      'functions/internal':
        'This request could not be completed. Please try again later.',
    }
    throw new Error(
      messages[error.code] ||
        error.message ||
        'This request could not be completed.'
    )
  }
}
