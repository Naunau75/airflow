from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='my_complete_pipeline',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Configuration commune pour les pods
    common_pod_config = {
        "namespace": "default",
        "image": "europe-west1-docker.pkg.dev/mon-projet/mon-repo/mon-image:latest", # À remplacer par votre image
        "image_pull_policy": "Always",
        "service_account_name": "default", # SA avec droits BigQuery
        "get_logs": True,
        "is_delete_operator_pod": True,
        "env_vars": {'GCP_PROJECT_ID': 'mon-projet-gcp'}
    }

    # Etape 1: Extraction Python
    task_extract = KubernetesPodOperator(
        task_id='extract_api',
        name='extract-job',
        cmds=["uv", "run", "python", "scripts/extract.py"],
        **common_pod_config
    )

    # Etape 2: Transformation dbt (Clean)
    task_dbt = KubernetesPodOperator(
        task_id='dbt_clean',
        name='dbt-job',
        # On assume que dbt_project est à la racine dans l'image Docker
        cmds=["bash", "-c", "cd dbt_project && uv run dbt run"],
        **common_pod_config
    )

    # Etape 3: Engineering Python (Final)
    task_transform = KubernetesPodOperator(
        task_id='python_engineering',
        name='transform-job',
        cmds=["uv", "run", "python", "scripts/transform.py"],
        **common_pod_config
    )

    task_extract >> task_dbt >> task_transform