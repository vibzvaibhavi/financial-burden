import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { AuthProvider } from './contexts/AuthContext'
import { ProtectedRoute } from './components/ProtectedRoute'
import Layout from './components/Layout'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import KYCAnalysis from './pages/KYCAnalysis'
import TransactionAnalysis from './pages/TransactionAnalysis'
import Compliance from './pages/Compliance'
import Audit from './pages/Audit'
import Reports from './pages/Reports'

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Toaster position="top-right" />
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }>
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="kyc-analysis" element={<KYCAnalysis />} />
              <Route path="transaction-analysis" element={<TransactionAnalysis />} />
              <Route path="compliance" element={<Compliance />} />
              <Route path="audit" element={<Audit />} />
              <Route path="reports" element={<Reports />} />
            </Route>
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  )
}

export default App
