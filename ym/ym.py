# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Union

import pandas as pd


class ym:
    """YearMonth object
    """
    def __init__(self, *args):
        """YearMonthオブジェクトのコンストラクタ
        """
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
                except (ValueError, TypeError):
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

        assert self._month >= 1 and self._month <= 12
        assert self._year >= 0 and self._year <= 9999
        self._year_str = "{0:04d}".format(self._year)
        self._month_str = "{0:02d}".format(self._month)
        self._repr = self._year_str + self._month_str

    def get_year(self) -> int:
        """「年」の情報を得る

        Returns:
            int: 「年」
        """
        return self._year

    year = property(get_year)

    def get_month(self) -> int:
        """「月」の情報を得る

        Returns:
            int: 「月」
        """
        return self._month

    month = property(get_month)

    def __repr__(self) -> str:
        return self._repr

    def __add__(self, n: int) -> "ym":
        if isinstance(n, int):
            m = (self._month + n - 1) % 12 + 1
            y = self._year + (self._month + n - 1) // 12
            obj = ym(y, m)
            return obj

        raise ValueError("サポートされていない足し算です。")

    def __sub__(self, n: Union[int, "ym"]) -> Union["ym", int]:
        if isinstance(n, int):
            m = (self._month - n - 1) % 12 + 1
            y = self._year + (self._month - n - 1) // 12
            obj = ym(y, m)
            return obj
        elif isinstance(n, ym):
            return (self._year * 12 + self._month) - (n._year * 12 + n._month)

        raise ValueError("サポートされていない引き算です。")

    def __eq__(self, obj: "ym") -> bool:
        if not isinstance(obj, ym):
            obj = ym(obj)
        return self._repr == obj._repr

    def __ne__(self, obj: "ym") -> bool:
        if not isinstance(obj, ym):
            obj = ym(obj)
        return self._repr != obj._repr

    def __lt__(self, obj: "ym") -> bool:
        if not isinstance(obj, ym):
            obj = ym(obj)
        return self._repr < obj._repr

    def __le__(self, obj: "ym") -> bool:
        if not isinstance(obj, ym):
            obj = ym(obj)
        return self._repr <= obj._repr

    def __gt__(self, obj: "ym") -> bool:
        if not isinstance(obj, ym):
            obj = ym(obj)
        return self._repr > obj._repr

    def __ge__(self, obj: "ym") -> bool:
        if not isinstance(obj, ym):
            obj = ym(obj)
        return self._repr >= obj._repr

    def __int__(self) -> int:
        return self._year * 100 + self._month

    def __hash__(self) -> int:
        return hash(self._repr)

    def toint(self) -> int:
        return int(self)

    def tostr(self) -> str:
        """文字列に変換

        Returns:
            str: 変換された文字列
        """
        return self._repr

    def todatetime(self, day: int = 1) -> datetime:
        """datetimeオブジェクトに変換

        Args:
            day (int, optional): 日(day). Defaults to 1.

        Returns:
            datetime: 変換されたdatetimeオブジェクト
        """
        return datetime(self._year, self._month, day)
