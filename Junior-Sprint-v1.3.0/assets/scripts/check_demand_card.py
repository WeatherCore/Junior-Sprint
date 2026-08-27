#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""需求卡发布前自检（阶段 1 硬性步骤）。

用法：
    python check_demand_card.py <草稿路径>               # 检查文件
    cat card.md | python check_demand_card.py -          # 从 stdin 读
    python check_demand_card.py card.md --strict         # 软性告警也视为失败
    python check_demand_card.py card.md --allow 文件,方法  # 放行确属业务用法的词

检查项：
  1. 结构 —— 三要素（背景 / 要什么 / 验收标准）章节齐全；验收标准 ≥3 条；
     含 Sprint ID（S-YYYYMMDD-N，N ≥1 位，与复盘报告 / state 文件一致）。
  2. 技术词泄漏 —— 分两级：
     硬性（FAIL）：语义无歧义的技术词，命中即必须改写——接口、数据库、字段、
       端点、路由、函数、变量、数据表、返回值、请求体，及 API / HTTP / JSON /
       SQL 等英文术语与常见框架名。
     软性（WARN）：业务语境可能合法的词（文件 / 方法 / 参数 / 异常 / 缓存……），
       命中出告警，由 AI 结合上下文判断；确属业务用法（如"上传文件""付款方法"）
       用 --allow 放行。
     说明：SKILL.md 客户口吻禁词表中的"文件 / 类 / 方法"在日常中文里一语多义，
     脚本把它们归入软性层，是为了区分"必须重写"与"需要确认"；禁词规则本身不变。

退出码：0 通过（允许有软性告警）；1 硬性违规或结构缺失；2 输入错误。
"""

import argparse
import re
import sys

# 中文技术词——语义无歧义，命中即 FAIL
HARD_CN = [
    "接口", "数据库", "字段", "端点", "路由", "函数", "变量",
    "数据表", "返回值", "请求体", "实体类", "抽象类", "父类", "子类",
]

# 中文技术词——业务语境可能合法，命中出 WARN
SOFT_CN = [
    "文件", "方法", "参数", "异常", "缓存", "队列", "线程", "并发",
    "进程", "模块", "请求", "响应", "代码", "脚本", "部署", "后端",
    "前端", "鉴权", "数据模型", "数据结构", "算法", "中间件", "配置文件",
    "类图", "类库",
]

# 英文术语与框架名——大小写不敏感、词边界匹配，命中即 FAIL
HARD_EN = [
    r"\bAPIs?\b", r"\bHTTPS?\b", r"\bJSON\b", r"\bXML\b", r"\bYAML\b",
    r"\bSQL\b", r"\bCRUD\b", r"\bORM\b", r"\bREST\b", r"\bJWT\b",
    r"\bDTOs?\b", r"\bDAOs?\b",
    r"\bfastapi\b", r"\bflask\b", r"\bdjango\b", r"\bpytest\b",
    r"\bpydantic\b", r"\bsqlalchemy\b", r"\bmybatis\b", r"\bjpa\b",
    r"\bhibernate\b", r"\bspring\s+boot\b", r"\bcontrolleradvice\b",
]

REQUIRED_SECTIONS = ["背景", "要什么", "验收标准"]
SPRINT_ID_RE = re.compile(r"S-\d{8}-\d{1,}")
SECTION_HEADING_RES = {
    "背景": re.compile(r"^#{2,6}\s*(?:业务背景|背景)\s*$", re.M),
    "要什么": re.compile(r"^#{2,6}\s*要什么\s*$", re.M),
    "验收标准": re.compile(r"^#{2,6}\s*验收标准\s*$", re.M),
}
# 模板元信息（格式说明行、HTML 注释）不参与扫描
META_LINE_RE = re.compile(r"^\s*(?:<!--|>\s*格式说明)")


def load_text(path):
    if path == "-":
        data = sys.stdin.buffer.read()
    else:
        try:
            with open(path, "rb") as f:
                data = f.read()
        except OSError as exc:
            print("[错误] 无法读取 %s：%s" % (path, exc))
            sys.exit(2)
    return data.decode("utf-8-sig", errors="replace")


def check_structure(text):
    problems, sprint_id = [], None
    for name in REQUIRED_SECTIONS:
        if not SECTION_HEADING_RES[name].search(text):
            problems.append("缺少「%s」章节标题（应为 ## / ### 级标题）" % name)
    m = SPRINT_ID_RE.search(text)
    if not m:
        problems.append("缺少 Sprint ID（格式 S-YYYYMMDD-N，N ≥1 位，须与复盘报告 / state 文件一致）")
    else:
        sprint_id = m.group(0)
    m = SECTION_HEADING_RES["验收标准"].search(text)
    if m:
        seg = text[m.end():]
        nxt = re.search(r"^#{1,6}\s", seg, re.M)
        if nxt:
            seg = seg[: nxt.start()]
        items = [l for l in seg.splitlines() if re.match(r"^\s*[-*]\s+\S", l)]
        if len(items) < 3:
            problems.append("验收标准只有 %d 条（要求 ≥3，含范围边界）" % len(items))
    return problems, sprint_id


def scan_terms(lines, allow):
    hard, soft, seen = [], [], set()

    def allowed(term):
        return any(term.lower() == a.lower() for a in allow)

    for no, line in enumerate(lines, 1):
        if META_LINE_RE.match(line):
            continue
        for term in HARD_CN:
            if term in line and (no, term) not in seen and not allowed(term):
                seen.add((no, term))
                hard.append((no, term, line.strip()))
        for term in SOFT_CN:
            if term in line and (no, term) not in seen and not allowed(term):
                seen.add((no, term))
                soft.append((no, term, line.strip()))
        for pat in HARD_EN:
            m = re.search(pat, line, re.IGNORECASE)
            if m and (no, m.group(0)) not in seen and not allowed(m.group(0)):
                seen.add((no, m.group(0)))
                hard.append((no, m.group(0), line.strip()))
    return hard, soft


def brief(line, limit=48):
    line = line.strip()
    return line[: limit - 1] + "…" if len(line) > limit else line


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass

    ap = argparse.ArgumentParser(
        description="需求卡发布前自检：三要素 / Sprint ID / 技术词泄漏")
    ap.add_argument("path", help="需求卡草稿路径（- 表示从 stdin 读）")
    ap.add_argument("--strict", action="store_true", help="软性告警也视为失败")
    ap.add_argument("--allow", action="append", default=[], metavar="词1,词2",
                    help="放行确属业务用法的词；可逗号分隔，可多次传入")
    args = ap.parse_args()

    allow = [t.strip() for chunk in args.allow for t in chunk.split(",") if t.strip()]

    text = load_text(args.path)
    lines = text.splitlines()

    print("=" * 56)
    print("需求卡发布前自检")
    print("=" * 56)

    problems, sprint_id = check_structure(text)
    for p in problems:
        print("[FAIL·结构] " + p)
    if not problems:
        print("[PASS·结构] 三要素齐全；Sprint ID %s 在位；验收标准 ≥3 条" % sprint_id)

    hard, soft = scan_terms(lines, allow)
    for no, term, line in hard:
        print("[FAIL·硬性] 第 %d 行命中技术词「%s」：%s" % (no, term, brief(line)))
    for no, term, line in soft:
        print("[WARN·软性] 第 %d 行疑似技术词「%s」（业务用法可 --allow 放行）：%s"
              % (no, term, brief(line)))
    if not hard and not soft:
        print("[PASS·口吻] 技术词扫描零命中")

    ok = not problems and not hard and (not args.strict or not soft)
    print("-" * 56)
    if ok:
        verdict = "通过" if not soft else "通过（含 %d 条软性告警，发布前自行确认）" % len(soft)
        print("结论：%s，可以发布。" % verdict)
        sys.exit(0)
    print("结论：不通过——按 FAIL 改写后重新自检。")
    sys.exit(1)


if __name__ == "__main__":
    main()
