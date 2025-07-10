'''
CLASS CREATE WEATHER MAP
'''
import weatherApi.userInterface.icons_manager as icoM
import weatherApi.exeAux.exeSQL as esql
from weatherApi.userInterface.map_builder import MapBuilder

import os
from datetime import datetime
import folium
import branca
import base64

class MapWEATHERBuilder(MapBuilder):
    
    def __init__(self,country='NL'):
        
        super().__init__()
        self.wMap = None
        
        #VALUES TO CHANGE
        self.typeMap      = ''
        self.txtScale     = ''
        self.htmlName     = 'weatherMap' + str(country) + '.html'
        self.output_path  = os.path.abspath(self.htmlName)
        
        #Dict of comuns icons to incrust in HTML
        self.icons_base64 = {
            "sunrise": self.get_base64_image(os.path.join("..", "resources", "icons", "sunrise-and-up-arrow-16478.png")),
            "sunset" : self.get_base64_image(os.path.join("..", "resources", "icons", "sunset-and-down-arrow-16479.png")),
            "visibility" : self.get_base64_image(os.path.join("..", "resources", "icons", "visibility.png")),
            }
    
    #TRANSFORM IMAGES IN BASE64 TO INCRUST IN IFrame (WEATHER INFO)
    def get_base64_image(self,path):
        
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")
            
        return f"data:image/png;base64,{encoded}"
    
    def get_html(self,city,country,mDesc,desc,temp,tFeeling
            ,temp_min,temp_max,pres,hum,visi,wind_speed,wind_gust
            ,rain,snow,cloud,sunrise,sunset):
            
            #Translate into datetime
            sunrise,sunset = datetime.fromtimestamp(int(sunrise)),datetime.fromtimestamp(int(sunset))
            
            #Fields that no always exist
            
            auxrain = f'''
                       <table border="1" style="width:100%; border-collapse: collapse; text-align:center; background-color:#f9f9f9;">
                         <tr>
                           <th>RAIN</th>
                           <td>{rain} mm/h</td>
                         </tr>
                       </table>
                       <br>
            ''' if rain != 'No Record' else ''
            
            auxsnow = f'''
                       <table border="1" style="width:100%; border-collapse: collapse; text-align:center; background-color:#f9f9f9;">
                         <tr>
                           <th>SNOW</th>
                           <td>Snow {snow} mm/h</td>
                         </tr>
                       </table>
                       <br>
            ''' if snow != 'No Record' else ''
            
            auxguts = f'''
                       <tr>
                         <th>WIND GUST</th>
                         <td>{wind_gust} miles/hour</td>
                       </tr>
            ''' if wind_gust != 'No Record' else ''
            
            
            #GET ICO IN BASE64 DICT
            sunrise_ico = self.icons_base64['sunrise']
            sunset_ico  = self.icons_base64['sunset']
            visibility_ico = self.icons_base64['visibility']
            
            #HTML body
            txt=f'''
            
            <h3 style="text-align:center">{city} - {country}</h3>

            <table style="border:1px solid black; width:100%; background-color:#f9f9f9;">
              <tr>
                <th style="border:1px solid black">{mDesc}</th>
                <th style="border:1px solid black">{desc}</th>
              </tr>
            </table>
            <br>
            <table border="1" style="width:100%; border-collapse: collapse; text-align:center; background-color:#f9f9f9;">
              <tr>
                <th>CLOUDINESS</th>
                <td>{cloud}%</td>
              </tr>
              <tr>
                <th>
                  <img src="{visibility_ico}" width="19" height="19" alt="Sunrise" style="vertical-align:middle;">
                </th>
                <td>{visi} m</td>
              </tr>
            </table>
            <br>
            <table border="1" style="width:100%; border-collapse: collapse; text-align:center; background-color:#f9f9f9;">
              <tr>
                <th>TEMPERATURE</th>
                <th>T. MIN</th>
                <th>T. MAX</th>
              </tr>
              <tr>
                <td>{temp}ºC</td>
                <td style="color: blue;">{temp_min}ºC</td>
                <td style="color: red;">{temp_max}ºC</td>
              </tr>
              <tr>
                <th>REAL FEEL</th>
                <td colspan="2" style="color: green;">{tFeeling}ºC</td>
              </tr>
            </table>
              <br>
            {auxrain}
            {auxsnow}
            <table border="1" style="width:100%; border-collapse: collapse; text-align:center; background-color:#f9f9f9;">
              <tr>
                <th>PRESSURE</th>
                <td>{pres} hPa</td>
              </tr>
              <tr>
                <th>HUMIDITY</th>
                <td>{hum}%</td>
              </tr>
            </table>
            <br>
            <table border="1" style="width:100%; border-collapse: collapse; text-align:center; background-color:#f9f9f9;">
              <tr>
                <th>WIND SPEED</th>
                <td>{wind_speed} m/s</td>
              </tr>
              {auxguts}
            </table>
            <br>
            <table border="1" style="width:100%; border-collapse: collapse; text-align:center; background-color:#f9f9f9;">
              <tr>
                <th colspan="2">SUNLIGTH</th>
              </tr>
              <tr>
                <td colspan="1">
                  <img src="{sunrise_ico}" width="19" height="19" alt="Sunrise" style="vertical-align:middle;">
                  {sunrise.strftime('%H:%M:%S')}
                </td>
                <td colspan="1">
                  <img src="{sunset_ico}" width="19" height="19" alt="Sunrise" style="vertical-align:middle;">
                  {sunset.strftime('%H:%M:%S')}
                </td>
              </tr>
            </table>
            
            '''
            
            return txt
    
    #CONSTRUCTOR WEATHER MAP
    def build(self):
        
        if os.path.exists(self.output_path):
            os.remove(self.output_path)
            
        self.build_base_map()
        self.wMap.save(self.htmlName)
        
        return self.output_path
    
    #CONSTRUCTOR WEATHER MAP
    def build_base_map(self):
        
        self.wMap = folium.Map(location=self.location, zoom_start=8, tiles='cartodb positron')
        
        listResult = esql.show_lastWeather_NL()
        
        for (city,country,lat,lon,mDesc,desc,temp,tFeeling
            ,temp_min,temp_max,pres,hum,visi,wind_speed,wind_gust
            ,rain,snow,cloud,sunrise,sunset) in listResult:
            
            html = self.get_html(city,country,mDesc,desc,temp,tFeeling
                                ,temp_min,temp_max,pres,hum,visi,wind_speed,wind_gust
                                ,rain,snow,cloud,sunrise,sunset)
            
            iframe = branca.element.IFrame(html=html, width=350, height=350)
            popup = folium.Popup(iframe, max_width=350)
            lat_lon = [lat, lon]
            
            folium.Marker(
                lat_lon,
                tooltip=city,
                popup=popup,
                icon=folium.CustomIcon(icoM.get_weather_ico(mDesc, desc), icon_size=(25, 25), icon_anchor=(10, 10))
                ).add_to(self.wMap)   
                
    # ADD NEW MARK
    def addMark(self,id_row):
        
        # Get list of values by city
        listResult = esql.show_currentWeatherCityById(id_row)
        
        (city,country,lat, lon, mDesc, desc, temp, tFeeling,
         temp_min, temp_max, pres, hum, visi, wind_speed,
         wind_gust, rain, snow, cloud, sunrise, sunset) = listResult[0]
         
        
        lat_lon = [lat, lon]
        self.location = lat_lon
        
        # Build by 0 if the map don't exists yet
        if self.wMap is None:
            self.build_base_map()
        else:
            self.build_base_map()
            
        #print(listResult)
               
        # GET HTML body 
        html = self.get_html(city, country, mDesc, desc, temp, tFeeling,
                             temp_min, temp_max, pres, hum, visi, wind_speed,
                             wind_gust, rain, snow, cloud, sunrise, sunset)
         
        iframe = branca.element.IFrame(html=html, width=400, height=350)
        popup = folium.Popup(iframe, max_width=500)
        
        folium.Marker(
                      lat_lon,
                      tooltip=city,
                      popup=popup,
                      icon=folium.CustomIcon(icoM.get_weather_ico(mDesc, desc), icon_size=(35, 35), icon_anchor=(35, 35))
        ).add_to(self.wMap)
        
        self.wMap.save(self.htmlName)
        
        #self.wMap.fit_bounds(lat_lon)
        
        return self.output_path
    
    # REMOVE TEMPORAL MARKS
    def removeMarks(self):
        self.restart_location()
        self.build()
        return self.output_path
    
'''
            <h3>{city} - {country}</h3>
            <p>{mDesc}<br>
            {desc}<br>
            {auxrain2}
            {auxsnow2}
            {temp}ºC [feel-like {tFeeling}ºC]<br>
            [min]  {temp_min}ºC<br>
            [max]  {temp_max}ºC<br>
            Pressure {pres} hPa<br>
            Humidity {hum}%<br>
            Wind speed {wind_speed} m/s<br> 
            {auxguts2}
            Cloudiness {cloud}%<br>
            Visibility {visi} m<br>
            Sunligth {sunrise.strftime('%H:%M:%S')} // {sunset.strftime('%H:%M:%S')}<br>
            </p>
'''            