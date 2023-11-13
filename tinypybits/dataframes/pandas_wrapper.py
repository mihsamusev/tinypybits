from typing import Sequence
import numpy as np
import pandas as pd


HOURLY = "H"
DAILY = "D"
WEEKLY = "W"
MONTHLY = "M"
YEARLY = "Y"
ABSOLUTE_TOLERANCE = 1e-4


class TimeIndexedSeries:
    def __init__(self, series: pd.Series):
        assert isinstance(
            series.index, (pd.PeriodIndex)
        ), "Input series should be datetime-indexed Pandas Series"
        self.__pandas: pd.Series = series
        self.__frequency = series.index.freq

    @property
    def frequency(self):
        return self.__frequency

    def to_pandas(self) -> pd.Series:
        return self.__pandas

    def __eq__(self, other: "TimeIndexedSeries") -> bool:
        return (
            isinstance(other, TimeIndexedSeries)
            and np.allclose(self.__pandas, other.to_pandas(), atol=ABSOLUTE_TOLERANCE)
            and (self.frequency == other.frequency)
        )

    @classmethod
    def from_values(cls, values: Sequence) -> "TimeIndexedSeries":
        return cls(pd.Series(values))
