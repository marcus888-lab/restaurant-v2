# Coffee Shop App - Project Overview

## 🏗️ System Architecture

```mermaid
graph TB
    subgraph "Landing Page (React + Vite)"
        A[Onboarding Page] --> B[Coffee Showcase]
        A --> C[Product Cards]
        A --> D[App Entry CTA]
    end
    
    subgraph "Coffee Shop App (React + Vite)"
        E[Coffee Menu] --> F[Coffee Details]
        F --> G[Shopping Cart]
        G --> H[Checkout]
        E --> I[User Profile]
        E --> J[Rewards Program]
    end
    
    subgraph "Admin Dashboard (React + Vite)"
        U[Dashboard] --> V[Menu Management]
        U --> W[Order Processing]
        U --> X[Analytics]
        U --> Y[Customer Management]
        U --> Z[Settings]
    end
    
    subgraph "Backend (FastAPI)"
        K[API Gateway] --> L[Order Service]
        K --> M[Menu Service]
        K --> N[User Service]
        K --> O[Rewards Service]
        K --> AA[Admin Service]
    end
    
    subgraph "Database"
        P[(PostgreSQL)]
    end
    
    subgraph "External Services"
        Q[Clerk Auth]
        R[Stripe Payment]
        S[SMS Notifications]
        T[Email Service]
    end
    
    A --> K
    E --> K
    U --> K
    L --> P
    M --> P
    N --> P
    O --> P
    AA --> P
    K --> Q
    H --> R
    K --> S
    K --> T
```

## ☕ Core Features

```mermaid
mindmap
  root((Coffee Shop))
    Customer Features
      Coffee Menu
      Product Details
      User Authentication
      Shopping Cart
      Order Management
      Rewards Program
    Admin Features
      Dashboard Analytics
      Menu Management
      Order Processing
      Customer Database
      Sales Reports
      System Settings
    UI/UX Features
      Chinese Language
      Mobile First
      Coffee Theme
      Custom Auth UI
      Admin Desktop UI
    Technical Features
      Protected Routes
      Role-Based Access
      API Integration
      Type Safety
      Fast Development
      Real-Time Updates
```

## 🔄 Order Flow

```mermaid
sequenceDiagram
    participant C as Customer
    participant W as Web App
    participant A as API
    participant D as Database
    participant CL as Clerk
    participant S as Stripe
    
    C->>W: Browse Coffee Menu
    W->>A: Get Coffee Items
    A->>D: Query Products
    D-->>A: Return Coffee List
    A-->>W: Coffee Data
    W-->>C: Display Menu
    
    C->>W: Sign In/Up
    W->>CL: Authenticate
    CL-->>W: Auth Token
    W-->>C: Logged In
    
    C->>W: Add to Cart
    C->>W: Checkout
    W->>S: Process Payment
    S-->>W: Payment Success
    W->>A: Create Order
    A->>D: Save Order
    A->>D: Update Rewards
    A-->>C: Order Confirmation
```

## 👨‍💼 Admin Flow

```mermaid
sequenceDiagram
    participant AD as Admin
    participant W as Admin Dashboard
    participant A as API
    participant D as Database
    participant CL as Clerk
    
    AD->>W: Login with Admin Credentials
    W->>CL: Authenticate
    CL-->>W: Admin Role Verified
    W-->>AD: Access Dashboard
    
    AD->>W: Update Menu Item
    W->>A: PUT /admin/menu/items
    A->>CL: Verify Admin Role
    CL-->>A: Authorized
    A->>D: Update Product
    D-->>A: Success
    A-->>W: Item Updated
    W-->>AD: Show Success
    
    AD->>W: View Analytics
    W->>A: GET /admin/analytics
    A->>D: Query Sales Data
    D-->>A: Analytics Data
    A-->>W: Formatted Reports
    W-->>AD: Display Charts
```

## 🗄️ Data Model

```mermaid
erDiagram
    User ||--o{ Order : places
    User ||--o| Rewards : has
    Order ||--o{ OrderItem : contains
    Coffee ||--o{ OrderItem : "ordered as"
    Category ||--o{ Coffee : contains
    User ||--o{ Review : writes
    Coffee ||--o{ Review : "reviewed in"
    
    User {
        string id PK
        string email
        string name
        string phone
        datetime createdAt
    }
    
    Coffee {
        string id PK
        string categoryId FK
        string name
        string description
        decimal price
        string imageUrl
        boolean available
    }
    
    Order {
        string id PK
        string userId FK
        decimal total
        string status
        datetime createdAt
    }
    
    Rewards {
        string id PK
        string userId FK
        integer points
        integer totalEarned
        datetime lastUpdated
    }
```

## 🎨 Design System

```mermaid
graph LR
    subgraph "Coffee Theme"
        A[Coffee Orange #FE9870]
        B[Coffee Cream #F4E6CD]
        C[Coffee Dark #1B2037]
        D[Coffee Gray #D1D2D7]
    end
    
    subgraph "Typography"
        E[Kumbh Sans - Body]
        F[Montserrat - Display]
    end
    
    subgraph "Components"
        G[Custom Auth UI]
        H[Coffee Cards]
        I[Mobile Nav]
        J[Rewards Progress]
    end
```

## 📱 Page Structure

```mermaid
flowchart TD
    A[Landing Page] --> B[Main App]
    A --> N[Admin App]
    
    B --> C[Public Pages]
    C --> D[Home]
    C --> E[Menu]
    C --> F[Coffee Details]
    C --> G[Sign In]
    C --> H[Sign Up]
    
    B --> I[Protected Pages]
    I --> J[Profile]
    I --> K[Orders]
    I --> L[Rewards]
    
    N --> O[Admin Login]
    O --> P[Admin Dashboard]
    P --> Q[Menu Management]
    P --> R[Order Processing]
    P --> S[Customer Management]
    P --> T[Analytics]
    P --> U[Settings]
    
    G --> M[Email Verification]
    H --> M
```

## 🚀 Deployment

```mermaid
flowchart LR
    subgraph "Development"
        A[Local Dev]
        B[pnpm Workspace]
    end
    
    subgraph "Production"
        C[Vercel Landing]
        D[Vercel Web App]
        H[Vercel Admin]
        E[Railway Backend]
        F[PostgreSQL DB]
        G[Clerk Auth]
    end
    
    A --> B
    B --> C
    B --> D
    B --> H
    B --> E
    E --> F
    D --> G
    H --> G
```

## Tech Stack

### Frontend
- **Landing Page**: React 18, Vite, Tailwind CSS
- **Web App**: React 18, Vite, Tailwind CSS, Clerk
- **Admin Dashboard**: React 18, Vite, Tailwind CSS, Clerk (Admin Role)
- **UI Components**: Custom auth UI, shadcn/ui base, Admin-specific components
- **State Management**: React hooks, Context API for admin state
- **Routing**: React Router v6 with role-based guards
- **Data Visualization**: Recharts for analytics

### Backend
- **API**: FastAPI (Python) with role-based endpoints
- **Database**: PostgreSQL with Prisma ORM
- **Authentication**: Clerk JWT verification with role checking
- **Admin Services**: Dedicated admin API routes
- **Real-Time**: WebSocket support for live updates
- **Hosting**: Railway/Render

### Key Features Implemented
- ✅ Beautiful onboarding page
- ✅ Custom authentication UI
- ✅ Coffee menu browsing
- ✅ Product details view
- ✅ User profiles
- ✅ Rewards program
- ✅ Protected routes
- ✅ Chinese language support
- 🚧 Admin dashboard
- 🚧 Menu management CRUD
- 🚧 Order processing system
- 🚧 Customer management
- 🚧 Sales analytics

### Upcoming Features
- 📋 Shopping cart
- 📋 Checkout flow
- 📋 Payment integration
- 📋 Order tracking
- 📋 Push notifications
- 📋 Real-time order updates
- 📋 Advanced reporting