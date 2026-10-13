"""Run SQLite schema, seed and analytics with Python standard library."""
import sqlite3
from pathlib import Path
root=Path(__file__).parent
connection=sqlite3.connect(':memory:')
connection.executescript((root/'schema.sql').read_text())
connection.executescript((root/'seed.sql').read_text())
sql='\n'.join(line for line in (root/'analysis.sql').read_text().splitlines() if not line.lstrip().startswith('--'))
for query in sql.split(';'):
    if query.strip():
        try:
            cursor=connection.execute(query)
            if cursor.description:
                print([x[0] for x in cursor.description])
                for record in cursor.fetchall():print(record)
                print()
        except sqlite3.ProgrammingError as exc:
            print('SQL error:',exc)
connection.close()
