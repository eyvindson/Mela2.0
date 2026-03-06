import sqlite3
from pathlib import Path


def preview_sqlite(db_path):
    db_path = Path(db_path)

    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get table names
    cursor.execute("""
        SELECT name 
        FROM sqlite_master 
        WHERE type='table'
        ORDER BY name;
    """)
    tables = cursor.fetchall()

    if not tables:
        print("No tables found.")
        return

    for (table_name,) in tables:
        print("=" * 80)
        print(f"TABLE: {table_name}")
        print("=" * 80)

        # Fetch first 10 rows
        cursor.execute(f"SELECT * FROM '{table_name}' LIMIT 10;")
        rows = cursor.fetchall()

        # Get column names
        column_names = [description[0] for description in cursor.description]
        print("Columns:", column_names)
        print()

        for row in rows:
            print(row)

        print("\n\n")  # space between tables

    conn.close()


if __name__ == "__main__":
    preview_sqlite("/home/ubuntu/NEW_TEST/Mela2.0/out/chunk_002/out/simulation_results_dead_Y.db")