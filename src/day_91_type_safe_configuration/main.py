"""Day 91 – Capstone: Type-safe Configuration System.

Scenario: an *IoT fleet firmware-rollout service*. Its settings are frozen
dataclasses whose **type hints drive parsing**: environment variables such as
``FLEET_DB__PORT=5433`` or ``FLEET_ROLLOUT__REGIONS=eu,us`` are coerced to
``int``, ``bool``, ``Path``, ``Literal``, ``Enum``, tuples and secrets, every
problem is reported at once, and secrets never appear in logs.

Deliverables (syllabus):
* Dataclasses as typed schemas (frozen, nested sections, defaults)
* Validation (type coercion from hints + cross-field rules, all errors at once)
* Environment variables (prefix, ``__`` nesting, optional ``.env`` file)
* Safe output: masked secrets and generated documentation
"""

from __future__ import annotations

import enum
import types
from dataclasses import MISSING, dataclass, field, fields, is_dataclass
from pathlib import Path
from typing import Any, Literal, Union, get_args, get_origin, get_type_hints

from dotenv import dotenv_values

DELIVERABLES: dict[str, str] = {
    "typed settings schema": "Settings",
    "secret values that mask themselves": "Secret",
    "type-hint driven coercion": "coerce",
    "load from environment variables": "load_settings",
    "all errors reported together": "ConfigError",
    "cross-field validation": "Settings.__post_init__",
    "generated documentation": "describe",
    "safe dump for logs": "safe_dict",
}

PREFIX = "FLEET_"


class ConfigError(ValueError):
    def __init__(self, problems: list[str]) -> None:
        super().__init__("invalid configuration:\n  - " + "\n  - ".join(problems))
        self.problems = problems


class Secret:
    """Holds a value that ``repr``/``str``/f-strings never reveal."""

    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        self._value = value

    def reveal(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return "Secret('**********')"

    __str__ = __repr__

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Secret) and other._value == self._value

    def __hash__(self) -> int:
        return hash(self._value)


class Channel(enum.StrEnum):
    STABLE = "stable"
    BETA = "beta"
    CANARY = "canary"


@dataclass(frozen=True)
class Database:
    """Device registry database."""

    host: str = "localhost"
    port: int = 5432
    user: str = "fleet"
    password: Secret = field(default_factory=lambda: Secret(""))


@dataclass(frozen=True)
class Rollout:
    """How new firmware is pushed to devices."""

    channel: Channel = Channel.STABLE
    batch_percent: float = 5.0
    regions: tuple[str, ...] = ("eu",)
    pause_on_error_rate: float = 0.02
    dry_run: bool = True


@dataclass(frozen=True)
class Settings:
    environment: Literal["dev", "staging", "prod"] = "dev"
    firmware_dir: Path = Path("firmware")
    workers: int = 4
    webhook_url: str | None = None
    db: Database = field(default_factory=Database)
    rollout: Rollout = field(default_factory=Rollout)

    def __post_init__(self) -> None:
        problems = []
        if not 1 <= self.workers <= 64:
            problems.append("workers must be 1–64")
        if not 0 < self.rollout.batch_percent <= 100:
            problems.append("rollout.batch_percent must be in (0, 100]")
        if self.environment == "prod":
            if self.rollout.channel is Channel.CANARY:
                problems.append("prod may not roll out the canary channel")
            if not self.db.password.reveal():
                problems.append("db.password is required in prod")
        if problems:
            raise ConfigError(problems)


TRUE, FALSE = {"1", "true", "yes", "on"}, {"0", "false", "no", "off"}


def coerce(raw: str, hint: Any) -> Any:
    """Convert one string into the annotated type – the heart of 'type-safe'."""
    origin, args = get_origin(hint), get_args(hint)
    if origin in (Union, types.UnionType):
        if raw.strip().lower() in {"", "none", "null"} and type(None) in args:
            return None
        (inner,) = [a for a in args if a is not type(None)]
        return coerce(raw, inner)
    if origin is Literal:
        if raw not in args:
            raise ValueError(f"expected one of {', '.join(map(str, args))}")
        return raw
    if origin is tuple:
        return tuple(coerce(part.strip(), args[0]) for part in raw.split(",") if part.strip())
    if hint is bool:
        value = raw.strip().lower()
        if value not in TRUE | FALSE:
            raise ValueError("expected true/false")
        return value in TRUE
    if isinstance(hint, type) and issubclass(hint, enum.Enum):
        try:
            return hint(raw.lower())
        except ValueError:
            raise ValueError(f"expected one of {', '.join(m.value for m in hint)}") from None
    if hint in (int, float, str, Path, Secret):
        return hint(raw)
    raise TypeError(f"unsupported config type {hint!r}")


def _build(cls: type, env: dict[str, str], path: str, problems: list[str]) -> Any:
    hints = get_type_hints(cls)
    values: dict[str, Any] = {}
    for f in fields(cls):
        hint = hints[f.name]
        dotted = f"{path}{f.name}"
        if is_dataclass(hint):
            values[f.name] = _build(hint, env, f"{dotted}.", problems)  # type: ignore[arg-type]
            continue
        key = PREFIX + dotted.replace(".", "__").upper()
        if key in env:
            try:
                values[f.name] = coerce(env[key], hint)
            except (ValueError, TypeError) as exc:
                problems.append(f"{key}={'***' if hint is Secret else repr(env[key])}: {exc}")
    try:
        return cls(**values)
    except ConfigError as exc:
        problems.extend(exc.problems)
        return None
    except TypeError:  # pragma: no cover - an inner section already failed
        return None


def load_settings(env: dict[str, str], env_file: Path | None = None) -> Settings:
    """Precedence: defaults < ``.env`` file < real environment."""
    merged = {k: v for k, v in (dotenv_values(env_file) if env_file else {}).items() if v is not None}
    merged.update(env)
    unknown = sorted(k for k in merged if k.startswith(PREFIX) and k not in known_keys())
    problems = [f"unknown setting {k} (typo?)" for k in unknown]
    settings = _build(Settings, merged, "", problems)
    if problems:
        raise ConfigError(problems)
    return settings


def known_keys(cls: type = Settings, path: str = "") -> set[str]:
    keys: set[str] = set()
    hints = get_type_hints(cls)
    for f in fields(cls):
        if is_dataclass(hints[f.name]):
            keys |= known_keys(hints[f.name], f"{path}{f.name}.")
        else:
            keys.add(PREFIX + f"{path}{f.name}".replace(".", "__").upper())
    return keys


def _default(f: Any) -> Any:
    return f.default if f.default is not MISSING else f.default_factory()


def _type_name(hint: Any) -> str:
    origin, args = get_origin(hint), get_args(hint)
    if origin in (Union, types.UnionType):
        return " / ".join(_type_name(a) for a in args if a is not type(None)) + " (optional)"
    if origin is Literal:
        return " / ".join(map(str, args))
    if origin is tuple:
        return f"comma-separated {_type_name(args[0])}"
    if isinstance(hint, type) and issubclass(hint, enum.Enum):
        return " / ".join(m.value for m in hint)
    return str(hint.__name__)


def describe(cls: type = Settings, path: str = "") -> list[str]:
    """One Markdown table row per variable – documentation that cannot drift from the code."""
    rows = ["| Variable | Type | Default |", "|---|---|---|"] if not path else []
    hints = get_type_hints(cls)
    for f in fields(cls):
        hint = hints[f.name]
        if is_dataclass(hint):
            rows += describe(hint, f"{path}{f.name}.")  # type: ignore[arg-type]
            continue
        name = PREFIX + f"{path}{f.name}".replace(".", "__").upper()
        type_name = _type_name(hint)
        default = _default(f)
        shown = ",".join(default) if isinstance(default, tuple) else getattr(default, "value", default)
        rows.append(f"| `{name}` | {type_name} | `{shown}` |")
    return rows


def safe_dict(obj: Any) -> Any:
    if is_dataclass(obj) and not isinstance(obj, type):
        return {f.name: safe_dict(getattr(obj, f.name)) for f in fields(obj)}
    if isinstance(obj, Secret):
        return "**********" if obj.reveal() else ""
    if isinstance(obj, enum.Enum):
        return obj.value
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, tuple):
        return list(obj)
    return obj


def main() -> None:
    print("Day 91 – Typed configuration for a firmware rollout\n")
    env = {"FLEET_ENVIRONMENT": "staging", "FLEET_DB__PORT": "5433", "FLEET_DB__PASSWORD": "s3cr3t",
           "FLEET_ROLLOUT__REGIONS": "eu, us ,apac", "FLEET_ROLLOUT__DRY_RUN": "no"}
    settings = load_settings(env)
    print(settings.db)
    print(safe_dict(settings))
    try:
        load_settings({"FLEET_ENVIRONMENT": "prod", "FLEET_WORKERS": "lots", "FLEET_ROLLOUT__CHANNEL": "canary",
                       "FLEET_DB_PASSWORD": "typo"})
    except ConfigError as exc:
        print(exc)
    print("\n".join(describe()[:5]), "\n…")


if __name__ == "__main__":
    main()
