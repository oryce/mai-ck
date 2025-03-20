export const hashCode = (string) => {
  let hash = 0

  for (let i = 0; i < string.length; i++) {
    let chr = string.charCodeAt(i)
    hash = (hash << 5) - hash + chr
    hash = hash & hash // Convert to 32-bit integer
  }

  return hash
}
