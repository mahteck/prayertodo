'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import api from '@/lib/api'
import { SpiritualTask, Masjid, TaskFilters } from '@/lib/types'
import TaskList from './components/TaskList'
import TaskFiltersComponent from './components/TaskFilters'

export default function TasksPage() {
  const router = useRouter()

  const [tasks, setTasks] = useState<SpiritualTask[]>([])
  const [masjids, setMasjids] = useState<Masjid[]>([])
  const [filters, setFilters] = useState<TaskFilters>({
    sort_by: 'created_at',
    sort_order: 'desc',
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Fetch tasks whenever filters change
  useEffect(() => {
    fetchTasks()
  }, [filters])

  // Fetch masjids for filter dropdown (once on mount)
  useEffect(() => {
    fetchMasjids()
  }, [])

  const fetchTasks = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await api.getTasks(filters)
      setTasks(data)
    } catch (err) {
      console.error('Error fetching tasks:', err)
      setError('Failed to load tasks. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const fetchMasjids = async () => {
    try {
      const data = await api.getMasjids()
      setMasjids(data.masjids || [])
    } catch (err) {
      console.error('Error fetching masjids:', err)
    }
  }

  const handleFilterChange = (newFilters: TaskFilters) => {
    setFilters(newFilters)
  }

  const handleEdit = (task: SpiritualTask) => {
    router.push(`/tasks/${task.id}/edit`)
  }

  const handleComplete = async (taskId: number) => {
    try {
      const task = tasks.find((t) => t.id === taskId)
      if (!task) return

      if (task.completed) {
        await api.uncompleteTask(taskId)
      } else {
        await api.completeTask(taskId)
      }

      // Refresh task list
      await fetchTasks()
    } catch (err) {
      console.error('Error updating task:', err)
      alert('Failed to update task. Please try again.')
    }
  }

  const handleDelete = async (taskId: number) => {
    try {
      await api.deleteTask(taskId)
      // Refresh task list
      await fetchTasks()
    } catch (err) {
      console.error('Error deleting task:', err)
      alert('Failed to delete task. Please try again.')
    }
  }

  const handleNewTask = () => {
    router.push('/tasks/new')
  }

  return (
    <div className="min-h-screen page-gradient">
      {/* Page Header */}
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white">Tasks</h1>
            <p className="text-gray-300 mt-1">
              Manage your spiritual tasks and activities
            </p>
          </div>
          <button
            onClick={handleNewTask}
            className="btn-primary flex items-center"
          >
            <svg
              className="w-5 h-5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 6v6m0 0v6m0-6h6m-6 0H6"
              />
            </svg>
            New Task
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 pb-8">
        {/* Filters */}
        <TaskFiltersComponent
          filters={filters}
          onFilterChange={handleFilterChange}
          masjids={masjids}
        />

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center items-center py-16">
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
              <p className="text-gray-300">Loading tasks...</p>
            </div>
          </div>
        )}

        {/* Error State */}
        {error && !loading && (
          <div className="bg-red-900/20 border border-red-800 rounded-lg p-6 mb-6">
            <div className="flex items-center">
              <svg
                className="w-6 h-6 text-red-400 mr-3"
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
              <div>
                <h3 className="text-red-300 font-medium">Error Loading Tasks</h3>
                <p className="text-red-400 text-sm mt-1">{error}</p>
              </div>
            </div>
            <button
              onClick={fetchTasks}
              className="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
            >
              Try Again
            </button>
          </div>
        )}

        {/* Task List */}
        {!loading && !error && (
          <>
            {/* Task Count */}
            <div className="mb-4 text-sm text-gray-300">
              Showing {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}
            </div>

            {/* Tasks */}
            <TaskList
              tasks={tasks}
              onEdit={handleEdit}
              onComplete={handleComplete}
              onDelete={handleDelete}
            />
          </>
        )}
      </div>
    </div>
  )
}
