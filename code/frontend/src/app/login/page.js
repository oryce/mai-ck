import clsx from 'clsx'
import Image from 'next/image'
import Link from 'next/link'

import { Button } from '@/components/button'
import { Heading, Subheading } from '@/components/heading'

export default function Login() {
  return (
    <div className="flex h-screen w-screen">
      {/* Background */}
      <div
        className="hidden flex-1 bg-[url('/background.jpg')] bg-cover bg-center lg:block"
        role="presentation"
      />
      {/* Main content */}
      <div className="flex-1 bg-zinc-100 lg:p-5 dark:bg-zinc-950">
        <div
          className={clsx(
            'flex h-full flex-col bg-white p-5 lg:rounded-lg lg:shadow-xs dark:bg-zinc-900',
            'lg:ring-1 lg:ring-zinc-950/5 lg:dark:ring-white/10'
          )}
        >
          <main className="flex grow flex-col items-center justify-center">
            <Image
              src="/logo.svg"
              alt="MAI's Hive Logo"
              width={180}
              height={180}
            />
            <div className="mt-6 text-center">
              <Heading>Центр электронных документов</Heading>
              <Subheading className="mt-2 lg:mt-0">
                Организация и анализ PDF-документов
              </Subheading>
            </div>
            <Button className="mt-8 w-20">Войти</Button>
          </main>
          <footer className="flex justify-center">
            <Link href="https://github.com/oryce/mai-ck" target="_blank">
              <Image
                className="hidden dark:inline"
                src="/github-light.svg"
                alt="GitHub Page"
                width={32}
                height={32}
              />
              <Image
                className="dark:hidden"
                src="/github-dark.svg"
                alt="GitHub Page"
                width={32}
                height={32}
              />
            </Link>
          </footer>
        </div>
      </div>
    </div>
  )
}
