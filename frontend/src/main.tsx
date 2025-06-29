// import { StrictMode } from 'react'
// import { createRoot } from 'react-dom/client'
// import './index.css';
// import App from './App.js'

// createRoot(document.getElementById('root')!).render(
//   <StrictMode>
//     <App />
//   </StrictMode>,
// )

// src/main.tsx
import React from 'react';
import { createRoot } from 'react-dom/client';
import './main.css';
import App from './App';

const container = document.getElementById('root');
const root = createRoot(container!);
root.render(<App />);