import type { ButtonHTMLAttributes, ReactNode } from 'react'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'social'
  size?: 'small' | 'medium' | 'large'
  isLoading?: boolean
  children: ReactNode
}

export function Button({ 
  variant = 'primary', 
  size = 'medium', 
  isLoading = false, 
  children, 
  className = '',
  disabled,
  ...props 
}: ButtonProps) {
  const baseStyles = 'rounded-xl font-bold transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed'
  
  const variants = {
    primary: 'bg-[#FE9870] text-[#333333] hover:bg-[#fd8a5a] shadow-[0px_13px_26px_0px_rgba(0,87,218,0.08)]',
    secondary: 'bg-white text-[#333333] border border-[#F1F1F1] hover:bg-gray-50',
    social: 'bg-white border border-[#F1F1F1] hover:bg-gray-50 flex items-center justify-center'
  }
  
  const sizes = {
    small: 'px-4 py-2 text-sm h-10',
    medium: 'px-6 py-3 text-base h-11',
    large: 'px-8 py-3 text-lg h-12'
  }
  
  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <div className="flex items-center justify-center">
          <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin mr-2" />
          Loading...
        </div>
      ) : (
        children
      )}
    </button>
  )
}