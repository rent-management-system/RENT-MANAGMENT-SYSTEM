import React, { type ReactNode } from 'react';
import type { User, LoginCredentials, RegisterInfo } from '../types/auth';
export interface AuthContextType {
    user: User | null;
    token: string | null;
    login: (credentials: LoginCredentials) => Promise<void>;
    register: (userInfo: RegisterInfo) => Promise<void>;
    logout: () => void;
    isLoading: boolean;
    error: string | null;
}
export declare const AuthContext: React.Context<AuthContextType | undefined>;
interface AuthProviderProps {
    children: ReactNode;
}
export declare const AuthProvider: React.FC<AuthProviderProps>;
export {};
