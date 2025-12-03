/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          900: "#050509",
          800: "#0b0b11",
        },
      },
      backgroundImage: {
        "radial-spot":
          "radial-gradient(circle at top left, #1d2333 0, #050509 45%, #000 100%)",
        "ring-gradient":
          "conic-gradient(from 180deg at 50% 50%, #22d3ee 0deg, #6366f1 120deg, #ec4899 240deg, #22d3ee 360deg)",
      },
      boxShadow: {
        "glow-cyan": "0 0 35px rgba(34,211,238,0.35)",
        "glass-xl": "0 18px 60px rgba(15,23,42,0.9)",
      },
      borderRadius: {
        "3xl": "1.75rem",
      },
    },
  },
  plugins: [],
}

