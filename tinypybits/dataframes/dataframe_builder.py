import pandas as pd

class Timeline:
    def __init__(self, start_date, end_date):
        pass

class PriceItem:
    def __init__(self):
        pass

    def to_timeseries(self):
        pass

class ResourceItem:
    def __init__(self):
        pass

    def to_timeseries(self):
        pass

class TableBuilder:
    def __init__(self):
        self.__dataframe = None
        self.__timeline = None
        self.__price_items = []
        self.__resource_items = []

    def add_timeline(self, timeline: Timeline):
        pass

    def add_price_items(self, item: PriceItem):
        pass

    def add_resource_item(self, item: ResourceItem):
        pass

    def build() -> pd.DataFrame:
        pass