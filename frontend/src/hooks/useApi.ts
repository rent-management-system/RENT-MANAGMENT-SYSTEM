import { useState, useCallback } from 'react';
import axios, {
  type AxiosRequestConfig,
  type AxiosResponse,
  AxiosError,
} from 'axios';
import { useAuth } from './useAuth';

interface UseApiResult<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  request: (
    config: AxiosRequestConfig,
  ) => Promise<AxiosResponse<T> | undefined>;
}

const useApi = <T = any>(): UseApiResult<T> => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const { token, logout } = useAuth();

  const request = useCallback(
    async (
      config: AxiosRequestConfig,
    ): Promise<AxiosResponse<T> | undefined> => {
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
        const axiosError = err as AxiosError<{ message?: string }>;
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
