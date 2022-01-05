# Copyright (c) Shuhei Nitta. All rights reserved.
from unittest import TestCase
from datetime import datetime

import pandas as pd

from ya3_report import weekly


class Test_index_datehour(TestCase):
    def setUp(self) -> None:
        self.df = pd.read_csv("tests/test_data.csv")

    def test_index(self) -> None:
        df = weekly.index_datehour(self.df)
        expects = {datetime(2022, 1, 1, i).isoformat(timespec="minutes") for i in range(24)}
        self.assertSetEqual(set(df.index), expects)

    def test_date(self) -> None:
        df = weekly.index_datehour(self.df)
        expects = [datetime(2022, 1, 1).date().isoformat() for _ in range(24)]
        for datehour, actual, expect in zip(df.index, df["date"], expects):
            with self.subTest(datehour=datehour):
                self.assertEqual(actual, expect)

    def test_hour(self) -> None:
        df = weekly.index_datehour(self.df)
        expects = list(range(24))
        for datehour, actual, expect in zip(df.index, df["hour"], expects):
            with self.subTest(datehour=datehour):
                self.assertEqual(actual, expect)

    def test_day(self) -> None:
        df = weekly.index_datehour(self.df)
        expects = ["Fri" for _ in range(24)]
        for datehour, actual, expect in zip(df.index, df["day"], expects):
            with self.subTest(datehour=datehour):
                self.assertEqual(actual, expect)

    def test_access(self) -> None:
        df = weekly.index_datehour(self.df)
        expects = [20] + [0 for _ in range(23)]
        for datehour, actual, expect in zip(df.index, df["access"], expects):
            with self.subTest(datehour=datehour):
                self.assertEqual(actual, expect)

    def test_watch(self) -> None:
        df = weekly.index_datehour(self.df)
        expects = [20] + [0 for _ in range(23)]
        for datehour, actual, expect in zip(df.index, df["watch"], expects):
            with self.subTest(datehour=datehour):
                self.assertEqual(actual, expect)

    def test_bid(self) -> None:
        df = weekly.index_datehour(self.df)
        expects = [20] + [0 for _ in range(23)]
        for datehour, actual, expect in zip(df.index, df["bid"], expects):
            with self.subTest(datehour=datehour):
                self.assertEqual(actual, expect)
