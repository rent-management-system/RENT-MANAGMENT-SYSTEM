import React, {
  createContext,
  useReducer,
  useEffect,
  useMemo,
  type ReactNode,
} from 'react';
import { User, LoginCredentials, RegisterInfo } from '../types/auth';
import authService from '../services/authService';
import { jwtDecode } from 'jwt-decode';

interface AuthState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
}

type AuthAction =
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: User }
  | { type: 'LOGIN_FAILURE'; payload: string }
  | { type: 'REGISTER_FAILURE'; payload: string }
  | { type: 'LOGOUT' }
  | { type: 'INITIALIZE'; payload: User | null };

export interface AuthContextType extends AuthState {
  login: (credentials: LoginCredentials) => Promise<User>;
  register: (userInfo: RegisterInfo) => Promise<void>;
  logout: () => void;
}

const initialState: AuthState = {
  user: null,
  isLoading: true,
  error: null,
};

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'LOGIN_START':
      return { ...state, isLoading: true, error: null };
    case 'LOGIN_SUCCESS':
      return { ...state, isLoading: false, user: action.payload, error: null };
    case 'LOGIN_FAILURE':
    case 'REGISTER_FAILURE':
      return { ...state, isLoading: false, error: action.payload, user: null };
    case 'LOGOUT':
      return { ...state, user: null, error: null };
    case 'INITIALIZE':
      return { ...state, user: action.payload, isLoading: false };
    default:
      return state;
  }
};

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  useEffect(() => {
    const initializeAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          // Ensure token is not expired
          const decoded: { exp: number } = jwtDecode(token);
          if (decoded.exp * 1000 < Date.now()) {
            localStorage.removeItem('token');
            dispatch({ type: 'INITIALIZE', payload: null });
            return;
          }
          
          const user = await authService.getCurrentUser();
          dispatch({ type: 'INITIALIZE', payload: user });
        } catch (error) {
          localStorage.removeItem('token');
          dispatch({ type: 'INITIALIZE', payload: null });
        }
      } else {
        dispatch({ type: 'INITIALIZE', payload: null });
      }
    };
    initializeAuth();
  }, []);

  const login = async (credentials: LoginCredentials) => {
    dispatch({ type: 'LOGIN_START' });
    try {
      const { user, token } = await authService.login(credentials);
      localStorage.setItem('token', token);
      dispatch({ type: 'LOGIN_SUCCESS', payload: user });
      return user;
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.detail || 'Login failed. Please check your credentials.';
      dispatch({ type: 'LOGIN_FAILURE', payload: errorMessage });
      throw new Error(errorMessage);
    }
  };

  const register = async (userInfo: RegisterInfo) => {
    try {
      await authService.register(userInfo);
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.detail || 'Registration failed. Please try again.';
      dispatch({ type: 'REGISTER_FAILURE', payload: errorMessage });
      throw new Error(errorMessage);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    dispatch({ type: 'LOGOUT' });
  };

  const value = useMemo(
    () => ({
      ...state,
      login,
      register,
      logout,
    }),
    [state],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};