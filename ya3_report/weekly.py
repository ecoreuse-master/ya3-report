# Copyright (c) 2022 Shuhei Nitta. All rights reserved.
from datetime import date, datetime, timedelta
from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt

from ya3_report import daily


def get_data(dt: Optional[date] = None) -> pd.DataFrame:  # pragma: no cover
    _dt = dt if dt else date.today()
    dfs: list[pd.DataFrame] = []
    for i in range(7):
        try:
            dfs.append(daily.get_data(_dt - timedelta(days=i)))
        except FileNotFoundError:
            continue
    return pd.concat(dfs)


def index_datehour(df: pd.DataFrame) -> pd.DataFrame:
    df_copy = df.copy()
    df_copy["date"] = df["datetime"].apply(lambda x: datetime.fromisoformat(x).date())
    dfs = []
    for dt, group in df_copy.groupby("date"):
        assert isinstance(dt, date)
        _df = daily.index_hour(group).reset_index()
        _df["date"] = dt.isoformat()
        _df["day"] = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][dt.weekday()]
        _df["date-hour"] = _df["hour"].apply(
            lambda hour: datetime(dt.year, dt.month, dt.day, hour).isoformat(timespec="minutes")
        )
        dfs.append(_df)
    return pd.concat(dfs).set_index("date-hour")


def plot_count_by_day(df_datehour: pd.DataFrame, label: str) -> plt.Axes:  # pragma: no cover
    _, axes = plt.subplots()
    for dt, group in df_datehour.groupby("date"):
        group.plot(
            x="hour",
            y=label,
            xlim=(0, 23),
            ax=axes,
            label=f"{dt} ({group['day'][0]})",
            title=f"{label} count in a week",
        )
    return axes
