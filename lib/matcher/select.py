from types import ModuleType

from . import naive, preemptive

MATCHERS = dict(naive=naive, preemptive=preemptive)


def get_matcher(name: str) -> ModuleType:
    module = MATCHERS.get(name)
    if not module:
        raise ValueError(f"Matcher name must be in {MATCHERS.keys()}")
    return module
