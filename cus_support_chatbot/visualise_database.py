import sqlite3
import pandas as pd
from database import update_dates

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_LLM_MODEL = os.getenv('GROQ_LLM_MODEL')
local_file = os.getenv('DB_file_name')

db = update_dates(local_file)

# Your db variable is the filename; first, create a connection
conn = sqlite3.connect(db)

# Visualize the tables
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tables in your DB:")
print(tables)

# Display data from each table
for table_name in tables['name']:
    print(f"\n--- {table_name} ---")
    df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 5;", conn)
    display(df)

# Close connection after visualization
conn.close()