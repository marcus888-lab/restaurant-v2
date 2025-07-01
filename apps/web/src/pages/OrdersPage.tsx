import React from 'react'
import { MainLayout } from '../components/layout/MainLayout'

export function OrdersPage() {
  return (
    <MainLayout>
      <div className="p-6">
        <h1 className="text-2xl font-bold text-[#F4E6CD] mb-6">我的订单</h1>
        
        <div className="text-center py-16">
          <div className="w-20 h-20 bg-[#222845] rounded-full mx-auto mb-4 flex items-center justify-center">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 3H5L5.4 5H19L18 11H6.6L5 3Z" stroke="#D1D2D7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <circle cx="9" cy="20" r="1" stroke="#D1D2D7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <circle cx="20" cy="20" r="1" stroke="#D1D2D7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <p className="text-[#D1D2D7] text-lg">暂无订单</p>
          <p className="text-[#D1D2D7] text-sm opacity-70 mt-2">您还没有任何订单记录</p>
        </div>
      </div>
    </MainLayout>
  )
}