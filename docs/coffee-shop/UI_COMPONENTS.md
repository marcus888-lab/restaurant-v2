# Restaurant UI Components

## 🎨 Design System

```mermaid
graph TD
    A[Design System] --> B[Colors]
    A --> C[Typography]
    A --> D[Components]
    A --> E[Layout]
    
    B --> F[Primary Orange]
    B --> G[Secondary Yellow]
    B --> H[Neutral Grays]
    B --> I[Semantic Colors]
    
    C --> J[Poppins Headings]
    C --> K[Inter Body]
    
    D --> L[Buttons]
    D --> M[Cards]
    D --> N[Forms]
    D --> O[Navigation]
    
    E --> P[Grid System]
    E --> Q[Spacing]
    E --> R[Breakpoints]
```

## 🎯 Core Components

### Button Component
```tsx
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'outline' | 'ghost'
  size: 'sm' | 'md' | 'lg'
  children: React.ReactNode
}
```

### Card Component
```tsx
interface CardProps {
  variant: 'default' | 'elevated' | 'outlined'
  padding: 'sm' | 'md' | 'lg'
  children: React.ReactNode
}
```

## 🍽️ Restaurant-Specific Components

```mermaid
flowchart TD
    A[Restaurant Components] --> B[MenuItemCard]
    A --> C[CartItem]
    A --> D[OrderStatusBadge]
    A --> E[ReservationCard]
    A --> F[ReviewCard]
    
    B --> G[Image]
    B --> H[Title & Price]
    B --> I[Add to Cart Button]
    
    C --> J[Item Details]
    C --> K[Quantity Controls]
    C --> L[Remove Option]
    
    D --> M[Status Color]
    D --> N[Status Text]
    D --> O[Progress Indicator]
```

## Color Palette
- **Primary**: #f97316 (Orange)
- **Secondary**: #eab308 (Yellow)
- **Success**: #10b981 (Green)
- **Warning**: #f59e0b (Amber)
- **Error**: #ef4444 (Red)

## Typography
- **Headings**: Poppins (Bold)
- **Body**: Inter (Regular/Medium)
- **Scale**: 12px - 48px with 1.5 line height