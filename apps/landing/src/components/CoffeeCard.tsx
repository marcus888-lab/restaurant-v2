import React from 'react';

interface CoffeeCardProps {
  name: string;
  description: string;
  rating: number;
  image: string;
}

export function CoffeeCard({ name, description, rating, image }: CoffeeCardProps) {
  return (
    <div className="relative w-[205.3px] h-[80px]">
      {/* Background Rectangle - offset by 7px from top */}
      <div className="absolute top-[7px] left-0 w-[199px] h-[73px] bg-[#F4E6CD] rounded-2xl"></div>
      
      {/* Coffee Image */}
      <div className="absolute top-[13px] left-[7px] w-[61px] h-[61px] rounded-xl overflow-hidden bg-gray-200">
        <img 
          src={image} 
          alt={name}
          className="w-full h-full object-cover"
        />
      </div>
      
      {/* Coffee Name */}
      <h3 className="absolute top-[23px] left-[73px] w-[72px] h-[22px] font-medium text-[18px] leading-[22.32px] text-[#1B2037]">
        {name}
      </h3>
      
      {/* Coffee Description */}
      <p className="absolute top-[50px] left-[73px] w-[60px] h-[15px] font-normal text-[12px] leading-[14.88px] text-[#1B2037] opacity-80">
        {description}
      </p>
      
      {/* Rating Badge */}
      <div className="absolute top-0 left-[158px] w-[47.3px] h-[23px] bg-[#FE9870] rounded-lg">
        {/* Inner Group */}
        <div className="absolute top-[4px] left-[8px] w-[32.3px] h-[15px]">
          {/* Star Icon */}
          <svg 
            width="11.3" 
            height="10.81" 
            viewBox="0 0 11 11" 
            fill="none" 
            xmlns="http://www.w3.org/2000/svg"
            className="absolute top-[2px] left-0 text-[#F4E6CD]"
          >
            <path 
              d="M5.5 0L6.74221 3.9013H10.9389L7.59835 6.3472L8.84056 10.2485L5.5 7.8026L2.15944 10.2485L3.40165 6.3472L0.0610737 3.9013H4.25779L5.5 0Z" 
              fill="currentColor"
            />
          </svg>
          
          {/* Rating Text */}
          <span className="absolute top-0 left-[15.3px] w-[17px] h-[15px] font-medium text-[12px] leading-[14.88px] text-[#1B2037]">
            {rating}
          </span>
        </div>
      </div>
    </div>
  );
}