import DocumentsClient from './documents'

export default async function Documents({ searchParams }) {
  const { page } = await searchParams
  const initialPage = parseInt(page) || 1

  return (
    <>
      <DocumentsClient initialPage={initialPage} />
    </>
  )
}
