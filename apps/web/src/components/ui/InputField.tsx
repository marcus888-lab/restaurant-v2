import { useState } from 'react'
import type { InputHTMLAttributes, ReactNode } from 'react'

interface InputFieldProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  showPasswordToggle?: boolean
  leftIcon?: ReactNode
  rightIcon?: ReactNode
}

export function InputField({ 
  label, 
  error, 
  showPasswordToggle = false,
  leftIcon,
  rightIcon,
  type = 'text',
  className = '',
  ...props 
}: InputFieldProps) {
  const [showPassword, setShowPassword] = useState(false)
  const [isFocused, setIsFocused] = useState(false)
  
  const inputType = showPasswordToggle ? (showPassword ? 'text' : 'password') : type
  
  return (
    <div className="w-full">
      {label && (
        <label className="block text-[#232323] font-bold text-xl mb-2 font-montserrat">
          {label}
        </label>
      )}
      
      <div className={`relative ${error ? 'mb-1' : 'mb-4'}`}>
        <div className={`
          relative flex items-center w-full h-16 px-6 rounded-xl border
          ${isFocused ? 'border-[#FF7F23] bg-white' : 'border-[#F1F1F1] bg-white'}
          ${error ? 'border-red-500' : ''}
          transition-all duration-200
        `}>
          {leftIcon && (
            <div className="mr-3 text-[#CCCCCC]">
              {leftIcon}
            </div>
          )}
          
          <input
            type={inputType}
            className={`
              flex-1 bg-transparent outline-none text-base font-semibold font-montserrat
              placeholder:text-[#CCCCCC] text-[#333333]
              ${className}
            `}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            {...props}
          />
          
          {showPasswordToggle && (
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="ml-3 text-[#FF7F23] hover:text-[#fd8a5a] transition-colors"
            >
              <svg width="20" height="16" viewBox="0 0 20 16" fill="none">
                <path
                  d="M10 0C5.5 0 1.73 2.61 0 6.5C1.73 10.39 5.5 13 10 13C14.5 13 18.27 10.39 20 6.5C18.27 2.61 14.5 0 10 0Z"
                  fill="currentColor"
                />
                <circle cx="10" cy="6.5" r="2.5" fill="white" />
                {!showPassword && (
                  <line x1="2" y1="2" x2="18" y2="14" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                )}
              </svg>
            </button>
          )}
          
          {rightIcon && !showPasswordToggle && (
            <div className="ml-3 text-[#CCCCCC]">
              {rightIcon}
            </div>
          )}
        </div>
      </div>
      
      {error && (
        <p className="text-red-500 text-sm mb-3 px-1">{error}</p>
      )}
    </div>
  )
}