# Copyright 2022 Shuhei Nitta. All rights reserved.
from pathlib import Path
from datetime import date, datetime
from typing import Optional, Callable, Any

import pandas as pd
import numpy as np
import numpy.typing as npt

from ya3_report import environ


def get_data(dt: Optional[date] = None) -> pd.DataFrame:  # pragma: no cover
    _dt: date = dt if dt else date.today()
    filepath: Path = (environ.DATA_DIR / _dt.isoformat()).with_suffix(environ.DATAFILE_SUFFIX)
    return pd.read_csv(filepath)


def index_hour(df: pd.DataFrame) -> pd.DataFrame:
    _df = pd.DataFrame(
        {
            "hour": list(range(0, 24)),
            "access": 0,
            "watch": 0,
            "bid": 0,
        }
    )
    count_labels = ["access", "watch", "bid"]
    for _, group in df.groupby("aID"):
        group.sort_values("datetime")
        group["hour"] = group["datetime"].map(lambda x: datetime.fromisoformat(x).hour)
        threshold_0: Callable[[Any], npt.NDArray[Any]] = lambda x: np.where(x < 0, 0, x)
        for label in count_labels:
            group[label + "_diff"] = threshold_0(group[label].diff())
        for hour, _group in group.groupby("hour"):
            for label in count_labels:
                _df.at[hour, label] += _group[label + "_diff"].sum()
    return _df.set_index("hour")


def index_aID(df: pd.DataFrame) -> pd.DataFrame:
    aIDs: list[str] = []
    titles: list[str] = []
    access: list[int] = []
    watch: list[int] = []
    bid: list[int] = []
    for aID, group in df.groupby("aID"):
        aIDs.append(aID)
        titles.append(list(group["title"])[-1])
        access.append(int(group["access"].max() - group["access"].min()))
        watch.append(int(group["watch"].max() - group["watch"].min()))
        bid.append(int(group["bid"].max() - group["bid"].min()))
    return pd.DataFrame({"aID": aIDs, "title": titles, "access": access, "watch": watch, "bid": bid}).set_index("aID")
