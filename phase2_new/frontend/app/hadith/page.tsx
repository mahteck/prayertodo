'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import api from '@/lib/api'
import { DailyHadith } from '@/lib/types'
import { formatDate } from '@/lib/utils'

export default function HadithPage() {
  const [hadith, setHadith] = useState<DailyHadith | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchTodaysHadith()
  }, [])

  const fetchTodaysHadith = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await api.getTodaysHadith()
      setHadith(data)
    } catch (err: any) {
      console.error('Error fetching hadith:', err)
      if (err.response?.status === 404) {
        setError('No hadith available for today. Please check back later.')
      } else {
        setError('Failed to load hadith. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen page-gradient flex items-center justify-center">
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
          <p className="text-gray-300">Loading today's hadith...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen page-gradient">
      {/* Header */}
      <div className="bg-salaat-black-light border-b border-salaat-black-lighter shadow-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white">Daily Hadith</h1>
              <p className="text-gray-300 mt-1">
                {hadith ? formatDate(hadith.hadith_date) : 'Spiritual guidance and inspiration'}
              </p>
            </div>
            <Link
              href="/"
              className="px-4 py-2 text-salaat-orange hover:text-salaat-orange-light font-medium"
            >
              ← Home
            </Link>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          {/* Error State */}
          {error && (
            <div className="card-dark rounded-2xl shadow-xl p-8 text-center">
              <svg
                className="w-16 h-16 text-salaat-orange mx-auto mb-4"
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
              <h2 className="text-2xl font-bold text-white mb-2">No Hadith Available</h2>
              <p className="text-gray-300 mb-6">{error}</p>
              <button
                onClick={fetchTodaysHadith}
                className="btn-primary"
              >
                Try Again
              </button>
            </div>
          )}

          {/* Hadith Display */}
          {hadith && !error && (
            <div className="card-dark rounded-2xl shadow-xl overflow-hidden">
              {/* Decorative Header */}
              <div className="orange-gradient px-8 py-6">
                <div className="flex items-center justify-center space-x-2 text-white">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
                  </svg>
                  <h2 className="text-xl font-semibold">Hadith of the Day</h2>
                </div>
                {hadith.theme && (
                  <div className="text-center mt-2">
                    <span className="inline-block px-4 py-1 bg-white/20 rounded-full text-sm text-white">
                      Theme: {hadith.theme}
                    </span>
                  </div>
                )}
              </div>

              {/* Arabic Text */}
              <div className="px-8 py-10 bg-salaat-black-lighter border-b-2 border-salaat-orange">
                <div className="text-center">
                  <p
                    className="text-3xl md:text-4xl leading-loose text-white font-arabic"
                    style={{
                      direction: 'rtl',
                      fontFamily: "'Amiri', 'Traditional Arabic', 'Arabic Typesetting', serif",
                      lineHeight: '2.5',
                    }}
                  >
                    {hadith.arabic_text}
                  </p>
                </div>
              </div>

              {/* English Translation */}
              <div className="px-8 py-8">
                <div className="mb-6">
                  <h3 className="text-sm font-semibold text-salaat-orange uppercase tracking-wide mb-3">
                    Translation
                  </h3>
                  <p className="text-lg text-gray-300 leading-relaxed italic">
                    "{hadith.english_translation}"
                  </p>
                </div>

                {/* Source Information */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-6 border-t border-salaat-black-lighter">
                  <div>
                    <h4 className="text-sm font-semibold text-white mb-1">Narrator</h4>
                    <p className="text-gray-300 flex items-center">
                      <svg
                        className="w-5 h-5 mr-2 text-salaat-orange"
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
                      {hadith.narrator}
                    </p>
                  </div>
                  <div>
                    <h4 className="text-sm font-semibold text-white mb-1">Source</h4>
                    <p className="text-gray-300 flex items-center">
                      <svg
                        className="w-5 h-5 mr-2 text-salaat-orange"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
                      </svg>
                      {hadith.source}
                    </p>
                  </div>
                </div>
              </div>

              {/* Footer Quote */}
              <div className="px-8 py-6 bg-salaat-black-lighter border-t border-salaat-black-lighter">
                <p className="text-center text-sm text-gray-400 italic">
                  "The best of you are those who learn the Quran and teach it." - Prophet Muhammad
                  (ﷺ)
                </p>
              </div>
            </div>
          )}

          {/* Additional Actions */}
          {hadith && !error && (
            <div className="mt-8 text-center space-y-4">
              <div className="flex justify-center gap-4">
                <button
                  onClick={() => window.print()}
                  className="btn-secondary"
                >
                  <svg
                    className="w-5 h-5 inline mr-2"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"
                    />
                  </svg>
                  Print Hadith
                </button>
                <button
                  onClick={() => {
                    const text = `${hadith.english_translation}\n\nNarrator: ${hadith.narrator}\nSource: ${hadith.source}`
                    navigator.clipboard.writeText(text)
                    alert('Hadith copied to clipboard!')
                  }}
                  className="btn-secondary"
                >
                  <svg
                    className="w-5 h-5 inline mr-2"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                    />
                  </svg>
                  Copy Text
                </button>
              </div>
              <p className="text-sm text-gray-400">
                Share this wisdom with others and spread the knowledge
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
