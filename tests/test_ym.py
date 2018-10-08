# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
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
            ym1.month = 13
        with self.assertRaises(AssertionError):
            ym1.month = 0
        with self.assertRaises(AssertionError):
            ym1.year = -1
        with self.assertRaises(AssertionError):
            ym1.year = 10000

        ym1.month = 1
        assert ym1 == "200101"
        ym1.year = 2003
        assert ym1 == 200301
        ym1 += 22
        assert ym1 == "200411"
        assert ym1 in [ym("200411"), ym2]

    def test_with_pandas(self):
        ym1 = ym(2001, 10)
        ym2 = ym(2002, 3)
        ym_series = pd.Series([ym1, ym2])
        assert (ym_series + 3 == pd.Series([ym(2002, 1), ym(2002, 6)])).all()
        assert (ym_series.apply(lambda v: v.year)
                == pd.Series([2001, 2002])).all()
        assert ((ym_series == "200110") == pd.Series([True, False])).all()

    def test_convert(self):
        ym1 = ym(2001, 10)
        assert ym1.toint() == 200110
        assert ym1.tostr() == "200110"
        assert ym1.todatetime(day=5) == datetime(2001, 10, 5)
        assert int(ym1) == 200110
        assert str(ym1) == "200110"
        # 年が3桁の場合のテスト
        assert ym(794, 10).toint() == 79410
        assert ym(794, 10).tostr() == "079410"


if __name__ == '__main__':
    unittest.main()
