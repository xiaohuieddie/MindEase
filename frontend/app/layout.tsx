import type { Metadata } from 'next'
import './globals.css'
import { ThemeProvider } from "@/components/theme-provider"
import LogViewer from "@/components/LogViewer"

export const metadata: Metadata = {
  title: 'MindEase - AI Mental Wellness Companion',
  description: 'Your AI-powered mental wellness companion for support and guidance',
  generator: 'MindEase',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
        >
          {children}
          {process.env.NODE_ENV === 'development' && <LogViewer />}
        </ThemeProvider>
      </body>
    </html>
  )
}
