import { Inter } from 'next/font/google'
import './globals.css'

const interSans = Inter({
  variable: '--font-inter-sans',
  subsets: ['latin', 'cyrillic'],
})

export const metadata = {
  title: 'Центр электронных документов',
  description: 'Организация и анализ PDF-документов',
}

export default function RootLayout({ children }) {
  return (
    <html lang="ru">
      <body className={`${interSans.variable} antialiased`}>{children}</body>
    </html>
  )
}
