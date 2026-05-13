from sqlalchemy import create_engine
import os
import pandas as pd

SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:sabi&22@localhost:5432/ohlcvt_db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

folder_path = "/Users/bushadigital/Downloads/master_q4"

columns= [
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "trades"
        ]

files = os.listdir(folder_path)

for file in files:
    if file.endswith(".csv"):

        full_path = os.path.join(folder_path, file)

        if os.path.getsize(full_path) == 0:
            print(f"Skipping {file} because it is empty.")
            continue

        df = pd.read_csv(full_path, header= None)

        first_row = df.iloc[0].astype(str).str.lower()

        if "timestamp" in first_row.values:
            df = df.iloc[1:]

        df = df.reset_index(drop=True)

        df.columns = columns

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit = 's', errors="coerce")
        df["timestamp"]= df["timestamp"].dt.floor("min")


        df.to_sql(
            "ohlcvt",
            engine,
            if_exists="append",
            index= False,
            method="multi",
            chunksize=2000
        )

        print(f"{file} uploaded successfully")


print("All Files Uploaded Successfully... yayyyyyyy")
