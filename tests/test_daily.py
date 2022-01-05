# Copyright (c) 2022 Shuhei Nitta. All rights reserved.
from unittest import TestCase

import pandas as pd

from ya3_report import daily


class Test_index_hour(TestCase):
    def setUp(self) -> None:
        self.df = pd.read_csv("tests/test_data.csv")

    def test_index(self) -> None:
        df = daily.index_hour(self.df)
        for actual, expect in zip(df.index, list(range(24))):
            with self.subTest(hour=actual):
                self.assertEqual(actual, expect)

    def test_access(self) -> None:
        df = daily.index_hour(self.df)
        expects = [20] + [0 for _ in range(23)]
        for hour, actual, expect in zip(df.index, df["access"], expects):
            with self.subTest(hour=hour):
                self.assertEqual(actual, expect)

    def test_watch(self) -> None:
        df = daily.index_hour(self.df)
        expects = [20] + [0 for _ in range(23)]
        for hour, actual, expect in zip(df.index, df["watch"], expects):
            with self.subTest(hour=hour):
                self.assertEqual(actual, expect)

    def test_bid(self) -> None:
        df = daily.index_hour(self.df)
        expects = [20] + [0 for _ in range(23)]
        for hour, actual, expect in zip(df.index, df["bid"], expects):
            with self.subTest(hour=hour):
                self.assertEqual(actual, expect)


class Test_index_aID(TestCase):
    def setUp(self) -> None:
        self.df = pd.read_csv("tests/test_data.csv")

    def test_index(self) -> None:
        df = daily.index_aID(self.df)
        self.assertSetEqual(set(df.index), set(self.df["aID"]))

    def test_access(self) -> None:
        df = daily.index_aID(self.df)
        expects = [2 for _ in df.index]
        for aID, actual, expect in zip(df.index, df["access"], expects):
            with self.subTest(aID=aID):
                self.assertEqual(actual, expect)

    def test_watch(self) -> None:
        df = daily.index_aID(self.df)
        expects = [2 for _ in df.index]
        for aID, actual, expect in zip(df.index, df["watch"], expects):
            with self.subTest(aID=aID):
                self.assertEqual(actual, expect)

    def test_bid(self) -> None:
        df = daily.index_aID(self.df)
        expects = [2 for _ in df.index]
        for aID, actual, expect in zip(df.index, df["bid"], expects):
            with self.subTest(aID=aID):
                self.assertEqual(actual, expect)
