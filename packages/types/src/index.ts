// Basic shared types
export interface User {
  id: string;
  email: string;
  name?: string;
  role: 'CUSTOMER' | 'ADMIN' | 'STAFF';
}

export interface Coffee {
  id: string;
  name: string;
  description?: string;
  price: number;
  imageUrl?: string;
  available: boolean;
  categoryId: string;
}

export interface Category {
  id: string;
  name: string;
  description?: string;
  active: boolean;
}