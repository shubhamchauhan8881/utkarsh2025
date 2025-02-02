/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors:{
        "purple":"#D300FF"
      },
      fontFamily:{
        "Cartesian": "Cartesian",
        "Sterion":"Sterion",
        "AquireLight":"AquireLight",
        "AquireBold":"AquireBold",
        "Zhabuki":"Zhabuki",
      }
    },
  },
  plugins: [],
}

