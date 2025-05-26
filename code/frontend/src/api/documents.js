import { authHeader, queryParams } from '.'

export const getDocuments = ({
  session,
  page = 1,
  perPage = 10,
  sort,
  tags,
}) => {
  const params = { page, perPage, sort, tags: tags.join(',') }

  return fetch(`/api/documents?${queryParams(params)}`, {
    headers: { ...authHeader(session) },
    cache: 'no-cache',
  }).then((res) => (res.ok ? res.json() : Promise.reject(res)))
}

export const uploadDocument = ({ session, file, uploadCb }) => {
  const xhr = new XMLHttpRequest()

  return new Promise((resolve, reject) => {
    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable) {
        uploadCb(e.loaded / e.total)
      } else {
        uploadCb(-1 /* indeterminate */)
      }
    })

    xhr.addEventListener('loadend', () => {
      if (xhr.readyState !== XMLHttpRequest.DONE) {
        reject({ message: '"loadend" received when the request was not ready' })
      } else if (xhr.status === 200) {
        try {
          resolve(JSON.parse(xhr.response))
        } catch (e) {
          reject({ message: e })
        }
      } else {
        reject({
          message: `Request failed with status code ${xhr.status}`,
          status: xhr.status,
          response: xhr.response,
        })
      }
    })

    xhr.addEventListener('error', () => {
      reject({ message: 'Network error' })
    })

    xhr.open('POST', '/api/documents/upload', true)
    xhr.setRequestHeader('Authorization', `Bearer ${session.idToken}`)

    const formData = new FormData()
    formData.set('file', file)
    xhr.send(formData)
  })
}