'''
CLASS CREATE POLLUTION MAP
'''
import weatherApi.userInterface.icons_manager as icoM
import weatherApi.exeAux.exeSQL as esql
from weatherApi.userInterface.map_builder import MapBuilder

import os
import folium
import branca
import base64

class MapPOLLUTIONBuilder(MapBuilder):
    
    def __init__(self,country='NL'):
        
        super().__init__()
        self.pMap = None
        
        #VALUES TO CHANGE
        self.typeMap      = ''
        self.txtScale     = ''
        self.htmlName     = 'pollutionMap' + str(country) + '.html'
        self.output_path  = os.path.abspath(self.htmlName)
        
        #Dict of comuns icons to incrust in HTML
        self.icons_base64 = {
            1: self.get_base64_image(os.path.join("..", "resources", "icons", "pollution_1.png")),
            2: self.get_base64_image(os.path.join("..", "resources", "icons", "pollution_2.png")),
            3: self.get_base64_image(os.path.join("..", "resources", "icons", "pollution_3.png")),
            4: self.get_base64_image(os.path.join("..", "resources", "icons", "pollution_4.png")),
            5: self.get_base64_image(os.path.join("..", "resources", "icons", "pollution_5.png"))
            }
    
    #TRANSFORM IMAGES IN BASE64 TO INCRUST IN IFrame (WEATHER INFO)
    def get_base64_image(self,path):
        
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")
            
        return f"data:image/png;base64,{encoded}"
    
    #RETURN COLORS OF LEVELS - SUPER SPAGUETTI
    def get_density_color(self,typo,value):
        
        if typo == 'CO':
            if -1 <= value < 4400:
                return f'<td style="color: #229954">{value}</td>'
            elif 4400 <= value < 9400:
                return f'<td style="color: #00FF00">{value}</td>'
            elif 9400 <= value < 12400:
                return f'<td style="color: #f1c40f">{value}</td>'
            elif 12400 <= value < 15400:
                return f'<td style="color: #f39c12">{value}</td>'
            elif value >= 15400:
                return f'<td style="color: #e74c3c">{value}</td>'
            else:
                return f'<td>{value}</td>'
        
        if typo == 'NO':
            if 0.1 <= value <= 100:
                return f'<td style="color: #229954">{value}</td>'
            elif 101 <= value <= 150 or 0.08 <= value <= 0.09:
                return f'<td style="color: #f1c40f">{value}</td>'
            elif 150 < value or value < 0.08:
                return f'<td style="color: #e74c3c">{value}</td>'
            else:
                return f'<td>{value}</td>'
            
        if typo == 'NO2':
            if 0 <= value < 40:
                return f'<td style="color: #229954">{value}</td>'
            elif 40 <= value < 70:
                return f'<td style="color: #00FF00">{value}</td>'
            elif 70 <= value < 150:
                return f'<td style="color: #f1c40f">{value}</td>'
            elif 150 <= value < 200:
                return f'<td style="color: #f39c12">{value}</td>'
            elif value >= 200:
                return f'<td style="color: #e74c3c">{value}</td>'
            else:
                return f'<td>{value}</td>'
            
        if typo == 'O3':
            if 0 <= value < 60:
                return f'<td style="color: #229954">{value}</td>'
            elif 60 <= value < 100:
                return f'<td style="color: #00FF00">{value}</td>'
            elif 100 <= value < 140:
                return f'<td style="color: #f1c40f">{value}</td>'
            elif 140 <= value < 180:
                return f'<td style="color: #f39c12">{value}</td>'
            elif value >= 180:
                return f'<td style="color: #e74c3c">{value}</td>'
            else:
                return f'<td>{value}</td>'
            
        if typo == 'SO2':
            if 0 <= value < 20:
                return f'<td style="color: #229954">{value}</td>'
            elif 20 <= value < 80:
                return f'<td style="color: #00FF00">{value}</td>'
            elif 80 <= value < 250:
                return f'<td style="color: #f1c40f">{value}</td>'
            elif 250 <= value < 350:
                return f'<td style="color: #f39c12">{value}</td>'
            elif value >= 350:
                return f'<td style="color: #e74c3c">{value}</td>'
            else:
                return f'<td>{value}</td>'
            
        if typo == 'NH3':
            if 0.1 <= value <= 200:
                return f'<td style="color: #229954">{value}</td>'
            elif 201 <= value <= 250 or 0.08 <= value <= 0.09:
                return f'<td style="color: #f1c40f">{value}</td>'
            elif 250 < value or value < 0.08:
                return f'<td style="color: #e74c3c">{value}</td>'
            else:
                return f'<td>{value}</td>'
            
        if typo == 'PM25':
            if 0 <= value < 10:
                return f'<td style="color: #229954">{value}</td>'
            elif 10 <= value < 25:
                return f'<td style="color: #00FF00">{value}</td>'
            elif 25 <= value < 50:
                return f'<td style="color: #f1c40f">{value}</td>'
            elif 50 <= value < 75:
                return f'<td style="color: #f39c12">{value}</td>'
            elif value >= 75:
                return f'<td style="color: #e74c3c">{value}</td>'
            else:
                return f'<td>{value}</td>'
        
        if typo == 'PM10':
            if 0 <= value < 20:
                return f'<td style="color: #229954">{value}</td>'
            elif 20 <= value < 50:
                return f'<td style="color: #00FF00">{value}</td>'
            elif 50 <= value < 100:
                return f'<td style="color: #f1c40f">{value}</td>'
            elif 100 <= value < 200:
                return f'<td style="color: #f39c12">{value}</td>'
            elif value >= 200:
                return f'<td style="color: #e74c3c">{value}</td>'
            else:
                return f'<td>{value}</td>'
            
        return f'<td>{value}</td>'
    
    def get_html(self,city,country,air_quality,air_co,air_no
            ,air_no2,air_o3,air_so2,air_pm2_5
            ,air_pm10,air_nh3):
        
        q_ico = self.icons_base64.get(air_quality, air_quality)
            
        co   = self.get_density_color('CO',air_co)
        no   = self.get_density_color('NO',air_no)
        no2  = self.get_density_color('NO2',air_no2)
        o3   = self.get_density_color('O3',air_o3)
        so2  = self.get_density_color('SO2',air_so2)
        nh3  = self.get_density_color('NH3',air_nh3)
        pm25 = self.get_density_color('PM25',air_pm2_5)
        pm10 = self.get_density_color('PM10',air_pm10)
            
        #HTML body
        txt=f'''
            
            <h3 style="text-align:center">{city} - {country}</h3>
            
            <table style="border:1px solid black; width:100%; background-color:#f9f9f9;">
              <tr>
                <th style="border:1px solid black">AIR QUALITY</th>
                <th style="border:1px solid black">
                  <img src="{q_ico}" width="19" height="19" alt="Sunrise" style="vertical-align:middle;">
                </th>
              </tr>
            </table>
            <br>
            <table border="1" style="width:100%; border-collapse: collapse; text-align:center; background-color:#f9f9f9;">
              <tr>
                <th>Carbon monoxide (CO)</th>
                {co}
              </tr>
              <tr>
                <th>Nitrogen monoxide (NO)</th>
                {no}
              </tr>
              <tr>
                <th>Nitrogen dioxide (NO2)</th>
                {no2}
              </tr>
              <tr>
                <th>Ozone (O3)</th>
                {o3}
              </tr>
              <tr>
                <th>Sulphur dioxide (SO2)</th>
                {so2}
              </tr>
              <tr>
                <th>Ammonia (NH3)</th>
                {nh3}
              </tr>
              <tr>
                <th>Particulates (PM_2.5)</th>
                {pm25}
              </tr>
              <tr>
                <th>Particulates (PM_10)</th>
                {pm10}
              </tr>
            </table>
            
            '''
            
        return txt
    
    
    #CONSTRUCTOR POLLUTION MAP
    def build(self):
        
        if os.path.exists(self.output_path):
            os.remove(self.output_path)
            
        self.build_base_map()
        self.pMap.save(self.htmlName)
        
        return self.output_path
    
    #CONSTRUCTOR POLLUTION MAP
    def build_base_map(self):    
          
        # STABLISH MAP
        self.pMap = folium.Map(location=self.location, zoom_start=8,tiles='cartodb positron')
        
        # CREATE CITIES MARKS
        listResult = esql.show_lastPollution_NL()
        
        for (city,country,lat,lon,air_quality,air_co,air_no
            ,air_no2,air_o3,air_so2,air_pm2_5
            ,air_pm10,air_nh3) in listResult:
            
            html = self.get_html(city,country,air_quality,air_co,air_no
            ,air_no2,air_o3,air_so2,air_pm2_5
            ,air_pm10,air_nh3)

            iframe = branca.element.IFrame(html=html,width=350, height=350) #width=220, height=305)
            popup  = folium.Popup(iframe, max_width=350) #max_width=220)
            
            lat_lon = [lat,lon]

            folium.Marker(
                lat_lon,
                tooltip = city,
                popup   = popup,
                icon    = folium.CustomIcon(icoM.get_pollution_ico(air_quality),icon_size=(35, 35),icon_anchor=(35, 35))
                ).add_to(self.pMap)                
                
        # SAVE HTML MAP
        self.pMap.save(self.htmlName)

        return self.output_path        
    
    # ADD NEW MARK
    def addMark(self,id_row):
        
        
        listResult = esql.show_currentPollutionCityById(id_row)
        
        (city,country,lat,lon,air_quality,air_co,air_no
        ,air_no2,air_o3,air_so2,air_pm2_5
        ,air_pm10,air_nh3) = listResult[0]
        
        lat_lon = [lat, lon]
        self.location = lat_lon
        
        # Build by 0 if the map don't exists yet
        if self.pMap is None:
            self.build_base_map()
        else:
            self.build_base_map()    
            
        # GET HTML body  
        html = self.get_html(city,country,air_quality,air_co,air_no
            ,air_no2,air_o3,air_so2,air_pm2_5
            ,air_pm10,air_nh3)

        iframe = branca.element.IFrame(html=html,width=350, height=350) #width=220, height=305)
        popup  = folium.Popup(iframe, max_width=350) #max_width=220)
        
        
        folium.Marker(
                      lat_lon,
                      tooltip=city,
                      popup=popup,
                      icon=folium.CustomIcon(icoM.get_pollution_ico(air_quality),icon_size=(35, 35),icon_anchor=(35, 35))
        ).add_to(self.pMap)
             
        self.pMap.save(self.htmlName)
        
        return self.output_path
    
    # REMOVE TEMPORAL MARKS
    def removeMarks(self):
        self.restart_location()
        self.build()
        return self.output_path
    
    