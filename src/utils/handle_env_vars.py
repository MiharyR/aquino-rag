import os

from dotenv import load_dotenv


def handle_env_vars() -> dict:
    load_dotenv()
    return {
        'host': os.getenv('QDRANT_HOST', 'localhost'),
        'port': int(os.getenv('QDRANT_PORT', 6333)),
        'embedding_model_name': os.getenv('EMBEDDING_MODEL_NAME', 'camembert/flaubert')
    }
