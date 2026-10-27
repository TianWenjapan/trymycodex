# FastAPI + SQLite 请求日志后端 —— 实现计划

## 一、摘要（Summary）

在 `/home/ubuntu/projects/atry` 下新建一个 Python 后端项目，使用 FastAPI 捕获客户端发出的 POST / GET 请求信息，并用 Python 标准库 `sqlite3` 将请求信息持久化保存到本地 SQLite 数据库。

本阶段**只编写源码与文档**，不安装依赖、不运行服务、不初始化 Python 环境（等用户下一步配置好环境后再安装与运行）。

## 二、当前状态分析

- `/home/ubuntu/projects/atry` 目前为空目录，属于全新项目。
- 无已有代码、无既有依赖、无约定可遵循，无需兼容旧架构。
- 已与用户确认两项关键决策：
  - 保存内容 = **通用请求日志**（method、path、query params、body、时间戳）。
  - 存储方式 = **标准库 `sqlite3`**（不引入 ORM）。

## 三、拟改动文件（新建 4 个）

| 文件 | 作用 |
| --- | --- |
| `README.md` | 任务计划与项目说明（用户要求任务开始前先写） |
| `requirements.txt` | 声明依赖 `fastapi`、`uvicorn`，供用户下一步配置环境时安装 |
| `db.py` | SQLite 连接/建表/保存/查询封装 |
| `main.py` | FastAPI 应用：请求捕获中间件 + 演示端点 |

## 四、详细设计

### 1. README.md

- 说明项目目标：捕获并记录客户端 POST/GET 请求到 SQLite。
- 列出文件结构与职责。
- 说明依赖与运行方式（`pip install -r requirements.txt`、`uvicorn main:app --reload`），并注明「本阶段不安装、不运行，待环境配置后再执行」。

### 2. requirements.txt

```
fastapi
uvicorn[standard]
```

### 3. db.py（标准库 sqlite3）

- 数据库文件：`app.db`（位于项目根目录）。
- 建表 SQL：

```sql
CREATE TABLE IF NOT EXISTS request_logs (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    method       TEXT NOT NULL,
    path         TEXT NOT NULL,
    query_params TEXT,
    body         TEXT,
    created_at   TEXT NOT NULL
);
```

- 提供函数：
  - `init_db()`：创建连接并执行建表（幂等，可重复调用）。
  - `save_request(method, path, query_params_json, body)`：插入一条日志，`created_at` 用本地时间 ISO 字符串。
  - `fetch_logs(limit=100)`：按 `id` 倒序查询最近 `limit` 条，返回 `list[dict]`（键与表字段对应）。

### 4. main.py（FastAPI）

- **请求捕获中间件** `log_requests`（`@app.middleware("http")`）：
  - 记录 `request.method`、`request.url.path`、`dict(request.query_params)`。
  - 对 `POST/PUT/PATCH` 读取 `await request.body()`，解码为 UTF-8 文本（失败则存 `str(raw)`），并把原始字节缓存到 `request.state.body`，避免下游端点二次读取报错。
  - 调用 `db.save_request(...)` 保存日志后 `call_next` 继续处理。
- **演示端点**：
  - `GET /`：返回欢迎/健康提示，说明服务在运行。
  - `POST /submit`：从 `request.state.body` 读取并回显收到的 JSON 请求体，返回确认信息。
  - `GET /logs`：调用 `db.fetch_logs()` 返回已保存的日志列表。
- 应用启动时调用 `db.init_db()`。

> 说明：`GET /logs` 本身也会被中间件记录为一条日志，属预期行为（它是通用请求日志的一部分）。

## 五、假设与决策

- 「read.md」统一实现为 `README.md`（业界惯例命名）。
- 保存内容采用**通用请求日志**（已确认）。
- 存储采用**标准库 `sqlite3`**（已确认）。
- 本阶段**不安装依赖、不运行服务**（按用户要求，等待下一步配置 Python 环境）。

## 六、验证步骤（待用户配置好 Python 环境后执行）

1. `python -m venv .venv` 并激活（或用户提供的方式）。
2. `pip install -r requirements.txt`。
3. `uvicorn main:app --reload` 启动服务。
4. 用 `curl` 验证：
   - `curl http://127.0.0.1:8000/` → 返回欢迎信息。
   - `curl -X POST http://127.0.0.1:8000/submit -H "Content-Type: application/json" -d '{"hello":"world"}'` → 返回回显确认。
   - `curl "http://127.0.0.1:8000/logs"` → 返回含上述请求记录的 JSON 列表。
5. 确认 `app.db` 生成，且 `request_logs` 表中存在对应记录。
