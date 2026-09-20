"""Запуск: python -m reportgen <payload> | all"""

from __future__ import annotations

import sys

from .generator import build_report
from .payloads import PAYLOADS


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    available = ", ".join(PAYLOADS) or "(нет модулей в payloads/)"
    if not args or args[0] in {"-h", "--help"}:
        print("Использование: python -m reportgen <имя>|all")
        print("Доступны:", available)
        return 0
    if args[0] == "all":
        example = PAYLOADS.get("example")
        seen: set[int] = set()
        targets = []
        for name, payload in PAYLOADS.items():
            if payload is example:
                continue
            marker = id(payload)
            if marker in seen:
                continue
            seen.add(marker)
            targets.append(name)
    else:
        targets = args
    unknown = [name for name in targets if name not in PAYLOADS]
    if unknown:
        print("Неизвестные пейлоады:", ", ".join(unknown))
        print("Доступны:", available)
        return 1
    for name in targets:
        path = build_report(PAYLOADS[name])
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
