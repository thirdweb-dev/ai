/**
 * Main Tool class implementation for Nebula Tools.
 */

import type { ToolDefinition, ToolParameter, FrameworkAdapter } from './types.js';

/**
 * Tool builder class for creating standardized AI function tools.
 */
export class Tool implements ToolDefinition {
  name: string;
  description: string;
  parameters: ToolParameter[];
  handler: (...args: unknown[]) => Promise<unknown>;
  
  private adapters: Map<string, FrameworkAdapter> = new Map();

  /**
   * Create a new Tool.
   */
  constructor(config: {
    name: string;
    description: string;
    parameters: ToolParameter[];
    handler: (...args: unknown[]) => Promise<unknown>;
  }) {
    this.name = config.name;
    this.description = config.description;
    this.parameters = config.parameters;
    this.handler = config.handler;
  }

  /**
   * Register a framework adapter.
   */
  registerAdapter(adapter: FrameworkAdapter): void {
    this.adapters.set(adapter.name, adapter);
  }

  /**
   * Convert the tool to a framework-specific format.
   */
  forFramework(frameworkName: string): unknown {
    const adapter = this.adapters.get(frameworkName);
    if (!adapter) {
      throw new Error(`No adapter registered for framework: ${frameworkName}`);
    }
    
    return adapter.convertTool(this);
  }
}