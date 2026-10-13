# MongoDB / Commerce Cohort Analytics

Indexed event collections, per-user funnel state via `$group/$addToSet`, cohort conversion rates and pipeline assertions. Includes a synthetic fixture and avoids requiring any cloud connection.

```bash
mongosh --file pipeline.js
```

Use a local MongoDB 6+ server and shell. **Will replace only the `sp_analytics_demo` fixture database's `events` and `orders` collections**.
