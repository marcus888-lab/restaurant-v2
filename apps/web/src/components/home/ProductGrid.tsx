import React from 'react'
import type { Coffee } from '../../types/api'

interface ProductGridProps {
  products: Coffee[]
  onProductSelect: (product: Coffee) => void
  loading?: boolean
}

export function ProductGrid({ products, onProductSelect, loading = false }: ProductGridProps) {
  const displayProducts = products

  if (loading) {
    return (
      <div className="px-6 mt-6">
        <div className="grid grid-cols-2 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="bg-[#222845] rounded-lg h-[204px] animate-pulse">
              <div className="p-1">
                <div className="bg-[#3A3F5C] rounded h-[143px] mb-2"></div>
                <div className="px-3 pb-3">
                  <div className="h-4 bg-[#3A3F5C] rounded mb-1"></div>
                  <div className="h-3 bg-[#3A3F5C] rounded w-3/4"></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="px-6 mt-6">
      <div className="grid grid-cols-2 gap-4">
        {displayProducts.map((product) => (
          <ProductCard
            key={product.id}
            product={product}
            onClick={() => onProductSelect(product)}
          />
        ))}
      </div>
    </div>
  )
}

interface ProductCardProps {
  product: Coffee
  onClick: () => void
}

function ProductCard({ product, onClick }: ProductCardProps) {
  return (
    <button
      onClick={onClick}
      className="bg-[#222845] rounded-lg h-[204px] w-full text-left transform transition-transform hover:scale-105 active:scale-95"
    >
      <div className="p-1 h-full flex flex-col">
        {/* Product Image */}
        <div className="relative h-[143px] bg-[#9E9E9E] rounded mb-2 overflow-hidden">
          {product.imageUrl ? (
            <img
              src={`http://localhost:5001${product.imageUrl}`}
              alt={product.name}
              className="w-full h-full object-cover"
              onError={(e) => {
                // Fallback to gray background on error
                const target = e.target as HTMLImageElement
                target.style.display = 'none'
              }}
            />
          ) : (
            <div className="w-full h-full bg-[#9E9E9E] flex items-center justify-center">
              <span className="text-[#666] text-xs">图片</span>
            </div>
          )}
        </div>

        {/* Product Info */}
        <div className="px-3 pb-3 flex-1 flex flex-col justify-between">
          <div>
            <h3 className="text-[#F4E6CD] text-[15px] font-normal leading-[19px] mb-1 truncate">
              {product.name}
            </h3>
            <p className="text-[#D1D2D7] text-xs font-normal leading-[15px] truncate">
              {product.description || '精选咖啡'}
            </p>
          </div>

          {/* Price Badge */}
          <div className="mt-2 ml-auto">
            <div className="bg-[#1B2037] bg-opacity-90 rounded px-2.5 py-1 inline-block">
              <span className="text-[#F4E6CD] text-sm font-medium">
                ¥{product.price.toFixed(2)}
              </span>
            </div>
          </div>
        </div>
      </div>
    </button>
  )
}