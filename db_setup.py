import duckdb

def setup_database():
    conn = duckdb.connect('observability.db')
    conn.execute("""
        CREATE TABLE IF NOT EXISTS telemetry (
            server_id VARCHAR,
            metric_name VARCHAR,
            metric_value DOUBLE,
            timestamp TIMESTAMP
        )
    """)
    
    # Insert generated data
    conn.execute("""
        INSERT INTO telemetry
        SELECT *
        FROM read_csv_auto('telemetry.csv')
    """)
    
    print("Database setup complete!")
    conn.close()

if __name__ == "__main__":
    setup_database()