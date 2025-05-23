const JSON_SERVER = process.env.NEXT_PUBLIC_JSON_SERVER

import { authHeader, queryParams } from '.'

export const getDocuments = ({
  session,
  page = 1,
  perPage = 10,
  sort,
  tags,
}) => {
  const params = JSON_SERVER
    ? {
        _page: page,
        _per_page: perPage,
        _sort: sort === 'newest-first' ? 'createDate' : '-createDate',
        tags: tags.join(','),
      }
    : { page, perPage, sort, tags: tags.join(',') }

  return fetch(`/api/documents?${queryParams(params)}`, {
    headers: { ...authHeader(session) },
    cache: 'no-cache',
  }).then((res) => res.json())
}
