

from typing import Any


def cache_dump_default(obj: Any):
    if isinstance(obj, set):
        return list(obj)
    # raise TypeError