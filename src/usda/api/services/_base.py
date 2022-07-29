from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Union

import pandas as pd
import requests


@dataclass
class ServiceBase(ABC):
    api_key: str
    url: str
    data: pd.DataFrame = pd.DataFrame
    
    @abstractmethod
    def get(self, query: str = None) -> str:
        req = requests.get(self.url)
        return f"<{self.url}> | status code: {req.status_code}"

    @abstractmethod
    def to_file(self, path: Union[Path, str], df: pd.DataFrame = None) -> None:
        ...

    @abstractmethod
    def dataframe(self) -> pd.DataFrame:
        ...

    def _path_prepare(self, path: Union[Path, str]) -> Path:
        return Path(path) if isinstance(path, str) else path