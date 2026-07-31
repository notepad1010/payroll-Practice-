import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from '@/lib/queryClient';
import { AuthProvider } from '@/context/AuthContext';
import { Toaster } from '@/components/ui/sonner'
import ProtectedRoute from '@/components/ProtectedRoute';
import Login from '@/pages/Login';
import Dashboard from '@/pages/Dashboard';
import EmployeeList from '@/pages/employees/EmployeeList';


export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/employees"
              element={
                <ProtectedRoute>
                  <EmployeeList />
                </ProtectedRoute>
              }
            />
          </Routes>
        </AuthProvider>
      <Toaster/>
      </BrowserRouter>
      
    </QueryClientProvider>
  );
}