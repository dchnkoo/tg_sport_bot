

def get_human_readable_size_mb(size: int) -> int:
    kb = size / 1024

    return int(kb / 1024)
