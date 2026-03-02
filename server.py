import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from mcp.server.sse import SseServerTransport


from confident_mcp import mcp
from confident.api import confident_api_key
import prompts.tools
import datasets.tools
import traces.tools
import annotations.tools
import test_runs.tools
import metric_collections.tools

app = FastAPI(title="Confident AI MCP Server")

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path in ["/docs", "/openapi.json", "/health"]:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=401, 
            content={"error": "Unauthorized: Missing or invalid Bearer token. Please provide your CONFIDENT_API_KEY."}
        )
    
    token = auth_header.split(" ")[1]
    confident_api_key.set(token)
    
    return await call_next(request)

sse = SseServerTransport("/messages")

@app.get("/mcp") # Usually used as /sse but using /mcp for convention
async def handle_sse(request: Request):
    """Initial connection endpoint for the MCP client"""
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await mcp._mcp_server.run(streams[0], streams[1], mcp._mcp_server.create_initialization_options())

@app.post("/messages")
async def handle_messages(request: Request):
    """Message passing endpoint for tool execution"""
    await sse.handle_post_message(request.scope, request.receive, request._send)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)