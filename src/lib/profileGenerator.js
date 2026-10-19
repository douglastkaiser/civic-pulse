import { callService } from './service'
export function generateProfile(quizAnswers) {
  return callService('generateResidentProfile', {
    quizAnswers,
    requestId: crypto.randomUUID(),
  })
}
