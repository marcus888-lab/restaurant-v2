import { useState, useEffect } from 'react'

interface BannerSlide {
  id: string
  title: string
  subtitle?: string
  buttonText: string
  backgroundColor: string
  textColor: string
  backgroundImage?: string
}

export function PromoBanner() {
  const [currentSlide, setCurrentSlide] = useState(0)

  const slides: BannerSlide[] = [
    {
      id: '1',
      title: '午夜\n推广',
      buttonText: '得到现在',
      backgroundColor: 'bg-gradient-to-r from-[#5B1B03] to-[#100909]',
      textColor: 'text-[#F4E6CD]',
      backgroundImage: 'bg-[url("http://localhost:5001/static/images/banner-promo.jpg")]'
    },
    {
      id: '2', 
      title: '早晨\n优惠',
      buttonText: '立即获取',
      backgroundColor: 'bg-gradient-to-r from-[#2D4A22] to-[#1A2F15]',
      textColor: 'text-[#F4E6CD]'
    },
    {
      id: '3',
      title: '下午\n特价',
      buttonText: '查看详情',
      backgroundColor: 'bg-gradient-to-r from-[#4A2D22] to-[#2F1A15]',
      textColor: 'text-[#F4E6CD]'
    }
  ]

  // Auto-advance slides
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length)
    }, 5000)
    
    return () => clearInterval(interval)
  }, [slides.length])

  const handleSlideChange = (index: number) => {
    setCurrentSlide(index)
  }

  const handleCtaClick = () => {
    // Handle CTA button click - navigate to offers page or specific promotion
    console.log('CTA clicked for slide:', slides[currentSlide].title)
  }

  return (
    <div className="px-6 mt-8">
      <div className="relative w-full h-[158px] rounded-lg overflow-hidden">
        {/* Slide Content */}
        <div className={`relative w-full h-full ${slides[currentSlide].backgroundColor} ${slides[currentSlide].backgroundImage || ''} bg-cover bg-center`}>
          {/* Overlay */}
          <div className="absolute inset-0 bg-gradient-to-r from-[#5B1B03] via-[#5B1B03]/70 to-transparent opacity-60"></div>
          
          {/* Content */}
          <div className="relative z-10 p-6 h-full flex flex-col justify-between">
            <div>
              <h2 className={`text-2xl font-bold leading-[30px] ${slides[currentSlide].textColor} whitespace-pre-line`}>
                {slides[currentSlide].title}
              </h2>
            </div>
            
            <button
              onClick={handleCtaClick}
              className="self-start bg-[#FE9870] text-[#1B2037] px-3 py-1.5 rounded text-xs font-medium hover:bg-[#FE9870]/90 transition-colors"
            >
              {slides[currentSlide].buttonText}
            </button>
          </div>
        </div>

        {/* Slide Indicators */}
        <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
          {slides.map((_, index) => (
            <button
              key={index}
              onClick={() => handleSlideChange(index)}
              className={`w-1 h-1 rounded-full transition-all duration-300 ${
                index === currentSlide 
                  ? 'bg-[#FE9870] w-10' 
                  : 'bg-[#D1D2D7] opacity-70'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  )
}