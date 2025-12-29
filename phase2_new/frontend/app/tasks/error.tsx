'use client'

import { useEffect } from 'react'
import Link from 'next/link'

export default function TasksError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error('Tasks error:', error)
  }, [error])

  return (
    <div className="min-h-screen page-gradient">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-2xl mx-auto card-dark rounded-lg shadow-md p-8 text-center">
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
          <h2 className="text-2xl font-bold text-white mb-2">Error Loading Tasks</h2>
          <p className="text-gray-300 mb-6">
            We encountered a problem while loading your tasks. This could be due to a network issue
            or a temporary server problem.
          </p>
          <div className="flex gap-4 justify-center">
            <button
              onClick={reset}
              className="btn-primary"
            >
              Try Again
            </button>
            <Link
              href="/"
              className="btn-secondary"
            >
              Back to Home
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
