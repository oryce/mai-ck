export const queryParams = (params) => {
  const queryParams = new URLSearchParams()

  Object.entries(params)
    .filter(([key, value]) => value)
    .forEach(([key, value]) => {
      queryParams.set(key, value)
    })

  return queryParams
}
