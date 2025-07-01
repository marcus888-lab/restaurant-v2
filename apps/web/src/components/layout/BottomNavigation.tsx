import React from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

interface NavItem {
  id: string
  label: string
  path: string
  icon: React.ReactNode
  activeIcon: React.ReactNode
}

export function BottomNavigation() {
  const location = useLocation()
  const navigate = useNavigate()

  const navItems: NavItem[] = [
    {
      id: 'home',
      label: '首页',
      path: '/home',
      icon: <HomeIcon />,
      activeIcon: <HomeActiveIcon />
    },
    {
      id: 'orders',
      label: '订单',
      path: '/orders',
      icon: <OrderIcon />,
      activeIcon: <OrderActiveIcon />
    },
    {
      id: 'rewards',
      label: '奖励',
      path: '/rewards',
      icon: <RewardIcon />,
      activeIcon: <RewardActiveIcon />
    },
    {
      id: 'profile',
      label: '我的',
      path: '/profile',
      icon: <UserIcon />,
      activeIcon: <UserActiveIcon />
    }
  ]

  const handleNavClick = (path: string) => {
    navigate(path)
  }

  return (
    <div className="fixed bottom-0 left-1/2 transform -translate-x-1/2 w-full max-w-sm bg-[#23283E] h-16 flex items-center justify-around z-50">
      {navItems.map((item) => {
        const isActive = location.pathname === item.path
        
        return (
          <button
            key={item.id}
            onClick={() => handleNavClick(item.path)}
            className="flex flex-col items-center justify-center h-full min-w-0 flex-1"
          >
            {isActive ? (
              <div className="relative">
                <div className="w-[34px] h-[34px] bg-[#FE9870] rounded-full flex items-center justify-center">
                  {item.activeIcon}
                </div>
              </div>
            ) : (
              <div className="w-6 h-6 flex items-center justify-center">
                {item.icon}
              </div>
            )}
          </button>
        )
      })}
    </div>
  )
}

// Home Icons
function HomeIcon() {
  return (
    <svg width="18" height="19" viewBox="0 0 18 19" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M1.4 7.07L9 1.18L16.6 7.07V16.18C16.6 16.626 16.422 17.054 16.109 17.367C15.796 17.68 15.368 17.858 14.922 17.858H3.078C2.632 17.858 2.204 17.68 1.891 17.367C1.578 17.054 1.4 16.626 1.4 16.18V7.07Z" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M6.6 17.858V9.418H11.4V17.858" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  )
}

function HomeActiveIcon() {
  return (
    <svg width="18" height="19" viewBox="0 0 18 19" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M1.4 7.07L9 1.18L16.6 7.07V16.18C16.6 16.626 16.422 17.054 16.109 17.367C15.796 17.68 15.368 17.858 14.922 17.858H3.078C2.632 17.858 2.204 17.68 1.891 17.367C1.578 17.054 1.4 16.626 1.4 16.18V7.07Z" stroke="#1B2037" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M6.6 17.858V9.418H11.4V17.858" stroke="#1B2037" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  )
}

// Order Icons
function OrderIcon() {
  return (
    <svg width="18" height="19" viewBox="0 0 18 19" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M3.5 4.598L14.5 4.598L13.622 14.598L4.378 14.598L3.5 4.598Z" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M3.5 4.598L2.5 2.598L1 2.598" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M12 8.598L12 10.598" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  )
}

function OrderActiveIcon() {
  return (
    <svg width="18" height="19" viewBox="0 0 18 19" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M3.5 4.598L14.5 4.598L13.622 14.598L4.378 14.598L3.5 4.598Z" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M3.5 4.598L2.5 2.598L1 2.598" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M12 8.598L12 10.598" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  )
}

// Reward Icons
function RewardIcon() {
  return (
    <svg width="20" height="19" viewBox="0 0 20 19" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M17 7.598L17 5.598C17 5.067 16.789 4.559 16.414 4.184C16.039 3.809 15.531 3.598 15 3.598L5 3.598C4.469 3.598 3.961 3.809 3.586 4.184C3.211 4.559 3 5.067 3 5.598L3 7.598" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M17 11.598L15 13.598L17 15.598L17 11.598Z" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M3 11.598L5 13.598L3 15.598L3 11.598Z" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M7 7.598L13 7.598" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M10 7.598L10 15.598" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  )
}

function RewardActiveIcon() {
  return (
    <svg width="20" height="19" viewBox="0 0 20 19" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M17 7.598L17 5.598C17 5.067 16.789 4.559 16.414 4.184C16.039 3.809 15.531 3.598 15 3.598L5 3.598C4.469 3.598 3.961 3.809 3.586 4.184C3.211 4.559 3 5.067 3 5.598L3 7.598" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M17 11.598L15 13.598L17 15.598L17 11.598Z" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M3 11.598L5 13.598L3 15.598L3 11.598Z" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M7 7.598L13 7.598" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M10 7.598L10 15.598" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  )
}

// User Icons
function UserIcon() {
  return (
    <svg width="17" height="19" viewBox="0 0 17 19" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M16 17.598V15.598C16 14.537 15.579 13.52 14.829 12.77C14.079 12.02 13.061 11.598 12 11.598L4 11.598C2.939 11.598 1.921 12.02 1.171 12.77C0.421 13.52 0 14.537 0 15.598V17.598" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M8 7.598C10.209 7.598 12 5.807 12 3.598C12 1.389 10.209 -0.402 8 -0.402C5.791 -0.402 4 1.389 4 3.598C4 5.807 5.791 7.598 8 7.598Z" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  )
}

function UserActiveIcon() {
  return (
    <svg width="17" height="19" viewBox="0 0 17 19" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M16 17.598V15.598C16 14.537 15.579 13.52 14.829 12.77C14.079 12.02 13.061 11.598 12 11.598L4 11.598C2.939 11.598 1.921 12.02 1.171 12.77C0.421 13.52 0 14.537 0 15.598V17.598" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M8 7.598C10.209 7.598 12 5.807 12 3.598C12 1.389 10.209 -0.402 8 -0.402C5.791 -0.402 4 1.389 4 3.598C4 5.807 5.791 7.598 8 7.598Z" stroke="#F4E6CD" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  )
}