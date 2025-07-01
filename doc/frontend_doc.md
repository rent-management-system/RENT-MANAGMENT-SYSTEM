# Frontend Documentation: A Comprehensive Guide

## 1. Introduction to the Frontend

Welcome to the frontend documentation for the Rent Management System! This guide is designed to help anyone, from beginners to experienced developers, understand how our user interface is built, how it works, and how it communicates with the backend API.

The frontend is what you see and interact with in your web browser. It's a **Single-Page Application (SPA)**, meaning that once you load it, most of the content changes happen dynamically without reloading the entire page. This makes the application feel fast and responsive.

**Our Frontend Technology Stack:**

*   **React:** A popular JavaScript library for building user interfaces. It allows us to create reusable UI components.
*   **TypeScript:** A superset of JavaScript that adds static typing. This helps us catch errors early, makes the code more robust, and improves developer experience with better autocompletion and refactoring tools.
*   **Vite:** A next-generation frontend tooling that provides an extremely fast development experience. It's used for building and serving our React application.
*   **Tailwind CSS:** A utility-first CSS framework. Instead of writing custom CSS for every element, we use pre-defined utility classes (like `flex`, `pt-4`, `text-center`) directly in our HTML/JSX to style our components. This speeds up development and ensures design consistency.
*   **Axios:** A popular JavaScript library used for making HTTP requests to the backend API.
*   **React Router:** A library for handling navigation within our single-page application, allowing us to define different "pages" or "views" based on the URL.
*   **React Context API:** A built-in React feature used for managing global application state, such as user authentication status, making it easily accessible to many components without passing props manually through every level of the component tree.

---

## 2. Getting Started: Setting Up the Frontend

To run the frontend application on your local machine, follow these simple steps:

1.  **Open your terminal or command prompt.**
2.  **Navigate to the frontend directory:**
    ```bash
    cd /home/dagi/Documents/Rent-managment-system/frontend
    ```
3.  **Install the necessary dependencies:**
    This command reads the `package.json` file and downloads all the required libraries and tools.
    ```bash
    npm install
    ```
4.  **Start the development server:**
    This command compiles the React application and serves it locally. It also watches for changes in your code and automatically reloads the browser.
    ```bash
    npm run dev
    ```
    You will typically see a message indicating that the server is running, usually at `http://localhost:5173`. Open this URL in your web browser to see the application.

---

## 3. Detailed Frontend Folder Structure and File Explanations

Understanding the project's structure is key to navigating and contributing to the codebase. Here's a breakdown of the `frontend` directory:

```
frontend/
├── .gitignore                 # Specifies intentionally untracked files to ignore by Git.
├── components.json            # Configuration for UI components (likely related to Shadcn UI or similar).
├── eslint.config.js           # ESLint configuration for code linting (identifying and fixing code quality issues).
├── index.html                 # The main HTML file that serves as the entry point for the web application.
├── package-lock.json          # Records the exact versions of dependencies installed.
├── package.json               # Defines project metadata and lists all dependencies and scripts.
├── postcss.config.js          # Configuration for PostCSS, used by Tailwind CSS for processing CSS.
├── README.md                  # General information about the frontend project.
├── tailwind.config.js         # Tailwind CSS configuration file.
├── tsconfig.app.json          # TypeScript configuration specific to the application code.
├── tsconfig.json              # Base TypeScript configuration.
├── tsconfig.node.json         # TypeScript configuration for Node.js environment (e.g., Vite config files).
├── tsconfig.tsbuildinfo       # TypeScript build information file (for faster incremental builds).
├── vite.config.d.ts           # TypeScript declaration file for Vite configuration.
├── vite.config.js             # JavaScript version of Vite configuration.
├── vite.config.ts             # TypeScript version of Vite configuration.
├── node_modules/              # Contains all installed Node.js packages (dependencies).
├── public/                    # Static assets served directly by the web server.
│   ├── index.html             # (Duplicate, likely a leftover or specific setup for public assets)
│   └── manifest.json          # Web App Manifest for Progressive Web App (PWA) features.
└── src/                       # Source code for the React application.
    ├── App.css                # Global CSS styles for the main App component.
    ├── App.d.ts               # TypeScript declaration file for App.js/App.tsx.
    ├── App.js                 # JavaScript version of the main App component.
    ├── App.tsx                # TypeScript JSX version of the main App component.
    ├── index.css              # Global CSS styles for the entire application.
    ├── index.d.ts             # TypeScript declaration file for index.js/index.tsx.
    ├── index.js               # JavaScript version of the application entry point.
    ├── index.tsx              # TypeScript JSX version of the application entry point.
    ├── main.css               # Main CSS file, likely imported into main.tsx.
    ├── main.d.ts              # TypeScript declaration file for main.js/main.tsx.
    ├── main.js                # JavaScript version of the application entry point.
    ├── main.tsx               # TypeScript JSX entry point for the React application.
    ├── tailwind.config.js     # (Duplicate, likely a leftover or specific setup for src)
    ├── utils.d.ts             # TypeScript declaration file for utils.js/utils.ts.
    ├── utils.js               # JavaScript version of utility functions.
    ├── utils.ts               # TypeScript version of utility functions.
    ├── vite-env.d.ts          # TypeScript declaration for Vite environment variables.
    ├── assets/                # Contains static assets like images.
    │   ├── react.svg          # React logo SVG.
    │   ├── images/            # Directory for images.
    │   └── styles/            # Directory for additional styles.
    ├── components/            # Reusable UI components.
    │   ├── auth/              # Authentication-related components.
    │   │   ├── GoogleCallback.d.ts  # TS declaration for GoogleCallback.
    │   │   ├── GoogleCallback.js    # JS version of GoogleCallback.
    │   │   ├── GoogleCallback.tsx   # TSX component for Google OAuth callback.
    │   │   ├── Login.d.ts           # TS declaration for Login.
    │   │   ├── Login.js             # JS version of Login.
    │   │   ├── Login.tsx            # TSX component for user login form.
    │   │   ├── Register.d.ts        # TS declaration for Register.
    │   │   ├── Register.js          # JS version of Register.
    │   │   └── Register.tsx         # TSX component for user registration form.
    │   ├── common/            # General-purpose, reusable UI elements.
    │   │   ├── Button.d.ts          # TS declaration for Button.
    │   │   ├── Button.js            # JS version of Button.
    │   │   ├── Button.tsx           # TSX component for a generic button.
    │   │   ├── ErrorMessage.d.ts    # TS declaration for ErrorMessage.
    │   │   ├── ErrorMessage.js      # JS version of ErrorMessage.
    │   │   └── ErrorMessage.tsx     # TSX component for displaying error messages.
    │   │   ├── Input.d.ts           # TS declaration for Input.
    │   │   ├── Input.js             # JS version of Input.
    │   │   └── Input.tsx            # TSX component for a generic input field.
    │   ├── layout/            # Components defining the overall page structure.
    │   │   ├── Footer.d.ts          # TS declaration for Footer.
    │   │   ├── Footer.js            # JS version of Footer.
    │   │   ├── Footer.tsx           # TSX component for the application footer.
    │   │   ├── Navbar.d.ts          # TS declaration for Navbar.
    │   │   ├── Navbar.js            # JS version of Navbar.
    │   │   └── Navbar.tsx           # TSX component for the application navigation bar.
    │   └── ui/                # UI components, likely from a UI library like Shadcn UI.
    │       ├── button.d.ts          # TS declaration for UI button.
    │       ├── button.js            # JS version of UI button.
    │       ├── button.tsx           # TSX component for UI button.
    │       ├── card.d.ts            # TS declaration for UI card.
    │       ├── card.js              # JS version of UI card.
    │       ├── card.tsx             # TSX component for UI card.
    │       ├── input.d.ts           # TS declaration for UI input.
    │       ├── input.js             # JS version of UI input.
    │       ├── input.tsx            # TSX component for UI input.
    │       ├── label.d.ts           # TS declaration for UI label.
    │       ├── label.js             # JS version of UI label.
    │       ├── label.tsx            # TSX component for UI label.
    │       ├── select.d.ts          # TS declaration for UI select.
    │       ├── select.tsx           # TSX component for UI select.
    │       ├── sonner.d.ts          # TS declaration for Sonner (toast notifications).
    │       ├── sonner.js            # JS version of Sonner.
    │       └── sonner.tsx           # TSX component for Sonner toast notifications.
    ├── context/               # React Context API providers for global state.
    │   ├── AuthContext.d.ts         # TS declaration for AuthContext.
    │   ├── AuthContext.js           # JS version of AuthContext.
    │   └── AuthContext.tsx          # TSX component providing authentication state and functions.
    ├── hooks/                 # Custom React hooks for reusable logic.
    │   ├── use-toast.d.ts           # TS declaration for use-toast hook.
    │   ├── use-toast.js             # JS version of use-toast hook.
    │   ├── use-toast.ts             # TS hook for displaying toast notifications.
    │   ├── useApi.d.ts              # TS declaration for useApi hook.
    │   ├── useApi.js                # JS version of useApi hook.
    │   ├── useApi.ts                # TS hook for making authenticated API requests.
    │   ├── useAuth.d.ts             # TS declaration for useAuth hook.
    │   ├── useAuth.js               # JS version of useAuth hook.
    │   └── useAuth.ts               # TS hook for accessing authentication context.
    ├── lib/                   # Utility functions and helpers.
    │   ├── utils.d.ts               # TS declaration for utils.
    │   ├── utils.js                 # JS version of utility functions.
    │   └── utils.ts                 # TS utility functions (e.g., for Tailwind CSS class merging).
    ├── pages/                 # Top-level components representing different views/pages.
    │   ├── Dashboard.d.ts           # TS declaration for Dashboard page.
    │   ├── Dashboard.js             # JS version of Dashboard page.
    │   ├── Dashboard.tsx            # TSX component for the user dashboard.
    │   ├── Home.d.ts                # TS declaration for Home page.
    │   ├── Home.js                  # JS version of Home page.
    │   ├── Home.tsx                 # TSX component for the home page.
    │   ├── LoginPage.d.ts           # TS declaration for Login page.
    │   ├── LoginPage.js             # JS version of Login page.
    │   ├── LoginPage.tsx            # TSX component for the login page.
    │   ├── Properties.d.ts          # TS declaration for Properties page.
    │   ├── Properties.js            # JS version of Properties page.
    │   ├── Properties.tsx           # TSX component for the properties listing page.
    │   ├── RegisterPage.d.ts        # TS declaration for Register page.
    │   ├── RegisterPage.js          # JS version of Register page.
    │   └── RegisterPage.tsx         # TSX component for the registration page.
    ├── services/              # Modules for interacting with the backend API.
    │   ├── api.d.ts                 # TS declaration for api service.
    │   ├── api.js                   # JS version of api service.
    │   ├── api.ts                   # TS module for configuring Axios and making API requests.
    │   ├── authService.d.ts         # TS declaration for authService.
    │   ├── authService.js           # JS version of authService.
    │   └── authService.ts           # TS module for authentication-related API calls.
    └── types/                 # TypeScript type definitions for data structures.
        ├── auth.d.ts                # TS declaration for authentication-related types.
        ├── auth.js                  # JS version of auth types.
        ├── auth.ts                  # TS definitions for user, login, and registration data.
        ├── property.d.ts            # TS declaration for property-related types.
        ├── property.js              # JS version of property types.
        └── property.ts              # TS definitions for property data.
```

**Note on `.js`, `.d.ts`, and `.tsx` files:** You'll notice many files have `.js`, `.d.ts`, and `.tsx` (or `.ts`) extensions. This is common in TypeScript projects:
*   `.tsx` (or `.ts`): This is the actual source code written in TypeScript (and JSX for `.tsx`).
*   `.js`: These are the compiled JavaScript files generated from the TypeScript code. When you run `npm run dev` or `npm run build`, TypeScript converts your `.ts`/`.tsx` files into plain `.js` files that browsers can understand.
*   `.d.ts`: These are TypeScript "declaration files." They describe the types of variables, functions, and classes in a JavaScript file. They are crucial for TypeScript to understand the structure of your code and provide features like autocompletion and type checking, even for JavaScript libraries.

---

## 4. Core Frontend Concepts for Beginners

Before diving into the code, let's clarify some fundamental concepts:

### What is React?
React is like a powerful toolkit for building interactive user interfaces. Instead of building an entire webpage as one big piece, React lets you break it down into smaller, self-contained parts called **components**. Think of components like LEGO bricks:
*   **Reusable:** You can use the same button component in many places.
*   **Modular:** Each component focuses on a specific part of the UI (e.g., a login form, a navigation bar).
*   **Declarative:** You describe *what* you want the UI to look like, and React figures out *how* to make it happen efficiently.

### What is TypeScript?
Imagine JavaScript with a built-in spell checker and grammar guide. That's TypeScript!
*   **Static Typing:** You can define the "type" of data (e.g., a variable `name` must be a `string`, `age` must be a `number`).
*   **Early Error Detection:** TypeScript catches common mistakes (like trying to add a number to a string) *before* you even run your code, saving you debugging time.
*   **Better Autocompletion:** Your code editor can provide smarter suggestions because it understands the data types.

### What is Vite?
Vite is a build tool that makes developing web applications super fast.
*   **Instant Server Start:** Unlike older tools that compile your entire project before starting, Vite starts almost instantly.
*   **Hot Module Replacement (HMR):** When you save a change in your code, Vite updates only that specific part of the application in the browser, without a full page reload. This is incredibly efficient for development.

### What is Tailwind CSS?
Tailwind CSS is a different way to style your web pages. Instead of writing CSS rules like this:
```css
.my-button {
  background-color: blue;
  padding: 16px;
  text-align: center;
}
```
You apply utility classes directly in your HTML/JSX:
```html
<button class="bg-blue-500 p-4 text-center">Click me</button>
```
This approach:
*   **Speeds up development:** You don't switch between HTML and CSS files as much.
*   **Ensures consistency:** You use a predefined set of styles, making your UI look uniform.
*   **Is highly customizable:** You can configure Tailwind to match your project's design system.

---

## 5. Deep Dive into `src/` Directory

The `src/` directory is where all the magic happens. It contains the source code for our React application.

### `src/main.tsx` (Application Entry Point)

This is the very first file that runs when your frontend application starts.
```typescript jsx
// src/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { Toaster } from './components/ui/sonner';
import App from './App';
import './index.css'; // Global styles

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
        <Toaster />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>,
);
```
*   **`import React from 'react'`**: Imports the React library, essential for building components.
*   **`import ReactDOM from 'react-dom/client'`**: Imports `ReactDOM`, which is responsible for rendering React components into the web browser's DOM (Document Object Model).
*   **`ReactDOM.createRoot(document.getElementById('root')!).render(...)`**: This line finds an HTML element with the ID `root` (which is in `public/index.html`) and tells React to render our entire application (`<App />`) inside it.
*   **`<React.StrictMode>`**: A React tool that helps identify potential problems in an application during development. It doesn't render any visible UI.
*   **`<BrowserRouter>`**: From `react-router-dom`, this component enables client-side routing. It keeps your UI in sync with the URL.
*   **`<AuthProvider>`**: This is our custom React Context Provider (explained later). It wraps the entire `App` to make authentication-related data (like user info and login/logout functions) available to *any* component within the application.
*   **`<App />`**: This is the main application component, where our routes and main layout are defined.
*   **`<Toaster />`**: A component for displaying "toast" notifications (small, temporary pop-up messages) to the user.

### `src/App.tsx` (Main Application Component & Routing)

This file defines the main structure of your application and sets up the different routes (pages).

```typescript jsx
// src/App.tsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/Home';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import Dashboard from './pages/Dashboard';
import Properties from './pages/Properties';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import { useAuth } from './hooks/useAuth'; // To check authentication status
import ProtectedRoute from './components/common/ProtectedRoute'; // For protecting routes

const App: React.FC = () => {
  const { user, isLoading } = useAuth(); // Get user and loading state from AuthContext

  if (isLoading) {
    // Optionally, render a loading spinner or splash screen here
    return <div>Loading application...</div>;
  }

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar /> {/* Always show the navigation bar */}
      <main className="flex-grow">
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected Routes */}
          <Route element={<ProtectedRoute isAllowed={!!user} />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/properties" element={<Properties />} />
            {/* Add more protected routes here */}
          </Route>

          {/* Catch-all route for 404 Not Found */}
          <Route path="*" element={<div>404 Not Found</div>} />
        </Routes>
      </main>
      <Footer /> {/* Always show the footer */}
    </div>
  );
};

export default App;
```
*   **`Routes` and `Route`**: These components from `react-router-dom` define which React component should be rendered for a specific URL path.
*   **Public Routes**: Pages like `/`, `/login`, and `/register` are accessible to everyone.
*   **Protected Routes**: Pages like `/dashboard` and `/properties` are wrapped within a `<ProtectedRoute>`. This custom component (explained below) checks if a user is logged in (`isAllowed={!!user}`) before rendering the child routes. If not, it redirects them to the login page.
*   **`Navbar` and `Footer`**: These layout components are rendered on every page, providing a consistent look and feel.
*   **`useAuth()`**: This custom hook (explained later) is used here to get the current user's authentication status (`user`) and whether the authentication check is still in progress (`isLoading`).

### `src/assets/` (Static Assets)

This directory holds static files like images, icons, or fonts that your application uses.
*   **`react.svg`**: The React logo.
*   **`images/`**: A sub-directory for organizing various images.
*   **`styles/`**: A sub-directory for additional, non-Tailwind specific CSS files or global styles.

### `src/components/` (Reusable UI Building Blocks)

This directory is where all the smaller, reusable pieces of your user interface live. Components are designed to be self-contained and focused on a single responsibility.

#### `src/components/auth/` (Authentication Components)

*   **`Login.tsx`**:
    *   **Purpose**: Renders the user login form.
    *   **Code Details**: This component manages the local state for email and password input fields. It uses the `useAuth` hook to call the `login` function when the form is submitted. It also displays toast notifications for success or failure.
    *   **Integration**: It interacts with `useAuth` (which in turn uses `authService`) to send login credentials to the backend.
*   **`Register.tsx`**:
    *   **Purpose**: Renders the user registration form.
    *   **Code Details**: Similar to `Login.tsx`, it manages form input state and uses `useAuth` to call the `register` function.
    *   **Integration**: Sends registration data to the backend via `useAuth` and `authService`.
*   **`GoogleCallback.tsx`**:
    *   **Purpose**: Handles the callback from Google after a user attempts to log in or register using Google OAuth.
    *   **Code Details**: This component typically extracts information from the URL (like authorization codes) and sends it to your backend's Google OAuth callback endpoint to complete the authentication process.
    *   **Integration**: Directly interacts with the backend's Google OAuth endpoint to exchange the authorization code for a JWT token.

#### `src/components/common/` (General Purpose UI Elements)

*   **`Button.tsx`**:
    *   **Purpose**: A generic, reusable button component.
    *   **Code Details**: It likely accepts props like `onClick`, `children` (the text/content inside the button), and styling props. It might use Tailwind CSS classes for its appearance.
    *   **Integration**: Used throughout the application for various actions.
*   **`Input.tsx`**:
    *   **Purpose**: A generic, reusable input field component.
    *   **Code Details**: Accepts props like `type` (text, email, password), `placeholder`, `value`, and `onChange`.
    *   **Integration**: Used in forms across the application.
*   **`ErrorMessage.tsx`**:
    *   **Purpose**: Displays error messages to the user.
    *   **Code Details**: Takes an `error` message as a prop and renders it in a visually distinct way (e.g., red text).
    *   **Integration**: Used by components like `Login.tsx` and `Register.tsx` to show API errors or validation messages.
*   **`ProtectedRoute.tsx`**:
    *   **Purpose**: A special component to protect routes that require user authentication.
    *   **Code Details**: It takes an `isAllowed` prop (a boolean indicating if the user is authenticated). If `isAllowed` is `true`, it renders its child routes (`<Outlet />` from `react-router-dom`). If `false`, it redirects the user to the login page.
    *   **Integration**: Works with `react-router-dom` and `useAuth` to control access to parts of the application.

#### `src/components/layout/` (Application Structure Components)

*   **`Navbar.tsx`**:
    *   **Purpose**: The top navigation bar of the application.
    *   **Code Details**: Contains links to different pages (Home, Dashboard, Properties, Login/Register/Logout). It might dynamically show "Login" and "Register" when logged out, and "Dashboard" and "Logout" when logged in, using the `useAuth` hook.
    *   **Integration**: Uses `react-router-dom` for navigation and `useAuth` for conditional rendering based on authentication status.
*   **`Footer.tsx`**:
    *   **Purpose**: The bottom section of the application, typically containing copyright information or links.
    *   **Code Details**: A simple presentational component with static content.
    *   **Integration**: Included in `App.tsx` to appear on all pages.

#### `src/components/ui/` (UI Library Components - likely Shadcn UI)

This folder likely contains components generated or adapted from a UI library like Shadcn UI. These components are built on top of Tailwind CSS and provide accessible, pre-styled UI elements. They often come with their own `.js`, `.d.ts`, and `.tsx` files.

*   **`button.tsx`, `card.tsx`, `input.tsx`, `label.tsx`, `select.tsx`**: These are highly customizable UI components that abstract away complex styling and accessibility concerns. They are built using Tailwind CSS and often integrate with Radix UI primitives for functionality.
*   **`sonner.tsx`**: This is specifically for "Sonner" toast notifications, providing a visually appealing way to show messages to the user.

### `src/context/AuthContext.tsx` (Authentication State Management)

This is a critical file that manages the global authentication state of your application.

```typescript jsx
// src/context/AuthContext.tsx (Simplified for explanation)
import React, { createContext, useState, useEffect, type ReactNode } from 'react';
import type { User, LoginCredentials, RegisterInfo } from '../types/auth';
import authService from '../services/authService'; // Imports the service for API calls

// 1. Define the shape of our AuthContext data
export interface AuthContextType {
  user: User | null; // The logged-in user's data, or null if not logged in
  token: string | null; // The JWT token, or null
  login: (credentials: LoginCredentials) => Promise<void>; // Function to log in
  register: (userInfo: RegisterInfo) => Promise<void>; // Function to register
  logout: () => void; // Function to log out
  isLoading: boolean; // True while checking auth status or performing auth actions
  error: string | null; // Any error message from auth operations
}

// 2. Create the Context object
export const AuthContext = createContext<AuthContextType | undefined>(undefined);

// 3. Create the Provider component
export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Effect to check for existing token on app load
  useEffect(() => {
    const initAuth = async () => {
      const storedToken = authService.getToken(); // Check localStorage for a token
      if (storedToken) {
        try {
          // If token exists, try to fetch user data to validate it
          const currentUser = await authService.getCurrentUser(storedToken);
          setUser(currentUser);
          setToken(storedToken);
        } catch (err) {
          // If token is invalid/expired, log out
          authService.logout();
          setUser(null);
          setToken(null);
          setError('Session expired or invalid. Please log in again.');
        }
      }
      setIsLoading(false); // Done loading initial auth state
    };
    initAuth();
  }, []); // Runs only once on component mount

  // Function to handle user login
  const login = async (credentials: LoginCredentials) => {
    setIsLoading(true);
    setError(null);
    try {
      // Call the authService to send login request to backend
      const access_token = await authService.login(credentials);
      // If successful, fetch user data using the new token
      const currentUser = await authService.getCurrentUser(access_token);
      setUser(currentUser);
      setToken(access_token);
    } catch (err: any) {
      console.error('Login failed:', err);
      setError(err.message || 'Login failed. Please check your credentials.');
      throw err; // Re-throw to allow components (like Login.tsx) to handle it
    } finally {
      setIsLoading(false);
    }
  };

  // Function to handle user registration (similar to login)
  const register = async (userInfo: RegisterInfo) => {
    setIsLoading(true);
    setError(null);
    try {
      await authService.register(userInfo);
    } catch (err: any) {
      console.error('Registration failed:', err);
      setError(err.message || 'Registration failed. Please try again.');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  // Function to handle user logout
  const logout = () => {
    setIsLoading(true);
    setError(null);
    try {
      authService.logout(); // Clear token from localStorage
      setUser(null);
      setToken(null);
    } catch (err: any) {
      console.error('Logout failed:', err);
      setError(err.message || 'Logout failed.');
    } finally {
      setIsLoading(false);
    }
  };

  // Provide the state and functions to all children components
  return (
    <AuthContext.Provider value={{ user, token, login, register, logout, isLoading, error }}>
      {children}
    </AuthContext.Provider>
  );
};
```
*   **`AuthContextType`**: This TypeScript interface defines the exact structure of the data and functions that will be available through our authentication context. This is crucial for type safety and autocompletion.
*   **`createContext`**: Creates the actual React Context object.
*   **`AuthProvider`**: This is a React component that "provides" the authentication state and functions to all its children. It uses React's `useState` to manage `user`, `token`, `isLoading`, and `error`.
*   **`useEffect`**: This hook runs side effects. Here, it's used to check for an existing token in `localStorage` when the application first loads. If a token is found, it tries to validate it by fetching the user's data from the backend.
*   **`login`, `register`, `logout` functions**: These functions encapsulate the logic for interacting with the `authService` (which talks to the backend) and updating the local authentication state. They also handle loading states and errors.
*   **`authService`**: This is where the actual API calls to the backend are made. The `AuthContext` uses `authService` to perform the network requests.

### `src/hooks/` (Custom React Hooks)

Custom hooks are JavaScript functions that let you use React features (like state and lifecycle methods) in functional components. They promote code reuse and make complex logic easier to manage.

*   **`useAuth.ts`**:
    ```typescript
    // src/hooks/useAuth.ts
    import { useContext } from 'react';
    import { AuthContext } from '../context/AuthContext';
    import type { AuthContextType } from '../context/AuthContext';

    export const useAuth = (): AuthContextType => {
      const context = useContext(AuthContext);
      if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
      }
      return context;
    };
    ```
    *   **Purpose**: Provides a convenient way for any component to access the authentication state and functions from `AuthContext` without directly importing `AuthContext` everywhere.
    *   **How it works**: It uses React's built-in `useContext` hook to read the value provided by the nearest `AuthContext.Provider`. It also includes a check to ensure it's used within an `AuthProvider` to prevent errors.
*   **`useApi.ts`**:
    *   **Purpose**: A custom hook for making authenticated API requests. It likely wraps `axios` and automatically includes the JWT token in the request headers.
    *   **Code Details**: It would get the `token` from `useAuth` and then configure an `axios` instance to include that token in the `Authorization` header for every request made through this hook.
    *   **Integration**: Components that need to fetch data from protected backend endpoints would use `useApi` instead of directly using `axios`.
*   **`use-toast.ts`**:
    *   **Purpose**: A custom hook to easily trigger and manage toast notifications (pop-up messages).
    *   **Code Details**: It provides a function (e.g., `toast.success()`, `toast.error()`) that components can call to display messages. It integrates with the `sonner` UI component.

### `src/lib/utils.ts` (General Utilities)

*   **Purpose**: Contains small, general-purpose utility functions that can be used across different parts of the application.
*   **Code Details**: For a Tailwind CSS project, this file often includes a `cn` function (from `clsx` and `tailwind-merge`) to conditionally combine Tailwind classes.
    ```typescript
    // src/lib/utils.ts (Example)
    import { type ClassValue, clsx } from "clsx"
    import { twMerge } from "tailwind-merge"

    export function cn(...inputs: ClassValue[]) {
      return twMerge(clsx(inputs))
    }
    ```
    This `cn` function is very useful for building dynamic Tailwind styles.

### `src/pages/` (Application Views/Pages)

These components represent the main "screens" or "views" of your application. They often compose smaller components from `src/components/`.

*   **`Home.tsx`**: The landing page of the application.
*   **`LoginPage.tsx`**: Renders the `Login` component from `src/components/auth/`.
*   **`RegisterPage.tsx`**: Renders the `Register` component from `src/components/auth/`.
*   **`Dashboard.tsx`**: The main dashboard for logged-in users. This page would typically fetch user-specific data from the backend using `useApi`.
*   **`Properties.tsx`**: A page to display a list of properties, likely fetching data from a backend `/properties` endpoint.

### `src/services/` (Backend API Interaction Layer)

This directory is crucial for how your frontend talks to your backend. It abstracts away the details of making HTTP requests.

*   **`api.ts`**:
    ```typescript
    // src/services/api.ts
    import axios from 'axios';
    import { API_BASE_URL } from '../utils/constants'; // Imports the backend API URL

    const api = axios.create({
      baseURL: API_BASE_URL, // All requests made with 'api' will start with this URL
      headers: {
        'Content-Type': 'application/json', // Default header for JSON requests
      },
    });

    export default api;
    ```
    *   **Purpose**: Configures the `axios` HTTP client. It sets the base URL for all API requests, so you don't have to type `http://localhost:8000` every time. It also sets a default `Content-Type` header for JSON requests.
    *   **Integration**: This `api` instance is imported and used by other services (like `authService`) to make requests.
*   **`authService.ts`**:
    ```typescript
    // src/services/authService.ts
    import api from './api'; // The configured axios instance
    import { type LoginCredentials, type RegisterInfo, type User } from '../types/auth'; // Data shapes
    import axios from 'axios'; // Import axios directly for specific cases

    // Create a separate axios instance for authentication requests that need x-www-form-urlencoded
    const authApi = axios.create({
      baseURL: API_BASE_URL, // Use the same base URL
    });

    class AuthService {
      // Handles user login
      login = async (credentials: LoginCredentials) => {
        // Create URLSearchParams for x-www-form-urlencoded format
        const params = new URLSearchParams();
        params.append('username', credentials.email); // Backend expects 'username'
        params.append('password', credentials.password);

        const response = await authApi.post('/auth/login', params, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded', // Explicitly set content type
          },
        });
        localStorage.setItem('token', response.data.access_token); // Store the JWT token
        return response.data.access_token;
      };

      // Handles user registration
      register = async (userInfo: RegisterInfo) => {
        const response = await api.post('/auth/register', userInfo); // Uses default JSON content type
        return response.data;
      };

      // Fetches current user details using a token
      getCurrentUser = async (token: string): Promise<User> => {
        const response = await api.get('/users/me', {
          headers: { Authorization: `Bearer ${token}` }, // Attach JWT token for authentication
        });
        return response.data;
      };

      // Retrieves token from local storage
      getToken = (): string | null => {
        return localStorage.getItem('token');
      };

      // Removes token from local storage (logs out user)
      logout = (): void => {
        localStorage.removeItem('token');
      };
    }

    export default new AuthService();
    ```
    *   **Purpose**: Contains all the functions related to user authentication (login, registration, getting current user, logout). It acts as a bridge between your React components and the backend authentication API.
    *   **Integration**:
        *   It uses the `api` (or `authApi` for specific cases like login) `axios` instance to send requests to the backend.
        *   It handles storing and retrieving the JWT (JSON Web Token) from the browser's `localStorage`. This token is essential for authenticating subsequent requests to protected endpoints.
        *   The `login` function specifically demonstrates how to send data in `x-www-form-urlencoded` format, which the FastAPI backend's `OAuth2PasswordRequestForm` expects.
        *   The `getCurrentUser` function shows how to include the `Authorization: Bearer <token>` header, which is how the backend verifies authenticated requests.

### `src/types/` (TypeScript Type Definitions)

This directory is crucial for TypeScript projects. It defines the "shapes" of your data, ensuring consistency and helping prevent errors.

*   **`auth.ts`**:
    ```typescript
    // src/types/auth.ts
    export interface User {
      id: number;
      email: string;
      full_name: string;
      role: 'tenant' | 'landlord' | 'admin'; // Example roles
      phone_number?: string; // Optional field
      profile_picture?: string; // Optional field
      is_active: boolean;
      created_at: string; // Or Date type if parsed
    }

    export interface LoginCredentials {
      email: string;
      password: string;
    }

    export interface RegisterInfo extends LoginCredentials {
      full_name: string;
      role: 'tenant' | 'landlord'; // Users can register as tenant or landlord
      phone_number?: string;
      profile_picture?: string;
    }

    export interface Token {
      access_token: string;
      token_type: string;
    }
    ```
    *   **Purpose**: Defines the data structures for users, login credentials, registration information, and API tokens.
    *   **Why it's important**: When you pass data around your application or send it to the backend, TypeScript checks if the data matches these defined interfaces. This prevents common bugs like typos in property names or sending the wrong type of data.
*   **`property.ts`**:
    *   **Purpose**: Defines the data structure for property objects (e.g., `Property` interface with fields like `id`, `address`, `rent`, `landlord_id`).

### `src/utils/` (General Utility Functions and Constants)

*   **`constants.ts`**:
    ```typescript
    // src/utils/constants.ts
    export const API_BASE_URL = 'http://localhost:8000'; // Your backend API URL
    // Other constants like API keys, default values, etc.
    ```
    *   **Purpose**: Stores important, unchanging values (constants) that are used throughout the application, like the backend API URL. This makes it easy to change these values in one place if needed.
*   **`helpers.ts`**:
    *   **Purpose**: Contains small, pure functions that perform specific tasks and don't depend on or modify the application's state. Examples might include date formatting, string manipulation, or validation helpers.

---

## 6. Frontend-Backend Integration: The Communication Flow

This section explains how the frontend and backend work together, focusing on the authentication process as a prime example.

1.  **User Interaction (Frontend)**:
    *   When a user visits the `/login` page, the `LoginPage.tsx` component renders the `Login.tsx` component.
    *   The user types their email and password into the `Input` components.
    *   When the user clicks the "Sign In" `Button`, the `handleLogin` function in `Login.tsx` is triggered.

2.  **Initiating Authentication (Frontend - `Login.tsx` -> `useAuth` -> `AuthContext`)**:
    *   `Login.tsx` calls the `login` function provided by the `useAuth` hook: `await login({ email, password });`.
    *   The `useAuth` hook (in `src/hooks/useAuth.ts`) simply returns the `login` function from the `AuthContext`.
    *   The `login` function within `AuthContext.tsx` is then executed. It sets `isLoading` to `true` (to show a loading spinner) and clears any previous errors.

3.  **Making the API Call (Frontend - `AuthContext` -> `authService` -> `api.ts`)**:
    *   Inside `AuthContext`'s `login` function, `authService.login(credentials)` is called.
    *   `authService.ts` then uses the `authApi` (an `axios` instance configured for `x-www-form-urlencoded` requests) to send a `POST` request to `http://localhost:8000/auth/login`. The `email` is sent as `username` and `password` as `password` in the form data.

4.  **Backend Processing (Backend - FastAPI)**:
    *   The FastAPI backend receives the `POST /auth/login` request.
    *   The `login` endpoint in `backend/app/routers/auth.py` uses `LoginCredentials` (a Pydantic model) to validate the incoming JSON data.
    *   It queries the database to find the user by email and verifies the password using `pwd_context.verify()`.
    *   If credentials are valid, it generates a JWT `access_token`. This token contains the user's email (`sub`, for "subject") and an expiration time.
    *   The backend sends a JSON response back to the frontend containing the `access_token` and `token_type: "bearer"`.

5.  **Handling the Response & Storing Token (Frontend - `authService` -> `AuthContext`)**:
    *   Back in `authService.ts`, the `axios` call receives the successful response from the backend.
    *   `localStorage.setItem('token', response.data.access_token)` saves the received JWT token in the browser's local storage. This token persists even if the user closes and reopens the browser.
    *   `authService.getCurrentUser(access_token)` is then called to fetch the full user profile from the backend's `/users/me` endpoint. This is important to get all user details (like `full_name`, `role`, etc.) that are not part of the login response. This request includes the `Authorization: Bearer <token>` header.

6.  **Updating Frontend State (Frontend - `AuthContext` -> Components)**:
    *   Once `getCurrentUser` successfully fetches the user data, `AuthContext` updates its `user` state with the fetched data and `token` state with the new token.
    *   It sets `isLoading` to `false`.
    *   Because `AuthContext` is a React Context, any component that uses the `useAuth` hook (like `Navbar.tsx` or `Dashboard.tsx`) will automatically re-render with the updated `user` and `token` values.
    *   `Login.tsx` then navigates the user to the `/dashboard` page using `navigate('/dashboard')`.

7.  **Accessing Protected Resources (Frontend - `ProtectedRoute` & `useApi`)**:
    *   When the user tries to access a protected route (e.g., `/dashboard`), the `ProtectedRoute.tsx` component checks the `user` state from `useAuth`. If `user` is not null, it allows the `Dashboard` component to render.
    *   Inside `Dashboard.tsx` (or any other protected page), if it needs to fetch more data from the backend (e.g., a list of properties), it would use the `useApi` hook. This hook automatically adds the `Authorization: Bearer <token>` header to all its requests, ensuring they are authenticated by the backend.

---

## 7. Conclusion

This detailed documentation should provide a solid foundation for understanding the Rent Management System's frontend. We've covered:

*   The core technologies (React, TypeScript, Vite, Tailwind CSS).
*   How to set up and run the project.
*   A comprehensive breakdown of the folder structure and the purpose of each significant file.
*   An in-depth explanation of the frontend-backend communication, particularly focusing on the authentication flow using JWT tokens.

By understanding these concepts and the role of each file, you should be well-equipped to navigate, debug, and contribute to this project. Remember, the best way to learn is by doing, so feel free to explore the code and experiment!
