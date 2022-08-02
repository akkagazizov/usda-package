from pathlib import Path
from typing import Union

import pandas as pd

from .prepare_path import path_prepare


def merge_and_savefile(path: Union[Path, str], dfs: dict[str, pd.DataFrame], year: int) -> None:
    path = path_prepare(path) / "FULL_file.xlsx"
    with pd.ExcelWriter(path) as writer:
        for i, df in dfs.items():
            df.to_excel(writer, sheet_name=f"{i}_{year}")
