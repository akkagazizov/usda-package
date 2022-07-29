from src.usda.api.services import FASService, MARSService, NASSService
from src.usda.api.services._base import ServiceBase

SETTINGS = {
    "fas": {
        "api_key": "jhk234nkj34jh5987812mn",
        "url": "https://www.fas.usda.gov",
    },
    "mars": {
        "api_key": "jhk234nkj34jh5987812mn",
        "url": "https://mymarketnews.ams.usda.gov",
    },
    "nass": {
        "api_key": "jhk234nkj34jh5987812mn",
        "url": "https://www.nass.usda.gov",
    },
}


def main() -> None:
    fas = FASService(api_key=SETTINGS["fas"]["api_key"], url=SETTINGS["fas"]["url"])
    nass = NASSService(api_key=SETTINGS["nass"]["api_key"], url=SETTINGS["nass"]["url"])
    mars = MARSService(api_key=SETTINGS["mars"]["api_key"], url=SETTINGS["mars"]["url"])
    
    all_services: list[ServiceBase] = [fas, nass, mars]
    
    for service in all_services:
        print(service.get())
        df = service.dataframe()
        print(df.head())
        service.to_file(f"C:\\Users\\eldar.gazizov\\Desktop\\usda-package", df)
        print("======================")


if __name__ == "__main__":
    main()