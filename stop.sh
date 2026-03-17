#!/usr/bin/env bash
# 停止零售电商项目：关闭后端与前端进程
set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_DIR="$ROOT/.run"

stop_by_pid() {
  local name=$1
  local pid_file=$2
  if [[ -f "$pid_file" ]]; then
    local pid
    pid=$(cat "$pid_file")
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true
      echo "已停止 $name (PID $pid)"
    fi
    rm -f "$pid_file"
  fi
}

stop_by_port() {
  local port=$1
  local pids
  pids=$(lsof -ti:"$port" 2>/dev/null) || true
  if [[ -n "$pids" ]]; then
    echo "$pids" | xargs kill 2>/dev/null || true
    echo "已停止占用端口 $port 的进程"
  fi
}

cd "$ROOT"

echo "停止后端..."
stop_by_pid "后端" "$RUN_DIR/backend.pid"
stop_by_port 8000

echo "停止前端..."
stop_by_pid "前端" "$RUN_DIR/frontend.pid"
stop_by_port 5173

echo "项目已停止。"
