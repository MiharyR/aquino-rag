import os

import click
from dotenv import load_dotenv

from src.ask_question.rag_answerer_name_to_class import RAG_ANSWERER_NAME_TO_CLASS


@click.command(help='Ask question to RAG')
@click.option(
    '--rag-answerer-name',
    '-r',
    default='base',
    required=False,
    help='The rag answerer to use (default: base)',
)
@click.option(
    '--question',
    '-q',
    required=True,
    help='Question to ask to the RAG',
)
@click.option(
    '--collection-name',
    '-c',
    required=True,
    help='The name where the data should be retrieved from',
)
@click.option(
    '--limit',
    '-n',
    default=3,
    required=False,
    help='Max number of results to return (default: 3)',
)
@click.option(
    '--score-threshold',
    '-s',
    default=0.5,
    required=False,
    help='Score threshold for filtering results',
)
def run(rag_answerer_name: str, question: str, collection_name: str, limit: int, score_threshold: float):
    """Ask a question to the RAG system and retrieve answers from the specified collection"""

    # Load environment variables from .env file
    load_dotenv()
    host = os.getenv('QDRANT_HOST', 'localhost')
    port = os.getenv('QDRANT_PORT', 6333)

    # Get the rag initializer class
    if rag_answerer_name in RAG_ANSWERER_NAME_TO_CLASS:
        rag_answerer_class = RAG_ANSWERER_NAME_TO_CLASS[rag_answerer_name]
    else:
        raise ValueError(
            f'Invalid rag_answerer_name: {rag_answerer_name}.'
            f'Available options are: {", ".join(RAG_ANSWERER_NAME_TO_CLASS.keys())}'
        )

    # Instanciate the RagAnswerer
    rag_answerer = rag_answerer_class(
        question=question,
        collection_name=collection_name,
        host=host,
        port=port,
        limit=limit,
        score_threshold=score_threshold,
    )

    # Run the rag answerer
    rag_answerer.run()


if __name__ == '__main__':
    run()
