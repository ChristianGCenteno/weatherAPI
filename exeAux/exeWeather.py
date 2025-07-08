'''
Module Aux to exe the weather and polution load
'''
import weatherApi.apiTools.ApiAdapter                 as apiAdapter
import weatherApi.SQLiteManagment.SqLiteAdapter       as sqlAdapter

#MAIN LOAD API REQUEST INTO SQLITE
def load_api_db(tableName,values,columns,types):
    
    declareCol   = []
    declareFk    = []
    rowsToInsert = []
    
    #Create Table if not exist
    for i,v in enumerate(columns):
        declare = [str(v),str(types[i]),"",""]
        declareCol.append(declare)
    
    #SQL CREATE
    sqlAdapter.sqlCreate(tableName,declareCol,declareFk)
    
    #Insert Values
    for value in values:
        v = list(map(str,value))
        rowsToInsert.append(v)
    
    #INSERT ROWS
    return_id = sqlAdapter.sqlInsert(tableName,columns,rowsToInsert)
    
    #SELECT TEST
    sqlAdapter.sqlSelect(tableName, ["*"])
    
    return return_id

#LOAD CURRENT WEATHER BY IP
def load_weather_ip():
    l,c,t = apiAdapter.get_weather_ip()
    return load_api_db('weather', l,c,t)
    
#LOAD CURRENT WEATHER BY LIST OF CITIES
def load_weather_lcities(listCities):
    l,c,t = apiAdapter.get_weather_cities(listCities)
    return load_api_db('weather', l,c,t)
    
#LOAD FORECAST WEATHER BY CITY
def load_fcweather_city(city):
    l,c,t = apiAdapter.get_fcWeather_city(city)
    return load_api_db('fc_weather', l,c,t)

#LOAD FORECAST WEATHER BY ZIP
def load_fcweather_zip(zipCode,country):
    l,c,t = apiAdapter.get_fcWeather_zip(zipCode,country)
    return load_api_db('fc_weather', l,c,t)

#LOAD CURRENT POLLUTION BY CITY
def load_pollution_city(city):
    l,c,t = apiAdapter.get_pollution_city(city)
    return load_api_db('pollution',l,c,t)

#LOAD CURRENT POLLUTION BY ZIP
def load_pollution_zip(zipcode,countryCode):
    l,c,t = apiAdapter.get_pollution_zip(zipcode,countryCode)
    return load_api_db('pollution',l,c,t)
    
#LOAD FORECAST POLLUTION BY CITY
def load_fcpollution_city(city):
    l,c,t = apiAdapter.get_pollution_city(city,1)
    return load_api_db('fc_pollution',l,c,t)

#LOAD FORECAST POLLUTION BY ZIP
def load_fcpollution_zip(zipcode,countryCode):
    l,c,t = apiAdapter.get_pollution_zip(zipcode,countryCode,1)
    return load_api_db('fc_pollution',l,c,t)


'''
# EXAMPLES
load_weather_ip() 
load_weather_lcities([['Leeuwarden','NL'],['Toledo','ES']])
load_fcweather_city('Camminghaburen')
load_fcweather_zip('8926LS','NL')

load_pollution_city('Camminghaburen')
load_fcpollution_city('Camminghaburen')

load_pollution_zip('45005','ES')
load_fcpollution_zip('45005','ES')
'''