'use client'

import { useRouter } from 'next/navigation'
import { SpiritualTask } from '@/lib/types'
import {
  formatDateTime,
  isOverdue,
  getPriorityColor,
  getCategoryBadgeColor,
  truncateText,
  parseTags,
  getRecurrenceLabel,
} from '@/lib/utils'

interface TaskCardProps {
  task: SpiritualTask
  onEdit?: (task: SpiritualTask) => void
  onComplete?: (taskId: number) => void
  onDelete?: (taskId: number) => void
}

export default function TaskCard({ task, onEdit, onComplete, onDelete }: TaskCardProps) {
  const router = useRouter()

  const handleCardClick = (e: React.MouseEvent) => {
    // Don't navigate if clicking on action buttons
    if ((e.target as HTMLElement).closest('button')) {
      return
    }
    router.push(`/tasks/${task.id}`)
  }

  const handleComplete = (e: React.MouseEvent) => {
    e.stopPropagation()
    if (onComplete) {
      onComplete(task.id)
    }
  }

  const handleEdit = (e: React.MouseEvent) => {
    e.stopPropagation()
    if (onEdit) {
      onEdit(task)
    }
  }

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation()
    if (onDelete && confirm('Are you sure you want to delete this task?')) {
      onDelete(task.id)
    }
  }

  const tags = parseTags(task.tags)
  const overdue = !task.completed && isOverdue(task.due_datetime || null)

  return (
    <div
      onClick={handleCardClick}
      className={`card-dark hover:border-salaat-orange/50 transition-all cursor-pointer ${
        task.completed ? 'opacity-75' : ''
      } ${overdue ? 'border-l-4 border-red-500' : ''}`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <h3 className={`text-lg font-semibold flex-1 ${task.completed ? 'line-through text-gray-500' : 'text-white'}`}>
          {task.title}
        </h3>
        {task.completed && (
          <span className="ml-2 text-green-500">
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clipRule="evenodd"
              />
            </svg>
          </span>
        )}
      </div>

      {/* Description */}
      {task.description && (
        <p className="text-gray-400 text-sm mb-3">{truncateText(task.description, 100)}</p>
      )}

      {/* Badges */}
      <div className="flex flex-wrap gap-2 mb-3">
        <span className={`px-3 py-1 text-xs font-medium rounded-full ${getCategoryBadgeColor(task.category)}`}>
          {task.category}
        </span>
        <span className={`px-3 py-1 text-xs font-medium rounded-full ${getPriorityColor(task.priority)}`}>
          {task.priority}
        </span>
        {task.recurrence !== 'None' && (
          <span className="px-3 py-1 text-xs font-medium rounded-full bg-salaat-orange/20 text-salaat-orange border border-salaat-orange/30">
            {getRecurrenceLabel(task.recurrence)}
          </span>
        )}
      </div>

      {/* Tags */}
      {tags.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-3">
          {tags.map((tag, index) => (
            <span key={index} className="px-2 py-1 text-xs bg-[#2A2A2A] text-gray-300 rounded">
              #{tag}
            </span>
          ))}
        </div>
      )}

      {/* Masjid */}
      {task.masjid && (
        <div className="flex items-center text-sm text-gray-400 mb-3">
          <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
              clipRule="evenodd"
            />
          </svg>
          <span>{task.masjid.name}</span>
        </div>
      )}

      {/* Due Date */}
      {task.due_datetime && (
        <div className="flex items-center text-sm mb-4">
          <svg className="w-4 h-4 mr-1 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
              clipRule="evenodd"
            />
          </svg>
          <span className={overdue ? 'text-red-400 font-semibold' : 'text-gray-400'}>
            {overdue && 'Overdue: '}
            {formatDateTime(task.due_datetime)}
          </span>
        </div>
      )}

      {/* Action Buttons */}
      {(onComplete || onEdit || onDelete) && (
        <div className="flex gap-2 mt-4 pt-4 border-t border-[#2A2A2A]">
          {onComplete && (
            <button
              onClick={handleComplete}
              className={`flex-1 px-3 py-2 text-sm font-medium rounded transition-colors ${
                task.completed
                  ? 'bg-[#2A2A2A] text-gray-300 hover:bg-[#353535]'
                  : 'bg-green-900/30 text-green-400 hover:bg-green-900/50 border border-green-800'
              }`}
            >
              {task.completed ? 'Mark Incomplete' : 'Mark Complete'}
            </button>
          )}
          {onEdit && (
            <button
              onClick={handleEdit}
              className="flex-1 px-3 py-2 text-sm font-medium text-salaat-orange bg-salaat-orange/10 rounded hover:bg-salaat-orange/20 border border-salaat-orange/30 transition-colors"
            >
              Edit
            </button>
          )}
          {onDelete && (
            <button
              onClick={handleDelete}
              className="px-3 py-2 text-sm font-medium text-red-400 bg-red-900/30 rounded hover:bg-red-900/50 border border-red-800 transition-colors"
            >
              Delete
            </button>
          )}
        </div>
      )}
    </div>
  )
}
