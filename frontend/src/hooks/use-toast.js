
import React, { createContext, useContext, useState, useCallback } from 'react';

const ToastContext = createContext();

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const toast = useCallback(({ title, description, variant = 'default' }) => {
    const id = Math.random().toString(36).substring(2, 9);
    setToasts((prev) => [
      ...prev,
      { id, title, description, variant },
    ]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4000);
  }, []);

  return (
    <ToastContext.Provider value={{ toast }}>
      {children}
      <div className="fixed bottom-4 right-4 z-50 space-y-2">
        {toasts.map(({ id, title, description, variant }) => (
          <div
            key={id}
            className={`px-4 py-2 rounded-md shadow-lg ${
              variant === 'destructive'
                ? 'bg-red-500 text-white'
                : variant === 'success'
                ? 'bg-green-500 text-white'
                : 'bg-white text-gray-800 dark:bg-gray-800 dark:text-white'
            }`}
          >
            <h3 className="font-medium">{title}</h3>
            {description && <p className="text-sm opacity-90">{description}</p>}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  return useContext(ToastContext);
}
