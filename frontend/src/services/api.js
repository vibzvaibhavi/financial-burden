import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API endpoints
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  me: () => api.get('/auth/me'),
  logout: () => api.post('/auth/logout'),
}

export const analysisAPI = {
  analyzeKYC: (data) => api.post('/analyze/kyc', data),
  analyzeTransaction: (data) => api.post('/analyze/transaction', data),
  comprehensiveAnalysis: (data) => api.post('/analyze/comprehensive', data),
  getStatus: () => api.get('/analyze/status'),
}

export const vantaAPI = {
  getControls: () => api.get('/vanta/controls'),
  getRisks: () => api.get('/vanta/risks'),
  getEvidence: (controlId) => api.get(`/vanta/evidence/${controlId}`),
  getOrganizationStatus: () => api.get('/vanta/organization/status'),
  getCompliancePosture: () => api.get('/vanta/compliance-posture'),
  getSummary: () => api.get('/vanta/summary'),
  healthCheck: () => api.get('/vanta/health'),
}

export const auditAPI = {
  listSARs: (customerId) => api.get('/audit/sars', { params: { customer_id: customerId } }),
  getSAR: (sarId, customerId) => api.get(`/audit/sars/${sarId}`, { params: { customer_id: customerId } }),
  createAuditLog: (action, details, userId) => api.post('/audit/logs', { action, details, user_id: userId }),
  listReports: (reportType, customerId) => api.get('/audit/reports', { params: { report_type: reportType, customer_id: customerId } }),
  getDashboard: () => api.get('/audit/dashboard'),
  exportData: (startDate, endDate, format) => api.get('/audit/export', { params: { start_date: startDate, end_date: endDate, format } }),
  healthCheck: () => api.get('/audit/health'),
}
