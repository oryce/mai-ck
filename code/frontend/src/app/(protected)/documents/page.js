'use client'

import { useState } from 'react'
import { clsx } from 'clsx'
import * as Headless from '@headlessui/react'
import {
  ArrowDownTrayIcon,
  ArrowTopRightOnSquareIcon,
  BarsArrowDownIcon,
  BarsArrowUpIcon,
  FunnelIcon,
  PencilSquareIcon,
} from '@heroicons/react/20/solid'
import { CalendarDaysIcon } from '@heroicons/react/16/solid'

import { Badge } from '@/components/badge'
import { Button } from '@/components/button'
import { Divider } from '@/components/divider'
import { Heading } from '@/components/heading'
import {
  ListboxLabel,
  ListboxOption,
  ListboxOptions,
} from '@/components/listbox'
import { Strong, Text } from '@/components/text'
import {
  Pagination,
  PaginationGap,
  PaginationList,
  PaginationNext,
  PaginationPage,
  PaginationPrevious,
} from '@/components/pagination'

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

function Document({ ...props }) {
  return (
    <div className="w-[250px] rounded-md shadow-xs ring-1 ring-zinc-950/5 md:w-[215px] dark:ring-white/10">
      <div
        className='h-[300px] rounded-t-md bg-[url("/pdf-placeholder.jpg")] bg-cover bg-center md:h-[270px]'
        role="presentation"
      />
      <div className="p-2">
        <Text>
          <Strong>Document title</Strong>
        </Text>
        <Text>
          <Badge color="indigo">Накладная</Badge>
          <span className="ml-2">
            <CalendarDaysIcon className="inline size-4" /> 18.03.2025
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
    </div>
  )
}

export default function Documents() {
  const [selectedSort, setSelectedSort] = useState('newest-first')
  const [selectedTags, setSelectedTags] = useState([])

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
        {[...Array(10)].map((_, i) => (
          <Document key={i} />
        ))}
      </section>
      <Pagination className="mt-6">
        <PaginationPrevious>Назад</PaginationPrevious>
        <PaginationList>
          <PaginationPage href="?page=1" current>
            1
          </PaginationPage>
          <PaginationPage href="?page=2">2</PaginationPage>
          <PaginationPage href="?page=3">3</PaginationPage>
          <PaginationPage href="?page=4">4</PaginationPage>
          <PaginationGap />
          <PaginationPage href="?page=4">8</PaginationPage>
          <PaginationPage href="?page=4">9</PaginationPage>
        </PaginationList>
        <PaginationNext href="?page=2">Вперёд</PaginationNext>
      </Pagination>
    </>
  )
}
