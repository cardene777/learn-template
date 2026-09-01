import { defineConfig } from 'astro/config';

export default defineConfig({
  output: 'static',
  build: {
    format: 'preserve',
  },
  markdown: {
    syntaxHighlight: false,
  },
  vite: {
    build: {
      sourcemap: false,
    },
  },
});
