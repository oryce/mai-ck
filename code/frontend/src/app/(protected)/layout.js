'use client'

import { useState } from 'react'
import Image from 'next/image'

import {
  ArrowRightStartOnRectangleIcon,
  Cog6ToothIcon,
} from '@heroicons/react/16/solid'
import { MagnifyingGlassIcon, ArrowUpTrayIcon } from '@heroicons/react/20/solid'

import { AvatarButton } from '@/components/avatar'
import { Button } from '@/components/button'
import {
  Dialog,
  DialogActions,
  DialogBody,
  DialogDescription,
  DialogTitle,
} from '@/components/dialog'
import {
  Dropdown,
  DropdownButton,
  DropdownDivider,
  DropdownHeader,
  DropdownItem,
  DropdownLabel,
  DropdownMenu,
} from '@/components/dropdown'
import { Input, InputGroup } from '@/components/input'
import {
  Navbar,
  NavbarItem,
  NavbarSection,
  NavbarSpacer,
} from '@/components/navbar'
import { StackedLayout } from '@/components/stacked-layout'
import { Link } from '@/components/link'

function UserDropdownMenu() {
  return (
    <Dropdown>
      <DropdownButton
        className="size-10"
        as={AvatarButton}
        src="https://avatars.githubusercontent.com/u/124599?v=4"
      />
      <DropdownMenu anchor="bottom start">
        <DropdownHeader>
          <span className="text-sm/7 font-semibold text-zinc-800 dark:text-white">
            Иван Иванов
          </span>
        </DropdownHeader>
        <DropdownDivider />
        <DropdownItem href="/settings">
          <Cog6ToothIcon />
          <DropdownLabel>Администрирование</DropdownLabel>
        </DropdownItem>
        <DropdownItem href="#">
          <ArrowRightStartOnRectangleIcon />
          <DropdownLabel>Выйти</DropdownLabel>
        </DropdownItem>
      </DropdownMenu>
    </Dropdown>
  )
}

function SearchDialog({ open, setOpen }) {
  return (
    <Dialog open={open} onClose={setOpen}>
      <DialogTitle>Поиск документов</DialogTitle>
      <DialogDescription>
        Введите название документа или текст из содержимого.
      </DialogDescription>
      <DialogBody>
        <InputGroup>
          <MagnifyingGlassIcon />
          <Input
            autoFocus
            name="search-query"
            placeholder="Введите запрос..."
          />
        </InputGroup>
      </DialogBody>
      <DialogActions>
        <Button plain onClick={() => setOpen(false)}>
          Закрыть
        </Button>
        <Button>Найти</Button>
      </DialogActions>
    </Dialog>
  )
}

export default function MainLayout({ children }) {
  const [searchOpen, setSearchOpen] = useState(false)

  return (
    <StackedLayout
      navbar={
        <Navbar>
          <Link href="/documents">
            <Image
              src="/logo-alt.svg"
              alt="MAI's Hive Logo"
              width={45}
              height={45}
            />
          </Link>
          <NavbarSection>
            <NavbarItem href="/documents" current={true}>
              Главная
            </NavbarItem>
          </NavbarSection>
          <NavbarSpacer />
          <NavbarSection>
            <NavbarItem onClick={() => setSearchOpen(true)}>
              <MagnifyingGlassIcon />
              <span className="max-lg:hidden">Найти</span>
            </NavbarItem>
            <SearchDialog open={searchOpen} setOpen={setSearchOpen} />
            <NavbarItem>
              <ArrowUpTrayIcon />
              <span className="max-lg:hidden">Загрузить</span>
            </NavbarItem>
            <UserDropdownMenu />
          </NavbarSection>
        </Navbar>
      }
      mobileSidebar={false}
    >
      {children}
    </StackedLayout>
  )
}
