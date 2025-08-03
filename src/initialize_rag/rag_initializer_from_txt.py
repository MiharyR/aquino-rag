from src.initialize_rag.rag_initializer import RagInitializer
from src.utils.timer_decorator import decorate_all_methods


@decorate_all_methods
class RagInitializerFromTxt(RagInitializer):
    """
    Class for initializing a RAG from a txt file.
    """

    def extract_text_from_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
