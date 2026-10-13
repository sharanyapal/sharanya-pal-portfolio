# Go / Multi-Tenant Rate Governor

Thread-safe per-tenant token bucket with injectable clock, burst capacity, fractional refill and idle-key cleanup.

```bash
go test -race ./...
```

Ideal for API gateways and IAM login throttling. In-memory demo only; distributed quotas need Redis/atomic counters.
