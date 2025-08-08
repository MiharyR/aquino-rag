from abc import ABC
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import VectorParams, Distance, PointStruct

from src.utils.timer_decorator import decorate_all_methods


@decorate_all_methods()
class RagInitializer(ABC):
    """
    Abstract class for initializing a Retrieval-Augmented Generation (RAG) system.
    This class uses Qdrant vector database.
    """

    def __init__(self, *args, **kwargs):
        self.file_path = kwargs.get('file_path')
        self.host = kwargs.get('host')
        self.port = kwargs.get('port', 6333)
        self.collection_name = kwargs.get('collection_name', 'collection')
        self.overwrite_collection = kwargs.get('overwrite_collection', False)
        self.embedding_model_name = kwargs.get('embedding_model_name')
        self.client = QdrantClient(host=self.host, port=self.port)

    def run(self):
        """Main method to run the RAG initialization process."""
        text = self.extract_text_from_file()
        text = self.clean_text(text)
        chunks = self.split_text_into_chunks(text)
        vectors = self.transform_chunks_into_vectors(chunks)
        self.upload_data(
            vectors=vectors,
            chunks=chunks,
            collection_name=self.collection_name,
            overwrite_collection=self.overwrite_collection
        )

    def extract_text_from_file(self) -> str:
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

    def transform_chunks_into_vectors(self, chunks: list) -> list:
        encoder = SentenceTransformer(self.embedding_model_name)
        return encoder.encode(chunks).tolist()

    def upload_data(
        self,
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

        if self.client.collection_exists(collection_name):
            if not overwrite_collection:
                return
            # Delete the collection if it exists
            self.client.delete_collection(collection_name)

        # Create collecion
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )

        # Upload vector and chunks to Qdrant
        self.client.upload_points(
            collection_name=collection_name,
            points=[PointStruct(id=i, vector=vec, payload={'text': chunks[i]}) for i, vec in enumerate(vectors)],
        )
