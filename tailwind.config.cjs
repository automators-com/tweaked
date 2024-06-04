/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}"],
  theme: {
    extend: {},
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
  daisyui: {
    themes: [
      {
        automators: {
          primary: "#FFFFFF",
          secondary: "#482B7D",
          accent: "#449BA7",
          "accent-content": "#FFFFFF",
          neutral: "#F2F2F2",
          "base-100": "#1B1C36",
          "base-200": "#282943",
          "base-300": "#282943",
        },
      },
      "light",
      "dark",
      "cupcake",
      "garden",
    ],
    base: true, // applies background color and foreground color for root element by default
    styled: true, // include daisyUI colors and design decisions for all components
    utils: true, // adds responsive and modifier utility classes
    logs: true, // Shows info about daisyUI version and used config in the console when building your CSS
    themeRoot: ":root", // The element that receives theme color CSS variables
  },
};
