'''
MODULE THAT ADAPT TO API
'''
#GET API KEY FROM .env FILE
from dotenv import load_dotenv
import os
import weatherApi.apiTools.getJson as gj

#CHARGE ENVIROMMENT VALUES
load_dotenv()
API_KEY = os.getenv("OWM_API_KEY")

#CORE PROCEDURE TO GET THE CURRENT WEATHER
def get_currentWeather(lat_lon=False,lc=[[]]):
    
    ll=[]
    
    if lat_lon is True:
        
        lat,lon = gj.get_ipLocation()
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}'
        l,c,t =  gj.core_currentWeather(url)
        ll.append(l)
        
    else:
        
        for k in lc:

            city,countryCode = k[0],k[1] 
            url=f'https://api.openweathermap.org/data/2.5/weather?q={city},{countryCode}&units=metric&appid={API_KEY}'
            #print(url)
            l,c,t =  gj.core_currentWeather(url) 
            ll.append(l)
     
    return ll,c,t

#CORE PROCEDURE TO GET THE CURRENT POLLUTION AND FORECAST
def get_currentPollution(city,country,ll,forecast):
    
    if forecast == 0:
        
        url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={ll[0]}&lon={ll[1]}&appid={API_KEY}'
            
    else:
            
        url = f'http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={ll[0]}&lon={ll[1]}&appid={API_KEY}'
      
    #19/05/2025 NEW FEATURE: ADD LAT & LON FOR MAP MARKERS
    return gj.core_currentPollution(city,country,url,ll)

#CORE PROCEDURE TO GET THE FORECAST WEATHER
def get_forecastWeather(ll):
    
    url = f'http://api.openweathermap.org/data/2.5/forecast?lat={ll[0]}&lon={ll[1]}&units=metric&appid={API_KEY}'
    
    return gj.core_forecastWeather(url)

#MAIN PROCEDURE TO GET THE LAT/LON
def get_loc_city(city):
    
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}'
    l =  gj.core_loc_city(url,1)
    
    return l

#MAIN PROCEDURE TO GET THE LAT/LON BY ZIP code
def get_loc_zip(zipCode,country):
    
    url = f'http://api.openweathermap.org/geo/1.0/zip?zip={zipCode},{country}&appid={API_KEY}'
    l = gj.core_loc_city(url,0)
    
    return l

#MAIN PROCEDURE TO GET THE CURRENT WEATHER BY IP
def get_weather_ip():
    return get_currentWeather(lat_lon=True)

#MAIN PROCEDURE TO GET THE CURRENT WEATHER BY CITIES LIST
def get_weather_cities(listCities):
    return get_currentWeather(lc=listCities)

#MAIN PROCEDURE TO GET THE FORECAST WEATHER BY CITY
def get_fcWeather_city(city):
    
    ll = get_loc_city(city)
    
    return get_forecastWeather([ll[1],ll[2]])

#MAIN PROCEDURE TO GET THE FORECAST WEATHER BY ZIP
def get_fcWeather_zip(zipCode,country):
        
    ll = get_loc_zip(zipCode,country) 

    return get_forecastWeather([ll[1],ll[2]])

#MAIN PROCEDURE TO GET THE POLLUTION BY CITY
def get_pollution_city(city,fc=0):
    
    city,lat,lon,country = get_loc_city(city) 
    
    return get_currentPollution(city,country,[lat,lon],fc)

#MAIN PROCEDURE TO GET THE POLLUTION BY ZIP code
def get_pollution_zip(zipCode,country,fc=0):
    
    city,lat,lon,country = get_loc_zip(zipCode,country) 

    return get_currentPollution(city,country,[lat,lon],fc)
