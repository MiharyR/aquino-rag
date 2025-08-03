import os

import click
from dotenv import load_dotenv

from src.initialize_rag.get_rag_initializer_class import get_rag_initializer_class


@click.command(help='Initialize RAG')
@click.option(
    '--file-path',
    '-f',
    required=True,
    help='File path for the rag',
)
@click.option(
    '--collection-name',
    '-c',
    required=True,
    help='The name where the data will be stored',
)
@click.option(
    '--overwrite-collection',
    is_flag=True,
    default=False,
    required=False,
    help='Overwrite the collection if it already exists',
)
def run(file_path: str, collection_name: str, overwrite_collection: bool):
    """Initialize RAG with the given file path and collection name"""

    # Load environment variables from .env file
    load_dotenv()
    host = os.getenv('QDRANT_HOST', 'localhost')
    port = os.getenv('QDRANT_PORT', 6333)

    # Get the rag initializer class based on the file type
    rag_initializer_class = get_rag_initializer_class(file_path)

    # Instantiate the rag initializer
    rag_initializer = rag_initializer_class(
        file_path=file_path,
        host=host,
        port=port,
        collection_name=collection_name,
        overwrite_collection=overwrite_collection,
    )

    # Run the rag initializer
    rag_initializer.run()


if __name__ == '__main__':
    run()
