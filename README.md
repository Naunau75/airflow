# 🚀 Data Pipeline: Airflow, dbt & BigQuery (Kubernetes)

Ce projet implémente un pipeline de données complet (ETL/ELT) orchestré par Apache Airflow, s'exécutant sur **Kubernetes**. Il intègre l'ingestion de données, la transformation via dbt, et le feature engineering avancé avec Python/Pandas sur Google Cloud Platform.

## 📋 Architecture du Pipeline

L'architecture repose sur la contenearisation de chaque tâche. Le DAG Airflow orchestre des **Pods Kubernetes** éphémères :

1.  **Extraction (EL)** :
    *   **Pod** : `extract-job`
    *   **Action** : Récupère les données API et charge les brutes dans BigQuery (`raw_data.users_raw`).

2.  **Transformation (T - dbt)** :
    *   **Pod** : `dbt-job`
    *   **Action** : Exécute `dbt run` pour nettoyer et typer les données (`stg_users`).

3.  **Engineering (T - Python)** :
    *   **Pod** : `transform-job`
    *   **Action** : Logique métier complexe en Python (`analytics.users_scored`).

---

## 🛠 Prérequis

*   **Cluster Kubernetes** (GKE ou local via Minikube/Docker Desktop).
*   **Airflow** déployé sur Kubernetes (ou configuré avec accès au cluster).
*   **Artifact Registry** (GCP) pour stocker l'image Docker.
*   **Service Account GCP** avec les droits BigQuery.

## ⚙️ Installation & Déploiement

Le déploiement repose sur une image Docker unique contenant tous les scripts et dépendances.

1.  **Build de l'image Docker** :
    ```bash
    # En local (pour test)
    docker build -t ma-pipeline-image:latest .
    ```

2.  **Configuration du DAG** :
    Modifiez `dags/pipeline_dag.py` pour pointer vers votre image Docker sur Artifact Registry :
    ```python
    image="europe-west1-docker.pkg.dev/mon-projet/mon-repo/mon-image:latest"
    ```

## 🚀 Utilisation

### Orchestration avec Airflow (Production)

Le DAG `my_complete_pipeline` utilise `KubernetesPodOperator`.
*   Chaque tâche démarre un conteneur isolé.
*   Les logs sont remontés dans l'interface Airflow.
*   Les ressources (CPU/RAM) sont libérées après chaque tâche.

### Exécution Manuelle (Développement)

Vous pouvez toujours exécuter les scripts manuellement en local via `uv` pour le debug :
```bash
uv run python scripts/extract.py
# etc...
```

---

## ✅ CI/CD (GitHub Actions)

Le workflow `.github/workflows/ci.yml` automatise la livraison continue :
1.  Authentification à GCP (via Workload Identity).
2.  Configuration de Docker.
3.  **Build** de l'image Docker.
4.  **Push** de l'image vers Google Artifact Registry à chaque merge sur `main`.

## 📂 Structure du Projet

```
.
├── Dockerfile           # Définition de l'image conteneur
├── airflow_projet/      # Méta-données Python
│   ├── pyproject.toml   # Dépendances (gérées par uv)
│   ├── .github/         # Workflow Build & Push
│   └── README.md        # Documentation
├── dags/                # DAGs Airflow (KubernetesPodOperator)
├── dbt_project/         # Projet dbt
└── scripts/             # Scripts Python ETL
```
