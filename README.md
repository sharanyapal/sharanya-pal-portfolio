# Sharanya Pal — Systems & Stories

<div align="center">

### A portfolio with a point of view

**Code you can inspect. Systems you can question. Interfaces you can explore.**

[Featured projects](./index.html) · [Career project index](./career/PROJECT_PORTFOLIO.md) · [Polyglot labs](./polyglot/) · [GitHub profile](https://github.com/sharanyapal)

</div>

---


**55 projects:** 24 foundational engineering apps, 15 advanced labs, and 16 new polyglot research and systems projects. The portfolio is a cinematic interactive website with **two curated, horizontally scrolling featured shelves**, genre filtering, keyboard-scroll navigation, and a collapsible archive for the previous 39 builds.

**Career project index:** [evidence-based IAM, cybersecurity, AI/ML and polyglot project showcase](./career/PROJECT_PORTFOLIO.md). This separates professional experience from personal projects and ongoing IIT Madras coursework.

## Polyglot expansion

All new projects are versioned in [`polyglot/`](./polyglot/). They use **Go (concurrent SSE and rate limiting), R (Bayesian experiments and portfolio risk), MATLAB/Octave (neural-network backprop), C11 (A* and ring buffers), C# (resilient asynchronous queues), Ruby (zero-trust policy DSL), MongoDB (aggregation analytics), TypeScript (event-sourced workflow DAGs), Python + Selenium (browser QA), and JavaScript/CSS (interactive web experiences)**.

### Playable browser demos

- [Event Horizon — Observability](./polyglot/sp-event-horizon/)
- [Attribution Atlas — Marketing science](./polyglot/sp-attribution-atlas/)
- [Graph Forge — Interactive path search](./polyglot/sp-graph-forge/)
- [Pixel Foundry — Image processing](./polyglot/sp-pixel-foundry/)

The app pages work without paid API keys or accounts. They use synthetic or user-imported local data unless explicitly stated otherwise. The language-specific services and algorithms are **source-run projects**, not misrepresented as cloud-deployed APIs.

## Beyond the featured shelves: classic C++

Alongside the 55 projects curated in this website, there is a separate **eight-project C++ console collection** on GitHub. It covers introductory banking and billing records, academic data, and familiar turn-based/word games:

| Records and real-world workflows | Games and control flow |
|:--|:--|
| [Bank Management](https://github.com/sharanyapal/cpp-bank-management-system) | [Tic-Tac-Toe](https://github.com/sharanyapal/cpp-tic-tac-toe) |
| [Library Management](https://github.com/sharanyapal/cpp-library-management-system) | [Snake & Ladder](https://github.com/sharanyapal/cpp-snake-and-ladder) |
| [Student Report Card](https://github.com/sharanyapal/cpp-student-report-card) | [Hangman](https://github.com/sharanyapal/cpp-hangman-game) |
| [Supermarket Billing](https://github.com/sharanyapal/cpp-supermarket-billing) | [Casino Guessing](https://github.com/sharanyapal/cpp-casino-number-guessing) |

These are independent source repositories, **not eight extra deployed games in the current portfolio site**. The C++ browser builds are experimental; the repositories link to their build status and document compiler compatibility constraints.

## Run locally

```bash
python -m http.server 8080
```

Open [localhost:8080](http://localhost:8080) from the directory containing `index.html`. Click **Now Showing** for the two featured rails or expand **Full Archive** for the previous projects. Public hosting requires an authorized deployment.

## Verification

CI runs Go race tests, C builds, Ruby Minitest, TypeScript tests, and Python syntax validation. R, MATLAB/Octave, and C# require their own runtimes for execution; those are not claimed as CI-passing. The Selenium QA suite additionally requires Chrome/Chromedriver and a served web application.

## GitHub, independent repositories, Vercel

The new 16 projects are included in this main repository as independent directories. The downloadable standalone release includes `publish_polyglot.py` (GitHub CLI authenticated publishing) and `deploy_windows.ps1` (Vercel CLI project linking and production deployment). Independent publication and remote hosting must be verified separately and are never inferred just from this commit.

**Security:** Do not commit tokens, account credentials, real production logs, customer information or paid API keys. User media and sample telemetry stay local to each app unless explicitly configured otherwise.
