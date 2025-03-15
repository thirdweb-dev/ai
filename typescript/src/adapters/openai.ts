/**
 * OpenAI adapter for Nebula Tools.
 */

import type { FrameworkAdapter, ToolDefinition, ToolParameter } from '../types.js';

/**
 * Adapter for OpenAI function tools.
 */
export class OpenAIAdapter implements FrameworkAdapter {
  name = 'openai';

  /**
   * Convert a tool to OpenAI function format.
   */
  convertTool(tool: ToolDefinition): Record<string, unknown> {
    return {
      type: 'function',
      function: {
        name: tool.name,
        description: tool.description,
        parameters: this.convertParameters(tool.parameters),
      },
    };
  }

  /**
   * Convert tool parameters to OpenAI parameters schema.
   */
  private convertParameters(parameters: ToolParameter[]): Record<string, unknown> {
    const properties: Record<string, Record<string, unknown>> = {};
    const required: string[] = [];

    for (const param of parameters) {
      properties[param.name] = {
        type: param.type,
        description: param.description,
      };

      if (param.enum) {
        // @ts-expect-error
        properties[param.name].enum = param.enum;
      }

      if (param.required !== false) {
        required.push(param.name);
      }
    }

    return {
      type: 'object',
      properties,
      required,
    };
  }
}