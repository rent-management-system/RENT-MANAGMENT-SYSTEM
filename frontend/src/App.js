import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Sonner as Toaster } from './components/ui/sonner.js';
import Login from './components/auth/Login.jsx';
import Register from './components/auth/Register';
import GoogleCallback from './components/auth/GoogleCallback';
import Dashboard from './pages/Dashboard';
import Properties from './pages/Properties';
const App = () => {
    return (_jsxs(Router, { children: [_jsxs(Routes, { children: [_jsx(Route, { path: "/login", element: _jsx(Login, {}) }), _jsx(Route, { path: "/register", element: _jsx(Register, {}) }), _jsx(Route, { path: "/google-callback", element: _jsx(GoogleCallback, {}) }), _jsx(Route, { path: "/dashboard", element: _jsx(Dashboard, {}) }), _jsx(Route, { path: "/properties", element: _jsx(Properties, {}) }), _jsx(Route, { path: "/", element: _jsx(Login, {}) })] }), _jsx(Toaster, {})] }));
};
export default App;
