import { Agent } from './agent';
import { ToolRequest, ToolResult, RunnerConfig } from './types';
import Anthropic from '@anthropic-ai/sdk';
import { ReadTool, WriteTool, BashTool } from './tools/io';

export class BlackboxRunner {
  private client: Anthropic;
  private tools = [new ReadTool(), new WriteTool(), new BashTool()];

  constructor(private config: RunnerConfig) {
    this.client = new Anthropic({ apiKey: config.apiKey });
  }

  async run<I, O>(agent: Agent<I, O>, input: I): Promise<O> {
    console.log(`[Runner] Starting agent: ${agent.name}`);
    
    // Prepare initial context
    const system = await agent.systemPrompt(input);
    const userMsg = await agent.buildUserMessage(input);
    
    let messages: Anthropic.MessageParam[] = [
      { role: 'user', content: userMsg }
    ];

    let iterations = 0;
    const MAX_ITERATIONS = this.config.maxIterations || 10;

    while (iterations < MAX_ITERATIONS) {
      iterations++;
      console.log(`[Runner] Iteration ${iterations}...`);

      const response = await this.client.messages.create({
        model: agent.model,
        max_tokens: 4096,
        system: system,
        messages: messages,
        tools: this.tools.map(t => ({
          name: t.name,
          description: t.description,
          input_schema: { type: 'object', properties: {} } // Simplified for now, should map Zod schema
        }))
      });

      // Handle response content
      const content = response.content;
      const textBlock = content.find(b => b.type === 'text');
      if (textBlock) {
        console.log(`[Runner] LLM Output: ${textBlock.text.substring(0, 100)}...`);
      }

      // Check for tool calls
      const toolCalls = content.filter(b => b.type === 'tool_use');
      
      if (toolCalls.length === 0) {
        // No tools, assume final answer
        if (textBlock) {
            return await agent.parseOutput(textBlock.text);
        }
        throw new Error('No final text output from LLM');
      }

      // Execute tools
      const toolResults: Anthropic.ToolResultBlockParam[] = [];
      
      for (const call of toolCalls) {
        if (call.type !== 'tool_use') continue;
        
        const tool = this.tools.find(t => t.name === call.name);
        let result = "";
        
        if (tool) {
          console.log(`[Runner] Executing tool: ${tool.name}`);
          try {
             result = await tool.execute(call.input);
          } catch (e: any) {
             result = `Error: ${e.message}`;
          }
        } else {
          result = `Error: Tool not found: ${call.name}`;
        }

        toolResults.push({
          type: 'tool_result',
          tool_use_id: call.id,
          content: result
        });
      }

      // Append assistant response and tool results to history
      messages.push({ role: 'assistant', content: content });
      messages.push({ role: 'user', content: toolResults });
    }

    throw new Error(`Max iterations (${MAX_ITERATIONS}) reached without final answer.`);
  }
}
