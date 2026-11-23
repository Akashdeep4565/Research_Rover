/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  prefix: "",
  theme: {
  	container: {
  		center: true,
  		padding: '2rem',
  		screens: {
  			'2xl': '1400px'
  		}
  	},
  	extend: {
  		colors: {
  			border: 'hsl(var(--border))',
  			input: 'hsl(var(--input))',
  			ring: 'hsl(var(--ring))',
  			background: 'hsl(var(--background))',
  			foreground: 'hsl(var(--foreground))',
  			destructive: {
  				DEFAULT: 'hsl(var(--destructive))',
  				foreground: 'hsl(var(--destructive-foreground))'
  			},
  			muted: {
  				DEFAULT: 'hsl(var(--muted))',
  				foreground: 'hsl(var(--muted-foreground))'
  			},
  			accent: {
  				DEFAULT: 'hsl(var(--accent))',
  				foreground: 'hsl(var(--accent-foreground))'
  			},
  			popover: {
  				DEFAULT: 'hsl(var(--popover))',
  				foreground: 'hsl(var(--popover-foreground))'
  			},
  			card: {
  				DEFAULT: 'hsl(var(--card))',
  				foreground: 'hsl(var(--card-foreground))'
  			},
  			chart: {
  				'1': 'hsl(var(--chart-1))',
  				'2': 'hsl(var(--chart-2))',
  				'3': 'hsl(var(--chart-3))',
  				'4': 'hsl(var(--chart-4))',
  				'5': 'hsl(var(--chart-5))'
  			},
  			// Radiant Luminary Surface Tokens
  			surface: 'var(--surface, #faf8ff)',
  			'surface-dim': 'var(--surface-dim, #d2d9f4)',
  			'surface-bright': 'var(--surface-bright, #faf8ff)',
  			'surface-container-lowest': 'var(--surface-container-lowest, #ffffff)',
  			'surface-container-low': 'var(--surface-container-low, #f2f3ff)',
  			'surface-container': 'var(--surface-container, #eaedff)',
  			'surface-container-high': 'var(--surface-container-high, #e2e7ff)',
  			'surface-container-highest': 'var(--surface-container-highest, #dae2fd)',
  			'surface-variant': 'var(--surface-variant, #dae2fd)',
  			'surface-tint': 'var(--surface-tint, #5148d7)',
  			'on-surface': 'var(--on-surface, #131b2e)',
  			'on-surface-variant': 'var(--on-surface-variant, #464554)',
  			'inverse-surface': 'var(--inverse-surface, #283044)',
  			'inverse-on-surface': 'var(--inverse-on-surface, #eef0ff)',
  			outline: 'var(--outline, #777586)',
  			'outline-variant': 'var(--outline-variant, #c7c4d7)',

  			// Radiant Luminary Primary Tokens
  			primary: {
  				DEFAULT: 'hsl(var(--primary))',
  				foreground: 'hsl(var(--primary-foreground))',
  				container: 'var(--brand-primary-container, #4338ca)',
  				fixed: 'var(--brand-primary-fixed, #e3dfff)',
  				'fixed-dim': 'var(--brand-primary-fixed-dim, #c3c0ff)',
  			},
  			'primary-container': 'var(--brand-primary-container, #4338ca)',
  			'primary-fixed': 'var(--brand-primary-fixed, #e3dfff)',
  			'primary-fixed-dim': 'var(--brand-primary-fixed-dim, #c3c0ff)',
  			'on-primary': 'var(--on-brand-primary, #ffffff)',
  			'on-primary-container': 'var(--on-brand-primary-container, #c1beff)',
  			'on-primary-fixed': 'var(--on-brand-primary-fixed, #100069)',
  			'on-primary-fixed-variant': 'var(--on-brand-primary-fixed-variant, #372abf)',
  			'inverse-primary': '#c3c0ff',

  			// Radiant Luminary Secondary Tokens
  			secondary: {
  				DEFAULT: 'hsl(var(--secondary))',
  				foreground: 'hsl(var(--secondary-foreground))',
  				container: 'var(--brand-secondary-container, #86f2e4)',
  				fixed: 'var(--brand-secondary-fixed, #89f5e7)',
  				'fixed-dim': 'var(--brand-secondary-fixed-dim, #6bd8cb)',
  			},
  			'secondary-container': 'var(--brand-secondary-container, #86f2e4)',
  			'secondary-fixed': 'var(--brand-secondary-fixed, #89f5e7)',
  			'secondary-fixed-dim': 'var(--brand-secondary-fixed-dim, #6bd8cb)',
  			'on-secondary': 'var(--on-brand-secondary, #ffffff)',
  			'on-secondary-container': 'var(--on-brand-secondary-container, #006f66)',
  			'on-secondary-fixed': 'var(--on-brand-secondary-fixed, #00201d)',
  			'on-secondary-fixed-variant': 'var(--on-brand-secondary-fixed-variant, #005049)',

  			// Radiant Luminary Tertiary Tokens
  			tertiary: {
  				DEFAULT: 'var(--brand-tertiary, #7b0022)',
  				container: 'var(--brand-tertiary-container, #a60031)',
  				fixed: 'var(--brand-tertiary-fixed, #ffdadb)',
  				'fixed-dim': 'var(--brand-tertiary-fixed-dim, #ffb2b7)',
  			},
  			'tertiary-container': 'var(--brand-tertiary-container, #a60031)',
  			'tertiary-fixed': 'var(--brand-tertiary-fixed, #ffdadb)',
  			'tertiary-fixed-dim': 'var(--brand-tertiary-fixed-dim, #ffb2b7)',
  			'on-tertiary': 'var(--on-brand-tertiary, #ffffff)',
  			'on-tertiary-container': 'var(--on-brand-tertiary-container, #ffb0b5)',
  			'on-tertiary-fixed': 'var(--on-brand-tertiary-fixed, #40000d)',
  			'on-tertiary-fixed-variant': 'var(--on-brand-tertiary-fixed-variant, #92002a)',
  		},
  		borderRadius: {
  			lg: 'var(--radius)',
  			md: 'calc(var(--radius) - 2px)',
  			sm: 'calc(var(--radius) - 4px)'
  		},
  		keyframes: {
  			'accordion-down': {
  				from: {
  					height: '0'
  				},
  				to: {
  					height: 'var(--radix-accordion-content-height)'
  				}
  			},
  			'accordion-up': {
  				from: {
  					height: 'var(--radix-accordion-content-height)'
  				},
  				to: {
  					height: '0'
  				}
  			},
  			'fade-in': {
  				from: {
  					opacity: '0',
  					transform: 'translateY(10px)'
  				},
  				to: {
  					opacity: '1',
  					transform: 'translateY(0)'
  				}
  			},
  			'slide-in': {
  				from: {
  					transform: 'translateX(-100%)'
  				},
  				to: {
  					transform: 'translateX(0)'
  				}
  			},
  			'pulse-glow': {
  				'0%, 100%': {
  					boxShadow: '0 0 5px rgba(59, 130, 246, 0.5)'
  				},
  				'50%': {
  					boxShadow: '0 0 20px rgba(59, 130, 246, 0.8)'
  				}
  			}
  		},
  		animation: {
  			'accordion-down': 'accordion-down 0.2s ease-out',
  			'accordion-up': 'accordion-up 0.2s ease-out',
  			'fade-in': 'fade-in 0.5s ease-out',
  			'slide-in': 'slide-in 0.3s ease-out',
  			'pulse-glow': 'pulse-glow 2s ease-in-out infinite'
  		},
  		fontFamily: {
  			display: [
  				'"Plus Jakarta Sans"',
  				'sans-serif'
  			],
  			sans: [
  				'Inter',
  				'system-ui',
  				'sans-serif'
  			],
  			mono: [
  				'"JetBrains Mono"',
  				'monospace'
  			],
  			'headline-lg': ['"Plus Jakarta Sans"', 'sans-serif'],
  			'headline-md': ['"Plus Jakarta Sans"', 'sans-serif'],
  			'headline-sm': ['"Plus Jakarta Sans"', 'sans-serif'],
  			'title-md': ['"Plus Jakarta Sans"', 'sans-serif'],
  			'display-xl': ['"Plus Jakarta Sans"', 'sans-serif'],
  			'display-lg': ['"Plus Jakarta Sans"', 'sans-serif'],
  			'body-lg': ['Inter', 'sans-serif'],
  			'body-md': ['Inter', 'sans-serif'],
  			'body-sm': ['Inter', 'sans-serif'],
  			'label-md': ['Inter', 'sans-serif'],
  			'label-sm': ['Inter', 'sans-serif'],
  			'code-sm': ['"JetBrains Mono"', 'monospace']
  		},
  		boxShadow: {
  			card: '0 10px 30px -5px rgba(42, 20, 180, 0.04), 0 4px 6px -2px rgba(0, 0, 0, 0.02)',
  			float: '0 20px 40px -10px rgba(42, 20, 180, 0.12), 0 0 1px 1px rgba(255, 255, 255, 0.8)',
  			glass: '0 8px 32px 0 rgba(31, 38, 135, 0.07)',
  			'glow-primary': '0 0 25px rgba(67, 56, 202, 0.25)',
  			'glow-secondary': '0 0 25px rgba(0, 106, 97, 0.25)'
  		},
  		backgroundImage: {
  			'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
  			'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))'
  		}
  	}
  },
  plugins: [require("tailwindcss-animate")],
}