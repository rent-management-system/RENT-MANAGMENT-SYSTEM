import { type LoginCredentials, type RegisterInfo, type User } from '../types/auth';
declare class AuthService {
    login: (credentials: LoginCredentials) => Promise<any>;
    register: (userInfo: RegisterInfo) => Promise<any>;
    getCurrentUser: (token: string) => Promise<User>;
    getToken: () => string | null;
    logout: () => void;
}
declare const _default: AuthService;
export default _default;
