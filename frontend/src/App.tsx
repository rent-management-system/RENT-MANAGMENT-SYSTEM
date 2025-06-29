import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { Toaster } from '@/components/ui/sonner';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import GoogleCallback from './components/auth/GoogleCallback';
import Dashboard from './pages/Dashboard';
import Properties from './pages/Properties';
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

// Scroll to top on route change
const ScrollToTop = () => {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
};

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Test element to verify Tailwind is working */}
      <div className="test-tailwind fixed top-4 right-4 z-50">
        Tailwind is working! 🎉
      </div>
      <Router>
        <ScrollToTop />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={
              <div className="text-center py-12">
                <h1 className="text-4xl font-bold text-gray-800 mb-4">Welcome to Rent Management System</h1>
                <p className="text-gray-600 mb-8">Please log in or register to continue</p>
                <div className="space-x-4">
                  <a href="/login" className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors">
                    Login
                  </a>
                  <a href="/register" className="bg-white hover:bg-gray-100 text-gray-800 font-medium py-2 px-6 border border-gray-300 rounded-lg transition-colors">
                    Register
                  </a>
                </div>
              </div>
            } />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/google-callback" element={<GoogleCallback />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/properties" element={<Properties />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
          <Toaster />
        </main>
      </Router>
    </div>
  );
};

export default App;