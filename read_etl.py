import pandas as pd
import sqlite3
import os

# Define paths
raw_folder = "CDR_Raw"

for file_name in os.listdir(raw_folder):
    if file_name.endswith(".csv"):
        file_path = os.path.join(raw_folder, file_name)
        print(f"Processing file: {file_name}")

        df = pd.read_csv(file_path)

        # ADD THIS LINE
        print("Columns found:", df.columns)

        # Stop here temporarily
        break

db_file = "cdr_pipeline.db"

# Connect to SQLite DB
conn = sqlite3.connect(db_file)

# Process all CSV files
for file_name in os.listdir(raw_folder):
    if file_name.endswith(".csv"):
        file_path = os.path.join(raw_folder, file_name)
        print(f"Processing file: {file_name}")
        
        # Read CSV into pandas
        df = pd.read_csv(file_path)
        
        # Transform data
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.drop_duplicates(subset=['CallID'], inplace=True)
        df['Charge'] = df['Charge'].fillna(0)
        df['Revenue_USD'] = df['Duration'] * df['Charge'] / 60  # Optional calculation
        
        # Load into SQLite
        df.to_sql("CDR_Transformed", conn, if_exists="append", index=False)
        print(f"Loaded {len(df)} rows into database.\n")

# Close connection
conn.close()
print("ETL pipeline completed successfully!")
