/**
 * lib/env.ts
 * Validates and provides typed access to environment variables using Zod.
 * Dependencies: zod (installed via npm)
 */

import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z
    .enum(['development', 'production', 'test'])
    .default('development'),
  DATABASE_URL: z.string().url(),
  API_SECRET: z.string().min(32),
  NEXT_PUBLIC_CLIENT_ID: z.string(),
});

const parsed = envSchema.safeParse(process.env);

if (!parsed.success) {
  console.error(
    '❌ Invalid environment variables:',
    parsed.error.flatten().fieldErrors
  );
  throw new Error('Invalid environment variables');
}

export const env = parsed.data;