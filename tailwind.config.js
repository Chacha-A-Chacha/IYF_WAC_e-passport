/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.{html, js}",  // Path to your Flask templates
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

// npx tailwindcss -i ./app/static/src/input.css -o ./app/static/dist/css/output.css --watch