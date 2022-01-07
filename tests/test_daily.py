# Copyright (c) 2022 Shuhei Nitta. All rights reserved.
from unittest import TestCase
from datetime import datetime
import functools

import pandas as pd

from ya3_report import daily

INDEX = list(range(3))


@functools.lru_cache()
def get_test_data() -> pd.DataFrame:
    dfs: list[pd.DataFrame] = []
    for hour in range(24):
        for n in range(3):
            dfs.append(pd.DataFrame({
                "aID": [f"{idx}".zfill(8) for idx in INDEX],
                "title": [f"title{idx}" for idx in INDEX],
                "datetime": [datetime(2022, 1, 1, hour, 20*n).isoformat(timespec="seconds") for _ in INDEX],
                "access": [hour+idx for idx in INDEX],
                "watch": [hour+idx for idx in INDEX],
                "bid": [hour+idx for idx in INDEX],
            }))
    return pd.concat(dfs)


class Test_index_hour(TestCase):
    def setUp(self) -> None:
        self.df = get_test_data()

    def test_index(self) -> None:
        df = daily.index_hour(self.df)
        for actual, expect in zip(df.index, list(range(24))):
            with self.subTest(hour=actual):
                self.assertEqual(actual, expect)

    def test_access(self) -> None:
        df = daily.index_hour(self.df)
        len_index = len(INDEX)
        expects = [len_index if hour != 0 else 0 for hour in range(24)]
        for hour, actual, expect in zip(df.index, df["access"], expects):
            with self.subTest(hour=hour):
                self.assertEqual(actual, expect)

    def test_watch(self) -> None:
        df = daily.index_hour(self.df)
        len_index = len(INDEX)
        expects = [len_index if hour != 0 else 0 for hour in range(24)]
        for hour, actual, expect in zip(df.index, df["watch"], expects):
            with self.subTest(hour=hour):
                self.assertEqual(actual, expect)

    def test_bid(self) -> None:
        df = daily.index_hour(self.df)
        len_index = len(INDEX)
        expects = [len_index if hour != 0 else 0 for hour in range(24)]
        for hour, actual, expect in zip(df.index, df["bid"], expects):
            with self.subTest(hour=hour):
                self.assertEqual(actual, expect)


class Test_index_aID(TestCase):
    def setUp(self) -> None:
        self.df = get_test_data()

    def test_index(self) -> None:
        df = daily.index_aID(self.df)
        self.assertSetEqual(set(df.index), set(self.df["aID"]))

    def test_access(self) -> None:
        df = daily.index_aID(self.df)
        expects = [23 for _ in df.index]
        for aID, actual, expect in zip(df.index, df["access"], expects):
            with self.subTest(aID=aID):
                self.assertEqual(actual, expect)

    def test_watch(self) -> None:
        df = daily.index_aID(self.df)
        expects = [23 for _ in df.index]
        for aID, actual, expect in zip(df.index, df["watch"], expects):
            with self.subTest(aID=aID):
                self.assertEqual(actual, expect)

    def test_bid(self) -> None:
        df = daily.index_aID(self.df)
        expects = [23 for _ in df.index]
        for aID, actual, expect in zip(df.index, df["bid"], expects):
            with self.subTest(aID=aID):
                self.assertEqual(actual, expect)
