import { jsx as _jsx } from 'react/jsx-runtime';
import React from 'react';
import { createRoot } from 'react-dom/client';
import './main.css';
import App from './App';
const container = document.getElementById('root');
const root = createRoot(container);
root.render(_jsx(React.StrictMode, { children: _jsx(App, {}) }));
