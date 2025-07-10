'''
MODULE TO CENTALIZE ERRORS
'''

# CUSTOM EXCEPTIONS --------------------------

class WeatherAPIError(Exception):
    """An error into API"""
    pass

class APIgetWeather(WeatherAPIError):
    """Problem getting weather info"""
    pass

class APIgetPollution(WeatherAPIError):
    """Problem getting pollution info"""
    pass

class APIgetLocation(WeatherAPIError):
    """Problem getting location info"""
    pass

# -----------------------------------------
