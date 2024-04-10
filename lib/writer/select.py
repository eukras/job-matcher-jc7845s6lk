from types import ModuleType

from . import tabulate, csv

WRITERS = dict(csv=csv, tabulate=tabulate)


def get_writer(name: str) -> ModuleType:
    module = WRITERS.get(name)
    if not module:
        raise ValueError(f"Matcher name must be in {WRITERS.keys()}")
    return module
