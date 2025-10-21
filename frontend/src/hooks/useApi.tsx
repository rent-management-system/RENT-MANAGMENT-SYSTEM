import { useState, useCallback } from 'react';
import axios, { AxiosError } from 'axios';
import { useAuth } from './useAuth';
const useApi = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { token, logout } = useAuth();
  const request = useCallback(
    async (config) => {
      setLoading(true);
      setError(null);
      try {
        const headers = token ? { Authorization: `Bearer ${token}` } : {};
        const response = await axios({
          ...config,
          headers: { ...headers, ...config.headers },
        });
        setData(response.data);
        return response;
      } catch (err) {
        const axiosError = err;
        if (axiosError.response) {
          if (axiosError.response.status === 401) {
            logout();
            setError('Unauthorized: Please log in again.');
          } else {
            setError(axiosError.response.data?.message || 'An error occurred.');
          }
        } else if (axiosError.request) {
          setError('No response received from server.');
        } else {
          setError(axiosError.message || 'An unknown error occurred.');
        }
        return undefined;
      } finally {
        setLoading(false);
      }
    },
    [token, logout],
  );
  return { data, loading, error, request };
};
export default useApi;
