"""Module with helper functions for making generators."""


def get_list_chunks(full_list, chunk_size):
    """Yield successive chunks from list."""
    for i in range(0, len(full_list), chunk_size):
        yield full_list[i:i + chunk_size]
