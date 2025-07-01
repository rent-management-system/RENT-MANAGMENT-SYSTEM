import api from './api';
import { type LoginCredentials, type RegisterInfo, type User } from '../types/auth';

class AuthService {
  login = async (credentials: LoginCredentials) => {
    const response = await api.post('/auth/login', credentials);
    localStorage.setItem('token', response.data.access_token);
    return response.data;
  };

  register = async (userInfo: RegisterInfo) => {
    const response = await api.post('/auth/register', userInfo);
    return response.data;
  };

  getCurrentUser = async (token: string): Promise<User> => {
    const response = await api.get('/users/me', {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  };

  getToken = (): string | null => {
    return localStorage.getItem('token');
  };

  logout = (): void => {
    localStorage.removeItem('token');
  };
}

export default new AuthService();