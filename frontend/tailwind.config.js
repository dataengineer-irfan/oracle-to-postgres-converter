/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Strict 9-color palette — no additions allowed
        bg:      '#0B1220',
        panel:   '#111827',
        border:  '#2A3441',
        text:    '#F8FAFC',
        muted:   '#94A3B8',
        primary: '#2563EB',
        success: '#22C55E',
        warning: '#F59E0B',
        error:   '#EF4444',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Menlo', 'Consolas', 'monospace'],
      },
      fontSize: {
        // Locked to spec: 12, 13, 14, 16, 18, 24 — nothing else
        'xs':   ['12px', { lineHeight: '16px' }],
        'sm':   ['13px', { lineHeight: '20px' }],
        'base': ['14px', { lineHeight: '20px' }],
        'lg':   ['16px', { lineHeight: '24px' }],
        'xl':   ['18px', { lineHeight: '28px' }],
        '2xl':  ['24px', { lineHeight: '32px' }],
      },
      borderRadius: {
        // ONE border radius. sm for interactive elements, none for panels.
        'none': '0px',
        DEFAULT: '2px',
        'sm': '2px',
        'md': '2px',
        'lg': '2px',
        'xl': '2px',
        '2xl': '2px',
        'full': '9999px',
      },
      spacing: {
        // 8px grid
        '0.5': '2px',
        '1':   '4px',
        '1.5': '6px',
        '2':   '8px',
        '3':   '12px',
        '4':   '16px',
        '5':   '20px',
        '6':   '24px',
        '8':   '32px',
        '10':  '40px',
        '12':  '48px',
        '16':  '64px',
      },
      boxShadow: {
        // No decorative shadows. Only functional ones.
        'none': 'none',
        'sm': 'none',
        DEFAULT: 'none',
        'md': 'none',
        'lg': 'none',
        'xl': 'none',
        '2xl': 'none',
        // Only dropdown/popup layer shadow — very subtle
        'dropdown': '0 4px 16px rgba(0,0,0,0.5)',
      },
      transitionDuration: {
        DEFAULT: '150ms',
        '150': '150ms',
      },
      height: {
        'header': '36px',
        'tab':    '36px',
        'toolbar':'32px',
        'row':    '24px',
      },
      width: {
        'sidebar': '240px',
        'inspector': '280px',
      }
    },
  },
  plugins: [],
}
