import pandas as pd
from google.cloud import bigquery
import os

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
SOURCE_TABLE = f"{PROJECT_ID}.dbt_staging.stg_users"
DEST_TABLE = f"{PROJECT_ID}.analytics.users_scored"

def advanced_transform():
    client = bigquery.Client(project=PROJECT_ID)
    
    # Lire les données clean
    query = f"SELECT * FROM `{SOURCE_TABLE}`"
    df = client.query(query).to_dataframe()
    
    print("Application de la logique métier...")
    # Exemple de logique Python : Scoring basé sur la longueur du nom
    # (Difficile à faire en SQL simple, justifie l'usage de Python ici)
    df['user_score'] = df['full_name'].apply(lambda x: len(x) * 1.5)
    
    # Sauvegarde finale
    df.to_gbq(
        destination_table=DEST_TABLE,
        project_id=PROJECT_ID,
        if_exists='replace'
    )
    print(f"Table finale créée : {DEST_TABLE}")

if __name__ == "__main__":
    advanced_transform()