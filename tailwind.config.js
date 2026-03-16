/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    fontSize: {
      xs: '0.7rem',
      sm: '0.8rem',
      base: '0.875rem',
      lg: '1rem',
      xl: '1.125rem',
      '2xl': '1.25rem',
      '3xl': '1.5rem',
    },
    extend: {
      colors: {
        'bg-primary': '#0a0e17',
        'bg-panel': '#111827',
        'bg-elevated': '#1a2236',
        'border': '#1e2d4a',
        'text-primary': '#e2e8f0',
        'text-secondary': '#64748b',
        'text-tertiary': '#475569',
        'accent-blue': '#3b82f6',
        'accent-green': '#22c55e',
        'accent-amber': '#f59e0b',
        'accent-red': '#ef4444',
        'accent-purple': '#a855f7',
        'quad-act': '#22c55e',
        'quad-know': '#3b82f6',
        'quad-watch': '#f59e0b',
        'quad-bg': '#475569',
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', 'monospace'],
        sans: ['"DM Sans"', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
