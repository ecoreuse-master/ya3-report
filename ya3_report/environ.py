# Copyright 2022 Shuhei Nitta. All rights reserved.
import os
from pathlib import Path


DATA_DIR = Path(os.environ.get("YA3_REPORT_DATA_DIR", "data"))
DATAFILE_SUFFIX = os.environ.get("YA3_REPORT_DATAFILE_SUFFIX", ".csv.gz")
