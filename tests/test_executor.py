import unittest
from unittest.mock import AsyncMock, patch
from mcpruntime.executor import MCPToolExecutor


class TestMCPToolExecutor(unittest.IsolatedAsyncioTestCase):
    async def test_executor_calls_mcp_client(self):
        executor = MCPToolExecutor("http://fake-server")

        with patch("mcpruntime.executor.Client") as MockClient:
            mock_client = MockClient.return_value.__aenter__.return_value
            mock_client.call_tool = AsyncMock(return_value={"ok": True})

            result = await executor.execute(
                tool_name="test_tool",
                arguments={"a": 1},
            )

            mock_client.call_tool.assert_awaited_once_with(
                tool_name="test_tool",
                arguments={"a": 1},
            )

            self.assertEqual(result, {"ok": True})


if __name__ == "__main__":
    unittest.main()
