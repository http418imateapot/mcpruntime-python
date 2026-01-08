import unittest
from typing import Optional, Literal
from mcpruntime.schema import mcp_tool_to_chatgpt_schema


class TestSchemaLiteralOptional(unittest.TestCase):
    def tool_with_literal(
        self,
        status: Literal["active", "inactive"],
    ):
        """Tool with literal"""
        pass

    def tool_with_optional(
        self,
        user_id: Optional[str],
    ):
        """Tool with optional"""
        pass

    def test_literal_becomes_enum(self):
        schema = mcp_tool_to_chatgpt_schema(self.tool_with_literal)
        prop = schema["function"]["parameters"]["properties"]["status"]

        assert prop["type"] == "string"
        assert prop["enum"] == ["active", "inactive"]

    def test_optional_not_required(self):
        schema = mcp_tool_to_chatgpt_schema(self.tool_with_optional)
        params = schema["function"]["parameters"]

        assert "user_id" in params["properties"]
        assert "user_id" not in params["required"]


if __name__ == "__main__":
    unittest.main()
