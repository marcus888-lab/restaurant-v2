import React from 'react'
import { useAuth, useUser } from '@clerk/clerk-react'
import { MainLayout } from '../components/layout/MainLayout'

export function ProfilePage() {
  const { signOut } = useAuth()
  const { user } = useUser()

  const handleSignOut = () => {
    signOut()
  }

  const menuItems = [
    { id: 'orders', label: '我的订单', icon: '📋' },
    { id: 'addresses', label: '收货地址', icon: '📍' },
    { id: 'favorites', label: '我的收藏', icon: '❤️' },
    { id: 'notifications', label: '消息通知', icon: '🔔' },
    { id: 'settings', label: '设置', icon: '⚙️' },
    { id: 'help', label: '帮助中心', icon: '❓' },
  ]

  return (
    <MainLayout>
      <div className="p-6">
        {/* User Profile Section */}
        <div className="flex items-center space-x-4 mb-8">
          <div className="w-16 h-16 bg-[#FE9870] rounded-full flex items-center justify-center">
            {user?.imageUrl ? (
              <img
                src={user.imageUrl}
                alt="Profile"
                className="w-full h-full rounded-full object-cover"
              />
            ) : (
              <span className="text-[#1B2037] text-xl font-bold">
                {user?.firstName?.charAt(0) || user?.emailAddresses[0]?.emailAddress.charAt(0) || 'U'}
              </span>
            )}
          </div>
          <div>
            <h2 className="text-[#F4E6CD] text-xl font-semibold">
              {user?.firstName || user?.emailAddresses[0]?.emailAddress || '用户'}
            </h2>
            <p className="text-[#D1D2D7] text-sm">
              {user?.emailAddresses[0]?.emailAddress}
            </p>
          </div>
        </div>

        {/* Menu Items */}
        <div className="space-y-2">
          {menuItems.map((item) => (
            <button
              key={item.id}
              className="w-full bg-[#222845] rounded-lg p-4 flex items-center justify-between hover:bg-[#2A2F45] transition-colors"
            >
              <div className="flex items-center space-x-3">
                <span className="text-xl">{item.icon}</span>
                <span className="text-[#F4E6CD] font-medium">{item.label}</span>
              </div>
              <svg width="8" height="12" viewBox="0 0 8 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M1 1L6 6L1 11" stroke="#D1D2D7" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          ))}
        </div>

        {/* Sign Out Button */}
        <button
          onClick={handleSignOut}
          className="w-full mt-8 bg-red-600 hover:bg-red-700 text-white rounded-lg p-4 font-medium transition-colors"
        >
          退出登录
        </button>
      </div>
    </MainLayout>
  )
}