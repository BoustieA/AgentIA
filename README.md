# Agent RAG pour la récupération des positions des programmes politiques

## Objectif

Ce projet vise à récupérer, via un système de recherche augmentée (RAG), les positions clés de différents programmes politiques à partir de documents PDF. 

Le système:

- indexe les PDF présents dans des dossiers de parti politique,
- stocke les embeddings dans une base vectorielle Chroma,
- expose un agent LangChain capable de rechercher dans ces bases,
- synthétise une réponse en s’appuyant sur les passages les plus pertinents de chaque document.

Le but est de répondre à des questions du type :

- « Quelle est la position de ce programme sur l’écologie ? »
- « Quels sont les points clés du programme X sur l’énergie ? »
- « Quelles différences majeures existent entre les programmes A et B ? »

---

## Principe de fonctionnement

Le projet repose sur un agent RAG :

1. Les documents PDF sont répartis par partis dans le dossier `politique/parti_x`.
2. Chaque dossier est transformé en une base vectorielle Chroma dans `chroma_db/`.
3. Un retriever est créé pour chaque base.
4. Un agent LangChain appelle ces retrievers et synthétise les informations retrouvées.
5. L’API FastAPI renvoie la réponse à une question posée par un utilisateur.

Le cœur du flux se trouve dans `main.py`.

---

## Architecture du projet

```text
agentIA/
├── main.py                 # API FastAPI + agent RAG
├── app.py                  # Interface Streamlit de test / chat
├── setup.py                # Script d’indexation des PDF vers Chroma
├── .gitignore              # Fichiers ignorés par Git
├── .env                    # Variables d’environnement locales
├── env/                    # Environnement virtuel Python local
├── politique/              # Dossiers de documents par programme (non versionné)
├── chroma_db/              # Bases vectorielles Chroma (non versionnée)
├── .git/                   # Git local du dépôt
└── README.md               # Documentation du projet
```

---

## Description des fichiers principaux

### `main.py`

Fichier principal du backend.

Il contient :

- le chargement des variables d’environnement,
- l’initialisation des embeddings HuggingFace,
- le chargement des bases Chroma depuis `chroma_db/`,
- la création de retrievers par programme,
- la création d’un agent LangChain,
- une route API `GET /ask` pour poser des questions en langage naturel.

Exemple de logique :

- chaque dossier de programme correspond à un retriever dédié,
- l’agent récupère les passages utiles de chaque source,
- la réponse est construite en combinant les résultats des outils.

### `app.py`

Petit client de démonstration basé sur Streamlit.

Il envoie la question de l’utilisateur à l’API FastAPI et affiche la réponse dans une interface de chat.

### `setup.py`

Script d’indexation des PDF.

Il permet de :

- parcourir les sous-dossiers de `politique/`,
- trouver tous les fichiers PDF,
- les diviser en chunks,
- les vectoriser avec des embeddings,
- les enregistrer dans `chroma_db/<nom_du_programme>`.

---

## Stack technique

- Python 3.11+
- FastAPI
- Streamlit
- LangChain
- Chroma
- HuggingFace embeddings
- Google Generative AI / modèles Gemini (via `langchain_google_genai`)
- dotenv

---

## Objectif fonctionnel détaillé

Le système est conçu pour analyser des programmes politiques à partir de documents PDF en répondant à des questions sur leurs positions stratégiques.

Il permet notamment :

- d’extraire les éléments de programme sur des sujets précis,
- d’identifier les positions de chaque formation politique,
- de comparer plusieurs programmes entre eux,
- de synthétiser une réponse structurée à partir de sources documentaires.

Le point important est que l’agent n’est pas un simple moteur de recherche brut : il agit comme un assistant qui cherche dans les bases vectorielles et reformule la réponse à partir des documents pertinents.

---

## Structure des dossiers et données externes

Le dépôt est volontairement minimaliste :

- le code applicatif est versionné,
- les documents source et les bases vectorielles ne sont pas inclus dans le dépôt Git.

### Dossier `politique/`

Le dossier `politique/` contient les PDF ou documents classés par programme politique. 

Il n’est pas intégré au dépôt Git et est donc normalement absent de la version partagée.

### Dossier `chroma_db/`

Le dossier `chroma_db/` stocke les bases vectorielles Chroma produites à partir des PDF.

Il est également ignoré par Git car il est généré localement et peut être volumineux.

### Fichier `.gitignore`

Le projet ignore explicitement :

```gitignore
politique
chroma_db
env
__pycache__
.env
```

Cela signifie que :

- les données politiques ne sont pas versionnées,
- la base vectoriale n’est pas enregistrée dans le dépôt,
- l’environnement virtuel local est exclu.

---

## Pré-requis

Avant de lancer le projet, il faut disposer de :

- Python installé,
- un environnement virtuel,
- un fichier `.env` avec les clés API nécessaires,
- des PDF dans le dossier `politique/` pour alimenter la base vectorielle.

---

## Déploiement local

### 1. Créer l’environnement virtuel

```bash
python -m venv env
```

### 2. Activer l’environnement

Sous Windows PowerShell :

```powershell
.\env\Scripts\Activate.ps1
```

### 3. Installer les dépendances

Selon votre configuration, installer les packages nécessaires pour LangChain, FastAPI, Streamlit, Chroma et les embeddings.

### 4. Configurer les variables d’environnement

Créer un fichier `.env` avec les variables nécessaires, notamment :

```env
GOOGLE_API_KEY=your_api_key
```

### 5. Préparer les documents

Ajouter les fichiers PDF dans les sous-dossiers de `politique/`.

### 6. Indexer les documents

Lancer le script d’indexation :

```bash
python setup.py
```

Cela créera les bases Chroma dans `chroma_db/`.

### 7. Lancer l’API

```bash
uvicorn main:app --reload
```

### 8. Lancer l’interface Streamlit

```bash
streamlit run app.py
```

---

## API

Le backend expose une route :

```http
GET /ask?question=Quelle est la position sur l'écologie ?
```

Réponse attendue :

```json
{
  "question": "Quelle est la position sur l'écologie ?",
  "response": "...réponse générée par l'agent à partir des sources pertinentes..."
}
```

---

## Points importants à retenir

- Le projet est un système RAG orienté politique.
- L’agent cherche des informations dans des bases vectorielles Chroma.
- Les programmes sont traités séparément puis combinés par l’agent.
- Le dossier `politique/` et la base `chroma_db/` ne sont pas présents dans le dépôt Git.
- L’objectif est bien d’extraire des positions politiques à partir de documents et de les synthétiser de manière exploitable.

---

## Conclusion

Ce projet combine :

- la récupération documentaire,
- l’indexation vectorielle,
- le raisonnement agentique,
- et la synthèse de réponses à partir de documents politiques.

Il fournit une base solide pour construire un assistant capable d’interroger des programmes à partir de leurs contenus officiels.
