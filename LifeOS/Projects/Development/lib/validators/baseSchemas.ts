import { z } from 'zod';

// Core validation schemas
export const EmailSchema = z.string().email();
export const PasswordSchema = z.string().min(8);
export const IdSchema = z.string().uuid();

// API request schemas
export const UserCreateSchema = z.object({
  email: EmailSchema,
  password: PasswordSchema,
  name: z.string().min(2)
});

export const UserUpdateSchema = UserCreateSchema.partial();