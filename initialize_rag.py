import logging
import pymupdf
import re

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import VectorParams, Distance, PointStruct


# Configs
path = 'somme.pdf'
collection_name = 'somme_theologique'


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)


# Extract pdf
logging.info(f'[start] - Extracting text from {path}...')
with pymupdf.open(path) as doc:
    text = '\n'.join(page.get_text() for page in doc)
logging.info(f'[end] - Text extracted from {path} successfully!')


# Clean text
logging.info('[start] - Cleaning text...')
text = text.replace('\n', ' ').replace('\xa0', ' ')
text = re.sub(r'[_]{3,}', '', text)  # supprimer les longues séries de underscores
text = re.sub(r'\s{2,}', ' ', text)  # compacter les espaces
logging.info('[end] - Text cleaned successfully!')


# Split text into chunks
def split_text(text, max_length=500, overlap=50):
    _chunks = []
    start = 0
    while start < len(text):
        end = start + max_length
        _chunks.append(text[start:end])
        start += max_length - overlap
    return _chunks


logging.info('[start] - Splitting text into chunks...')
chunks = split_text(text)
logging.info(f'[end] - Text split into {len(chunks)} chunks successfully!')


# Init client
logging.info('[start] - Initializing Qdrant client...')
client = QdrantClient(host='localhost', port=6333)
logging.info('[end] - Qdrant client initialized successfully!')


# Delete the collection if it exists
if client.collection_exists(collection_name):
    logging.info(f'[start] - Collection {collection_name} already exists, deleting it...')
    client.delete_collection(collection_name)
    logging.info(f'[end] - Collection {collection_name} deleted successfully!')


# Create the collection
logging.info(f'[start] - Creating collection {collection_name}...')
client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
)
logging.info(f'[end] - Collection {collection_name} created successfully!')


# Transform chunks into vector
logging.info('[start] - Encoding text chunks into vectors...')
encoder = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
vectors = encoder.encode(chunks).tolist()
logging.info('[end] - Text chunks encoded into vectors successfully!')


# Upload chunks to Qdrant
logging.info(f'[start] - Uploading {len(chunks)} chunks to collection {collection_name}...')
client.upload_points(
    collection_name=collection_name,
    points=[PointStruct(id=i, vector=vec, payload={"text": chunks[i]}) for i, vec in enumerate(vectors)],
)
logging.info(f'[end] - {len(chunks)} chunks uploaded to collection {collection_name} successfully!')
