USE_ROUNDED_COORDS = True
OPENWEATHER_API = '4085262ea595e404992d6b75029d2a38'

OPENWEATHER_URL = (
        'https://api.openweathermap.org/data/2.5/weather?'
        'lat={latitude}&lon={longitude}&'
        'appid=' + OPENWEATHER_API + '&lang=ru&'
                                     'units=metric'
)
