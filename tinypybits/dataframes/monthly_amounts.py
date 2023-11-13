from datetime import timedelta, datetime
import pandas as pd

# Example hourly series indexed with datetime
series = pd.Series(data=0,
    index=pd.period_range(
        start=datetime(2020, 1, 1),
        end=datetime(2020, 12, 31),
        freq=timedelta(hours=1)))
series = series[~((series.index.month == 2) & (series.index.day == 29))]
print(series.shape)


total_amount = 8000

monthly_iterator = series.groupby(pd.Grouper(freq='M'))

prev_index = 0
amounts = []
for month, last_index in monthly_iterator.groups.items():
    size = last_index - prev_index
    amount = total_amount * (size / series.shape[0])
    amounts.append(amount)
    print(f"Month-{month}, {amount=}: {size=}, {prev_index}:{last_index}")
    prev_index = last_index

print(f"{amounts=}, sum={sum(amounts)}")