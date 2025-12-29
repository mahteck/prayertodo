'use client'

import { Masjid } from '@/lib/types'
import MasjidCard from './MasjidCard'

interface MasjidListProps {
  masjids: Masjid[]
  onSelectMasjid?: (masjid: Masjid) => void
}

export default function MasjidList({ masjids, onSelectMasjid }: MasjidListProps) {
  if (masjids.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 px-4">
        <div className="text-gray-500 mb-4">
          <svg className="w-24 h-24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
            />
          </svg>
        </div>
        <h3 className="text-xl font-medium text-gray-300 mb-2">No masjids found</h3>
        <p className="text-gray-400 text-center max-w-md">
          No masjids match your current search criteria. Try adjusting your filters.
        </p>
      </div>
    )
  }

  return (
    <div className="grid gap-6 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
      {masjids.map((masjid) => (
        <MasjidCard key={masjid.id} masjid={masjid} onClick={onSelectMasjid} />
      ))}
    </div>
  )
}
