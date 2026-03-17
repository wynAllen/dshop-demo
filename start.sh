#!/usr/bin/env bash
# 启动零售电商项目：后端 API + 前端开发服务
set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
RUN_DIR="$ROOT/.run"
mkdir -p "$RUN_DIR"

check_port() {
  if lsof -ti:"$1" >/dev/null 2>&1; then
    echo "端口 $1 已被占用，请先执行 ./stop.sh 或关闭占用进程。"
    return 1
  fi
  return 0
}

echo "检查端口..."
check_port 8000 || exit 1
check_port 5173 || exit 1

echo "启动后端 (http://localhost:8000) ..."
PYTHONPATH=. .venv_retail/bin/uvicorn retail_api.main:create_app --factory --host 0.0.0.0 --port 8000 \
  >> "$RUN_DIR/backend.log" 2>&1 &
echo $! > "$RUN_DIR/backend.pid"

echo "启动前端 (http://localhost:5173) ..."
(cd retail_web && npm run dev) >> "$RUN_DIR/frontend.log" 2>&1 &
echo $! > "$RUN_DIR/frontend.pid"

sleep 2
if ! kill -0 "$(cat "$RUN_DIR/backend.pid")" 2>/dev/null; then
  echo "后端启动失败，请查看 .run/backend.log"
  exit 1
fi
if ! kill -0 "$(cat "$RUN_DIR/frontend.pid")" 2>/dev/null; then
  echo "前端启动失败，请查看 .run/frontend.log"
  exit 1
fi

echo "已启动。"
echo "  后端 API: http://localhost:8000"
echo "  前端页面: http://localhost:5173"
echo "  停止项目: ./stop.sh"
