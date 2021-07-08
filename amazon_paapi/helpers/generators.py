"""Module with helper functions for making generators."""


from typing import Generator


def get_list_chunks(full_list: list[str], chunk_size: int) -> Generator[list[str], None, None]:
    """Yield successive chunks from list."""
    for i in range(0, len(full_list), chunk_size):
        yield full_list[i:i + chunk_size]
