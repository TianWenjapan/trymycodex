# FastAPI + SQLite 请求日志后端

## 项目目标

使用 FastAPI 捕获客户端发出的 POST / GET 请求信息，并通过 Python 标准库 `sqlite3` 将这些请求信息持久化保存到本地 SQLite 数据库。

## 文件结构

| 文件 | 作用 |
| --- | --- |
| `README.md` | 项目说明与任务计划 |
| `requirements.txt` | 依赖声明 |
| `db.py` | SQLite 连接、建表、保存、查询封装 |
| `main.py` | FastAPI 应用：请求捕获中间件 + 演示端点 |

## 依赖

```
fastapi
uvicorn[standard]
```

## 运行方式

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

> 注意：当前阶段仅完成源码与文档，**尚未安装依赖、尚未运行服务**，等待 Python 环境配置完成后再执行上述命令。

## 接口说明

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/` | 欢迎/健康提示 |
| POST | `/submit` | 回显收到的 JSON 请求体 |
| GET | `/logs` | 返回已保存的请求日志列表 |

所有请求（含 `/logs` 本身）都会由中间件记录到 `request_logs` 表中。

## 数据存储

- 数据库文件：`app.db`（项目根目录）。
- 表 `request_logs` 字段：`id`、`method`、`path`、`query_params`、`body`、`created_at`。
