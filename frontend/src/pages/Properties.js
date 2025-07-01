import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import React from 'react';
const Properties = () => {
    // In a real application, you would fetch and display property data here.
    // This might involve using the useApi hook to fetch data.
    // Example: const { data: properties, loading, error, request } = useApi<Property[]>();
    return (_jsxs("div", { className: "container mx-auto px-4 py-8", children: [_jsx("h1", { className: "text-3xl font-bold text-gray-800 mb-6", children: "Properties" }), _jsx("div", { className: "bg-white p-6 rounded-lg shadow-md", children: _jsx("p", { className: "text-gray-700", children: "List of properties will appear here." }) })] }));
};
export default Properties;
