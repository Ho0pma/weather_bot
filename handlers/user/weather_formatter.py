from .weather_api_service import Weather


def format_weather(weather: Weather) -> str:
    """Formats weather data in string"""
    return (
        f'{weather.city}, {weather.weather_type.value}, температура {weather.temperature}°C, '
        f'ощущается как {weather.temperature_feels_like}°C\n'
        f'Скорость ветра: {weather.wind} м/с\n'
        f'Восход: {weather.sunrise.strftime("%H:%M")}\n'
        f'Закат: {weather.sunset.strftime("%H:%M")}\n'
    )
