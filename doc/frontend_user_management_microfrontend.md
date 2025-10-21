# Frontend Micro-frontend for User Management Microservice

## Introduction

This document outlines the conceptual design and features of the frontend micro-frontend responsible for interacting with the User Management Backend Microservice. It describes how user-related functionalities, such as authentication, profile management, and administrative user controls, are exposed to the end-user through a modular and independently deployable frontend component.

## Purpose

The User Management Micro-frontend serves as the user interface layer for all interactions with the User Management Backend Microservice. Its primary goals are:
*   To provide a seamless and intuitive user experience for registration, login, and profile management.
*   To enforce role-based access control (RBAC) on the frontend, mirroring backend permissions.
*   To handle secure token management (JWTs) for authenticated sessions.
*   To integrate smoothly into a larger Rental Management System frontend application using micro-frontend architectural patterns.
*   To support multilingual interfaces (English, Amharic, Afaan Oromo) for accessibility.

## Architecture Overview: Micro-frontend Approach

This micro-frontend is designed to be a self-contained, independently developed, and deployable unit that integrates into a larger "shell" or "container" application.

*   **Shell Application:** The main Rental Management System frontend application acts as the shell, responsible for:
    *   Loading and orchestrating different micro-frontends.
    *   Providing global layout, navigation, and shared dependencies.
    *   Defining communication channels between micro-frontends.
*   **User Management Micro-frontend:** This specific micro-frontend focuses solely on user-related concerns. It exposes its functionalities (e.g., login page, profile page) as routes or components that the shell application can render.
*   **Communication:**
    *   **Props/Custom Events:** Communication with the shell application and other micro-frontends can occur via props (for direct parent-child relationships) or custom browser events (for more decoupled, sibling-to-sibling communication).
    *   **Shared State (Optional):** A lightweight global state management solution (e.g., Context API, Zustand) might be used for sharing minimal, non-sensitive user data (e.g., `isLoggedIn`, `userRole`) across micro-frontends, if necessary, while avoiding tight coupling.

## Key Components and Modules

The micro-frontend is logically divided into several components and modules, reflecting the backend's structure and user interactions.

### 1. Authentication Module

This module handles all user authentication flows.

*   **`Login.tsx`:**
    *   **Functionality:** Provides a form for users to enter their email and password.
    *   **Interaction:** Sends credentials to `POST /api/v1/auth/login`.
    *   **Response Handling:** Stores received `access_token` and `refresh_token` securely (e.g., in HTTP-only cookies or local storage, with careful security considerations). Handles `HTTP 401` for incorrect credentials and `HTTP 403` for pre-seeded admins requiring password change.
    *   **Google OAuth:** Initiates the Google OAuth flow, redirecting to Google's authentication page.
*   **`Register.tsx`:**
    *   **Functionality:** Provides a form for new users to sign up, including fields for `email`, `password`, `full_name`, `phone_number`, `preferred_language`, and `preferred_currency`.
    *   **Interaction:** Sends user data to `POST /api/v1/users/register`.
    *   **Validation:** Performs client-side validation, including the Ethiopian phone number regex (`+251[79]\d{8}$`).
    *   **Error Handling:** Displays appropriate messages for duplicate emails or invalid input.
*   **`GoogleCallback.tsx`:**
    *   **Functionality:** Handles the redirect from Google OAuth after successful authentication.
    *   **Interaction:** Exchanges the authorization code for tokens with the backend (assumed to be a separate backend endpoint or handled within the `login` flow).
    *   **Token Storage:** Stores received JWTs.
*   **`ChangePassword.tsx`:**
    *   **Functionality:** Allows authenticated users to change their password, requiring `old_password` and `new_password`.
    *   **Interaction:** Sends data to `POST /api/v1/auth/change-password`.
    *   **Permissions:** Accessible only to authenticated users.
*   **Logout Functionality:**
    *   **Functionality:** Clears stored tokens and redirects the user to the login page.
    *   **Interaction:** May optionally call a backend logout endpoint to invalidate server-side sessions/refresh tokens (though current backend design relies on token expiry/cleanup).

### 2. User Profile Module

This module allows authenticated users to view and manage their profile information.

*   **`ProfileView.tsx` (or integrated into `Dashboard.tsx`):**
    *   **Functionality:** Displays the current user's details (`full_name`, `email`, `phone_number`, `preferred_language`, `preferred_currency`).
    *   **Interaction:** Fetches data from `GET /api/v1/users/me`.
    *   **Permissions:** Accessible only to authenticated users.
*   **`ProfileEdit.tsx` (or integrated into `Dashboard.tsx`):**
    *   **Functionality:** Provides a form to update user details (`full_name`, `phone_number`, `preferred_language`, `preferred_currency`).
    *   **Interaction:** Sends updated data to `PUT /api/v1/users/me`.
    *   **Validation:** Client-side validation for `phone_number` regex.
    *   **Permissions:** Accessible only to authenticated users.

### 3. Admin User Management Module

This module provides administrative functionalities for managing users.

*   **`UserList.tsx`:**
    *   **Functionality:** Displays a paginated list of all registered users.
    *   **Interaction:** Fetches data from `GET /api/v1/admin/users`.
    *   **Permissions:** Accessible only to users with the `ADMIN` role. Displays `HTTP 403` if unauthorized.
*   **`UserDetail.tsx`:**
    *   **Functionality:** Displays detailed information for a specific user, identified by `user_id`.
    *   **Interaction:** Fetches data from `GET /api/v1/admin/users/{user_id}`.
    *   **Permissions:** Accessible only to users with the `ADMIN` role.

### 4. Shared Components and Utilities

These are foundational elements supporting the micro-frontend.

*   **`AuthContext.tsx` / `useAuth.ts`:**
    *   **Functionality:** Manages the authentication state (e.g., `isLoggedIn`, `user`, `accessToken`, `refreshToken`).
    *   **Token Refresh Logic:** Implements automatic token refreshing using `POST /api/v1/auth/refresh` when the access token is about to expire or has expired.
    *   **User Data Provider:** Makes authenticated user data available throughout the micro-frontend.
*   **`api.ts` / `authService.ts` / `useApi.ts`:**
    *   **Functionality:** Centralized API client (e.g., Axios instance) configured to interact with the backend microservice.
    *   **JWT Injection:** Automatically attaches the `access_token` to the `Authorization: Bearer <token>` header of all outgoing requests.
    *   **Error Interceptors:** Handles global API errors, such as `HTTP 401 Unauthorized` (redirect to login) or `HTTP 403 Forbidden` (display permission error).
*   **`components/common/` & `components/ui/`:** Reusable UI components (e.g., `Button.tsx`, `Input.tsx`, `ErrorMessage.tsx`, `card.tsx`, `label.tsx`) for consistent styling and user experience.
*   **`router/ProtectedRoute.tsx` & `router/GuestRoute.tsx`:** Components to protect routes based on authentication status and user roles, redirecting unauthorized users.
*   **`utils/helpers.ts`:** Utility functions, potentially including client-side phone number formatting or language-specific text handling.

## Interaction with Backend Microservice

The frontend micro-frontend communicates exclusively with the User Management Backend Microservice via its RESTful API endpoints.

*   **API Endpoint Mapping:** Each significant user action on the frontend (login, register, view profile, etc.) corresponds directly to a specific backend API endpoint.
*   **JWT Handling:**
    *   Upon successful login/refresh, the `access_token` and `refresh_token` are received.
    *   The `access_token` is included in the `Authorization: Bearer <token>` header for all subsequent authenticated requests.
    *   The `refresh_token` is used by the `AuthContext` to silently obtain new `access_token`s when needed.
*   **Error Handling:**
    *   **HTTP 401 Unauthorized:** Triggers a redirect to the login page and clears local authentication state.
    *   **HTTP 403 Forbidden:** Displays a user-friendly message indicating insufficient permissions.
    *   **Validation Errors (HTTP 422/400):** Displays specific error messages returned by the backend (e.g., "Email already registered", "Invalid phone number") next to the relevant input fields.
*   **Data Flow:** Frontend components send data conforming to backend Pydantic schemas (e.g., `UserCreate`, `UserUpdate`) and receive responses structured according to backend schemas (e.g., `User`, `Token`, `UserTokenData`).

## Technology Stack (Assumed based on project context)

*   **Framework:** React (TypeScript)
*   **Routing:** React Router
*   **State Management:** React Context API (for authentication state), potentially a lightweight library like Zustand for other local states.
*   **Styling:** Tailwind CSS (as indicated by `tailwind.config.js`), potentially with Shadcn UI components.
*   **API Client:** Axios or standard Fetch API.
*   **Build Tool:** Vite (as indicated by `vite.config.ts`).

## Deployment Considerations

*   **Independent Deployment:** The User Management Micro-frontend can be built, tested, and deployed independently of the main shell application and other micro-frontends.
*   **Integration:** The shell application would dynamically load this micro-frontend, possibly using techniques like Webpack Module Federation, single-spa, or simpler iframe/script loading, depending on the chosen micro-frontend framework.

## Future Considerations

*   **Full Google OAuth Flow:** Implement the complete Google OAuth callback logic within the micro-frontend and integrate it with the backend's Google OAuth endpoints.
*   **Real-time Updates:** For features like user status changes (if applicable), consider WebSockets for real-time updates.
*   **Internationalization (i18n):** Implement a robust i18n library (e.g., `react-i18next`) to fully support dynamic language switching based on `preferred_language` settings.
*   **Accessibility (a11y):** Ensure all components adhere to WCAG guidelines for users with disabilities.
*   **Performance Optimization:** Implement lazy loading for routes and components, code splitting, and image optimization.

---
