export type AgentConfig = {
  name: string;
  description: string;
  model: string;
  personaPath: string;
}

export type ToolRequest = {
  id: string;
  name: string;
  input: any;
}

export type ToolResult = {
  tool_use_id: string;
  type: 'tool_result';
  content: string;
  is_error?: boolean;
}

export interface RunnerConfig {
  apiKey: string;
  maxIterations?: number;
}
