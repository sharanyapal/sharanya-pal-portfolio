# C / A* Grid Search With Binary Heap

Low-level route planner on a blocked grid using an admissible Manhattan heuristic, priority heap and parent-chain reconstruction. Includes an executable expected-route assertion.

```bash
make
```

For larger graphs, use decrease-key / heap generations to avoid repeated insertions. The demo is deterministic.
