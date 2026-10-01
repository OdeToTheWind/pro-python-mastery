# Day 61 – SMS / Notification Automation Reflection

**Date:** 2026-09-29 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_61_sms_notification_automation/main.py`](../../src/day_61_sms_notification_automation/main.py) · **Tests:** [`tests/test_day_61.py`](../../tests/test_day_61.py) (12 tests)

## Scenario
A *server-monitoring alerter* that texts the on-call engineer when a health check fails. It integrates with Twilio when credentials and the ``twilio`` package are present, and otherwise falls back to a safe dry run.

## Syllabus deliverables
> Twilio integration and secure secrets management

| Deliverable | Implemented in |
|---|---|
| ✅ Twilio client integration | `TwilioSender` |
| ✅ dry-run fallback | `DryRunSender` |
| ✅ choosing a transport safely | `make_sender` |
| ✅ secrets from environment | `TwilioConfig.from_env` |
| ✅ secret masking | `mask_sid` |
| ✅ phone number validation (E.164) | `validate_e164` |
| ✅ message composition and segment counting | `compose_alert` |

## Key learnings
- E.164 (`+14155550123`) is the only safe phone format for SMS APIs.
- Inject the Twilio client factory so the integration can be tested without the network.
- Choose a dry-run transport unless credentials *and* the library are present.

## Pitfalls I hit (and how I fixed them)
- Configured credentials without `twilio` installed used to crash with `ImportError`.

## Run it
```bash
./propython.sh 61                 # study mode: explanation, code map, notes and tests
python -m src.day_61_sms_notification_automation.main
pytest tests/test_day_61.py -v
```

## Next step
- Combine scraping, scheduling and notifications in the bot suite (Day 97).
