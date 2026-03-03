# Confident AI MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![Confident AI](https://img.shields.io/badge/Confident_AI-Platform-purple.svg)](https://confident-ai.com)

The Confident AI MCP Server connects AI-powered tools directly to [Confident AI](https://confident-ai.com), the AI quality platform. This gives AI agents, coding assistants, and chatbots the ability to manage prompts, pull evaluation datasets, inspect production traces, trigger LLM evaluations, annotate outputs, and review test runs — all through natural language from inside your editor.

[Confident AI](https://confident-ai.com) is the backend and persistence layer for [DeepEval](https://github.com/confident-ai/deepeval), the open-source LLM evaluation framework (think: pytest for LLMs). DeepEval runs completely on its own — locally, in CI, wherever you want. Confident AI is the optional layer that adds prompt versioning, centralized datasets, production tracing, cloud evaluations, and human annotations on top. This MCP server gives you direct access to all of it.

### Use Cases

- **Iterate on prompts without leaving your editor.** Pull your latest prompt, tweak the template, push it back, and tag a new version — all from a single conversation with your AI assistant. No tab-switching, no copy-pasting between browser windows.
- **Run an evaluation and act on the results immediately.** Trigger a cloud evaluation against your metric collection, see exactly which test cases failed and why, then use those results to guide your next code change — in one continuous workflow.
- **Use human feedback to drive your next iteration.** Pull annotation data (thumbs up/down, star ratings, expected outputs) that your team left on production traces, and use it as context to decide what to fix or improve next.
- **Debug production issues from where you code.** Inspect traces, drill into individual spans, filter by errors or time range — find out what went wrong in production without opening a dashboard.
- **Evaluate production traffic on the fly.** Pick a trace, thread, or span from production and trigger an evaluation against it right from your editor. No need to set up a test harness.
- **Prep evaluation datasets without context-switching.** Pull your existing datasets from Confident AI and use them in local test runs or agent workflows, or simulate multi-turn conversations to stress-test your chatbot.

Built for developers who want to manage their LLM quality infrastructure from inside AI-powered editors like Cursor, Claude Desktop, and Windsurf — from simple queries to complex multi-step agent workflows.

## Jump Ahead

- [Why MCP for Evals?](#why-mcp-for-evals) — Why this exists and how it connects to Confident AI
- [Prerequisites](#prerequisites) — What you need before you start
- [Quickstart](#quickstart) — Get up and running in under a minute
  - [Cursor](#cursor) · [Claude Code (or Desktop)](#claude-code-or-desktop) · [Windsurf](#windsurf) · [Run Locally](#running-the-server-locally)
- [Configuration](#configuration) — Environment variables for regions, on-prem, and advanced setup
- [Available Tools](#available-tools) — Full reference of all 27 tools
- [License](#license)

## Why MCP for Evals?

Evaluating LLMs is iterative. A typical loop looks like:

1. Run evals
2. Read the results
3. Tweak a prompt
4. Re-run
5. Check traces, read annotations your team left
6. Repeat

Today that means bouncing between your editor, a dashboard, and maybe a notebook. Every tab switch breaks your flow.

This MCP server puts that entire loop inside your editor:

- Pull a prompt, push a change, trigger an evaluation
- Inspect the failures, check what your team annotated
- Decide what to fix next — all in one conversation with your AI assistant

Confident AI has a full [web UI](https://app.confident-ai.com) where you can do all of this with a mouse. This is the same platform, accessed from your editor instead. Think: AWS web console vs. AWS CLI — same resources, different interface.

The server speaks the [Model Context Protocol (MCP)](https://modelcontextprotocol.io), so any compatible client connects out of the box. The web UI isn't going anywhere. This is just another way in.

## Prerequisites

1. A [Confident AI API key](https://app.confident-ai.com).
2. An MCP-compatible client — [Cursor](https://www.cursor.com), [Claude](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview), [Windsurf](https://windsurf.com), or any other client that supports the Model Context Protocol.

## Quickstart

Confident AI hosts the MCP server for you. Pick your region:

| Region       | MCP Server URL                                                               |
| ------------ | ---------------------------------------------------------------------------- |
| US (default) | [`https://mcp.confident-ai.com/mcp`](https://mcp.confident-ai.com/mcp)       |
| EU           | [`https://eu.mcp.confident-ai.com/mcp`](https://eu.mcp.confident-ai.com/mcp) |
| AU           | [`https://au.mcp.confident-ai.com/mcp`](https://au.mcp.confident-ai.com/mcp) |
| Self-hosted  | Use your own deployment URL                                                  |

> [!TIP]
> The examples below use the **US** server URL. For other regions, swap the URL:
>
> - **EU:** `https://eu.mcp.confident-ai.com/mcp`
> - **AU:** `https://au.mcp.confident-ai.com/mcp`
> - **Self-hosted / On-prem:** If you're running your own instance of Confident AI, you can run this MCP server yourself and point it at your deployment. See [Running the Server Locally](#-running-the-server-locally) for setup instructions.

### 🖥️ Cursor

Add the following to your `.cursor/mcp.json` file:

```json
{
  "mcpServers": {
    "confident-ai": {
      "url": "https://mcp.confident-ai.com/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_CONFIDENT_API_KEY>"
      }
    }
  }
}
```

### 🤖 Claude Code (or Desktop)

**Claude Code** — run the following command in your terminal:

```bash
claude mcp add confident-ai \
  --transport sse \
  --url https://mcp.confident-ai.com/mcp \
  --header "Authorization: Bearer <YOUR_CONFIDENT_API_KEY>"
```

**Claude Desktop** — add the following to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "confident-ai": {
      "url": "https://mcp.confident-ai.com/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_CONFIDENT_API_KEY>"
      }
    }
  }
}
```

### 🏄 Windsurf

Add the following to your Windsurf MCP configuration:

```json
{
  "mcpServers": {
    "confident-ai": {
      "serverUrl": "https://mcp.confident-ai.com/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_CONFIDENT_API_KEY>"
      }
    }
  }
}
```

### 🛠️ Running the Server Locally

If you're self-hosting or contributing to this project, you can run the server from source.

**Prerequisites:** Python >= 3.12, [Poetry](https://python-poetry.org/)

```bash
poetry install
uv run server.py
```

The server will start on `http://0.0.0.0:8081` with two endpoints:

| Endpoint    | Method | Description                                 |
| ----------- | ------ | ------------------------------------------- |
| `/mcp`      | GET    | SSE connection endpoint for MCP clients     |
| `/messages` | POST   | Message passing endpoint for tool execution |

Both endpoints require a `Bearer` token in the `Authorization` header (your [Confident AI API key](https://app.confident-ai.com)).

When running locally, point your MCP client to `http://localhost:8081/mcp` instead of the hosted URLs above.

To run in stdio mode instead (for MCP clients that communicate over stdin/stdout), uncomment the relevant block at the bottom of `server.py`:

```python
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Configuration

> [!NOTE]
> This section is only relevant if you're [running the server locally](#running-the-server-locally). If you're using the hosted server, the only thing you need is your API key in the quickstart configs above.

The server is configured through environment variables. You can set these in a `.env` file in the project root.

| Variable                        | Description                                                         | Default  |
| ------------------------------- | ------------------------------------------------------------------- | -------- |
| `CONFIDENT_API_KEY`             | Your Confident AI API key                                           | Required |
| `CONFIDENT_ENVIRONMENT`         | `LOCAL`, `PROD`, or `ON_PREM`                                       | `LOCAL`  |
| `CONFIDENT_REGION`              | `US`, `EU`, or `AU` (only used when `CONFIDENT_ENVIRONMENT=PROD`)   | `US`     |
| `CONFIDENT_BACKEND_LOCAL_URL`   | Backend URL for local development                                   | —        |
| `CONFIDENT_BACKEND_US_PROD_URL` | US production backend URL                                           | —        |
| `CONFIDENT_BACKEND_EU_PROD_URL` | EU production backend URL                                           | —        |
| `CONFIDENT_BACKEND_AU_PROD_URL` | AU production backend URL                                           | —        |
| `CONFIDENT_BACKEND_ON_PREM_URL` | On-prem backend URL (required when `CONFIDENT_ENVIRONMENT=ON_PREM`) | —        |

## Available Tools

<details>
<summary><strong>Prompts</strong> — 7 tools</summary>

Manage prompt templates with full version control — pull, push, version, and interpolate.

| Tool                    | Description                                                            |
| ----------------------- | ---------------------------------------------------------------------- |
| `pull_prompt`           | Fetch a prompt by alias, version, label, or commit hash                |
| `push_prompt`           | Create or update a prompt template on Confident AI                     |
| `interpolate_prompt`    | Locally render a prompt template by replacing placeholders with values |
| `create_prompt_version` | Assign a version string to a specific prompt commit                    |
| `list_prompt_versions`  | List all formal versions of a prompt                                   |
| `list_prompt_commits`   | List the full commit history of a prompt                               |
| `list_prompts`          | List all prompts in your project                                       |

</details>

<details>
<summary><strong>Datasets</strong> — 2 tools</summary>

Pull evaluation datasets for use in local test runs or agent workflows.

| Tool            | Description                                          |
| --------------- | ---------------------------------------------------- |
| `pull_dataset`  | Fetch a dataset (single-turn or multi-turn) by alias |
| `list_datasets` | List all datasets in your project                    |

</details>

<details>
<summary><strong>Evaluate</strong> — 2 tools</summary>

Trigger cloud evaluations and simulate multi-turn conversations.

| Tool                    | Description                                                                               |
| ----------------------- | ----------------------------------------------------------------------------------------- |
| `run_llm_evals`         | Run cloud evaluations on a batch of test cases against a metric collection                |
| `simulate_conversation` | Simulate the next turn of a multi-turn conversation using a scenario and expected outcome |

</details>

<details>
<summary><strong>Traces, Threads, and Spans</strong> — 9 tools</summary>

Browse, inspect, and evaluate production observability data at every level of your LLM pipeline.

| Tool              | Description                                                                 |
| ----------------- | --------------------------------------------------------------------------- |
| `list_traces`     | List traces with filtering by environment, time range, and sort order       |
| `get_trace`       | Get full details of a specific trace, including all spans                   |
| `list_threads`    | List conversation threads with filtering and pagination                     |
| `get_thread`      | Get full details of a thread, including all traces and thread-level metrics |
| `list_spans`      | List spans with filtering by type, error state, prompt version, and more    |
| `get_span`        | Get full details of a span, including I/O, cost, metrics, and annotations   |
| `evaluate_trace`  | Trigger a cloud evaluation on a specific trace                              |
| `evaluate_thread` | Trigger a cloud evaluation on a conversation thread                         |
| `evaluate_span`   | Trigger a cloud evaluation on a specific span                               |

</details>

<details>
<summary><strong>Annotations</strong> — 4 tools</summary>

Create and manage human feedback on traces, spans, and threads.

| Tool                | Description                                                                        |
| ------------------- | ---------------------------------------------------------------------------------- |
| `list_annotations`  | List annotations with filtering by target, type, and rating range                  |
| `get_annotation`    | Get full details of a specific annotation                                          |
| `create_annotation` | Create a new annotation (thumbs rating or star rating) on a trace, span, or thread |
| `update_annotation` | Update an existing annotation's rating, explanation, or expected output            |

</details>

<details>
<summary><strong>Test Runs</strong> — 2 tools</summary>

Inspect past evaluation runs and their results.

| Tool             | Description                                                                         |
| ---------------- | ----------------------------------------------------------------------------------- |
| `list_test_runs` | List test runs with filtering by status, time range, and multi-turn type            |
| `get_test_run`   | Get full details of a test run, including per-test-case metric scores and reasoning |

</details>

<details>
<summary><strong>Metric Collections</strong> — 1 tool</summary>

Discover available metric collections before triggering evaluations.

| Tool                      | Description                                                         |
| ------------------------- | ------------------------------------------------------------------- |
| `list_metric_collections` | List all metric collections, including their metrics and thresholds |

</details>

## Public Endpoint

> [!CAUTION]
> The hosted `/mcp` endpoint is strictly for internal development and experimental use. **It is not designed for public consumption.** The API and its underlying data structures are unstable and subject to change, breaking updates, or removal at any time without prior notice. Do not build production applications or rely on this public endpoint for any critical workflows.

## License

This project is licensed under the terms of the [MIT License](LICENSE).
