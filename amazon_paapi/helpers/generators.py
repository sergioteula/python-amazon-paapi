"""Module with helper functions for making generators."""


from typing import Generator, List


def get_list_chunks(full_list: List[str], chunk_size: int) -> Generator[List[str], None, None]:
    """Yield successive chunks from List."""
    for i in range(0, len(full_list), chunk_size):
        yield full_list[i:i + chunk_size]
