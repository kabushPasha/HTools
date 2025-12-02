import { defineConfig } from 'vite';

export default defineConfig({
  base: "",           // VERY IMPORTANT for itch.io (makes all asset paths relative)
  server: {
    open: true             // auto-open browser when running dev
  },
  build: {
    outDir: 'dist',        // default, but you can change if you want
    emptyOutDir: true
  }
});