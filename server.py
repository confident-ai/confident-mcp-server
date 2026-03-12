import uvicorn
from fastapi import FastAPI, HTTPException, Request, Depends
from mcp.server.sse import SseServerTransport
from fastapi.middleware.cors import CORSMiddleware
from mcp_logger import logger, AuditLoggingMiddleware


from confident_mcp import mcp
from confident.api import confident_api_key
import prompts.tools
import datasets.tools
import traces.tools
import annotations.tools
import test_runs.tools
import metric_collections.tools
import evaluate.tools

app = FastAPI(title="Confident AI MCP Server")

async def set_auth(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(401, "Missing/invalid Bearer token.")
    token = auth_header.split(" ")[1]
    confident_api_key.set(token)

sse = SseServerTransport("/messages")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.add_middleware(AuditLoggingMiddleware)

@app.get("/mcp") # Usually used as /sse but using /mcp for convention
async def handle_sse(request: Request):
    """Initial connection endpoint for the MCP client"""
    await set_auth(request)

    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await mcp._mcp_server.run(streams[0], streams[1], mcp._mcp_server.create_initialization_options())

@app.post("/messages")
async def handle_messages(request: Request):
    """Message passing endpoint for tool execution"""
    await set_auth(request)

    await sse.handle_post_message(request.scope, request.receive, request._send)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)


# Uncomment below to run MCP server using stdio (Comment above code as well)

# if __name__ == "__main__":
#     mcp.run(transport="stdio")
