from itertools import product
from typing import Generator


def get_sorted_matches(jobs: Generator, job_seekers: Generator) -> Generator:
    """
    Apply sorting to matching skills data.
    """
    yield from sorted(get_matches(jobs, job_seekers), key=sort_by)


def get_matches(jobs: Generator, job_seekers: Generator) -> Generator:
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

    Naive strategy:

        - Iterate over all possible pairs of jobs and job seekers to check
          matching skills.
    """
    for job, job_seeker in product(jobs, job_seekers):
        required_skills = job["required_skills"]
        matches = job_seeker["skills"].intersection(required_skills)
        if len(matches) > 0 and len(required_skills) > 0:
            percent = len(matches) * 100 / len(required_skills)
            yield tuple(
                [
                    job_seeker["id"],
                    job_seeker["name"],
                    job["id"],
                    job["title"],
                    len(matches),
                    round(percent),
                ]
            )


def sort_by(match: tuple) -> tuple:
    """
    Sort results by:
    - the last column (matching_skill_percent), INT, DESCENDING
    - the second last column (matching_skill_count), INT, DESCENDING
    - the third column (job_id), INT, ASCENDING
    - the first column (job_seeker_id), INT, ASCENDING (added to requirements
      for consistent output)

    This is more tightly specified than requirements for easier comparison.
    """
    return (0 - match[-1], 0 - match[-2], match[2], match[0])
