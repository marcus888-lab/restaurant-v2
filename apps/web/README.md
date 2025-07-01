# Coffee Shop Web App

Customer-facing web application for the Coffee Shop.

## 🚀 Features

- Browse coffee menu by categories
- View detailed product information
- Add items to shopping cart
- User authentication with Clerk
- Order management and tracking
- Rewards program integration
- User profile management
- Responsive design for mobile and desktop

## 🛠️ Tech Stack

- React 18 with TypeScript
- Vite for fast development and builds
- Tailwind CSS for styling
- Clerk for authentication
- React Router for navigation
- Custom coffee theme

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

The web app will be available at http://localhost:5173

## 🔐 Authentication

Uses Clerk for authentication with:
- Email/password signup and login
- Social login options
- Custom Chinese UI support
- Protected routes for authenticated users
- Role-based access control

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
├── pages/           # Route pages
├── hooks/           # Custom React hooks
├── context/         # React Context providers
├── utils/           # Utility functions
├── types/           # TypeScript type definitions
├── assets/          # Images and static assets
├── App.tsx          # Main app component
└── main.tsx         # Entry point
```

## 🎨 Styling

- Coffee Orange (#FE9870) - Primary actions
- Coffee Cream (#F4E6CD) - Backgrounds
- Coffee Dark (#1B2037) - Text and headers
- Coffee Gray (#D1D2D7) - Borders and subtle elements

## 🔗 API Integration

Connects to FastAPI backend at `http://localhost:5001` for:
- User management
- Menu data
- Order processing
- Rewards tracking

## 🌐 Deployment

Optimized for Vercel deployment:
- Configure build settings
- Set environment variables
- Deploy with domain `app.coffeeshop.com`