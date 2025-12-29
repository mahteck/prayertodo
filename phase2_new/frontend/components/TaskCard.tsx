'use client'

import { SpiritualTask } from '@/lib/types'
import { format } from 'date-fns'

interface TaskCardProps {
  task: SpiritualTask
  onToggleComplete: (id: number) => void
  onEdit: (id: number) => void
  onDelete: (id: number) => void
}

export default function TaskCard({ task, onToggleComplete, onEdit, onDelete }: TaskCardProps) {
  const getCategoryIcon = (category: string): string => {
    switch (category) {
      case 'Farz': return '🕌'
      case 'Sunnah': return '📿'
      case 'Nafl': return '✨'
      case 'Deed': return '🤲'
      default: return '📝'
    }
  }

  const getCategoryColor = (category: string): string => {
    switch (category) {
      case 'Farz': return 'bg-red-100 text-red-800 border-red-200'
      case 'Sunnah': return 'bg-green-100 text-green-800 border-green-200'
      case 'Nafl': return 'bg-blue-100 text-blue-800 border-blue-200'
      case 'Deed': return 'bg-purple-100 text-purple-800 border-purple-200'
      default: return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const getPriorityColor = (priority: string): string => {
    switch (priority) {
      case 'Urgent': return 'bg-red-100 text-red-800 border-red-200'
      case 'High': return 'bg-orange-100 text-orange-800 border-orange-200'
      case 'Medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'Low': return 'bg-green-100 text-green-800 border-green-200'
      default: return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  return (
    <div className={`bg-white rounded-lg shadow-sm border p-4 transition-all hover:shadow-md ${
      task.completed ? 'opacity-75' : ''
    }`}>
      <div className="flex items-start space-x-3">
        {/* Checkbox */}
        <input
          type="checkbox"
          checked={task.completed}
          onChange={() => onToggleComplete(task.id)}
          className="mt-1 h-5 w-5 text-islamic-green rounded focus:ring-islamic-green cursor-pointer"
        />

        {/* Content */}
        <div className="flex-1 min-w-0">
          {/* Title */}
          <h3 className={`text-lg font-semibold mb-2 ${
            task.completed ? 'line-through text-gray-500' : 'text-gray-900'
          }`}>
            {getCategoryIcon(task.category)} {task.title}
          </h3>

          {/* Description */}
          {task.description && (
            <p className={`text-sm mb-3 ${
              task.completed ? 'text-gray-400' : 'text-gray-600'
            }`}>
              {task.description}
            </p>
          )}

          {/* Badges */}
          <div className="flex flex-wrap gap-2 mb-3">
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${getCategoryColor(task.category)}`}>
              {task.category}
            </span>
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${getPriorityColor(task.priority)}`}>
              {task.priority}
            </span>
            {task.recurrence !== 'None' && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800 border border-indigo-200">
                🔄 {task.recurrence}
              </span>
            )}
          </div>

          {/* Metadata */}
          <div className="flex flex-wrap gap-3 text-xs text-gray-500 mb-2">
            {task.due_datetime && (
              <span className="flex items-center">
                📅 Due: {format(new Date(task.due_datetime), 'MMM d, yyyy h:mm a')}
              </span>
            )}
            {task.masjid && (
              <span className="flex items-center">
                🕌 {task.masjid.name}
              </span>
            )}
          </div>

          {/* Tags */}
          {task.tags && (
            <div className="flex flex-wrap gap-1 mb-2">
              {task.tags.split(',').map((tag, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-700"
                >
                  #{tag.trim()}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex flex-col space-y-2">
          <button
            onClick={() => onEdit(task.id)}
            className="text-blue-600 hover:text-blue-800 p-1"
            title="Edit task"
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
          <button
            onClick={() => onDelete(task.id)}
            className="text-red-600 hover:text-red-800 p-1"
            title="Delete task"
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  )
}
