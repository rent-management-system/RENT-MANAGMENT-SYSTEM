import api from './api';
import { LoginCredentials, RegisterInfo, User } from '../types/auth';

interface LoginResponse {
  access_token: string;
  token_type: string;
}

class AuthService {
  async login(credentials: LoginCredentials): Promise<{ user: User; token: string }> {
    const response = await api.post<LoginResponse>('/auth/login', credentials);
    const token = response.data.access_token;
    
    // After getting the token, get user data
    const user = await this.getCurrentUser(token);
    return { user, token };
  }

  async register(userInfo: RegisterInfo): Promise<User> {
    const response = await api.post<User>('/auth/register', userInfo);
    return response.data;
  }

  async getCurrentUser(token?: string): Promise<User> {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await api.get<User>('/users/me', { headers });
    return response.data;
  }
}

export default new AuthService();
