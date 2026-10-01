# Day 21 – Return vs. Print Reflection

**Date:** 2026-04-02 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_21_return_vs_print/main.py`](../../src/day_21_return_vs_print/main.py) · **Tests:** [`tests/test_day_21.py`](../../tests/test_day_21.py) (9 tests)

## Scenario
A *freelancer invoicing tool* – the same calculations written two ways (print-only vs return) to show why returning data is the reusable design.

## Syllabus deliverables
> Differentiating output vs return values, reusability and function design

| Deliverable | Implemented in |
|---|---|
| ✅ print-only function (anti-pattern) | `print_line_total` |
| ✅ returning function (reusable) | `line_total` |
| ✅ return value of a print-only function is None | `compare_designs` |
| ✅ reusability: composing returned values | `invoice_totals` |
| ✅ function design: pure core + I/O shell | `render_invoice` |

## Key learnings
- A function that only prints gives its caller `None`, so nothing can build on it.
- Keep a pure core (returns data) and a thin shell (prints, writes files, sends email).
- Returned values are trivially testable; printed text needs capturing.

## Pitfalls I hit (and how I fixed them)
- Discounts above 100 % produced negative invoices until the input was validated.

## Run it
```bash
python -m src.day_21_return_vs_print.main
pytest tests/test_day_21.py -v
```

## Next step
- Apply the pure-core/thin-shell split to the CLI capstone on Day 83.
