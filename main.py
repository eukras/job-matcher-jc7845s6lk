"""
Print matches for CSV files in dataset directory using specified matcher
"""

import click
import os

from tabulate import tabulate

from lib.files import match_files
from lib.matcher.select import MATCHERS, get_matcher
from lib.writer.select import WRITERS, get_writer
from lib.skills import SKILLS_COLUMNS


DATASETS = os.listdir("datasets")


@click.command()
@click.option(
    "--dataset",
    type=click.Choice(DATASETS),
    default="challenge",
    show_default="challenge",
)
@click.option(
    "--matcher",
    type=click.Choice(list(MATCHERS)),
    default="naive",
    show_default="naive",
)
@click.option(
    "--writer",
    type=click.Choice(list(WRITERS)),
    default="csv",
    show_default="csv",
)
def command(dataset="challenge", matcher="naive", writer="csv"):
    """
    Match jobs to job seekers in a specified dataset, using a specified
    matching strategy, and tabulate the results.
    """

    jobs_csv_path = f"datasets/{dataset}/jobs.csv"
    job_seekers_csv_path = f"datasets/{dataset}/job_seekers.csv"

    if writer != "csv":
        print()
        print("MATCHER :", matcher)
        print("WRITER  :", writer)
        print("DATASET :", jobs_csv_path)
        print("        :", job_seekers_csv_path)
        print()

    strategy = get_matcher(matcher)
    formatter = get_writer(writer)

    formatter.write(
        match_files(
            strategy.get_sorted_matches,
            os.path.abspath(jobs_csv_path),
            os.path.abspath(job_seekers_csv_path),
        ),
        SKILLS_COLUMNS,
    )


if __name__ == "__main__":
    command()
