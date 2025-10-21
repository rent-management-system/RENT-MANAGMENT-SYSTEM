import { jsx as _jsx } from 'react/jsx-runtime';
import React from 'react';
const Footer = () => {
  return _jsx('footer', {
    className: 'bg-white shadow-md mt-auto',
    children: _jsx('div', {
      className: 'container mx-auto px-4 py-4',
      children: _jsx('p', {
        className: 'text-center text-gray-600',
        children: '\u00A9 2025 Rent Management System. All rights reserved.',
      }),
    }),
  });
};
export default Footer;
