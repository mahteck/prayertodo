'use client'

import { useState, useEffect } from 'react'
import { useRouter, useParams } from 'next/navigation'
import Link from 'next/link'
import api from '@/lib/api'
import { MasjidFormData, Masjid } from '@/lib/types'

export default function EditMasjidPage() {
  const router = useRouter()
  const params = useParams()
  const masjidId = parseInt(params.id as string)

  const [loading, setLoading] = useState(false)
  const [fetchLoading, setFetchLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [masjid, setMasjid] = useState<Masjid | null>(null)

  const [formData, setFormData] = useState<MasjidFormData>({
    name: '',
    area_name: '',
    city: '',
    address: '',
    imam_name: '',
    phone: '',
    fajr_time: '',
    dhuhr_time: '',
    asr_time: '',
    maghrib_time: '',
    isha_time: '',
    jummah_time: '',
  })

  useEffect(() => {
    if (masjidId) {
      fetchMasjid()
    }
  }, [masjidId])

  const fetchMasjid = async () => {
    try {
      setFetchLoading(true)
      const data = await api.getMasjid(masjidId)
      setMasjid(data)

      // Populate form
      setFormData({
        name: data.name || '',
        area_name: data.area_name || '',
        city: data.city || '',
        address: data.address || '',
        imam_name: data.imam_name || '',
        phone: data.phone || '',
        fajr_time: data.fajr_time || '',
        dhuhr_time: data.dhuhr_time || '',
        asr_time: data.asr_time || '',
        maghrib_time: data.maghrib_time || '',
        isha_time: data.isha_time || '',
        jummah_time: data.jummah_time || '',
      })
    } catch (err: any) {
      console.error('Error fetching masjid:', err)
      setError('Failed to load masjid. Please try again.')
    } finally {
      setFetchLoading(false)
    }
  }

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {}

    if (!formData.name.trim()) {
      newErrors.name = 'Masjid name is required'
    }

    if (!formData.area_name?.trim()) {
      newErrors.area = 'Area is required'
    }

    // Validate prayer times format (HH:MM)
    const timeRegex = /^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/
    const requiredTimes = ['fajr_time', 'dhuhr_time', 'asr_time', 'maghrib_time', 'isha_time']

    requiredTimes.forEach(field => {
      const value = formData[field as keyof MasjidFormData]
      if (!value || !timeRegex.test(value as string)) {
        newErrors[field] = 'Valid time required (HH:MM format)'
      }
    })

    if (formData.jummah_time && !timeRegex.test(formData.jummah_time)) {
      newErrors.jummah_time = 'Valid time required (HH:MM format)'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validate()) {
      return
    }

    try {
      setLoading(true)
      setError(null)

      await api.updateMasjid(masjidId, formData)

      // Success - navigate back to detail page
      router.push(`/masjids/${masjidId}`)
    } catch (err: any) {
      console.error('Error updating masjid:', err)
      // Handle validation errors (array of objects)
      if (err.response?.data?.detail && Array.isArray(err.response.data.detail)) {
        const fieldErrors: Record<string, string> = {}
        const errorMessages: string[] = []

        err.response.data.detail.forEach((e: any) => {
          const message = e.msg || e.message || 'Invalid input'
          errorMessages.push(message)

          // If the error has a location field, map it to the form field
          if (e.loc && Array.isArray(e.loc) && e.loc.length > 1) {
            const fieldName = e.loc[e.loc.length - 1]
            fieldErrors[fieldName] = message
          }
        })

        if (Object.keys(fieldErrors).length > 0) {
          setErrors(fieldErrors)
        }
        setError(errorMessages.join(', ') || 'Validation failed. Please check your input.')
      } else if (typeof err.response?.data?.detail === 'string') {
        setError(err.response.data.detail)
      } else {
        setError('Failed to update masjid. Please try again.')
      }
      setLoading(false)
    }
  }

  const handleChange = (field: keyof MasjidFormData, value: string) => {
    setFormData({ ...formData, [field]: value })
    // Clear error for this field
    if (errors[field]) {
      setErrors({ ...errors, [field]: '' })
    }
  }

  if (fetchLoading) {
    return (
      <div className="min-h-screen page-gradient flex items-center justify-center">
        <div className="flex flex-col items-center">
          <svg className="animate-spin h-12 w-12 text-salaat-orange mb-4" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          <p className="text-gray-300">Loading masjid...</p>
        </div>
      </div>
    )
  }

  if (!masjid) {
    return (
      <div className="min-h-screen page-gradient">
        <div className="container mx-auto px-4 py-16">
          <div className="max-w-2xl mx-auto card-dark p-8 text-center">
            <h2 className="text-2xl font-bold text-white mb-2">Masjid Not Found</h2>
            <p className="text-gray-300 mb-6">The masjid you are trying to edit does not exist.</p>
            <Link href="/masjids" className="btn-primary">
              Back to Masjids
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen page-gradient">
      {/* Page Header */}
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center">
          <Link href={`/masjids/${masjidId}`} className="mr-4 text-gray-300 hover:text-salaat-orange focus:outline-none transition-colors">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </Link>
          <div>
            <h1 className="text-3xl font-bold text-white">Edit Masjid</h1>
            <p className="text-gray-300 mt-1">Update masjid information and prayer times</p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 pb-8">
        <div className="max-w-3xl mx-auto">
          {/* Error Message */}
          {error && (
            <div className="bg-red-900/20 border border-red-800 rounded-lg p-4 mb-6">
              <div className="flex items-center">
                <svg className="w-5 h-5 text-red-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p className="text-red-300">{error}</p>
              </div>
            </div>
          )}

          {/* Form */}
          <div className="card-dark p-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Basic Information */}
              <div>
                <h2 className="text-xl font-bold text-white mb-4">Basic Information</h2>

                {/* Masjid Name */}
                <div className="mb-4">
                  <label htmlFor="name" className="form-label">
                    Masjid Name <span className="text-red-400">*</span>
                  </label>
                  <input
                    id="name"
                    type="text"
                    value={formData.name}
                    onChange={(e) => handleChange('name', e.target.value)}
                    className={`input-field w-full ${
                      errors.name ? 'border-red-500 focus:ring-red-500' : ''
                    }`}
                  />
                  {errors.name && <p className="text-red-400 text-sm mt-1">{errors.name}</p>}
                </div>

                {/* Area and City */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <label htmlFor="area" className="form-label">
                      Area <span className="text-red-400">*</span>
                    </label>
                    <input
                      id="area"
                      type="text"
                      value={formData.area_name}
                      onChange={(e) => handleChange('area_name', e.target.value)}
                      className={`input-field w-full ${
                        errors.area_name ? 'border-red-500 focus:ring-red-500' : ''
                      }`}
                    />
                    {errors.area_name && <p className="text-red-400 text-sm mt-1">{errors.area_name}</p>}
                  </div>

                  <div>
                    <label htmlFor="city" className="form-label">
                      City
                    </label>
                    <input
                      id="city"
                      type="text"
                      value={formData.city}
                      onChange={(e) => handleChange('city', e.target.value)}
                      className="input-field w-full"
                    />
                  </div>
                </div>

                {/* Address */}
                <div className="mb-4">
                  <label htmlFor="address" className="form-label">
                    Address
                  </label>
                  <textarea
                    id="address"
                    value={formData.address}
                    onChange={(e) => handleChange('address', e.target.value)}
                    rows={2}
                    className="input-field w-full"
                  />
                </div>

                {/* Imam and Phone */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="imam_name" className="form-label">
                      Imam Name
                    </label>
                    <input
                      id="imam_name"
                      type="text"
                      value={formData.imam_name}
                      onChange={(e) => handleChange('imam_name', e.target.value)}
                      className="input-field w-full"
                    />
                  </div>

                  <div>
                    <label htmlFor="phone" className="form-label">
                      Phone
                    </label>
                    <input
                      id="phone"
                      type="tel"
                      value={formData.phone}
                      onChange={(e) => handleChange('phone', e.target.value)}
                      className="input-field w-full"
                    />
                  </div>
                </div>
              </div>

              {/* Prayer Times */}
              <div>
                <h2 className="text-xl font-bold text-white mb-4">
                  Prayer Times <span className="text-sm text-gray-400">(24-hour format: HH:MM)</span>
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {/* Fajr */}
                  <div>
                    <label htmlFor="fajr_time" className="form-label">
                      Fajr <span className="text-red-400">*</span>
                    </label>
                    <input
                      id="fajr_time"
                      type="time"
                      value={formData.fajr_time}
                      onChange={(e) => handleChange('fajr_time', e.target.value)}
                      className={`input-field w-full ${
                        errors.fajr_time ? 'border-red-500 focus:ring-red-500' : ''
                      }`}
                    />
                    {errors.fajr_time && <p className="text-red-400 text-sm mt-1">{errors.fajr_time}</p>}
                  </div>

                  {/* Dhuhr */}
                  <div>
                    <label htmlFor="dhuhr_time" className="form-label">
                      Dhuhr <span className="text-red-400">*</span>
                    </label>
                    <input
                      id="dhuhr_time"
                      type="time"
                      value={formData.dhuhr_time}
                      onChange={(e) => handleChange('dhuhr_time', e.target.value)}
                      className={`input-field w-full ${
                        errors.dhuhr_time ? 'border-red-500 focus:ring-red-500' : ''
                      }`}
                    />
                    {errors.dhuhr_time && <p className="text-red-400 text-sm mt-1">{errors.dhuhr_time}</p>}
                  </div>

                  {/* Asr */}
                  <div>
                    <label htmlFor="asr_time" className="form-label">
                      Asr <span className="text-red-400">*</span>
                    </label>
                    <input
                      id="asr_time"
                      type="time"
                      value={formData.asr_time}
                      onChange={(e) => handleChange('asr_time', e.target.value)}
                      className={`input-field w-full ${
                        errors.asr_time ? 'border-red-500 focus:ring-red-500' : ''
                      }`}
                    />
                    {errors.asr_time && <p className="text-red-400 text-sm mt-1">{errors.asr_time}</p>}
                  </div>

                  {/* Maghrib */}
                  <div>
                    <label htmlFor="maghrib_time" className="form-label">
                      Maghrib <span className="text-red-400">*</span>
                    </label>
                    <input
                      id="maghrib_time"
                      type="time"
                      value={formData.maghrib_time}
                      onChange={(e) => handleChange('maghrib_time', e.target.value)}
                      className={`input-field w-full ${
                        errors.maghrib_time ? 'border-red-500 focus:ring-red-500' : ''
                      }`}
                    />
                    {errors.maghrib_time && <p className="text-red-400 text-sm mt-1">{errors.maghrib_time}</p>}
                  </div>

                  {/* Isha */}
                  <div>
                    <label htmlFor="isha_time" className="form-label">
                      Isha <span className="text-red-400">*</span>
                    </label>
                    <input
                      id="isha_time"
                      type="time"
                      value={formData.isha_time}
                      onChange={(e) => handleChange('isha_time', e.target.value)}
                      className={`input-field w-full ${
                        errors.isha_time ? 'border-red-500 focus:ring-red-500' : ''
                      }`}
                    />
                    {errors.isha_time && <p className="text-red-400 text-sm mt-1">{errors.isha_time}</p>}
                  </div>

                  {/* Jummah */}
                  <div>
                    <label htmlFor="jummah_time" className="form-label">
                      Jummah (Optional)
                    </label>
                    <input
                      id="jummah_time"
                      type="time"
                      value={formData.jummah_time}
                      onChange={(e) => handleChange('jummah_time', e.target.value)}
                      className={`input-field w-full ${
                        errors.jummah_time ? 'border-red-500 focus:ring-red-500' : ''
                      }`}
                    />
                    {errors.jummah_time && <p className="text-red-400 text-sm mt-1">{errors.jummah_time}</p>}
                  </div>
                </div>
              </div>

              {/* Form Actions */}
              <div className="flex items-center justify-end space-x-4 pt-4 border-t border-[#2A2A2A]">
                <Link
                  href={`/masjids/${masjidId}`}
                  className="btn-secondary"
                >
                  Cancel
                </Link>
                <button
                  type="submit"
                  disabled={loading}
                  className={`btn-primary flex items-center ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  {loading ? (
                    <>
                      <svg className="animate-spin h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      Updating...
                    </>
                  ) : (
                    'Update Masjid'
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}
