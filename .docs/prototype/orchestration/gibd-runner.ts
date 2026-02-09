import { BlackboxRunner } from './runner';
import { Agent } from './agent';
import * as dotenv from 'dotenv';
import { z } from 'zod';

dotenv.config();

// Simple CLI Simulation
async function main() {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    console.error('Missing ANTHROPIC_API_KEY in .env');
    process.exit(1);
  }

  const runner = new BlackboxRunner({ apiKey, maxIterations: 5 });

  // Test: Echo Agent
  class EchoAgent extends Agent<string, string> {
    name = 'echo';
    description = 'Echoes the user message back.';
    model = 'claude-3-haiku-20240307';
    
    async systemPrompt(input: string): Promise<string> {
      return 'You are an echo bot. Repeat the user message EXACTLY.';
    }
    
    async buildUserMessage(input: string): Promise<string> {
      return `User said: "${input}"`;
    }
    
    async parseOutput(response: string): Promise<string> {
      return response.trim();
    }
  }

  const agent = new EchoAgent();
  const input = process.argv[2] || 'Hello GIBD!';

  try {
    const output = await runner.run(agent, input);
    console.log(`\n[FINAL OUTPUT]: ${output}`);
  } catch (error) {
    console.error(error);
  }
}

main();
