/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#1E3A8A' }, // Blue
        secondary: { DEFAULT: '#4B5563' }, // Gray
        accent: { DEFAULT: '#2DD4BF' }, // Teal
        neutral: { DEFAULT: '#F9FAFB' }, // Off-white
        error: { DEFAULT: '#EF4444' }, // Red
        success: { DEFAULT: '#10B981' }, // Green
      },
    },
  },
  plugins: [],
};