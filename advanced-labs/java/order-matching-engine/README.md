# Order Matching Engine — Java

A synchronized limit order book with **price-time priority**, best bid/ask, partial fills, FIFO execution at price levels and cancellation. Uses TreeMap + ArrayDeque with deterministic order IDs and recorded trade fills.

```sh
javac MatchingEngine.java
java -ea MatchingEngine
```

No stock exchange connectivity, orders, or financial trades are performed: this is a self-contained matching-engine simulator.
