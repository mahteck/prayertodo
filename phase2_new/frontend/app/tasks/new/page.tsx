'use client'

import { useState, useEffect, Suspense } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import api from '@/lib/api'
import { TaskFormData } from '@/lib/types'
import TaskForm from '../components/TaskForm'

function NewTaskContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [preSelectedMasjidId, setPreSelectedMasjidId] = useState<number | undefined>(undefined)

  useEffect(() => {
    // Get masjid ID from URL query parameter
    const masjidParam = searchParams.get('masjid')
    if (masjidParam) {
      const masjidId = parseInt(masjidParam)
      if (!isNaN(masjidId)) {
        setPreSelectedMasjidId(masjidId)
      }
    }
  }, [searchParams])

  const handleSubmit = async (formData: TaskFormData) => {
    try {
      setLoading(true)
      setError(null)

      await api.createTask(formData)

      // Success - navigate to tasks list
      router.push('/tasks')
    } catch (err: any) {
      console.error('Error creating task:', err)
      // Handle validation errors (array of objects)
      if (err.response?.data?.detail && Array.isArray(err.response.data.detail)) {
        const errorMessages = err.response.data.detail.map((e: any) => e.msg || e.message).join(', ')
        setError(errorMessages || 'Validation failed. Please check your input.')
      } else if (typeof err.response?.data?.detail === 'string') {
        setError(err.response.data.detail)
      } else {
        setError('Failed to create task. Please try again.')
      }
      setLoading(false)
    }
  }

  const handleCancel = () => {
    router.push('/tasks')
  }

  return (
    <div className="min-h-screen page-gradient">
      {/* Header */}
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center">
          <button
            onClick={handleCancel}
            className="mr-4 text-gray-300 hover:text-salaat-orange focus:outline-none transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 19l-7-7 7-7"
              />
            </svg>
          </button>
          <div>
            <h1 className="text-3xl font-bold text-white">Create New Task</h1>
            <p className="text-gray-300 mt-1">Add a new spiritual task or activity</p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-3xl mx-auto">
          {/* Error Message */}
          {error && (
            <div className="bg-red-900/20 border border-red-800 rounded-lg p-4 mb-6">
              <div className="flex items-center">
                <svg
                  className="w-5 h-5 text-red-400 mr-2"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <p className="text-red-300">{error}</p>
              </div>
            </div>
          )}

          {/* Task Form */}
          <div className="card-dark p-8">
            <TaskForm
              onSubmit={handleSubmit}
              onCancel={handleCancel}
              isLoading={loading}
              preSelectedMasjidId={preSelectedMasjidId}
            />
          </div>
        </div>
      </div>
    </div>
  )
}

export default function NewTaskPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen page-gradient flex items-center justify-center">
        <div className="text-center">
          <svg
            className="animate-spin h-12 w-12 text-salaat-orange mx-auto mb-4"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          <p className="text-gray-300">Loading...</p>
        </div>
      </div>
    }>
      <NewTaskContent />
    </Suspense>
  )
}
