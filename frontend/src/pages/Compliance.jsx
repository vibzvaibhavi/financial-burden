import React, { useState, useEffect } from 'react'
import { Shield, CheckCircle, AlertTriangle, Clock, RefreshCw } from 'lucide-react'
import { vantaAPI } from '../services/api'
import toast from 'react-hot-toast'

const StatusBadge = ({ status }) => {
  const colors = {
    compliant: 'bg-success-100 text-success-800',
    needs_attention: 'bg-warning-100 text-warning-800',
    non_compliant: 'bg-danger-100 text-danger-800',
    unknown: 'bg-gray-100 text-gray-800'
  }
  
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status] || colors.unknown}`}>
      {status.replace('_', ' ').toUpperCase()}
    </span>
  )
}

const ControlCard = ({ control }) => (
  <div className="card">
    <div className="flex items-start justify-between">
      <div className="flex-1">
        <h3 className="text-sm font-medium text-gray-900">{control.name || control.title || 'Control'}</h3>
        <p className="text-sm text-gray-600 mt-1">{control.description || 'No description available'}</p>
        {control.category && (
          <span className="inline-block mt-2 px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
            {control.category}
          </span>
        )}
      </div>
      <div className="ml-4">
        {control.status === 'passed' ? (
          <CheckCircle className="h-5 w-5 text-success-500" />
        ) : control.status === 'failed' ? (
          <AlertTriangle className="h-5 w-5 text-danger-500" />
        ) : (
          <Clock className="h-5 w-5 text-warning-500" />
        )}
      </div>
    </div>
  </div>
)

export default function Compliance() {
  const [complianceData, setComplianceData] = useState(null)
  const [controls, setControls] = useState([])
  const [riskFindings, setRiskFindings] = useState([])
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)

  useEffect(() => {
    fetchComplianceData()
  }, [])

  const fetchComplianceData = async () => {
    try {
      setLoading(true)
      
      // Fetch compliance summary
      const summaryResponse = await vantaAPI.getSummary()
      setComplianceData(summaryResponse.data.data)
      
      // Fetch controls
      const controlsResponse = await vantaAPI.getControls()
      setControls(controlsResponse.data.data?.data || [])
      
      // Fetch risk findings
      const risksResponse = await vantaAPI.getRisks()
      setRiskFindings(risksResponse.data.data?.data || [])
      
    } catch (error) {
      console.error('Error fetching compliance data:', error)
      toast.error('Failed to load compliance data')
    } finally {
      setLoading(false)
    }
  }

  const handleRefresh = async () => {
    setRefreshing(true)
    await fetchComplianceData()
    setRefreshing(false)
    toast.success('Compliance data refreshed')
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
          <h1 className="text-2xl font-bold text-gray-900">Compliance Status</h1>
          <p className="mt-1 text-sm text-gray-500">
            Real-time compliance monitoring with Vanta API integration
          </p>
        </div>
        <button
          onClick={handleRefresh}
          disabled={refreshing}
          className="btn btn-secondary"
        >
          {refreshing ? (
            <RefreshCw className="h-4 w-4 animate-spin mr-2" />
          ) : (
            <RefreshCw className="h-4 w-4 mr-2" />
          )}
          Refresh
        </button>
      </div>

      {/* Compliance Overview */}
      {complianceData && (
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <div className="card">
            <div className="flex items-center">
              <div className="p-2 rounded-lg bg-primary-500">
                <Shield className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Compliance Score</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {complianceData.compliance_score || 0}%
                </p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="p-2 rounded-lg bg-success-500">
                <CheckCircle className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Controls Passed</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {complianceData.passed_controls || 0} / {complianceData.total_controls || 0}
                </p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="p-2 rounded-lg bg-warning-500">
                <AlertTriangle className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Risk Findings</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {complianceData.risk_findings_count || 0}
                </p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="p-2 rounded-lg bg-gray-500">
                <Clock className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Last Updated</p>
                <p className="text-sm font-semibold text-gray-900">
                  {complianceData.last_updated ? 
                    new Date(complianceData.last_updated).toLocaleDateString() : 
                    'Never'
                  }
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Overall Status */}
      {complianceData && (
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-medium text-gray-900">Overall Compliance Status</h2>
              <p className="text-sm text-gray-600 mt-1">
                Current compliance posture based on Vanta monitoring
              </p>
            </div>
            <StatusBadge status={complianceData.status} />
          </div>
        </div>
      )}

      {/* Controls */}
      <div className="card">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Compliance Controls</h2>
        {controls.length > 0 ? (
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            {controls.slice(0, 10).map((control, index) => (
              <ControlCard key={index} control={control} />
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <Shield className="h-12 w-12 mx-auto mb-4 text-gray-300" />
            <p>No controls data available</p>
          </div>
        )}
      </div>

      {/* Risk Findings */}
      {riskFindings.length > 0 && (
        <div className="card">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Risk Findings</h2>
          <div className="space-y-4">
            {riskFindings.slice(0, 5).map((finding, index) => (
              <div key={index} className="border border-warning-200 rounded-lg p-4 bg-warning-50">
                <div className="flex items-start">
                  <AlertTriangle className="h-5 w-5 text-warning-500 mr-3 mt-0.5 flex-shrink-0" />
                  <div className="flex-1">
                    <h3 className="text-sm font-medium text-warning-900">
                      {finding.title || finding.name || 'Risk Finding'}
                    </h3>
                    <p className="text-sm text-warning-700 mt-1">
                      {finding.description || finding.details || 'No description available'}
                    </p>
                    {finding.severity && (
                      <span className="inline-block mt-2 px-2 py-1 bg-warning-200 text-warning-800 text-xs rounded">
                        {finding.severity}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Organization Status */}
      {complianceData?.organization_status && (
        <div className="card">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Organization Status</h2>
          <div className="bg-gray-50 rounded-lg p-4">
            <pre className="text-sm text-gray-700 whitespace-pre-wrap">
              {JSON.stringify(complianceData.organization_status, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  )
}
