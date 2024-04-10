from lib.skills import split_skills_list


def test_split_skills_list():
    assert split_skills_list("a, b") == set(["a", "b"])
    assert split_skills_list("a, b, b") == set(["a", "b"])  # Ignore duplicates
    assert split_skills_list("a, b, B") == set(["a", "b", "B"])  # Case sensitive
    assert split_skills_list("a,b") == set(["a,b"])
    assert split_skills_list("a b") == set(["a b"])
    assert split_skills_list("") == set([""])
