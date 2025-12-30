'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import api from '@/lib/api'
import { Masjid, SpiritualTask } from '@/lib/types'
import { formatDateTime, getPriorityColor, getCategoryBadgeColor } from '@/lib/utils'

export default function MasjidDetailPage() {
  const params = useParams()
  const masjidId = parseInt(params.id as string)

  const [masjid, setMasjid] = useState<Masjid | null>(null)
  const [tasks, setTasks] = useState<SpiritualTask[]>([])
  const [showCompleted, setShowCompleted] = useState(false)
  const [loading, setLoading] = useState(true)
  const [tasksLoading, setTasksLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (masjidId) {
      fetchMasjid()
      fetchTasks()
    }
  }, [masjidId, showCompleted])

  const fetchMasjid = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await api.getMasjid(masjidId)
      setMasjid(data)
    } catch (err: any) {
      console.error('Error fetching masjid:', err)
      if (err.response?.status === 404) {
        setError('Masjid not found')
      } else {
        setError('Failed to load masjid. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  const fetchTasks = async () => {
    try {
      setTasksLoading(true)
      const data = await api.getMasjidTasks(masjidId, showCompleted ? undefined : false)
      setTasks(data)
    } catch (err) {
      console.error('Error fetching tasks:', err)
    } finally {
      setTasksLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-salaat-black flex items-center justify-center">
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
          <p className="text-gray-300">Loading masjid details...</p>
        </div>
      </div>
    )
  }

  if (error || !masjid) {
    return (
      <div className="min-h-screen bg-salaat-black">
        <div className="container mx-auto px-4 py-16">
          <div className="max-w-2xl mx-auto card-dark rounded-lg shadow-md p-8 text-center">
            <svg
              className="w-16 h-16 text-red-400 mx-auto mb-4"
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
            <h2 className="text-2xl font-bold text-white mb-2">Masjid Not Found</h2>
            <p className="text-gray-300 mb-6">
              {error || 'The masjid you are looking for does not exist.'}
            </p>
            <Link
              href="/masjids"
              className="inline-block px-6 py-3 btn-primary font-medium rounded-lg"
            >
              Back to Masjids
            </Link>
          </div>
        </div>
      </div>
    )
  }

  // Parse facilities
  let facilities: { [key: string]: any } = {}
  if (masjid.facilities) {
    try {
      facilities = JSON.parse(masjid.facilities)
    } catch (e) {
      // If not JSON, ignore
    }
  }

  return (
    <div className="min-h-screen bg-salaat-black">
      {/* Page Header */}
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center">
          <Link
            href="/masjids"
            className="mr-4 text-gray-400 hover:text-white focus:outline-none"
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
          <div>
            <h1 className="text-3xl font-bold text-white">{masjid.name}</h1>
            <p className="text-gray-400 mt-1">Masjid Details and Information</p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 pb-8">
        <div className="max-w-5xl mx-auto">
          {/* Masjid Information Card */}
          <div className="card-dark rounded-lg shadow-md p-8 mb-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-white">Information</h2>
              <Link
                href={`/masjids/${masjid.id}/edit` as any}
                className="px-4 py-2 btn-secondary rounded-lg flex items-center gap-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Edit
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Location */}
              {(masjid.area_name || masjid.city) && (
                <div>
                  <h3 className="text-sm font-semibold text-gray-300 mb-2">Location</h3>
                  <div className="flex items-center text-gray-300">
                    <svg
                      className="w-5 h-5 mr-2 text-gray-400"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
                        clipRule="evenodd"
                      />
                    </svg>
                    <span>
                      {masjid.area_name && <span className="font-medium">{masjid.area_name}</span>}
                      {masjid.area_name && masjid.city && <span className="mx-1">•</span>}
                      {masjid.city && <span>{masjid.city}</span>}
                    </span>
                  </div>
                </div>
              )}

              {/* Address */}
              {masjid.address && (
                <div>
                  <h3 className="text-sm font-semibold text-gray-300 mb-2">Address</h3>
                  <p className="text-gray-300">{masjid.address}</p>
                </div>
              )}

              {/* Imam */}
              {masjid.imam_name && (
                <div>
                  <h3 className="text-sm font-semibold text-gray-300 mb-2">Imam</h3>
                  <div className="flex items-center text-gray-300">
                    <svg
                      className="w-5 h-5 mr-2 text-gray-400"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                      />
                    </svg>
                    <span>{masjid.imam_name}</span>
                  </div>
                </div>
              )}

              {/* Phone */}
              {masjid.phone && (
                <div>
                  <h3 className="text-sm font-semibold text-gray-300 mb-2">Phone</h3>
                  <div className="flex items-center">
                    <svg
                      className="w-5 h-5 mr-2 text-gray-400"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"
                      />
                    </svg>
                    <a
                      href={`tel:${masjid.phone}`}
                      className="text-salaat-orange hover:text-salaat-orange-light hover:underline font-medium"
                    >
                      {masjid.phone}
                    </a>
                  </div>
                </div>
              )}
            </div>

            {/* Facilities */}
            {Object.keys(facilities).length > 0 && (
              <div className="mt-6">
                <h3 className="text-sm font-semibold text-gray-300 mb-3">Facilities</h3>
                <div className="flex flex-wrap gap-3">
                  {Object.entries(facilities).map(([key, value]) => (
                    <div
                      key={key}
                      className={`px-4 py-2 rounded-lg border ${
                        value
                          ? 'bg-green-900/30 text-green-400 border-green-800'
                          : 'bg-gray-800 text-gray-400 border-gray-700'
                      }`}
                    >
                      <span className="font-medium">
                        {key.charAt(0).toUpperCase() + key.slice(1)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Prayer Times Card */}
          <div className="card-dark rounded-lg shadow-md p-8 mb-6">
            <h2 className="text-2xl font-bold text-white mb-6">Prayer Times</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
              {masjid.fajr_time && (
                <div className="text-center p-4 bg-indigo-900/30 rounded-lg border border-indigo-700">
                  <p className="text-sm font-medium text-indigo-300 mb-1">Fajr</p>
                  <p className="text-2xl font-bold text-indigo-400">{masjid.fajr_time}</p>
                </div>
              )}
              {masjid.dhuhr_time && (
                <div className="text-center p-4 bg-yellow-900/30 rounded-lg border border-yellow-700">
                  <p className="text-sm font-medium text-yellow-300 mb-1">Dhuhr</p>
                  <p className="text-2xl font-bold text-yellow-400">{masjid.dhuhr_time}</p>
                </div>
              )}
              {masjid.asr_time && (
                <div className="text-center p-4 bg-amber-900/30 rounded-lg border border-amber-700">
                  <p className="text-sm font-medium text-amber-300 mb-1">Asr</p>
                  <p className="text-2xl font-bold text-amber-400">{masjid.asr_time}</p>
                </div>
              )}
              {masjid.maghrib_time && (
                <div className="text-center p-4 bg-rose-900/30 rounded-lg border border-rose-700">
                  <p className="text-sm font-medium text-rose-300 mb-1">Maghrib</p>
                  <p className="text-2xl font-bold text-rose-400">{masjid.maghrib_time}</p>
                </div>
              )}
              {masjid.isha_time && (
                <div className="text-center p-4 bg-purple-900/30 rounded-lg border border-purple-700">
                  <p className="text-sm font-medium text-purple-300 mb-1">Isha</p>
                  <p className="text-2xl font-bold text-purple-400">{masjid.isha_time}</p>
                </div>
              )}
              {masjid.jummah_time && (
                <div className="text-center p-4 bg-emerald-900/30 rounded-lg border border-emerald-700 md:col-span-2 lg:col-span-1">
                  <p className="text-sm font-medium text-emerald-300 mb-1">Jummah</p>
                  <p className="text-2xl font-bold text-emerald-400">{masjid.jummah_time}</p>
                </div>
              )}
            </div>
          </div>

          {/* Associated Tasks */}
          <div className="card-dark rounded-lg shadow-md p-8">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
              <h2 className="text-2xl font-bold text-white">Associated Tasks</h2>
              <div className="flex items-center gap-4">
                <Link
                  href={`/tasks/new?masjid=${masjid.id}`}
                  className="px-4 py-2 btn-primary font-medium rounded-lg flex items-center gap-2"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  Add Task
                </Link>
                <label className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={showCompleted}
                    onChange={(e) => setShowCompleted(e.target.checked)}
                    className="mr-2 w-4 h-4 text-salaat-orange focus:ring-salaat-orange border-gray-700 rounded"
                  />
                  <span className="text-sm text-gray-300">Show completed</span>
                </label>
              </div>
            </div>

            {tasksLoading ? (
              <div className="flex justify-center py-8">
                <svg
                  className="animate-spin h-8 w-8 text-salaat-orange"
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
              </div>
            ) : tasks.length === 0 ? (
              <div className="text-center py-8 text-gray-400">
                <p>No tasks associated with this masjid</p>
              </div>
            ) : (
              <div className="space-y-3">
                {tasks.map((task) => (
                  <Link
                    key={task.id}
                    href={`/tasks/${task.id}`}
                    className="block bg-gray-800/50 hover:bg-gray-800 rounded-lg p-4 transition-colors border border-gray-700"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h4
                          className={`font-semibold text-white mb-1 ${
                            task.completed ? 'line-through text-gray-400' : ''
                          }`}
                        >
                          {task.title}
                        </h4>
                        <div className="flex flex-wrap gap-2 mb-2">
                          <span
                            className={`px-2 py-1 text-xs font-medium rounded-full border ${getCategoryBadgeColor(
                              task.category
                            )}`}
                          >
                            {task.category}
                          </span>
                          <span
                            className={`px-2 py-1 text-xs font-medium rounded-full border ${getPriorityColor(
                              task.priority
                            )}`}
                          >
                            {task.priority}
                          </span>
                          {task.completed && (
                            <span className="px-2 py-1 text-xs font-medium rounded-full border bg-green-100 text-green-800 border-green-200">
                              Completed
                            </span>
                          )}
                        </div>
                        {task.due_datetime && (
                          <p className="text-sm text-gray-400">
                            Due: {formatDateTime(task.due_datetime)}
                          </p>
                        )}
                      </div>
                      <svg
                        className="w-5 h-5 text-gray-500 ml-4 flex-shrink-0"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 5l7 7-7 7"
                        />
                      </svg>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>

          {/* Back Link */}
          <div className="mt-6 text-center">
            <Link href="/masjids" className="text-salaat-orange hover:text-salaat-orange-light font-medium">
              ← Back to Masjids
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
