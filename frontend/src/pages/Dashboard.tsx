import React from 'react';

const Dashboard: React.FC = () => {
  // In a real application, you would fetch and display user-specific data here.
  // This might involve using the useAuth hook to get user info, or useApi to fetch data.
  // Example: const { user } = useAuth();
  // Example: const { data, loading, error, request } = useApi();

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Dashboard</h1>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <p className="text-gray-700">Welcome to your dashboard! More content will be added here soon.</p>
        {/* Future content like user stats, recent activities, property summaries would go here */}
      </div>
    </div>
  );
};

export default Dashboard;
