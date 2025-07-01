import { useState } from 'react'
import { useSignUp } from '@clerk/clerk-react'
import { Link } from 'react-router-dom'
import { AuthLayout } from './AuthLayout'
import { Button } from '../ui/Button'
import { InputField } from '../ui/InputField'

export function SignUpPage() {
  const { signUp, setActive, isLoaded } = useSignUp()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [pendingVerification, setPendingVerification] = useState(false)
  const [code, setCode] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!isLoaded) return

    if (password !== confirmPassword) {
      setError('密码不匹配')
      return
    }

    setIsLoading(true)
    setError('')

    try {
      await signUp.create({
        emailAddress: email,
        password,
      })

      await signUp.prepareEmailAddressVerification({ strategy: 'email_code' })
      setPendingVerification(true)
    } catch (err) {
      console.error('Error:', err)
      setError('注册失败，请重试')
    } finally {
      setIsLoading(false)
    }
  }

  const handleVerifyEmail = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!isLoaded) return

    setIsLoading(true)
    setError('')

    try {
      const completeSignUp = await signUp.attemptEmailAddressVerification({
        code,
      })

      if (completeSignUp.status === 'complete') {
        await setActive({ session: completeSignUp.createdSessionId })
        // Redirect will happen automatically
      } else {
        setError('验证码无效')
      }
    } catch (err) {
      console.error('Error:', err)
      setError('验证失败，请重试')
    } finally {
      setIsLoading(false)
    }
  }

  if (pendingVerification) {
    return (
      <AuthLayout title="邮箱验证">
        <div className="space-y-6">
          <h2 className="text-[#232323] font-bold text-2xl font-montserrat">验证邮箱</h2>
          <p className="text-[#232323] text-sm">
            我们已向 {email} 发送了验证码
          </p>
          
          <form onSubmit={handleVerifyEmail} className="space-y-4">
            <InputField
              type="text"
              placeholder="请输入验证码"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              required
            />
            
            {error && (
              <div className="text-red-500 text-sm text-center">{error}</div>
            )}
            
            <Button 
              type="submit" 
              className="w-full"
              isLoading={isLoading}
              disabled={!code}
            >
              验证
            </Button>
          </form>
          
          <button 
            onClick={() => setPendingVerification(false)}
            className="w-full text-[#FF7F23] text-sm hover:underline"
          >
            返回注册
          </button>
        </div>
      </AuthLayout>
    )
  }

  return (
    <AuthLayout title="欢迎加入">
      <div className="space-y-6">
        <h2 className="text-[#232323] font-bold text-2xl font-montserrat">注册</h2>
        
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
            placeholder="请输入"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            showPasswordToggle
            required
          />
          
          <InputField
            type="password"
            placeholder="确认密码"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
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
            disabled={!email || !password || !confirmPassword}
          >
            创建账户
          </Button>
        </form>
        
        <p className="text-[#232323] text-xs text-center leading-6">
          通过点击"注册"按钮，您接受此应用程序的条款和隐私
        </p>
        
        <div className="text-center">
          <span className="text-[#232323] text-sm">已有账户? </span>
          <Link 
            to="/sign-in" 
            className="text-[#FF7F23] text-sm font-bold hover:underline"
          >
            立即登录
          </Link>
        </div>
      </div>
    </AuthLayout>
  )
}