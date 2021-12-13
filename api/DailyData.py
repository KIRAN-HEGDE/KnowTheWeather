import os
import requests
from dotenv import load_dotenv

from api.CurrentData import CurrentData


class DailyData:
    URL_FOR_DAILY_DATA = "https://api.openweathermap.org/data/2.5/onecall"

    def __init__(self, data: dict):
        self.co_ordinates = {'lat': data["lat"], 'lon': data['lon']}
        self.data_list: list = data['daily']

    @classmethod
    def by_latitude_longitude(cls, lat: float, long: float):
        query = {'lat': lat, 'lon': long, 'appid': os.getenv("API_KEY")}
        response = requests.get(DailyData.URL_FOR_DAILY_DATA, params=query).json()

        # print(response)
        return cls(response)

    @classmethod
    def by_city_name(cls, city_name: str):
        lat, lon = CurrentData.by_city_name(city_name).get_coordinates()
        return DailyData.by_latitude_longitude(lat, lon)

    def __str__(self) -> str:
        return "DailyData[\n" \
               + f"     Coordinates={self.co_ordinates}\n" \
               + f"     daily_data={self.data_list}\n" \
               + "]"


if __name__ == "__main__":
    load_dotenv()
    daily_data = DailyData.by_city_name("sagar")
    print(daily_data)
