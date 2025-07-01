
interface CTAButtonsProps {
  onStart: () => void;
  onSkip: () => void;
}

export function CTAButtons({ onStart, onSkip }: CTAButtonsProps) {
  return (
    <div className="w-[224px] h-[89px] relative">
      {/* Skip Button - transparent background */}
      <div className="absolute top-[46px] left-0 w-[224px] h-[43px] bg-[#FE9870] opacity-0 rounded-lg"></div>
      <button
        onClick={onSkip}
        className="absolute top-[58px] left-[96.76px] w-[30px] h-[19px] text-[#FE9870] font-medium text-[15px] leading-[18.6px] hover:underline transition-all"
      >
        跳过
      </button>
      
      {/* Start Button */}
      <button
        onClick={onStart}
        className="absolute top-0 left-0 w-[224px] h-[43px] bg-[#FE9870] rounded-lg font-normal text-[15px] leading-[18.6px] text-[#1B2037] hover:bg-[#FE9870]/90 transition-all"
      >
        让我们开始
      </button>
    </div>
  );
}