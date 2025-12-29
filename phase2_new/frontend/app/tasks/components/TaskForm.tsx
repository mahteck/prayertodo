'use client'

import { useState, useEffect } from 'react'
import { TaskFormData, SpiritualTask, TaskCategory, Priority, Recurrence, Masjid } from '@/lib/types'
import api from '@/lib/api'
import { joinTags, parseTags } from '@/lib/utils'

interface TaskFormProps {
  initialData?: SpiritualTask | null
  onSubmit: (data: TaskFormData) => Promise<void>
  onCancel: () => void
  isLoading?: boolean
  preSelectedMasjidId?: number
}

export default function TaskForm({ initialData, onSubmit, onCancel, isLoading = false, preSelectedMasjidId }: TaskFormProps) {
  const [masjids, setMasjids] = useState<Masjid[]>([])
  const [loadingMasjids, setLoadingMasjids] = useState(true)
  const [errors, setErrors] = useState<Record<string, string>>({})

  const [formData, setFormData] = useState<TaskFormData>({
    title: initialData?.title || '',
    description: initialData?.description || '',
    category: initialData?.category || TaskCategory.OTHER,
    priority: initialData?.priority || Priority.MEDIUM,
    tags: initialData?.tags || '',
    masjid_id: initialData?.masjid_id || preSelectedMasjidId || null,
    due_datetime: initialData?.due_datetime || null,
    recurrence: initialData?.recurrence || Recurrence.NONE,
  })

  // Fetch masjids for dropdown
  useEffect(() => {
    const fetchMasjids = async () => {
      try {
        const data = await api.getMasjids()
        setMasjids(data)
      } catch (error) {
        console.error('Error fetching masjids:', error)
      } finally {
        setLoadingMasjids(false)
      }
    }
    fetchMasjids()
  }, [])

  // Update masjid_id when preSelectedMasjidId changes
  useEffect(() => {
    if (preSelectedMasjidId && !initialData) {
      setFormData(prev => ({ ...prev, masjid_id: preSelectedMasjidId }))
    }
  }, [preSelectedMasjidId, initialData])

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {}

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required'
    }

    if (formData.description && formData.description.length > 2000) {
      newErrors.description = 'Description must be less than 2000 characters'
    }

    if (formData.due_datetime) {
      const dueDate = new Date(formData.due_datetime)
      const now = new Date()
      if (dueDate < now && !initialData) {
        newErrors.due_datetime = 'Due date must be in the future'
      }
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validate()) {
      return
    }

    try {
      await onSubmit(formData)
    } catch (error) {
      console.error('Error submitting form:', error)
    }
  }

  const handleChange = (field: keyof TaskFormData, value: any) => {
    setFormData({ ...formData, [field]: value })
    // Clear error for this field when user starts typing
    if (errors[field]) {
      setErrors({ ...errors, [field]: '' })
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Title */}
      <div>
        <label htmlFor="title" className="form-label">
          Title <span className="text-red-500">*</span>
        </label>
        <input
          id="title"
          type="text"
          value={formData.title}
          onChange={(e) => handleChange('title', e.target.value)}
          disabled={isLoading}
          className={`input-field w-full ${
            errors.title ? 'border-red-500 focus:ring-red-500' : ''
          } ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
          placeholder="Enter task title"
        />
        {errors.title && <p className="mt-1 text-sm text-red-400">{errors.title}</p>}
      </div>

      {/* Description */}
      <div>
        <label htmlFor="description" className="form-label">
          Description
        </label>
        <textarea
          id="description"
          value={formData.description || ''}
          onChange={(e) => handleChange('description', e.target.value)}
          disabled={isLoading}
          rows={4}
          maxLength={2000}
          className={`textarea-field w-full ${
            errors.description ? 'border-red-500 focus:ring-red-500' : ''
          } ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
          placeholder="Describe the task (optional)"
        />
        <div className="mt-1 flex justify-between">
          {errors.description && <p className="text-sm text-red-400">{errors.description}</p>}
          <p className="text-sm text-gray-400 ml-auto">{formData.description?.length || 0}/2000</p>
        </div>
      </div>

      {/* Category and Priority */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="category" className="form-label">
            Category <span className="text-red-500">*</span>
          </label>
          <select
            id="category"
            value={formData.category}
            onChange={(e) => handleChange('category', e.target.value as TaskCategory)}
            disabled={isLoading}
            className={`select-field w-full ${
              isLoading ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          >
            <option value={TaskCategory.FARZ}>Farz (Obligatory)</option>
            <option value={TaskCategory.SUNNAH}>Sunnah</option>
            <option value={TaskCategory.NAFL}>Nafl (Voluntary)</option>
            <option value={TaskCategory.DEED}>Good Deed</option>
            <option value={TaskCategory.OTHER}>Other</option>
          </select>
        </div>

        <div>
          <label htmlFor="priority" className="form-label">
            Priority <span className="text-red-500">*</span>
          </label>
          <select
            id="priority"
            value={formData.priority}
            onChange={(e) => handleChange('priority', e.target.value as Priority)}
            disabled={isLoading}
            className={`select-field w-full ${
              isLoading ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          >
            <option value={Priority.URGENT}>Urgent</option>
            <option value={Priority.HIGH}>High</option>
            <option value={Priority.MEDIUM}>Medium</option>
            <option value={Priority.LOW}>Low</option>
          </select>
        </div>
      </div>

      {/* Tags */}
      <div>
        <label htmlFor="tags" className="form-label">
          Tags
        </label>
        <input
          id="tags"
          type="text"
          value={formData.tags || ''}
          onChange={(e) => handleChange('tags', e.target.value)}
          disabled={isLoading}
          className={`input-field w-full ${
            isLoading ? 'opacity-50 cursor-not-allowed' : ''
          }`}
          placeholder="prayer, quran, charity (comma-separated)"
        />
        <p className="mt-1 text-sm text-gray-400">Enter tags separated by commas</p>
      </div>

      {/* Masjid and Recurrence */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="masjid" className="form-label">
            Masjid (Optional)
          </label>
          <select
            id="masjid"
            value={formData.masjid_id || ''}
            onChange={(e) => handleChange('masjid_id', e.target.value ? parseInt(e.target.value) : null)}
            disabled={isLoading || loadingMasjids}
            className={`select-field w-full ${
              isLoading || loadingMasjids ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          >
            <option value="">No masjid</option>
            {Array.isArray(masjids) && masjids.map((masjid) => (
              <option key={masjid.id} value={masjid.id}>
                {masjid.name} {masjid.area && `(${masjid.area})`}
              </option>
            ))}
          </select>
          {loadingMasjids && <p className="mt-1 text-sm text-gray-400">Loading masjids...</p>}
        </div>

        <div>
          <label htmlFor="recurrence" className="form-label">
            Recurrence
          </label>
          <select
            id="recurrence"
            value={formData.recurrence}
            onChange={(e) => handleChange('recurrence', e.target.value as Recurrence)}
            disabled={isLoading}
            className={`select-field w-full ${
              isLoading ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          >
            <option value={Recurrence.NONE}>Once</option>
            <option value={Recurrence.DAILY}>Daily</option>
            <option value={Recurrence.WEEKLY}>Weekly</option>
            <option value={Recurrence.MONTHLY}>Monthly</option>
          </select>
        </div>
      </div>

      {/* Due Date & Time */}
      <div>
        <label htmlFor="dueDateTime" className="form-label">
          Due Date & Time (Optional)
        </label>
        <input
          id="dueDateTime"
          type="datetime-local"
          value={formData.due_datetime || ''}
          onChange={(e) => handleChange('due_datetime', e.target.value || null)}
          disabled={isLoading}
          className={`input-field w-full ${
            errors.due_datetime ? 'border-red-500 focus:ring-red-500' : ''
          } ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
        />
        {errors.due_datetime && <p className="mt-1 text-sm text-red-400">{errors.due_datetime}</p>}
      </div>

      {/* Action Buttons */}
      <div className="flex gap-4 pt-4 border-t border-[#2A2A2A]">
        <button
          type="submit"
          disabled={isLoading}
          className={`btn-primary flex-1 ${
            isLoading ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Saving...
            </span>
          ) : initialData ? (
            'Update Task'
          ) : (
            'Create Task'
          )}
        </button>
        <button
          type="button"
          onClick={onCancel}
          disabled={isLoading}
          className={`btn-secondary ${
            isLoading ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          Cancel
        </button>
      </div>
    </form>
  )
}
