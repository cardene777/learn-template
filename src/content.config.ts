import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';

export const collections = {
  content: defineCollection({
    loader: glob({ pattern: '**/*.md', base: './.astro-content' }),
  }),
};
