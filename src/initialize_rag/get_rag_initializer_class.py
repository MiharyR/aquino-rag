from src.initialize_rag.rag_initializer_from_pdf import RagInitializerFromPdf
from src.initialize_rag.rag_initializer_from_txt import RagInitializerFromTxt


def get_rag_initializer_class(file_path: str):
    if file_path.endswith('.pdf'):
        return RagInitializerFromPdf
    elif file_path.endswith('.txt'):
        return RagInitializerFromTxt
    else:
        raise ValueError(f"Unsupported file type for RAG initialization: {file_path}")
