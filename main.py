import pymupdf
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings


path = 'somme.pdf'


# Extract pdf
doc = pymupdf.open(path)
text = "\n".join(page.get_text() for page in doc)
doc.close()

# Chunk text
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_text(text)

# print nb chunks
print(chunks[0])
print('-'*10)
print(chunks[1])

# Transform chunks into vectors
# embedding_model = OpenAIEmbeddings()
# vectors = embedding_model.embed_documents(chunks)


