"""
LLM-facing schema introspection for MCP tools.

This module intentionally generates minimal schemas to constrain
LLM behavior, not to fully describe validation rules.
"""

import inspect
from typing import get_type_hints, get_origin, get_args, Union, Literal


def _map_python_type(python_type):
    """Map basic Python types to JSON Schema types."""
    if python_type == str:
        return "string"
    if python_type == int:
        return "integer"
    if python_type == float:
        return "number"
    if python_type == bool:
        return "boolean"
    if python_type == list:
        return "array"
    if python_type == dict:
        return "object"
    return "string"  # fallback for LLM tolerance


def _extract_optional(python_type):
    """
    Detect Optional[T] or Union[T, None].

    Returns:
        (is_optional: bool, inner_type)
    """
    origin = get_origin(python_type)
    args = get_args(python_type)

    if origin is Union and type(None) in args:
        inner = next(t for t in args if t is not type(None))
        return True, inner

    return False, python_type


def _extract_literal(python_type):
    """
    Detect Literal[...] and return enum values if present.
    """
    origin = get_origin(python_type)
    if origin is Literal:
        return list(get_args(python_type))
    return None


def mcp_tool_to_chatgpt_schema(tool_func):
    sig = inspect.signature(tool_func)
    type_hints = get_type_hints(tool_func)

    properties = {}
    required = []

    for name, param in sig.parameters.items():
        if name not in type_hints:
            continue

        python_type = type_hints[name]

        # --- Optional handling ---
        is_optional, inner_type = _extract_optional(python_type)

        # --- Literal handling ---
        enum_values = _extract_literal(inner_type)

        schema_entry = {}

        if enum_values:
            # Literal -> enum
            schema_entry["type"] = "string"
            schema_entry["enum"] = enum_values
        else:
            schema_entry["type"] = _map_python_type(inner_type)

        # --- Description extraction (best-effort) ---
        param_desc = ""
        if tool_func.__doc__:
            for line in tool_func.__doc__.splitlines():
                if line.strip().startswith(name):
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        param_desc = parts[1].strip()
                        break

        if param_desc:
            schema_entry["description"] = param_desc

        properties[name] = schema_entry

        # --- Required logic ---
        if not is_optional and param.default is inspect.Parameter.empty:
            required.append(name)

    return {
        "type": "function",
        "function": {
            "name": tool_func.__name__,
            "description": tool_func.__doc__ or "",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        },
    }
