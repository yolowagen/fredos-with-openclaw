import { definePluginEntry, type AnyAgentTool, type OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";

function normalizeBaseUrl(rawBaseUrl: string | undefined): string {
  const trimmed = rawBaseUrl?.trim() || "http://localhost:8000";
  const withoutTrailingSlash = trimmed.replace(/\/+$/, "");
  return withoutTrailingSlash.endsWith("/api") ? withoutTrailingSlash : `${withoutTrailingSlash}/api`;
}

function readPluginConfigRecord(raw: unknown): Record<string, unknown> {
  return raw && typeof raw === "object" && !Array.isArray(raw)
    ? (raw as Record<string, unknown>)
    : {};
}

function resolveProjectMap(raw: unknown): Record<string, number> {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return {};

  const out: Record<string, number> = {};
  for (const [key, value] of Object.entries(raw as Record<string, unknown>)) {
    const projectId = Number(value);
    if (key && Number.isInteger(projectId) && projectId > 0) {
      out[key] = projectId;
    }
  }
  return out;
}

function resolveBridgeProjectId(
  agentId: string | undefined,
  pluginConfig: Record<string, unknown>,
): number | undefined {
  const projectMap = resolveProjectMap(pluginConfig.projectMap);
  if (agentId) {
    const mapped = projectMap[agentId];
    if (Number.isInteger(mapped) && mapped > 0) {
      return mapped;
    }
  }

  const fallbackProjectId = Number(pluginConfig.fallbackProjectId);
  if (Number.isInteger(fallbackProjectId) && fallbackProjectId > 0) {
    return fallbackProjectId;
  }

  return undefined;
}

async function postBridgeEvent(
  api: OpenClawPluginApi,
  url: string,
  payload: Record<string, unknown>,
): Promise<void> {
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const body = await res.text();
      api.logger.warn?.(
        `fredos bridge call failed (${res.status}) ${url}${body ? `: ${body}` : ""}`,
      );
    }
  } catch (err) {
    api.logger.warn?.(`fredos bridge call failed (${url}): ${String(err)}`);
  }
}

function buildRetrievalPath(mode: string, projectId: number): string {
  switch (mode) {
    case "A":
      return `/retrieve/project-overview/${projectId}`;
    case "C":
      return `/retrieve/research/${projectId}`;
    case "D":
      return "/retrieve/personal-strategy";
    case "B":
    default:
      return `/projects/${projectId}`;
  }
}

async function readJsonResponse(url: string, init?: RequestInit) {
  const res = await fetch(url, init);
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`${init?.method ?? "GET"} ${url} failed with HTTP ${res.status}${body ? `: ${body}` : ""}`);
  }
  return res.json();
}

function createFredosRetrieveContextTool(api: OpenClawPluginApi): AnyAgentTool {
  return {
    name: "fredos_retrieve_context",
    label: "FredOS Retrieve Context",
    description: "Retrieve project overview, tasks, and memory based on FredOS retrieval modes.",
    parameters: {
      type: "object",
      properties: {
        project_id: { type: "number", description: "The FredOS project ID to retrieve." },
        mode: {
          type: "string",
          enum: ["A", "B", "C", "D"],
          description: "Mode A (overview), B (project record), C (research context), D (personal strategy)",
        },
      },
      required: ["project_id", "mode"],
    },
    async execute(_id: string, params: Record<string, unknown>) {
      const mode = String(params.mode ?? "A");
      const projectId = Number(params.project_id ?? 0);
      const endpoint = buildRetrievalPath(mode, projectId);
      const url = `${normalizeBaseUrl(api.pluginConfig?.baseUrl)}${endpoint}`;

      try {
        const res = await fetch(url);
        if (!res.ok) {
          const body = await res.text();
          throw new Error(`GET ${url} failed with HTTP ${res.status}${body ? `: ${body}` : ""}`);
        }

        const data = await res.json();
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ mode, source: url, data }, null, 2),
            },
          ],
        };
      } catch (err: any) {
        return { content: [{ type: "text", text: `FredOS API Error: ${err.message}` }] };
      }
    },
  } as AnyAgentTool;
}

function createFredosListProjectsTool(api: OpenClawPluginApi): AnyAgentTool {
  return {
    name: "fredos_list_projects",
    label: "FredOS List Projects",
    description: "List FredOS projects so the router or memory worker can resolve candidate project scope before retrieval.",
    parameters: {
      type: "object",
      properties: {
        status: { type: "string", description: "Optional project status filter." },
        client_name: { type: "string", description: "Optional client name filter." },
      },
    },
    async execute(_id: string, params: Record<string, unknown>) {
      const url = new URL(`${normalizeBaseUrl(api.pluginConfig?.baseUrl)}/projects`);
      if (typeof params.status === "string" && params.status.trim()) {
        url.searchParams.set("status", params.status.trim());
      }
      if (typeof params.client_name === "string" && params.client_name.trim()) {
        url.searchParams.set("client_name", params.client_name.trim());
      }

      try {
        const data = await readJsonResponse(url.toString());
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ source: url.toString(), data }, null, 2),
            },
          ],
        };
      } catch (err: any) {
        return { content: [{ type: "text", text: `FredOS API Error: ${err.message}` }] };
      }
    },
  } as AnyAgentTool;
}

function createFredosCreateTaskTool(api: OpenClawPluginApi): AnyAgentTool {
  return {
    name: "fredos_create_task",
    label: "FredOS Create Task",
    description: "Create a new task in the FredOS canonical memory store.",
    parameters: {
      type: "object",
      properties: {
        project_id: { type: "number" },
        title: { type: "string" },
        task_type: { type: "string", enum: ["research", "memory_update", "planning", "execution"] },
      },
      required: ["project_id", "title", "task_type"],
    },
    async execute(_id: string, params: Record<string, unknown>) {
      const url = `${normalizeBaseUrl(api.pluginConfig?.baseUrl)}/tasks`;

      try {
        const res = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            project_id: params.project_id,
            title: params.title,
            task_type: params.task_type,
          }),
        });

        if (!res.ok) {
          const body = await res.text();
          throw new Error(`POST ${url} failed with HTTP ${res.status}${body ? `: ${body}` : ""}`);
        }

        const data = await res.json();
        return {
          content: [
            {
              type: "text",
              text: `Task created successfully in FredOS: ID ${data.id}, title "${data.title}"`,
            },
          ],
        };
      } catch (err: any) {
        return { content: [{ type: "text", text: `FredOS API Error: ${err.message}` }] };
      }
    },
  } as AnyAgentTool;
}

function createFredosWriteStructuredTool(api: OpenClawPluginApi): AnyAgentTool {
  return {
    name: "fredos_write_structured",
    label: "FredOS Write Structured",
    description: "Write governed durable records through the FredOS service layer wrapper.",
    parameters: {
      type: "object",
      properties: {
        record_type: { type: "string", enum: ["task", "decision", "knowledge"] },
        project_id: { type: "number" },
        title: { type: "string" },
        author_agent: { type: "string" },
        rationale: { type: "string" },
        task_id: { type: "number" },
        summary: { type: "string" },
        content: { type: "string" },
        recommendations: { type: "string" },
        confidence: { type: "number" },
        source_refs: { type: "string" },
      },
      required: ["record_type", "project_id", "title", "author_agent", "rationale"],
    },
    async execute(_id: string, params: Record<string, unknown>) {
      const url = `${normalizeBaseUrl(api.pluginConfig?.baseUrl)}/fredos/write-structured`;

      try {
        const data = await readJsonResponse(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(params),
        });
        return {
          content: [{ type: "text", text: JSON.stringify({ source: url, data }, null, 2) }],
        };
      } catch (err: any) {
        return { content: [{ type: "text", text: `FredOS API Error: ${err.message}` }] };
      }
    },
  } as AnyAgentTool;
}

function createFredosUpdateTaskTool(api: OpenClawPluginApi): AnyAgentTool {
  return {
    name: "fredos_update_task",
    label: "FredOS Update Task",
    description: "Update task state through the governed FredOS task wrapper.",
    parameters: {
      type: "object",
      properties: {
        task_id: { type: "number" },
        author_agent: { type: "string" },
        rationale: { type: "string" },
        status: { type: "string" },
        priority: { type: "string" },
        owner_type: { type: "string" },
        owner_name: { type: "string" },
        needs_research: { type: "boolean" },
        needs_execution: { type: "boolean" },
      },
      required: ["task_id", "author_agent", "rationale"],
    },
    async execute(_id: string, params: Record<string, unknown>) {
      const taskId = Number(params.task_id ?? 0);
      const url = `${normalizeBaseUrl(api.pluginConfig?.baseUrl)}/fredos/tasks/${taskId}`;
      const { task_id, ...body } = params;

      try {
        const data = await readJsonResponse(url, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        });
        return {
          content: [{ type: "text", text: JSON.stringify({ source: url, data }, null, 2) }],
        };
      } catch (err: any) {
        return { content: [{ type: "text", text: `FredOS API Error: ${err.message}` }] };
      }
    },
  } as AnyAgentTool;
}

function createFredosLinkEntitiesTool(api: OpenClawPluginApi): AnyAgentTool {
  return {
    name: "fredos_link_entities",
    label: "FredOS Link Entities",
    description: "Create governed entity or memory links through the FredOS service layer.",
    parameters: {
      type: "object",
      properties: {
        author_agent: { type: "string" },
        relation_type: { type: "string" },
        from_memory_id: { type: "number" },
        to_memory_id: { type: "number" },
        project_id: { type: "number" },
        task_id: { type: "number" },
        rationale: { type: "string" },
      },
      required: ["author_agent", "relation_type", "rationale"],
    },
    async execute(_id: string, params: Record<string, unknown>) {
      const url = `${normalizeBaseUrl(api.pluginConfig?.baseUrl)}/fredos/link-entities`;

      try {
        const data = await readJsonResponse(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(params),
        });
        return {
          content: [{ type: "text", text: JSON.stringify({ source: url, data }, null, 2) }],
        };
      } catch (err: any) {
        return { content: [{ type: "text", text: `FredOS API Error: ${err.message}` }] };
      }
    },
  } as AnyAgentTool;
}

export default definePluginEntry({
  id: "fredos",
  name: "FredOS Mainframe",
  description: "Grants agents access to the FredOS L0-L4 canonical memory architecture.",
  register(api: OpenClawPluginApi) {
    api.registerTool(createFredosRetrieveContextTool(api), { optional: false });
    api.registerTool(createFredosListProjectsTool(api), { optional: false });
    api.registerTool(createFredosCreateTaskTool(api), { optional: false });
    api.registerTool(createFredosWriteStructuredTool(api), { optional: false });
    api.registerTool(createFredosUpdateTaskTool(api), { optional: false });
    api.registerTool(createFredosLinkEntitiesTool(api), { optional: false });

    const bridgeBaseUrl = normalizeBaseUrl(api.pluginConfig?.baseUrl);
    const pluginConfig = readPluginConfigRecord(api.pluginConfig);

    api.on("agent_end", async (event, ctx) => {
      try {
        const messages = event.messages as Array<{ role?: string; content?: unknown }>;
        if (!messages || messages.length === 0) return;

        let lastUser = "";
        let lastAssistant = "";
        const toolCalls: Array<{ name: string }> = [];

        for (let i = messages.length - 1; i >= 0; i--) {
          const msg = messages[i];
          const role = msg?.role;
          const content =
            typeof msg?.content === "string"
              ? msg.content
              : Array.isArray(msg?.content)
                ? (msg.content as Array<{ type?: string; text?: string }>)
                    .filter((c) => c.type === "text")
                    .map((c) => c.text ?? "")
                    .join("\n")
                : "";

          if (role === "assistant" && !lastAssistant && content.trim()) {
            lastAssistant = content.trim();
          }
          if (role === "user" && !lastUser && content.trim()) {
            lastUser = content.trim();
          }
          if (role === "assistant" && Array.isArray(msg?.content)) {
            for (const block of msg.content as Array<{ type?: string; name?: string }>) {
              if (block.type === "tool_use" && block.name) {
                toolCalls.push({ name: block.name });
              }
            }
          }
          if (lastUser && lastAssistant) break;
        }

        if (!lastUser && !lastAssistant) return;

        const sessionId = ctx.sessionId ?? "unknown";
        const sessionKey = ctx.sessionKey ?? "unknown";
        const agentId = ctx.agentId ?? "unknown";
        const projectId = resolveBridgeProjectId(agentId, pluginConfig);

        await postBridgeEvent(api, `${bridgeBaseUrl}/bridge/ingest-turn`, {
          openclaw_session_id: sessionId,
          openclaw_session_key: sessionKey,
          openclaw_agent_id: agentId,
          project_id: projectId,
          user_message: lastUser || "(no user message)",
          assistant_message: lastAssistant || "(no assistant message)",
          tool_calls: toolCalls.length > 0 ? toolCalls : undefined,
          duration_ms: event.durationMs,
          success: event.success,
        });
      } catch {
        // Fire-and-forget, never block OpenClaw pipeline
      }
    });

    api.on("after_compaction", async (event, ctx) => {
      try {
        const sessionId = ctx.sessionId ?? "unknown";
        const sessionKey = ctx.sessionKey ?? "unknown";
        const agentId = ctx.agentId ?? "unknown";
        const projectId = resolveBridgeProjectId(agentId, pluginConfig);

        await postBridgeEvent(api, `${bridgeBaseUrl}/bridge/ingest-summary`, {
          openclaw_session_id: sessionId,
          openclaw_session_key: sessionKey,
          openclaw_agent_id: agentId,
          project_id: projectId,
          summary_text: `[Compaction] ${event.compactedCount} messages compacted from ${event.messageCount} total. Token count: ${event.tokenCount ?? "unknown"}.`,
          message_count: event.messageCount,
          compacted_count: event.compactedCount,
        });
      } catch {
        // Fire-and-forget
      }
    });

    api.on("before_reset", async (event, ctx) => {
      try {
        const sessionId = ctx.sessionId ?? "unknown";
        const sessionKey = ctx.sessionKey ?? "unknown";
        const agentId = ctx.agentId ?? "unknown";
        const projectId = resolveBridgeProjectId(agentId, pluginConfig);

        await postBridgeEvent(api, `${bridgeBaseUrl}/bridge/finalize-session`, {
          openclaw_session_id: sessionId,
          openclaw_session_key: sessionKey,
          openclaw_agent_id: agentId,
          project_id: projectId,
          reason: event.reason ?? "reset",
        });
      } catch {
        // Fire-and-forget
      }
    });

    api.on("session_end", async (event, ctx) => {
      try {
        const sessionId = event.sessionId ?? ctx.sessionId ?? "unknown";
        const sessionKey = event.sessionKey ?? ctx.sessionKey ?? "unknown";
        const agentId = ctx.agentId ?? "unknown";
        const projectId = resolveBridgeProjectId(agentId, pluginConfig);

        await postBridgeEvent(api, `${bridgeBaseUrl}/bridge/finalize-session`, {
          openclaw_session_id: sessionId,
          openclaw_session_key: sessionKey,
          openclaw_agent_id: agentId,
          project_id: projectId,
          reason: "session_end",
        });
      } catch {
        // Fire-and-forget
      }
    });
  },
});
