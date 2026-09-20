"""Автоподхват пейлоадов из соседних модулей.

Имя команды: stem файла, `_` → `-` (`isad_pr1.py` → `isad-pr1`).
Дополнительные имена: `ALIASES` в модуле или `meta.aliases` в `PAYLOAD`.
"""

from __future__ import annotations

import importlib
from pathlib import Path

PAYLOADS: dict[str, dict] = {}

_pkg = Path(__file__).resolve().parent
for _path in sorted(_pkg.glob("*.py")):
    if _path.name.startswith("_"):
        continue
    _mod = importlib.import_module(f".{_path.stem}", __package__)
    _payload = getattr(_mod, "PAYLOAD", None)
    if _payload is None:
        continue
    _names = [_path.stem.replace("_", "-")]
    _names.extend(getattr(_mod, "ALIASES", ()))
    _names.extend((_payload.get("meta") or {}).get("aliases") or ())
    for _name in _names:
        PAYLOADS[_name] = _payload
