"""
Minimal example: ChatGPT + mcpruntime + MCP

This example demonstrates:
- Exposing MCP tools to ChatGPT via schema introspection
- Letting ChatGPT decide which tool to call
- Executing the tool via mcpruntime
- Feeding results back to ChatGPT for response generation
"""

import json
import asyncio
from openai import OpenAI

from mcpruntime.executor import MCPToolExecutor
from mcpruntime.schema import mcp_tool_to_chatgpt_schema


# --- Example MCP tool (normally lives in MCP server code) ---

def get_user_info(user_id: str):
    """Get user information by user ID"""
    return {
        "user_id": user_id,
        "status": "active",
        "role": "user",
    }


# --- Build ChatGPT-facing tool schema via introspection ---

CHATGPT_TOOLS = [
    mcp_tool_to_chatgpt_schema(get_user_info)
]


SYSTEM_PROMPT = """
You are an internal operations assistant.

Rules:
- You may request tools when needed
- You must not guess tool results
- Tool execution is handled by the runtime
"""


async def main():
    client = OpenAI()
    executor = MCPToolExecutor(
        server_url="http://localhost:8000/mcp"
    )

    user_message = "Check the status of user_123"

    # --- Step 1: Ask ChatGPT (decision only) ---

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        tools=CHATGPT_TOOLS,
        tool_choice="auto",
    )

    message = response.choices[0].message

    # --- Step 2: Execute MCP tool if requested ---

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        result = await executor.execute(
            tool_name=tool_name,
            arguments=arguments,
        )

        # --- Step 3: Feed tool result back to ChatGPT ---

        final = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
                message,
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                },
            ],
        )

        print(final.choices[0].message.content)

    else:
        # ChatGPT decided no tool was needed
        print(message.content)


if __name__ == "__main__":
    asyncio.run(main())
