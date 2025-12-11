# ⚡ Booster ses pipelines Data : Airflow + dbt + uv (le "game changer")

La vitesse d'exécution n'est pas qu'une métrique de vanité, c'est de l'argent.

Dans une architecture Data moderne sur **Kubernetes**, on a souvent le réflexe d'isoler chaque tâche (extraction, transformation, modèle ML) dans son propre Pod. C'est l'approche que j'utilise avec le `KubernetesPodOperator` d'Airflow pour garantir une isolation parfaite.

Mais il y a un coût caché : le **"Cold Start"**.

Si chaque lancement de tâche nécessite d'installer des dépendances Python via pip, on perd de précieuses minutes à chaque run, sans parler des coûts de compute inutiles sur le Cloud.

C'est là qu'intervient **uv**.

### 🦀 Pourquoi uv change la donne ?

J'ai récemment intégré `uv` (le gestionnaire de paquets écrit en Rust par Astral) au cœur de mon pipeline Airflow, et l'impact est immédiat.

Au lieu de gérer des environnements virtuels complexes ou d'attendre des résolutions de dépendances interminables, j'utilise `uv` directement dans mes définitions de tâches Airflow.

Voici à quoi ressemble une tâche dans mon DAG :

```python
# Exemple de tâche Airflow optimisée
task_extract = KubernetesPodOperator(
    task_id='extract_api',
    name='extract-job',
    # uv exécute le script à la vitesse de l'éclair ⚡️
    cmds=["uv", "run", "python", "scripts/extract.py"],
    **common_pod_config
)
```

### 🚀 Les 3 avantages concrets en Production

1.  **Builds Docker ultra-rapides** : En CI/CD, la construction de l'image unique du projet est drastiquement réduite grâce au cache et la vitesse de résolution de `uv`.
2.  **Runtime Overhead quasi-nul** : `uv run` est instantané. Il n'y a pas cette latence perceptible qu'on a parfois avec d'autres outils lors de l'initialisation de l'environnement au démarrage du Pod.
3.  **Gestion unifiée** : Plus besoin de jongler entre `pip`, `poetry` ou `venv`. Le fichier `pyproject.toml` est la seule source de vérité, et `uv` s'occupe du reste.

### 💡 Conclusion

L'architecture **Airflow + Kubernetes** est puissante pour la scalabilité. Mais couplée à des outils performants comme **uv** (et **dbt** pour la transfo), elle devient redoutablement efficace.

On ne parle plus seulement de faire passer de la donnée d'un point A à un point B, mais de le faire avec une ingénierie logicielle de pointe.

Et vous, vous utilisez quoi pour gérer vos deps Python en prod ? 👇

#DataEngineering #Rust #Python #Airflow #DevOps #GoogleCloud
