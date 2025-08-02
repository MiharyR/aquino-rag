from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


# query
query = 'Qu’est-ce que la grâce selon Thomas d’Aquin ?'


# Vectorized query
encoder = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
query_vectorized = encoder.encode(query).tolist()


# Ask query
client = QdrantClient(host='localhost', port=6333)
results = client.query_points(
    collection_name='somme_theologique',
    query=query_vectorized,
    limit=3,
    score_threshold=0.4
)


# Print results
for i, point in enumerate(results.points):
    print(f'\n--- Résultat {i + 1} ---')
    print(f'{point.id=}')
    print(f'{point.score=}')
    print(point.payload['text'])
    print('\n')

