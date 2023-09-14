from aiogram import Dispatcher
from aiogram.types import Message

from .coordinates import get_coordinates
from .weather_api_service import get_weather
from .weather_formatter import format_weather
from .exceptions import ApiServiceError, CantGetCoordinates


async def start(message: Message):
    try:
        coordinates = get_coordinates()
    except CantGetCoordinates:
        print('Не удалось получить GPS координаты')
        exit(1)
    try:
        weather = get_weather(coordinates)
    except ApiServiceError:
        print(f'Не удалось получить сведения о погоде по координатам: {coordinates}')
        exit(1)
    formatted_weather = format_weather(weather)
    await message.bot.send_message(message.chat.id, formatted_weather)


def register_user_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start, commands=['start'])
