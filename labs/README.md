# SP / THE BUILD VAULT — 24 engineering projects

A cinematic, interactive project gallery by **Sharanya Pal**, System Engineer (TCS Digital), with client-facing IAM support and ServiceNow catalog workflow experience.

**Live gallery:** https://sharanya-dev-labs.vercel.app  
**Source:** https://github.com/sharanyapal/sharanya-pal-portfolio/tree/main/labs

## 24 real projects

| Technology | Count | What is included |
|---|---:|---|
| Browser apps (HTML/CSS/JavaScript) | 12 | Access Matrix, Password Forge, JSON Studio, Regex Lab, CSV Insights, Hash Studio, Sorting Arena, Markdown Studio, Neon Runner, Finance Engine, TaskFlow, Prompt Lab |
| Python | 7 | IAM policy audit, local RAG retrieval with optional LLM, incident classifier, model benchmark, log anomaly monitor, API uptime monitor, integrity manifest CLI |
| Java | 4 | Atomic ledger transfers, Dijkstra shortest path, generic LRU cache, password policy validation |
| SQL | 1 | Retail analytics with window functions, joins, aggregate queries, indexes |

## Run locally

```bash
python -m http.server 8000
# Open http://localhost:8000/labs/ if this is inside the portfolio repository
```

Or run from inside this directory and open http://localhost:8000/.

Individual browser projects run through their `apps/<name>/index.html` paths. Python projects have their own `main.py` and optional `requirements.txt`. Java apps use `javac Main.java && java Main`, with self-tests via `java -ea Main --self-test`. SQL examples can be explored with `python sql/retail-analytics/demo.py`.

## Validate

```bash
node --check assets/gallery.js
for f in apps/*/app.js; do node --check "$f"; done
for d in python/*; do (cd "$d" && python -m pytest -q); done # install pytest, scikit-learn and httpx
```

## Engineering notes

These are **working educational demonstrations**, not production identity platforms or commercial banking software. The incident model uses a tiny synthetic dataset, the RAG app retrieves cited local passages and invokes an LLM only with your own configured API key. The browser Prompt Lab is a prompt composer and does not contact an LLM. None of the demos expose real customer data or production credentials.

No credentials are included. Deploy only the static gallery and `assets/`, `apps/` to a public host; keep Python/Java/SQL source in GitHub for runnable inspection.
