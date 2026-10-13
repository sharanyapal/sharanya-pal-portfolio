# Go / Streaming Telemetry Router

A small standard-library-only concurrent SSE server. Go channels separate the producer, detection engine and bounded subscribers; slow clients cannot stall ingestion. 5xx anomalies are detected using per-source sliding event-time windows.

```bash
go test ./...
go run .
# in another terminal
curl -N http://127.0.0.1:8088/events
```

Architecture: ticker → bounded channel → detector + fanout → SSE clients. Runs on localhost only. **Synthetic telemetry, not production logs.**
