from typing import Union, NamedTuple
from dataclasses import dataclass
from pathlib import Path

from requests.auth import HTTPBasicAuth

from ._base import ServiceBase


@dataclass
class MARSService(ServiceBase):
    """"""
    url: str = "https://marsapi.ams.usda.gov/services/v1.2"
    
    class EndpointAPI(NamedTuple):
        GET_REPORTS = '/reports'
    
    def get(self, endpoint: EndpointAPI, params: dict = None) -> str:
        self.auth = HTTPBasicAuth(username=self.api_key, password="")
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
