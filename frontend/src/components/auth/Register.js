import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { API_BASE_URL } from '../../utils/constants';
const Register = () => {
    const [email, setEmail] = useState('');
    const [fullName, setFullName] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('tenant');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [profilePicture, setProfilePicture] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            await axios.post(`${API_BASE_URL}/auth/register`, {
                email,
                full_name: fullName,
                password,
                role,
                phone_number: phoneNumber,
                profile_picture: profilePicture
            });
            navigate('/login');
        }
        catch (err) {
            setError('Registration failed');
        }
    };
    return (_jsx("div", { className: "min-h-screen bg-neutral flex items-center justify-center", children: _jsxs("div", { className: "max-w-md w-full mx-auto p-6 bg-white rounded-lg shadow-lg", children: [_jsx("h2", { className: "text-2xl font-bold mb-4 text-primary", children: "Register" }), _jsxs("form", { onSubmit: handleRegister, children: [_jsxs("div", { className: "mb-4", children: [_jsx("label", { className: "block text-sm font-medium mb-1 text-secondary", children: "Email" }), _jsx("input", { type: "email", value: email, onChange: (e) => setEmail(e.target.value), className: "w-full p-2 border border-secondary rounded focus:ring focus:ring-accent", required: true })] }), _jsxs("div", { className: "mb-4", children: [_jsx("label", { className: "block text-sm font-medium mb-1 text-secondary", children: "Full Name" }), _jsx("input", { type: "text", value: fullName, onChange: (e) => setFullName(e.target.value), className: "w-full p-2 border border-secondary rounded focus:ring focus:ring-accent", required: true })] }), _jsxs("div", { className: "mb-4", children: [_jsx("label", { className: "block text-sm font-medium mb-1 text-secondary", children: "Password" }), _jsx("input", { type: "password", value: password, onChange: (e) => setPassword(e.target.value), className: "w-full p-2 border border-secondary rounded focus:ring focus:ring-accent", required: true })] }), _jsxs("div", { className: "mb-4", children: [_jsx("label", { className: "block text-sm font-medium mb-1 text-secondary", children: "Role" }), _jsxs("select", { value: role, onChange: (e) => setRole(e.target.value), className: "w-full p-2 border border-secondary rounded focus:ring focus:ring-accent", children: [_jsx("option", { value: "tenant", children: "Tenant" }), _jsx("option", { value: "owner", children: "Owner" }), _jsx("option", { value: "admin", children: "Admin" }), _jsx("option", { value: "broker", children: "Broker" })] })] }), _jsxs("div", { className: "mb-4", children: [_jsx("label", { className: "block text-sm font-medium mb-1 text-secondary", children: "Phone Number" }), _jsx("input", { type: "text", value: phoneNumber, onChange: (e) => setPhoneNumber(e.target.value), className: "w-full p-2 border border-secondary rounded focus:ring focus:ring-accent" })] }), _jsxs("div", { className: "mb-4", children: [_jsx("label", { className: "block text-sm font-medium mb-1 text-secondary", children: "Profile Picture URL" }), _jsx("input", { type: "text", value: profilePicture, onChange: (e) => setProfilePicture(e.target.value), className: "w-full p-2 border border-secondary rounded focus:ring focus:ring-accent" })] }), error && _jsx("p", { className: "text-error mb-4", children: error }), _jsx("button", { type: "submit", className: "w-full bg-primary text-white p-2 rounded hover:bg-accent transition", children: "Register" })] }), _jsx("a", { href: "http://localhost:8000/auth/google", className: "block text-center mt-4 text-accent hover:underline", children: "Register with Google" })] }) }));
};
export default Register;
