# 🚀 Data Pipeline: Airflow, dbt & BigQuery

Ce projet implémente un pipeline de données complet (ETL/ELT) orchestré par Apache Airflow, intégrant l'ingestion de données, la transformation via dbt, et le feature engineering avancé avec Python/Pandas sur Google Cloud Platform (BigQuery).

## 📋 Architecture du Pipeline

Le flux de données se décompose en 3 étapes principales, orchestrées séquentiellement :

1.  **Extraction (EL)** :
    *   Script : `scripts/extract.py`
    *   Action : Récupère les données utilisateurs depuis une API (JSONPlaceholder).
    *   Destination : Charge les données brutes dans BigQuery (`raw_data.users_raw`).

2.  **Transformation (T - dbt)** :
    *   Outil : dbt (data build tool)
    *   Action : Nettoyage, typage et standardisation des données.
    *   Modèle : `stg_users` (staging).
    *   Sortie : Table propre dans BigQuery (`dbt_staging.stg_users`).

3.  **Engineering (T - Python)** :
    *   Script : `scripts/transform.py`
    *   Action : Logique métier complexe (ex: scoring utilisateurs) difficile à implémenter en SQL pur.
    *   Sortie : Table analytique finale (`analytics.users_scored`).

---

## 🛠 Prérequis

*   **Python** (>= 3.12)
*   **uv** (Gestionnaire de paquets rapide)
*   **Compte Google Cloud Platform (GCP)** avec BigQuery activé.
*   **Service Account GCP** avec les droits BigQuery (Admin ou Data Editor).

## ⚙️ Installation

1.  **Cloner le dépôt** :
    ```bash
    git clone <votre-repo-url>
    cd airflow-projet
    ```

2.  **Installer les dépendances** avec `uv` :
    ```bash
    uv sync
    ```

3.  **Configuration dbt** :
    Assurez-vous que votre fichier `profiles.yml` est correctement configuré pour pointer vers votre projet GCP.

## 🚀 Utilisation

### Configuration de l'environnement

Créez un fichier `.env` ou exportez la variable d'environnement nécessaire :

```bash
export GCP_PROJECT_ID="votre-projet-gcp-id"
```

Pour l'authentification locale, utilisez le SDK Google Cloud :
```bash
gcloud auth application-default login
```

### Exécution Manuelle (Pas à pas)

Vous pouvez tester chaque brique individuellement via `uv` :

1.  **Extraction** :
    ```bash
    uv run python ../scripts/extract.py
    ```

2.  **Transformation dbt** :
    ```bash
    cd ../dbt_project
    uv run dbt run
    ```

3.  **Transformation Python** :
    ```bash
    uv run python ../scripts/transform.py
    ```

### Orchestration avec Airflow

Le DAG est défini dans `dags/pipeline_dag.py`.
*   Assurez-vous qu'Airflow est configuré pour scanner le dossier `dags`.
*   Le DAG `my_complete_pipeline` s'exécutera quotidiennement.

---

## ✅ CI/CD

Le projet inclut un workflow GitHub Actions (`.github/workflows/ci.yml`) qui :
*   Installe les dépendances avec `uv`.
*   Vérifie la qualité du code (Linting).
*   Teste la connexion dbt (`dbt debug`) à chaque Push/PR sur la branche `main`.

## 📂 Structure du Projet

```
.
├── airflow_projet/      # Configuration Python & CI
│   ├── pyproject.toml   # Dépendances du projet
│   ├── .github/         # Workflows CI/CD
│   └── README.md        # Documentation
├── dags/                # DAGs Airflow
│   └── pipeline_dag.py  # Définition du pipeline
├── dbt_project/         # Projet dbt
│   ├── models/          # Modèles SQL
│   └── profiles.yml     # Configuration connexion BQ
└── scripts/             # Scripts Python ETL
    ├── extract.py       # Ingestion API -> BQ
    └── transform.py     # Logique métier Python
```
