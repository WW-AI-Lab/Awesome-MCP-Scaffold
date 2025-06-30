# BEST_PRACTICES.md

> 🛠 **目标**：面向生产环境的 FastMCP（SDK v1.10.1）服务端最佳实践。把项目结构、部署建议、旁路能力一次性讲清楚，避免“跑得通却难以运维”的尴尬。

------

## 1 · 传输层选型

| 场景                | 建议传输                   | 说明                                           |
| ------------------- | -------------------------- | ---------------------------------------------- |
| 本地 CLI / IDE 调试 | **stdio**                  | 免端口，路径最短                               |
| Web / 多端客户端    | **Streamable HTTP**        | 与 LB / 授权中间件兼容性最佳；支持 HTTP2 / H2C |
| 需要长连推送        | Streamable HTTP + 内建 SSE | 同一路径自动升级，无需额外 /sse 端点           |

⚠️ 公网部署须在入口网关做 Host 校验或绑定 `127.0.0.1`，防止 DNS 重绑定攻击。

------

\## 2 · 目录规划（生产级模板）

```text
mcp-server/
├── server/                  # 核心 Python 包 (import server)
│   ├── __init__.py
│   ├── main.py              # FastMCP 实例 & 应用入口
│   ├── config.py            # Pydantic Settings / env 解析
│   ├── resources/           # 所有 @mcp.resource
│   │   ├── __init__.py
│   │   └── greeting.py
│   ├── tools/               # 所有 @mcp.tool
│   │   ├── __init__.py
│   │   └── math.py
│   ├── prompts/             # 所有 @mcp.prompt
│   │   ├── __init__.py
│   │   └── echo.py
│   ├── routes/              # 旁路 REST API
│   │   ├── __init__.py
│   │   ├── health.py
│   │   └── convert.py
│   └── static/              # 静态资源目录 (由 StaticFiles 挂载)
├── tests/                   # pytest & httpx
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/                # 纯函数单测
│   └── integration/         # 端到端调用 Streamable HTTP
├── scripts/                 # 本地运维脚本
│   ├── start.sh             # 统一入口 (uvicorn / gunicorn)
│   └── migrate.sh           # DB / KV 迁移示例
├── configs/                 # 配置&密钥模板 (不进 Git)
│   ├── logging.yml          # 结构化日志配置
│   └── .env.example         # 环境变量示例 (.env ➜ docker-compose)
├── deploy/                  # 部署相关统一目录
│   ├── docker/              # 容器化
│   │   ├── Dockerfile
│   │   └── entrypoint.sh
│   ├── kubernetes/          # K8s / Helm Chart
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   └── ci/                  # CI/CD (GitHub Actions / GitLab CI)
│       └── github/
│           └── workflows/
│               └── ci.yml
├── pyproject.toml           # Poetry / PEP 621；锁定 mcp==1.10.1
├── README.md                # 项目概览 & 快速上手
└── docs/                    # 研发 / 运维文档
    ├── QUICKSTART.md
    ├── BEST_PRACTICES.md
    └── API_REFERENCE.md
```

### 目录要点

| 目录            | 用途 / 亮点                                                  |
| --------------- | ------------------------------------------------------------ |
| **server/**     | 代码即协议，按资源 / 工具 / Prompt 分层；`config.py` 统一加载 `os.environ`，避免到处散落 `os.getenv()` |
| **routes/**     | 只放旁路 HTTP；保持 MCP 内核纯净。                           |
| **tests/**      | 单元测试覆盖纯函数；集成测试直接连 `/mcp` Streamable HTTP，确保工具 & 资源在真实协议下可调用。 |
| **deploy/**     | 部署相关统一目录，包含容器化、K8s、CI/CD等所有部署配置。   |
| **deploy/docker/** | 独立于源码，任何对容器的改动不污染服务器包；`entrypoint.sh` 负责读取 `/configs/.env` ➜ 生成最终配置。 |
| **deploy/kubernetes/** | 与 CI 解耦，避免 Helm 过度耦合早期项目；生产再补 Helm Chart。 |
| **docs/**       | 把**运行（QUICKSTART）**、**开发（BEST_PRACTICES）**、**接口（API_REFERENCE）**拆开，便于新人定向阅读。 |

> ✅ **实践法则**：一切与业务逻辑无关的可变内容（配置 / 日志 / 密钥）永远放到 `configs/` 或外部挂卷。

------

\## 3 · 旁路能力

| 需求        | 做法                                                         |
| ----------- | ------------------------------------------------------------ |
| 健康检测    | `GET /health`：返回 200 & build sha                          |
| RESTful API | `POST /api/v1/xxx`：其他RESTful API入口                      |
| 静态文件    | `StaticFiles(directory=server.static)` ➜ `/static`           |
| 子微服务    | `from fastapi import APIRouter`; 挂 `router` 到 `app.mount("/sub", sub_app)` |

> **命名建议**：旁路路由统一放 `routes/`，文件名与 HTTP path 保持一致，查找成本=0。

------

\## 4 · 部署小贴士

1. **进程模型**：Uvicorn Worker ≥ *4* (`--worker-class=uvicorn.workers.UvicornWorker`)；IO 密集型建议 2 × CPU Core。
2. **日志**：统一使用结构化 JSON ➜ ELK / Loki；不要 `print()`。
3. **版本锁定**：`mcp==1.10.1`、`fastapi~=0.115.14`；升级时先在 staging 打回归测试。
4. **安全**：
   - Streamable HTTP 端点置于 `/mcp`，其余自定义 API 不共享 Cookie；
   - 公网仅暴露 443 TLS，内部 `ClusterIP` 通信走 H2C。
5. **监控**：Prometheus + OpenTelemetry Exporter；关键指标：`tool_invocation_total`, `tool_latency_seconds`, `resource_hit_total`。