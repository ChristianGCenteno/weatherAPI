'''
Module Aux to exe the FORECAST MANAGMMENT
'''
import weatherApi.exeAux.exeSQL as esql

import statistics
from datetime import datetime 
from collections import Counter

## WEATHER SECTION

# RETURN A LIST OF CITIES LOAD IN FORECAST BUFFER
def get_bufferWeather_cities():
    return esql.get_cities_buffer_weather()

# RETURN DICT OF FC WEATHER AND TRANSALTE DATETIME DICT
def get_WeatherDict():
    
    # dict where will host the results
    result = {}
    # get list of data cities
    cities = get_bufferWeather_cities()
    
    # loop cities to get FC data
    for city in cities:
        
        cty     = str(city[0])
        results = esql.get_dataCity_buffer_weather(cty)
        
        # create dict with datetimes as keys index number 13
        a = {value[13]: value for value in results}
        # create ditct by city
        b = {cty:a}
        
        # add dict into results dict
        result = {**result, **b}
        
    return result

## - END WEATHER SECTION

## GROUP AGGREGATION SECTION

# RETURN LIST OF TEMPERATURES BY DAY
def get_tempList(buffer,keys):
    return [ v[5] for k,v in buffer.items() if k in keys]

# RETURN AVEREGE TEMPERATURE TODAY
def get_TempAvg(buffer,keys):
    # Get list of temperatures
    temperatures = get_tempList(buffer, keys)
    # Return avg temperature
    return statistics.mean(temperatures)

# RETURN MINIMUN TEMPERATURE TODAY
def get_TempMin(buffer,keys):
    # Get list of temperatures
    temperatures = get_tempList(buffer, keys)
    # Return max temperature
    return min(temperatures)

# RETURN MAXIMUM TEMPERATURE TODAY
def get_TempMax(buffer,keys):
    # Get list of temperatures
    temperatures = get_tempList(buffer, keys)
    # Return max temperature
    return max(temperatures)      

# RETURN LIST OF PRESSURE BY DAY
def get_presList(buffer,keys):
    return [ v[8] for k,v in buffer.items() if k in keys]

# RETURN AVEREGE PRESSURE TODAY
def get_presAvg(buffer,keys):
    # Get list of pressures
    pressures = get_presList(buffer, keys)
    # Return max temperature
    return statistics.mean(pressures) 

# RETURN LIST OF HUMIDITY BY DAY
def get_humList(buffer,keys):
    return [ v[9] for k,v in buffer.items() if k in keys]

# RETURN AVEREGE HUMIDIDY TODAY
def get_humAvg(buffer,keys):
    # Get list of humidity
    humidity = get_humList(buffer, keys)
    # Return max temperature
    return statistics.mean(humidity) 

# RETURN LIST OF WIND BY DAY
def get_windList(buffer,keys):
    return [ v[10] for k,v in buffer.items() if k in keys]

# RETURN AVEREGE WIND TODAY
def get_windAvg(buffer,keys):
    # Get list of pressures
    winds = get_windList(buffer, keys)
    # Return max temperature
    return statistics.mean(winds) 

# RETURN LIST OF WEATHER DESCRIPTION BY DAY
def get_weatherDict(buffer,keys):
    return [ f"{v[3]};{v[4]}" for k,v in buffer.items() if k in keys]

# RETURN TOP 1 MOST COMMON WEATHER DESCRIPTION
def get_weatherCounter(buffer,keys):
    
    # Get list of description
    weathers = get_weatherDict(buffer, keys)
    # Get Counter
    countResult = Counter(weathers)
    # Obtain top 1 most_common description
    result = countResult.most_common(1)

    # Return two values
    return result[0][0].strip().split(';') 

# RETURN LIST OF POLLUTION AIR QUALITY BY DAY
def get_airQualityDict(buffer,keys):
    return [ v[3] for k,v in buffer.items() if k in keys]

# RETURN TOP 1 MOST COMMON AIR QUEALITY
def get_pollutionCounter(buffer,keys):
    
    # Get list of description
    qualities = get_airQualityDict(buffer, keys)
    # Get Counter
    countResult = Counter(qualities)
    # Obtain top 1 most_common description
    result = countResult.most_common(1)

    # Return two values
    return result[0][0]


## - END GROUP AGGREGATION SECTION

# RETURN DICT OF DATESTAMP -> DATETIME TRANSALE BY CITY
def get_dtTransalor_weatherCity(fcWeather):   
    
    # Get DATETIME and DATE lists
    dtFormated = [*map(datetime.fromtimestamp,fcWeather.keys())]
    dFormated  = [*map(datetime.date,dtFormated)]
    # Create a tuple lists
    dtTuple = list(zip(dFormated,dtFormated))

    # Create a dict
    dtDict_translate = dict(zip(fcWeather.keys(),dtTuple))

    return dtDict_translate

# RETURN LIST OF DAYS
def get_days(dictDT):
    
    # Days List    
    days = []
    
    # Get prety Date 
    for v in dictDT.values():
        
        dt = v[0]
        days.append(dt)
    
    return list(dict.fromkeys(days))

## POLLUTION SECTION

# RETURN A LIST OF CITIES LOAD IN FORECAST BUFFER
def get_bufferPollution_cities():
    return esql.get_cities_buffer_pollution()

# RETURN DICT OF FC WEATHER AND TRANSALTE DATETIME DICT
def get_PollutionDict():
    
    # dict where will host the results
    result = {}
    # get list of data cities
    cities = get_bufferPollution_cities()
    
    # loop cities to get FC data
    for city in cities:
        
        cty = str(city[0])
        
        results = esql.get_dataCity_buffer_pollution(cty)
        print(results)
        # create dict with datetimes as keys index number 4
        a = {value[4]: value for value in results}
        # create ditct by city
        b = {cty:a}
        
        # add dict into results dict
        result = {**result, **b}
        
    return result

## - END POLLUTION SECTION

## DATA STR SECTION

# RETURN DATE INTO STR FORMAT
def get_str_date(dateType):
    return dateType.strftime("%d/%m/%Y")

# RETURN DATE INTO DAY OF WEEK STR FORMAT
def get_str_dayWeek(dateType):
    return dateType.strftime('%A')

# RETURN HOUR INTO STR FORMAT
def get_str_hour(intDate):
    dateType = datetime.fromtimestamp(intDate)
    return dateType.strftime("%Hh")

# RETURN DICT TRANLATE KEYS
def get_daykeys(dictDT,dateData):
    
    keys = [k for k, v in dictDT.items() if v[0] == dateData]
    
    return keys
    
## - END DATA STR SECTION