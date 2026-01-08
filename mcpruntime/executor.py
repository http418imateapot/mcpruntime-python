"""
MCP tool execution runtime.

This module is responsible for executing MCP tools requested by
external decision-makers (e.g. LLMs, agents), and nothing else.

It does NOT:
- perform schema generation
- know about ChatGPT or any LLM
- apply business logic or validation
"""
from fastmcp import Client


class MCPToolExecutor:
    def __init__(self, server_url: str):
        self.server_url = server_url

    async def execute(self, tool_name: str, arguments: dict) -> dict:
        async with Client(self.server_url) as client:
            return await client.call_tool(
                tool_name=tool_name,
                arguments=arguments,
            )
