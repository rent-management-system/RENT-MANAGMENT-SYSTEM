import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Toaster } from '@/components/ui/sonner';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import GoogleCallback from './components/auth/GoogleCallback';
import Dashboard from './pages/Dashboard';
import Properties from './pages/Properties';

const App: React.FC = () => {
  return (
    <div>
      <div className="bg-red-500 text-white p-4">Tailwind is working!</div>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/google-callback" element={<GoogleCallback />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/properties" element={<Properties />} />
          <Route path="/" element={<Login />} />
        </Routes>
        <Toaster />
      </Router>
    </div>
  );
};

export default App;