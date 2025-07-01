import { useState } from 'react'
import { useSignIn } from '@clerk/clerk-react'
import { Link } from 'react-router-dom'
import { AuthLayout } from './AuthLayout'
import { Button } from '../ui/Button'
import { InputField } from '../ui/InputField'
import { SocialAuthButton } from '../ui/SocialAuthButton'

export function SignInPage() {
  const { signIn, setActive, isLoaded } = useSignIn()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!isLoaded) return

    setIsLoading(true)
    setError('')

    try {
      const result = await signIn.create({
        identifier: email,
        password,
      })

      if (result.status === 'complete') {
        await setActive({ session: result.createdSessionId })
        // Redirect will happen automatically
      } else {
        setError('登录失败，请检查您的凭据')
      }
    } catch (err) {
      console.error('Error:', err)
      setError('登录失败，请检查您的凭据')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSocialSignIn = async (provider: 'oauth_google' | 'oauth_facebook') => {
    if (!isLoaded) return

    try {
      await signIn.authenticateWithRedirect({
        strategy: provider,
        redirectUrl: '/sso-callback',
        redirectUrlComplete: '/dashboard'
      })
    } catch (err) {
      console.error('Social sign-in error:', err)
      setError('社交登录失败')
    }
  }

  return (
    <AuthLayout title="欢迎回来">
      <div className="space-y-6">
        <h2 className="text-[#232323] font-bold text-2xl font-montserrat">登录</h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <InputField
            type="email"
            placeholder="请输入"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          
          <InputField
            type="password"
            placeholder="密码"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            showPasswordToggle
            required
          />
          
          {error && (
            <div className="text-red-500 text-sm text-center">{error}</div>
          )}
          
          <Button 
            type="submit" 
            className="w-full"
            isLoading={isLoading}
            disabled={!email || !password}
          >
            登录
          </Button>
        </form>
        
        <div className="flex items-center justify-between text-sm">
          <span className="text-[#232323]">忘记密码了?</span>
          <button className="text-[#FF7F23] font-bold hover:underline">
            重置密码
          </button>
        </div>
        
        <div className="flex items-center justify-center space-x-4">
          <Link 
            to="/sign-up" 
            className="text-[#232323] text-sm hover:text-[#FF7F23] transition-colors"
          >
            或者注册
          </Link>
          <div className="flex space-x-3">
            <SocialAuthButton 
              provider="google" 
              onClick={() => handleSocialSignIn('oauth_google')}
            />
            <SocialAuthButton 
              provider="facebook" 
              onClick={() => handleSocialSignIn('oauth_facebook')}
            />
          </div>
        </div>
      </div>
    </AuthLayout>
  )
}