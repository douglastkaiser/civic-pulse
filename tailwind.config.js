/** @type {import('tailwindcss').Config} */

function withOpacity(varName) {
  return ({ opacityValue }) => {
    if (opacityValue !== undefined) {
      return `rgb(var(${varName}) / ${opacityValue})`
    }
    return `rgb(var(${varName}))`
  }
}

export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    fontSize: {
      xs: '0.75rem',
      sm: '0.85rem',
      base: '0.9375rem',
      lg: '1.0625rem',
      xl: '1.1875rem',
      '2xl': '1.375rem',
      '3xl': '1.625rem',
    },
    extend: {
      colors: {
        'bg-primary': withOpacity('--bg-primary'),
        'bg-panel': withOpacity('--bg-panel'),
        'bg-elevated': withOpacity('--bg-elevated'),
        'border': withOpacity('--border'),
        'text-primary': withOpacity('--text-primary'),
        'text-secondary': withOpacity('--text-secondary'),
        'text-tertiary': withOpacity('--text-tertiary'),
        'accent-blue': withOpacity('--accent-blue'),
        'accent-green': withOpacity('--accent-green'),
        'accent-amber': withOpacity('--accent-amber'),
        'accent-red': withOpacity('--accent-red'),
        'accent-purple': withOpacity('--accent-purple'),
        'quad-act': withOpacity('--quad-act'),
        'quad-know': withOpacity('--quad-know'),
        'quad-watch': withOpacity('--quad-watch'),
        'quad-bg': withOpacity('--quad-bg'),
      },
      fontFamily: {
        mono: ['var(--font-mono)', 'monospace'],
        sans: ['var(--font-sans)', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
