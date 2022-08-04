from collections import defaultdict
import pandas as pd


def resample_datetime_field(df: pd.DataFrame, key: str) -> set[int]:
    df[key] = pd.to_datetime(df[key])
    df.sort_values(by=[key])
    range_of_years = df[key].dt.year
    return set(range_of_years.unique())


def make_subdataframes_by_year(range_years: list[int], dfs: dict[str, pd.DataFrame]) -> dict[int, pd.DataFrame]:
    sub_dfs = defaultdict(list)
    for name, df in dfs.items():
        for year in range_years:
            sub_dfs[name].append(df[df["year"] == year])

    return sub_dfs
