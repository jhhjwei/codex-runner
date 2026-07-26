#!/usr/bin/env python3
"""Config-driven CSV/JSON transformer using only Python's standard library."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


TRUE_VALUES = {"1", "true", "yes", "y", "on"}
FALSE_VALUES = {"0", "false", "no", "n", "off", ""}


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    raise ValueError(f"invalid boolean: {value!r}")


def optional_number(value: Any) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    return float(value)


def normalize_rule(raw: dict[str, Any]) -> dict[str, Any]:
    source = str(raw.get("source", "")).strip()
    if not source:
        raise ValueError("every rule requires a non-empty 'source'")

    target = str(raw.get("target") or source).strip()
    data_type = str(raw.get("type") or "string").strip().lower()

    choices_raw = raw.get("choices")
    if isinstance(choices_raw, list):
        choices = [str(item) for item in choices_raw]
    elif choices_raw is None or str(choices_raw).strip() == "":
        choices = []
    else:
        choices = [item.strip() for item in str(choices_raw).split("|") if item.strip()]

    return {
        "source": source,
        "target": target,
        "type": data_type,
        "required": parse_bool(raw.get("required", False)),
        "default": raw.get("default", ""),
        "trim": parse_bool(raw.get("trim", True)),
        "case": str(raw.get("case") or "").strip().lower(),
        "multiplier": optional_number(raw.get("multiplier")),
        "offset": optional_number(raw.get("offset")),
        "min": optional_number(raw.get("min")),
        "max": optional_number(raw.get("max")),
        "choices": choices,
    }


def read_config(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        rules = payload["fields"] if isinstance(payload, dict) else payload
    elif suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rules = list(csv.DictReader(handle))
    else:
        raise ValueError("config must be .csv or .json")

    if not isinstance(rules, list) or not rules:
        raise ValueError("config must contain at least one field rule")
    return [normalize_rule(rule) for rule in rules]


def read_rows(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    if suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            payload = [payload]
        if not isinstance(payload, list) or any(not isinstance(row, dict) for row in payload):
            raise ValueError("JSON input must be an object or a list of objects")
        return payload
    raise ValueError("input must be .csv or .json")


def cast_value(value: Any, data_type: str) -> Any:
    if data_type in {"string", "str"}:
        return str(value)
    if data_type in {"integer", "int"}:
        numeric = float(value)
        if not numeric.is_integer():
            raise ValueError(f"not an integer: {value!r}")
        return int(numeric)
    if data_type in {"number", "float"}:
        return float(value)
    if data_type in {"boolean", "bool"}:
        return parse_bool(value)
    raise ValueError(f"unsupported type: {data_type}")


def transform_value(raw_value: Any, rule: dict[str, Any]) -> Any:
    missing = raw_value is None or str(raw_value).strip() == ""
    if missing:
        if rule["required"] and str(rule["default"]).strip() == "":
            raise ValueError("required value is missing")
        raw_value = rule["default"]

    if isinstance(raw_value, str) and rule["trim"]:
        raw_value = raw_value.strip()

    value = cast_value(raw_value, rule["type"])

    if isinstance(value, str):
        if rule["case"] == "lower":
            value = value.lower()
        elif rule["case"] == "upper":
            value = value.upper()
        elif rule["case"] not in {"", "keep"}:
            raise ValueError(f"unsupported case transform: {rule['case']}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if rule["multiplier"] is not None:
            value *= rule["multiplier"]
        if rule["offset"] is not None:
            value += rule["offset"]
        if rule["min"] is not None and value < rule["min"]:
            raise ValueError(f"value {value} is below minimum {rule['min']}")
        if rule["max"] is not None and value > rule["max"]:
            raise ValueError(f"value {value} is above maximum {rule['max']}")

    if rule["choices"] and str(value) not in rule["choices"]:
        raise ValueError(f"value {value!r} is not one of {rule['choices']}")

    return value


def transform_rows(
    rows: list[dict[str, Any]], rules: list[dict[str, Any]], strict: bool
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    output: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for row_number, row in enumerate(rows, start=2):
        transformed: dict[str, Any] = {}
        row_errors: list[dict[str, str]] = []

        for rule in rules:
            try:
                transformed[rule["target"]] = transform_value(row.get(rule["source"]), rule)
            except (TypeError, ValueError) as exc:
                row_errors.append({
                    "field": rule["source"],
                    "message": str(exc),
                })

        if row_errors:
            error_record = {"row": row_number, "errors": row_errors}
            errors.append(error_record)
            if strict:
                raise ValueError(json.dumps(error_record, ensure_ascii=False))
        else:
            output.append(transformed)

    return output, errors


def write_rows(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    suffix = path.suffix.lower()
    path.parent.mkdir(parents=True, exist_ok=True)

    if suffix == ".json":
        path.write_text(
            json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return

    if suffix == ".csv":
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return

    raise ValueError("output must be .csv or .json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Transform CSV/JSON records with rules stored in CSV or JSON."
    )
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--errors", type=Path, default=Path("errors.json"))
    parser.add_argument("--strict", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        rules = read_config(args.config)
        rows = read_rows(args.input)
        output, errors = transform_rows(rows, rules, args.strict)
        write_rows(args.output, output, [rule["target"] for rule in rules])
        args.errors.write_text(
            json.dumps(errors, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except (OSError, ValueError, json.JSONDecodeError, csv.Error) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"processed={len(rows)} accepted={len(output)} rejected={len(errors)}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
