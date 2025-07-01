# Frontend Documentation

## 1. Introduction

Welcome to the frontend documentation for the Rent Management System. This document provides a comprehensive overview of the frontend architecture, components, and how it interacts with the backend API.

The frontend is a **Single-Page Application (SPA)** built using **React** and **TypeScript**. It is responsible for providing the user interface and managing the user experience.

**Technology Stack:**
- **Framework:** React
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios
- **Routing:** React Router
- **State Management:** React Context API

---

## 2. Project Setup

To get the frontend running locally, follow these steps:

1.  **Navigate to the frontend directory:**
    ```bash
    cd /home/dagi/Documents/Rent-managment-system/frontend
    ```

2.  **Install dependencies:**
    All required Node.js packages are listed in `package.json`.
    ```bash
    npm install
    ```

3.  **Run the development server:**
    The application is run using `vite`, a modern frontend build tool.
    ```bash
    npm run dev
    ```
    - The server will be accessible at `http://localhost:5173` (or another port if 5173 is busy).

---

## 3. Folder Structure

The frontend code is organized into a modular and scalable structure.

```
frontend/
├── public/
│   └── index.html
└── src/
    ├── assets/
    ├── components/
    │   ├── auth/
    │   ├── common/
    │   └── layout/
    ├── context/
    ├── hooks/
    ├── lib/
    ├── pages/
    ├── services/
    ├── types/
    └── utils/
```

#### File-by-File Explanation:

- **`public/`**: Contains static assets that are not processed by the build tool, like the main `index.html` file.

- **`src/`**: This is where all the application's source code lives.

- **`src/main.tsx`**: The entry point of the React application. It renders the root component (`App`) into the DOM.

- **`src/App.tsx`**: The main application component. It sets up the routing and wraps the application with the `AuthProvider` to provide authentication context to all components.

- **`src/pages/`**: Each file in this directory represents a page in the application (e.g., `LoginPage.tsx`, `Dashboard.tsx`). These components are responsible for the overall layout and data fetching for a specific page.

- **`src/components/`**: Contains reusable UI components.
    - **`auth/`**: Components specifically for authentication, like `Login.tsx` and `Register.tsx`.
    - **`common/`**: Generic, reusable components like `Button.tsx`, `Input.tsx`, etc.
    - **`layout/`**: Components that define the overall structure of the application, like `Navbar.tsx` and `Footer.tsx`.

- **`src/services/`**: This directory handles all communication with the backend API.
    - **`api.ts`**: Creates and configures the main `axios` instance, setting the `baseURL` for all API requests.
    - **`authService.ts`**: Contains functions for making authentication-related API calls, like `login`, `register`, and `getCurrentUser`.

- **`src/context/`**: Manages global application state using React's Context API.
    - **`AuthContext.tsx`**: This is the most important context. It provides the `user` object, the `token`, and functions like `login` and `logout` to the entire application. This allows any component to know if a user is logged in and to perform authentication actions.

- **`src/hooks/`**: Contains custom React hooks.
    - **`useAuth.ts`**: A simple hook that provides easy access to the `AuthContext`.

- **`src/types/`**: Defines TypeScript types and interfaces for the application, ensuring data consistency (e.g., `User`, `LoginCredentials`).

- **`src/utils/`**: Contains utility functions and constants.

---

## 4. Frontend-Backend Integration

The frontend and backend communicate via a RESTful API. Here's how the integration works:

1.  **API Client (`axios`)**: The `src/services/api.ts` file creates a centralized `axios` instance. All API requests go through this instance, which is configured with the backend's base URL (`http://localhost:8000`).

2.  **Service Layer**: The `src/services/authService.ts` file acts as a service layer that abstracts the API calls. For example, the `login` function in this file takes the user's credentials, makes a `POST` request to the `/auth/login` endpoint, and returns the access token.

3.  **State Management (`AuthContext`)**: The `src/context/AuthContext.tsx` file uses the `authService` to manage the user's authentication state.
    - When the `login` function in the context is called, it calls `authService.login`.
    - If the login is successful, the context stores the returned `token` in `localStorage` and fetches the user's data by calling `authService.getCurrentUser`.
    - The `user` and `token` are then made available to all components through the `useAuth` hook.

4.  **Protected Routes**: We can use the `useAuth` hook to create protected routes. For example, the `Dashboard` page can check if a user is logged in. If not, it can redirect them to the `LoginPage`.

5.  **CORS (Cross-Origin Resource Sharing)**: The backend is configured to allow requests from the frontend's origin (`http://localhost:5173`). This is done in `backend/app/main.py` using `CORSMiddleware`.