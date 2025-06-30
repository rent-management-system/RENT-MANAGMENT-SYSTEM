import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  return (
    <div className="text-center py-12">
      <h1 className="text-4xl font-bold text-gray-800 mb-4">Welcome to Rent Management System</h1>
      <p className="text-gray-600 mb-8">Please log in or register to continue</p>
      <div className="space-x-4">
        <Link to="/login" className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors">
          Login
        </Link>
        <Link to="/register" className="bg-white hover:bg-gray-100 text-gray-800 font-medium py-2 px-6 border border-gray-300 rounded-lg transition-colors">
          Register
        </Link>
      </div>
    </div>
  );
};

export default Home;