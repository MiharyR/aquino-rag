import click

from src.initialize_rag.rag_initializer_name_to_class import RAG_INITIALIZER_NAME_TO_CLASS
from src.utils.handle_env_vars import handle_env_vars


@click.command(help='Initialize RAG')
@click.option(
    '--rag-initializer-name',
    '-r',
    required=True,
    help='The rag initializer to use',
)
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
    '-o',
    is_flag=True,
    default=False,
    help='If true, the collection will be overwritten if it already exists',
)
def run(rag_initializer_name: str, file_path: str, collection_name: str, overwrite_collection: bool):
    """Initialize RAG with the given file path and collection name"""

    # Load environment variables from .env file
    env_vars = handle_env_vars()

    # Get the rag initializer class
    if rag_initializer_name in RAG_INITIALIZER_NAME_TO_CLASS:
        rag_initializer_class = RAG_INITIALIZER_NAME_TO_CLASS[rag_initializer_name]
    else:
        raise ValueError(
            f'Invalid rag_initializer_name: {rag_initializer_name}.'
            f'Available options are: {", ".join(RAG_INITIALIZER_NAME_TO_CLASS.keys())}'
        )

    # Instantiate the rag initializer
    rag_initializer = rag_initializer_class(
        file_path=file_path,
        host=env_vars['host'],
        port=env_vars['port'],
        collection_name=collection_name,
        overwrite_collection=overwrite_collection,
        embedding_model_name=env_vars['embedding_model_name'],
    )

    # Run the rag initializer
    rag_initializer.run()


if __name__ == '__main__':
    run()
