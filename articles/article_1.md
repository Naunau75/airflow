# 🚀 Retour d'expérience : Moderniser ses pipelines Airflow avec Kubernetes et uv

Nous avons tous été confrontés à ce dilemme en Data Engineering : comment garantir une **isolation parfaite** de nos tâches sans sacrifier la **performance** ?

L'utilisation de **KubernetesPodOperator** sur Airflow est souvent la réponse idéale pour l'isolation. Chaque tâche tourne dans son propre conteneur, avec ses propres ressources. C'est propre, c'est robuste.

Pourtant, cette robustesse a souvent un prix : la lourdeur. Des images Docker massives, des temps de démarrage ("cold starts") et une gestion des dépendances Python parfois capricieuse via `pip` ou `poetry`.

C'est là que j'ai décidé d'expérimenter une nouvelle approche en intégrant **uv**, le gestionnaire de paquets écrit en Rust par l'équipe d'Astral.

---

### 💡 Pourquoi ce changement ?

L'objectif n'était pas seulement de gagner quelques millisecondes, mais d'améliorer l'expérience de développement (DevEx) et la fiabilité en production.

En remplaçant mes installations classiques par `uv`, j'ai observé trois impacts majeurs :

1.  **Une vitesse de résolution fulgurante** : `uv` est incroyablement rapide. La résolution des dépendances et la création des environnements virtuels sont quasi-instantanées.
2.  **Des builds CD simplifiés** : Fini les minutes perdues à attendre l'installation des librairies lors de la construction des images Docker.
3.  **Une syntaxe unifiée** : Plus de jonglage. Un seul fichier `pyproject.toml` et une commande simple pour exécuter n'importe quel script.

### 🛠 Concrètement, ça donne quoi ?

L'intégration dans Airflow reste très élégante. Voici un extrait de mon DAG où j'utilise `uv` comme point d'entrée pour mes scripts Python :

```python
# Un exemple de tâche utilisant uv pour une exécution optimisée
task_extract = KubernetesPodOperator(
    task_id='extract_api_data',
    name='extract-job',
    # uv run s'occupe de l'environnement à la volée ⚡️
    cmds=["uv", "run", "python", "scripts/extract.py"],
    **common_pod_config
)
```

En une ligne, on s'assure que le script tourne dans un environnement déterministe, sans la latence habituelle.

### 🤝 Le mot de la fin

Associer la puissance d'orchestration d'**Airflow**, la flexibilité de **Kubernetes** et la performance de **Rust (via uv)** crée une stack vraiment plaisante à utiliser au quotidien. On passe moins de temps à attendre et plus de temps à créer de la valeur.

Et vous, quels outils utilisez-vous pour optimiser vos environnements Python en production ? Je serais curieux d'avoir vos retours ! 👇

#DataEngineering #Airflow #Python #Rust #Kubernetes #DevEx #OpenSource
