'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import api from '@/lib/api'
import { SpiritualTask, TaskStatistics, DailyHadith } from '@/lib/types'
import { formatDateTime, truncateText } from '@/lib/utils'

export default function Home() {
  const [stats, setStats] = useState<TaskStatistics | null>(null)
  const [upcomingTasks, setUpcomingTasks] = useState<SpiritualTask[]>([])
  const [todaysHadith, setTodaysHadith] = useState<DailyHadith | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)

      // Fetch all dashboard data in parallel
      const [statsData, upcomingData, hadithData] = await Promise.allSettled([
        api.getTaskStatistics(),
        api.getUpcomingTasks(7, 5),
        api.getTodaysHadith(),
      ])

      if (statsData.status === 'fulfilled') {
        setStats(statsData.value)
      }

      if (upcomingData.status === 'fulfilled') {
        setUpcomingTasks(upcomingData.value)
      }

      if (hadithData.status === 'fulfilled') {
        setTodaysHadith(hadithData.value)
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen page-gradient">
      <main className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-10">
          <h1 className="text-5xl font-bold text-white mb-3">
            <span className="text-salaat-orange">Assalamu Alaikum</span>
          </h1>
          <p className="text-gray-300 text-lg">
            Welcome to SalaatFlow - Your Islamic Task Management System
          </p>
        </div>

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="flex flex-col items-center">
              <svg
                className="animate-spin h-14 w-14 text-salaat-orange mb-4"
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
              <p className="text-gray-300">Loading dashboard...</p>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Statistics Cards */}
            {stats && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="card-dark">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-400 mb-1">Total Tasks</p>
                      <p className="text-3xl font-bold text-white">{stats.total}</p>
                    </div>
                    <div className="w-14 h-14 bg-salaat-orange bg-opacity-20 rounded-xl flex items-center justify-center">
                      <svg className="w-7 h-7 text-salaat-orange" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                        <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
                      </svg>
                    </div>
                  </div>
                </div>

                <div className="card-dark">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-400 mb-1">Completed</p>
                      <p className="text-3xl font-bold text-green-400">{stats.completed}</p>
                    </div>
                    <div className="w-14 h-14 bg-green-500 bg-opacity-20 rounded-xl flex items-center justify-center">
                      <svg className="w-7 h-7 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                    </div>
                  </div>
                </div>

                <div className="card-dark">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-400 mb-1">Pending</p>
                      <p className="text-3xl font-bold text-salaat-orange">{stats.pending}</p>
                    </div>
                    <div className="w-14 h-14 bg-salaat-orange bg-opacity-20 rounded-xl flex items-center justify-center">
                      <svg className="w-7 h-7 text-salaat-orange" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                      </svg>
                    </div>
                  </div>
                </div>

                <div className="card-dark">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-400 mb-1">Completion Rate</p>
                      <p className="text-3xl font-bold text-salaat-orange">{stats.completion_rate.toFixed(0)}%</p>
                    </div>
                    <div className="w-14 h-14 bg-salaat-orange bg-opacity-20 rounded-xl flex items-center justify-center">
                      <svg className="w-7 h-7 text-salaat-orange" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 0l-2 2a1 1 0 101.414 1.414L8 10.414l1.293 1.293a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Quick Actions */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Link
                href="/tasks/new"
                className="card-dark hover:border-salaat-orange transition-all group"
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-white">New Task</h3>
                  <div className="w-10 h-10 bg-salaat-orange bg-opacity-20 rounded-full flex items-center justify-center group-hover:bg-opacity-100 transition-all">
                    <svg className="w-5 h-5 text-salaat-orange group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                  </div>
                </div>
                <p className="text-gray-300">Create a new spiritual task or activity</p>
              </Link>

              <Link
                href="/tasks"
                className="card-dark hover:border-salaat-orange transition-all group"
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-white">View All Tasks</h3>
                  <div className="w-10 h-10 bg-salaat-orange bg-opacity-20 rounded-full flex items-center justify-center group-hover:bg-opacity-100 transition-all">
                    <svg className="w-5 h-5 text-salaat-orange group-hover:text-white transition-colors" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                      <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
                    </svg>
                  </div>
                </div>
                <p className="text-gray-300">Browse and manage your tasks</p>
              </Link>

              <Link
                href="/masjids"
                className="card-dark hover:border-salaat-orange transition-all group"
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-white">Find Masjids</h3>
                  <div className="w-10 h-10 bg-salaat-orange bg-opacity-20 rounded-full flex items-center justify-center group-hover:bg-opacity-100 transition-all">
                    <span className="text-xl group-hover:scale-110 transition-transform">🕌</span>
                  </div>
                </div>
                <p className="text-gray-300">Explore masjids in your area</p>
              </Link>
            </div>

            {/* Upcoming Tasks */}
            {upcomingTasks.length > 0 && (
              <div className="card-dark">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-bold text-white">Upcoming Tasks</h2>
                  <Link href="/tasks" className="text-salaat-orange hover:text-orange-400 text-sm font-medium">
                    View All →
                  </Link>
                </div>
                <div className="space-y-3">
                  {upcomingTasks.map((task) => (
                    <Link
                      key={task.id}
                      href={`/tasks/${task.id}`}
                      className="block p-4 bg-[#2A2A2A] rounded-lg hover:border hover:border-salaat-orange transition-all"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="font-semibold text-white mb-1">{task.title}</h3>
                          {task.description && (
                            <p className="text-sm text-gray-300 mb-2">
                              {truncateText(task.description, 80)}
                            </p>
                          )}
                          {task.due_datetime && (
                            <p className="text-sm text-gray-300">
                              Due: {formatDateTime(task.due_datetime)}
                            </p>
                          )}
                        </div>
                        <svg className="w-5 h-5 text-gray-400 ml-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>
            )}

            {/* Today's Hadith Preview */}
            {todaysHadith && (
              <div className="card-dark">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-bold text-white flex items-center">
                    <span className="mr-2">📖</span>
                    Today's Hadith
                  </h2>
                  <Link href="/hadith" className="text-salaat-orange hover:text-orange-400 text-sm font-medium">
                    Read Full →
                  </Link>
                </div>
                <div className="mb-4">
                  <p className="text-gray-300 italic leading-relaxed">
                    "{truncateText(todaysHadith.english_translation, 150)}"
                  </p>
                </div>
                <div className="flex items-center justify-between text-sm text-gray-300">
                  <span>Narrator: {todaysHadith.narrator}</span>
                  <span>{todaysHadith.source}</span>
                </div>
              </div>
            )}

            {/* Empty State */}
            {!stats && !loading && (
              <div className="card-dark p-12 text-center">
                <div className="text-gray-600 mb-4">
                  <svg className="w-24 h-24 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <h3 className="text-xl font-medium text-white mb-2">Get Started with SalaatFlow</h3>
                <p className="text-gray-400 mb-6">
                  Create your first task to start organizing your spiritual activities
                </p>
                <Link
                  href="/tasks/new"
                  className="btn-primary inline-block"
                >
                  Create First Task
                </Link>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}
