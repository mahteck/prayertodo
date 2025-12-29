'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import api from '@/lib/api'
import { MasjidFormData } from '@/lib/types'
import FormInput from '@/components/forms/FormInput'
import FormTextarea from '@/components/forms/FormTextarea'

export default function NewMasjidPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [errors, setErrors] = useState<Record<string, string>>({})

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

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {}

    if (!formData.name.trim()) {
      newErrors.name = 'Masjid name is required'
    }

    if (!formData.area_name.trim()) {
      newErrors.area_name = 'Area is required'
    }

    // Validate prayer times format (HH:MM)
    const timeRegex = /^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/
    const requiredTimes: (keyof MasjidFormData)[] = ['fajr_time', 'dhuhr_time', 'asr_time', 'maghrib_time', 'isha_time']

    requiredTimes.forEach(field => {
      const value = formData[field]
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

      await api.createMasjid(formData)

      // Success - navigate to masjids list
      router.push('/masjids')
    } catch (err: any) {
      console.error('Error creating masjid:', err)
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
        setError('Failed to create masjid. Please try again.')
      }
      setLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData({ ...formData, [name]: value })
    // Clear error for this field
    if (errors[name]) {
      setErrors({ ...errors, [name]: '' })
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
            <h1 className="text-3xl font-bold text-white">Add New Masjid</h1>
            <p className="text-gray-400 mt-1">Add a masjid with prayer times</p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 pb-8">
        <div className="max-w-3xl mx-auto">
          {/* Error Message */}
          {error && (
            <div className="card-dark border-red-800 mb-6">
              <div className="flex items-center">
                <svg
                  className="w-5 h-5 text-red-400 mr-2"
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
                <p className="text-red-400">{error}</p>
              </div>
            </div>
          )}

          {/* Form */}
          <div className="card-dark">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Basic Information */}
              <div>
                <h2 className="text-xl font-bold text-white mb-4">Basic Information</h2>

                <FormInput
                  label="Masjid Name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="e.g., Masjid Al-Huda"
                  required
                  error={errors.name}
                />

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <FormInput
                    label="Area"
                    name="area_name"
                    value={formData.area_name}
                    onChange={handleChange}
                    placeholder="e.g., DHA Phase 5"
                    required
                    error={errors.area_name}
                  />

                  <FormInput
                    label="City"
                    name="city"
                    value={formData.city || ''}
                    onChange={handleChange}
                    placeholder="e.g., Karachi"
                  />
                </div>

                <FormTextarea
                  label="Address"
                  name="address"
                  value={formData.address || ''}
                  onChange={handleChange}
                  placeholder="Full address..."
                  rows={2}
                />

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <FormInput
                    label="Imam Name"
                    name="imam_name"
                    value={formData.imam_name || ''}
                    onChange={handleChange}
                    placeholder="Imam's name"
                  />

                  <FormInput
                    label="Phone"
                    name="phone"
                    type="tel"
                    value={formData.phone || ''}
                    onChange={handleChange}
                    placeholder="Contact number"
                  />
                </div>
              </div>

              {/* Prayer Times */}
              <div>
                <h2 className="text-xl font-bold text-white mb-4">
                  Prayer Times <span className="text-sm text-gray-400">(24-hour format: HH:MM)</span>
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <FormInput
                    label="Fajr"
                    name="fajr_time"
                    type="time"
                    value={formData.fajr_time}
                    onChange={handleChange}
                    required
                    error={errors.fajr_time}
                  />

                  <FormInput
                    label="Dhuhr"
                    name="dhuhr_time"
                    type="time"
                    value={formData.dhuhr_time}
                    onChange={handleChange}
                    required
                    error={errors.dhuhr_time}
                  />

                  <FormInput
                    label="Asr"
                    name="asr_time"
                    type="time"
                    value={formData.asr_time}
                    onChange={handleChange}
                    required
                    error={errors.asr_time}
                  />

                  <FormInput
                    label="Maghrib"
                    name="maghrib_time"
                    type="time"
                    value={formData.maghrib_time}
                    onChange={handleChange}
                    required
                    error={errors.maghrib_time}
                  />

                  <FormInput
                    label="Isha"
                    name="isha_time"
                    type="time"
                    value={formData.isha_time}
                    onChange={handleChange}
                    required
                    error={errors.isha_time}
                  />

                  <FormInput
                    label="Jummah (Optional)"
                    name="jummah_time"
                    type="time"
                    value={formData.jummah_time || ''}
                    onChange={handleChange}
                    error={errors.jummah_time}
                  />
                </div>
              </div>

              {/* Form Actions */}
              <div className="flex items-center justify-end space-x-4 pt-4 border-t border-salaat-black-lighter">
                <Link
                  href="/masjids"
                  className="btn-secondary"
                >
                  Cancel
                </Link>
                <button
                  type="submit"
                  disabled={loading}
                  className="btn-primary disabled:bg-salaat-orange-dark disabled:opacity-50 flex items-center"
                >
                  {loading ? (
                    <>
                      <svg className="animate-spin h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      Saving...
                    </>
                  ) : (
                    'Save Masjid'
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
