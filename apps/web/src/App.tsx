import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from '@clerk/clerk-react'
import { SignInPage } from './components/auth/SignInPage'
import { SignUpPage } from './components/auth/SignUpPage'
import { ProtectedRoute } from './components/auth/ProtectedRoute'
import { Dashboard } from './pages/Dashboard'

function App() {
  const { isLoaded, isSignedIn } = useAuth()

  if (!isLoaded) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#1B1F36]">
        <div className="w-12 h-12 border-4 border-[#FE9870] border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route 
          path="/sign-in" 
          element={isSignedIn ? <Navigate to="/dashboard" replace /> : <SignInPage />} 
        />
        <Route 
          path="/sign-up" 
          element={isSignedIn ? <Navigate to="/dashboard" replace /> : <SignUpPage />} 
        />
        
        {/* Protected routes */}
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } 
        />
        
        {/* Default redirect */}
        <Route 
          path="/" 
          element={<Navigate to={isSignedIn ? "/dashboard" : "/sign-in"} replace />} 
        />
        
        {/* Catch all route */}
        <Route 
          path="*" 
          element={<Navigate to={isSignedIn ? "/dashboard" : "/sign-in"} replace />} 
        />
      </Routes>
    </Router>
  )
}

export default App
