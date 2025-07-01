import { type AxiosRequestConfig, type AxiosResponse } from 'axios';
interface UseApiResult<T> {
    data: T | null;
    loading: boolean;
    error: string | null;
    request: (config: AxiosRequestConfig) => Promise<AxiosResponse<T> | undefined>;
}
declare const useApi: <T = any>() => UseApiResult<T>;
export default useApi;
