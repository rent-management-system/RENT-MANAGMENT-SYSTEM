import { jsx as _jsx, jsxs as _jsxs } from 'react/jsx-runtime';
import React from 'react';
import { Link } from 'react-router-dom';
const Home = () => {
  return _jsxs('div', {
    className: 'text-center py-12',
    children: [
      _jsx('h1', {
        className: 'text-4xl font-bold text-gray-800 mb-4',
        children: 'Welcome to Rent Management System',
      }),
      _jsx('p', {
        className: 'text-gray-600 mb-8',
        children: 'Please log in or register to continue',
      }),
      _jsxs('div', {
        className: 'space-x-4',
        children: [
          _jsx(Link, {
            to: '/login',
            className:
              'bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors',
            children: 'Login',
          }),
          _jsx(Link, {
            to: '/register',
            className:
              'bg-white hover:bg-gray-100 text-gray-800 font-medium py-2 px-6 border border-gray-300 rounded-lg transition-colors',
            children: 'Register',
          }),
        ],
      }),
    ],
  });
};
export default Home;
