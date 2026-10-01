# Day 54 – Sending Email with Python and SMTP Reflection

**Date:** 2026-05-05 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_54_sending_email/main.py`](../../src/day_54_sending_email/main.py) · **Tests:** [`tests/test_day_54.py`](../../tests/test_day_54.py) (10 tests)

## Scenario
A *weekly study-report mailer*. It builds a proper MIME message (plain text + HTML + attachment), validates addresses, reads SMTP credentials from the environment and sends with ``smtplib`` over TLS – or does a dry run.

## Syllabus deliverables
> Automating email delivery with smtplib

| Deliverable | Implemented in |
|---|---|
| ✅ smtplib delivery (STARTTLS / SSL) | `send_email` |
| ✅ building a MIME message | `build_report_email` |
| ✅ attachments | `build_report_email` |
| ✅ address validation | `validate_address` |
| ✅ credentials from environment | `SmtpConfig.from_env` |
| ✅ dry-run mode for safe testing | `send_email` |

## Key learnings
- `EmailMessage` builds correct multipart messages (text, HTML, attachments).
- STARTTLS on port 587 or implicit SSL on 465, always with `ssl.create_default_context()`.
- Credentials come from the environment; `field(repr=False)` keeps them out of logs.

## Pitfalls I hit (and how I fixed them)
- Rejecting newlines in addresses prevents header injection (`\nBcc:`).

## Run it
```bash
./propython.sh 54                 # study mode: explanation, code map, notes and tests
python -m src.day_54_sending_email.main
pytest tests/test_day_54.py -v
```

## Next step
- Schedule weekly reports with the task runner (Day 89).
