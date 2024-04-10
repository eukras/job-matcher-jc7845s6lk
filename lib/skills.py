"""
Skills processing functions.

Use sets to find intersections.
"""

import random
from typing import FrozenSet


SKILLS_COLUMNS = [
    "jobseeker_id",
    "jobseeker_name",
    "job_id",
    "job_title",
    "matching_skill_count",
    "matching_skill_percent",
]

FAKE_SKILLS = [f"Skill {i}" for i in range(1, 100)]


def split_skills_list(skills_list: str) -> FrozenSet[str]:
    """
    Turn a comma-space separated strings into a set.

    This must be a frozenset so it can be used for hashing.
    """
    return frozenset(skills_list.split(", "))


def fake_skillset(_min=1, _max=6) -> FrozenSet[str]:
    """
    Generate a set of random skills.
    """
    return frozenset(random.choices(FAKE_SKILLS, k=random.randint(_min, _max)))
