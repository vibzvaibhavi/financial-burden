import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { CreditCard, Loader2, AlertCircle, CheckCircle } from 'lucide-react'
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

export default function TransactionAnalysis() {
  const [analysisResult, setAnalysisResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const { register, handleSubmit, formState: { errors }, reset } = useForm()

  const onSubmit = async (data) => {
    try {
      setLoading(true)
      setAnalysisResult(null)
      
      const response = await analysisAPI.analyzeTransaction(data)
      setAnalysisResult(response.data)
      toast.success('Transaction analysis completed successfully!')
      
    } catch (error) {
      console.error('Transaction analysis error:', error)
      toast.error('Failed to analyze transaction')
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
        <h1 className="text-2xl font-bold text-gray-900">Transaction Analysis</h1>
        <p className="mt-1 text-sm text-gray-500">
          Analyze transactions for suspicious activity using Claude 3 Sonnet 4
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Form */}
        <div className="card">
          <div className="flex items-center mb-4">
            <CreditCard className="h-6 w-6 text-primary-600 mr-2" />
            <h2 className="text-lg font-medium text-gray-900">Transaction Information</h2>
          </div>
          
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="label">Transaction ID *</label>
              <input
                type="text"
                className="input"
                {...register('transaction_id', { required: 'Transaction ID is required' })}
                placeholder="Enter transaction ID"
              />
              {errors.transaction_id && (
                <p className="mt-1 text-sm text-danger-600">{errors.transaction_id.message}</p>
              )}
            </div>

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

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">Amount *</label>
                <input
                  type="number"
                  step="0.01"
                  className="input"
                  {...register('amount', { 
                    required: 'Amount is required',
                    min: { value: 0.01, message: 'Amount must be positive' }
                  })}
                  placeholder="0.00"
                />
                {errors.amount && (
                  <p className="mt-1 text-sm text-danger-600">{errors.amount.message}</p>
                )}
              </div>
              <div>
                <label className="label">Currency</label>
                <select className="input" {...register('currency')}>
                  <option value="USD">USD</option>
                  <option value="EUR">EUR</option>
                  <option value="GBP">GBP</option>
                  <option value="JPY">JPY</option>
                  <option value="CAD">CAD</option>
                  <option value="AUD">AUD</option>
                </select>
              </div>
            </div>

            <div>
              <label className="label">Transaction Type *</label>
              <select
                className="input"
                {...register('transaction_type', { required: 'Transaction type is required' })}
              >
                <option value="">Select transaction type</option>
                <option value="Wire Transfer">Wire Transfer</option>
                <option value="ACH Transfer">ACH Transfer</option>
                <option value="Cash Deposit">Cash Deposit</option>
                <option value="Cash Withdrawal">Cash Withdrawal</option>
                <option value="Check">Check</option>
                <option value="Credit Card">Credit Card</option>
                <option value="Debit Card">Debit Card</option>
                <option value="Cryptocurrency">Cryptocurrency</option>
                <option value="International Transfer">International Transfer</option>
                <option value="Other">Other</option>
              </select>
              {errors.transaction_type && (
                <p className="mt-1 text-sm text-danger-600">{errors.transaction_type.message}</p>
              )}
            </div>

            <div>
              <label className="label">Transaction Date *</label>
              <input
                type="datetime-local"
                className="input"
                {...register('date', { required: 'Transaction date is required' })}
              />
              {errors.date && (
                <p className="mt-1 text-sm text-danger-600">{errors.date.message}</p>
              )}
            </div>

            <div>
              <label className="label">Origin *</label>
              <input
                type="text"
                className="input"
                {...register('origin', { required: 'Origin is required' })}
                placeholder="Enter origin (account, institution, etc.)"
              />
              {errors.origin && (
                <p className="mt-1 text-sm text-danger-600">{errors.origin.message}</p>
              )}
            </div>

            <div>
              <label className="label">Destination *</label>
              <input
                type="text"
                className="input"
                {...register('destination', { required: 'Destination is required' })}
                placeholder="Enter destination (account, institution, etc.)"
              />
              {errors.destination && (
                <p className="mt-1 text-sm text-danger-600">{errors.destination.message}</p>
              )}
            </div>

            <div>
              <label className="label">Purpose *</label>
              <textarea
                className="input"
                rows={3}
                {...register('purpose', { required: 'Purpose is required' })}
                placeholder="Describe the purpose of this transaction"
              />
              {errors.purpose && (
                <p className="mt-1 text-sm text-danger-600">{errors.purpose.message}</p>
              )}
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
                  'Analyze Transaction'
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
              <span className="ml-2 text-gray-600">Analyzing transaction...</span>
            </div>
          )}

          {analysisResult && !loading && (
            <div className="space-y-6">
              {/* Suspicion Summary */}
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-medium text-gray-900">Suspicion Assessment</h3>
                  <RiskLevelBadge level={analysisResult.risk_level} />
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Suspicion Score</span>
                  <span className="text-lg font-semibold text-gray-900">
                    {analysisResult.risk_score}/100
                  </span>
                </div>
              </div>

              {/* Red Flags */}
              {analysisResult.risk_factors && analysisResult.risk_factors.length > 0 && (
                <div>
                  <h3 className="text-sm font-medium text-gray-900 mb-2">Red Flags</h3>
                  <ul className="space-y-1">
                    {analysisResult.risk_factors.map((flag, index) => (
                      <li key={index} className="flex items-start">
                        <AlertCircle className="h-4 w-4 text-danger-500 mr-2 mt-0.5 flex-shrink-0" />
                        <span className="text-sm text-gray-700">{flag}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* AML Concerns */}
              {analysisResult.compliance_notes && Array.isArray(analysisResult.compliance_notes) && analysisResult.compliance_notes.length > 0 && (
                <div>
                  <h3 className="text-sm font-medium text-gray-900 mb-2">AML Concerns</h3>
                  <ul className="space-y-1">
                    {analysisResult.compliance_notes.map((concern, index) => (
                      <li key={index} className="flex items-start">
                        <AlertCircle className="h-4 w-4 text-warning-500 mr-2 mt-0.5 flex-shrink-0" />
                        <span className="text-sm text-gray-700">{concern}</span>
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
              <CreditCard className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>Submit transaction information to begin analysis</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
