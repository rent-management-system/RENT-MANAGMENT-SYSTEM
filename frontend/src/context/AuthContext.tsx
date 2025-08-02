import { jsx as _jsx } from 'react/jsx-runtime';
import React, { createContext, useState, useEffect } from 'react';
import authService from '../services/authService';
export const AuthContext = createContext(undefined);
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
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
  const login = async (credentials) => {
    setIsLoading(true);
    setError(null);
    try {
      const access_token = await authService.login(credentials);
      const currentUser = await authService.getCurrentUser(access_token);
      setUser(currentUser);
      setToken(access_token);
    } catch (err) {
      console.error('Login failed:', err);
      setError(err.message || 'Login failed. Please check your credentials.');
      throw err; // Re-throw to allow components to handle it
    } finally {
      setIsLoading(false);
    }
  };
  const register = async (userInfo) => {
    setIsLoading(true);
    setError(null);
    try {
      await authService.register(userInfo);
    } catch (err) {
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
    } catch (err) {
      console.error('Logout failed:', err);
      setError(err.message || 'Logout failed.');
    } finally {
      setIsLoading(false);
    }
  };
  return _jsx(AuthContext.Provider, {
    value: { user, token, login, register, logout, isLoading, error },
    children: children,
  });
};
