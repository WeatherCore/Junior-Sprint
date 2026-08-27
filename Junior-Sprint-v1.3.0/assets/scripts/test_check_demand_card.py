#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_demand_card.py 的回归自测。

直接 import 同目录下的 linter 模块，对核心函数做单元断言。
运行：python test_check_demand_card.py
依赖：本文件与 check_demand_card.py 同目录。
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_SPEC = importlib.util.spec_from_file_location(
    "check_demand_card", os.path.join(HERE, "check_demand_card.py")
)
linter = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(linter)


def _valid_card(sprint_id="S-20260820-01"):
    return """# 需求卡 · S-20260820-01

## 背景
用户希望标记待办为已完成，列表要能区分。

## 要什么
- 用户能标记一条待办为已完成
- 列表能区分已完成和未完成

## 验收标准
- 标记完成后列表能看出已完成
- 再点一次能取消标记
- 标记不存在的待办要明确提示
- 本次不做完成时间记录
""".replace("S-20260820-01", sprint_id)


def test_valid_passes():
    problems, sid = linter.check_structure(_valid_card())
    assert not problems, problems
    assert sid == "S-20260820-01"
    hard, soft = linter.scan_terms(_valid_card().splitlines(), [])
    assert not hard, hard


def test_single_digit_id_passes():
    text = _valid_card("S-20260820-1")
    problems, sid = linter.check_structure(text)
    assert not problems, problems
    assert sid == "S-20260820-1"


def test_tech_word_fails():
    text = _valid_card().replace("用户能标记一条待办为已完成",
                                 "新增一个接口接收标记请求")
    hard, _ = linter.scan_terms(text.splitlines(), [])
    assert any(t == "接口" for _, t, _ in hard), "应命中硬性词 接口"


def test_missing_section_fails():
    text = _valid_card().replace("## 验收标准", "## 其他")
    problems, _ = linter.check_structure(text)
    assert any("验收标准" in p for p in problems), problems


def test_missing_sprint_id_fails():
    text = _valid_card().replace("S-20260820-01", "需求卡")
    problems, sid = linter.check_structure(text)
    assert sid is None
    assert any("Sprint ID" in p for p in problems), problems


def test_allow_overrides_hard():
    text = _valid_card().replace("用户能标记一条待办为已完成",
                                 "新增一个接口接收标记请求")
    hard, _ = linter.scan_terms(text.splitlines(), ["接口"])
    assert not hard, "allow 后应不再命中 接口"


def test_strict_soft_word():
    text = _valid_card().replace("用户希望标记待办为已完成",
                                 "用户希望导出一个文件")
    _, soft = linter.scan_terms(text.splitlines(), [])
    assert any(t == "文件" for _, t, _ in soft), "文件 应为软性词"


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        t()
        print("  ✓ %s" % t.__name__)
        passed += 1
    print("Ran %d tests ... OK" % passed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
