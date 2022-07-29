from typing import Union, NamedTuple
from dataclasses import dataclass
from pathlib import Path

from ._base import ServiceBase


@dataclass
class NASSService(ServiceBase):
    """"""
    
    url: str = "http://quickstats.nass.usda.gov/api"
    
    class EndpointAPI(NamedTuple):
        GET_API = '/api_GET/'
        GET_PARAM_VALUE = '/get_param_values/'
        GET_COUNTS = '/get_counts/'
    
    def get(self, endpoint: EndpointAPI, params: dict = None) -> str:
        payload = dict(key=self.api_key, format="JSON")
        if params: payload.update(params)
        req = super().get(endpoint, payload)
        if isinstance(req, int): 
            return req
        self.data = req.json()["data"]
        return req.status_code
    
    def to_file(self, path: Union[Path, str]) -> Path:
        path = self._path_prepare(path) / f"{__class__.__name__}.csv"
        super().to_file(path)
        return path

    def get_data(self) -> dict:
        return self.data

