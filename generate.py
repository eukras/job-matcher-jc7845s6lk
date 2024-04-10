"""
Print matches for CSV files in dataset directory using specified matcher
"""

from os import write
import click
import csv

from lib.data.jobs import fake_job, job_columns, write_job
from lib.data.job_seekers import fake_job_seeker, job_seeker_columns, write_job_seeker


JOBS_CSV_PATH = "datasets/generated/jobs.csv"
JOB_SEEKERS_CSV_PATH = "datasets/generated/job_seekers.csv"


@click.command()
@click.option("--num_jobs", type=click.INT, default=1000, show_default="1000")
@click.option("--num_job_seekers", type=click.INT, default=1000, show_default="1000")
def command(num_jobs=1000, num_job_seekers=1000):

    with open(JOBS_CSV_PATH, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=job_columns)
        writer.writeheader()
        for i in range(num_jobs):
            writer.writerow(write_job(fake_job(id=i + 1)))

    print(f"Wrote {num_jobs} jobs to {JOBS_CSV_PATH}")

    with open(JOB_SEEKERS_CSV_PATH, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=job_seeker_columns)
        writer.writeheader()
        for i in range(num_job_seekers):
            writer.writerow(write_job_seeker(fake_job_seeker(id=i + 1)))

    print(f"Wrote {num_job_seekers} job seekers to {JOB_SEEKERS_CSV_PATH}")


if __name__ == "__main__":
    command()
