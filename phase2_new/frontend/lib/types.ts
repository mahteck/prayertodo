/**
 * TypeScript types for SalaatFlow
 * These mirror the backend SQLModel models
 */

// Enums
export enum TaskCategory {
  FARZ = "Farz",
  SUNNAH = "Sunnah",
  NAFL = "Nafl",
  DEED = "Deed",
  OTHER = "Other",
}

export enum Priority {
  URGENT = "Urgent",
  HIGH = "High",
  MEDIUM = "Medium",
  LOW = "Low",
}

export enum Recurrence {
  NONE = "None",
  DAILY = "Daily",
  WEEKLY = "Weekly",
  MONTHLY = "Monthly",
}

// Models
export interface Masjid {
  id: number
  name: string
  area_name: string
  city?: string | null
  address?: string | null
  imam_name?: string | null
  phone?: string | null
  latitude?: number | null
  longitude?: number | null
  fajr_time: string
  dhuhr_time: string
  asr_time: string
  maghrib_time: string
  isha_time: string
  jummah_time?: string | null
  created_at: string
  updated_at: string
}

export interface SpiritualTask {
  id: number
  title: string
  description?: string | null
  category: TaskCategory
  priority: Priority
  tags?: string | null
  masjid_id?: number | null
  masjid?: Masjid | null
  due_datetime?: string | null
  recurrence: Recurrence
  completed: boolean
  completed_at?: string | null
  created_at: string
  updated_at: string
}

export interface DailyHadith {
  id: number
  hadith_date: string
  arabic_text: string
  english_translation: string
  narrator: string
  source: string
  theme?: string | null
  created_at: string
}

// API Types
export interface TaskFilters {
  category?: TaskCategory
  priority?: Priority
  completed?: boolean
  masjid_id?: number
  recurrence?: Recurrence
  search?: string
  sort_by?: string
  sort_order?: 'asc' | 'desc'
  skip?: number
  limit?: number
}

export interface MasjidFilters {
  area_name?: string
  search?: string
  offset?: number
  limit?: number
}

export interface TaskStatistics {
  total: number
  completed: number
  pending: number
  completion_rate: number
  by_category: {
    [key: string]: {
      total: number
      completed: number
      pending: number
    }
  }
  by_priority: {
    [key: string]: {
      total: number
      completed: number
      pending: number
    }
  }
}

// Form Data Types
export interface TaskFormData {
  title: string
  description?: string
  category: TaskCategory
  priority: Priority
  tags?: string
  masjid_id?: number | null
  due_datetime?: string | null
  recurrence: Recurrence
}

export interface MasjidFormData {
  name: string
  area_name: string
  city?: string
  address?: string
  imam_name?: string
  phone?: string
  latitude?: number
  longitude?: number
  fajr_time: string
  dhuhr_time: string
  asr_time: string
  maghrib_time: string
  isha_time: string
  jummah_time?: string
}
