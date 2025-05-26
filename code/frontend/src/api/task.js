import { authHeader } from '.'

export const getTaskStatus = ({ session, taskId }) =>
  fetch(`/api/tasks/${taskId}`, {
    headers: { ...authHeader(session) },
    cache: 'no-store',
  }).then((res) => (res.ok ? res.json() : Promise.reject(res)))
