# C# / Resilient Async Worker Engine

.NET 8 bounded channels, concurrent consumers, transient-failure retries and exponential backoff with cooperative cancellation. Demonstrates backpressure and deterministic failure injection.

```bash
dotnet run
```

Requires .NET 8 SDK; it was **not runtime-tested** in this build environment. Production queues also need an idempotency store, dead-letter queue and structured metrics.
