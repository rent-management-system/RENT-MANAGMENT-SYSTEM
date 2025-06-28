/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1E3A8A', // indigo-900
        },
        secondary: {
          DEFAULT: '#4B5563', // gray-600
        },
        accent: {
          DEFAULT: '#2DD4BF', // teal-400
        },
        neutral: {
          DEFAULT: '#F9FAFB', // gray-50
        },
        error: {
          DEFAULT: '#EF4444', // red-500
        },
        success: {
          DEFAULT: '#10B981', // green-500
        },
      },
    },
  },
  plugins: [],
};