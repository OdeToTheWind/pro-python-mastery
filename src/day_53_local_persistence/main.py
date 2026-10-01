"""Day 53 – Local Persistence.

Scenario: a *language-learning app* that remembers each learner's XP, streak
and settings between runs – safely.

Deliverables (syllabus):
* Saving application state between runs
* Loading it back (with defaults, schema migration and corruption recovery)
* Safe persistence practices: atomic writes, explicit file location, autosave
"""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

DELIVERABLES: dict[str, str] = {
    "save state": "ProgressStore.save",
    "load state with defaults": "ProgressStore.load",
    "schema migration": "migrate",
    "corruption recovery with backup": "ProgressStore.load",
    "atomic writes": "ProgressStore.save",
    "explicit, git-ignored storage location": "default_store_path",
    "autosave on every change": "ProgressStore.update",
}

SCHEMA_VERSION = 2
DEFAULTS: dict[str, Any] = {"version": SCHEMA_VERSION, "xp": 0, "streak": 0, "language": "es",
                            "settings": {"sound": True, "daily_goal": 20}}


def default_store_path() -> Path:
    return Path.cwd() / ".data" / "progress.json"


def migrate(data: dict[str, Any]) -> dict[str, Any]:
    """Upgrade old save files instead of crashing on them.

    v1 stored ``score`` and ``level``; v2 renamed ``score`` → ``xp`` and dropped ``level``.
    """
    version = data.get("version", 1)
    if version == 1:
        data = {**data, "xp": data.get("score", 0), "version": 2}
        data.pop("score", None)
        data.pop("level", None)
    return data


def _merge_defaults(data: dict[str, Any]) -> dict[str, Any]:
    merged = {**DEFAULTS, **data}
    merged["settings"] = {**DEFAULTS["settings"], **data.get("settings", {})}
    return merged


class ProgressStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or default_store_path()
        self.data = self.load()

    def load(self) -> dict[str, Any]:
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(raw, dict):
                raise ValueError("progress file must hold a JSON object")
        except FileNotFoundError:
            return _merge_defaults({})
        except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
            # Never silently overwrite the user's data: keep a copy for recovery.
            backup = self.path.with_suffix(".json.corrupt")
            shutil.copy2(self.path, backup)
            return _merge_defaults({})
        return _merge_defaults(migrate(raw))

    def save(self) -> None:
        """Atomic: write a temp file then ``os.replace`` it over the real one."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=self.path.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(self.data, handle, indent=2, sort_keys=True)
            os.replace(tmp, self.path)
        except BaseException:
            Path(tmp).unlink(missing_ok=True)
            raise

    def update(self, **changes: Any) -> dict[str, Any]:
        """Change values and save immediately, so a crash never loses progress."""
        unknown = set(changes) - set(DEFAULTS)
        if unknown:
            raise KeyError(f"unknown fields: {sorted(unknown)}")
        self.data.update(changes)
        self.save()
        return self.data

    def add_xp(self, points: int) -> int:
        if points <= 0:
            raise ValueError("points must be positive")
        return int(self.update(xp=self.data["xp"] + points)["xp"])


def main(path: Path | None = None) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        target = path or Path(tmp) / "progress.json"
        print(f"Day 53 – Progress store at {target}\n")
        target.write_text('{"version": 1, "score": 120, "level": 3}', encoding="utf-8")
        store = ProgressStore(target)
        print("Migrated v1 save:", store.data)
        store.add_xp(30)
        store.update(streak=5)
        print("Reloaded from disk:", ProgressStore(target).data)
        target.write_text("{corrupted", encoding="utf-8")
        recovered = ProgressStore(target)
        print("After corruption:", recovered.data["xp"], "| backup kept:",
              target.with_suffix(".json.corrupt").exists())


if __name__ == "__main__":
    main()
