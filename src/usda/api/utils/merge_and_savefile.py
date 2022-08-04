from pathlib import Path
from typing import Union

import pandas as pd

from .prepare_path import path_prepare
from .data_manipulation import resample_datetime_field, make_subdataframes_by_year


def merge_and_savefile(path: Union[Path, str], dfs: dict[str, pd.DataFrame]) -> None:
    path = path_prepare(path) / "FULL_file.xlsx"
    years = get_range_years(dfs)
    dfs = make_subdataframes_by_year(years, dfs)
    with pd.ExcelWriter(path) as writer:
        for name, _dfs in dfs.items():
            for df, year in zip(_dfs, years):
                df.to_excel(writer, sheet_name=f"{name}_{year}")


def get_range_years(dfs: dict[str, pd.DataFrame]):
    for i, df in dfs.items():
        if i == "fas":
            ry1 = resample_datetime_field(df, "weekEndingDate")
            df["year"] = df["weekEndingDate"].dt.year
        if i == "nass":
            ry2 = resample_datetime_field(df, "load_time")
    return sorted(list(ry1 & ry2))
