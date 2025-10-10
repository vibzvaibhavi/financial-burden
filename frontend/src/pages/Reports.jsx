import React, { useState, useEffect } from 'react'
import { BarChart3, Download, Calendar, TrendingUp, AlertTriangle, CheckCircle } from 'lucide-react'
import { auditAPI, analysisAPI, vantaAPI } from '../services/api'
import toast from 'react-hot-toast'

const StatCard = ({ title, value, icon: Icon, color, trend }) => (
  <div className="card">
    <div className="flex items-center">
      <div className={`p-2 rounded-lg ${color}`}>
        <Icon className="h-6 w-6 text-white" />
      </div>
      <div className="ml-4">
        <p className="text-sm font-medium text-gray-600">{title}</p>
        <p className="text-2xl font-semibold text-gray-900">{value}</p>
        {trend && (
          <p className="text-xs text-gray-500">{trend}</p>
        )}
      </div>
    </div>
  </div>
)

export default function Reports() {
  const [dashboardData, setDashboardData] = useState(null)
  const [complianceData, setComplianceData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [dateRange, setDateRange] = useState({
    start: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    end: new Date().toISOString().split('T')[0]
  })

  useEffect(() => {
    fetchReportsData()
  }, [])

  const fetchReportsData = async () => {
    try {
      setLoading(true)
      
      // Fetch audit dashboard data
      const auditResponse = await auditAPI.getDashboard()
      setDashboardData(auditResponse.data.data)
      
      // Fetch compliance summary
      const complianceResponse = await vantaAPI.getSummary()
      setComplianceData(complianceResponse.data.data)
      
    } catch (error) {
      console.error('Error fetching reports data:', error)
      toast.error('Failed to load reports data')
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async (format = 'json') => {
    try {
      const response = await auditAPI.exportData(dateRange.start, dateRange.end, format)
      toast.success(`${format.toUpperCase()} export initiated successfully`)
    } catch (error) {
      console.error('Export error:', error)
      toast.error('Failed to initiate export')
    }
  }

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
          <h1 className="text-2xl font-bold text-gray-900">Reports & Analytics</h1>
          <p className="mt-1 text-sm text-gray-500">
            Comprehensive reporting and analytics dashboard
          </p>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => handleExport('json')}
            className="btn btn-secondary"
          >
            <Download className="h-4 w-4 mr-2" />
            Export JSON
          </button>
          <button
            onClick={() => handleExport('csv')}
            className="btn btn-primary"
          >
            <Download className="h-4 w-4 mr-2" />
            Export CSV
          </button>
        </div>
      </div>

      {/* Date Range Selector */}
      <div className="card">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Report Period</h2>
        <div className="flex flex-col sm:flex-row gap-4">
          <div>
            <label className="label">Start Date</label>
            <input
              type="date"
              className="input"
              value={dateRange.start}
              onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
            />
          </div>
          <div>
            <label className="label">End Date</label>
            <input
              type="date"
              className="input"
              value={dateRange.end}
              onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
            />
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Total Analyses"
          value={dashboardData?.analyses?.total_today || 0}
          icon={BarChart3}
          color="bg-primary-500"
          trend="+12% from last month"
        />
        <StatCard
          title="High Risk Cases"
          value={dashboardData?.analyses?.high_risk || 0}
          icon={AlertTriangle}
          color="bg-danger-500"
        />
        <StatCard
          title="SARs Generated"
          value={dashboardData?.sars?.total || 0}
          icon={CheckCircle}
          color="bg-warning-500"
        />
        <StatCard
          title="Compliance Score"
          value={complianceData?.compliance_score || 0}
          icon={TrendingUp}
          color="bg-success-500"
        />
      </div>

      {/* Risk Analysis Breakdown */}
      <div className="card">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Risk Analysis Breakdown</h2>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Low Risk</span>
            <div className="flex items-center space-x-2">
              <div className="w-32 bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-success-500 h-2 rounded-full" 
                  style={{ 
                    width: `${(dashboardData?.analyses?.low_risk || 0) / Math.max(dashboardData?.analyses?.total_today || 1, 1) * 100}%` 
                  }}
                ></div>
              </div>
              <span className="text-sm font-medium text-gray-900 w-8">
                {dashboardData?.analyses?.low_risk || 0}
              </span>
            </div>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Medium Risk</span>
            <div className="flex items-center space-x-2">
              <div className="w-32 bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-warning-500 h-2 rounded-full" 
                  style={{ 
                    width: `${(dashboardData?.analyses?.medium_risk || 0) / Math.max(dashboardData?.analyses?.total_today || 1, 1) * 100}%` 
                  }}
                ></div>
              </div>
              <span className="text-sm font-medium text-gray-900 w-8">
                {dashboardData?.analyses?.medium_risk || 0}
              </span>
            </div>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">High Risk</span>
            <div className="flex items-center space-x-2">
              <div className="w-32 bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-danger-500 h-2 rounded-full" 
                  style={{ 
                    width: `${(dashboardData?.analyses?.high_risk || 0) / Math.max(dashboardData?.analyses?.total_today || 1, 1) * 100}%` 
                  }}
                ></div>
              </div>
              <span className="text-sm font-medium text-gray-900 w-8">
                {dashboardData?.analyses?.high_risk || 0}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Compliance Overview */}
      {complianceData && (
        <div className="card">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Compliance Overview</h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <div>
              <h3 className="text-sm font-medium text-gray-600">Controls Passed</h3>
              <p className="text-2xl font-semibold text-gray-900">
                {complianceData.passed_controls || 0} / {complianceData.total_controls || 0}
              </p>
              <p className="text-sm text-gray-500">
                {complianceData.total_controls > 0 ? 
                  Math.round((complianceData.passed_controls / complianceData.total_controls) * 100) : 0
                }% pass rate
              </p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-600">Risk Findings</h3>
              <p className="text-2xl font-semibold text-gray-900">
                {complianceData.risk_findings_count || 0}
              </p>
              <p className="text-sm text-gray-500">Active findings</p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-600">Overall Status</h3>
              <p className="text-2xl font-semibold text-gray-900 capitalize">
                {complianceData.status || 'Unknown'}
              </p>
              <p className="text-sm text-gray-500">
                Last updated: {complianceData.last_updated ? 
                  new Date(complianceData.last_updated).toLocaleDateString() : 
                  'Never'
                }
              </p>
            </div>
          </div>
        </div>
      )}

      {/* System Health */}
      <div className="card">
        <h2 className="text-lg font-medium text-gray-900 mb-4">System Health</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div>
            <h3 className="text-sm font-medium text-gray-600">System Status</h3>
            <p className="text-sm font-semibold text-gray-900 capitalize">
              {dashboardData?.system?.status || 'Unknown'}
            </p>
          </div>
          <div>
            <h3 className="text-sm font-medium text-gray-600">Encryption</h3>
            <p className="text-sm font-semibold text-gray-900 capitalize">
              {dashboardData?.system?.encryption || 'Unknown'}
            </p>
          </div>
          <div>
            <h3 className="text-sm font-medium text-gray-600">Last Backup</h3>
            <p className="text-sm font-semibold text-gray-900">
              {dashboardData?.system?.last_backup ? 
                new Date(dashboardData.system.last_backup).toLocaleDateString() : 
                'Never'
              }
            </p>
          </div>
          <div>
            <h3 className="text-sm font-medium text-gray-600">Recent SARs</h3>
            <p className="text-sm font-semibold text-gray-900">
              {dashboardData?.sars?.recent || 0}
            </p>
          </div>
        </div>
      </div>

      {/* Report Actions */}
      <div className="card">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Generate Reports</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <button
            onClick={() => handleExport('json')}
            className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <Download className="h-8 w-8 text-primary-600 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-900">Export JSON</p>
              <p className="text-xs text-gray-500">Machine-readable format</p>
            </div>
          </button>
          <button
            onClick={() => handleExport('csv')}
            className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <Download className="h-8 w-8 text-primary-600 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-900">Export CSV</p>
              <p className="text-xs text-gray-500">Spreadsheet format</p>
            </div>
          </button>
          <button
            onClick={fetchReportsData}
            className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <Calendar className="h-8 w-8 text-primary-600 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-900">Refresh Data</p>
              <p className="text-xs text-gray-500">Update all metrics</p>
            </div>
          </button>
        </div>
      </div>
    </div>
  )
}
