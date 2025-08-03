from abc import ABC
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import VectorParams, Distance, PointStruct

from src.utils.constants import MODEL_FOR_EMBEDDING
from src.utils.timer_decorator import decorate_all_methods


@decorate_all_methods
class RagInitializer(ABC):
    """
    Abstract class for initializing a Retrieval-Augmented Generation (RAG) system.
    This class uses Qdrant vector database.
    """

    def __init__(self, *args, **kwargs):
        self.file_path = kwargs.get('file_path')
        self.model_name = kwargs.get('model_name', 'all-MiniLM-L6-v2')
        self.host = kwargs.get('host')
        self.port = kwargs.get('port', 6333)
        self.collection_name = kwargs.get('collection_name', 'collection')
        self.overwrite_collection = kwargs.get('overwrite_collection', False)
        self.model_name = MODEL_FOR_EMBEDDING

    def run(self):
        """Main method to run the RAG initialization process."""
        text = self.extract_text_from_file(self.file_path)
        text = self.clean_text(text)
        chunks = self.split_text_into_chunks(text)
        vectors = self.transform_chunks_into_vectors(chunks, self.model_name)
        client = self.init_client(self.host, self.port)
        self.upload_data(
            client=client,
            vectors=vectors,
            chunks=chunks,
            collection_name=self.collection_name,
            overwrite_collection=self.overwrite_collection
        )

    def extract_text_from_file(self, file_path: str) -> str:
        raise NotImplementedError('This method should be implemented in a subclass')

    def clean_text(self, text: str) -> str:
        return text

    def split_text_into_chunks(self, text: str) -> list:
        max_length, overlap, start = 500, 50, 0
        chunks = []
        while start < len(text):
            end = start + max_length
            chunks.append(text[start:end])
            start += max_length - overlap
        return chunks

    def transform_chunks_into_vectors(self, chunks: list, model_name: str) -> list:
        encoder = SentenceTransformer(model_name)
        return encoder.encode(chunks).tolist()

    def init_client(self, host: str, port: int = 6333) -> QdrantClient:
        return QdrantClient(host=host, port=port)

    def upload_data(
        self,
        client: QdrantClient,
        vectors: list,
        chunks: list,
        collection_name: str,
        overwrite_collection: bool = False,
    ):
        """
        Uploads vectors and chunks to a Qdrant collection.
        - If the collection already exists:
            - if `overwrite_collection` is False : it does nothing
            - if `overwrite_collection` is True: it deletes the existing collection before creating a new one.
        """

        if client.collection_exists(collection_name):
            if not overwrite_collection:
                return
            # Delete the collection if it exists
            client.delete_collection(collection_name)

        # Create collecion
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )

        # Upload vector and chunks to Qdrant
        client.upload_points(
            collection_name=collection_name,
            points=[PointStruct(id=i, vector=vec, payload={'text': chunks[i]}) for i, vec in enumerate(vectors)],
        )
