# ☕ Coffee Shop Application

A modern, full-stack coffee shop application built with React, FastAPI, and PostgreSQL. This monorepo contains a complete solution for managing a coffee shop business, including customer ordering, admin management, and analytics.

## 🚀 Features

### Customer Features
- **Browse Menu**: Explore coffee categories, view detailed product information with images
- **User Authentication**: Secure login/signup with Clerk (Chinese UI support)
- **Shopping Cart**: Add items, modify quantities, save for later
- **Order Management**: Place orders, track order status in real-time
- **Rewards Program**: Earn points, redeem rewards, track loyalty status
- **Profile Management**: Update personal information, view order history
- **Payment Integration**: Multiple payment methods support

### Admin Features
- **Menu Management**: Add/edit/remove products, manage categories
- **Order Dashboard**: View and manage incoming orders in real-time
- **Inventory Tracking**: Monitor stock levels, receive low-stock alerts
- **Analytics**: Sales reports, customer insights, popular products
- **User Management**: View customer profiles, manage rewards
- **Settings**: Store hours, pricing, promotions

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **Zustand** - State management
- **React Query** - Data fetching
- **Framer Motion** - Animations

### Backend
- **FastAPI** - Python web framework
- **PostgreSQL** - Database
- **Prisma** - ORM
- **Redis** - Caching
- **Pydantic** - Data validation
- **JWT** - Authentication

### Infrastructure
- **Vercel** - Frontend hosting
- **Railway/Render** - Backend hosting
- **Clerk** - Authentication service
- **Cloudinary** - Image storage
- **Stripe** - Payment processing

## 📁 Project Structure

```
coffee-shop/
├── apps/
│   ├── landing/          # Marketing landing page
│   ├── web/             # Customer web application
│   ├── admin/           # Admin dashboard
│   └── backend/         # FastAPI backend
├── packages/
│   ├── ui/              # Shared UI components
│   ├── utils/           # Shared utilities
│   └── types/           # Shared TypeScript types
├── docs/                # Documentation
├── scripts/             # Build and deployment scripts
└── docker/              # Docker configurations
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL 14+
- Redis (optional for caching)
- pnpm (recommended) or npm

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/coffee-shop.git
cd coffee-shop
```

2. Install dependencies:
```bash
# Install frontend dependencies
pnpm install

# Install backend dependencies
cd apps/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Copy example env files
cp apps/web/.env.example apps/web/.env.local
cp apps/admin/.env.example apps/admin/.env.local
cp apps/backend/.env.example apps/backend/.env

# Update with your credentials:
# - Clerk API keys
# - Database URL
# - Cloudinary credentials
# - Stripe API keys
```

4. Set up the database:
```bash
# Run database migrations
cd apps/backend
prisma migrate dev

# Seed initial data (optional)
python scripts/seed.py
```

### Running Development Servers

```bash
# Run all frontend apps (from root)
pnpm dev

# Or run individual apps:
pnpm dev:landing   # Landing page
pnpm dev:web       # Customer app
pnpm dev:admin     # Admin dashboard

# Run backend (from apps/backend)
cd apps/backend
uvicorn main:app --reload --port 8000
```

### Available Scripts

```bash
pnpm build        # Build all apps
pnpm lint         # Lint all code
pnpm test         # Run tests
pnpm format       # Format code
```

## 🧪 Testing

```bash
# Frontend tests
pnpm test

# Backend tests
cd apps/backend
pytest

# E2E tests
pnpm test:e2e
```

## 🚢 Deployment

### Frontend Deployment (Vercel)

1. Connect your GitHub repository to Vercel
2. Configure build settings for each app:
   - Root Directory: `apps/[app-name]`
   - Build Command: `pnpm build`
   - Output Directory: `dist`

### Backend Deployment (Railway/Render)

1. Create a new Python service
2. Set environment variables
3. Configure build command: `pip install -r requirements.txt`
4. Configure start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Database Deployment

1. Provision a PostgreSQL database
2. Run migrations: `prisma migrate deploy`
3. Configure connection string in backend

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Code Style

- Follow ESLint rules for TypeScript/JavaScript
- Use Black formatter for Python
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Coffee icon by [Freepik](https://www.freepik.com)
- UI components inspired by [shadcn/ui](https://ui.shadcn.com)
- Authentication powered by [Clerk](https://clerk.dev)

## 📞 Support

For support, email support@coffeeshop.com or open an issue in this repository.

---

Built with ❤️ and ☕ by the Coffee Shop Team