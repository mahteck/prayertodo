'use client'

interface AreaFilterProps {
  areas: string[]
  selectedArea: string | null
  onAreaChange: (area: string | null) => void
}

export default function AreaFilter({ areas, selectedArea, onAreaChange }: AreaFilterProps) {
  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value
    onAreaChange(value === '' ? null : value)
  }

  return (
    <div className="w-full">
      <label htmlFor="areaFilter" className="form-label">
        Filter by Area
      </label>
      <select
        id="areaFilter"
        value={selectedArea || ''}
        onChange={handleChange}
        className="select-field w-full"
      >
        <option value="">All Areas</option>
        {areas.map((area) => (
          <option key={area} value={area}>
            {area}
          </option>
        ))}
      </select>
    </div>
  )
}
