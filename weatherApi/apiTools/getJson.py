'''
MODULE THAT GET THE JSON DATA USING WEATHER API
'''

import requests
import weatherApi.exceptionManager.exceptManager as exM

#from datetime import datetime

#DISCLAMER: use ip to geolocate. So it's only aproximate to the real place
def get_ipLocation():
    
    #Acces to API ipInfo
    response = requests.get('https://ipinfo.io/json')
    
    if response.status_code == 200 or len(response) != 0:
        
        data = response.json()
        #Extract latitude and Longitude - "lat,lon"
        loc = data['loc']
        lat, lon = loc.split(',')
        
        return lat,lon
        
    else:
        print(f"REQUEST ERR: {response.status_code}")
        raise exM.APIgetLocation(f"ERR: {response.status_code} - API LOCATION")

#PROCEDURE TO EXTRACT THE API INFO
def core_currentWeather(url):
    
    #Request GET
    response = requests.get(url)
    
    #Verify response status(code 200)
    if response.status_code == 200:
        
        #JSON Conversion
        data = response.json()
        
        #Extract JSON values
        city            = data['name']
        latitude        = data['coord']['lat']
        longitude       = data['coord']['lon']
        country         = data['sys']['country']
        #base            = data['base']
        mainDesc        = data['weather'][0]['main']
        description     = data['weather'][0]['description']
        temperature     = data['main']['temp']# - 273.15
        thermal_feeling = data['main']['feels_like']# - 273.15
        temp_min        = data['main']['temp_min']
        temp_max        = data['main']['temp_max']
        presure         = data['main']['pressure']
        humidity        = data['main']['humidity']
        visibility      = data['visibility']
        wind_speed      = data['wind']['speed']
        wind_deg        = data['wind']['deg']
        
        try:
            wind_gust = data['wind']['gust']
        except KeyError:
            wind_gust = "No Record"
        
        try:
            rain = data['rain']['1h']
        except KeyError:
            rain = "No Record"
        
        try:
            snow = data['snow']['1h']
        except KeyError:
            snow = "No Record"
        
        cloudiness      = data['clouds']['all']
        sunrise         = data['sys']['sunrise']
        sunset          = data['sys']['sunset']
        dt              = data['dt']
        
        #sunrisedt = datetime.fromtimestamp(sunrise)
        #sunsetdt  = datetime.fromtimestamp(sunset)
        #dt_dt     = datetime.fromtimestamp(dt)
        
        l = [city,latitude,longitude,country,mainDesc,description,temperature,thermal_feeling
            ,temp_min,temp_max,presure,humidity,visibility,wind_speed,wind_deg,wind_gust
            ,rain,snow,cloudiness,sunrise,sunset,dt]
        
        #Show results
        '''
        print(f"City: {city} ({country})")
        #print(f"Record base type: {base}")
        print(f"Weather: {mainDesc}")
        print(f"Weather 2: {description}")
        print(f"Temperature: {temperature: .2f}°C (Thermal feeling: {thermal_feeling: .2f}°C)")
        print(f"Temperature amplitude {temp_min} - {temp_max}")
        print(f"Humidity: {humidity}%")
        print(f"Presure: {presure}")
        print(f"Visibility range: {visibility} m")
        print(f"Wind: {wind_speed} m/s")
        print(f"Wind degree: {wind_deg}º")
        print(f"Wind guts: {wind_gust} m/s")
        print(f"Cloudiness: {cloudiness}%")
        print(f"Rain: {rain} mm/h")
        print(f"Snow: {snow} mm/h")
        print(f"Sunrise: {sunrisedt.strftime('%H:%M:%S')}")
        print(f"Sunset: {sunsetdt.strftime('%H:%M:%S')}")
        print(f"dt: {dt_dt}")
        
        print(l)
        '''
        
        c = ['city','latitude','longitude','country','mainDesc','description','temperature','thermal_feeling'
            ,'temp_min','temp_max','presure','humidity','visibility','wind_speed','wind_deg','wind_gust'
            ,'rain','snow','cloudiness','sunrise','sunset','dt']
        t = ['VARCHAR(255)','VARCHAR(255)','VARCHAR(255)','VARCHAR(50)','VARCHAR(255)','VARCHAR(255)','NUMERIC','NUMERIC'
            ,'NUMERIC','NUMERIC','NUMERIC','NUMERIC','NUMERIC','NUMERIC','NUMERIC','NUMERIC'
            ,'NUMERIC','NUMERIC','NUMERIC','VARCHAR(255)','VARCHAR(255)','NUMERIC']
        
        
        return l,c,t
    
    else:
        print(f"REQUEST ERR: {response.status_code}")
        raise exM.APIgetWeather(f"ERR: {response.status_code} - API WEATHER")


#PROCEDURE TO EXTRACT THE API INFO
#19/05/2025 NEW FEATURE: ADD LAT & LON FOR MAP MARKERS
def core_currentPollution(city,country,url,ll):
    
    #Request GET
    response = requests.get(url)
    
    #Verify response status(code 200)
    if response.status_code == 200:
        
        #JSON Conversion
        data = response.json()
        l = []
        
        #Extract JSON values
        list_values     = data['list']
        
        #Loop the values
        for v in list_values:
            
            air_quality = v['main']['aqi']
            air_co      = v['components']['co']
            air_no      = v['components']['no']
            air_no2     = v['components']['no2']
            air_o3      = v['components']['o3']
            air_so2     = v['components']['so2']
            air_pm2_5   = v['components']['pm2_5']
            air_pm10    = v['components']['pm10']
            air_nh3     = v['components']['nh3']
            dt          = v['dt']
            
            #dt_dt       = datetime.fromtimestamp(dt)
            
            #19/05/2025 NEW FEATURE
            lv = [city,country,ll[0],ll[1],air_quality,air_co,air_no,air_no2,air_o3,air_so2,air_pm2_5,air_pm10,air_nh3,dt]
            
            #SHOW RESULTS
            '''
            print(lv)
            print(dt_dt)
            '''
            
            l.append(lv)
        
        #19/05/2025 NEW FEATURE
        c = ['city','country','latitude','longitude','air_quality','air_co','air_no','air_no2','air_o3','air_so2','air_pm2_5','air_pm10','air_nh3','dt']
        t = ['VARCHAR(255)','VARCHAR(255)','VARCHAR(255)','VARCHAR(50)','NUMERIC','NUMERIC','NUMERIC','NUMERIC','NUMERIC','NUMERIC','NUMERIC','NUMERIC','NUMERIC','NUMERIC']
        
        return l,c,t
    
    else:
        print(f"REQUEST ERR: {response.status_code}")
        raise exM.APIgetPollution(f"ERR: {response.status_code} - API POLLUTION")
    

#PROCEDURE TO EXTRACT THE API INFO
def core_forecastWeather(url):
    
    #Request GET
    response = requests.get(url)
    
    #Verify response status(code 200)
    if response.status_code == 200:
        
        #JSON Conversion
        data = response.json()
        l = []
        
        #Extract JSON values
        list_values     = data['list']
        
        #Loop the values
        for v in list_values:
            
            city            = data['city']['name']
            latitude        = data['city']['coord']['lat']
            longitude       = data['city']['coord']['lon']
            country         = data['city']['country']
            #Base not exists in forecast*
            mainDesc        = v['weather'][0]['main']
            description     = v['weather'][0]['description']
            temperature     = v['main']['temp']# - 273.15
            thermal_feeling = v['main']['feels_like']# - 273.15
            temp_min        = v['main']['temp_min']
            temp_max        = v['main']['temp_max']
            presure         = v['main']['pressure']
            humidity        = v['main']['humidity']
            visibility      = v['visibility']
            wind_speed      = v['wind']['speed']
            wind_deg        = v['wind']['deg']
            
            try:
                wind_gust = v['wind']['gust']
            except KeyError:
                wind_gust = "No Record"
            
            try:
                rain = v['rain']['3h']
            except KeyError:
                rain = "No Record"
                
            try:
                snow = v['snow']['3h']
            except KeyError:
                snow = "No Record"
            
            cloudiness      = v['clouds']['all']
            sunrise         = data['city']['sunrise']
            sunset          = data['city']['sunset']
            dt              = v['dt']
            
            #sunrisedt = datetime.fromtimestamp(sunrise)
            #sunsetdt  = datetime.fromtimestamp(sunset)
            #dt_dt     = datetime.fromtimestamp(dt)
            
            ldata = [city,latitude,longitude,country,mainDesc,description,temperature,thermal_feeling
                     ,temp_min,temp_max,presure,humidity,visibility,wind_speed,wind_deg,wind_gust
                     ,rain,snow,cloudiness,sunrise,sunset,dt]
            
            l.append(ldata)
            
            #Show results
            '''
            print(f"City: {city} ({country})")
            print(f"Weather: {mainDesc}")
            print(f"Weather 2: {description}")
            print(f"Temperature: {temperature: .2f}°C (Thermal feeling: {thermal_feeling: .2f}°C)")
            print(f"Temperature amplitude {temp_min} - {temp_max}")
            print(f"Humidity: {humidity}%")
            print(f"Presure: {presure}")
            print(f"Visibility range: {visibility} m")
            print(f"Wind: {wind_speed} m/s")
            print(f"Wind degree: {wind_deg}º")
            print(f"Wind guts: {wind_gust} m/s")
            print(f"Cloudiness: {cloudiness}%")
            print(f"Rain: {rain} mm/h")
            print(f"Snow: {snow} mm/h")
            print(f"Sunrise: {sunrisedt.strftime('%H:%M:%S')}")
            print(f"Sunset: {sunsetdt.strftime('%H:%M:%S')}")
            print(f"dt: {dt_dt}")
            '''
        
        
        c = ['city','latitude','longitude','country','mainDesc','description','temperature','thermal_feeling'
            ,'temp_min','temp_max','presure','humidity','visibility','wind_speed','wind_deg','wind_gust'
            ,'rain','snow','cloudiness','sunrise','sunset','dt']
        t = ['VARCHAR(255)','VARCHAR(255)','VARCHAR(255)','VARCHAR(50)','VARCHAR(255)','VARCHAR(255)','NUMERIC','NUMERIC'
            ,'NUMERIC','NUMERIC','NUMERIC','NUMERIC','NUMERIC','NUMERIC','NUMERIC','NUMERIC'
            ,'NUMERIC','NUMERIC','NUMERIC','VARCHAR(255)','VARCHAR(255)','NUMERIC']
            
        return l,c,t
    
    else:
        print(f"REQUEST ERR: {response.status_code}")
        raise exM.APIgetWeather(f"ERR: {response.status_code} - API WEATHER")


#PROCEDURE TO EXTRACT THE API INFO
def core_loc_city(url,control):
    
    #Request GET
    response = requests.get(url)

    #Verify response status(code 200)
    if response.status_code == 200:
      
        #JSON Conversion
        data = response.json()

        if data:
            
            l = []
            
            #Extract JSON values
            if control==1:
                city      = data[0]['name']
                latitude  = data[0]['lat']
                longitude = data[0]['lon']
                country   = data[0]['country']
                
            else:
                city      = data['name']
                latitude  = data['lat']
                longitude = data['lon']
                country   = data['country']
                
            l = [city,latitude,longitude,country]
            
            #Show results
            
            '''
            print(f"City: {city} ({country})")
            print(f"Lat: {latitude}, Lon: {longitude}")
            print(l)    
            '''
            return l
        
        else:
            print(f"REQUEST ERR: {response.status_code}")
            raise exM.APIgetLocation(f"ERR: {response.status_code} - API LOCATION")  
    
    else:
        print(f"REQUEST ERR: {response.status_code}")
        raise exM.APIgetLocation(f"ERR: {response.status_code} - API LOCATION")
