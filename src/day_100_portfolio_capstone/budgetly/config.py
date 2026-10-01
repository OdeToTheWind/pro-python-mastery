"""Configuration: defaults < TOML file < environment variables."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

from .models import CATEGORIES, BudgetError


@dataclass(frozen=True)
class Config:
    db_path: Path = Path.home() / ".local" / "share" / "budgetly" / "budget.db"
    currency: str = "EUR"
    budgets: dict[str, Decimal] = field(default_factory=dict)
    log_level: str = "WARNING"


def load_config(path: Path | None = None, env: dict[str, str] | None = None) -> Config:
    env = dict(os.environ) if env is None else env
    values: dict[str, object] = {}
    if path is not None:
        if not path.exists():
            raise BudgetError(f"config file {path} does not exist")
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            raise BudgetError(f"config file {path} is invalid: {exc}") from None
        if "db_path" in data:
            values["db_path"] = Path(data["db_path"]).expanduser()
        if "currency" in data:
            values["currency"] = str(data["currency"])
        budgets = data.get("budgets", {})
        unknown = set(budgets) - set(CATEGORIES)
        if unknown:
            raise BudgetError(f"budgets for unknown categories: {', '.join(sorted(unknown))}")
        values["budgets"] = {k: Decimal(str(v)) for k, v in budgets.items()}
    if "BUDGETLY_DB" in env:
        values["db_path"] = Path(env["BUDGETLY_DB"]).expanduser()
    if "BUDGETLY_LOG_LEVEL" in env:
        level = env["BUDGETLY_LOG_LEVEL"].upper()
        if level not in {"DEBUG", "INFO", "WARNING", "ERROR"}:
            raise BudgetError(f"invalid BUDGETLY_LOG_LEVEL {level!r}")
        values["log_level"] = level
    return Config(**values)  # type: ignore[arg-type]
