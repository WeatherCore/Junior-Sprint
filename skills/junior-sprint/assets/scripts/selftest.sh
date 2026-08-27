#!/usr/bin/env bash
# Junior Sprint · check_demand_card.py 自测入口
# 用法：bash selftest.sh   （或任意有 python3/python 的环境）
# 可通过 PYTHON 环境变量指定解释器：PYTHON=/path/to/python bash selftest.sh
set -u

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 在 Git Bash / Cygwin / WSL 等环境下，把 Unix 路径转成 Windows 绝对路径，
# 避免直接传给原生 Windows python.exe 时被解读成 D:\d\... 之类的错误路径。
if command -v cygpath >/dev/null 2>&1; then
  SCRIPT_DIR="$(cygpath -w "$SCRIPT_DIR")"
fi

PY="${PYTHON:-python3}"

# 找不到 python3 时退而求其次用 python
if ! command -v "$PY" >/dev/null 2>&1; then
  PY="python"
fi

if ! command -v "$PY" >/dev/null 2>&1; then
  echo "未找到 python，请设置 PYTHON 环境变量指向可用的 Python 解释器" >&2
  exit 2
fi

exec "$PY" "$SCRIPT_DIR/test_check_demand_card.py"
