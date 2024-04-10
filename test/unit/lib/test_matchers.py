"""
Use fixture generators to simulate CSV file data.
"""

from itertools import pairwise
from typing import Generator

from lib.matcher.select import MATCHERS, get_matcher


def get_jobs() -> Generator:
    yield from [
        dict(id=1, title="Intern", required_skills=frozenset(["A"])),
        dict(id=2, title="Junior Role", required_skills=frozenset(["B", "C"])),
        dict(
            id=3,
            title="Senior Role",
            required_skills=frozenset(["B", "C", "D", "E", "F"]),
        ),
    ]


def get_job_seekers() -> Generator:
    yield from [
        dict(id=4, name="Unskilled", skills=frozenset([])),
        dict(id=5, name="Beginner", skills=frozenset(["A", "D"])),
        dict(
            id=6, name="Professional", skills=frozenset(["A", "B", "C", "D", "E", "F"])
        ),
    ]


def test_get_jobs():
    jobs = get_jobs()
    row = next(jobs)
    assert row == dict(id=1, title="Intern", required_skills=frozenset(["A"]))


def test_get_job_seekers():
    job_seekers = get_job_seekers()
    row = next(job_seekers)
    assert row == dict(id=4, name="Unskilled", skills=frozenset([]))


def test_get_sorted_matches():
    """
    Test that all matchers produce the same results
    """
    for matcher in MATCHERS:
        strategy = get_matcher(matcher)
        matches = strategy.get_sorted_matches(get_jobs(), get_job_seekers())
        assert list(matches) == [
            (6, "Professional", 3, "Senior Role", 5, 100),
            (6, "Professional", 2, "Junior Role", 2, 100),
            (5, "Beginner", 1, "Intern", 1, 100),
            (6, "Professional", 1, "Intern", 1, 100),
            (5, "Beginner", 3, "Senior Role", 1, 20),
        ]


def test_sort_order():
    """
    Test that all matchers give the sort order:
       - [-1] DESC
       - [-2] DESC
       - [2] ASC
       - [0] ASC
    """
    for matcher in MATCHERS:
        strategy = get_matcher(matcher)
        matches = strategy.get_sorted_matches(get_jobs(), get_job_seekers())
        for a, b in pairwise(matches):
            assert a[-1] >= b[-1]
            if a[-1] == b[-1]:
                assert a[-2] >= b[-2]
                if a[-2] == b[-2]:
                    assert a[2] <= b[2]
                    if a[2] == b[2]:
                        assert a[0] <= b[0]
