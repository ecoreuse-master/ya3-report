# Copyright 2022 Shuhei Nitta. All rights reserved.
import os
import subprocess
from pathlib import Path

import click


CONVERT_CHOICE = [
    "",
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


def create_report(report_path: Path, output: Path, to: str) -> None:
    subprocess.run(
        ["papermill", report_path.as_posix(), output],
        env=os.environ,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if to:
        subprocess.run(
            ["jupyter", "nbconvert", output, "--to", to],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
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
@click.option("--to", type=click.Choice(CONVERT_CHOICE), default="", help="convert type", show_default=True)
def daily(output: str, to: str) -> None:
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
@click.option("--to", type=click.Choice(CONVERT_CHOICE), default="", help="convert type", show_default=True)
def weekly(output: str, to: str) -> None:
    report_path = Path(__file__).parent / "notebooks" / "weekly_report.ipynb"
    create_report(report_path, Path(output), to)
