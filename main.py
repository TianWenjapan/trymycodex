"""FastAPI 应用：捕获客户端 POST/GET 请求并保存到 SQLite。"""

import json

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db.init_db()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    method = request.method
    path = request.url.path
    query_params = dict(request.query_params)

    body = ""
    if method in ("POST", "PUT", "PATCH"):
        raw = await request.body()
        request.state.body = raw
        try:
            body = raw.decode("utf-8")
        except UnicodeDecodeError:
            body = str(raw)

    db.save_request(
        method,
        path,
        json.dumps(query_params, ensure_ascii=False),
        body,
    )

    response = await call_next(request)
    return response


@app.get("/")
async def root():
    return {"message": "FastAPI request logger is running"}


@app.post("/submit")
async def submit(request: Request):
    raw = getattr(request.state, "body", b"")
    received = {}
    if raw:
        try:
            received = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            received = {"raw": raw.decode("utf-8", errors="replace")}
    return JSONResponse({"status": "ok", "received": received})


@app.get("/logs")
async def logs():
    return {"logs": db.fetch_logs()}
