// API Response Types
export interface StandardResponse<T> {
  success: boolean
  data: T
  message: string
}

// Coffee and Category Types
export interface Category {
  id: string
  name: string
  description?: string
  active: boolean
  sortOrder: number
  createdAt: string
  updatedAt: string
}

export interface Coffee {
  id: string
  name: string
  description?: string
  price: number
  categoryId: string
  available: boolean
  imageUrl?: string
  createdAt: string
  updatedAt: string
}

export interface CoffeeWithCategory extends Coffee {
  category: Category
}

// Order Types
export interface OrderItem {
  id: string
  coffeeId: string
  quantity: number
  price: number
  size: string
  notes?: string
  coffee: Coffee
}

export interface Order {
  id: string
  userId: string
  orderNumber: string
  subtotal: number
  tax: number
  total: number
  status: 'PENDING' | 'CONFIRMED' | 'PREPARING' | 'READY' | 'COMPLETED' | 'CANCELLED'
  type: 'PICKUP' | 'DELIVERY'
  orderItems: OrderItem[]
  createdAt: string
  updatedAt: string
}

// Review Types
export interface Review {
  id: string
  userId: string
  coffeeId: string
  rating: number
  comment?: string
  coffee: Coffee
  createdAt: string
  updatedAt: string
}

// Rewards Types
export interface Rewards {
  id: string
  userId: string
  currentPoints: number
  totalEarned: number
  totalRedeemed: number
  createdAt: string
  updatedAt: string
}

// Request Types
export interface OrderCreateRequest {
  type: 'PICKUP' | 'DELIVERY'
  items: {
    coffeeId: string
    quantity: number
    size: string
    notes?: string
  }[]
}

export interface ReviewCreateRequest {
  coffeeId: string
  rating: number
  comment?: string
}

export interface RewardsRedeemRequest {
  coffeeId: string
  size: string
}