import { jsx as _jsx, Fragment as _Fragment, jsxs as _jsxs } from "react/jsx-runtime";
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
const Navbar = () => {
    const { user, logout } = useAuth();
    return (_jsx("nav", { className: "bg-white shadow-md", children: _jsx("div", { className: "container mx-auto px-4", children: _jsxs("div", { className: "flex justify-between items-center py-4", children: [_jsx(Link, { to: "/", className: "text-2xl font-bold text-gray-800", children: "Rent Management" }), _jsx("div", { className: "flex items-center space-x-4", children: user ? (_jsxs(_Fragment, { children: [_jsx(Link, { to: "/dashboard", className: "text-gray-600 hover:text-gray-800", children: "Dashboard" }), _jsx(Link, { to: "/properties", className: "text-gray-600 hover:text-gray-800", children: "Properties" }), _jsx("button", { onClick: logout, className: "bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors", children: "Logout" })] })) : (_jsxs(_Fragment, { children: [_jsx(Link, { to: "/login", className: "text-gray-600 hover:text-gray-800", children: "Login" }), _jsx(Link, { to: "/register", className: "bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors", children: "Register" })] })) })] }) }) }));
};
export default Navbar;
