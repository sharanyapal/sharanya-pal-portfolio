# Python + Selenium / Portfolio End-to-End QA

Parameterized Chrome UI smoke tests for the four polyglot companion websites, plus a behavior assertion for attribution-model switching. Designed for local or CI headless Chrome via Selenium Manager.

```bash
pip install -r requirements.txt
# From the parent directory of the four website project folders:
python -m http.server 8080
# In a second terminal:
APP_BASE_URL=http://127.0.0.1:8080 pytest -q
```

Requires Chrome and Selenium; these E2E tests are **not automatically run** when browser drivers are unavailable.
