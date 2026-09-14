"""Запуск: python -m reportgen pr1 | pr2 | all"""

from __future__ import annotations

import sys

from .generator import build_report
from .payloads import PAYLOADS


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {"-h", "--help"}:
        print("Использование: python -m reportgen [pr1|pr2|isad-pr1|isad-pr2|all]")
        return 0
    targets = list(PAYLOADS) if args[0] == "all" else args
    unknown = [name for name in targets if name not in PAYLOADS]
    if unknown:
        print("Неизвестные пейлоады:", ", ".join(unknown))
        print("Доступны:", ", ".join(PAYLOADS))
        return 1
    for name in targets:
        path = build_report(PAYLOADS[name])
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
