from faker import Faker

from ..skills import fake_skillset, split_skills_list


job_columns = ["id", "title", "required_skills"]


def init_job(_: dict) -> dict:
    """
    Preprocess CSV strings.
    """
    return dict(
        id=int(_["id"]),
        title=_["title"],
        required_skills=split_skills_list(_["required_skills"]),
    )


def fake_job(id: int) -> dict:
    """
    Create a fake job seeker for generated CSV (or other purposes)
    """
    fake = Faker()
    return dict(
        id=int(id),
        title=fake.job(),
        required_skills=fake_skillset(),
    )
