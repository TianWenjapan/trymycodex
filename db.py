"""SQLite 数据库封装：连接、建表、保存与查询请求日志。"""

import sqlite3
from datetime import datetime

DB_PATH = "app.db"


def _connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    """创建 request_logs 表（幂等，可重复调用）。"""
    conn = _connect()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS request_logs (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                method       TEXT NOT NULL,
                path         TEXT NOT NULL,
                query_params TEXT,
                body         TEXT,
                created_at   TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def save_request(method: str, path: str, query_params_json: str, body: str) -> None:
    """插入一条请求日志。"""
    created_at = datetime.now().isoformat(timespec="seconds")
    conn = _connect()
    try:
        conn.execute(
            """
            INSERT INTO request_logs (method, path, query_params, body, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (method, path, query_params_json, body, created_at),
        )
        conn.commit()
    finally:
        conn.close()


def fetch_logs(limit: int = 100) -> list[dict]:
    """按 id 倒序返回最近 limit 条日志。"""
    conn = _connect()
    try:
        rows = conn.execute(
            """
            SELECT id, method, path, query_params, body, created_at
            FROM request_logs
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    finally:
        conn.close()

    keys = ("id", "method", "path", "query_params", "body", "created_at")
    return [dict(zip(keys, row)) for row in rows]
