import os

import click
from dotenv import load_dotenv

from src.ask_question.rag_answerer import RagAnswerer


@click.command(help='Ask question to RAG')
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
    help='Max number of results to return (default: 3)',
)
@click.option(
    '--score-threshold',
    '-s',
    default=0.5,
    help='Score threshold for filtering results',
)
def run(question: str, collection_name: str, limit: int, score_threshold: float):
    """Ask a question to the RAG system and retrieve answers from the specified collection"""

    # Load environment variables from .env file
    load_dotenv()
    host = os.getenv('QDRANT_HOST', 'localhost')
    port = os.getenv('QDRANT_PORT', 6333)

    # Instanciate the RagAnswerer
    rag_answerer = RagAnswerer(
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
