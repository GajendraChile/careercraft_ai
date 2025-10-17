from course_recommendation_agent import create_course_recommendation_agent
from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient
from strands.multiagent.a2a import A2AServer
from a2a.types import AgentSkill, AgentCard, AgentCapabilities
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

mcp_server_url = os.getenv("MCP_SERVER_URL")
port = os.getenv("PORT")
deployed_agent_url = os.getenv("DEPLOYED_AGENT_URL")
skill = AgentSkill(
        id='course recommender agent',
        name='course recommender Agent',
        description='Agent that recommends courses for filling skill gaps.',
        tags=['Course', 'Course Recommendations']
    )

streamable_http_mcp_client = MCPClient(lambda: streamablehttp_client(mcp_server_url))
with streamable_http_mcp_client:
    tools = streamable_http_mcp_client.list_tools_sync()
    print("Tool fetching complete")
    agent = create_course_recommendation_agent(tools)
    profile_a2a_server = A2AServer(agent= agent, skills= [skill], host="0.0.0.0", port = port, http_url=deployed_agent_url, serve_at_root= True)
    profile_a2a_server.capabilities = AgentCapabilities(streaming = False)
    # Access the underlying FastAPI app
    fastapi_app = profile_a2a_server.to_fastapi_app()
    # Add custom middleware, routes, or configuration
    origins = ["*"]

    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins, # Allow all origins
        allow_credentials=True,
        allow_methods=["*"], # Allow all methods
        allow_headers=["*"], # Allow all headers
        )

    # Or access the Starlette app
    starlette_app = profile_a2a_server.to_starlette_app()
    # Customize as needed

    # You can then serve the customized app directly
    uvicorn.run(fastapi_app, host="0.0.0.0", port=9002)