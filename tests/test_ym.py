# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
from array import array
import unittest
import pandas as pd
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../ym')))
from ym import ym


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_definition(self):
        ym1 = ym(2001, 10)
        ym2 = ym(2002, 10)
        ym3 = ym("200210")
        ym4 = ym(200210)
        ym5 = ym(datetime(2002, 10, 1))
        assert ym1 != ym2
        assert ym2 == ym3
        assert ym2 == ym4
        assert ym2 == ym5
        with self.assertRaises(AssertionError):
            ym0 = ym(200213)
        with self.assertRaises(AssertionError):
            ym0 = ym(200200)
        with self.assertRaises(AssertionError):
            ym0 = ym(-12312)
        with self.assertRaises(AssertionError):
            ym0 = ym(2000012)
        with self.assertRaises(ValueError):
            ym0 = ym("2000012")
        with self.assertRaises(ValueError):
            ym0 = ym("79412")

        ym1 -= 10
        assert ym1 == "200012"
        ym1 -= 24
        assert ym1 == "199812"
        ym1 += 1
        assert ym1 == "199901"
        ym1 += 45
        assert ym1 == "200210"
        assert ym1 in [ym("200411"), ym2]
        assert ym("200411") - ym("200401") == 10
        assert ym("200210") - ym("199901") == 45
        with self.assertRaises(ValueError):
            ym("200411") + ym("200401")

    def test_with_pandas(self):
        ym1 = ym(2001, 10)
        ym2 = ym(2002, 3)
        ym_series = pd.Series([ym1, ym2])
        assert (ym_series == "200110").sum() == 1
        assert (ym_series + 3 == pd.Series([ym(2002, 1), ym(2002, 6)])).all()
        assert (ym_series.apply(lambda v: v.year)
                == pd.Series([2001, 2002])).all()
        assert ((ym_series == "200110") == pd.Series([True, False])).all()

    def test_convert(self):
        ym1 = ym(2001, 10)
        assert ym1.toint() == 200110
        assert isinstance(ym1.toint(), int)
        assert ym1.tostr() == "200110"
        assert isinstance(ym1.tostr(), str)
        assert ym1.todatetime(day=5) == datetime(2001, 10, 5)
        assert isinstance(ym1.todatetime(), datetime)
        assert int(ym1) == 200110
        assert str(ym1) == "200110"
        # 年が3桁の場合のテスト
        assert ym(794, 10).toint() == 79410
        assert ym(794, 10).tostr() == "079410"

    def test_hashable(self):
        key = ym(2001, 1)
        with self.assertRaises(AttributeError):
            key.month = 2
        with self.assertRaises(AttributeError):
            key.year = 2002

        dct = {key: 'hoge'}
        assert dct[key] == 'hoge'
        df = pd.DataFrame({
            "string": ['hoge', 'fuga', 'piyo'],
            "ym": [ym(200101), ym(200101), ym(200102)]
        })
        res = df.groupby("ym").size()
        assert (res.index == pd.Series([ym(200101), "200102"])).all()
        assert (res.values == array("I", [2, 1])).all()


if __name__ == '__main__':
    unittest.main()
