from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Union, NamedTuple, Any

import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from requests import Response


@dataclass
class ServiceBase(ABC):
    api_key: str
    url: str
    headers: dict = field(default_factory=lambda: {"Accept": "application/json"})
    auth: HTTPBasicAuth = None
    data: dict = field(default_factory=dict)

    class EndpointAPI(NamedTuple):
        ...

    @abstractmethod
    def get(self, endpoint: Union[EndpointAPI, str], params: dict = None) -> Union[Response, str]:
        req = requests.get(self.url + endpoint, params=params, auth=self.auth, headers=self.headers)
        if req.status_code == 200:
            return req
        return req.status_code

    @abstractmethod
    def to_file(self, path: Union[Path, str], df: pd.DataFrame) -> Path:
        df.to_csv(path, index=False)
        return path

    @abstractmethod
    def plot(self, df: Any, x: str, y: str, type="bar") -> None:
        ...

    @abstractmethod
    def _prepare_data(self, df: Any, *args, **kwargs) -> Any:
        ...

    def get_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.data)

    def _path_prepare(self, path: Union[Path, str]) -> Path:
        return Path(path) if isinstance(path, str) else path
