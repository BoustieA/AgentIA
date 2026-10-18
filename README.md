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
