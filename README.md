# Aquino-rag

This project allows you to:
1. initialize a RAG
2. ask questions to this RAG

This project uses the vector database [Qdrant](https://qdrant.tech/qdrant-vector-database/).





## Table of Contents
- [I. Project structure](#i-project-structure)  
- [II. Prerequisites](#ii-prerequisites)  
- [III. Initialize rag](#iii-initialize-rag)
- [VI. Ask rag](#iv-ask-rag)





## I. Project structure
```
aquino-rag/
│
├── data/                                        # contains data which can be used
│   ├── somme.pdf
│   ├── somme_theologique_72a102.pdf
│   ⋮
│
├── src/                                         # contains all the source code
│   │
│   ├── ask_rag/                                 # contains all the code to ask questions to the RAG
│   │   ├── rag_answerer/                        # contains implementations of RAG answerers
│   │   ├── cli.py                               # cli (Command Line Interface)
│   │   ├── rag_answerer_name_to_class.py        # lists all the RAG answerers available
│   │   └── readme.md
│   │
│   ├── initialize_rag/                          # contains all the code to initialize the RAG
│   │   ├── rag_initializer/                     # contains implementations of RAG initializers
│   │   ├── cli.py                               # cli (Command Line Interface)
│   │   ├── rag_initializer_name_to_class.py     # list all the RAG initializers available
│   │   └── readme.md
│   │
│   │
│   └── utils/                                   # contains utility functions
│
├── .env
├── .gitignore
├── docker-compose.yml
├── README.md
└── requirements.txt
```





## II. Prerequisites

1. Instal docker

2. Install python3.11

3. Create a python3.11 virtual environment :
```bash
python3.11 -m venv .venv/aquino_rag
source .venv/aquino_rag/bin/activate
which python
```

4. Install dependencies : : `pip install -r requirements.txt`

5. Create a `.env` file at the root. The rag will use it to connect to Qdrant.
```ini
QDRANT_HOST='localhost'
QDRANT_PORT=6333
EMBEDDING_MODEL_NAME='camembert/flaubert'
```





## III. Initialize rag
[documentation](src/initialize_rag/readme.md) : `src/initialize_rag/readme.md`





## IV. Ask rag
[documentation](src/ask_rag/readme.md) : `src/ask_rag/readme.md`
