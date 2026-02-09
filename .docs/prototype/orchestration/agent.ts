import { ToolRequest, ToolResult } from './types';

export abstract class Agent<Input = any, Output = any> {
  abstract name: string;
  abstract description: string;
  abstract model: string;
  abstract systemPrompt(input: Input): Promise<string>;
  abstract buildUserMessage(input: Input): Promise<string>;
  abstract parseOutput(response: string): Promise<Output>;

  // Optional: Hook for intercepting tool calls before execution
  async preToolExecution(toolCall: ToolRequest): Promise<void> {}
  
  // Optional: Hook for modifying tool results
  async onToolResult(toolCall: ToolRequest, result: ToolResult): Promise<ToolResult> {
    return result;
  }
}
