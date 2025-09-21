import logging
import os
from datetime import datetime
from contextlib import AsyncExitStack
from client import MCPClient
from typing import Optional
import asyncio

logs_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(logs_dir, exist_ok=True)

# 生成日志文件名（按日期）
today = datetime.now().strftime("%Y-%m-%d")
log_file = os.path.join(logs_dir, f"ReAct.log")
# 配置根日志记录器
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
    ]
)

# 配置httpx日志级别为INFO，让它输出到我们的日志文件
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.INFO)
# 配置FastMCP相关的日志
mcp_logger = logging.getLogger("mcp")
mcp_logger.setLevel(logging.INFO)

logger = logging.getLogger(__name__)

class ReAct:
    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.client: Optional[MCPClient] = None
        
    async def initialize_client(self, 
                                host: str = "127.0.0.1", 
                                port: int = 8000):
        self.client = await self.exit_stack.enter_async_context(MCPClient())
        await self.client.connect_to_server(f"http://{host}:{port}/mcp")

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.exit_stack.aclose()
        
async def main():
    async with ReAct() as agent:
        await agent.initialize_client(host="127.0.0.1", port=8888)
        
if __name__ == "__main__":
    asyncio.run(main())