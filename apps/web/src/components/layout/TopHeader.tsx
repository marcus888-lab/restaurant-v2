import React, { useState } from 'react'

export function TopHeader() {
  const [showLocationDropdown, setShowLocationDropdown] = useState(false)
  
  // Mock locations - in real app this would come from API
  const locations = [
    '美国纽约百老汇大街343号',
    '美国纽约第五大道125号',
    '美国纽约时代广场789号'
  ]
  
  const [selectedLocation, setSelectedLocation] = useState(locations[0])

  const handleLocationSelect = (location: string) => {
    setSelectedLocation(location)
    setShowLocationDropdown(false)
  }

  return (
    <div className="relative px-6 py-2.5 bg-[#1B1F36]">
      <div className="flex items-center justify-between">
        {/* Location Section */}
        <div className="flex-1">
          <div className="flex flex-col">
            <span className="text-[#D1D2D7] text-sm font-normal leading-[17px]">
              收货地址
            </span>
            <div className="flex items-center mt-1">
              <span className="text-[#F4E6CD] text-base font-medium leading-5 mr-2 truncate max-w-[200px]">
                {selectedLocation}
              </span>
              <button
                onClick={() => setShowLocationDropdown(!showLocationDropdown)}
                className="flex-shrink-0 w-3.5 h-3.5 flex items-center justify-center"
              >
                <ChevronDownIcon />
              </button>
            </div>
          </div>
        </div>

        {/* Profile Avatar */}
        <div className="w-[42px] h-[42px] bg-[#9E9E9E] rounded-full flex items-center justify-center ml-4">
          <div className="w-8 h-8 bg-[#9E9E9E] rounded-full"></div>
        </div>
      </div>

      {/* Location Dropdown */}
      {showLocationDropdown && (
        <>
          <div 
            className="fixed inset-0 z-40"
            onClick={() => setShowLocationDropdown(false)}
          />
          <div className="absolute top-full left-6 right-6 mt-1 bg-[#23283E] rounded-lg shadow-lg z-50 border border-[#444]">
            {locations.map((location, index) => (
              <button
                key={index}
                onClick={() => handleLocationSelect(location)}
                className={`w-full px-4 py-3 text-left text-[#F4E6CD] hover:bg-[#2A2F45] transition-colors ${
                  index === 0 ? 'rounded-t-lg' : ''
                } ${index === locations.length - 1 ? 'rounded-b-lg' : 'border-b border-[#444]'} ${
                  location === selectedLocation ? 'bg-[#FE9870] bg-opacity-20' : ''
                }`}
              >
                <span className="text-sm font-medium">{location}</span>
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  )
}

function ChevronDownIcon() {
  return (
    <svg width="11" height="5" viewBox="0 0 11 5" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path 
        d="M1.76 0.44L5.5 4.18L9.24 0.44" 
        stroke="#FE9870" 
        strokeWidth="1.5" 
        strokeLinecap="round" 
        strokeLinejoin="round"
      />
    </svg>
  )
}