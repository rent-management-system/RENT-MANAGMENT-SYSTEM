export interface User {
    id: number;
    email: string;
    full_name: string;
    role: string;
    phone_number: string;
    profile_picture: string;
}
export interface LoginCredentials {
    email: string;
    password: string;
}
export interface RegisterInfo {
    full_name: string;
    email: string;
    password: string;
    phone_number: string;
    role: string;
}
