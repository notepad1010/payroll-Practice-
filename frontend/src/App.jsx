import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import EmployeeList from './pages/employees/EmployeeList'
import AttendanceList from './pages/attendance/AttendanceList'
import LeaveRequestList from './pages/leave/LeaveRequestList'
import PayrunList from './pages/payroll/PayrunList'

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={
            <ProtectedRoute><Dashboard /></ProtectedRoute>
          } />
          <Route path="/employees" element={
            <ProtectedRoute><EmployeeList /></ProtectedRoute>
          } />
          <Route path="/attendance" element={
            <ProtectedRoute><AttendanceList /></ProtectedRoute>
          } />
          <Route path="/leave" element={
            <ProtectedRoute><LeaveRequestList /></ProtectedRoute>
          } />
          <Route path="/payroll" element={
            <ProtectedRoute><PayrunList /></ProtectedRoute>
          } />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}