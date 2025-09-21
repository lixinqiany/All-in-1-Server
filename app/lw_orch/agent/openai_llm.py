from openai import OpenAI
from pydantic import BaseModel
from typing import Union, List, Iterable, Optional
from openai.types.responses import ResponseInputParam, ToolParam, ResponseFunctionToolCall
from mcp.types import Tool, CallToolResult
import json

class ResponsesRequest(BaseModel):
    model: str
    instructions: str
    input: Union[str, ResponseInputParam]
    tools: Optional[Iterable[ToolParam]] = None

class OpenAILLM:
    def __init__(self, 
                 api_key: str, 
                 base_url: str):
        self.openai = OpenAI(api_key=api_key, base_url=base_url)
    
    def create_responses(self, request: ResponsesRequest):
        """对应OpenAI的responses接口发起请求
        """
        return self.openai.responses.create(**request.model_dump())
    
    def parse_openai_function_call(self, content: list) -> str:
        """ parse the openai function call response """
        tool_name = content.name
        tool_args = json.loads(content.arguments)
        
        return tool_name, tool_args
    
    def convert2openai_function_call_output(self, 
                                            content: ResponseFunctionToolCall,
                                            mcp_result: CallToolResult) -> dict:
        """ convert the openai function call output to an input item for next round """
        result = mcp_result.structuredContent if mcp_result.structuredContent is not None else mcp_result.content
        return {
            "type": "function_call_output",
            "call_id": content.call_id,
            "output": json.dumps(result)
        }
        
        
        
if __name__ == "__main__":
    llm = OpenAILLM(api_key="sk-at-10789555983862555a019807b9227be90e8e59b3fd49720dd34b54987ecf8b97", 
                    base_url="https://chat.appexnetworks.com/open-api/v1/relay/openai/v1")
    print(llm.create_responses(
        ResponsesRequest(model="gpt-4.1", 
                         instructions="You are a helpful assistant.", 
                         input="Hello, how are you?")))