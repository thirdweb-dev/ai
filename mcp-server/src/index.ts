#!/usr/bin/env node

const mode = process.argv[process.argv.length - 1];
if (mode === "sse") {
  import("./sse.js");
} else {
  import("./stdio.js");
}

