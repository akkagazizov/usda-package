from pathlib import Path

import pandas as pd

from src.usda.api.services import NASSService, MARSService, FASService


ROOT_DIR_PATH = Path(__name__).absolute().parent
PATH_TO_SAVE_DATA = ROOT_DIR_PATH / "data"

# API_KEY taken after registering on each website
SETTINGS = {
    "fas": {
        "api_key": "api_key",
        "url": "https://apps.fas.usda.gov/OpenData/swagger/docs/v1",
    },
    "mars": {
        "api_key": "api_key",
        "url": "https://marsapi.ams.usda.gov/services/v1.2",
    },
    "nass": {
        "api_key": "api_key",
        "url": "http://quickstats.nass.usda.gov/api",
    },
}


def main() -> None:

    # Init USDA APIs services
    nass = NASSService(SETTINGS["nass"]["api_key"])
    fas = FASService(SETTINGS["fas"]["api_key"])
    mars = MARSService(SETTINGS["mars"]["api_key"])

    # Set endpoints and query params for search and filter
    commodityCode = 101
    year = 2012
    stat_mars = mars.get()
    stat_fas = fas.get(endpoint=f"/esr/exports/commodityCode/{commodityCode}/allCountries/marketYear/{year}")
    stat_nass = nass.get(params={"commodity_desc": "CORN", "year__GE": "2018", "state_alpha": "VA"})

    # DataFrames container
    dfs: list[pd.DataFrame] = []

    # Main loop walk through all of services
    for service, name, stat in zip([nass, mars], ["NASS", "MARS"], [stat_nass, stat_mars]):
        print(f"==========={name}===========")
        print(f"status code: {stat}")
        print(f"url: {service.url}")
        df = service.get_dataframe()
        dfs.append(df)
        print(df.head())
        path = service.to_file(PATH_TO_SAVE_DATA, df)
        print(f"See: {path}")
        print("==========================")

    # Draw histogram sum value CORNs per year from 2018 to 2022
    nass.plot(dfs[0], x="year", y="Value")


if __name__ == "__main__":
    main()
