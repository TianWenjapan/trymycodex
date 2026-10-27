#!/usr/bin/env bash
# 一键启动整个项目：后端 (FastAPI, 8001) + 前端 (静态服务器, 8080)
# 用法：./start.sh  （按 Ctrl+C 停止全部服务）

# 切换到脚本所在目录（项目根目录）
cd "$(dirname "$0")"

BACKEND_PORT=8001
FRONTEND_PORT=8080
PUBLIC_IP="146.56.209.130"

STOPPED=0

cleanup() {
    [ "$STOPPED" -eq 1 ] && return
    STOPPED=1
    echo ""
    echo "正在停止服务..."
    [ -n "${BACKEND_PID:-}" ] && kill "$BACKEND_PID" 2>/dev/null
    [ -n "${FRONTEND_PID:-}" ] && kill "$FRONTEND_PID" 2>/dev/null
    wait 2>/dev/null
    echo "已停止。"
}
trap cleanup INT TERM EXIT

# 检查虚拟环境是否就绪
if [ ! -x "python_vnev/bin/uvicorn" ]; then
    echo "错误：未找到 python_vnev/bin/uvicorn，请先创建虚拟环境并安装依赖。" >&2
    exit 1
fi

echo "启动后端 (0.0.0.0:${BACKEND_PORT}) ..."
python_vnev/bin/uvicorn main:app --host 0.0.0.0 --port "${BACKEND_PORT}" &
BACKEND_PID=$!

echo "启动前端 (0.0.0.0:${FRONTEND_PORT}) ..."
python3 frontend_server.py &
FRONTEND_PID=$!

echo ""
echo "后端地址: http://${PUBLIC_IP}:${BACKEND_PORT}"
echo "前端地址: http://${PUBLIC_IP}:${FRONTEND_PORT}"
echo "按 Ctrl+C 停止全部服务。"
echo ""

wait
