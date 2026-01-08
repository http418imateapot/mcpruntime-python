"""
Example MCP server for mcpruntime.

This server is intentionally minimal and exists solely to demonstrate:
- MCP tool definitions
- Pydantic-based input/output models
- Literal types for LLM-facing schema introspection

It is NOT intended for production use.
"""

from fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Literal

mcp = FastMCP("example-mcp-server")


# --------------------------------
# Data models (schema source of truth)
# --------------------------------

class UserInfo(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    name: str = Field(..., description="Full name of the user")
    email: str = Field(..., description="Email address of the user")
    status: Literal["active", "inactive", "suspended"] = Field(
        ..., description="Current status of the user"
    )
    last_login: str = Field(..., description="ISO 8601 timestamp of last login")
    role: str = Field(..., description="User role in the system")


# ------------------------
# MCP tools
# ------------------------

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool()
def get_user_info(user_id: str) -> UserInfo:
    """Get user information by user ID"""
    return UserInfo(
        user_id=user_id,
        name="John Doe",
        email="john.doe@example.com",
        status="active",
        last_login="2024-01-15T10:30:00Z",
        role="user",
    )


# ------------------------
# Run the server
# ------------------------

if __name__ == "__main__":
    # Default MCP endpoint: http://localhost:8000/mcp
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
        path="/mcp",
    )
