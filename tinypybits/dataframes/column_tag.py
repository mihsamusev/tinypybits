import pandas as pd


def pretty(tag: "ColumnTag") -> str:
    begin = f"{tag.id}[{tag.unit}"
    end = "]"
    if tag.labels:
        joined = ", ".join(tag.labels)
        end = f"; {joined}]"
    return begin + end


class ColumnTag:
    """
    id -> always unique and can be used to query a column, immutable after tag is created
    labels -> can be transformed together with dataframe
    units -> can be transformed together with dataframe
    """

    def __init__(self, id: str, unit=str, labels: list[str] = None) -> None:
        self.__id = id
        self.unit = unit
        self.labels = labels

    @property
    def id(self) -> str:
        return self.__id

    def __str__(self):
        return pretty(self)

