import pandas as pd

from column_tag import ColumnTag



def convert_to_euro(dataframe: pd.DataFrame, rate: float) -> pd.DataFrame:
    dollar_columns = [c for c in dataframe.columns if c.unit == "$"]

    # column tag update part
    euro_columns = dollar_columns.copy()
    for c in euro_columns:
        c.unit = "€"
    dataframe = dataframe.rename(columns=dict(zip(dollar_columns, euro_columns)))

    # data update part
    dataframe[dollar_columns] = dataframe[dollar_columns] * rate
    return dataframe


def get_by_id(dataframe: pd.DataFrame, id: str) -> pd.DataFrame:
    """
    alternatives:
        1)
        dataframe.filter(like=id) # neat

        2)
        dataframe.loc[:, df.columns.str.contains(id)] # fugly AF
    """
    matches = [c for c in dataframe.columns if c.id == id]
    return dataframe[matches]

def main():
    dataframe = pd.DataFrame(
        {
            ColumnTag("burger", unit="$", labels=["USA", "discounted"]): [10.0, 20.0],
            ColumnTag("eagle", unit="$", labels=["USA"]): [1000.0, 2000.0],
            ColumnTag("bubble tea", unit="€", labels=["EU"]): [42.0, 69.0],
        }
    )

    print("\n", dataframe.columns)
    print("\n", dataframe.to_string())

    # How to make sure that the column data and column tag are never out of sync?
    print("\n", convert_to_euro(dataframe, 0.420).to_string())

    # How do i know that working with tagged colums and avoid mixing in normal strings?
    # - wrap pd.DataFrame to TaggedDataFrame? how to support dozens of useful dataframe methods?
    # - keep the discipline of only interacting with columns with special functions like "get_by_id" instead of "[]"
    print("\n", get_by_id(dataframe, "burger"))
    print("\n", dataframe.filter(like="bubble"))
    get(dataframe, Electronyzer.power_output)
    get(dataframe, Electrolyzer, variables.PowerOutput())


if __name__ == "__main__":
    main()