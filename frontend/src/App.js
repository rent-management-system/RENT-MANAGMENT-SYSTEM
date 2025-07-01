import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Toaster } from './components/ui/sonner';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import Dashboard from './pages/Dashboard';
import Properties from './pages/Properties';
import Home from './pages/Home';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
const App = () => {
    return (_jsx(Router, { children: _jsx(AuthProvider, { children: _jsxs("div", { className: "flex flex-col min-h-screen bg-gray-50", children: [_jsx(Navbar, {}), _jsx("main", { className: "flex-grow container mx-auto px-4 py-8", children: _jsxs(Routes, { children: [_jsx(Route, { path: "/", element: _jsx(Home, {}) }), _jsx(Route, { path: "/login", element: _jsx(LoginPage, {}) }), _jsx(Route, { path: "/register", element: _jsx(RegisterPage, {}) }), _jsx(Route, { path: "/dashboard", element: _jsx(Dashboard, {}) }), _jsx(Route, { path: "/properties", element: _jsx(Properties, {}) })] }) }), _jsx(Footer, {}), _jsx(Toaster, {})] }) }) }));
};
export default App;
