import { getServerSession } from 'next-auth'
import Inter from 'next/font/local'

import './globals.css'

import { authOptions } from './api/auth/[...nextauth]/route'
import Providers from './providers'

const interSans = Inter({
  variable: '--font-inter-sans',
  src: [
    { path: './fonts/inter.ttf' },
    { path: './fonts/inter-italic.ttf', style: 'italic' },
  ],
})

export const metadata = {
  title: 'Центр электронных документов',
  description: 'Организация и анализ PDF-документов',
}

export default async function RootLayout({ children }) {
  const session = await getServerSession(authOptions)

  return (
    <html lang="ru">
      <body className={`${interSans.variable} antialiased`}>
        <Providers session={session}>{children}</Providers>
      </body>
    </html>
  )
}
