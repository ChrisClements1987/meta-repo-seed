import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: '{{PRODUCT_NAME_TITLE}}',
  description: 'Professional {{PRODUCT_NAME_TITLE}} application built with Business-in-a-Box',
  keywords: ['{{PRODUCT_NAME}}', 'nextjs', 'react', 'typescript'],
  authors: [{ name: 'Business-in-a-Box' }],
  viewport: 'width=device-width, initial-scale=1',
  themeColor: '#000000',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div id="__next">
          {children}
        </div>
      </body>
    </html>
  )
}
