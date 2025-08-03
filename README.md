# Aquino-rag

Ce projet permet:
1. d'initialiser un RAG
2. de poser des questions à ce RAG

Ce projet utilise la base vectoriel [Qdrant](https://qdrant.tech/qdrant-vector-database/).

### Table des matières
- [I. Pré-requis](#i-pré-requis)  
- [II. Initialiser le RAG](#ii-initialiser-le-rag)  
- [III. Poser une question au RAG](#iii-poser-une-question-au-rag)  



## I. Pré-requis
1. Installer docker

2. Installer python 3.11

3. Créer un environnement virtuel python3.11 :
```bash
python3.11 -m venv .venv/aquino_rag
source .venv/aquino_rag/bin/activate
which python
```

4. Installer les dépendances : `pip install -r requirements.txt`

5. Créer un fichier `.env` à la racine. Le rag l'utilisera pour se connecter à Qdrant.  
```ini
QDRANT_HOST='localhost'
QDRANT_PORT=6333
```




## II. Initialiser le rag

1/ Lancer Qdrant : `docker-compose up -d`

2/ Lancer le script d'initialisation du RAG :

- Commande : 
```bash
python src/initialize_rag/cli.py \
    --file-path <file_path> \
    --collection-name <collection_name>` \
    [--overwrite-collection]
```

- Exemple : 
```bash
python src/initialize_rag/cli.py \
    --file-path files/somme_theologique_72a102.pdf \
    --collection-name somme_theologique
```

- Paramètres :
  - `file_path` : chemin vers le fichier à indexer
  - `collection_name` : nom de la collection dans Qdrant où les vecteurs seront stockés
  - `overwrite_collection` : si la collection existe déjà, elle sera écrasée (optionnel, par défaut c'est `False`)


- Fonctionnement du script :
  1. Extrait le texte du fichier
  2. Nettoie le texte (si besoin)
  3. Découpe le texte en chunks
  4. Transforme les chunks en vecteurs
  5. Enregistre les vecteurs à Qdrant
      1. crée la collection si elle n'existe pas
      2. ajoute les vecteurs à la collection




## III. Poser une question au RAG

- Commande : 
```bash
python src/ask_question/cli.py \ 
    --question "<question>" \
    --collection-name <collection_name> \
    [--limit <limit>]
    [--score-threshold <score_threshold>]
```

- Exemple :
```bash
python src/cli/ask_question/cli.py \
    --question "Qu'est que la grâce ?" \
    --collection-name somme_theologique \
    --limit 5 \
    --score-threshold 0.7
```

- Paramètres :
  - `question` : la question à poser au RAG
  - `collection_name` : nom de la collection dans Qdrant où les vecteurs sont stockés
  - `limit` : nombre maximum de résultats à retourner (optionnel, par défaut c'est 3)
  - `score_threshold` : seuil de similarité pour filtrer les résultats (optionnel, par défaut c'est 0.5)


- Fonctionnement du script :
  1. Transforme la question en vecteurs
  2. Recherche les vecteurs les plus proches dans Qdrant
  3. Retourne les resultats correspondants
      - les chunks correspondants
      - le score de similarité
