import getpass
import os
import shutil
import requests
import sqlite3
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

# Access variables using os.getenv
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_LLM_MODEL = os.getenv('GROQ_LLM_MODEL')
db = os.getenv('DB_file_name')
tavily_key = os.getenv("TAVILY_API_KEY")

# Database source was from Langchain    
# Alternative database is https://github.com/ebciii/travel_db?utm_source=chatgpt.com

db_url = "https://storage.googleapis.com/benchmarks-artifacts/travel-db/travel2.sqlite"
local_file = "travel2.sqlite"
# The backup lets us restart for each tutorial section
backup_file = "travel2.backup.sqlite"
overwrite = False

if overwrite or not os.path.exists(local_file):
    response = requests.get(db_url)
    response.raise_for_status()  # Ensure the request was successful
    with open(local_file, "wb") as f:
        f.write(response.content)
        
    # Backup - we will use this to "reset" our DB in each section
    shutil.copy(local_file, backup_file)

# Convert the flights to present time for our tutorial
def update_dates(file):
    shutil.copy(backup_file, file)

    # Connect to your SQLite database
    conn = sqlite3.connect(file)
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn).name.tolist()
    tdf = {}
    for t in tables:
        tdf[t] = pd.read_sql(f"SELECT * from {t}", conn)

    example_time = pd.to_datetime(
        tdf["flights"]["actual_departure"].replace("\\N", pd.NaT)
    ).max()
    current_time = pd.to_datetime("now").tz_localize(example_time.tz)
    time_diff = current_time - example_time

    tdf["bookings"]["book_date"] = (
        pd.to_datetime(tdf["bookings"]["book_date"].replace("\\N", pd.NaT), utc=True)
        + time_diff
    )

    datetime_columns = [
        "scheduled_departure",
        "scheduled_arrival",
        "actual_departure",
        "actual_arrival",
    ]
    for column in datetime_columns:
        tdf["flights"][column] = (
            pd.to_datetime(tdf["flights"][column].replace("\\N", pd.NaT)) + time_diff
        )

    for table_name, df in tdf.items():
        df.to_sql(table_name, conn, if_exists="replace", index=False)
    del df
    del tdf
    conn.commit()
    conn.close()
    return file

db = update_dates(local_file)