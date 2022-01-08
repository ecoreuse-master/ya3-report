# Copyright 2022 Shuhei Nitta. All rights reserved.
from pathlib import Path
from datetime import date, datetime
from typing import Optional

import pandas as pd
import numpy as np

from ya3_report import environ


def get_data(dt: Optional[date] = None) -> pd.DataFrame:  # pragma: no cover
    _dt: date = dt if dt else date.today()
    filepath: Path = (environ.DATA_DIR / _dt.isoformat()).with_suffix(environ.DATAFILE_SUFFIX)
    return pd.read_csv(filepath)


def index_hour(df: pd.DataFrame) -> pd.DataFrame:
    return df. \
        groupby(["aID", "title"]). \
        apply(
            # indexing by hour
            lambda df: df. \
            set_index("datetime"). \
            sort_index(). \
            diff(). \
            apply(lambda x: np.where(x < 0, 0, x)). \
            groupby(lambda x: datetime.fromisoformat(x).hour). \
            sum()
        ). \
        groupby(lambda index: index[2]). \
        sum(). \
        assign(hour=lambda df: df.index). \
        set_index("hour")


def index_aID(df: pd.DataFrame) -> pd.DataFrame:
    return df. \
        groupby(["aID", "title"]). \
        apply(lambda df: index_hour(df).sum()). \
        reset_index("title")


if __name__ == "__main__":  # pragma: no cover
    from datetime import date
    df = get_data(date(2022, 1, 3))
    print(index_hour(df))
