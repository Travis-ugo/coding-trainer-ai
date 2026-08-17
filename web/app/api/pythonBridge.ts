import { execFile } from "child_process";
import path from "path";

const PYTHON_API_BASE = process.env.PYTHON_API_URL || "http://127.0.0.1:8000";
const WORKSPACE_ROOT = path.resolve(process.cwd(), "..");

export async function runPythonBridge(
  endpoint: string,
  method: "GET" | "POST" = "GET",
  payload: Record<string, unknown> = {}
): Promise<unknown> {
  const cleanEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;

  // 1. Primary HTTP fetch to standalone Python API server daemon
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 1000);
    const url = `${PYTHON_API_BASE}${cleanEndpoint}`;
    const options: RequestInit = {
      method,
      headers: { "Content-Type": "application/json" },
      signal: controller.signal,
    };
    if (method === "POST") {
      options.body = JSON.stringify(payload);
    }
    const res = await fetch(url, options);
    clearTimeout(timeoutId);

    if (res.ok) {
      return await res.json();
    }
  } catch {
    // Daemon not running or timed out; fall back to safe execFile subprocess bridge
  }

  // 2. Safe execFile subprocess execution (stdin/stdout JSON bridge)
  // No shell string interpolation -> ZERO shell injection vulnerability
  return new Promise((resolve, reject) => {
    const bridgeEndpoint = cleanEndpoint.replace(/^\/api\//, "");
    const child = execFile(
      "python3",
      ["-m", "coding_trainer_ai.bridge", bridgeEndpoint],
      { cwd: WORKSPACE_ROOT },
      (error, stdout) => {
        if (error) {
          return reject(error);
        }
        try {
          const parsed = JSON.parse(stdout);
          resolve(parsed);
        } catch (parseErr) {
          reject(parseErr);
        }
      }
    );

    if (method === "POST" && payload) {
      child.stdin?.write(JSON.stringify(payload));
    }
    child.stdin?.end();
  });
}
