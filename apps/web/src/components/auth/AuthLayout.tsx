import type { ReactNode } from 'react'

interface AuthLayoutProps {
  children: ReactNode
  title: string
  subtitle?: string
}

export function AuthLayout({ children, title, subtitle }: AuthLayoutProps) {
  return (
    <div className="min-h-screen bg-[#1B1F36] flex items-center justify-center p-7">
      {/* Background pattern/image would go here */}
      <div className="w-full max-w-md">
        {/* Welcome text */}
        <div className="text-center mb-12">
          <h1 className="text-[#F4E6CD] text-3xl font-medium font-kumbh-sans leading-[1.24]">
            {title}
          </h1>
          {subtitle && (
            <p className="text-[#F4E6CD] text-lg mt-2">{subtitle}</p>
          )}
        </div>
        
        {/* Auth card */}
        <div className="bg-white rounded-2xl p-7 shadow-[0px_35px_40px_0px_rgba(0,0,0,0.21)]">
          {children}
        </div>
      </div>
    </div>
  )
}