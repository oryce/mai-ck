import Inter from 'next/font/local'
import './globals.css'

const interSans = Inter({
  variable: '--font-inter-sans',
  src: [
    { path: './fonts/inter.ttf' },
    { path: './fonts/inter-italic.ttf', style: 'italic'} 
  ]
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
