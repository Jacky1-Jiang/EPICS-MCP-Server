from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
import asyncio
env_path = ".env"  
load_dotenv(env_path)

azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
model = AzureChatOpenAI(
    azure_deployment="gpt-4o-mini-2",  
    api_version="2024-02-01",  
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


async def run_agent():
    async with MultiServerMCPClient(
        {

            "mcp_epics_server":{
                "url": "http://localhost:8000/sse",
                "transport":"sse"
            }
        }

    ) as client:
        agent = create_react_agent(model, client.get_tools())
        epics_response = await agent.ainvoke({"messages":"To query the value of a PV (Process Variable) named temperature:water"})

        return epics_response     

if __name__  == "__main__":
    response = asyncio.run(run_agent())
    for m in response["messages"]:
        m.pretty_print()
