"""
Minimal MCP client example.

This script demonstrates how to:
- Connect to an MCP server
- List available tools
- Call a tool with explicit arguments

It is intentionally simple and NOT a generic test harness.
"""

import collections
import collections.abc
import asyncio
from fastmcp import Client

# ===== Python 3.12 collections compatibility patch =====
for name in (
    "MutableSet",
    "MutableMapping",
    "Mapping",
    "Sequence",
    "Iterable",
    "Callable",
):
    if not hasattr(collections, name):
        setattr(collections, name, getattr(collections.abc, name))
# =======================================================


MCP_SERVER_URL = "http://localhost:8000/mcp"


async def main():
    print(f"Connecting to MCP server at {MCP_SERVER_URL}")

    async with Client(MCP_SERVER_URL) as client:

        # --- 1. List available tools ---
        tools = await client.list_tools()
        print(f"\nAvailable tools ({len(tools)}):")

        for tool in tools:
            print(f"- {tool.name}: {tool.description}")

        # --- 2. Call example tools explicitly ---

        print("\nCalling tool: add(a=3, b=4)")
        result = await client.call_tool(
            "add",
            arguments={"a": 3, "b": 4},
        )
        print(f"Result: {result}")

        print("\nCalling tool: get_user_info(user_id='user_123')")
        result = await client.call_tool(
            "get_user_info",
            arguments={"user_id": "user_123"},
        )
        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
