from typing import NamedTuple
from urllib.request import urlopen

from . import settings
from .exceptions import CantGetCoordinates
import json


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def get_coordinates() -> Coordinates:
    coordinates = _get_ipinfo_coordinates()
    return _round_coordinates(coordinates)


def _get_ipinfo_coordinates() -> Coordinates:
    ipinfo_output = _get_ipinfo_output()
    coordinates = _parse_coordinates(ipinfo_output)
    return coordinates


def _get_ipinfo_output() -> dict:
    output = json.load(urlopen("https://ipinfo.io/json"))
    return output


def _parse_coordinates(ipinfo_output: dict) -> Coordinates:
    try:
        output = ipinfo_output['loc'].split(',')
    except:
        raise CantGetCoordinates

    return Coordinates(
        latitude=float(output[0]),
        longitude=float(output[1])
    )


def _round_coordinates(coordinates: Coordinates) -> Coordinates:
    if not settings.USE_ROUNDED_COORDS:
        return coordinates
    return Coordinates(
        *map(lambda x: round(x, 1), [coordinates.latitude, coordinates.longitude])
    )
