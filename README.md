# Sharanya Pal — Cinematic Portfolio + 24 Working Projects

**Production:** https://sharanya-pal-cinematic-portfolio.vercel.app/  
**24-project Build Vault:** https://sharanya-pal-cinematic-portfolio.vercel.app/#lab-vault

The main page is a cinematic, retro-tech portfolio with Signal Radio, six case-study episodes, a work/education timeline, an interactive terminal, and a **24-project Build Vault integrated into the homepage**.

The Build Vault is *not a directory of mockups*: all 12 HTML/JavaScript apps live under `labs/apps/`, each with browser-runnable code; seven Python tools, four Java apps and one SQL analytics demo live under `labs/python/`, `labs/java/` and `labs/sql/` with per-project README instructions and tests. The Python/Java/SQL tools are not offered as server-hosted interactive backends: run them locally using instructions in GitHub.

# Sharanya Pal — Systems & Stories

An original cinematic personal portfolio inspired by the browsing experiences of streaming platforms and the controls of music players. Built with HTML, CSS and vanilla JavaScript, with no dependencies or build step.

**Live portfolio:** [sharanya-pal-cinematic-portfolio.vercel.app](https://sharanya-pal-cinematic-portfolio.vercel.app)  
**LinkedIn:** [Sharanya Pal](https://www.linkedin.com/in/sharanya-pal-a9a637187/)

## Features

- Cinematic hero with original portrait photography and motion treatments
- Streaming-inspired project shelves and interactive case-study dialogs
- **Signal Radio:** a Spotify-inspired player with four original browser-generated synthesized soundscapes, playlist, seek, next/previous, volume and a floating mini-player
- Clear **Work & Education** timeline with filters and expandable roles
- Retro command-line interaction and keyboard command palette (`Ctrl/Cmd + K`)
- Responsive layouts, keyboard navigation, and reduced-motion support
- Contact shortcuts and mobile navigation

## Run locally

No installations required. Open `index.html` in a modern browser. For local server testing:

```bash
python -m http.server 8000
```

Then visit <http://localhost:8000>.

## Deploy

Import this repository into Vercel, and select **Other** (static website). Leave the build command empty and serve files directly from the repository root. The default document is `index.html`.

Alternatively, enable GitHub Pages from the repository root on the `main` branch.

## Edit

- `index.html`: page structure, professional details, headline, and SEO metadata
- `styles.css`: layout, colors, animation, responsiveness
- `script.js`: interactive projects, search, timeline, terminal, and audio controls
- `assets/`: web-optimized personal photos and the original favicon

Audio is synthesized locally by the Web Audio API; there are no third-party song files or streaming services.

## Professional content

This is a personal portfolio for a **System Engineer at TCS Digital**, working in the **IAM Support Analyst** capacity for Westpac Bank. It also describes ServiceNow Service Catalog/EAR work involving configuration, scripting, and workflows. This is not an official site of TCS or Westpac Bank. No client-confidential data or production code is published here.

## Images and reuse

The included photos are personal images of Sharanya Pal. Please do not reuse them without permission. This repository does not grant a license to third parties to redistribute personal photographs or other portfolio content.

© 2026 Sharanya Pal.
