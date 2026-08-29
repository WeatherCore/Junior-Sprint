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

# 探测可用的解释器：不仅要在 PATH 里，还要真能运行——
# Windows 的 python3 可能是 Microsoft Store 占位别名（在 PATH 中存在但执行即失败），
# 所以用 `"$PY" -c ""` 实测，失败就退而求其次用 python。
PY="${PYTHON:-python3}"
if ! command -v "$PY" >/dev/null 2>&1 || ! "$PY" -c "" >/dev/null 2>&1; then
  PY="python"
fi

if ! command -v "$PY" >/dev/null 2>&1 || ! "$PY" -c "" >/dev/null 2>&1; then
  echo "未找到可用的 python，请设置 PYTHON 环境变量指向可用的 Python 解释器" >&2
  exit 2
fi

exec "$PY" "$SCRIPT_DIR/test_check_demand_card.py"
