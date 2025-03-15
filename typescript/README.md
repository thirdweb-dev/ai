# Nebula Tools for TypeScript

AI function tools definition for TypeScript that provides a unified way to define tools and adapters to different AI frameworks.

## Installation

```bash
npm install nebula-tools-typescript
# or
yarn add nebula-tools-typescript
# or
pnpm add nebula-tools-typescript
```

## Usage

```typescript
import { Tool, OpenAIAdapter } from 'nebula-tools-typescript';

// Define a tool
const calculatorTool = new Tool({
  name: 'calculator',
  description: 'Perform a calculation',
  parameters: [
    {
      name: 'expression',
      type: 'string',
      description: 'The mathematical expression to calculate',
      required: true
    }
  ],
  handler: async ({ expression }) => {
    // In a real application, use a safer evaluation method
    const result = eval(expression);
    return { result };
  }
});

// Register an adapter
calculatorTool.registerAdapter(new OpenAIAdapter());

// Convert to OpenAI format
const openaiTool = calculatorTool.forFramework('openai');

// Use with an OpenAI client
// await openai.chat.completions.create({
//   model: "gpt-4-turbo",
//   messages: [{ role: "user", content: "Calculate 2+2" }],
//   tools: [openaiTool],
// });
```

## Features

- Define tools once, use them across multiple AI frameworks
- Consistent API across languages
- Type-safe tool definitions
- Extensible adapter system for different AI frameworks

## Available Adapters

- OpenAI
- (More coming soon)

## Development

```bash
# Install dependencies
pnpm install

# Build
pnpm build

# Test
pnpm test

# Lint
pnpm lint
```

## License

MIT