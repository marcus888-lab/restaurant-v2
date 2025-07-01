import { CoffeeCard } from './CoffeeCard';
import { SlideIndicators } from './SlideIndicators';
import { CTAButtons } from './CTAButtons';

export function OnboardingSlide() {
  const handleStart = () => {
    // Navigate to web app
    window.location.href = 'http://localhost:5173';
  };

  const handleSkip = () => {
    // Navigate to web app
    window.location.href = 'http://localhost:5173';
  };

  return (
    <div className="w-full max-w-[375px] h-[812px] mx-auto bg-white relative overflow-hidden">
      {/* Full-screen Dark Background Overlay */}
      <div className="absolute inset-0 w-[375px] h-[812px] bg-[#1B1F36]"></div>

      {/* White Title Section Overlay */}
      <div className="absolute top-[52px] left-[41px] w-[293px] h-[140px] rounded-lg">
        <div className="pt-4 px-4">
          <h1 className="font-display font-medium text-[34px] leading-[42.16px] text-[#F4E6CD] text-center mb-[16px]">
            我们为您提供最好的咖啡
          </h1>
          <p className="font-body font-light text-[16px] leading-[19.84px] text-[#D1D2D7] text-center">
            您可以轻松选购来自全球各地的优质咖啡豆，品尝不同风味的手冲咖啡
          </p>
        </div>
      </div>

      {/* Coffee Background Image Section */}
      <div className="absolute top-[233px] left-0 w-[375px] h-[346px]">
        <div 
          className="absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{
            backgroundImage: 'url(/images/hero-coffee-bg.png)',
          }}
        />
        {/* Coffee Card */}
        <div className="absolute top-[33px] left-[150px] w-[205.3px] h-[80px]">
          <CoffeeCard
            name="卡布奇诺"
            description="简易坚果味"
            rating={4.7}
            image="/images/cappuccino.png"
          />
        </div>
      </div>

      {/* Slide Indicators */}
      <div className="absolute top-[611px] left-[150px] w-[64px] h-[4px]">
        <SlideIndicators currentSlide={2} totalSlides={4} />
      </div>

      {/* CTA Buttons */}
      <div className="absolute top-[707px] left-[77px] w-[224px] h-[89px]">
        <CTAButtons onStart={handleStart} onSkip={handleSkip} />
      </div>
    </div>
  );
}