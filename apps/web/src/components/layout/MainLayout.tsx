import React from 'react'
import { BottomNavigation } from './BottomNavigation'
import { TopHeader } from './TopHeader'

interface MainLayoutProps {
  children: React.ReactNode
  showHeader?: boolean
  showBottomNav?: boolean
}

export function MainLayout({ 
  children, 
  showHeader = true, 
  showBottomNav = true 
}: MainLayoutProps) {
  return (
    <div className="min-h-screen bg-[#1B1F36] text-[#F4E6CD] flex flex-col max-w-sm mx-auto">
      {showHeader && <TopHeader />}
      
      <main className="flex-1 pb-16">
        {children}
      </main>
      
      {showBottomNav && <BottomNavigation />}
    </div>
  )
}