import asyncio
from typing import  Any,Dict,List
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_core.tools import tool

class MCPClient:
    def __init__(self,repository_path:str):
        self.repository_path=repository_path
        self.session=None
        self.read=None
        self.write=None
        self._client_context=None
        self._session_context=None
    
    async def connect(self):
        """Connect the MCP Git Server"""
        server_params=StdioServerParameters(
            command='npx',
            args=[
                "-y",
                "@modelcontextprotocol/server.git",
                "--repository",
                self.repository_path
            ]
        )
        
        self._client_context=stdio_client(server_params)
        self.read,self.write=await self._client_context.__aenter__()

        self._session_context=ClientSession(self.read,self.write)
        self.session= await self._session_context.__aenter__()

        await self.session.initialize()




        