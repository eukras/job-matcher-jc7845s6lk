from lib.files import read_csv

JOBS_FILE_PATH = "datasets/challenge/jobs.csv"
JOBS_COLUMNS = ["id", "title", "required_skills"]


def test_without_headers():
    """
    Confirm shape of file read in. Initial rows will be

    id,title,required_skills
    1,Ruby Developer,"Ruby, SQL, Problem Solving"
    2,Frontend Developer,"JavaScript, HTML/CSS, React, Teamwork"
    3,Backend Developer,"Java, SQL, Node.js, Problem Solving"
    4,Fullstack Developer,"JavaScript, HTML/CSS, Node.js, Ruby, SQL, Communication"
    5,Machine Learning Engineer,"Python, Machine Learning, Adaptability"
    6,Cloud Architect,"Cloud Computing, Python, Communication"
    7,Data Analyst,"Python, SQL, Machine Learning, Adaptability"
    8,Web Developer,"HTML/CSS, JavaScript, Ruby, Teamwork"
    9,Python Developer,"Python, SQL, Problem Solving, Self Motivated"
    """

    def init_jobs_row(row):
        return row

    table = read_csv(
        file_path=JOBS_FILE_PATH,
        file_columns=JOBS_COLUMNS,
        init_row=init_jobs_row,
        ignore_header=True,
    )

    row = next(table)
    assert row == dict(
        id="1", title="Ruby Developer", required_skills="Ruby, SQL, Problem Solving"
    )

    for row in table:
        assert len(row) == 3
        assert int(row["id"]) > 0
        assert len(row["title"]) > 0
        assert len(row["required_skills"]) > 0
