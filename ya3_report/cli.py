# Copyright 2022 Shuhei Nitta. All rights reserved.
import os
import subprocess
from pathlib import Path

import click
import papermill


CONVERT_CHOICE = [
    "asciidoc",
    "custom",
    "html",
    "latex",
    "markdown",
    "notebook",
    "pdf",
    "python",
    "rst",
    "script",
    "slides",
    "webpdf",
]


@click.group()
def main() -> None:
    pass


@main.group()
@click.option(
    "-d",
    "--data-dir",
    type=click.types.Path(exists=True, file_okay=False),
    default="data",
    help="data directory",
    show_default=True,
)
@click.option("--datafile-suffix", type=str, default=".csv.gz", help="suffix of data files", show_default=True)
def report(
    data_dir: str,
    datafile_suffix: str,
) -> None:
    os.environ["YA3_REPORT_DATA_DIR"] = data_dir
    os.environ["YA3_REPORT_DATAFILE_SUFFIX"] = datafile_suffix


def create_report(report_path: Path, output: Path, tos: tuple[str, ...]) -> None:
    papermill.execute_notebook(report_path.as_posix(), output, progress_bar=False)
    for to in tos:
        subprocess.run(
            ["jupyter", "nbconvert", output, "--to", to],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )


@report.command()
@click.option(
    "-o",
    "--output",
    type=click.types.Path(),
    default="daily_report.ipynb",
    help="output path",
    show_default=True,
)
@click.option(
    "--to",
    type=click.Choice(CONVERT_CHOICE),
    default=[],
    multiple=True,
    help="convert type",
)
def daily(output: str, to: tuple[str, ...]) -> None:
    report_path = Path(__file__).parent / "notebooks" / "daily_report.ipynb"
    create_report(report_path, Path(output), to)


@report.command()
@click.option(
    "-o",
    "--output",
    type=click.types.Path(),
    default="weekly_report.ipynb",
    help="output path",
    show_default=True,
)
@click.option(
    "--to",
    type=click.Choice(CONVERT_CHOICE),
    default=[],
    multiple=True,
    help="convert type",
)
def weekly(output: str, to: tuple[str, ...]) -> None:
    report_path = Path(__file__).parent / "notebooks" / "weekly_report.ipynb"
    create_report(report_path, Path(output), to)
