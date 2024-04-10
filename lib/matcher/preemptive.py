from functools import lru_cache
from itertools import product
from typing import Generator


def get_sorted_matches(jobs: Generator, job_seekers: Generator) -> Generator:
    """
    For each seeker that has more than one job match:

    Yield a sextuple that contains:
        - jobseeker_id : int
        - jobseeker_name : str
        - job_id : int
        - job_title : str
        - matching_skill_count : int
        - matching_skill_percent : int

    Use tuples for efficiency.

    Preemptive strategy:

        - Index each skillset to a list of job and job seeker IDs
            - frozensets work as dictionary hashes (see lib/skills.py)
        - Index job IDs to titles and job seeker IDs to names
        - Create tuples of skills, intersections, counts and percentages
            - Sort tuples by percentages DESC and counts DESC
        - For each set of tuples:
          - Iterate jobs IDs ASC and job_seeker IDs ASC for each skillset
          - Yield a match data sextuple for each combination

    This generates in the correct order and does not require subsequent
    sorting.
    """
    job_titles = dict()
    job_seeker_names = dict()
    job_skills = dict()
    job_seeker_skills = dict()

    for job in jobs:
        job_titles[job["id"]] = job["title"]
        if job["required_skills"] in job_skills:
            job_skills[job["required_skills"]].append(job["id"])
        else:
            job_skills[job["required_skills"]] = [job["id"]]

    for job_seeker in job_seekers:
        job_seeker_names[job_seeker["id"]] = job_seeker["name"]
        if job_seeker["skills"] in job_seeker_skills:
            job_seeker_skills[job_seeker["skills"]].append(job_seeker["id"])
        else:
            job_seeker_skills[job_seeker["skills"]] = [job_seeker["id"]]

    # Generate skillsets for all intersections, with counts and percentages
    job_skillsets = list(job_skills.keys())
    job_seeker_skillsets = list(job_seeker_skills.keys())
    skillsets = [
        tuple(
            [
                job_skillset,
                job_seeker_skillset,
                calc_count(job_skillset, job_seeker_skillset),
                calc_percentage(job_skillset, job_seeker_skillset),
            ]
        )
        for job_skillset, job_seeker_skillset in product(
            job_skillsets, job_seeker_skillsets
        )
        if len(job_skillset.intersection(job_seeker_skillset)) > 0
        # and calc_percentage(job_skillset, job_seeker_skillset) > 50
    ]

    def sort_skillsets(_: tuple) -> tuple:
        """
        Sort skillsets by descending matching_skill_percent (last column), then
        matching_skill_count (second last column).
        """
        return (0 - _[-1], 0 - _[-2])

    sorted_skillsets = sorted(skillsets, key=sort_skillsets)

    # Get all jobs and jobseekers for each skillset, yield tuples in order
    # This takes most of the time.
    for (
        job_skillset,
        job_seeker_skillset,
        matching_skill_count,
        matching_skill_percent,
    ) in sorted_skillsets:
        for job_id, job_seeker_id in product(
            job_skills[job_skillset], job_seeker_skills[job_seeker_skillset]
        ):
            yield tuple(
                [
                    job_seeker_id,
                    job_seeker_names[job_seeker_id],
                    job_id,
                    job_titles[job_id],
                    matching_skill_count,
                    matching_skill_percent,
                ]
            )


def calc_count(_set: frozenset, _subset: frozenset) -> int:
    return len(_set.intersection(_subset))


def calc_percentage(_set: frozenset, _subset: frozenset) -> int:
    return round(calc_count(_set, _subset) / len(_set) * 100)
