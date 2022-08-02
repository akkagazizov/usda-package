from typing import Union, NamedTuple, Any
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from requests.auth import HTTPBasicAuth

from ._base import ServiceBase
from src.usda.api.utils.prepare_path import path_prepare


@dataclass
class MARSService(ServiceBase):
    """
    Agricultural Marketing Service (MARS)
    """

    url: str = "https://marsapi.ams.usda.gov/services/v1.2"

    class EndpointAPI(NamedTuple):
        GET_REPORTS = "/reports"

    def get(self, endpoint: Union[EndpointAPI, str] = EndpointAPI.GET_REPORTS, params: dict = None) -> str:
        self.auth = HTTPBasicAuth(username=self.api_key, password="")
        req = super().get(endpoint, params)
        if isinstance(req, int):
            return req
        self.data = req.json()
        return req.status_code

    def to_file(self, path: Union[Path, str], df: pd.DataFrame) -> Path:
        path = path_prepare(path) / f"{__class__.__name__}.csv"
        super().to_file(path, df)
        return path

    def plot(self, df: Any, x: str = None, y: str = None, type="bar") -> None:
        df = self._prepare_data(df)
        df.plot(kind=type)
        plt.show()

    def _prepare_data(self, df: Any, *args, **kwargs) -> Any:
        dfgroup = df["markets"].value_counts().sort_values()
        return dfgroup
