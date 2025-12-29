'use client'

import { useState, useEffect } from 'react'
import { TaskFilters, Masjid, TaskCategory, Priority, Recurrence } from '@/lib/types'

interface TaskFiltersProps {
  filters: TaskFilters
  onFilterChange: (filters: TaskFilters) => void
  masjids: Masjid[]
}

export default function TaskFiltersComponent({ filters, onFilterChange, masjids }: TaskFiltersProps) {
  const [searchText, setSearchText] = useState(filters.search || '')

  // Debounce search input
  useEffect(() => {
    const timer = setTimeout(() => {
      onFilterChange({ ...filters, search: searchText || undefined })
    }, 300)

    return () => clearTimeout(timer)
  }, [searchText])

  const handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value
    onFilterChange({
      ...filters,
      category: value ? (value as TaskCategory) : undefined,
    })
  }

  const handlePriorityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value
    onFilterChange({
      ...filters,
      priority: value ? (value as Priority) : undefined,
    })
  }

  const handleStatusChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value
    onFilterChange({
      ...filters,
      completed: value === '' ? undefined : value === 'true',
    })
  }

  const handleMasjidChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value
    onFilterChange({
      ...filters,
      masjid_id: value ? parseInt(value) : undefined,
    })
  }

  const handleRecurrenceChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value
    onFilterChange({
      ...filters,
      recurrence: value ? (value as Recurrence) : undefined,
    })
  }

  const handleSortByChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onFilterChange({ ...filters, sort_by: e.target.value })
  }

  const handleSortOrderChange = () => {
    const newOrder = filters.sort_order === 'asc' ? 'desc' : 'asc'
    onFilterChange({ ...filters, sort_order: newOrder })
  }

  const handleClearFilters = () => {
    setSearchText('')
    onFilterChange({
      sort_by: 'created_at',
      sort_order: 'desc',
    })
  }

  const hasActiveFilters =
    filters.category ||
    filters.priority ||
    filters.completed !== undefined ||
    filters.masjid_id ||
    filters.recurrence ||
    filters.search

  return (
    <div className="card-dark mb-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-white">Filters & Search</h2>
        {hasActiveFilters && (
          <button
            onClick={handleClearFilters}
            className="text-sm text-salaat-orange hover:text-orange-400 font-medium"
          >
            Clear All
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Search */}
        <div className="col-span-full">
          <label htmlFor="search" className="form-label">
            Search
          </label>
          <input
            id="search"
            type="text"
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            placeholder="Search in title and description..."
            className="input-field w-full"
          />
        </div>

        {/* Category Filter */}
        <div>
          <label htmlFor="category" className="form-label">
            Category
          </label>
          <select
            id="category"
            value={filters.category || ''}
            onChange={handleCategoryChange}
            className="select-field w-full"
          >
            <option value="">All Categories</option>
            <option value={TaskCategory.FARZ}>Farz (Obligatory)</option>
            <option value={TaskCategory.SUNNAH}>Sunnah</option>
            <option value={TaskCategory.NAFL}>Nafl (Voluntary)</option>
            <option value={TaskCategory.DEED}>Good Deed</option>
            <option value={TaskCategory.OTHER}>Other</option>
          </select>
        </div>

        {/* Priority Filter */}
        <div>
          <label htmlFor="priority" className="form-label">
            Priority
          </label>
          <select
            id="priority"
            value={filters.priority || ''}
            onChange={handlePriorityChange}
            className="select-field w-full"
          >
            <option value="">All Priorities</option>
            <option value={Priority.URGENT}>Urgent</option>
            <option value={Priority.HIGH}>High</option>
            <option value={Priority.MEDIUM}>Medium</option>
            <option value={Priority.LOW}>Low</option>
          </select>
        </div>

        {/* Status Filter */}
        <div>
          <label htmlFor="status" className="form-label">
            Status
          </label>
          <select
            id="status"
            value={filters.completed === undefined ? '' : filters.completed.toString()}
            onChange={handleStatusChange}
            className="select-field w-full"
          >
            <option value="">All Tasks</option>
            <option value="false">Pending</option>
            <option value="true">Completed</option>
          </select>
        </div>

        {/* Masjid Filter */}
        <div>
          <label htmlFor="masjid" className="form-label">
            Masjid
          </label>
          <select
            id="masjid"
            value={filters.masjid_id || ''}
            onChange={handleMasjidChange}
            className="select-field w-full"
          >
            <option value="">All Masjids</option>
            {Array.isArray(masjids) && masjids.map((masjid) => (
              <option key={masjid.id} value={masjid.id}>
                {masjid.name} {masjid.area && `(${masjid.area})`}
              </option>
            ))}
          </select>
        </div>

        {/* Recurrence Filter */}
        <div>
          <label htmlFor="recurrence" className="form-label">
            Recurrence
          </label>
          <select
            id="recurrence"
            value={filters.recurrence || ''}
            onChange={handleRecurrenceChange}
            className="select-field w-full"
          >
            <option value="">All</option>
            <option value={Recurrence.NONE}>Once</option>
            <option value={Recurrence.DAILY}>Daily</option>
            <option value={Recurrence.WEEKLY}>Weekly</option>
            <option value={Recurrence.MONTHLY}>Monthly</option>
          </select>
        </div>

        {/* Sort By */}
        <div>
          <label htmlFor="sortBy" className="form-label">
            Sort By
          </label>
          <select
            id="sortBy"
            value={filters.sort_by || 'created_at'}
            onChange={handleSortByChange}
            className="select-field w-full"
          >
            <option value="created_at">Created Date</option>
            <option value="due_datetime">Due Date</option>
            <option value="priority">Priority</option>
            <option value="title">Title</option>
            <option value="updated_at">Updated Date</option>
          </select>
        </div>

        {/* Sort Order */}
        <div>
          <label className="form-label">Sort Order</label>
          <button
            onClick={handleSortOrderChange}
            className="w-full px-3 py-2 bg-salaat-black-light border border-salaat-black-lighter rounded-md text-white hover:bg-salaat-black-lighter focus:outline-none focus:ring-2 focus:ring-salaat-orange focus:border-transparent flex items-center justify-center transition-colors"
          >
            {filters.sort_order === 'asc' ? (
              <>
                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M3 3a1 1 0 000 2h11a1 1 0 100-2H3zM3 7a1 1 0 000 2h7a1 1 0 100-2H3zM3 11a1 1 0 100 2h4a1 1 0 100-2H3zM15 8a1 1 0 10-2 0v5.586l-1.293-1.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L15 13.586V8z" />
                </svg>
                Ascending
              </>
            ) : (
              <>
                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M3 3a1 1 0 000 2h11a1 1 0 100-2H3zM3 7a1 1 0 000 2h5a1 1 0 000-2H3zM3 11a1 1 0 100 2h4a1 1 0 100-2H3zM13 16a1 1 0 102 0v-5.586l1.293 1.293a1 1 0 001.414-1.414l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 101.414 1.414L13 10.414V16z" />
                </svg>
                Descending
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  )
}
