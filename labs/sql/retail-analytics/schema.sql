-- Reproducible SQLite analytics dataset, synthetic retail transactions.
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS customers (customer_id INTEGER PRIMARY KEY, name TEXT NOT NULL, region TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS products (product_id INTEGER PRIMARY KEY, category TEXT NOT NULL, name TEXT NOT NULL, unit_price NUMERIC NOT NULL CHECK(unit_price>=0));
CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(customer_id), ordered_at TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('paid','refunded')));
CREATE TABLE IF NOT EXISTS order_items (order_id INTEGER NOT NULL REFERENCES orders(order_id), product_id INTEGER NOT NULL REFERENCES products(product_id), quantity INTEGER NOT NULL CHECK(quantity>0), PRIMARY KEY(order_id,product_id));
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(ordered_at);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
