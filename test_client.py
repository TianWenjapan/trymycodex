"""模拟客户端向后端发送 POST / GET 请求的测试脚本。

使用 Python 标准库 urllib，无需额外依赖。
运行前请先启动后端：python_vnev/bin/uvicorn main:app --host 0.0.0.0 --port 8001
"""

import json
import urllib.parse
import urllib.request

BASE_URL = "http://146.56.209.130:8001"


def send_post(path: str, payload: dict) -> tuple[int, dict]:
    """发送 POST 请求（JSON body），返回 (状态码, 响应 JSON)。"""
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def send_get(path: str, params: dict | None = None) -> tuple[int, dict]:
    """发送 GET 请求，返回 (状态码, 响应 JSON)。"""
    if params:
        path = f"{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(f"{BASE_URL}{path}") as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def main() -> None:
    print("== 模拟客户端请求 ==")

    # 1. POST 请求：登录类数据
    status, body = send_post("/submit", {"name": "teanwen", "action": "login"})
    print(f"POST /submit -> {status} {body}")

    # 2. POST 请求：订单类数据
    status, body = send_post("/submit", {"order_id": 1001, "items": ["apple", "banana"]})
    print(f"POST /submit -> {status} {body}")

    # 3. GET 请求：首页
    status, body = send_get("/")
    print(f"GET / -> {status} {body}")

    # 4. GET 请求：带查询参数的日志查询
    status, body = send_get("/logs", params={"limit": 20})
    print(f"GET /logs?limit=20 -> {status}")

    print("\n== 服务端已保存的请求日志 ==")
    for log in body["logs"]:
        print(
            f"#{log['id']} {log['method']} {log['path']} "
            f"query={log['query_params']} body={log['body']} at={log['created_at']}"
        )


if __name__ == "__main__":
    main()
