/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#7c3aed",
        accent: "#f97316",
        success: "#22c55e",
        danger: "#ef4444",
        surface: "#0f172a"
      }
    }
  },
  plugins: []
};
