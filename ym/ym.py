# -*- coding: utf-8 -*-

from datetime import datetime
import pandas as pd


class YM(object):
    def __init__(self, *args):
        if len(args) == 2:
            self._year = args[0]
            self._month = args[1]
        elif len(args) == 1 and isinstance(args[0], str):
            arg = args[0]
            if len(arg) == 6:
                self._year = int(arg[:4])
                self._month = int(arg[4:])
            else:
                try:
                    a = pd.Timestamp(arg)
                    self._year = a.year
                    self._month = a.month
                except:
                    raise ValueError("引数が条件を満たしていません。")
        elif len(args) == 1 and isinstance(args[0], int):
            arg = args[0]
            self._year = arg // 100
            self._month = arg % 100
        elif len(args) == 1 and isinstance(args[0], datetime):
            arg = args[0]
            self._year = arg.year
            self._month = arg.month
        else:
            raise ValueError("引数が条件を満たしていません。")

        self._year_str = "{0:04d}".format(self._year)
        self._month_str = "{0:02d}".format(self._month)
        self._repr = self._year_str + self._month_str

    def get_year(self):
        return self._year

    def set_year(self, year):
        assert year >= 0 and year <= 9999
        self._year = year
        self._year_str = "{0:04d}".format(self._year)
        self._repr = self._year_str + self._month_str

    year = property(get_year, set_year)

    def get_month(self):
        return self._month

    def set_month(self, month):
        assert month >= 1 and month <= 12
        self._month = month
        self._month_str = "{0:02d}".format(self._month)
        self._repr = self._year_str + self._month_str

    month = property(get_month, set_month)

    def __repr__(self):
        return self._repr

    def __add__(self, n):
        m = (self._month + n) % 12
        y = self._year + (self._month + n) // 12
        obj = YM(y, m)
        return obj

    def __sub__(self, n):
        m = (self._month - n) % 12
        y = self._year + (self._month - n) // 12
        obj = YM(y, m)
        return obj

    def __eq__(self, obj):
        if not isinstance(obj, YM):
            obj = YM(obj)
        return self._repr == obj._repr

    def __ne__(self, obj):
        if not isinstance(obj, YM):
            obj = YM(obj)
        return self._repr != obj._repr

    def __lt__(self, obj):
        if not isinstance(obj, YM):
            obj = YM(obj)
        return self._repr < obj._repr

    def __le__(self, obj):
        if not isinstance(obj, YM):
            obj = YM(obj)
        return self._repr <= obj._repr

    def __gt__(self, obj):
        if not isinstance(obj, YM):
            obj = YM(obj)
        return self._repr > obj._repr

    def __ge__(self, obj):
        if not isinstance(obj, YM):
            obj = YM(obj)
        return self._repr >= obj._repr

    def __int__(self):
        return self._year * 100 + self._month

    def toint(self):
        return int(self)

    def tostr(self):
        return self._repr

    def todatetime(self, day=1):
        return datetime(self._year, self._month, day)
