import React from 'react';

interface SlideIndicatorsProps {
  currentSlide: number;
  totalSlides: number;
}

export function SlideIndicators({ currentSlide, totalSlides }: SlideIndicatorsProps) {
  return (
    <div className="flex items-center justify-center gap-2">
      {Array.from({ length: totalSlides }).map((_, index) => (
        <div
          key={index}
          className={`rounded-full transition-all duration-300 ${
            index === currentSlide
              ? 'w-10 h-1 bg-coffee-orange'
              : 'w-1 h-1 bg-coffee-gray opacity-70'
          }`}
        />
      ))}
    </div>
  );
}