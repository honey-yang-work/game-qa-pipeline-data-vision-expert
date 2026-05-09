from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


CASE_COLUMNS = [
    "模块",
    "ID",
    "子功能",
    "标题",
    "优先级(P0-P3)",
    "追踪编号",
    "前置条件",
    "步骤",
    "预期结果",
]

RTM_COLUMNS = [
    "模块",
    "追踪编号",
    "追踪类型",
    "追踪描述",
    "测试用例ID",
    "覆盖状态",
    "备注",
]

CODE_TRACE_COLUMNS = [
    "需求ID",
    "表字段ID",
    "配置表路径",
    "Sheet",
    "配置字段",
    "配置值",
    "默认值",
    "边界值",
    "配置风险",
    "协议/入口",
    "业务承载",
    "数据承载",
    "输出承载",
    "风险点",
    "测试用例ID",
    "命中置信度",
]

CASE_ALIASES = {
    "模块": ["模块"],
    "ID": ["ID"],
    "子功能": ["子功能"],
    "标题": ["标题"],
    "优先级(P0-P3)": ["优先级(P0-P3)"],
    "追踪编号": ["追踪编号", "需求编号", "关联编号"],
    "前置条件": ["前置条件"],
    "步骤": ["步骤"],
    "预期结果": ["预期结果"],
}

RTM_ALIASES = {
    "模块": ["模块"],
    "追踪编号": ["追踪编号", "需求编号", "关联编号"],
    "追踪类型": ["追踪类型", "编号类型"],
    "追踪描述": ["追踪描述", "需求描述", "字段描述", "需求/字段描述"],
    "测试用例ID": ["测试用例ID"],
    "覆盖状态": ["覆盖状态"],
    "备注": ["备注"],
}

CODE_TRACE_ALIASES = {
    "需求ID": ["需求ID", "需求编号", "R"],
    "表字段ID": ["表字段ID", "字段ID", "T"],
    "配置表路径": ["配置表路径", "表格路径", "配置文件", "配置表"],
    "Sheet": ["Sheet", "工作表", "页签"],
    "配置字段": ["配置字段", "字段名", "配置列"],
    "配置值": ["配置值", "字段值", "命中值"],
    "默认值": ["默认值", "Default"],
    "边界值": ["边界值", "最小值/最大值", "范围"],
    "配置风险": ["配置风险", "配置问题", "配置缺陷"],
    "协议/入口": ["协议/入口", "入口", "协议", "路由", "RPC"],
    "业务承载": ["业务承载", "业务代码", "Service", "Handler", "Controller"],
    "数据承载": ["数据承载", "配置/DB/Cache", "配置", "DB", "Cache"],
    "输出承载": ["输出承载", "回包/事件/日志", "回包", "事件", "日志"],
    "风险点": ["风险点", "风险"],
    "测试用例ID": ["测试用例ID"],
    "命中置信度": ["命中置信度", "置信度"],
}

PRIORITY_PATTERN = re.compile(r"^P[0-3](?:\(.+\))?$")
TRACE_PATTERN = re.compile(r"\b[RT]\d+\b")
REQUIREMENT_PATTERN = re.compile(r"\bR\d+\b")
TABLE_FIELD_PATTERN = re.compile(r"\bT\d+\b")
CODE_TRACE_CONFIDENCE_VALUES = {"高", "中高", "低"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a game QA structured payload.")
    parser.add_argument("--input-json", required=True, help="Path to the input JSON file.")
    parser.add_argument("--system-name", default="", help="Optional expected system-name prefix.")
    return parser.parse_args()


def normalize_scalar(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value).strip()


def lookup(record: dict[str, Any], aliases: dict[str, list[str]], canonical_key: str) -> str:
    for alias in aliases[canonical_key]:
        if alias in record:
            return normalize_scalar(record[alias])
    return ""


def normalize_records(records: list[Any], columns: list[str], aliases: dict[str, list[str]]) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"row {index} must be an object")
        normalized.append({column: lookup(record, aliases, column) for column in columns})
    return normalized


def extract_trace_ids(value: str) -> set[str]:
    return set(TRACE_PATTERN.findall(value or ""))


def load_payload(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("Input JSON must be an object.")
    return payload


def validate_payload(payload: dict[str, Any], system_name: str = "") -> list[str]:
    errors: list[str] = []
    raw_cases = payload.get("test_cases")
    raw_rtm = payload.get("rtm")
    raw_code_trace = payload.get("code_traceability", [])

    if not isinstance(raw_cases, list):
        errors.append("test_cases must be a list")
        raw_cases = []
    if not isinstance(raw_rtm, list):
        errors.append("rtm must be a list")
        raw_rtm = []
    if raw_code_trace is None:
        raw_code_trace = []
    if not isinstance(raw_code_trace, list):
        errors.append("code_traceability must be a list when provided")
        raw_code_trace = []

    try:
        cases = normalize_records(raw_cases, CASE_COLUMNS, CASE_ALIASES)
    except ValueError as error:
        errors.append(f"test_cases {error}")
        cases = []

    try:
        rtm_rows = normalize_records(raw_rtm, RTM_COLUMNS, RTM_ALIASES)
    except ValueError as error:
        errors.append(f"rtm {error}")
        rtm_rows = []

    try:
        code_trace_rows = normalize_records(raw_code_trace, CODE_TRACE_COLUMNS, CODE_TRACE_ALIASES)
    except ValueError as error:
        errors.append(f"code_traceability {error}")
        code_trace_rows = []

    seen_case_ids: set[str] = set()
    case_trace_ids: set[str] = set()
    case_ids: set[str] = set()

    for index, case in enumerate(cases, start=1):
        row_label = f"test_cases[{index}]"
        case_id = case["ID"]
        if not case_id:
            errors.append(f"{row_label}.ID is required")
        elif case_id in seen_case_ids:
            errors.append(f"{row_label}.ID duplicate: {case_id}")
        else:
            seen_case_ids.add(case_id)
            case_ids.add(case_id)

        priority = case["优先级(P0-P3)"]
        if not PRIORITY_PATTERN.match(priority):
            errors.append(f"{row_label}.优先级(P0-P3) invalid: {priority!r}")

        traces = extract_trace_ids(case["追踪编号"])
        if not traces:
            errors.append(f"{row_label}.追踪编号 must include at least one R/T ID")
        case_trace_ids.update(traces)

        if system_name:
            if case["模块"] and not case["模块"].startswith(f"{system_name}-"):
                errors.append(f"{row_label}.模块 must start with {system_name}-")
            if case["子功能"] and not case["子功能"].startswith(f"{system_name}-"):
                errors.append(f"{row_label}.子功能 must start with {system_name}-")
            if case["标题"] and not case["标题"].startswith(f"{system_name}_"):
                errors.append(f"{row_label}.标题 must start with {system_name}_")

    rtm_trace_ids: set[str] = set()
    for index, row in enumerate(rtm_rows, start=1):
        row_label = f"rtm[{index}]"
        trace_ids = extract_trace_ids(row["追踪编号"])
        if not trace_ids:
            errors.append(f"{row_label}.追踪编号 must include an R/T ID")
        rtm_trace_ids.update(trace_ids)

        linked_ids = [item.strip() for item in re.split(r"[,，;；\s]+", row["测试用例ID"]) if item.strip()]
        if row["覆盖状态"] in {"Covered", "Partially Covered"} and not linked_ids:
            errors.append(f"{row_label}.测试用例ID is required when 覆盖状态 is {row['覆盖状态']}")
        for linked_id in linked_ids:
            if linked_id not in case_ids:
                errors.append(f"{row_label}.测试用例ID references unknown case: {linked_id}")

    missing_in_rtm = sorted(case_trace_ids - rtm_trace_ids)
    if missing_in_rtm:
        errors.append("trace IDs used by test cases but missing in RTM: " + ", ".join(missing_in_rtm))

    for index, row in enumerate(code_trace_rows, start=1):
        row_label = f"code_traceability[{index}]"
        if not REQUIREMENT_PATTERN.search(row["需求ID"]):
            errors.append(f"{row_label}.需求ID must include an R ID")
        if row["表字段ID"] and not TABLE_FIELD_PATTERN.search(row["表字段ID"]):
            errors.append(f"{row_label}.表字段ID must include a T ID when provided")
        if not row["协议/入口"]:
            errors.append(f"{row_label}.协议/入口 is required")
        if not row["业务承载"]:
            errors.append(f"{row_label}.业务承载 is required")
        if row["表字段ID"] and not (row["配置表路径"] or row["配置字段"]):
            errors.append(f"{row_label}.表字段ID provided but 配置表路径 or 配置字段 is missing")
        confidence = row["命中置信度"]
        if confidence not in CODE_TRACE_CONFIDENCE_VALUES:
            errors.append(f"{row_label}.命中置信度 must be one of 高 / 中高 / 低")

        linked_ids = [item.strip() for item in re.split(r"[,，;；\s]+", row["测试用例ID"]) if item.strip()]
        for linked_id in linked_ids:
            if linked_id not in case_ids:
                errors.append(f"{row_label}.测试用例ID references unknown case: {linked_id}")

    return errors


def main() -> int:
    args = parse_args()
    payload = load_payload(Path(args.input_json))
    errors = validate_payload(payload, args.system_name)
    if errors:
        print("PAYLOAD_INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PAYLOAD_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
