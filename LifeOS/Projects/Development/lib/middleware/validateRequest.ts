import { NextRequest, NextResponse } from 'next/server';
import { ZodError, ZodSchema } from 'zod';

/**
 * validateRequest.ts - Middleware for Zod schema validation
 * 
 * Usage:
 * import { validateRequest } from '@/lib/middleware/validateRequest';
 * import { UserCreateSchema } from '@/lib/validators/baseSchemas';
 * 
 * export async function POST(req: NextRequest) {
 *   const validation = await validateRequest(UserCreateSchema)(req);
 *   if (validation) return validation;
 *   // Proceed with valid data...
 * }
 */

export function validateRequest(schema: ZodSchema) {
  return async (req: NextRequest) => {
    try {
      const body = await req.json();
      const validated = await schema.parseAsync(body);
      req.validatedData = validated;
      return null;
    } catch (error) {
      if (error instanceof ZodError) {
        return NextResponse.json(
          { error: 'Validation failed', issues: error.errors },
          { status: 400 }
        );
      }
      return NextResponse.json(
        { error: 'Invalid request format' },
        { status: 400 }
      );
    }
  };
}

// Augment NextRequest type with validatedData
declare module 'next/server' {
  interface NextRequest {
    validatedData?: unknown;
  }
}