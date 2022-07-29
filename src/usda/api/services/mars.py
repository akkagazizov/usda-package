from typing import Union
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from ._base import ServiceBase


@dataclass
class MARSService(ServiceBase):
    def get(self, query: str = None) -> str:
        msg = super().get(query)
        return f"<{__class__.__name__}>\n" + msg
    
    def to_file(self, path: Union[Path, str], df: pd.DataFrame = None) -> None:
        path = self._path_prepare(path)
        if not df.empty:
            df.to_csv(path / f"{__class__.__name__}.csv", index=False)
        else:
            with open(path / f"{__class__.__name__}.txt", "w") as fh:
                fh.write(f"Hello from {__class__.__name__}")

    def dataframe(self) -> pd.DataFrame:
        return self.data({"urls":["www.google.com", "www.wiki.com"],
                             "rating":[5,5],
                             "count_visited":[100000, 1234]})
