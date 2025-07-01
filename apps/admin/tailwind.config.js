/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        coffee: {
          orange: '#FE9870',
          cream: '#F4E6CD',
          dark: '#1B2037',
          gray: '#D1D2D7',
        }
      },
      fontFamily: {
        'display': ['Montserrat', 'sans-serif'],
        'body': ['Kumbh Sans', 'sans-serif'],
      }
    },
  },
  plugins: [],
}