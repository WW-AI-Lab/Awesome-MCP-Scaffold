# BEST_PRACTICES.md

> 🛠 **Objective**: Production-oriented FastMCP (SDK v1.10.1) server best practices. Clarify project structure, deployment recommendations, and bypass capabilities all at once to avoid the embarrassment of "runs but hard to maintain".

------

## 1 · Transport Layer Selection

| Scenario                | Recommended Transport      | Description                                     |
| ----------------------- | -------------------------- | ----------------------------------------------- |
| Local CLI / IDE Debug  | **stdio**                  | No ports, shortest path                        |
| Web / Multi-client      | **Streamable HTTP**        | Best compatibility with LB / auth middleware; supports HTTP2 / H2C |
| Long connection push    | Streamable HTTP + built-in SSE | Auto-upgrade on same path, no additional /sse endpoint needed |

⚠️ Public deployments must implement Host validation or bind to `127.0.0.1` at gateway to prevent DNS rebinding attacks.

------

## 2 · Directory Structure (Production Template)

```text
mcp-server/
├── server/                  # Core Python package (import server)
│   ├── __init__.py
│   ├── main.py              # FastMCP instance & app entry
│   ├── config.py            # Pydantic Settings / env parsing
│   ├── resources/           # All @mcp.resource
│   │   ├── __init__.py
│   │   └── greeting.py
│   ├── tools/               # All @mcp.tool
│   │   ├── __init__.py
│   │   └── math.py
│   ├── prompts/             # All @mcp.prompt
│   │   ├── __init__.py
│   │   └── echo.py
│   ├── routes/              # Bypass REST API
│   │   ├── __init__.py
│   │   ├── health.py
│   │   └── convert.py
│   └── static/              # Static resources directory (mounted by StaticFiles)
├── tests/                   # pytest & httpx
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/                # Pure function unit tests
│   └── integration/         # End-to-end Streamable HTTP calls
├── scripts/                 # Local ops scripts
│   ├── start.sh             # Unified entry (uvicorn / gunicorn)
│   └── migrate.sh           # DB / KV migration example
├── configs/                 # Config & secret templates (not in Git)
│   ├── logging.yml          # Structured logging config
│   └── .env.example         # Environment variable example (.env ➜ docker-compose)
├── deploy/                  # Unified deployment directory
│   ├── docker/              # Containerization
│   │   ├── Dockerfile
│   │   └── entrypoint.sh
│   ├── kubernetes/          # K8s / Helm Chart
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   └── ci/                  # CI/CD (GitHub Actions / GitLab CI)
│       └── github/
│           └── workflows/
│               └── ci.yml
├── pyproject.toml           # Poetry / PEP 621; lock mcp==1.10.1
├── README.md                # Project overview & quick start
└── docs/                    # Development / ops documentation
    ├── QUICKSTART.md
    ├── BEST_PRACTICES.md
    └── API_REFERENCE.md
```

### Directory Key Points

| Directory           | Purpose / Highlights                                         |
| ------------------- | ------------------------------------------------------------ |
| **server/**         | Code as protocol, layered by resources / tools / prompts; `config.py` unified loading of `os.environ`, avoiding scattered `os.getenv()` |
| **routes/**         | Only bypass HTTP; keep MCP core clean.                      |
| **tests/**          | Unit tests cover pure functions; integration tests directly connect `/mcp` Streamable HTTP, ensuring tools & resources are callable under real protocol. |
| **deploy/**         | Unified deployment directory containing all deployment configs including containerization, K8s, CI/CD. |
| **deploy/docker/**  | Independent of source code, any container changes don't pollute server package; `entrypoint.sh` reads `/configs/.env` ➜ generates final config. |
| **deploy/kubernetes/** | Decoupled from CI, avoiding Helm over-coupling early projects; add Helm Chart in production. |
| **docs/**           | Separate **running (QUICKSTART)**, **development (BEST_PRACTICES)**, **interface (API_REFERENCE)** for targeted reading by newcomers. |

> ✅ **Practice Rule**: All variable content unrelated to business logic (config / logs / secrets) should always be placed in `configs/` or external volumes.

------

## 3 · Bypass Capabilities

| Need            | Approach                                                     |
| --------------- | ------------------------------------------------------------ |
| Health Check    | `GET /health`: Return 200 & build sha                       |
| RESTful API     | `POST /api/v1/xxx`: Other RESTful API entries               |
| Static Files    | `StaticFiles(directory=server.static)` ➜ `/static`          |
| Sub-microservice | `from fastapi import APIRouter`; mount `router` to `app.mount("/sub", sub_app)` |

> **Naming Suggestion**: Unified bypass routes in `routes/`, filename consistent with HTTP path, search cost = 0.

------

## 4 · Deployment Tips

1. **Process Model**: Uvicorn Worker ≥ *4* (`--worker-class=uvicorn.workers.UvicornWorker`); IO-intensive suggests 2 × CPU Core.
2. **Logging**: Unified structured JSON ➜ ELK / Loki; no `print()`.
3. **Version Locking**: `mcp==1.10.1`, `fastapi~=0.115.14`; regression test in staging before upgrade.
4. **Security**:
   - Streamable HTTP endpoint at `/mcp`, other custom APIs don't share cookies;
   - Public only expose 443 TLS, internal `ClusterIP` communication via H2C.
5. **Monitoring**: Prometheus + OpenTelemetry Exporter; key metrics: `tool_invocation_total`, `tool_latency_seconds`, `resource_hit_total`. 