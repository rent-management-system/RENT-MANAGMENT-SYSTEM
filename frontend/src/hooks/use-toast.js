// import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
// import { clsx } from 'clsx'; // Import clsx
export {};
// interface Toast {
//   id: string;
//   title: string;
//   description?: string;
//   variant?: 'default' | 'destructive' | 'success';
// }
// interface ToastContextType {
//   toast: (options: Omit<Toast, 'id'>) => void;
// }
// const ToastContext = createContext<ToastContextType | undefined>(undefined);
// interface ToastProviderProps {
//   children: ReactNode;
// }
// export function ToastProvider({ children }: ToastProviderProps) {
//   const [toasts, setToasts] = useState<Toast[]>([]);
//   const toast = useCallback(({ title, description, variant = 'default' }: Omit<Toast, 'id'>) => {
//     const id = Math.random().toString(36).substring(2, 9);
//     setToasts((prev) => [
//       ...prev,
//       { id, title, description, variant },
//     ]);
//     setTimeout(() => {
//       setToasts((prev) => prev.filter((t) => t.id !== id));
//     }, 4000);
//   }, []);
//   return (
//     <ToastContext.Provider value={{ toast }}>
//       {children}
//       <div className="fixed bottom-4 right-4 z-50 space-y-2">
//         {toasts.map(({ id, title, description, variant }) => (
//           <div
//             key={id}
//             className={clsx(
//               "px-4 py-2 rounded-md shadow-lg",
//               variant === 'destructive' && 'bg-red-500 text-white',
//               variant === 'success' && 'bg-green-500 text-white',
//               variant === 'default' && 'bg-white text-gray-800 dark:bg-gray-800 dark:text-white'
//             )}
//           >
//             <h3 className="font-medium">{title}</h3>
//             {description && <p className="text-sm opacity-90">{description}</p>}
//           </div>
//         ))}
//       </div>
//     </ToastContext.Provider>
//   );
// }
// export function useToast() {
//   const context = useContext(ToastContext);
//   if (context === undefined) {
//     throw new Error('useToast must be used within a ToastProvider');
//   }
//   return context;
// }
