interface FormSelectProps {
  label: string
  name: string
  value: string | number
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void
  options: { value: string | number; label: string }[]
  required?: boolean
  error?: string
  placeholder?: string
}

export default function FormSelect({
  label,
  name,
  value,
  onChange,
  options,
  required = false,
  error,
  placeholder,
}: FormSelectProps) {
  return (
    <div className="mb-4">
      <label htmlFor={name} className="form-label">
        {label}
        {required && <span className="text-salaat-orange ml-1">*</span>}
      </label>
      <select
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        required={required}
        className="select-field w-full"
      >
        {placeholder && (
          <option value="" disabled>
            {placeholder}
          </option>
        )}
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && <p className="error-message">{error}</p>}
    </div>
  )
}
