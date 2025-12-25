import pandas as pd
from sqlalchemy import create_engine
import os

# Folder with CSV files
raw_folder = "CDR_Raw"  # Make sure this folder exists and has your CSVs

# PostgreSQL connection details
db_user = "postgres"
db_pass = "Dev%40ti2016"   # @ replaced with %40
db_host = "localhost"
db_port = "5432"
db_name = "telco_cdr"

# Create SQLAlchemy engine
engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
)

# Loop through all CSV files in the folder
for file_name in os.listdir(raw_folder):
    if file_name.endswith(".csv"):
        file_path = os.path.join(raw_folder, file_name)
        print(f"Processing file: {file_name}")
        
        # Read CSV
        df = pd.read_csv(file_path)
        
        # Convert Timestamp column to datetime if it exists
        if 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        
        # Optional: create a Revenue column if Charge exists
        if 'Charge' in df.columns:
            df['Revenue'] = df['Charge'] * 1  # adjust formula if needed
        
        # Load to PostgreSQL, table will be created if it doesn't exist
        df.to_sql('CDR_Transformed', engine, if_exists='append', index=False)

print("ETL to PostgreSQL completed successfully!")
