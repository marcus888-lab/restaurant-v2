import React from 'react'
import { MainLayout } from '../components/layout/MainLayout'

export function RewardsPage() {
  return (
    <MainLayout>
      <div className="p-6">
        <h1 className="text-2xl font-bold text-[#F4E6CD] mb-6">我的奖励</h1>
        
        {/* Points Card */}
        <div className="bg-gradient-to-r from-[#FE9870] to-[#FF8A65] rounded-xl p-6 mb-6">
          <div className="text-[#1B2037]">
            <h2 className="text-lg font-semibold mb-2">积分余额</h2>
            <div className="text-3xl font-bold mb-1">0</div>
            <p className="text-sm opacity-80">总共获得: 0 积分</p>
          </div>
        </div>

        {/* Member Tier */}
        <div className="bg-[#222845] rounded-xl p-6 mb-6">
          <h3 className="text-[#F4E6CD] text-lg font-semibold mb-4">会员等级</h3>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-[#FE9870] font-medium">铜卡会员</p>
              <p className="text-[#D1D2D7] text-sm">每笔消费获得1倍积分</p>
            </div>
            <div className="w-12 h-12 bg-[#CD7F32] rounded-full flex items-center justify-center">
              <span className="text-white font-bold">铜</span>
            </div>
          </div>
        </div>

        {/* Benefits */}
        <div className="bg-[#222845] rounded-xl p-6">
          <h3 className="text-[#F4E6CD] text-lg font-semibold mb-4">会员权益</h3>
          <ul className="space-y-3">
            <li className="flex items-center text-[#D1D2D7]">
              <div className="w-2 h-2 bg-[#FE9870] rounded-full mr-3"></div>
              每笔消费获得1倍积分
            </li>
            <li className="flex items-center text-[#D1D2D7]">
              <div className="w-2 h-2 bg-[#FE9870] rounded-full mr-3"></div>
              200积分兑换免费咖啡
            </li>
          </ul>
        </div>
      </div>
    </MainLayout>
  )
}