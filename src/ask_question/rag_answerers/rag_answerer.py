from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from src.utils.constants import MODEL_FOR_EMBEDDING
from src.utils.timer_decorator import decorate_all_methods


@decorate_all_methods
class RagAnswerer:

    def __init__(self, *args, **kwargs):
        self.question = kwargs.get('question')
        self.host = kwargs.get('host')
        self.port = kwargs.get('port', 6333)
        self.collection_name = kwargs.get('collection_name', 'collection')
        self.limit = kwargs.get('limit', 3)
        self.score_threshold = kwargs.get('score_threshold', 0.5)
        self.client = QdrantClient(host=self.host, port=self.port)
        self.model_name = MODEL_FOR_EMBEDDING


    def run(self):
        vectorized_question = self.vectorize_question()
        results = self.query_quadrant(vectorized_question)
        self.handle_results(results)

    def vectorize_question(self):
        encoder = SentenceTransformer(self.model_name)
        return encoder.encode(self.question).tolist()

    def query_quadrant(self, vectorized_question: list):
        return self.client.query_points(
            collection_name=self.collection_name,
            query=vectorized_question,
            limit=self.limit,
            score_threshold=self.score_threshold,
        )

    def handle_results(self, results):
        for i, point in enumerate(results.points):
            print(f'\n--- Résultat {i + 1} ---')
            print(f'{point.id=}')
            print(f'{point.score=}')
            print(point.payload['text'])
            print('\n')
