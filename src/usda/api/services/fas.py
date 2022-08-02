from typing import Union, NamedTuple, Any
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from ._base import ServiceBase
from src.usda.api.utils.prepare_path import path_prepare


@dataclass
class FASService(ServiceBase):
    """
    Foreign Agricultural Service (FAS)
    """

    url: str = "https://apps.fas.usda.gov/OpenData/api"

    class EndpointAPI(NamedTuple):
        ...

    def get(self, endpoint: Union[EndpointAPI, str], params: dict = None, **kwargs) -> str:
        self.headers.update({"API_KEY": self.api_key})
        req = super().get(endpoint.format(kwargs), params)
        if isinstance(req, int):
            return req
        self.data = req.json()
        return req.status_code

    def to_file(self, path: Union[Path, str], df: pd.DataFrame) -> Path:
        path = path_prepare(path) / f"{__class__.__name__}.csv"
        super().to_file(path, df)
        return path

    def plot(self, df: Any, x: str, y: str, type="bar") -> None:
        return super().plot(df, x, y, type)

    def _prepare_data(self, df: Any, *args, **kwargs) -> Any:
        return super()._prepare_data(df, *args, **kwargs)


@dataclass
class ESR(FASService):
    """Export Sales Report

    :param FASService
    """

    class EndpointAPI(NamedTuple):
        REGION_CODE_NAME = "/esr/regions"
        COUNTRY_CODE_NAME = "/esr/countries"
        COMMODITY_CODE_NAME = "/esr/commodities"
        UNITS_OF_MEASURE = "/esr/unitsOfMeasure"
        DATA_RELEASE_DATES = "/esr/datareleasedates"
        EXPORTS_DATA = "/esr/exports/commodityCode/{commodityCode}/allCountries/marketYear/{marketYear}"


@dataclass
class GATS(FASService):
    """Global Agricultural Trade System

    :param FASService
    """

    class EndpointAPI(NamedTuple):
        EXPORT_DATA_RELEASE_DATES = "/gats/census/data/exports/dataReleaseDates"
        IMPORT_DATA_RELEASE_DATES = "/gats/census/data/imports/dataReleaseDates"
        REGION_CODE_NAME = "/gats/regions"
        COUNTRY_CODE_NAME = "/gats/countries"
        COMMODITY_CODE_NAME = "/gats/commodities"
        HS6_COMMODITY_CODE_NAME = "/gats/HS6Commodities"
        UNITS_OF_MEASURE = "/gats/unitsOfMeasure"
        CUSTOM_DISTRICTS = "/gats/customsDistricts"
        CENSUS_IMPORT_DATA = "/gats/censusImports/partnerCode/{partnerCode}/year/{year}/month/{month}"
        CENSUS_EXPORT_DATA = "/gats/censusExports/partnerCode/{partnerCode}/year/{year}/month/{month}"


@dataclass
class PSD(FASService):
    """Production, Supply & Distribution

    :param FASService
    """

    class EndpointAPI(NamedTuple):
        REGION_CODE_NAME = "/psd/regions"
        COUNTRY_CODE_NAME = "/psd/countries"
        COMMODITY_CODE_NAME = "/psd/commodities"
        UNITS_OF_MEASURE = "/psd/unitsOfMeasure"
        COMMODITY_ATTRS = "/psd/commodityAttributes"
        DATA_RELEASE_DATES = "/psd/commodity/{commodityCode}/dataReleaseDates"
        EXPORTS_DATA = "/esr/exports/commodityCode/{commodityCode}/allCountries/marketYear/{marketYear}"
