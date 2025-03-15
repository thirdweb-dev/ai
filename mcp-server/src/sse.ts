import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import { Hono } from "hono";
import { serve, type HttpBindings } from "@hono/node-server";
import { createServer } from "./mcp.js";

const app = new Hono<{ Bindings: HttpBindings }>();

const { server } = createServer();

let transport: SSEServerTransport;

app.get("/sse", async (c) => {
  transport = new SSEServerTransport("/message", c.env.outgoing);
  await server.connect(transport);

  server.onclose = async () => {
    await server.close();
    process.exit(0);
  };
});

app.post("/message", async (c) => {
  await transport.handlePostMessage(c.env.incoming, c.env.outgoing);
});

const PORT = Number(process.env.PORT || 3000);
const HOSTNAME = process.env.HOSTNAME || "0.0.0.0";
serve({ fetch: app.fetch, port: PORT, hostname: HOSTNAME });