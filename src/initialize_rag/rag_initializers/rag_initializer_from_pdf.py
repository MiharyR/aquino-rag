from src.initialize_rag.rag_initializers.rag_initializer import RagInitializer
import pymupdf
import re

from src.utils.timer_decorator import decorate_all_methods


@decorate_all_methods()
class RagInitializerFromPdf(RagInitializer):
    """
    Class for initializing a RAG from a PDF file.
    """

    def extract_text_from_file(self) -> str:
        with pymupdf.open(self.file_path) as doc:
            text = '\n'.join(page.get_text() for page in doc)
        return text

    def clean_text(self, text: str) -> str:
        text = text.replace('\n', ' ').replace('\xa0', ' ')

        # supprimer les longues séries de underscores
        text = re.sub(r'[_]{3,}', '', text)

        # compacter les espaces
        text = re.sub(r'\s{2,}', ' ', text)

        return text
