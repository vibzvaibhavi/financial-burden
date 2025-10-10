import React, { useState, useEffect } from 'react'
import { FileText, Download, Search, Calendar, User } from 'lucide-react'
import { auditAPI } from '../services/api'
import toast from 'react-hot-toast'

const SARCard = ({ sar }) => (
  <div className="card hover:shadow-md transition-shadow">
    <div className="flex items-start justify-between">
      <div className="flex-1">
        <h3 className="text-sm font-medium text-gray-900">{sar.sar_id}</h3>
        <p className="text-sm text-gray-600 mt-1">
          Customer: {sar.customer_id || 'Unknown'}
        </p>
        <p className="text-xs text-gray-500 mt-1">
          Last Modified: {new Date(sar.last_modified).toLocaleString()}
        </p>
      </div>
      <div className="ml-4">
        <button className="text-primary-600 hover:text-primary-800 text-sm font-medium">
          View
        </button>
      </div>
    </div>
  </div>
)

export default function Audit() {
  const [sars, setSars] = useState([])
  const [dashboardData, setDashboardData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCustomer, setSelectedCustomer] = useState('')

  useEffect(() => {
    fetchAuditData()
  }, [])

  const fetchAuditData = async () => {
    try {
      setLoading(true)
      
      // Fetch SARs
      const sarsResponse = await auditAPI.listSARs()
      setSars(sarsResponse.data.data.sars || [])
      
      // Fetch dashboard data
      const dashboardResponse = await auditAPI.getDashboard()
      setDashboardData(dashboardResponse.data.data)
      
    } catch (error) {
      console.error('Error fetching audit data:', error)
      toast.error('Failed to load audit data')
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async () => {
    try {
      const startDate = new Date()
      startDate.setMonth(startDate.getMonth() - 1)
      const endDate = new Date()
      
      const response = await auditAPI.exportData(
        startDate.toISOString().split('T')[0],
        endDate.toISOString().split('T')[0],
        'json'
      )
      
      toast.success('Export initiated successfully')
    } catch (error) {
      console.error('Export error:', error)
      toast.error('Failed to initiate export')
    }
  }

  const filteredSARs = sars.filter(sar => {
    const matchesSearch = sar.sar_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (sar.customer_id && sar.customer_id.toLowerCase().includes(searchTerm.toLowerCase()))
    const matchesCustomer = !selectedCustomer || sar.customer_id === selectedCustomer
    return matchesSearch && matchesCustomer
  })

  const uniqueCustomers = [...new Set(sars.map(sar => sar.customer_id).filter(Boolean))]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Audit & Reports</h1>
          <p className="mt-1 text-sm text-gray-500">
            SAR documents, audit logs, and compliance reports
          </p>
        </div>
        <button
          onClick={handleExport}
          className="btn btn-primary"
        >
          <Download className="h-4 w-4 mr-2" />
          Export Data
        </button>
      </div>

      {/* Dashboard Stats */}
      {dashboardData && (
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <div className="card">
            <div className="flex items-center">
              <div className="p-2 rounded-lg bg-primary-500">
                <FileText className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total SARs</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {dashboardData.sars.total}
                </p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="p-2 rounded-lg bg-warning-500">
                <Calendar className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Recent SARs</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {dashboardData.sars.recent}
                </p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="p-2 rounded-lg bg-success-500">
                <FileText className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Analyses Today</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {dashboardData.analyses.total_today}
                </p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="p-2 rounded-lg bg-gray-500">
                <User className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">System Status</p>
                <p className="text-sm font-semibold text-gray-900 capitalize">
                  {dashboardData.system.status}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="card">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <label className="label">Search SARs</label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                className="input pl-10"
                placeholder="Search by SAR ID or Customer ID..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          <div className="sm:w-48">
            <label className="label">Filter by Customer</label>
            <select
              className="input"
              value={selectedCustomer}
              onChange={(e) => setSelectedCustomer(e.target.value)}
            >
              <option value="">All Customers</option>
              {uniqueCustomers.map(customer => (
                <option key={customer} value={customer}>{customer}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* SARs List */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-medium text-gray-900">
            Suspicious Activity Reports ({filteredSARs.length})
          </h2>
        </div>
        
        {filteredSARs.length > 0 ? (
          <div className="space-y-4">
            {filteredSARs.map((sar, index) => (
              <SARCard key={index} sar={sar} />
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <FileText className="h-12 w-12 mx-auto mb-4 text-gray-300" />
            <p>No SARs found</p>
            {searchTerm && (
              <p className="text-sm mt-2">Try adjusting your search criteria</p>
            )}
          </div>
        )}
      </div>

      {/* System Information */}
      {dashboardData && (
        <div className="card">
          <h2 className="text-lg font-medium text-gray-900 mb-4">System Information</h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <h3 className="text-sm font-medium text-gray-600">System Status</h3>
              <p className="text-sm text-gray-900 capitalize">{dashboardData.system.status}</p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-600">Encryption</h3>
              <p className="text-sm text-gray-900 capitalize">{dashboardData.system.encryption}</p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-600">Last Backup</h3>
              <p className="text-sm text-gray-900">
                {new Date(dashboardData.system.last_backup).toLocaleString()}
              </p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-600">Compliance Status</h3>
              <p className="text-sm text-gray-900 capitalize">{dashboardData.compliance.status}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
