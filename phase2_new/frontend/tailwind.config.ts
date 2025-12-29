import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'islamic-green': {
          DEFAULT: '#006747',
          50: '#e6f2ed',
          100: '#ccede0',
          200: '#99dbc1',
          300: '#66c8a2',
          400: '#33b683',
          500: '#006747',
          600: '#005239',
          700: '#003d2b',
          800: '#00291d',
          900: '#00140e',
        },
        'islamic-gold': {
          DEFAULT: '#D4AF37',
          light: '#F4E5BC',
          dark: '#B8942A',
        },
        'salaat-black': {
          DEFAULT: '#000000',
          light: '#1A1A1A',
          lighter: '#2A2A2A',
        },
        'salaat-orange': {
          DEFAULT: '#FF6B35',
          light: '#FF8C61',
          dark: '#E05A2C',
        },
        'salaat-white': {
          DEFAULT: '#FFFFFF',
          off: '#F5F5F5',
          gray: '#E5E5E5',
        },
      },
    },
  },
  plugins: [],
}
export default config
