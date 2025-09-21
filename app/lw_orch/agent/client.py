import asyncio
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import Tool
import logging


logger = logging.getLogger(__name__)

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
    
    async def get_prompts(self) -> list[str]:
        """Get the prompts available from the MCP server"""
        response = await self.session.list_prompts()
        return response.prompts
    
    async def connect_to_server(self, server_url: str):
        """Connect to an MCP server via streamable HTTP

        Args:
            server_url: URL of the MCP server (e.g., 'http://localhost:3000/mcp')
        """
        # Create streamable HTTP client connection
        read_stream, write_stream, _ = await self.exit_stack.enter_async_context(streamablehttp_client(server_url))
        
        # Create client session
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )

        await self.session.initialize()
        logger.info("Connected to the MCP server now!")
        
        self.tools = await self.get_tools()
        logger.info("Already retrieve the tools from the MCP server!")
        
        self.prompts = await self.get_prompts()
        logger.info("Already retrieve the prompts from the MCP server!")
        
    async def get_tools(self) -> list[Tool]:
        """Get the tools available from the MCP server"""
        response = await self.session.list_tools()
        return response.tools
    
    async def call_tool(self, tool_name: str, tool_args: dict):
        """Call a tool from the MCP server"""
        response = await self.session.call_tool(tool_name, tool_args)
        return response
       
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        self.session = None
        await self.exit_stack.aclose()
        