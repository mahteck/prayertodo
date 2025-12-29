/**
 * Utility functions for SalaatFlow frontend
 * Date formatting, color helpers, and common logic
 */

import { format, parseISO, isPast } from 'date-fns'
import { Priority, TaskCategory, Recurrence } from './types'

/**
 * Format ISO date string to readable format
 * @param dateString - ISO date string (e.g., "2025-12-27")
 * @returns Formatted date (e.g., "Dec 27, 2025")
 */
export function formatDate(dateString: string): string {
  try {
    const date = parseISO(dateString)
    return format(date, 'MMM dd, yyyy')
  } catch (error) {
    return dateString
  }
}

/**
 * Format ISO datetime string to readable format
 * @param dateString - ISO datetime string
 * @returns Formatted datetime (e.g., "Dec 27, 2025 3:30 PM")
 */
export function formatDateTime(dateString: string): string {
  try {
    const date = parseISO(dateString)
    return format(date, 'MMM dd, yyyy h:mm a')
  } catch (error) {
    return dateString
  }
}

/**
 * Check if a task due date is overdue
 * @param dueDate - ISO datetime string or null
 * @returns true if overdue, false otherwise
 */
export function isOverdue(dueDate: string | null): boolean {
  if (!dueDate) return false
  try {
    const date = parseISO(dueDate)
    return isPast(date)
  } catch (error) {
    return false
  }
}

/**
 * Get Tailwind CSS color classes for task priority
 * @param priority - Task priority level
 * @returns Tailwind CSS classes for background and text color
 */
export function getPriorityColor(priority: Priority): string {
  switch (priority) {
    case Priority.URGENT:
      return 'bg-red-100 text-red-800 border-red-200'
    case Priority.HIGH:
      return 'bg-orange-100 text-orange-800 border-orange-200'
    case Priority.MEDIUM:
      return 'bg-yellow-100 text-yellow-800 border-yellow-200'
    case Priority.LOW:
      return 'bg-green-100 text-green-800 border-green-200'
    default:
      return 'bg-gray-100 text-gray-800 border-gray-200'
  }
}

/**
 * Get Tailwind CSS color classes for task category badge
 * @param category - Task category
 * @returns Tailwind CSS classes for background and text color
 */
export function getCategoryBadgeColor(category: TaskCategory): string {
  switch (category) {
    case TaskCategory.FARZ:
      return 'bg-purple-100 text-purple-800 border-purple-200'
    case TaskCategory.SUNNAH:
      return 'bg-blue-100 text-blue-800 border-blue-200'
    case TaskCategory.NAFL:
      return 'bg-teal-100 text-teal-800 border-teal-200'
    case TaskCategory.DEED:
      return 'bg-emerald-100 text-emerald-800 border-emerald-200'
    case TaskCategory.OTHER:
      return 'bg-gray-100 text-gray-800 border-gray-200'
    default:
      return 'bg-gray-100 text-gray-800 border-gray-200'
  }
}

/**
 * Get human-readable label for recurrence pattern
 * @param recurrence - Recurrence enum value
 * @returns Human-readable string
 */
export function getRecurrenceLabel(recurrence: Recurrence): string {
  switch (recurrence) {
    case Recurrence.NONE:
      return 'Once'
    case Recurrence.DAILY:
      return 'Every day'
    case Recurrence.WEEKLY:
      return 'Every week'
    case Recurrence.MONTHLY:
      return 'Every month'
    default:
      return 'Once'
  }
}

/**
 * Truncate text to specified length with ellipsis
 * @param text - Text to truncate
 * @param maxLength - Maximum length before truncation
 * @returns Truncated text with "..." if needed
 */
export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

/**
 * Parse comma-separated tags string into array
 * @param tags - Comma-separated tags string
 * @returns Array of tag strings
 */
export function parseTags(tags: string | null | undefined): string[] {
  if (!tags) return []
  return tags.split(',').map(tag => tag.trim()).filter(tag => tag.length > 0)
}

/**
 * Join array of tags into comma-separated string
 * @param tags - Array of tag strings
 * @returns Comma-separated tags string
 */
export function joinTags(tags: string[]): string {
  return tags.join(', ')
}

/**
 * Get icon name for task category (for UI rendering)
 * @param category - Task category
 * @returns Icon identifier string
 */
export function getCategoryIcon(category: TaskCategory): string {
  switch (category) {
    case TaskCategory.FARZ:
      return 'required'
    case TaskCategory.SUNNAH:
      return 'recommended'
    case TaskCategory.NAFL:
      return 'voluntary'
    case TaskCategory.DEED:
      return 'good-deed'
    case TaskCategory.OTHER:
      return 'other'
    default:
      return 'other'
  }
}
