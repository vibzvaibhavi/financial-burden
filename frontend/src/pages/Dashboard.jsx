import React, { useState, useEffect } from 'react'
import { 
  Shield, 
  UserCheck, 
  CreditCard, 
  FileText, 
  TrendingUp, 
  AlertTriangle,
  CheckCircle,
  Clock
} from 'lucide-react'
import { analysisAPI, vantaAPI, auditAPI } from '../services/api'
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

const RiskLevelBadge = ({ level }) => {
  const colors = {
    LOW: 'risk-low',
    MEDIUM: 'risk-medium',
    HIGH: 'risk-high'
  }
  
  return (
    <span className={`risk-badge ${colors[level] || 'risk-medium'}`}>
      {level}
    </span>
  )
}

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState({
    analyses: { total_today: 0, high_risk: 0, medium_risk: 0, low_risk: 0 },
    compliance: { status: 'unknown', last_check: null },
    sars: { total: 0, recent: 0 },
    system: { status: 'operational', last_backup: null, encryption: 'enabled' }
  })
  const [complianceData, setComplianceData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      
      // Fetch audit dashboard data
      const auditResponse = await auditAPI.getDashboard()
      setDashboardData(auditResponse.data.data)
      
      // Fetch compliance summary
      const complianceResponse = await vantaAPI.getSummary()
      setComplianceData(complianceResponse.data.data)
      
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
      toast.error('Failed to load dashboard data')
    } finally {
      setLoading(false)
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
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          FinTrust AI - Secure FinTech Compliance Copilot
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Analyses Today"
          value={dashboardData.analyses.total_today}
          icon={TrendingUp}
          color="bg-primary-500"
          trend="+12% from yesterday"
        />
        <StatCard
          title="High Risk Cases"
          value={dashboardData.analyses.high_risk}
          icon={AlertTriangle}
          color="bg-danger-500"
        />
        <StatCard
          title="SARs Generated"
          value={dashboardData.sars.total}
          icon={FileText}
          color="bg-warning-500"
        />
        <StatCard
          title="Compliance Score"
          value={complianceData?.compliance_score || 0}
          icon={Shield}
          color="bg-success-500"
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Risk Analysis Overview */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Risk Analysis Overview</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Low Risk</span>
              <div className="flex items-center space-x-2">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-success-500 h-2 rounded-full" 
                    style={{ width: `${(dashboardData.analyses.low_risk / Math.max(dashboardData.analyses.total_today, 1)) * 100}%` }}
                  ></div>
                </div>
                <span className="text-sm font-medium text-gray-900">{dashboardData.analyses.low_risk}</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Medium Risk</span>
              <div className="flex items-center space-x-2">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-warning-500 h-2 rounded-full" 
                    style={{ width: `${(dashboardData.analyses.medium_risk / Math.max(dashboardData.analyses.total_today, 1)) * 100}%` }}
                  ></div>
                </div>
                <span className="text-sm font-medium text-gray-900">{dashboardData.analyses.medium_risk}</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">High Risk</span>
              <div className="flex items-center space-x-2">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-danger-500 h-2 rounded-full" 
                    style={{ width: `${(dashboardData.analyses.high_risk / Math.max(dashboardData.analyses.total_today, 1)) * 100}%` }}
                  ></div>
                </div>
                <span className="text-sm font-medium text-gray-900">{dashboardData.analyses.high_risk}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Compliance Status */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Compliance Status</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Overall Status</span>
              <div className="flex items-center space-x-2">
                {complianceData?.status === 'compliant' ? (
                  <CheckCircle className="h-5 w-5 text-success-500" />
                ) : (
                  <AlertTriangle className="h-5 w-5 text-warning-500" />
                )}
                <span className="text-sm font-medium text-gray-900 capitalize">
                  {complianceData?.status || 'Unknown'}
                </span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Controls Passed</span>
              <span className="text-sm font-medium text-gray-900">
                {complianceData?.passed_controls || 0} / {complianceData?.total_controls || 0}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Risk Findings</span>
              <span className="text-sm font-medium text-gray-900">
                {complianceData?.risk_findings_count || 0}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Last Updated</span>
              <span className="text-sm text-gray-500">
                <Clock className="h-4 w-4 inline mr-1" />
                {complianceData?.last_updated ? 
                  new Date(complianceData.last_updated).toLocaleDateString() : 
                  'Never'
                }
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <a
            href="/kyc-analysis"
            className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <UserCheck className="h-8 w-8 text-primary-600 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-900">KYC Analysis</p>
              <p className="text-xs text-gray-500">Analyze customer profiles</p>
            </div>
          </a>
          <a
            href="/transaction-analysis"
            className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <CreditCard className="h-8 w-8 text-primary-600 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-900">Transaction Analysis</p>
              <p className="text-xs text-gray-500">Check suspicious activity</p>
            </div>
          </a>
          <a
            href="/compliance"
            className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <Shield className="h-8 w-8 text-primary-600 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-900">Compliance Check</p>
              <p className="text-xs text-gray-500">View compliance status</p>
            </div>
          </a>
          <a
            href="/audit"
            className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <FileText className="h-8 w-8 text-primary-600 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-900">Audit Reports</p>
              <p className="text-xs text-gray-500">View audit logs</p>
            </div>
          </a>
        </div>
      </div>
    </div>
  )
}
