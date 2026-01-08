import unittest
from mcpruntime.schema import mcp_tool_to_chatgpt_schema


class TestSchemaBasic(unittest.TestCase):
    def simple_tool(self, a: str, b: int):
        """Simple test tool"""
        pass

    def test_basic_schema_generation(self):
        schema = mcp_tool_to_chatgpt_schema(self.simple_tool)
        params = schema["function"]["parameters"]

        assert params["type"] == "object"
        assert set(params["properties"].keys()) == {"a", "b"}
        assert set(params["required"]) == {"a", "b"}

        assert params["properties"]["a"]["type"] == "string"
        assert params["properties"]["b"]["type"] == "integer"


if __name__ == "__main__":
    unittest.main()
