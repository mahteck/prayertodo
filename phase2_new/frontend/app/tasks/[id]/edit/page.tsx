'use client'

import { useState, useEffect } from 'react'
import { useRouter, useParams } from 'next/navigation'
import api from '@/lib/api'
import { TaskFormData, SpiritualTask } from '@/lib/types'
import TaskForm from '../../components/TaskForm'

export default function EditTaskPage() {
  const router = useRouter()
  const params = useParams()
  const taskId = parseInt(params.id as string)

  const [task, setTask] = useState<SpiritualTask | null>(null)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (taskId) {
      fetchTask()
    }
  }, [taskId])

  const fetchTask = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await api.getTask(taskId)
      setTask(data)
    } catch (err: any) {
      console.error('Error fetching task:', err)
      if (err.response?.status === 404) {
        setError('Task not found')
      } else {
        setError('Failed to load task. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (formData: TaskFormData) => {
    try {
      setSubmitting(true)
      setError(null)

      await api.updateTask(taskId, formData)

      // Success - navigate to task detail
      router.push(`/tasks/${taskId}`)
    } catch (err: any) {
      console.error('Error updating task:', err)
      // Handle validation errors (array of objects)
      if (err.response?.data?.detail && Array.isArray(err.response.data.detail)) {
        const errorMessages = err.response.data.detail.map((e: any) => e.msg || e.message).join(', ')
        setError(errorMessages || 'Validation failed. Please check your input.')
      } else if (typeof err.response?.data?.detail === 'string') {
        setError(err.response.data.detail)
      } else {
        setError('Failed to update task. Please try again.')
      }
      setSubmitting(false)
    }
  }

  const handleCancel = () => {
    router.push(`/tasks/${taskId}`)
  }

  if (loading) {
    return (
      <div className="min-h-screen page-gradient flex items-center justify-center">
        <div className="flex flex-col items-center">
          <svg
            className="animate-spin h-12 w-12 text-salaat-orange mb-4"
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
          <p className="text-gray-300">Loading task...</p>
        </div>
      </div>
    )
  }

  if (error || !task) {
    return (
      <div className="min-h-screen page-gradient">
        <div className="container mx-auto px-4 py-16">
          <div className="max-w-2xl mx-auto card-dark rounded-lg shadow-md p-8 text-center">
            <svg
              className="w-16 h-16 text-red-400 mx-auto mb-4"
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
            <h2 className="text-2xl font-bold text-white mb-2">Task Not Found</h2>
            <p className="text-gray-300 mb-6">
              {error || 'The task you are trying to edit does not exist or has been deleted.'}
            </p>
            <button
              onClick={() => router.push('/tasks')}
              className="inline-block px-6 py-3 btn-primary text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Back to Tasks
            </button>
          </div>
        </div>
      </div>
    )
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
            <h1 className="text-3xl font-bold text-white">Edit Task</h1>
            <p className="text-gray-300 mt-1">Update task information</p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-3xl mx-auto">
          {/* Error Message */}
          {error && !loading && (
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
          <div className="card-dark rounded-lg shadow-md p-8">
            <TaskForm
              initialData={task}
              onSubmit={handleSubmit}
              onCancel={handleCancel}
              isLoading={submitting}
            />
          </div>
        </div>
      </div>
    </div>
  )
}
