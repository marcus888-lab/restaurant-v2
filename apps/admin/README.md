# Coffee Shop Admin Dashboard

Admin dashboard for managing the Coffee Shop business operations.

## 🚀 Features

- Dashboard with analytics overview
- Menu management (CRUD operations)
- Order processing and tracking
- Customer management
- Sales analytics and reports
- Inventory management
- Settings and configuration
- Real-time order updates

## 🛠️ Tech Stack

- React 18 with TypeScript
- Vite for fast development and builds
- Tailwind CSS for styling
- Clerk for admin authentication
- React Router for navigation
- Recharts for analytics visualization
- Desktop-optimized UI

## 📦 Setup

1. Install dependencies:
```bash
pnpm install
```

2. Copy environment variables:
```bash
cp .env.example .env.local
```

3. Update `.env.local` with your Clerk credentials:
```env
VITE_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key_here
VITE_API_URL=http://localhost:5001
```

4. Start development server:
```bash
pnpm dev
```

The admin dashboard will be available at http://localhost:5175

## 🔐 Authentication & Authorization

Uses Clerk for authentication with admin role verification:
- Admin-only access with role-based permissions
- Secure login with admin credentials
- Session management
- Protected admin routes

**Note:** Only users with `ADMIN` role in Clerk can access this dashboard.

## 🏗️ Building

Build for production:
```bash
pnpm build
```

Preview production build:
```bash
pnpm preview
```

## 📁 Structure

```
src/
├── components/       # Reusable UI components
│   ├── charts/      # Analytics chart components
│   ├── forms/       # Form components
│   └── tables/      # Data table components
├── pages/           # Admin route pages
│   ├── dashboard/   # Dashboard overview
│   ├── menu/        # Menu management
│   ├── orders/      # Order management
│   ├── customers/   # Customer management
│   └── settings/    # Settings pages
├── hooks/           # Custom React hooks
├── context/         # React Context providers
├── utils/           # Utility functions
├── types/           # TypeScript type definitions
├── App.tsx          # Main app component
└── main.tsx         # Entry point
```

## 📊 Analytics Features

- Sales overview charts
- Order trends analysis
- Popular products tracking
- Customer analytics
- Revenue reports
- Real-time metrics

## 🎨 Design System

Desktop-first design optimized for efficiency:
- Clean, professional interface
- Data-dense layouts
- Quick action buttons
- Responsive tables
- Interactive charts

## 🔗 API Integration

Connects to FastAPI backend admin endpoints:
- Menu CRUD operations
- Order management
- Customer data
- Analytics data
- Settings management

## 🌐 Deployment

Optimized for Vercel deployment:
- Configure build settings
- Set environment variables
- Deploy with domain `admin.coffeeshop.com`

## 🔒 Security

- Admin role verification
- Protected routes
- Secure API calls
- Session timeout
- Audit logging