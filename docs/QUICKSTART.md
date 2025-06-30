# QUICKSTART.md

> 👇 **单文件可运行示例** —— 先跑通，再拆分模块

```python
# server.py
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from starlette.requests import Request

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="DemoServer",
    stateless_http=True,          # 更易于水平扩容
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
    """示例旁路：统一文件转换接口"""
    # 真实逻辑请自行实现
    data = await request.json()
    return JSONResponse({"echo": data})

# ---------- Static Files ----------
def mount_static(app):
    static_dir = Path(__file__).parent / "static"
    static_dir.mkdir(exist_ok=True)
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# ---------- Run ----------
if __name__ == "__main__":
    #把 static 和自定义路由挂到 HTTP App 上
    app = mcp.streamable_http_app()
    mount_static(app)
    mcp.run(transport="streamable-http")
```

> **关键点回顾**  
> * **mcp.streamable_http_app()** 返回的是标准 **FastAPI** 实例；因此能随意再 `app.get()` / `app.post()`，或如上挂静态目录。  
> * `stateless_http=True` 关闭会话持久化，易于 k8s 横向扩容；若需要会话、SSE stream，可去掉此参数并用默认 **Stateful**。  
> * 旁路自定义路由用 **@mcp.custom_route**，省却自己组合子 FastAPI。  