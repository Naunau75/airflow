import requests
import pandas as pd
from google.cloud import bigquery
import os

# Configuration
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = "raw_data"
TABLE_ID = "users_raw"
API_URL = "https://jsonplaceholder.typicode.com/users"

def extract_and_load():
    print(f"Extraction depuis {API_URL}...")
    response = requests.get(API_URL)
    data = response.json()
    
    # Création DataFrame
    df = pd.DataFrame(data)
    
    # Conversion types complexes en string pour le stockage RAW (simplification)
    df['address'] = df['address'].astype(str)
    df['company'] = df['company'].astype(str)

    # Chargement BigQuery
    client = bigquery.Client(project=PROJECT_ID)
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE", # Écrase la table à chaque run
        autodetect=True
    )
    
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()
    print(f"Chargé {job.output_rows} lignes dans {table_ref}.")

if __name__ == "__main__":
    extract_and_load()