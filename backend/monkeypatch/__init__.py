import contextlib

import rtfparse.entities

from .rtfparser_patch import Control_Word


@contextlib.contextmanager
def with_monkey_patched_rtfparser():
    original = rtfparse.entities.Control_Word

    try:
        rtfparse.entities.Control_Word = Control_Word
        yield
    finally:
        rtfparse.entities.Control_Word = original
