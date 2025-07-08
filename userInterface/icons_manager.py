'''
MODULE TO MANAGE THE ICONS
'''
import os

#RETURN THE ICON NAME WEATHER - SPAGHETTI
def select_weather_icon(mDesc, desc):
    
    if mDesc == 'Thunderstorm':
        return 'blue-cloud-and-lightning-16466.png'
    elif mDesc == 'Drizzle':
        return 'downpour-rain-and-blue-cloud-16463.png'
    elif mDesc == 'Rain':
        if desc in ['heavy intensity rain', 'very heavy rain', 'extreme rain']:
            return 'rainy-day-and-blue-cloud-16462.png'
        elif desc in ['shower rain', 'heavy intensity shower rain', 'ragged shower rain']:
            return 'downpour-rain-and-blue-cloud-16463.png'
        elif desc in ['light intensity', 'shower rain']:
            return 'lightning-and-rainy-weather-16465.png'
        else:
            return 'rainy-day-16464.png'
    elif mDesc == 'Snow':
        if desc == 'rain and snow':
            return 'hail-and-blue-cloud-16491.png'
        elif desc == 'heavy shower snow':
            return 'snowy-weather-16472.png'
        else:
            return 'winter-snowfall-16473.png'
    elif mDesc == 'Clear':
        return 'sunny-day-16458.png'
    elif mDesc == 'Clouds':
        if desc == 'few clouds':
            return 'sun-and-blue-cloud-16460.png'
        elif desc in ['scattered clouds', 'broken clouds']:
            return 'blue-clouds-and-sun-16461.png'
        elif desc == 'overcast clouds':
            return 'cloudy-weather-16459.png'
    elif mDesc == 'Tornado':
        return 'storm-or-typhoon-16483.png'
    else:
        return 'alert.png'
    
#RETURN THE ICON NAME POLLUTION - SPAGHETTI
def select_pollution_icon(air_quality):
    if air_quality == 1:
        return 'pollution_1.png'
    elif air_quality == 2:
        return 'pollution_2.png'
    elif air_quality == 3:
        return 'pollution_3.png'
    elif air_quality == 4:
        return 'pollution_4.png'
    elif air_quality == 5:
        return 'pollution_5.png'
    else:
        return 'alert.png'

#RETURN THE ICON NAME STATIC
def select_static_img(text):
    
    #Dict with values
    dct = { 'rain' : 'rain.png'
           ,'snow' : 'snow.png'
           ,'tMin' : 'tMin.png'
           ,'tMax' : 'tMax.png'#'thermometer-and-hot-16481.png'
           ,'wind' : 'windy-16476.png'
           ,'pres' : 'pressure.png'
           ,'humi' : 'humidity.png'
           }
    
    return dct.get(text, 'alert.png')
    
#RETURN PATH ICON
def path_weather_ico(icon):
    icopath = os.path.abspath(os.path.join("..", "resources", "icons", icon))
    return icopath
    
#USE THE LAST PROCEDURE TO TRANLATE TXT -> ICON
def get_weather_ico(mDesc,desc):
    icon = select_weather_icon(mDesc,desc)
    return path_weather_ico(icon)

#USE THE LAST PROCEDURE TO TRANLATE TXT -> ICON
def get_pollution_ico(air_q):
    icon = select_pollution_icon(air_q)
    return path_weather_ico(icon)
    
#RETURN THE STATIC ICON
def get_static_ico(text):
    icon = select_static_img(text)
    return path_weather_ico(icon)
