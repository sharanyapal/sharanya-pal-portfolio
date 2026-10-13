# SP Advanced Labs — Real Systems, Real Source

**15 additional engineering projects** built to extend the original Sharanya Pal cinematic portfolio. The first 10 are browser experiences; the remaining five are independently runnable Python/Java engines.

## Browser systems

| Folder | Core implementation |
| --- | --- |
| `apps/chess-engine` | Pseudo-legal move generation filtered for checks, complete castling/en passant/promotion, local 2-player, reversible state, minimax opponent |
| `apps/pac-maze` | Real-time animation, input state, tile collision, BFS ghost routing, timers and scoring |
| `apps/market-lab` | CSV ingest, EMA crossover, next-bar execution, fees, max drawdown, equity and trade report |
| `apps/vision-lab` | Permissioned webcam capture, on-device frame differencing and snapshot exports |
| `apps/chain-lab` | SHA-256 WebCrypto hash chain, asynchronous proof of work mining, tamper evidence |
| `apps/threat-lab` | Security-event parsing, sliding windows, brute-force and spray analytics |
| `apps/neural-playground` | 2→hidden→1 tanh/sigmoid neural network, hand-coded SGD backprop, synthetic datasets |
| `apps/growth-lab` | A/B two-proportion z-test and reproducible epsilon-greedy simulation |
| `apps/cloud-lab` | Replicated service + shared dependency model, seeded Monte Carlo failure simulation |
| `apps/climate-live` | **Real Open-Meteo** current weather and air-quality fetch + hourly forecast plot |

## Backend projects

- `python/stream-events`: event-time stream processing with watermarks, deduplication, out-of-order event buffering, sliding-window alerting
- `python/grounded-rag`: local BM25 passages, extractive evidence-first answers with abstention, optional authenticated OpenAI Responses API adapter (server-side `OPENAI_API_KEY` only)
- `python/quant-risk`: walk-forward backtesting, bootstrap value at risk and expected shortfall
- `python/image-forensics`: SHA-256 file integrity, visual difference hash, EXIF-safe re-encode (requires Pillow)
- `java/order-matching-engine`: price-time priority limit order book with synchronized matching, cancellation and partial fills

## Run

```bash
cd sharanya-advanced-labs
python -m http.server 8000
# http://localhost:8000
```

Python tests:

```bash
cd python/stream-events && python -m unittest discover -v
cd ../grounded-rag && python -m unittest discover -v
cd ../quant-risk && python -m unittest discover -v
cd ../image-forensics && python -m unittest discover -v
```

Java checks:

```bash
cd java/order-matching-engine
javac MatchingEngine.java && java -ea MatchingEngine
```

Browser cryptography and webcam require a secure origin (`https://` or `http://localhost`). The cloud, market and marketing simulations are explicitly **not live or production infrastructure**; the climate app retrieves actual current information from Open-Meteo.

### Security & integrity

- No API keys, tokens, private enterprise data or proprietary company code included.
- Webcam video and uploaded security logs are processed locally, never sent to a server.
- OpenAI inference is a *server-side optional integration*; no public unauthenticated paid inference endpoint is deployed.
- Applications are educational portfolio tools; not financial or security advice.
