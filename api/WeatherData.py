from dotenv import load_dotenv

from .CurrentData import CurrentData
from .DailyData import DailyData

load_dotenv()


class WeatherData:

    def __init__(self, current_data: CurrentData, daily_data: DailyData):
        self.current_data = current_data
        self.daily_data = daily_data

    @classmethod
    def by_city_name(cls, city_name: str):
        current_data = CurrentData.by_city_name(city_name)
        lat, lon = current_data.get_coordinates()
        daily_data = DailyData.by_latitude_longitude(lat, lon)

        return cls(current_data, daily_data)

    @classmethod
    def by_latitude_longitude(cls, lat: float, lon: float):
        current_data = CurrentData.by_latitude_longitude(lat, lon)
        daily_data = DailyData.by_latitude_longitude(lat, lon)
        return cls(current_data, daily_data)

    def __str__(self) -> str:
        return f"{self.current_data} \n {self.daily_data}"


if __name__ == "__main__":
    weather_data = WeatherData.by_city_name("sagar")
    print(weather_data)
    weather_data_by_lat_lon = WeatherData.by_latitude_longitude(34.00, 35.00)
    print(weather_data_by_lat_lon)
