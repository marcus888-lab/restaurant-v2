import { useUser, useClerk } from '@clerk/clerk-react'
import { Button } from '../components/ui/Button'

export function Dashboard() {
  const { user } = useUser()
  const { signOut } = useClerk()

  const handleSignOut = () => {
    signOut()
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-8">
          <div className="flex justify-between items-start mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                欢迎回到咖啡馆
              </h1>
              <p className="text-gray-600">
                你好, {user?.emailAddresses[0]?.emailAddress}
              </p>
            </div>
            <Button 
              variant="secondary" 
              onClick={handleSignOut}
            >
              退出登录
            </Button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-gradient-to-br from-orange-100 to-orange-200 p-6 rounded-lg">
              <h3 className="font-semibold text-orange-800 mb-2">今日订单</h3>
              <p className="text-2xl font-bold text-orange-900">12</p>
            </div>
            
            <div className="bg-gradient-to-br from-green-100 to-green-200 p-6 rounded-lg">
              <h3 className="font-semibold text-green-800 mb-2">总收入</h3>
              <p className="text-2xl font-bold text-green-900">¥1,234</p>
            </div>
            
            <div className="bg-gradient-to-br from-blue-100 to-blue-200 p-6 rounded-lg">
              <h3 className="font-semibold text-blue-800 mb-2">会员数量</h3>
              <p className="text-2xl font-bold text-blue-900">56</p>
            </div>
          </div>
          
          <div className="mt-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">快速操作</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Button variant="secondary" className="h-20">
                新订单
              </Button>
              <Button variant="secondary" className="h-20">
                菜单管理
              </Button>
              <Button variant="secondary" className="h-20">
                会员管理
              </Button>
              <Button variant="secondary" className="h-20">
                报告
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}