import * as fs from 'fs/promises';
import { exec } from 'child_process';
import { promisify } from 'util';
import { z } from 'zod';
import { Tool } from './base';

const execAsync = promisify(exec);

export class ReadTool implements Tool {
  name = 'read_file';
  description = 'Read file contents from the local filesystem. Arguments: path (string).';
  schema = z.object({
    path: z.string().describe('Absolute path to file'),
  });

  async execute(args: { path: string }): Promise<string> {
    try {
      return await fs.readFile(args.path, 'utf-8');
    } catch (error: any) {
      return `Error reading file: ${error.message}`;
    }
  }
}

export class WriteTool implements Tool {
  name = 'write_file';
  description = 'Write content to a file. Arguments: path (string), content (string).';
  schema = z.object({
    path: z.string().describe('Absolute path to file'),
    content: z.string().describe('Content to write'),
  });

  async execute(args: { path: string; content: string }): Promise<string> {
    try {
      await fs.writeFile(args.path, args.content, 'utf-8');
      return `Successfully wrote to ${args.path}`;
    } catch (error: any) {
      return `Error writing file: ${error.message}`;
    }
  }
}

export class BashTool implements Tool {
  name = 'bash';
  description = 'Execute a bash command. Arguments: command (string).';
  schema = z.object({
    command: z.string().describe('Bash command to execute'),
  });

  async execute(args: { command: string }): Promise<string> {
    try {
      const { stdout, stderr } = await execAsync(args.command);
      return stdout + (stderr ? `\nSTDERR:\n${stderr}` : '');
    } catch (error: any) {
      return `Error executing command: ${error.message}`;
    }
  }
}
