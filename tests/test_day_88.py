"""Tests for Day 88 – Automated Report Generator."""

import csv
import io
import re
from datetime import date
from decimal import Decimal

import pytest

from src.day_88_automated_report_generator.main import (
    Entry,
    aggregate,
    build_reports,
    main,
    render_html,
    sample_entries,
    to_csv,
    to_pdf,
)


@pytest.fixture
def summary():
    return aggregate(sample_entries(), "2026-09")


def test_aggregation_groups_sorts_and_filters_month(summary):
    assert [(ln.client, ln.project, ln.amount) for ln in summary.lines][:2] == [
        ("Nordwind GmbH", "Logo <v2>", Decimal("660.00")),
        ("Café Lumen", "Menu redesign", Decimal("488.75"))]
    assert summary.per_client["Café Lumen"] == Decimal("768.75")
    assert summary.total == Decimal("1478.75") and summary.total_hours == Decimal("16.75")
    assert summary.top_client == "Café Lumen"


def test_rounding_happens_per_line_not_per_entry():
    entries = [Entry(date(2026, 1, d), "A", "p", Decimal("0.333"), Decimal("1.5")) for d in (1, 2, 3)]
    assert aggregate(entries, "2026-01").total == Decimal("1.50")  # 0.4995*3 → 1.4985 → 1.50


def test_aggregation_rejects_bad_hours_and_handles_empty():
    with pytest.raises(ValueError, match="non-positive"):
        aggregate([Entry(date(2026, 1, 1), "A", "p", Decimal("0"), Decimal("1"))], "2026-01")
    empty = aggregate([], "2026-01")
    assert empty.total == Decimal("0.00") and empty.top_client == "-"
    assert "No work logged" in render_html(empty, "Studio")


def test_html_is_escaped_and_complete(summary):
    page = render_html(summary, "Pixel & Pine")
    assert "Pixel &amp; Pine – report for 2026-09" in page and "Logo &lt;v2&gt;" in page
    assert "<strong>€1478.75</strong>" in page and "$" not in page


def test_csv_blocks_formula_injection(summary):
    rows = list(csv.DictReader(io.StringIO(to_csv(summary))))
    assert rows[-1] == {"client": "TOTAL", "project": "", "hours": "16.75", "amount_eur": "1478.75"}
    hostile = next(r for r in rows if "cmd" in r["client"])
    assert hostile["client"].startswith("'=")


def test_pdf_structure_and_xref_offsets():
    pdf = to_pdf("Report (draft)", ["Café 100%", r"back\slash"])
    assert pdf.startswith(b"%PDF-1.4") and pdf.rstrip().endswith(b"%%EOF")
    assert rb"(Report \(draft\))" in pdf and rb"back\\slash" in pdf and "Café".encode("latin-1") in pdf
    xref_at = int(pdf.rsplit(b"startxref\n", 1)[1].split()[0])
    assert pdf[xref_at:].startswith(b"xref")
    offsets = [int(m) for m in re.findall(rb"(\d{10}) 00000 n", pdf)]
    assert [pdf[o:].split(b"\n", 1)[0] for o in offsets] == [b"%d 0 obj" % n for n in range(1, 6)]
    length = int(re.search(rb"/Length (\d+)", pdf).group(1))
    assert pdf.split(b"stream\n", 1)[1][length:].startswith(b"\nendstream")


def test_build_reports_writes_three_files(tmp_path):
    paths = build_reports(sample_entries(), "2026-09", tmp_path / "out")
    assert sorted(p.suffix for p in paths.values()) == [".csv", ".html", ".pdf"]
    assert b"TOTAL" in paths["pdf"].read_bytes() and paths["csv"].read_text().startswith("client,")


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "top client: Café Lumen" in out and "pdf: report-2026-09.pdf" in out
