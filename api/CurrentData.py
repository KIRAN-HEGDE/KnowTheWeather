import requests
from dotenv import load_dotenv
import os


class CurrentData:
    URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, response: dict):
        self.co_ordinates: dict = response["coord"]
        self.weather_desc: dict = response["weather"][0]
        self.temp_details: dict = response["main"]
        self.wind_details: dict = response['wind']

    @classmethod
    def by_city_name(cls, city_name: str):
        query = {'q': city_name, 'appid': os.getenv("API_KEY")}
        response = requests.get(CurrentData.URL, params=query).json()
        if response["cod"] != 200:
            raise Exception(response["message"])
        # print(response)
        return cls(response)

    @classmethod
    def by_latitude_longitude(cls, lat: float, lon: float):
        query = {'lat': lat, 'lon': lon, 'appid': os.getenv("API_KEY")}
        response = requests.get(CurrentData.URL, params=query).json()
        if response["cod"] != 200:
            raise Exception(response["message"])
        # print(response)
        return cls(response)

    def get_coordinates(self):
        lat = float(self.co_ordinates['lat'])
        lon = float(self.co_ordinates['lon'])
        return lat, lon

    def __str__(self) -> str:
        return f"CurrentWeatherData[" + "\n" \
               + f"    co_ordinates={self.co_ordinates}\n" \
               + f"    weather_desc={self.weather_desc}\n" \
               + f"    temperature_details={self.temp_details}\n" \
               + f"    wind_details={self.wind_details}\n" \
               + "]"


if __name__ == "__main__":
    load_dotenv()
    weather_details = CurrentData.by_city_name("sagar")
    # print(weather_details)
    weather_details2 = CurrentData.by_latitude_longitude(35.02, 90.00)
    # print(weather_details2)
    # print(weather_details.get_coordinates())
