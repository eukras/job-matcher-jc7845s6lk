from faker import Faker

from ..skills import split_skills_list, fake_skillset


job_seeker_columns = ["id", "name", "skills"]


def init_job_seeker(_: dict) -> dict:
    """
    Preprocess CSV strings.
    """
    return dict(
        id=int(_["id"]),
        name=_["name"],
        skills=split_skills_list(_["skills"]),
    )


def fake_job_seeker(id: int) -> dict:
    """
    Create a fake job for generated CSV (or other purposes)
    """
    fake = Faker()
    return dict(
        id=int(id),
        name=fake.name(),
        skills=fake_skillset(),
    )
