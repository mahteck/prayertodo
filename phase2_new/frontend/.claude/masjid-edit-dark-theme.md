# Masjid Edit Form - Dark Theme Update

## File: /mnt/d/Data/GIAIC/hackathon2_prayertodo/phase2_new/frontend/app/masjids/[id]/edit/page.tsx

## Changes Needed:

### Area and City Section (Lines 217-246)
Replace all:
- `className="block text-sm font-medium text-gray-700 mb-1"` → `className="form-label"`
- `className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500..."` → `className="input-field w-full"`
- `border-gray-300` → remove (already in input-field)
- `text-red-500` (for errors) → `text-red-400`

### Address Section (Lines 248-260)
- Label: `className="form-label"`
- Textarea: `className="textarea-field w-full"`

### Imam and Phone Section (Lines 262-289)
- Labels: `className="form-label"`
- Inputs: `className="input-field w-full"`

### Prayer Times Header (Line 294)
- `className="text-xl font-bold text-gray-800 mb-4"` → `className="text-xl font-bold text-white mb-4"`
- `className="text-sm text-gray-500"` → `className="text-sm text-gray-400"`

### All Prayer Time Inputs (Lines 298-400)
- All labels: `className="form-label"`
- All inputs: `className="input-field w-full ${errors.xxx ? 'border-red-500 focus:ring-red-500' : ''}"`
- All error messages: `text-red-400`

### Form Actions (Lines 403-428)
- Border: `className="flex items-center justify-end space-x-4 pt-4 border-t border-[#2A2A2A]"`
- Cancel button: `className="btn-secondary"`
- Submit button: `className="btn-primary flex items-center ${loading ? 'opacity-50 cursor-not-allowed' : ''}"`
