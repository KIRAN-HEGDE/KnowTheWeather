import requests
from dotenv import load_dotenv
import os

load_dotenv()


class WeatherDetails:
    URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, response: dict):
        self.co_ordinates = response["coord"]
        self.weather_desc = response["weather"]
        self.temp_details = response["main"]
        self.wind_details = response['wind']

    @classmethod
    def by_city_name(cls, city_name: str):
        query = {'q': city_name, 'appid': os.getenv("API_KEY")}
        response = requests.get(WeatherDetails.URL, params=query).json()
        if response["cod"] != 200:
            raise Exception(response["message"])
        # print(response)
        return cls(response)

    @classmethod
    def by_latitude_longitude(cls, lat: float, lon: float):
        query = {'lat': lat, 'lon': lon, 'appid': os.getenv("API_KEY")}
        response = requests.get(WeatherDetails.URL, params=query).json()
        if response["cod"] != 200:
            raise Exception(response["message"])
        # print(response)
        return cls(response)

    def __str__(self) -> str:
        return f"WeatherDetails[" + "\n" \
               + f"    co_ordinates={self.co_ordinates}\n" \
               + f"    weather_desc={self.weather_desc}\n" \
               + f"    temperature_details={self.temp_details}\n" \
               + f"    wind_details={self.wind_details}\n" \
               + "]"


if __name__ == "__main__":
    weather_details = WeatherDetails.by_city_name("sagar")
    print(weather_details)
    weather_details2 = WeatherDetails.by_latitude_longitude(35.02, 90.00)
    print(weather_details2)
