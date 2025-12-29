'use client'

import { SpiritualTask } from '@/lib/types'
import TaskCard from './TaskCard'

interface TaskListProps {
  tasks: SpiritualTask[]
  onEdit: (task: SpiritualTask) => void
  onComplete: (taskId: number) => void
  onDelete: (taskId: number) => void
}

export default function TaskList({ tasks, onEdit, onComplete, onDelete }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 px-4">
        <div className="text-gray-600 mb-4">
          <svg className="w-24 h-24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
        </div>
        <h3 className="text-xl font-medium text-white mb-2">No tasks found</h3>
        <p className="text-gray-400 text-center max-w-md">
          No tasks match your current filters. Try adjusting your search criteria or create a new task to get started.
        </p>
      </div>
    )
  }

  return (
    <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onEdit={onEdit}
          onComplete={onComplete}
          onDelete={onDelete}
        />
      ))}
    </div>
  )
}
