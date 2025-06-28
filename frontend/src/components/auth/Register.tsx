import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { API_BASE_URL } from '../../utils/constants';

const Register: React.FC = () => {
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('tenant');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [profilePicture, setProfilePicture] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e: React.FormEvent) => {
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
    } catch (err) {
      setError('Registration failed');
    }
  };

  return (
    <div className="min-h-screen bg-neutral flex items-center justify-center">
      <div className="max-w-md w-full mx-auto p-6 bg-white rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold mb-4 text-primary">Register</h2>
        <form onSubmit={handleRegister}>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1 text-secondary">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full p-2 border border-secondary rounded focus:ring focus:ring-accent"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1 text-secondary">Full Name</label>
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className="w-full p-2 border border-secondary rounded focus:ring focus:ring-accent"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1 text-secondary">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-2 border border-secondary rounded focus:ring focus:ring-accent"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1 text-secondary">Role</label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="w-full p-2 border border-secondary rounded focus:ring focus:ring-accent"
            >
              <option value="tenant">Tenant</option>
              <option value="owner">Owner</option>
              <option value="admin">Admin</option>
              <option value="broker">Broker</option>
            </select>
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1 text-secondary">Phone Number</label>
            <input
              type="text"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              className="w-full p-2 border border-secondary rounded focus:ring focus:ring-accent"
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1 text-secondary">Profile Picture URL</label>
            <input
              type="text"
              value={profilePicture}
              onChange={(e) => setProfilePicture(e.target.value)}
              className="w-full p-2 border border-secondary rounded focus:ring focus:ring-accent"
            />
          </div>
          {error && <p className="text-error mb-4">{error}</p>}
          <button type="submit" className="w-full bg-primary text-white p-2 rounded hover:bg-accent transition">
            Register
          </button>
        </form>
        <a href="http://localhost:8000/auth/google" className="block text-center mt-4 text-accent hover:underline">
          Register with Google
        </a>
      </div>
    </div>
  );
};

export default Register;