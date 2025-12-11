FROM python:3.12-slim

# Installation de uv pour la gestion des dépendances
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Définition du dossier de travail
WORKDIR /app

# Optimisation du cache : on copie d'abord les fichiers de dépendances
# Note : pyproject.toml et uv.lock sont dans le sous-dossier airflow_projet/
COPY airflow_projet/pyproject.toml airflow_projet/uv.lock ./

# Installation des dépendances
# On utilise --system pour installer directement dans l'environnement Python global du conteneur
# ce qui évite d'avoir à gérer l'activation d'un venv
RUN uv sync --frozen --no-cache --system

# Copie de l'intégralité du projet
COPY . .

# Configuration des variables d'environnement
ENV PYTHONPATH=/app
ENV DBT_PROFILES_DIR=/app/dbt_project
ENV GCP_PROJECT_ID=""

# Commande par défaut
CMD ["bash"]
