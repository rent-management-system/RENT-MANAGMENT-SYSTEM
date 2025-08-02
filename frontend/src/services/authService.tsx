import api from './api';
import {} from '../types/auth';
class AuthService {
  login = async (credentials) => {
    const response = await api.post('/auth/login', credentials);
    localStorage.setItem('token', response.data.access_token);
    return response.data.access_token;
  };
  register = async (userInfo) => {
    const response = await api.post('/auth/register', userInfo);
    return response.data;
  };
  getCurrentUser = async (token) => {
    const response = await api.get('/users/me', {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  };
  getToken = () => {
    return localStorage.getItem('token');
  };
  logout = () => {
    localStorage.removeItem('token');
  };
}
export default new AuthService();
