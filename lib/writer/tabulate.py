"""
Write tabular data in a pretty, human-readable format.

NOTE: This can take up most of the processing time on large result sets;
counting and tabulation cannot take full advantage of generators. Use 'csv'
instead (the default) in this case.
"""

from tabulate import tabulate
from typing import Generator


def write(table: Generator, file_columns: list):
    """
    Print a generated dataset.
    """

    count = len(new_table := list(table))

    print(tabulate(new_table, headers=file_columns))
    print()
    print(f"({count} rows)")
