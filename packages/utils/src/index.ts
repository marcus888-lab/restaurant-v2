// Basic utility functions
export const formatPrice = (price: number): string => {
  return `¥${price.toFixed(2)}`;
};

export const formatDate = (date: Date): string => {
  return date.toLocaleDateString('zh-CN');
};

export const generateOrderNumber = (): string => {
  return `CF${Date.now().toString().slice(-8)}`;
};