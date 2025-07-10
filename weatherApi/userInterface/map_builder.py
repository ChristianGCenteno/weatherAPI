'''
MAIN CLASS - CONSTRUCTOR HTML MAP
'''
import os
import json
import folium
from pandas import read_csv
from branca.colormap import linear

class MapBuilder:
    
    def __init__(self):
        
        #VALUES TO CHANGE
        self.typeMap      = ''
        self.txtScale     = ''
        self.htmlName     = ''
        
        #DEFAULT VALUES
        self.location     = [52.1326, 5.2913]
        self.csv_path     = os.path.abspath(os.path.join("..", "csv", "cities_complete.csv"))
        self.geojson_path = os.path.abspath(os.path.join("..", "resources", "geojson", "georef-netherlands-gemeente@public.geojson"))
        self.output_path  = os.path.abspath(self.htmlName)
        self.country_dict = {}
        self.colormap     = None
        self.scalemin     = 0
        self.scalemax     = 30
        
    #Procedure to determined the value of the city color
    def get_color(self,feature):
        try:
            name  = feature["properties"]["gem_name"][0]
            value = self.country_dict.get(name)
            
            if value is None:
                return 'black'
            
            return self.colormap(value)
            
        except KeyError:
            return 'black'
        
    #Procedure to change ranges
    def change_minScale(self,minimal):
        self.scalemin = minimal
    
    def change_maxScale(self,maximal):
        self.scalemax = maximal
        
    #Procedure to set the html map path
    def change_htmlPath(self):
        self.output_path = os.path.abspath(self.htmlName)
    
    #Procedure to restart location center map
    def restart_location(self):
        self.location = [52.1326, 5.2913]
    
    #Constructor DEM map
    def build(self):
        
        #LOAD CSV
        df = read_csv(self.csv_path, sep=';',decimal='.', index_col='id', encoding='utf-8')
        
        #LOAD GeoJSON AND GET NAMES
        with open(self.geojson_path, encoding='utf-8') as f:
            geojson_data = json.load(f)
            
        cities_names = {feature["properties"]["gem_name"][0] for feature in geojson_data["features"]}
        
        #CLEAN DF: ONLY THE CITIES NAMES THAT EXISTS IN GEOJSON
        df = df[df['name'].isin(cities_names)]
        
        #BUILD COLORMAP
        self.country_dict     = df.set_index("name")[self.typeMap]
        self.change_minScale(df.dem.min())
        self.colormap         = linear.RdYlGn_05.scale(self.scalemin, self.scalemax)
        self.colormap.caption = str(self.txtScale) + " color scale"
        self.output_path      = os.path.abspath(self.htmlName)
        
        #CREATE MAP
        m = folium.Map(location=[52.1326, 5.2913], zoom_start=7, tiles="cartodb positron")
        
        #ADD GEOJSON
        folium.GeoJson(
            self.geojson_path,
            zoom_on_click=False,
            style_function= lambda feature: {
                  "fillColor": self.get_color(feature),
                  "color": "black",
                  "weight": 1,
                  "dashArray": "5, 5",
            },
            #popup=folium.GeoJsonPopup(fields=["gem_name"], labels=False),
        ).add_to(m)
        
        self.colormap.add_to(m)
        
        #GENERATE MARKS
        for _, serie in df.iterrows():
            
            name  = serie['name']
            popup = self.typeMap + ": " + str(serie[self.typeMap])
            lat   = serie['latitude']
            lon   = serie['longitude']
            
            folium.Circle(
                location     = [lat, lon],
                radius       = 550,  #Meters
                color        = 'blue',
                fill         = True,
                fill_color   = 'blue',
                fill_opacity = 0.8,
                tooltip      = name,
                popup        = folium.Popup(popup,max_width=300)
            ).add_to(m)
            
        #SAVE HTML MAP
        m.save(self.htmlName)
        
        return self.output_path        
    
    #CHECK IF HTML EXISTS, IF NOT CREATE
    def get_map(self):
        
        #CHECK PATH
        self.change_htmlPath()
        self.output_path = os.path.abspath(self.htmlName)
        
        #CONTROL STATES
        if os.path.exists(self.output_path):
            #print(f"MAP: '{self.htmlName}' already exists. Returning..")
            return self.output_path
        else:
            #print(f"MAP: '{self.htmlName}' not exists. Building...")
            return self.build()

        '''
        marker_cluster = MarkerCluster().add_to(m)
            folium.CircleMarker(
                location=[lat, lon],
                radius=5,
                tooltip=tooltip,
                popup=str(popup),
                color='blue',
                fill=True,
                fill_opacity=0.7
            ).add_to(marker_cluster)
            
        '''