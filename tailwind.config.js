/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{py,html,js}",
    "./components/**/*.{py,html,js}",
    "./app.py"
  ],
  corePlugins: {
    preflight: false
  },
  theme: {
    extend: {
      colors: {
        brand: {
          deep: '#006A50',
          teal: '#106E98',
          green: '#43A842',
          'green-text': '#2B8530'
        },
        ink: {
          DEFAULT: '#1B1B1B',
          soft: '#5F6B7A',
          muted: '#6B7686'
        },
        page: '#FAFAFA',
        surface: '#FFFFFF',
        line: '#E5E7EB',
        note: {
          bg: '#FBF5DF',
          edge: '#9A8B3C'
        },
        etat: {
          bon: '#43A842',
          moyen: '#F2B705',
          mauvais: '#D64545',
          travaux: '#106E98'
        }
      },
      fontFamily: {
        sans: ['Poppins', 'system-ui', 'sans-serif']
      }
    }
  },
  plugins: []
}
