import argparse
import json
import sys
from pathlib import Path

from insight_service import generate_manager_insight
from insight_service.domain.schemas import Task1InspectionOutput


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a plain-English manager insight from Task 1 JSON."
    )
    parser.add_argument(
        "--task1-json",
        required=False,
        help="Path to Task 1 JSON output file. If omitted, reads JSON from stdin.",
    )
    return parser


def _load_json(task1_json_path: str | None) -> dict:
    if task1_json_path:
        data = Path(task1_json_path).read_text(encoding="utf-8")
    else:
        data = sys.stdin.read()
    return json.loads(data)


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    try:
        obj = _load_json(args.task1_json)
        validated = Task1InspectionOutput.model_validate(obj)
        insight = generate_manager_insight(validated.model_dump())
        print(insight)
        return 0
    except Exception as exc:
        print(f"Failed to generate insight: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
