import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import { createVuePlugin } from "vite-plugin-vue2";

const env = process.env;
const target = env.BACKEND_URL || "http://localhost:8000/";

export default defineConfig({
  plugins: [createVuePlugin()],
  server: {
    proxy: {
      "/api": target,
    },
  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
});
