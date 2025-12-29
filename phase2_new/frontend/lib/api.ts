/**
 * API client for SalaatFlow backend
 * Uses Axios for HTTP requests
 */

import axios, { AxiosInstance } from 'axios'
import type {
  SpiritualTask,
  Masjid,
  DailyHadith,
  TaskFilters,
  MasjidFilters,
  TaskStatistics,
  TaskFormData,
  MasjidFormData,
} from './types'

// API Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const API_VERSION = '/api/v1'

// Create Axios instance
const axiosInstance: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}${API_VERSION}`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// API methods
const api = {
  // ==================== TASKS ====================

  // Get all tasks with optional filters
  getTasks: async (filters?: TaskFilters): Promise<SpiritualTask[]> => {
    const response = await axiosInstance.get<SpiritualTask[]>('/tasks', {
      params: filters,
    })
    return response.data
  },

  // Get single task by ID
  getTask: async (id: number): Promise<SpiritualTask> => {
    const response = await axiosInstance.get<SpiritualTask>(`/tasks/${id}`)
    return response.data
  },

  // Get upcoming tasks
  getUpcomingTasks: async (days: number = 7, limit: number = 10): Promise<SpiritualTask[]> => {
    const response = await axiosInstance.get<SpiritualTask[]>('/tasks/upcoming', {
      params: { days, limit },
    })
    return response.data
  },

  // Get task statistics
  getTaskStatistics: async (): Promise<TaskStatistics> => {
    const response = await axiosInstance.get<TaskStatistics>('/tasks/stats/summary')
    return response.data
  },

  // Create new task
  createTask: async (task: TaskFormData): Promise<SpiritualTask> => {
    const response = await axiosInstance.post<SpiritualTask>('/tasks', task)
    return response.data
  },

  // Update existing task
  updateTask: async (id: number, task: TaskFormData): Promise<SpiritualTask> => {
    const response = await axiosInstance.put<SpiritualTask>(`/tasks/${id}`, task)
    return response.data
  },

  // Mark task as complete
  completeTask: async (id: number): Promise<SpiritualTask> => {
    const response = await axiosInstance.patch<SpiritualTask>(`/tasks/${id}/complete`)
    return response.data
  },

  // Mark task as incomplete
  uncompleteTask: async (id: number): Promise<SpiritualTask> => {
    const response = await axiosInstance.patch<SpiritualTask>(`/tasks/${id}/incomplete`)
    return response.data
  },

  // Delete task
  deleteTask: async (id: number): Promise<void> => {
    await axiosInstance.delete(`/tasks/${id}`)
  },

  // Bulk complete tasks
  bulkCompleteTasks: async (taskIds: number[]): Promise<{ updated: number; not_found: number[]; message: string }> => {
    const response = await axiosInstance.post('/tasks/bulk/complete', taskIds)
    return response.data
  },

  // Bulk delete tasks
  bulkDeleteTasks: async (taskIds: number[]): Promise<{ deleted: number; not_found: number[]; message: string }> => {
    const response = await axiosInstance.post('/tasks/bulk/delete', taskIds)
    return response.data
  },

  // ==================== MASJIDS ====================

  // Get all masjids with optional filters
  getMasjids: async (filters?: MasjidFilters): Promise<{ masjids: Masjid[]; total: number; limit: number; offset: number }> => {
    const response = await axiosInstance.get<{ masjids: Masjid[]; total: number; limit: number; offset: number }>('/masjids', {
      params: filters,
    })
    return response.data
  },

  // Get unique area names
  getAreas: async (): Promise<{ areas: string[]; total: number }> => {
    const response = await axiosInstance.get<{ areas: string[]; total: number }>('/masjids/areas/list')
    return response.data
  },

  // Get single masjid by ID
  getMasjid: async (id: number): Promise<Masjid> => {
    const response = await axiosInstance.get<Masjid>(`/masjids/${id}`)
    return response.data
  },

  // Get tasks for a specific masjid
  getMasjidTasks: async (id: number, completed?: boolean): Promise<SpiritualTask[]> => {
    const response = await axiosInstance.get<SpiritualTask[]>(`/masjids/${id}/tasks`, {
      params: completed !== undefined ? { completed } : {},
    })
    return response.data
  },

  // Create new masjid
  createMasjid: async (masjid: MasjidFormData): Promise<Masjid> => {
    const response = await axiosInstance.post<Masjid>('/masjids', masjid)
    return response.data
  },

  // Update existing masjid
  updateMasjid: async (id: number, masjid: MasjidFormData): Promise<Masjid> => {
    const response = await axiosInstance.put<Masjid>(`/masjids/${id}`, masjid)
    return response.data
  },

  // Delete masjid
  deleteMasjid: async (id: number): Promise<void> => {
    await axiosInstance.delete(`/masjids/${id}`)
  },

  // ==================== DAILY HADITH ====================

  // Get today's hadith
  getTodaysHadith: async (): Promise<DailyHadith> => {
    const response = await axiosInstance.get<DailyHadith>('/hadith/today')
    return response.data
  },

  // Get all hadith entries
  getHadithList: async (theme?: string, skip: number = 0, limit: number = 100): Promise<DailyHadith[]> => {
    const response = await axiosInstance.get<DailyHadith[]>('/hadith', {
      params: { theme, skip, limit },
    })
    return response.data
  },

  // Get hadith by specific date
  getHadithByDate: async (date: string): Promise<DailyHadith> => {
    const response = await axiosInstance.get<DailyHadith>(`/hadith/date/${date}`)
    return response.data
  },

  // Get hadith by ID
  getHadith: async (id: number): Promise<DailyHadith> => {
    const response = await axiosInstance.get<DailyHadith>(`/hadith/${id}`)
    return response.data
  },

  // Create new hadith entry
  createHadith: async (hadith: Omit<DailyHadith, 'id' | 'created_at'>): Promise<DailyHadith> => {
    const response = await axiosInstance.post<DailyHadith>('/hadith', hadith)
    return response.data
  },

  // Update existing hadith
  updateHadith: async (id: number, hadith: Omit<DailyHadith, 'id' | 'created_at'>): Promise<DailyHadith> => {
    const response = await axiosInstance.put<DailyHadith>(`/hadith/${id}`, hadith)
    return response.data
  },

  // Delete hadith
  deleteHadith: async (id: number): Promise<void> => {
    await axiosInstance.delete(`/hadith/${id}`)
  },
}

export default api
