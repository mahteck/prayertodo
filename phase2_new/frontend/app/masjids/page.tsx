'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import api from '@/lib/api'
import { Masjid } from '@/lib/types'
import MasjidList from './components/MasjidList'
import AreaFilter from './components/AreaFilter'

export default function MasjidsPage() {
  const router = useRouter()

  const [masjids, setMasjids] = useState<Masjid[]>([])
  const [areas, setAreas] = useState<string[]>([])
  const [selectedArea, setSelectedArea] = useState<string>('')
  const [searchText, setSearchText] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [total, setTotal] = useState(0)

  useEffect(() => {
    fetchAreas()
  }, [])

  useEffect(() => {
    fetchMasjids()
  }, [selectedArea, searchText])

  const fetchAreas = async () => {
    try {
      const data = await api.getAreas()
      setAreas(data.areas)
    } catch (err) {
      console.error('Error fetching areas:', err)
    }
  }

  const fetchMasjids = async () => {
    try {
      setLoading(true)
      setError(null)
      const filters: any = {}
      if (selectedArea) filters.area_name = selectedArea
      if (searchText.trim()) filters.search = searchText.trim()

      const data = await api.getMasjids(filters)
      setMasjids(data.masjids)
      setTotal(data.total)
    } catch (err) {
      console.error('Error fetching masjids:', err)
      setError('Failed to load masjids. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleAreaChange = (area: string | null) => {
    setSelectedArea(area || '')
  }

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchText(e.target.value)
  }

  const handleSelectMasjid = (masjid: Masjid) => {
    router.push(`/masjids/${masjid.id}`)
  }

  return (
    <div className="min-h-screen bg-salaat-black">
      {/* Page Header */}
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white">Masjids</h1>
            <p className="text-gray-400 mt-1">Find and explore masjids in your area</p>
          </div>
          <Link
            href="/masjids/new"
            className="btn-primary flex items-center"
          >
            <svg
              className="w-5 h-5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 6v6m0 0v6m0-6h6m-6 0H6"
              />
            </svg>
            Add Masjid
          </Link>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 pb-8">
        {/* Filters */}
        <div className="card-dark mb-6">
          <h2 className="text-lg font-semibold text-white mb-4">Search & Filter</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Search */}
            <div>
              <label htmlFor="search" className="form-label">
                Search Masjids
              </label>
              <input
                id="search"
                type="text"
                value={searchText}
                onChange={handleSearchChange}
                placeholder="Search by name, area, or city..."
                className="input-field w-full"
              />
            </div>

            {/* Area Filter */}
            <AreaFilter
              areas={areas}
              selectedArea={selectedArea}
              onAreaChange={handleAreaChange}
            />
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center items-center py-16">
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
              <p className="text-gray-400">Loading masjids...</p>
            </div>
          </div>
        )}

        {/* Error State */}
        {error && !loading && (
          <div className="card-dark border-red-800 mb-6">
            <div className="flex items-center">
              <svg
                className="w-6 h-6 text-red-400 mr-3"
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
              <div>
                <h3 className="text-red-400 font-medium">Error Loading Masjids</h3>
                <p className="text-red-300 text-sm mt-1">{error}</p>
              </div>
            </div>
            <button
              onClick={fetchMasjids}
              className="mt-4 px-4 py-2 bg-red-900 text-white rounded-md hover:bg-red-800 transition-colors"
            >
              Try Again
            </button>
          </div>
        )}

        {/* Masjid Count */}
        {!loading && !error && (
          <div className="mb-4 text-sm text-gray-400">
            Showing {masjids.length} {masjids.length === 1 ? 'masjid' : 'masjids'}
            {selectedArea && ` in ${selectedArea}`}
          </div>
        )}

        {/* Masjid List */}
        {!loading && !error && (
          <MasjidList masjids={masjids} onSelectMasjid={handleSelectMasjid} />
        )}
      </div>
    </div>
  )
}
