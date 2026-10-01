"""Tests for Day 70 – Metaclasses."""

import json

import pytest

from src.day_70_metaclasses_intro.main import (
    WHEN_TO_USE,
    Converter,
    CsvToJson,
    DocxExporter,
    Exporter,
    MarkdownToHtml,
    PdfExporter,
    PluginMeta,
    convert,
    main,
    make_converter,
    metaclass_conflict,
    type_facts,
)


@pytest.fixture
def clean_registry():
    saved = dict(PluginMeta.registry)
    yield
    PluginMeta.registry.clear()
    PluginMeta.registry.update(saved)


def test_type_facts():
    assert all(type_facts().values())


def test_metaclass_is_the_class_of_plugins():
    assert type(MarkdownToHtml) is PluginMeta
    assert isinstance(Converter, type)


def test_plugins_are_registered_automatically():
    assert PluginMeta.registry[("md", "html")] is MarkdownToHtml
    assert PluginMeta.registry[("csv", "json")] is CsvToJson
    assert Converter not in PluginMeta.registry.values()


def test_convert_dispatches_through_registry():
    assert convert("# Hi\n\ntext", "MD", "HTML") == "<h1>Hi</h1>\n<p>text</p>"
    assert json.loads(convert("a,b\n1,2", "csv", "json")) == [{"a": "1", "b": "2"}]
    with pytest.raises(LookupError):
        convert("x", "pdf", "md")


@pytest.mark.usefixtures("clean_registry")
@pytest.mark.parametrize(
    ("namespace", "message"),
    [({"source": "x"}, "must define target"),
     ({"source": "x", "target": "y"}, "must implement convert"),
     ({"source": "md", "target": "html", "convert": lambda s, t: t}, "already exists")],
)
def test_metaclass_rejects_bad_classes_at_definition_time(namespace, message):
    with pytest.raises(TypeError, match=message):
        type(Converter)("Bad", (Converter,), namespace)


@pytest.mark.usefixtures("clean_registry")
def test_dynamic_class_creation_with_type():
    cls = make_converter("txt", "rev", lambda text: text[::-1])
    assert cls.__name__ == "TxtToRev" and type(cls) is PluginMeta
    assert convert("abc", "txt", "rev") == "cba"


@pytest.mark.usefixtures("clean_registry")
def test_class_statement_triggers_metaclass():
    class YamlToJson(Converter):
        source, target = "yaml", "json"

        def convert(self, text):
            return text

    assert PluginMeta.registry[("yaml", "json")] is YamlToJson


def test_init_subclass_alternative():
    assert Exporter.registry[".pdf"] is PdfExporter and DocxExporter.extension == ".docx"
    assert type(PdfExporter) is type  # no custom metaclass involved
    with pytest.raises(TypeError, match="start with"):
        type("Bad", (Exporter,), {}, extension="txt")


def test_metaclass_conflict():
    assert "metaclass conflict" in metaclass_conflict()


def test_decision_guide_prefers_simpler_tools():
    assert WHEN_TO_USE["register subclasses automatically"].startswith("__init_subclass__")
    assert "don't" in WHEN_TO_USE["anything an ordinary function or base class can do"]


@pytest.mark.usefixtures("clean_registry")
def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "dynamic class: SHOUT" in out and "rejected at definition time: Broken must define target" in out
