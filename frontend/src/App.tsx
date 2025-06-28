import * as React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Sonner as Toaster } from './components/ui/sonner.js';
import { Login } from './components/auth/Login.js';
import Register from './components/auth/Register.js';
import GoogleCallback from './components/auth/GoogleCallback.js';
import Dashboard from './pages/Dashboard.js';
import Properties from './pages/Properties.js';

const App: React.FC = () => {
  return (
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
  );
};

export default App;