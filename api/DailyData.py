import requests

from .CurrentData import CurrentData


class DailyData:
    URL_FOR_DAILY_DATA = "https://api.openweathermap.org/data/2.5/onecall"

    def __init__(self, data: dict):
        self.co_ordinates = {'lat': data["lat"], 'lon': data['lon']}
        self.data_list: list = data['daily']
        self.time_zone: str = data['timezone']

    @classmethod
    def by_latitude_longitude(cls, lat: float, long: float):
        query = {'lat': lat, 'lon': long, 'appid': '1c2e706a6a347e137b47207ca013c8da'}
        response = requests.get(DailyData.URL_FOR_DAILY_DATA, params=query)
        response.raise_for_status()
        response = response.json()
        return cls(response)

    @classmethod
    def by_city_name(cls, city_name: str):
        lat, lon = CurrentData.by_city_name(city_name).get_coordinates()
        return DailyData.by_latitude_longitude(lat, lon)

    def __str__(self) -> str:
        return "DailyData[\n" \
               + f"     Coordinates={self.co_ordinates}\n" \
               + f"     daily_data={self.data_list}\n" \
               + f"     time_zone={self.time_zone}\n" \
               + "]"


if __name__ == "__main__":
    daily_data = DailyData.by_city_name("sagar")
    print(daily_data)
