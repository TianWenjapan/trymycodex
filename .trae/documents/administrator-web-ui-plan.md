# administrator 网页（后端数据展示）—— 实现计划

## 一、摘要（Summary）

在 `/home/ubuntu/projects/atry/administrator` 下新建一个纯静态网页，用原生 HTML + CSS + JS 通过 `fetch` 拉取后端 `GET /logs` 的数据并渲染为表格展示。同时在 `main.py` 中加入 CORS 中间件，使前端能跨域访问后端接口。

本阶段需先编写 `administrator/read.md`，写清代码编写思路与网页查看方式。

## 二、当前状态分析

- 后端 [main.py](file:///home/ubuntu/projects/atry/main.py) 提供：
  - `GET /` 欢迎信息
  - `POST /submit` 回显
  - `GET /logs` 返回 `{"logs": [{id, method, path, query_params, body, created_at}, ...]}`
- 后端**未配置 CORS**，前端跨域 fetch 会被浏览器拦截。
- 后端运行地址 `http://127.0.0.1:8000`。
- 已与用户确认：前端用**纯静态 HTML+JS**；查看方式为**后端加 CORS + 单独静态服务器**。

## 三、拟改动文件（新建 2 个、修改 1 个）

| 文件 | 操作 | 作用 |
| --- | --- | --- |
| `administrator/read.md` | 新建 | 说明代码编写思路与网页查看方式 |
| `administrator/index.html` | 新建 | 纯静态网页：拉取并展示后端数据 |
| `main.py` | 修改 | 加入 CORS 中间件，允许跨域访问 |

## 四、详细设计

### 1. administrator/read.md

写清两部分内容：
- **代码怎么编写**：`index.html` 的三段式结构（HTML 骨架 + CSS 样式 + JS `fetch` 拉取 `/logs` 并渲染表格），说明字段来源与渲染逻辑。
- **网页怎么查看**：分三步——① 启动后端 `python_vnev/bin/uvicorn main:app --host 127.0.0.1 --port 8000`；② 在 `administrator` 目录启动静态服务器 `python3 -m http.server 8080`；③ 浏览器打开 `http://127.0.0.1:8080`。

### 2. administrator/index.html

单文件，内联 CSS 与 JS，无任何外部依赖：
- **HTML**：标题 + 一个「刷新」按钮 + 一个 `<table>`（表头：ID / 方法 / 路径 / 查询参数 / 请求体 / 时间）。
- **CSS**：简洁表格样式（边框、隔行底色、等宽字体显示请求体）。
- **JS**（`<script>`）：
  - `fetch('http://127.0.0.1:8000/logs')` 获取数据；
  - 从返回 JSON 的 `logs` 数组逐条生成 `<tr>`，字段对应用 `<td>` 展示；
  - 请求失败时在页面显示错误提示；
  - 「刷新」按钮点击后重新拉取；页面加载完成时自动拉取一次。

### 3. main.py（修改）

在文件顶部引入并注册 CORS 中间件：
- 新增导入：`from fastapi.middleware.cors import CORSMiddleware`
- 在 `app = FastAPI()` 之后、`db.init_db()` 之前（或之后）调用：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

> 说明：允许任意来源（`*`）是为演示方便；生产环境应改为具体的页面来源域名。

## 五、假设与决策

- 文件命名为用户指定的 `read.md`（非 `README.md`）。
- 前端为**纯静态 HTML+JS**（已确认）。
- 查看方式为**后端加 CORS + `python3 -m http.server` 静态服务器**（已确认）。
- 静态服务器端口用 `8080`（避免与后端 `8000` 冲突）。
- `GET /logs` 本身也会被后端中间件记录为一条日志，属预期行为。

## 六、验证步骤

1. 启动后端：`python_vnev/bin/uvicorn main:app --host 127.0.0.1 --port 8000`。
2. 在 `administrator` 目录启动静态服务器：`python3 -m http.server 8080`。
3. 浏览器打开 `http://127.0.0.1:8080`，应能看到日志表格。
4. 先用 `curl -X POST http://127.0.0.1:8000/submit -H "Content-Type: application/json" -d '{"k":"v"}'` 造一条数据，点「刷新」，表格应出现新记录。
