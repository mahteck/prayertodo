'use client'

import { useRouter } from 'next/navigation'
import { Masjid } from '@/lib/types'

interface MasjidCardProps {
  masjid: Masjid
  onClick?: (masjid: Masjid) => void
}

export default function MasjidCard({ masjid, onClick }: MasjidCardProps) {
  const router = useRouter()

  const handleClick = () => {
    if (onClick) {
      onClick(masjid)
    } else {
      router.push(`/masjids/${masjid.id}`)
    }
  }

  // Parse facilities if it's a JSON string
  let facilities: string[] = []
  if (masjid.facilities) {
    try {
      const parsed = JSON.parse(masjid.facilities)
      facilities = Object.entries(parsed)
        .filter(([_, value]) => value === true)
        .map(([key, _]) => key)
    } catch (e) {
      // If not JSON, treat as comma-separated string
      facilities = masjid.facilities.split(',').map(f => f.trim()).filter(f => f.length > 0)
    }
  }

  return (
    <div
      onClick={handleClick}
      className="card-dark rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer"
    >
      {/* Masjid Name */}
      <h3 className="text-xl font-semibold text-white mb-3">{masjid.name}</h3>

      {/* Location Info */}
      <div className="space-y-2 mb-4">
        {(masjid.area_name || masjid.city) && (
          <div className="flex items-center text-gray-300">
            <svg className="w-5 h-5 mr-2 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
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
        )}

        {masjid.address && (
          <div className="flex items-start text-gray-300">
            <svg
              className="w-5 h-5 mr-2 mt-0.5 text-gray-400 flex-shrink-0"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
              />
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
              />
            </svg>
            <span className="line-clamp-2">{masjid.address}</span>
          </div>
        )}

        {masjid.imam_name && (
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
            <span>Imam: {masjid.imam_name}</span>
          </div>
        )}

        {masjid.phone && (
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
                d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"
              />
            </svg>
            <a
              href={`tel:${masjid.phone}`}
              onClick={(e) => e.stopPropagation()}
              className="text-salaat-orange hover:text-salaat-orange-light hover:underline"
            >
              {masjid.phone}
            </a>
          </div>
        )}
      </div>

      {/* Facilities */}
      {facilities.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-semibold text-gray-300 mb-2">Facilities</h4>
          <div className="flex flex-wrap gap-2">
            {facilities.slice(0, 4).map((facility, index) => (
              <span
                key={index}
                className="px-2 py-1 text-xs bg-salaat-orange/20 text-salaat-orange rounded-full border border-salaat-orange"
              >
                {facility.charAt(0).toUpperCase() + facility.slice(1)}
              </span>
            ))}
            {facilities.length > 4 && (
              <span className="px-2 py-1 text-xs bg-gray-700 text-gray-300 rounded-full">
                +{facilities.length - 4} more
              </span>
            )}
          </div>
        </div>
      )}

      {/* View Details Button */}
      <div className="pt-4 border-t border-[#2A2A2A]">
        <button className="w-full px-4 py-2 text-salaat-orange font-medium rounded-md hover:bg-salaat-orange/10 transition-colors flex items-center justify-center">
          <span>View Details</span>
          <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5l7 7-7 7"
            />
          </svg>
        </button>
      </div>
    </div>
  )
}
