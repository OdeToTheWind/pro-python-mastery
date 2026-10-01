"""Day 88 – Capstone: Automated Report Generator.

Scenario: a *freelance design studio's month-end report*. Time-tracking
entries are aggregated per client and project with exact ``Decimal`` money,
then rendered three ways: an HTML e-mail body from ``string.Template``
(auto-escaped), a CSV for the accountant, and a one-page PDF written by hand
– no third-party PDF library needed.

Deliverables (syllabus):
* Data aggregation (group, sum, sort, totals, top client)
* ``string.Template`` rendering (with HTML escaping and missing-key checks)
* CSV output (``csv.DictWriter``, spreadsheet-safe values)
* PDF output (a minimal, valid PDF 1.4 document with a correct xref table)
"""

from __future__ import annotations

import csv
import html
import io
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from string import Template

DELIVERABLES: dict[str, str] = {
    "aggregation by client and project": "aggregate",
    "string.Template rendering": "render_html",
    "CSV export": "to_csv",
    "PDF export": "to_pdf",
    "one-call report build": "build_reports",
}

CENT = Decimal("0.01")


@dataclass(frozen=True, slots=True)
class Entry:
    day: date
    client: str
    project: str
    hours: Decimal
    rate: Decimal  # per hour


@dataclass(frozen=True, slots=True)
class Line:
    client: str
    project: str
    hours: Decimal
    amount: Decimal


@dataclass(frozen=True, slots=True)
class Summary:
    month: str
    lines: list[Line]
    per_client: dict[str, Decimal]
    total_hours: Decimal
    total: Decimal

    @property
    def top_client(self) -> str:
        return max(self.per_client, key=lambda c: (self.per_client[c], c)) if self.per_client else "-"


def aggregate(entries: list[Entry], month: str) -> Summary:
    """Only the given ``YYYY-MM``; money rounds once per line, never per entry."""
    hours: dict[tuple[str, str], Decimal] = defaultdict(Decimal)
    amounts: dict[tuple[str, str], Decimal] = defaultdict(Decimal)
    for e in entries:
        if e.day.strftime("%Y-%m") != month:
            continue
        if e.hours <= 0:
            raise ValueError(f"non-positive hours on {e.day} for {e.client}")
        key = (e.client.strip(), e.project.strip())
        hours[key] += e.hours
        amounts[key] += e.hours * e.rate
    lines = [Line(c, p, hours[(c, p)], amounts[(c, p)].quantize(CENT, ROUND_HALF_UP))
             for c, p in sorted(hours, key=lambda k: (-amounts[k], k))]
    per_client: dict[str, Decimal] = defaultdict(Decimal)
    for line in lines:
        per_client[line.client] += line.amount
    return Summary(month, lines, dict(sorted(per_client.items())), sum((ln.hours for ln in lines), Decimal()),
                   sum((ln.amount for ln in lines), Decimal("0.00")))


HTML_PAGE = Template("""<html><body>
<h1>$studio – report for $month</h1>
<p>Total: <strong>€$total</strong> for $hours hours. Top client: $top_client.</p>
<table>
<tr><th>Client</th><th>Project</th><th>Hours</th><th>Amount</th></tr>
$rows
</table>
</body></html>""")
HTML_ROW = Template("<tr><td>$client</td><td>$project</td><td>$hours</td><td>€$amount</td></tr>")


def render_html(summary: Summary, studio: str) -> str:
    """``substitute`` (not ``safe_substitute``) so a missing field fails loudly; every value is escaped."""
    rows = "\n".join(HTML_ROW.substitute(client=html.escape(ln.client), project=html.escape(ln.project),
                                         hours=ln.hours, amount=ln.amount) for ln in summary.lines)
    return HTML_PAGE.substitute(studio=html.escape(studio), month=summary.month, total=summary.total,
                                hours=summary.total_hours, top_client=html.escape(summary.top_client),
                                rows=rows or "<tr><td colspan=4>No work logged</td></tr>")


def _cell(value: str) -> str:
    """Neutralise spreadsheet formula injection (=, +, -, @ at the start of a cell)."""
    return "'" + value if value[:1] in {"=", "+", "-", "@"} else value


def to_csv(summary: Summary) -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=["client", "project", "hours", "amount_eur"], lineterminator="\n")
    writer.writeheader()
    for ln in summary.lines:
        writer.writerow({"client": _cell(ln.client), "project": _cell(ln.project),
                         "hours": ln.hours, "amount_eur": ln.amount})
    writer.writerow({"client": "TOTAL", "project": "", "hours": summary.total_hours, "amount_eur": summary.total})
    return buffer.getvalue()


def _pdf_text(value: str) -> str:
    safe = value.encode("latin-1", "replace").decode("latin-1")  # built-in fonts are Latin-1 only
    return safe.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def to_pdf(title: str, lines: list[str]) -> bytes:
    """Hand-built PDF: 5 objects, a content stream and a byte-exact cross-reference table."""
    text = [f"BT /F1 16 Tf 50 790 Td ({_pdf_text(title)}) Tj ET"]
    text += [f"BT /F1 10 Tf 50 {760 - 14 * i} Td ({_pdf_text(line)}) Tj ET" for i, line in enumerate(lines[:50])]
    stream = "\n".join(text).encode("latin-1")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> "
        b"/Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>",
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % number + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    out += b"".join(b"%010d 00000 n \n" % offset for offset in offsets)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objects) + 1, xref)
    return bytes(out)


def build_reports(entries: list[Entry], month: str, out_dir: Path, studio: str = "Pixel & Pine") -> dict[str, Path]:
    summary = aggregate(entries, month)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {"html": out_dir / f"report-{month}.html", "csv": out_dir / f"report-{month}.csv",
             "pdf": out_dir / f"report-{month}.pdf"}
    paths["html"].write_text(render_html(summary, studio), encoding="utf-8")
    paths["csv"].write_text(to_csv(summary), encoding="utf-8", newline="")
    pdf_lines = [f"{ln.client[:18]:<18} {ln.project[:18]:<18} {ln.hours:>6}h {ln.amount:>10}" for ln in summary.lines]
    pdf_lines += ["", f"{'TOTAL':<38} {summary.total_hours:>6}h {summary.total:>10}"]
    paths["pdf"].write_bytes(to_pdf(f"{studio} - {month}", pdf_lines))
    return paths


def sample_entries() -> list[Entry]:
    d, r = Decimal, date
    return [
        Entry(r(2026, 9, 2), "Café Lumen", "Menu redesign", d("3.5"), d("85")),
        Entry(r(2026, 9, 3), "Café Lumen", "Menu redesign", d("2.25"), d("85")),
        Entry(r(2026, 9, 9), "Nordwind GmbH", "Logo <v2>", d("6"), d("110")),
        Entry(r(2026, 9, 15), "=cmd|' /C calc'!A0", "Hostile import", d("1"), d("50")),
        Entry(r(2026, 9, 21), "Café Lumen", "Social posts", d("4"), d("70")),
        Entry(r(2026, 10, 1), "Nordwind GmbH", "Next month", d("8"), d("110")),
    ]


def main() -> None:
    import tempfile

    print("Day 88 – Month-end report generator\n")
    summary = aggregate(sample_entries(), "2026-09")
    print(to_csv(summary))
    print("top client:", summary.top_client)
    with tempfile.TemporaryDirectory() as tmp:
        for kind, path in build_reports(sample_entries(), "2026-09", Path(tmp)).items():
            print(f"{kind:>4}: {path.name} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
