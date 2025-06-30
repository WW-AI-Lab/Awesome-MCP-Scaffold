# QUICKSTART.md

> 👇 **Single File Runnable Example** —— Get it running first, then split into modules

```python
# server.py
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from starlette.requests import Request

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="DemoServer",
    stateless_http=True,          # Easier for horizontal scaling
)

# ---------- Resource ----------
@mcp.resource("greeting://{name}", title="Say Hello")
def greet(name: str) -> str:
    return f"Hello, {name}!"

# ---------- Tool ----------
@mcp.tool(title="Add", description="Add two integers")
def add(a: int, b: int) -> int:
    return a + b

# ---------- Prompt ----------
@mcp.prompt(title="Echo Prompt")
def echo_prompt(message: str) -> str:
    return f"Please reply with the same text: {message}"

# ---------- Bypass Routes ----------
@mcp.custom_route(path="/health", methods=["GET"])
async def health(_: Request):
    return JSONResponse({"status": "ok"})

@mcp.custom_route(path="/api/v1/convert", methods=["POST"])
async def api_unified_convert(request: Request):
    """Example bypass: unified file conversion interface"""
    # Please implement actual logic yourself
    data = await request.json()
    return JSONResponse({"echo": data})

# ---------- Static Files ----------
def mount_static(app):
    static_dir = Path(__file__).parent / "static"
    static_dir.mkdir(exist_ok=True)
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# ---------- Run ----------
if __name__ == "__main__":
    # Mount static and custom routes to HTTP App
    app = mcp.streamable_http_app()
    mount_static(app)
    mcp.run(transport="streamable-http")
```

> **Key Points Review**  
> * **mcp.streamable_http_app()** returns a standard **FastAPI** instance; therefore you can freely add `app.get()` / `app.post()`, or mount static directories as above.  
> * `stateless_http=True` disables session persistence, easy for k8s horizontal scaling; if you need sessions or SSE streams, you can remove this parameter and use the default **Stateful**.  
> * Bypass custom routes use **@mcp.custom_route**, saving you from composing sub-FastAPI yourself. 