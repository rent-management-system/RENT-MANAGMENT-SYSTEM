import React, { createContext, useState, useEffect, type ReactNode } from 'react';
import type { User, LoginCredentials, RegisterInfo } from '../types/auth';
import authService from '../services/authService';

export interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (userInfo: RegisterInfo) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
  error: string | null;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const initAuth = async () => {
      const storedToken = authService.getToken();
      if (storedToken) {
        try {
          const currentUser = await authService.getCurrentUser(storedToken);
          setUser(currentUser);
          setToken(storedToken);
        } catch (err) {
          console.error('Failed to fetch user from token:', err);
          authService.logout();
          setUser(null);
          setToken(null);
          setError('Session expired or invalid. Please log in again.');
        }
      }
      setIsLoading(false);
    };
    initAuth();
  }, []);

  const login = async (credentials: LoginCredentials) => {
    setIsLoading(true);
    setError(null);
    try {
      const { access_token } = await authService.login(credentials);
      const currentUser = await authService.getCurrentUser(access_token);
      setUser(currentUser);
      setToken(access_token);
    } catch (err: any) {
      console.error('Login failed:', err);
      setError(err.message || 'Login failed. Please check your credentials.');
      throw err; // Re-throw to allow components to handle it
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (userInfo: RegisterInfo) => {
    setIsLoading(true);
    setError(null);
    try {
      await authService.register(userInfo);
    } catch (err: any) {
      console.error('Registration failed:', err);
      setError(err.message || 'Registration failed. Please try again.');
      throw err; // Re-throw to allow components to handle it
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setIsLoading(true);
    setError(null);
    try {
      authService.logout();
      setUser(null);
      setToken(null);
    } catch (err: any) {
      console.error('Logout failed:', err);
      setError(err.message || 'Logout failed.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout, isLoading, error }}>
      {children}
    </AuthContext.Provider>
  );
};
