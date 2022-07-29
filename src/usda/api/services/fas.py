from typing import Union
from dataclasses import dataclass
from pathlib import Path

from ._base import ServiceBase


@dataclass
class FASService(ServiceBase):
    """"""
    
    url: str = "https://apps.fas.usda.gov/OpenData/api"
    
    def get(self, endpoint: str = "/gats/regions", params: dict = None) -> str:
        self.headers.update({"API_KEY": self.api_key})
        req = super().get(endpoint, params)
        if isinstance(req, int): 
            return req
        self.data = req.json()
        return req.status_code
    
    def to_file(self, path: Union[Path, str]) -> None:
        path = self._path_prepare(path) / f"{__class__.__name__}.csv"
        super().to_file(path)
        return path

    def get_data(self) -> dict:
        return self.data
