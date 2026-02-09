import { z, ZodSchema } from 'zod';

export interface Tool {
  name: string;
  description: string;
  schema: ZodSchema;
  execute(args: any): Promise<string>;
}
