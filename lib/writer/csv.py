"""
Write tabular data in a pretty, human-readable format.

NOTE: This can take up most of the processing time on large result sets;
counting and tabulation cannot take full advantage of generators.
"""

import csv
import sys

from typing import Generator


def write(table: Generator, file_columns: list):
    """
    Print CSV rows to STDOUT
    """
    writer = csv.writer(sys.stdout)
    writer.writerow(file_columns)
    for row in table:
        writer.writerow(row)
