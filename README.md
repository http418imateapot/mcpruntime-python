# mcpruntime

**mcpruntime** is a minimal runtime bridge that allows LLMs (e.g. ChatGPT) to
*describe*, *select*, and *invoke* MCP tools — without embedding business logic
or agent behavior into the runtime itself.

This project focuses strictly on **execution plumbing**, not decision-making.

---

## Why mcpruntime exists

When building LLM-powered systems that interact with internal tools or services,
three concerns are often mixed together:

1. **Decision layer** – natural language understanding, reasoning, tool selection  
2. **Runtime layer** – executing a tool call safely and consistently  
3. **Service layer** – the actual business logic (APIs, databases, infra)

`mcpruntime` exists to **isolate the runtime layer**.

It intentionally does **not**:
- act as an agent framework
- manage prompts or memory
- implement business logic
- replace MCP servers

---

## Design principles

- **Runtime only**  
  This library executes tool calls. It does not decide *what* to call.

- **LLM-agnostic**  
  Works with ChatGPT or any LLM capable of function / tool calling.

- **MCP-native**  
  Uses MCP as the execution boundary. MCP servers remain the source of truth.

- **Explicit over magic**  
  No hidden side effects, no implicit agent behavior.

---

## Architecture overview

```text
User / Chat UI
      ↓
LLM (ChatGPT)
  - sees tool schema
  - decides which tool to call
      ↓
mcpruntime
  - executes MCP tool call
      ↓
MCP Server
  - actual business logic
```

---

## Installation

```bash
pip install mcpruntime
```

For development:

```bash
pip install -e .
```

---

## Core components

### MCPToolExecutor

MCPToolExecutor is responsible for one thing only:
executing a tool call against an MCP server.

```python
from mcpruntime.executor import MCPToolExecutor

executor = MCPToolExecutor("http://localhost:8000/mcp")

result = await executor.execute(
    tool_name="get_user_info",
    arguments={"user_id": "user_123"}
)
```

### Schema generation (Python → ChatGPT)

You can convert Python tool functions into ChatGPT-compatible
tool schemas using mcp_tool_to_chatgpt_schema.

```python
from mcpruntime.schema import mcp_tool_to_chatgpt_schema

def get_user_info(user_id: str):
    """Get user information by user ID"""
    pass

schema = mcp_tool_to_chatgpt_schema(get_user_info)
```

Supported features:

- basic Python types → JSON Schema
- Optional[T] → non-required parameters
- Literal[...] → enum constraints

---

## Minimal end-to-end flow

```text
User message
  ↓
ChatGPT (with tool schemas)
  ↓
ChatGPT returns tool name + arguments
  ↓
mcpruntime executes MCP tool
  ↓
Result is returned to ChatGPT
  ↓
ChatGPT responds in natural language
```

mcpruntime is only involved in the execution step.

---

## Testing philosophy

This project uses standard library unittest.

Tests are designed to:

- verify runtime boundaries
- ensure schema correctness
- prevent silent execution regressions

Run tests locally:

```bash
python -m unittest discover -s tests
```

---

## CI philosophy

CI guarantees:

- code style consistency
- Python 3.12 compatibility
- runtime correctness via unit tests

CI does not include explicit compile checks,
because all runtime code is imported and executed during tests.

---

## What this project is NOT

- An AI agent framework
- A prompt engineering toolkit
- A workflow engine
- A replacement for MCP servers

If you are looking for agent orchestration or memory management,
this library is intentionally not that.

---

## When should you use mcpruntime?

Use this project if:

- you already have MCP servers
- you want LLMs to safely invoke internal tools
- you want a clean boundary between reasoning and execution

Do not use it if:

- you want an opinionated agent framework
- you expect runtime-side decision logic
- you want automatic tool chaining

---

## License

MIT License
