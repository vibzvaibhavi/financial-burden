import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { UserCheck, Loader2, AlertCircle, CheckCircle } from 'lucide-react'
import { analysisAPI } from '../services/api'
import toast from 'react-hot-toast'

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

export default function KYCAnalysis() {
  const [analysisResult, setAnalysisResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const { register, handleSubmit, formState: { errors }, reset } = useForm()

  const onSubmit = async (data) => {
    try {
      setLoading(true)
      setAnalysisResult(null)
      
      const response = await analysisAPI.analyzeKYC(data)
      setAnalysisResult(response.data)
      toast.success('KYC analysis completed successfully!')
      
    } catch (error) {
      console.error('KYC analysis error:', error)
      toast.error('Failed to analyze KYC profile')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    reset()
    setAnalysisResult(null)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">KYC Analysis</h1>
        <p className="mt-1 text-sm text-gray-500">
          Analyze customer profiles for risk assessment using Claude 3 Sonnet 4
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Form */}
        <div className="card">
          <div className="flex items-center mb-4">
            <UserCheck className="h-6 w-6 text-primary-600 mr-2" />
            <h2 className="text-lg font-medium text-gray-900">Customer Information</h2>
          </div>
          
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="label">Customer ID *</label>
              <input
                type="text"
                className="input"
                {...register('customer_id', { required: 'Customer ID is required' })}
                placeholder="Enter customer ID"
              />
              {errors.customer_id && (
                <p className="mt-1 text-sm text-danger-600">{errors.customer_id.message}</p>
              )}
            </div>

            <div>
              <label className="label">Full Name *</label>
              <input
                type="text"
                className="input"
                {...register('name', { required: 'Name is required' })}
                placeholder="Enter full name"
              />
              {errors.name && (
                <p className="mt-1 text-sm text-danger-600">{errors.name.message}</p>
              )}
            </div>

            <div>
              <label className="label">Date of Birth *</label>
              <input
                type="date"
                className="input"
                {...register('date_of_birth', { required: 'Date of birth is required' })}
              />
              {errors.date_of_birth && (
                <p className="mt-1 text-sm text-danger-600">{errors.date_of_birth.message}</p>
              )}
            </div>

            <div>
              <label className="label">Address *</label>
              <textarea
                className="input"
                rows={3}
                {...register('address', { required: 'Address is required' })}
                placeholder="Enter full address"
              />
              {errors.address && (
                <p className="mt-1 text-sm text-danger-600">{errors.address.message}</p>
              )}
            </div>

            <div>
              <label className="label">Occupation *</label>
              <input
                type="text"
                className="input"
                {...register('occupation', { required: 'Occupation is required' })}
                placeholder="Enter occupation"
              />
              {errors.occupation && (
                <p className="mt-1 text-sm text-danger-600">{errors.occupation.message}</p>
              )}
            </div>

            <div>
              <label className="label">Annual Income *</label>
              <input
                type="number"
                className="input"
                {...register('annual_income', { 
                  required: 'Annual income is required',
                  min: { value: 0, message: 'Income must be positive' }
                })}
                placeholder="Enter annual income"
              />
              {errors.annual_income && (
                <p className="mt-1 text-sm text-danger-600">{errors.annual_income.message}</p>
              )}
            </div>

            <div>
              <label className="label">Source of Funds *</label>
              <select
                className="input"
                {...register('source_of_funds', { required: 'Source of funds is required' })}
              >
                <option value="">Select source of funds</option>
                <option value="Employment">Employment</option>
                <option value="Business">Business</option>
                <option value="Investment">Investment</option>
                <option value="Inheritance">Inheritance</option>
                <option value="Gift">Gift</option>
                <option value="Other">Other</option>
              </select>
              {errors.source_of_funds && (
                <p className="mt-1 text-sm text-danger-600">{errors.source_of_funds.message}</p>
              )}
            </div>

            <div>
              <label className="label">PEP Status</label>
              <select className="input" {...register('pep_status')}>
                <option value="No">No</option>
                <option value="Yes">Yes</option>
                <option value="Family Member">Family Member</option>
              </select>
            </div>

            <div>
              <label className="label">Sanctions Check</label>
              <select className="input" {...register('sanctions_check')}>
                <option value="Clear">Clear</option>
                <option value="Flagged">Flagged</option>
                <option value="Pending">Pending</option>
              </select>
            </div>

            <div className="flex space-x-3">
              <button
                type="submit"
                disabled={loading}
                className="btn btn-primary flex-1"
              >
                {loading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin mr-2" />
                    Analyzing...
                  </>
                ) : (
                  'Analyze KYC Profile'
                )}
              </button>
              <button
                type="button"
                onClick={handleReset}
                className="btn btn-secondary"
              >
                Reset
              </button>
            </div>
          </form>
        </div>

        {/* Results */}
        <div className="card">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Analysis Results</h2>
          
          {loading && (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
              <span className="ml-2 text-gray-600">Analyzing profile...</span>
            </div>
          )}

          {analysisResult && !loading && (
            <div className="space-y-6">
              {/* Risk Summary */}
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-medium text-gray-900">Risk Assessment</h3>
                  <RiskLevelBadge level={analysisResult.risk_level} />
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Risk Score</span>
                  <span className="text-lg font-semibold text-gray-900">
                    {analysisResult.risk_score}/100
                  </span>
                </div>
              </div>

              {/* Risk Factors */}
              {analysisResult.risk_factors && analysisResult.risk_factors.length > 0 && (
                <div>
                  <h3 className="text-sm font-medium text-gray-900 mb-2">Risk Factors</h3>
                  <ul className="space-y-1">
                    {analysisResult.risk_factors.map((factor, index) => (
                      <li key={index} className="flex items-start">
                        <AlertCircle className="h-4 w-4 text-warning-500 mr-2 mt-0.5 flex-shrink-0" />
                        <span className="text-sm text-gray-700">{factor}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Recommendations */}
              {analysisResult.recommendations && analysisResult.recommendations.length > 0 && (
                <div>
                  <h3 className="text-sm font-medium text-gray-900 mb-2">Recommendations</h3>
                  <ul className="space-y-1">
                    {analysisResult.recommendations.map((recommendation, index) => (
                      <li key={index} className="flex items-start">
                        <CheckCircle className="h-4 w-4 text-success-500 mr-2 mt-0.5 flex-shrink-0" />
                        <span className="text-sm text-gray-700">{recommendation}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Compliance Notes */}
              {analysisResult.compliance_notes && (
                <div>
                  <h3 className="text-sm font-medium text-gray-900 mb-2">Compliance Notes</h3>
                  <p className="text-sm text-gray-700 bg-blue-50 p-3 rounded-lg">
                    {analysisResult.compliance_notes}
                  </p>
                </div>
              )}

              {/* Analysis Summary */}
              {analysisResult.analysis_summary && (
                <div>
                  <h3 className="text-sm font-medium text-gray-900 mb-2">Analysis Summary</h3>
                  <p className="text-sm text-gray-700 bg-gray-50 p-3 rounded-lg">
                    {analysisResult.analysis_summary}
                  </p>
                </div>
              )}

              {/* Metadata */}
              <div className="border-t pt-4">
                <div className="grid grid-cols-2 gap-4 text-xs text-gray-500">
                  <div>
                    <span className="font-medium">Analysis ID:</span>
                    <br />
                    {analysisResult.analysis_id}
                  </div>
                  <div>
                    <span className="font-medium">Timestamp:</span>
                    <br />
                    {new Date(analysisResult.timestamp).toLocaleString()}
                  </div>
                </div>
              </div>
            </div>
          )}

          {!analysisResult && !loading && (
            <div className="text-center py-8 text-gray-500">
              <UserCheck className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>Submit customer information to begin KYC analysis</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
