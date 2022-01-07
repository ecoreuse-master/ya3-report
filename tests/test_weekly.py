# Copyright (c) 2022 Shuhei Nitta. All rights reserved.
from unittest import TestCase
from datetime import datetime
import functools
import itertools

import pandas as pd

from ya3_report import weekly


INDEX = list(range(3))


@functools.lru_cache()
def get_test_data() -> pd.DataFrame:
    dfs: list[pd.DataFrame] = []
    for day, hour, n in itertools.product(range(1, 8), range(24), range(3)):
        dfs.append(pd.DataFrame({
            "aID": [f"{idx}".zfill(8) for idx in INDEX],
            "title": [f"title{idx}" for idx in INDEX],
            "datetime": [datetime(2022, 1, day, hour, 20*n).isoformat(timespec="seconds") for _ in INDEX],
            "access": [day+hour+idx for idx in INDEX],
            "watch": [day+hour+idx for idx in INDEX],
            "bid": [day+hour+idx for idx in INDEX],
        }))
    return pd.concat(dfs)


class Test_index_datehour(TestCase):
    def setUp(self) -> None:
        self.df = get_test_data()

    def test_index(self) -> None:
        df = weekly.index_datehour(self.df)
        expects = {
            datetime(2022, 1, day, hour).isoformat(timespec="minutes")
            for day, hour in itertools.product(range(1, 8), range(24))
        }
        self.assertSetEqual(set(df.index), expects)

    def test_date(self) -> None:
        df = weekly.index_datehour(self.df)
        expects = [
            datetime(2022, 1, day, hour).date().isoformat()
            for day, hour in itertools.product(range(1, 8), range(24))
        ]
        for datehour, actual, expect in zip(df.index, df["date"], expects):
            with self.subTest(datehour=datehour):
                self.assertEqual(actual, expect)

    def test_hour(self) -> None:
        df = weekly.index_datehour(self.df)
        expects = [hour for _, hour in itertools.product(range(7), range(24))]
        for datehour, actual, expect in zip(df.index, df["hour"], expects):
            with self.subTest(datehour=datehour):
                self.assertEqual(actual, expect)

    def test_day(self) -> None:
        df = weekly.index_datehour(self.df)
        expects = [day for day, _ in itertools.product(["Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu"], range(24))]
        for datehour, actual, expect in zip(df.index, df["day"], expects):
            with self.subTest(datehour=datehour):
                self.assertEqual(actual, expect)

    def test_access(self) -> None:
        df = weekly.index_datehour(self.df)
        len_index = len(INDEX)
        expects = [len_index if hour != 0 else 0 for _, hour in itertools.product(range(7), range(24))]
        for datehour, actual, expect in zip(df.index, df["access"], expects):
            with self.subTest(datehour=datehour):
                self.assertEqual(actual, expect)

    def test_watch(self) -> None:
        df = weekly.index_datehour(self.df)
        len_index = len(INDEX)
        expects = [len_index if hour != 0 else 0 for _, hour in itertools.product(range(7), range(24))]
        for datehour, actual, expect in zip(df.index, df["watch"], expects):
            with self.subTest(datehour=datehour):
                self.assertEqual(actual, expect)

    def test_bid(self) -> None:
        df = weekly.index_datehour(self.df)
        len_index = len(INDEX)
        expects = [len_index if hour != 0 else 0 for _, hour in itertools.product(range(7), range(24))]
        for datehour, actual, expect in zip(df.index, df["bid"], expects):
            with self.subTest(datehour=datehour):
                self.assertEqual(actual, expect)
