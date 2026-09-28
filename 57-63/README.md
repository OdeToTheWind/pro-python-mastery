# Pro-Python-Mastery – Intermediate Projects (Days 57–63)

API clients, automation & data acquisition (client-side only).

## Structure

```
pro-python-mastery/
├── src/
│   ├── day_57_rest_apis_json/main.py
│   ├── day_58_http_requests/main.py
│   ├── day_59_request_parameters_headers_payloads/main.py
│   ├── day_60_api_authentication/main.py
│   ├── day_61_sms_notification_automation/main.py
│   ├── day_62_web_scraping/main.py
│   └── day_63_browser_automation_selenium/main.py
├── tests/
│   ├── conftest.py
│   ├── test_day_57.py … test_day_63.py
├── progress/reflections/
│   ├── day-57-reflection.md … day-63-reflection.md
├── propython.sh
└── requirements.txt
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate          # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run a single day
python -m src.day_57_rest_apis_json.main

# Run the engineering check (days 57–63 + tests)
./propython.sh
```

## Notes

- Days that talk to the network (58–60, 62) use public demo services (jsonplaceholder, httpbin, quotes.toscrape.com).
- Day 61 (SMS) defaults to a safe dry-run unless real Twilio credentials are present in `.env`.
- Day 63 (Selenium) falls back to a dry-run explanation when Selenium / Chrome is not available.
- All modules are fully typed and come with unit tests that mock external calls.
