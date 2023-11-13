from datetime import datetime
import pandas as pd
from tinypybits.timeseries.pandas_wrapper import (
    TimeIndexedSeries,
)

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)
NORMAL_YEAR_DAYS = 365

def leap_days_mask(time_index):
    return (time_index.month == 2) & (time_index.day == 29)

def test_timeseries_equal_by_values():
    first = TimeIndexedSeries(
        pd.Series([1, 1, 1], index=pd.period_range(START_DATE, periods=3))
    )
    second = TimeIndexedSeries(
        pd.Series([1, 1, 1], index=pd.period_range(START_DATE, periods=3))
    )
    assert first == second


def test_filtering_series_doesnt_change_period_index():
    days = "D"
    index = pd.period_range(START_DATE, END_DATE, freq=days)
    series = pd.Series([0.0] * len(index), index=index)
    assert len(series) == 2 * NORMAL_YEAR_DAYS + 1

    series = series[~leap_days_mask(series.index)]
    assert len(series) == 2 * NORMAL_YEAR_DAYS
    assert series.index.freq == days


def test_filtering_series_does_change_datetime_index():
    days = "D"
    index = pd.date_range(START_DATE, END_DATE, freq=days)
    series = pd.Series([0.0] * len(index), index=index)
    assert len(series) == 2 * NORMAL_YEAR_DAYS + 1

    series = series[~leap_days_mask(series.index)]
    assert len(series) == 2 * NORMAL_YEAR_DAYS
    assert series.index.freq != days


def test_can_upscale_series():
    yearly_index = pd.period_range(
        start=START_DATE,
        end=END_DATE,
        freq="A"
    )
    yearly_series = pd.Series([1.0] * len(yearly_index), index=yearly_index)
    assert len(yearly_series) == 2

    new_freq = "D"
    resampled = yearly_series.resample(new_freq).ffill()
    assert len(resampled) == 2 * NORMAL_YEAR_DAYS + 1
    resampled = resampled[~leap_days_mask(resampled.index)]
    
    assert len(resampled) == 2 * NORMAL_YEAR_DAYS
    assert resampled.index.freq == new_freq
