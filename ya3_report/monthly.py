# Copyright (c) 2022 Shuhei Nitta. All rights reserved.
import calendar
from datetime import date
from typing import Optional

import pandas as pd

from ya3_report import daily


def get_data(dt: Optional[date] = None) -> pd.DataFrame:  # pragma: no cover
    _dt = dt if dt else date.today()
    dfs = [pd.DataFrame()]
    for _dt_ in calendar.Calendar().itermonthdates(_dt.year, _dt.month):
        try:
            dfs.append(daily.get_data(_dt_))
        except FileNotFoundError:
            continue
    return pd.concat(dfs)
