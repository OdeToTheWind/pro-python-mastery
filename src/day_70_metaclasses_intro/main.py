"""Day 70 – Metaclasses (Introduction).

Scenario: a *document-converter app* with format plugins (Markdown → HTML,
CSV → JSON …). Every plugin class must declare its formats and is registered
automatically – first with a metaclass, then with the simpler
``__init_subclass__`` hook that is usually the better choice.

Deliverables (syllabus):
* ``type`` – the class of classes, and creating classes dynamically
* Custom metaclasses (``__new__`` to validate and register classes)
* When – and when not – to use them (``__init_subclass__``, decorators, conflicts)
"""

from __future__ import annotations

import csv
import io
import json
from typing import Any, ClassVar

DELIVERABLES: dict[str, str] = {
    "type is the class of classes": "type_facts",
    "creating a class dynamically with type()": "make_converter",
    "custom metaclass validating class definitions": "PluginMeta",
    "custom metaclass registering subclasses": "PluginMeta.registry",
    "simpler alternative: __init_subclass__": "Exporter",
    "metaclass conflicts (a reason to avoid them)": "metaclass_conflict",
    "decision guide": "WHEN_TO_USE",
}

WHEN_TO_USE: dict[str, str] = {
    "register subclasses automatically": "__init_subclass__ (no metaclass needed)",
    "validate class attributes at definition time": "__init_subclass__",
    "add methods/attributes to one class": "class decorator",
    "customise the class *namespace* or creation of the class object itself": "metaclass (e.g. Enum, ABCMeta, ORMs)",
    "anything an ordinary function or base class can do": "don't use a metaclass",
}


def type_facts() -> dict[str, bool]:
    class Example:
        pass

    return {
        "instance's class is Example": type(Example()) is Example,
        "Example's class is type": type(Example) is type,
        "type's class is type": type(type) is type,
        "classes are objects": isinstance(Example, object),
    }


class PluginMeta(type):
    """Runs when a *class* is defined (not when an instance is created)."""

    registry: ClassVar[dict[tuple[str, str], type]] = {}
    REQUIRED = ("source", "target")

    def __new__(mcls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> PluginMeta:
        cls = super().__new__(mcls, name, bases, namespace)
        if namespace.get("abstract", False):
            return cls  # the base class itself is not a plugin
        missing = [attr for attr in mcls.REQUIRED if not namespace.get(attr)]
        if missing:
            raise TypeError(f"{name} must define {', '.join(missing)}")
        if "convert" not in namespace:
            raise TypeError(f"{name} must implement convert()")
        key = (namespace["source"].lower(), namespace["target"].lower())
        if key in mcls.registry:
            raise TypeError(f"a converter for {key[0]}→{key[1]} already exists")
        mcls.registry[key] = cls
        return cls


class Converter(metaclass=PluginMeta):
    abstract = True
    source = ""
    target = ""

    def convert(self, text: str) -> str:
        raise NotImplementedError


class MarkdownToHtml(Converter):
    source, target = "md", "html"

    def convert(self, text: str) -> str:
        lines = []
        for line in text.splitlines():
            if line.startswith("# "):
                lines.append(f"<h1>{line[2:]}</h1>")
            elif line.strip():
                lines.append(f"<p>{line}</p>")
        return "\n".join(lines)


class CsvToJson(Converter):
    source, target = "csv", "json"

    def convert(self, text: str) -> str:
        return json.dumps(list(csv.DictReader(io.StringIO(text))))


def convert(text: str, source: str, target: str) -> str:
    try:
        plugin = PluginMeta.registry[(source.lower(), target.lower())]
    except KeyError:
        raise LookupError(f"no converter for {source}→{target}") from None
    return plugin().convert(text)  # type: ignore[no-any-return]


def make_converter(source: str, target: str, func: Any) -> type:
    """``type(name, bases, namespace)`` builds a class at runtime – and still goes
    through ``PluginMeta`` because the base class uses it."""
    name = f"{source.title()}To{target.title()}"
    return PluginMeta(name, (Converter,), {"source": source, "target": target,
                                                  "convert": lambda self, text: func(text)})


class Exporter:
    """The modern alternative: ``__init_subclass__`` runs for every subclass, no metaclass."""

    registry: ClassVar[dict[str, type[Exporter]]] = {}
    extension: ClassVar[str] = ""

    def __init_subclass__(cls, /, extension: str, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if not extension.startswith("."):
            raise TypeError("extension must start with '.'")
        cls.extension = extension
        Exporter.registry[extension] = cls


class PdfExporter(Exporter, extension=".pdf"):
    pass


class DocxExporter(Exporter, extension=".docx"):
    pass


def metaclass_conflict() -> str:
    """Two unrelated metaclasses can't be combined – one reason to avoid them."""

    class OtherMeta(type):
        pass

    class Other(metaclass=OtherMeta):
        pass

    try:
        type("Both", (Converter, Other), {"abstract": True})
    except TypeError as exc:
        return str(exc)
    return "no conflict"  # pragma: no cover


def main() -> None:
    print("Day 70 – Converter plugins\n")
    print("type facts:", type_facts())
    print("registered:", sorted(PluginMeta.registry))
    print(convert("# Title\nHello metaclasses", "md", "html"))
    print(convert("name,lang\nAda,Python", "csv", "json"))
    make_converter("txt", "upper", str.upper)
    print("dynamic class:", convert("shout", "txt", "upper"))
    try:
        PluginMeta("Broken", (Converter,), {"source": "x"})
    except TypeError as exc:
        print("rejected at definition time:", exc)
    print("exporters via __init_subclass__:", sorted(Exporter.registry))
    print("conflict:", metaclass_conflict())
    for need, answer in WHEN_TO_USE.items():
        print(f"  {need:<70} → {answer}")


if __name__ == "__main__":
    main()
