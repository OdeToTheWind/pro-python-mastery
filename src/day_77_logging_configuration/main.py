"""Day 77 – Logging & Configuration.

Scenario: a *food-delivery dispatch service* that reads its settings from
INI, YAML or TOML files (plus environment overrides) and logs to the console
for humans and to a rotating JSON file for machines.

Deliverables (syllabus):
* Logging handlers (StreamHandler, RotatingFileHandler), formatters (text and
  JSON), levels and per-logger configuration (``dictConfig``)
* Configuration with ``configparser`` (INI), YAML (``PyYAML``) and TOML (``tomllib``)
* Layered settings: defaults < file < environment variables, validated once
"""

from __future__ import annotations

import configparser
import json
import logging
import logging.config
import os
import tomllib
from collections.abc import Mapping
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any

import yaml

DELIVERABLES: dict[str, str] = {
    "configparser (INI)": "load_ini",
    "YAML (safe_load)": "load_yaml",
    "TOML (tomllib)": "load_toml",
    "layered settings with env overrides": "load_settings",
    "logging levels": "Settings.log_level",
    "JSON formatter": "JsonFormatter",
    "handlers + dictConfig": "configure_logging",
    "rotating file handler": "configure_logging",
    "contextual logging (extra fields)": "dispatch",
}

ENV_PREFIX = "DISPATCH_"
LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


@dataclass(frozen=True, slots=True)
class Settings:
    service: str = "dispatch"
    log_level: str = "INFO"
    max_drivers: int = 50
    surge_multiplier: float = 1.0
    log_file: str = ".data/dispatch.log"

    def __post_init__(self) -> None:
        if self.log_level not in LEVELS:
            raise ValueError(f"log_level must be one of {LEVELS}")
        if self.max_drivers < 1:
            raise ValueError("max_drivers must be positive")
        if not 1.0 <= self.surge_multiplier <= 5.0:
            raise ValueError("surge_multiplier must be between 1.0 and 5.0")


def _coerce(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Convert strings from INI/env into the dataclass field types; reject unknown keys."""
    types = {f.name: f.type for f in fields(Settings)}
    unknown = set(raw) - set(types)
    if unknown:
        raise KeyError(f"unknown settings: {sorted(unknown)}")
    converted: dict[str, Any] = {}
    for key, value in raw.items():
        kind = types[key]
        converted[key] = int(value) if kind == "int" else float(value) if kind == "float" else (
            str(value).upper() if key == "log_level" else str(value))
    return converted


def load_ini(text: str) -> dict[str, Any]:
    parser = configparser.ConfigParser()
    parser.read_string(text)
    return dict(parser["dispatch"]) if parser.has_section("dispatch") else {}


def load_yaml(text: str) -> dict[str, Any]:
    """Always ``safe_load``: plain ``yaml.load`` can construct arbitrary Python objects."""
    data = yaml.safe_load(text) or {}
    if not isinstance(data, dict):
        raise ValueError("YAML config must be a mapping")
    return dict(data.get("dispatch", {}))


def load_toml(text: str) -> dict[str, Any]:
    return dict(tomllib.loads(text).get("dispatch", {}))


LOADERS = {".ini": load_ini, ".cfg": load_ini, ".yaml": load_yaml, ".yml": load_yaml, ".toml": load_toml}


def load_settings(path: Path | None = None, env: Mapping[str, str] | None = None) -> Settings:
    """defaults < config file < environment variables (``DISPATCH_MAX_DRIVERS=80``)."""
    layered: dict[str, Any] = {}
    if path is not None:
        try:
            loader = LOADERS[path.suffix.lower()]
        except KeyError:
            raise ValueError(f"unsupported config format {path.suffix!r}") from None
        layered.update(loader(path.read_text(encoding="utf-8")))
    env = os.environ if env is None else env
    layered.update({k[len(ENV_PREFIX):].lower(): v for k, v in env.items() if k.startswith(ENV_PREFIX)})
    return Settings(**_coerce(layered))


class JsonFormatter(logging.Formatter):
    """One JSON object per line – easy for log platforms to index."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for key in ("order_id", "driver"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def configure_logging(settings: Settings, *, console: bool = True) -> logging.Logger:
    """Console (human text) + rotating JSON file, configured declaratively."""
    Path(settings.log_file).parent.mkdir(parents=True, exist_ok=True)
    handlers: dict[str, dict[str, Any]] = {
        "file": {"class": "logging.handlers.RotatingFileHandler", "filename": settings.log_file,
                 "maxBytes": 100_000, "backupCount": 3, "encoding": "utf-8", "formatter": "json",
                 "level": "DEBUG"},
    }
    if console:
        handlers["console"] = {"class": "logging.StreamHandler", "formatter": "text", "level": settings.log_level}
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"text": {"format": "%(asctime)s %(levelname)-8s %(name)s: %(message)s"},
                       "json": {"()": JsonFormatter}},
        "handlers": handlers,
        "loggers": {settings.service: {"level": "DEBUG", "handlers": list(handlers), "propagate": False}},
    })
    return logging.getLogger(settings.service)


def dispatch(logger: logging.Logger, order_id: str, drivers_free: int, settings: Settings) -> str:
    """Choose a log level that matches the situation; attach context with ``extra``."""
    context = {"order_id": order_id}
    if drivers_free == 0:
        logger.error("no drivers available", extra=context)
        return "queued"
    if drivers_free < settings.max_drivers // 10:
        logger.warning("low driver availability: %d free", drivers_free, extra=context)
    logger.debug("assigning driver from pool of %d", drivers_free, extra=context)
    logger.info("order dispatched", extra={**context, "driver": f"D{drivers_free:03d}"})
    return "dispatched"


SAMPLE_CONFIGS = {
    "dispatch.ini": "[dispatch]\nmax_drivers = 40\nlog_level = warning\n",
    "dispatch.yaml": "dispatch:\n  max_drivers: 60\n  surge_multiplier: 1.5\n",
    "dispatch.toml": "[dispatch]\nservice = \"dispatch-eu\"\nmax_drivers = 70\n",
}


def main() -> None:
    import tempfile

    print("Day 77 – Dispatch logging & config\n")
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        for name, text in SAMPLE_CONFIGS.items():
            (folder / name).write_text(text, encoding="utf-8")
            print(f"{name:<14} →", asdict(load_settings(folder / name, env={})))
        settings = load_settings(folder / "dispatch.toml", env={"DISPATCH_LOG_FILE": str(folder / "app.log"),
                                                                 "DISPATCH_LOG_LEVEL": "info"})
        logger = configure_logging(settings)
        for order, free in (("A-1", 30), ("A-2", 3), ("A-3", 0)):
            dispatch(logger, order, free, settings)
        for handler in logger.handlers:
            handler.close()
        print("\nlast JSON log line:", (folder / "app.log").read_text(encoding="utf-8").splitlines()[-1])


if __name__ == "__main__":
    main()
