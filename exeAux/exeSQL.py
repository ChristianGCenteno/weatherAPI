'''
Module Aux to exe the SQL SELECT interaction
'''
import weatherApi.SQLiteManagment.SqLiteAdapter as sqlAdapter

## COLUMNS SECTION

#Default Weather Columns to SELECT
columnsWeather = ['city','country','latitude','longitude','mainDesc','description'
                 ,'temperature','thermal_feeling','temp_min','temp_max','presure'
                 ,'humidity','visibility','wind_speed','wind_gust','rain','snow'
                 ,'cloudiness','sunrise','sunset']

#Default Pollution Columns to SELECT
columnsPollution = ['city','country','latitude','longitude','air_quality','air_co'
                   ,'air_no','air_no2','air_o3','air_so2','air_pm2_5','air_pm10'
                   ,'air_nh3']

#Default ForeCast Weather Columns to SELECT
columnsFcWeather = ['id','city','country','mainDesc','description','temperature','temp_min'
                   ,'temp_max','presure','humidity','wind_speed','rain','snow','dt']

#Default ForeCast Pollution Columns to SELECT
columnsFcPollution = ['Id','city','country','air_quality','dt']

## END - COLUMNS SECTION


#Return weather table info
def get_listWeather(columns,clasules=[],orderBy=[],limit=0,show=0):
    listResult = sqlAdapter.sqlSelect('weather',columns,clasules,orderBy,limit,show)
    return listResult

#Return the weather fields of each row to display in the main map
def check_listWeather():
    listResult = get_listWeather(columnsWeather)
    return listResult

#Return the last datatime weather
def show_lastdateWeather_NL():
    return show_lastdateWeather('NL')

#Return the last datatime for NL
def show_lastdateWeather(code):
    listResult = sqlAdapter.sqlSelect('weather',['MAX(dt)'],[['country','=',f"'{code}'"]],limit=1)
    return listResult[0]

#Get IdCountry code to 'INNER'
def get_countryCode(cc='NL'):
    return sqlAdapter.sqlSelect('cat_country', columns=['id'], clasules=[['value','=',"'" + cc + "'"]],limit=1)

#RETURN CITIES LIST
def get_cities(idCountry):
    return sqlAdapter.sqlSelect('cities',['name',"'NL'"],[['countryCode','=',str(idCountry)]])

#Return the NL cities list
def show_cities_NL():

    idCountry = get_countryCode('NL')
    idCountry = idCountry[0][0]
    
    listResult = get_cities(idCountry)

    return listResult

#RETURN LAST WEATHER CITY
def show_currentWeatherCity(city,country):
    return sqlAdapter.sqlSelect('weather',columnsWeather, [['city','=',"'"+str(city)+"'"],['country','=',"'"+str(country)+"'"]], orderBy=[['dt','DESC']], limit=1)

#RETURN LAST WEATHER CITY BY ID
def show_currentWeatherCityById(id_row):
    return sqlAdapter.sqlSelect('weather',columnsWeather, [['id','=',"'"+str(id_row)+"'"]], orderBy=[['dt','DESC']], limit=1)

#Return the last datatime pollution for NL
def show_lastdatePollution(code):
    listResult = sqlAdapter.sqlSelect('pollution',['MAX(dt)'],[['country','=',f"'{code}'"]],limit=1)
    return listResult[0]

#Return the last datatime pollution for NL
def show_lastdatePollution_NL():
    return show_lastdatePollution('NL')

#GET LIST OF LAST WEATHER DATA IN NL
def show_lastWeather_NL():
    return show_lastWeather('NL')

#DISCLAIMER: IS A TOO SPECIFIC FUNCTION SO THE SQLtxt IT'S HANDMANDDE
def show_lastWeather(countryCode):

    query = f'''
        SELECT w.city,w.country,w.latitude,w.longitude,w.mainDesc,w.description
            ,w.temperature,w.thermal_feeling,w.temp_min,w.temp_max,w.presure
            ,w.humidity,w.visibility,w.wind_speed,w.wind_gust,w.rain,w.snow
            ,w.cloudiness,w.sunrise,w.sunset
          FROM weather w
         INNER JOIN (
                    SELECT city, MAX(dt) AS date
                      FROM weather
                     WHERE country = '{countryCode}'
                     GROUP BY city
                    ) last
            ON w.city = last.city 
           AND w.dt = last.date;
        '''
    
    return sqlAdapter.sql_execute(query)

#RETURN LAST POLLUTION CITY BY ID
def show_currentPollutionCityById(id_row):
    return sqlAdapter.sqlSelect('pollution',columnsPollution, [['id','=',"'"+str(id_row)+"'"]], orderBy=[['dt','DESC']], limit=1)

#GET LIST OF LAST POLLUTION DATA IN NL
def show_lastPollution_NL():
    return show_lastPollution('NL')

#DISCLAIMER: IS A TOO SPECIFIC FUNCTION SO THE SQLtxt IT'S HANDMANDDE
def show_lastPollution(countryCode):

    query = f'''
        SELECT p.city,p.country,p.latitude,p.longitude,p.air_quality,p.air_co,p.air_no,p.air_no2,p.air_o3,p.air_so2
              ,p.air_pm2_5,p.air_pm10,p.air_nh3
          FROM pollution p
         INNER JOIN (
                    SELECT city, MAX(dt) AS date
                      FROM pollution
                     WHERE country = '{countryCode}'
                     GROUP BY city
                    ) last
            ON p.city = last.city 
           AND p.dt = last.date;
        '''
    
    return sqlAdapter.sql_execute(query)

# FORECAST SECTION

#DISCLAIMER: IS A TOO SPECIFIC FUNCTION SO THE SQLtxt IT'S HANDMANDDE
#CREATE BUFFER VIEW OF FC_WEATHER
def create_buffer_weather():
    
    query = '''
        CREATE VIEW IF NOT EXISTS
          vw_buffer_fcWeather
        AS
          SELECT id,city,country,mainDesc,description,temperature,temp_min,temp_max,presure,humidity,wind_speed,rain,snow,dt
          FROM (
                SELECT last.Mid,(ROW_NUMBER() OVER (PARTITION BY w.city ORDER BY w.id DESC)) AS gid,w.*
                FROM fc_weather w
                INNER JOIN (
                            SELECT 
                              MAX(id) as Mid
                             ,city
                            FROM
                              fc_weather 
                            GROUP BY
                              city
                           ) last
                ON w.city = last.city
                WHERE 
                  strftime('%Y%m%d',datetime(w.dt, 'unixepoch')) >= strftime('%Y%m%d',datetime())
                ) subq
        WHERE 
          gid <= 40
        ORDER BY
          Mid DESC
         ,dt ASC
        ;
    '''
    
    return sqlAdapter.sql_execute(query)
    
# GET CITIES LIST IN BUFFER
def get_cities_buffer_weather():
    return sqlAdapter.sql_execute('SELECT DISTINCT city FROM vw_buffer_fcWeather;')

# GET DATA FORECAST WEATHER BY CITY NAME
def get_dataCity_buffer_weather(city):
    return sqlAdapter.sqlSelect('vw_buffer_fcWeather',columnsFcWeather, [['city','=',"'"+str(city)+"'"]])

# CLEAN DATA FORECAST WEATHER
def clean_cities_buffer_weather():
    sqlAdapter.sql_execute('DELETE FROM fc_weather;')

#DISCLAIMER: IS A TOO SPECIFIC FUNCTION SO THE SQLtxt IT'S HANDMANDDE
#CREATE BUFFER VIEW OF FC_POLLUTION
def create_buffer_pollution():
    
    query = '''
        CREATE VIEW IF NOT EXISTS
          vw_buffer_fcPollution
        AS
          SELECT id,city,country,air_quality,dt
          FROM (
                SELECT last.Mid,(ROW_NUMBER() OVER (PARTITION BY p.city ORDER BY p.id DESC)) AS gid,p.*
                FROM fc_pollution p
                INNER JOIN (
                            SELECT 
                              MAX(id) as Mid
                             ,city
                            FROM
                              fc_pollution 
                            GROUP BY
                              city
                           ) last
                ON p.city = last.city
                WHERE 
                  strftime('%Y%m%d',datetime(p.dt, 'unixepoch')) >= strftime('%Y%m%d',datetime())
                ) subq
            WHERE 
              gid <= 96
            ORDER BY
              Mid DESC
             ,dt ASC
        ;
    '''
    
    return sqlAdapter.sql_execute(query)

# GET CITIES LIST IN BUFFER
def get_cities_buffer_pollution():
    return sqlAdapter.sql_execute('SELECT DISTINCT city FROM vw_buffer_fcPollution;')

# GET DATA FORECAST POLLUTION BY CITY NAME
def get_dataCity_buffer_pollution(city):
    return sqlAdapter.sqlSelect('vw_buffer_fcPollution',columnsFcPollution, [['city','=',"'"+str(city)+"'"]])

# CLEAN DATA FORECAST POLLUTION
def clean_cities_buffer_pollution():
    sqlAdapter.sql_execute('DELETE FROM fc_pollution;')
