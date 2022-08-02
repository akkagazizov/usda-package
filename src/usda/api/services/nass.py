from typing import Union, NamedTuple, Any
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from ._base import ServiceBase
from src.usda.api.utils.prepare_path import path_prepare


@dataclass
class NASSService(ServiceBase):
    """
    National Agricultural Statistics Service (NASS)
    """

    url: str = "http://quickstats.nass.usda.gov/api"

    class EndpointAPI(NamedTuple):
        GET_API = "/api_GET/"

    def get(self, endpoint: Union[EndpointAPI, str] = EndpointAPI.GET_API, params: dict = None) -> str:
        payload = dict(key=self.api_key, format="JSON")
        if params:
            payload.update(params)
        req = super().get(endpoint, payload)
        if isinstance(req, int):
            return req
        self.data = req.json()["data"]
        return req.status_code

    def to_file(self, path: Union[Path, str], df: pd.DataFrame) -> Path:
        path = path_prepare(path) / f"{__class__.__name__}.csv"
        super().to_file(path, df)
        return path

    def _prepare_data(self, df: Any, *args, **kwargs) -> Any:
        df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
        dfgroup = df.groupby(["state_name", "year"])["Value"].sum()
        return dfgroup

    def plot(self, df: Any, x: str, y: str, type="bar") -> None:
        df = self._prepare_data(df)
        df.plot(kind=type, x=x, y=y)
        plt.title("National Agricultural Statistics Service")
        plt.show()
