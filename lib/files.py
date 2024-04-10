""""
Supply an efficient generator for CSV files.

A 2018 benchmark suggest DictReader is fastest, mostly because it only returns
strings. Working with dicts is friendlier than tuples, and not slower.

https://medium.com/casual-inference/the-most-time-efficient-ways-to-import-csv-data-in-python-cc159b44063d
"""

import csv
from typing import Callable, Generator

from lib.data.jobs import read_job, job_columns
from lib.data.job_seekers import read_job_seeker, job_seeker_columns


def read_csv(
    file_path: str, file_columns: list, init_row: Callable, ignore_header: bool = True
) -> Generator[dict, None, None]:
    """
    Generate a list of strings for each row.
    """
    with open(file_path) as file_pointer:
        reader = csv.DictReader(file_pointer, fieldnames=file_columns)
        if ignore_header:
            _ = next(reader)  # discard first row
        for row in reader:
            yield init_row(row)


def match_files(
    match_skills: Callable, job_file_path: str, job_seekers_file_path: str
) -> Generator:
    """
    Generate matches from jobs and job_seekers CSV files, given file paths.
    """

    jobs = read_csv(
        file_path=job_file_path,
        file_columns=job_columns,
        init_row=read_job,
        ignore_header=True,
    )

    job_seekers = read_csv(
        file_path=job_seekers_file_path,
        file_columns=job_seeker_columns,
        init_row=read_job_seeker,
        ignore_header=True,
    )

    yield from match_skills(jobs, job_seekers)
