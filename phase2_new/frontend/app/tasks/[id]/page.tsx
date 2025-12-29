'use client'

import { useState, useEffect } from 'react'
import { useRouter, useParams } from 'next/navigation'
import Link from 'next/link'
import api from '@/lib/api'
import { SpiritualTask } from '@/lib/types'
import {
  formatDateTime,
  isOverdue,
  getPriorityColor,
  getCategoryBadgeColor,
  parseTags,
  getRecurrenceLabel,
  formatDate,
} from '@/lib/utils'

export default function TaskDetailPage() {
  const router = useRouter()
  const params = useParams()
  const taskId = parseInt(params.id as string)

  const [task, setTask] = useState<SpiritualTask | null>(null)
  const [loading, setLoading] = useState(true)
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

  const handleToggleComplete = async () => {
    if (!task) return

    try {
      if (task.completed) {
        await api.uncompleteTask(taskId)
      } else {
        await api.completeTask(taskId)
      }
      // Refresh task
      await fetchTask()
    } catch (err) {
      console.error('Error updating task:', err)
      alert('Failed to update task. Please try again.')
    }
  }

  const handleEdit = () => {
    router.push(`/tasks/${taskId}/edit`)
  }

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task? This action cannot be undone.')) {
      return
    }

    try {
      await api.deleteTask(taskId)
      router.push('/tasks')
    } catch (err) {
      console.error('Error deleting task:', err)
      alert('Failed to delete task. Please try again.')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="flex flex-col items-center">
          <svg
            className="animate-spin h-12 w-12 text-indigo-600 mb-4"
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
          <p className="text-gray-600">Loading task...</p>
        </div>
      </div>
    )
  }

  if (error || !task) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="container mx-auto px-4 py-16">
          <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-8 text-center">
            <svg
              className="w-16 h-16 text-red-500 mx-auto mb-4"
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
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Task Not Found</h2>
            <p className="text-gray-600 mb-6">
              {error || 'The task you are looking for does not exist or has been deleted.'}
            </p>
            <Link
              href="/tasks"
              className="inline-block px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Back to Tasks
            </Link>
          </div>
        </div>
      </div>
    )
  }

  const tags = parseTags(task.tags)
  const overdue = !task.completed && isOverdue(task.due_datetime || null)

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center">
            <Link
              href="/tasks"
              className="mr-4 text-gray-600 hover:text-gray-800 focus:outline-none"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M15 19l-7-7 7-7"
                />
              </svg>
            </Link>
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-gray-800">Task Details</h1>
              <p className="text-gray-600 mt-1">View and manage task information</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Task Card */}
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            {/* Title Section */}
            <div className={`p-8 ${overdue ? 'border-l-4 border-red-500' : ''}`}>
              <div className="flex items-start justify-between mb-4">
                <h2
                  className={`text-3xl font-bold flex-1 ${
                    task.completed ? 'text-gray-500 line-through' : 'text-gray-800'
                  }`}
                >
                  {task.title}
                </h2>
                {task.completed && (
                  <span className="ml-4 text-green-600">
                    <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fillRule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </span>
                )}
              </div>

              {/* Badges */}
              <div className="flex flex-wrap gap-2 mb-6">
                <span
                  className={`px-3 py-1 text-sm font-medium rounded-full border ${getCategoryBadgeColor(
                    task.category
                  )}`}
                >
                  {task.category}
                </span>
                <span
                  className={`px-3 py-1 text-sm font-medium rounded-full border ${getPriorityColor(
                    task.priority
                  )}`}
                >
                  {task.priority} Priority
                </span>
                {task.recurrence !== 'None' && (
                  <span className="px-3 py-1 text-sm font-medium rounded-full border bg-indigo-100 text-indigo-800 border-indigo-200">
                    {getRecurrenceLabel(task.recurrence)}
                  </span>
                )}
                {task.completed && (
                  <span className="px-3 py-1 text-sm font-medium rounded-full border bg-green-100 text-green-800 border-green-200">
                    Completed
                  </span>
                )}
              </div>

              {/* Description */}
              {task.description && (
                <div className="mb-6">
                  <h3 className="text-sm font-semibold text-gray-700 mb-2">Description</h3>
                  <p className="text-gray-700 whitespace-pre-wrap">{task.description}</p>
                </div>
              )}

              {/* Details Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                {/* Due Date */}
                {task.due_datetime && (
                  <div>
                    <h3 className="text-sm font-semibold text-gray-700 mb-2">Due Date & Time</h3>
                    <div className="flex items-center">
                      <svg
                        className="w-5 h-5 mr-2 text-gray-500"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                          clipRule="evenodd"
                        />
                      </svg>
                      <span className={overdue ? 'text-red-600 font-semibold' : 'text-gray-700'}>
                        {overdue && 'Overdue: '}
                        {formatDateTime(task.due_datetime)}
                      </span>
                    </div>
                  </div>
                )}

                {/* Masjid */}
                {task.masjid && (
                  <div>
                    <h3 className="text-sm font-semibold text-gray-700 mb-2">Masjid</h3>
                    <Link
                      href={`/masjids/${task.masjid.id}`}
                      className="flex items-center text-indigo-600 hover:text-indigo-800"
                    >
                      <svg
                        className="w-5 h-5 mr-2"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
                          clipRule="evenodd"
                        />
                      </svg>
                      <span className="hover:underline">{task.masjid.name}</span>
                    </Link>
                  </div>
                )}

                {/* Completed At */}
                {task.completed_at && (
                  <div>
                    <h3 className="text-sm font-semibold text-gray-700 mb-2">Completed At</h3>
                    <p className="text-gray-700">{formatDateTime(task.completed_at)}</p>
                  </div>
                )}

                {/* Created */}
                <div>
                  <h3 className="text-sm font-semibold text-gray-700 mb-2">Created</h3>
                  <p className="text-gray-700">{formatDateTime(task.created_at)}</p>
                </div>

                {/* Updated */}
                <div>
                  <h3 className="text-sm font-semibold text-gray-700 mb-2">Last Updated</h3>
                  <p className="text-gray-700">{formatDateTime(task.updated_at)}</p>
                </div>
              </div>

              {/* Tags */}
              {tags.length > 0 && (
                <div>
                  <h3 className="text-sm font-semibold text-gray-700 mb-2">Tags</h3>
                  <div className="flex flex-wrap gap-2">
                    {tags.map((tag, index) => (
                      <span
                        key={index}
                        className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full"
                      >
                        #{tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="bg-gray-50 px-8 py-6 border-t border-gray-200">
              <div className="flex flex-wrap gap-3">
                <button
                  onClick={handleToggleComplete}
                  className={`flex-1 min-w-[200px] px-6 py-3 font-medium rounded-lg transition-colors ${
                    task.completed
                      ? 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      : 'bg-green-600 text-white hover:bg-green-700'
                  }`}
                >
                  {task.completed ? 'Mark as Incomplete' : 'Mark as Complete'}
                </button>
                <button
                  onClick={handleEdit}
                  className="flex-1 min-w-[200px] px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors"
                >
                  Edit Task
                </button>
                <button
                  onClick={handleDelete}
                  className="px-6 py-3 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 transition-colors"
                >
                  Delete Task
                </button>
              </div>
            </div>
          </div>

          {/* Back Link */}
          <div className="mt-6 text-center">
            <Link href="/tasks" className="text-indigo-600 hover:text-indigo-800 font-medium">
              ← Back to Tasks
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
