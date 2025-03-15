/**
 * Core type definitions for Nebula Tools.
 */

/**
 * Base interface for tool parameters.
 */
export interface ToolParameter {
  name: string;
  type: string;
  description: string;
  required?: boolean;
  enum?: string[];
  default?: unknown;
}

/**
 * Tool definition interface.
 */
export interface ToolDefinition {
  name: string;
  description: string;
  parameters: ToolParameter[];
  handler: (...args: unknown[]) => Promise<unknown>;
}

/**
 * Framework-specific adapter interface.
 */
export interface FrameworkAdapter {
  name: string;
  convertTool: (tool: ToolDefinition) => Record<string, unknown>;
}