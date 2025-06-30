import axios from 'axios';
import { API_BASE_URL } from '../utils/constants';

const api = axios.create({
  baseURL: API_BASE_URL,
});

class AuthService {
  login = async (credentials: any) => {
    const response = await api.post('/auth/login', new URLSearchParams(credentials), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    localStorage.setItem('token', response.data.access_token);
    return response.data;
  };

  register = async (userInfo: any) => {
    const response = await api.post('/auth/register', userInfo, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  };

  getCurrentUser = async (token: string) => {
    const response = await api.get('/users/me', {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  };

  getToken = () => {
    return localStorage.getItem('token');
  };

  logout = ()_=> {
    localStorage.removeItem('token');
  };
}

export default new AuthService();