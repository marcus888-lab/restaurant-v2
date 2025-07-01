import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@clerk/clerk-react'
import { MainLayout } from '../components/layout/MainLayout'
import { PromoBanner } from '../components/home/PromoBanner'
import { CategoryFilter } from '../components/home/CategoryFilter'
import { ProductGrid } from '../components/home/ProductGrid'
import { apiClient } from '../lib/api'
import type { Coffee } from '../types/api'

export function HomePage() {
  const navigate = useNavigate()
  const { getToken } = useAuth()
  const [products, setProducts] = useState<Coffee[]>([])
  const [categories, setCategories] = useState<Array<{
    id: string
    name: string
    active: boolean
  }>>([])
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [loading, setLoading] = useState(true)

  // Set up authentication token
  useEffect(() => {
    apiClient.setGetToken(getToken)
  }, [getToken])

  // Load initial data
  useEffect(() => {
    loadData()
  }, [])

  // Load products when category changes (skip initial load)
  useEffect(() => {
    if (!loading) {
      loadProducts(selectedCategory === 'all' ? undefined : selectedCategory)
    }
  }, [selectedCategory, loading])

  const loadData = async () => {
    try {
      setLoading(true)
      
      // Try to load from API
      const [categoriesResponse, productsResponse] = await Promise.all([
        apiClient.getCategories().catch(err => {
          console.warn('Categories API failed:', err)
          return null
        }),
        apiClient.getMenuItems().catch(err => {
          console.warn('Products API failed:', err)
          return null
        })
      ])

      // Handle categories
      if (categoriesResponse?.success) {
        // Filter active categories and sort
        const backendCategories = categoriesResponse.data
          .filter(cat => cat.active)
          .sort((a, b) => a.sortOrder - b.sortOrder)
          .map(cat => ({
            id: cat.id,
            name: cat.name,
            active: cat.active
          }))
        
        // Add "所有" (All) as the first option
        const allCategories = [
          { id: 'all', name: '所有', active: true },
          ...backendCategories
        ]
        setCategories(allCategories)
      } else {
        setCategories([])
      }

      // Handle products  
      if (productsResponse?.success) {
        setProducts(productsResponse.data.filter(product => product.available))
      } else {
        setProducts([])
      }
    } catch (err) {
      console.error('Unexpected error loading data:', err)
      setCategories([])
      setProducts([])
    } finally {
      setLoading(false)
    }
  }

  const loadProducts = async (categoryId?: string) => {
    try {
      console.log('Loading products for category:', categoryId || 'all')
      const response = await apiClient.getMenuItems(categoryId)
      if (response?.success) {
        console.log('Loaded products:', response.data.length)
        setProducts(response.data.filter(product => product.available))
      }
    } catch (err) {
      console.warn('Failed to load products for category:', categoryId, err)
      // Don't show error for category filter, just keep existing products
    }
  }

  const handleCategorySelect = (categoryId: string) => {
    setSelectedCategory(categoryId)
  }

  const handleProductSelect = (product: Coffee) => {
    // Navigate to product detail page
    navigate(`/product/${product.id}`)
  }

  // Remove the error state since we're using fallback data
  // if (error) {
  //   return (
  //     <MainLayout>
  //       <div className="flex-1 flex items-center justify-center p-6">
  //         <div className="text-center">
  //           <p className="text-[#F4E6CD] mb-4">{error}</p>
  //           <button
  //             onClick={loadData}
  //             className="bg-[#FE9870] text-[#1B2037] px-6 py-2 rounded-lg font-medium hover:bg-[#FE9870]/90 transition-colors"
  //           >
  //             重试
  //           </button>
  //         </div>
  //       </div>
  //     </MainLayout>
  //   )
  // }

  return (
    <MainLayout>
      <div className="flex flex-col">
        {/* Promotional Banner - scrolls with content */}
        <PromoBanner />
        
        {/* Fixed Category Filter */}
        <div className="sticky top-0 bg-[#1B1F36] z-10 shadow-sm">
          <CategoryFilter
            categories={categories}
            selectedCategory={selectedCategory}
            onCategorySelect={handleCategorySelect}
          />
        </div>
        
        {/* Product Grid */}
        <ProductGrid
          products={products}
          onProductSelect={handleProductSelect}
          loading={loading}
        />
      </div>
    </MainLayout>
  )
}