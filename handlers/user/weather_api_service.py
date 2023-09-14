""" КОМУНИКАЦИЯ С ВНЕШНИМ СЕРВИСОМ ПОГОДЫ - openweather """
from urllib.error import URLError

import requests

from datetime import datetime
from enum import Enum
from typing import NamedTuple, Literal

from . import settings
from .coordinates import Coordinates
from .exceptions import ApiServiceError

Celsius = float


class WeatherType(Enum):  # фишка в том, что каждый элемент Enum будет иметь такой же тип как Enum
    THUNDERSTORM = 'Гроза'
    DRIZZLE = 'Изморозь'
    RAIN = 'Дождь'
    SNOW = 'Снег'
    CLEAR = 'Ясно'
    FOG = 'Туман'
    CLOUDS = 'Облачно'


# про Enum:
# его полезно использовать тк можно достучаться и до значения справа, и до значения слева
# print(WeatherType.RAIN.value)  # Дождь
# print(WeatherType.RAIN.name)  # RAIN
# а без унаследования от класса Enum такой фишки не будет


class Weather(NamedTuple):
    temperature: Celsius  # alias - псевдоним, если к примеру нужно будет менять на другой тип - поменять нужно будет
    # только в одном месте. Также сразу понять в чем идет измерение температуры.
    temperature_feels_like: Celsius
    wind: int
    weather_type: WeatherType  # когда идет задача на перечисление чего-либо - задача для Enum
    sunrise: datetime
    sunset: datetime
    city: str


def get_weather(coordinates: Coordinates) -> Weather:
    """Requests weather in OpenWeather API and returns it"""
    openweather_response = _get_openweather_response(
        latitude=coordinates.latitude, longitude=coordinates.longitude
    )
    print(openweather_response)
    weather = _parse_openweather_response(openweather_response)
    return weather


def _get_openweather_response(latitude: float, longitude: float) -> dict:
    url = settings.OPENWEATHER_URL.format(latitude=latitude, longitude=longitude)
    try:
        return requests.get(url).json()
    except URLError:
        raise ApiServiceError


def _parse_openweather_response(openweather_dict: dict) -> Weather:
    return Weather(
        temperature=_parse_temperature(openweather_dict),
        temperature_feels_like=_parse_temperature_feels_like(openweather_dict),
        wind=_parse_wind(openweather_dict),
        weather_type=_parse_weather_type(openweather_dict),
        sunrise=_parse_sun_time(openweather_dict, 'sunrise'),
        sunset=_parse_sun_time(openweather_dict, 'sunset'),
        city=_parse_city(openweather_dict)
    )


def _parse_temperature(openweather_dict: dict) -> Celsius:
    return openweather_dict['main']['temp']


def _parse_temperature_feels_like(openweather_dict: dict) -> Celsius:
    return openweather_dict['main']['feels_like']


def _parse_wind(openweather_dict: dict) -> int:
    return openweather_dict['wind']['speed']


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict['weather'][0]['id'])
    except (IndexError, KeyError):
        raise ApiServiceError
    weather_types = {
        '1': WeatherType.THUNDERSTORM,
        '3': WeatherType.DRIZZLE,
        '5': WeatherType.RAIN,
        '6': WeatherType.SNOW,
        '7': WeatherType.FOG,
        '800': WeatherType.CLEAR,
        '80': WeatherType.CLOUDS,
    }
    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise ApiServiceError


def _parse_sun_time(
        openweather_dict: dict,
        time: Literal['sunset'] | Literal['sunrise']) -> datetime:
    return datetime.fromtimestamp(openweather_dict['sys'][time])


def _parse_city(openweather_dict: dict) -> str:
    return openweather_dict['name']
