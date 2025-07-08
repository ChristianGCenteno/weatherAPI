'''
CLASS CREATE DEM & POP MAP
'''
from weatherApi.userInterface.map_builder import MapBuilder

#CLASS TO DEM MAP
class MapDEMBuilder(MapBuilder):
    
    def __init__(self,country='NL'):
        
        #GET VALUES OF THE MAIN CLASS
        super().__init__()
        #VALUES TO CHANGE
        self.typeMap      = 'dem'
        self.txtScale     = 'Altitude'
        self.htmlName     = 'demMap' + str(country) + '.html'
        #SET MAXIMUN COLOR SCALE
        self.change_maxScale(30)
    
#CLASS TO POPULATION MAP
class MapPOPBuilder(MapBuilder):
    
    def __init__(self,country='NL'):
        
        #GET VALUES OF THE MAIN CLASS
        super().__init__()
        #VALUES TO CHANGE
        self.typeMap      = 'population'
        self.txtScale     = 'Population'
        self.htmlName     = 'popMap' + str(country) + '.html'
        #SET MAXIMUN COLOR SCALE
        self.change_maxScale(100000)

'''
import os
import folium
from pandas import read_csv
from branca.colormap import linear


class MapDEMBuilder:
    
    def __init__(self):
        
        self.csv_path     = os.path.abspath(os.path.join("..", "csv", "cities_complete.csv"))
        self.geojson_path = os.path.abspath(os.path.join("..", "resources", "geojson", "georef-netherlands-gemeente@public.geojson"))
        self.output_path  = os.path.abspath("demMap.html")
        self.country_dict = {}
        self.colormap     = None
        
    #Procedure to determined the value of the city color
    def get_color(self,feature):
        try:
            name  = feature["properties"]["gem_name"][0]
            value = self.country_dict.get(name)
            return self.colormap(value)
        except KeyError:
            return 'black'
    
    #Constructor DEM map
    def build(self):
        
        #LOAD CSV
        df                = read_csv(self.csv_path, sep=';', decimal='.', index_col='id', encoding='utf-8')
        self.country_dict = df.set_index("name")["dem"]
        self.colormap     = linear.RdYlGn_05.scale(df.dem.min(), 30)
        
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
            popup=folium.GeoJsonPopup(fields=["gem_name"], labels=False)
        ).add_to(m)
        
        self.colormap.caption = "Altitude color scale"
        self.colormap.add_to(m)
        
        m.save(self.output_path)
        
        return self.output_path        
'''

'''
#Procedure to determined the value of the city color
def get_color(feature):
    try:
        name = feature["properties"]["gem_name"][0]
        return colormap(country_dict[name])
    except KeyError:
        return 'black'


currentPath  = os.getcwd()
resourcePath = os.path.join(currentPath,'..')
resourcePath = os.path.join(resourcePath,'resources')
resourcePath = os.path.join(resourcePath,'geojson')
geojsonPath  = os.path.join(resourcePath,'georef-netherlands-gemeente@public.geojson')


#Path
path = os.path.join(os.getcwd(),"..")
path = os.path.join(path,'csv')
        
#Read the csv file
csvPath = os.path.join(path,'cities_complete.csv')
dfCsv   = read_csv(csvPath,sep=';',decimal='.',index_col='id')

#Create a linear color scale for the map
colormap = linear.RdYlGn_05.scale(
    dfCsv.dem.min(), 30
)

#Create a dict with the dem value using the name city like index
country_dict = dfCsv.set_index("name")["dem"]

#Set the popup value without labels
popup = folium.GeoJsonPopup(fields=["gem_name"],labels=False)

#Create the map object focus in The Netherlands. With a simple looks
m = folium.Map(location=[52.1326, 5.2913], zoom_start=7,tiles='cartodb positron')

#Create a folium GeoJson using de public Netherlands GeoJson file
folium.GeoJson(geojsonPath,zoom_on_click=False
              ,style_function= lambda feature: {

                  "fillColor": get_color(feature),
                  "color": "black",
                  "weight": 1,
                  "dashArray": "5, 5",
            },
              popup = popup
              ).add_to(m)

colormap.caption = "Altitude color scale"
colormap.add_to(m)

# Guarda el mapa en un archivo HTML
m.save('demMap.html')

# Abre el mapa en el navegador

webbrowser.open('demMap.html')
'''
        

        
        
'''
import webbrowser
import os
import folium
from pandas import read_csv
from branca.colormap import linear


class MapPOPBuilder:
    
    def __init__(self):
        
        self.csv_path     = os.path.abspath(os.path.join("..", "csv", "cities_complete.csv"))
        self.geojson_path = os.path.abspath(os.path.join("..", "resources", "geojson", "georef-netherlands-gemeente@public.geojson"))
        self.output_path  = os.path.abspath("popMap.html")
        self.country_dict = {}
        self.colormap     = None
        
    #Procedure to determined the value of the city color
    def get_color(self,feature):
        try:
            name  = feature["properties"]["gem_name"][0]
            value = self.country_dict.get(name)
            return self.colormap(value)
        except KeyError:
            return 'black'
    
    #Constructor POP map
    def build(self):
        
        #LOAD CSV
        df                = read_csv(self.csv_path, sep=';', decimal='.', index_col='id', encoding='utf-8')
        self.country_dict = df.set_index("name")["population"]
        self.colormap     = linear.RdYlGn_05.scale(df.population.min(), 100000)
        
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
            popup=folium.GeoJsonPopup(fields=["gem_name"], labels=False)
        ).add_to(m)
        
        self.colormap.caption = "Population color scale"
        self.colormap.add_to(m)
        
        m.save(self.output_path)
        webbrowser.open(self.output_path)
        
        return self.output_path        

clase = MapPOPBuilder()
clase.build()
'''
