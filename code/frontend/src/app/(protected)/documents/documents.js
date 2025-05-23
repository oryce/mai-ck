'use client'

import * as Headless from '@headlessui/react'
import { CalendarDaysIcon } from '@heroicons/react/16/solid'
import {
  ArrowDownTrayIcon,
  ArrowTopRightOnSquareIcon,
  BarsArrowDownIcon,
  BarsArrowUpIcon,
  FunnelIcon,
  PencilSquareIcon,
} from '@heroicons/react/20/solid'
import { clsx } from 'clsx'
import { useSession } from 'next-auth/react'
import { useEffect, useState } from 'react'

import { getDocuments } from '@/api/documents'
import { Badge, RandomBadge } from '@/components/badge'
import { Button } from '@/components/button'
import { Divider } from '@/components/divider'
import { Heading } from '@/components/heading'
import {
  ListboxLabel,
  ListboxOption,
  ListboxOptions,
} from '@/components/listbox'
import {
  Pagination,
  PaginationGap,
  PaginationList,
  PaginationNext,
  PaginationPage,
  PaginationPrevious,
} from '@/components/pagination'
import { Strong, Text } from '@/components/text'

function SortSelector({ selectedSort, setSelectedSort, ...props }) {
  const sorts = [
    {
      value: 'newest-first',
      name: 'Сначала новые',
      icon: <BarsArrowDownIcon />,
    },
    {
      value: 'oldest-first',
      name: 'Сначала старые',
      icon: <BarsArrowUpIcon />,
    },
  ]

  return (
    <Headless.Listbox value={selectedSort} onChange={setSelectedSort}>
      <Headless.ListboxButton as={Button} outline>
        {sorts.find((sort) => sort.value === selectedSort).icon}
      </Headless.ListboxButton>
      <ListboxOptions>
        {sorts.map(({ value, name }) => (
          <ListboxOption key={value} value={value}>
            <ListboxLabel>{name}</ListboxLabel>
          </ListboxOption>
        ))}
      </ListboxOptions>
    </Headless.Listbox>
  )
}

function TagSelector({ selectedTags, setSelectedTags, ...props }) {
  const tags = [
    { value: 'signature', name: 'Подпись' },
    { value: 'stamp', name: 'Печать' },
  ]

  return (
    <Headless.Listbox value={selectedTags} onChange={setSelectedTags} multiple>
      <Headless.ListboxButton as={Button} outline>
        <FunnelIcon />
      </Headless.ListboxButton>
      <ListboxOptions>
        {tags.map(({ value, name }) => (
          <ListboxOption key={value} value={value}>
            {name}
          </ListboxOption>
        ))}
      </ListboxOptions>
    </Headless.Listbox>
  )
}

function DocumentSkeleton({ ...props }) {
  return (
    <div className="h-[270px] w-[215px] animate-pulse rounded-md bg-zinc-200" />
  )
}

function Document({ document, ...props }) {
  const { name, createDate, type, tags } = document

  const formattedDate = new Intl.DateTimeFormat('ru-RU', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date(createDate))

  return (
    <div
      className={clsx(
        'relative w-[250px] rounded-md shadow-xs md:w-[215px]',
        'ring-1 ring-zinc-950/5 dark:ring-white/10'
      )}
    >
      <div
        className="h-[300px] rounded-t-md bg-[url(/pdf-placeholder.jpg)] bg-cover bg-center md:h-[270px]"
        role="presentation"
      />
      <div className="p-2">
        <Text>
          <Strong>{name}</Strong>
        </Text>
        <Text>
          <Badge color="indigo">{type}</Badge>
          <span className="ml-2">
            <CalendarDaysIcon className="inline size-4" /> {formattedDate}
          </span>
        </Text>
        <div className="mt-1.5 flex justify-around gap-2">
          <Button className="w-full" outline>
            <ArrowTopRightOnSquareIcon />
          </Button>
          <Button className="w-full" outline>
            <PencilSquareIcon />
          </Button>
          <Button className="w-full" outline>
            <ArrowDownTrayIcon />
          </Button>
        </div>
      </div>
      <div className="absolute top-1 right-1 flex flex-col items-end gap-0.5">
        {tags.map((tag, i) => (
          <RandomBadge key={i}>{tag}</RandomBadge>
        ))}
      </div>
    </div>
  )
}

function Paginator({ currentPage, pageInfo, className, ...props }) {
  const { first, last, prev, next, pages } = pageInfo

  const getPageNumbers = () => {
    const minPages = 7

    if (pages <= minPages) {
      // Show pages fully.
      return [...Array(pages)].map((_, i) => i + 1)
    }

    let pageList = []

    // Always show the first page.
    pageList.push(first)

    const startPage = Math.max(2, currentPage - 1)
    const endPage = Math.min(pages - 1, currentPage + 1)

    // Add a gap if we're away from the first page.
    if (startPage > 2) {
      pages.push('...')
    }

    for (let i = startPage; i <= endPage; i++) {
      pages.push(i)
    }

    // Add a gap if we're away from the last page.
    if (endPage < pages - 1) {
      pages.push('...')
    }

    // Always show the last page.
    pageList.push(last)

    return pageList
  }

  const pageNumbers = getPageNumbers()

  return (
    <Pagination className={className}>
      <PaginationPrevious href={prev && `?page=${prev}`}>
        Назад
      </PaginationPrevious>
      <PaginationList>
        {pageNumbers.map((page, i) =>
          page === '...' ? (
            <PaginationGap key={i} />
          ) : (
            <PaginationPage
              key={i}
              href={`?page=${page}`}
              current={page === currentPage}
            >
              {page}
            </PaginationPage>
          )
        )}
      </PaginationList>
      <PaginationNext href={next && `?page=${next}`}>Вперёд</PaginationNext>
    </Pagination>
  )
}

export default function DocumentsClient({ currentPage }) {
  const { data: session } = useSession()
  const [documents, setDocuments] = useState([])
  const [isLoading, setLoading] = useState(false)
  const [selectedSort, setSelectedSort] = useState('newest-first')
  const [selectedTags, setSelectedTags] = useState([])
  const [pageInfo, setPageInfo] = useState(null)

  useEffect(() => {
    setLoading(true)

    getDocuments({
      session,
      page: currentPage,
      perPage: 10,
      sort: selectedSort,
      tags: selectedTags,
    })
      .then((res) => {
        const { data: documents, ...pageInfo } = res

        setDocuments(documents)
        setPageInfo(pageInfo)
        setLoading(false)
      })
      .catch(() => alert('Cannot load documents'))
  }, [currentPage, selectedSort, selectedTags])

  return (
    <>
      <section className="flex justify-between">
        <Heading>Документы</Heading>
        <div className="space-x-2">
          <SortSelector
            selectedSort={selectedSort}
            setSelectedSort={setSelectedSort}
          />
          <TagSelector
            selectedTags={selectedTags}
            setSelectedTags={setSelectedTags}
          />
        </div>
      </section>
      <Divider className="mt-2" />
      <section
        className={clsx(
          'mt-6 grid w-full justify-items-center gap-4',
          'grid-cols-1 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5'
        )}
      >
        {isLoading
          ? [...Array(10)].map((_, i) => <DocumentSkeleton key={i} />)
          : documents.map((document, i) => (
              <Document key={i} document={document} />
            ))}
      </section>
      {pageInfo && (
        <Paginator
          className="mt-6"
          currentPage={currentPage}
          pageInfo={pageInfo}
        />
      )}
    </>
  )
}
