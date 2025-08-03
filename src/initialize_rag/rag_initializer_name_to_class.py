from src.initialize_rag.rag_initializer_from_pdf import RagInitializerFromPdf
from src.initialize_rag.rag_initializer_from_txt import RagInitializerFromTxt


RAG_INITIALIZER_NAME_TO_CLASS = {
    'from_txt': RagInitializerFromTxt,
    'from_pdf': RagInitializerFromPdf,
}
