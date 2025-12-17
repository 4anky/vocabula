import "@vitejs/plugin-react"
import "vite"
import react
import { defineConfig }

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost",
        changeOrigin: true,
      },
    },
  },
});
