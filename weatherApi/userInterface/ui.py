'''
MAIN UI WEATHER WINDOWS
'''
import weatherApi.exceptionManager.exceptManager as exM
import weatherApi.exeAux.exeSQL as esql
import weatherApi.exeAux.exeWeather as eweather

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QTabWidget, QDialog
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys
import os


import weatherApi.userInterface.ui_aux as mk
import weatherApi.userInterface.loading_engine as le
from weatherApi.userInterface.weather_map_builder import MapWEATHERBuilder
from weatherApi.userInterface.pollution_map_builder import MapPOLLUTIONBuilder
from weatherApi.userInterface.static_map_builder import MapDEMBuilder,MapPOPBuilder

'''
eweather.load_fcweather_city('Leeuwarden')
eweather.load_fcweather_city('Drachten')
eweather.load_fcweather_city('Utrecht')
eweather.load_fcweather_city('Toledo')
'''

#FUNCTION THAT EXECUTE AND LOAD THE NL CITIES WEATHER
def updateWeather_NL():
    
    '''
    lCities= [['Camminghaburen','NL'],['Amsterdam','NL'],['Rotterdam','NL'],['Drachten','NL'],['Utrecht','NL'],['Zwolle','NL'],['Groningen','NL']]
    eweather.load_weather_lcities(lCities)
    '''
    data             = esql.show_cities_NL()
    result           = le.city_loop_weather(data)
    #Only to wait all the exec
    result_windowscz = result.exec_()

    
#FUNCTION THAT EXECUTE AND LOAD THE NL CITIES POLLUTION
def updatePolution_NL():
    
    '''
    lCities = [['Camminghaburen'],['Amsterdam'],['Rotterdam'],['Drachten'],['Utrecht'],['Zwolle'],['Groningen']]
    '''
    data             = esql.show_cities_NL()
    result           = le.city_loop_pollution(data)
    #Only to wait all the exec
    result_windowscz = result.exec_()
        
        
#FUNCTION THAT RETURN HELP ZIPCODE HELP
def get_helpzipcode():
    
    txt = '''HERE IS SOME EXAMPLES OF COUNTRY CODE
    
    NETHERLAND:\t NL
    SPAIN:\t ES
    ENGLAND:\t GB
    '''
    return txt
    

#CLASS OF THE MAIN UI WINDOW
class VentanaPrincipal(QWidget):
        
    def __init__(self):
        
        super().__init__()
        
        #TODO: CHECK IF DB EXIST. CASE TRUE -> CREATE "INSTALATOR DB"
        #updateWeather_NL()
        #updatePolution_NL()
        
        self.setWindowTitle("WEATHER APP")
        self.setGeometry(100, 100, 1000, 600)

        # MAIN LAYOUT VERTICAL
        main_layout = QVBoxLayout()

        # CREATE TABS
        self.tabs = QTabWidget()
        
        ## TAB 1: WEATHER MAP
        self.tab_map = mk.create_tab(self.tabs,'WEATHER MAP')
        
        ## TAB 2: FC WEATHER
        self.tab_fcW = mk.create_tab(self.tabs,'FC WEATHER')
        
        ## TAB 3: POLLUTION MAP
        self.tab_poll = mk.create_tab(self.tabs,'POLLUTION MAP')
        
        ## TAB 4: FC POLLUTION
        self.tab_fcP = mk.create_tab(self.tabs,'FC POLLUTION')
        
        ## TAB 5: MISCELLANEOUS
        self.tab_misc = mk.create_tab(self.tabs,'MISCELLANEOUS MAPS')
        
        # 1 - WEATHER MAP     
        
        ## LEFT BUTTONS   
        name_controls_w     = 'OPTIONS'
        button_show_toledo  = QPushButton('SHOW TOLEDO')
        button_add_markW    = QPushButton('ADD WEATHER MARK')
        button_marks_delteW = QPushButton('REMOVE TMP MARKS')
        
        listButtons_w      = [button_show_toledo,button_add_markW,button_marks_delteW]
        
        ## LEFT FOOTER BUTTON
        button_updateWea   = QPushButton("UPDATE MAP")
        lastDateWeater     = esql.show_lastdateWeather_NL()
        
        # RIGTH PANEL: WEATHER MAP
        self.browserWeather  = QWebEngineView()
        self.weather_builder = MapWEATHERBuilder()
        self.path_map        = self.weather_builder.get_map()
        
        ## BROWSE HTML
        self.browserWeather.setUrl(QUrl.fromLocalFile(os.path.abspath(self.path_map)))
        
        ## CREATE QHBoxLayout
        self.layout_weatherMap_total = mk.StandarLayoutBuilder(self.browserWeather, name_controls_w, listButtons_w, button_updateWea, lastDateWeater)        
          
        ##. ADD LOGIC BUTTONS
        button_updateWea.clicked.connect(self.update_WeatherMap)
        button_show_toledo.clicked.connect(lambda: self.add_weather_marker('Toledo', 'ES'))
        
        button_add_markW.clicked.connect(self.load_cityWeather)
        button_marks_delteW.clicked.connect(self.rmv_weather_marks)

        ## ADD AL THE LAYOUT TO THE MAP TAB
        self.tab_map.setLayout(self.layout_weatherMap_total)
        
        # 2 - FORECAST WEATHER
        
        ## LEFT BUTTONS   
        name_controls_fcw     = 'OPTIONS'
        button_add_markfcw    = QPushButton('ADD BY CITY')
        button_add_zipfcw     = QPushButton('ADD BY ZIPCODE')
        button_marks_deltefcw = QPushButton('REMOVE CITIES')
        
        listButtons_fcw       = [button_add_markfcw,button_add_zipfcw,button_marks_deltefcw]
        
        # RIGTH PANEL: PANEL DATA
        self.forecastPanel_weather = mk.ForecastWeatherLayout()
        
        self.PanelFCW = QWidget()
        self.PanelFCW.setLayout(self.forecastPanel_weather)
        
        ## CREATE QHBoxLayout
        self.layout_forecastW_total = mk.StandarLayoutBuilder(self.PanelFCW, name_controls_fcw, listButtons_fcw)    
        
        ##. ADD LOGIC BUTTONS
        button_add_markfcw.clicked.connect(self.load_cityFcWeather)
        button_add_zipfcw.clicked.connect(self.load_zipFcWeather)
        button_marks_deltefcw.clicked.connect(self.rmv_cityFcWeather)
        
        ## ADD AL THE LAYOUT TO THE FORECAST TAB
        self.tab_fcW.setLayout(self.layout_forecastW_total) 
        
        # 3 - POLLUTION TAB
        
        ## LEFT BUTTONS   
        name_controls_p     = 'OPTIONS'
        button_add_markP    = QPushButton('ADD POLLUTION MARK')
        button_marks_delteP = QPushButton('REMOVE TMP MARKS')
        
        listButtons_p      = [button_add_markP,button_marks_delteP]
        
        ## LEFT FOOTER BUTTON
        button_updatePol   = QPushButton("Update Map")
        lastDatePollution  = esql.show_lastdatePollution_NL() #TODO
        
        # RIGTH PANEL: WEATHER MAP
        self.browserPollution  = QWebEngineView()
        self.pollution_builder = MapPOLLUTIONBuilder()
        self.path_pollutionmap = self.pollution_builder.get_map()
        
        ## BROWSE HTML
        self.browserPollution.setUrl(QUrl.fromLocalFile(os.path.abspath(self.path_pollutionmap)))
        
        ## CREATE QHBoxLayout
        self.layout_pollution_total = mk.StandarLayoutBuilder(self.browserPollution, name_controls_p, listButtons_p, button_updatePol, lastDatePollution)      
        
        ##. ADD LOGIC TO UPDATE BUTTON
        button_add_markP.clicked.connect(self.load_cityPollution)
        button_marks_delteP.clicked.connect(self.rmv_pollution_marks)
        
        button_updatePol.clicked.connect(self.update_PollutionMap)

        ## ADD AL THE LAYOUT TO THE MAP TAB
        self.tab_poll.setLayout(self.layout_pollution_total)
        
        
        # 4 - FORECAST POLLUTION
        
        ## LEFT BUTTONS   
        name_controls_fcp     = 'OPTIONS'
        button_add_markfcp    = QPushButton('ADD BY CITY')
        button_add_zipfcp     = QPushButton('ADD BY ZIPCODE')
        button_marks_deltefcp = QPushButton('REMOVE CITIES')
        
        listButtons_fcp       = [button_add_markfcp,button_add_zipfcp,button_marks_deltefcp]
        
        # RIGTH PANEL: PANEL DATA
        self.forecastPanel_pollution = mk.ForecastPollutionLayout()
        
        self.PanelFCP = QWidget()
        self.PanelFCP.setLayout(self.forecastPanel_pollution)
        
        ## CREATE QHBoxLayout
        self.layout_forecastP_total = mk.StandarLayoutBuilder(self.PanelFCP, name_controls_fcp, listButtons_fcp)    
        
        ##. ADD LOGIC BUTTONS
        button_add_markfcp.clicked.connect(self.load_cityFcPollution)
        button_add_zipfcp.clicked.connect(self.load_zipFcPollution)
        button_marks_deltefcp.clicked.connect(self.rmv_cityFcPollution)
        
        ## ADD AL THE LAYOUT TO THE FORECAST TAB
        self.tab_fcP.setLayout(self.layout_forecastP_total) 
        
        # 5 - MISCELLANEOUS TAB
        
        ## LEFT BUTTONS
        name_controls_m = 'MAPS'
        button_dem_map  = QPushButton("SHOW DEM MAP")
        button_pop_map  = QPushButton("SHOW POPULATION MAP")
        listButtons_m   = [button_dem_map,button_pop_map]
        
        ## LEFT FOOTER BUTTON
        #button_update_dem = QPushButton("Update DEM")
        
        # RIGTH PANEL: MAP ENGINE
        self.dem_builder          = MapDEMBuilder()
        self.pop_builder          = MapPOPBuilder()
        
        ## PATHS MAPS
        self.path_dem             = self.dem_builder.get_map()
        self.path_pop             = self.pop_builder.get_map()
        
        ## ENGINE BROWSE
        self.browserMiscellaneous = QWebEngineView()
        
        ## BROWSE HTML (DEFAULT: DEM)
        self.browserMiscellaneous.setUrl(QUrl.fromLocalFile(os.path.abspath(self.path_dem)))
        
        ## CREATE QHBoxLayout
        self.layout_miscellaneous_total = mk.StandarLayoutBuilder(self.browserMiscellaneous, name_controls_m, listButtons_m) #, button_update_dem, lastDateWeater)
        
        ##. ADD LOGIC TO BUTTONS
        button_dem_map.clicked.connect(self.show_dem_map)
        button_pop_map.clicked.connect(self.show_pop_map)
        
        ##button_update_dem.clicked.connect(self.update_dem_map)
        
        ## ADD AL THE LAYOUT TO THE MAP TAB
        self.tab_misc.setLayout(self.layout_miscellaneous_total)
        
        # -- ADD TAB TO THE MAIN LAYOUT -- #
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    
    ## ~~~ LOGIC SEGMENT ~~~ ##
    
    # BTN LOGIG: LOAD NEW DATA AND REBUILD WEATHER MAP
    def update_WeatherMap(self):
        
        try:
            
            # RECHARGE THE WEATHER API
            updateWeather_NL()
            
            # RESTART MAP POSSITION
            self.weather_builder.restart_location()
            
            # UPDATE THE LABEL OF LAST DATE
            self.layout_weatherMap_total.update_dateLabel(esql.show_lastdateWeather_NL())

            # RECREATE AND RELOAD THE MAP
            self.weather_builder.build()
            self.browserWeather.setUrl(QUrl.fromLocalFile(os.path.abspath(self.path_map)))
            
        except Exception as e:
            print("ERROR UPDATING WEATHER MAP: ", e)
    
    
    # BTN LOGIG: LOAD NEW DATA AND REBUILD POLLUTION MAP
    def update_PollutionMap(self):
        
        try:
            
            # RECHARGE POLLUTION API
            updatePolution_NL()
            
            # RESTART MAP POSSITION
            self.pollution_builder.restart_location()
            
            # UPDATE THE LABEL OF LAST DATE
            self.layout_pollution_total.update_dateLabel(esql.show_lastdatePollution_NL())

            # RECREATE AND RELOAD THE MAP
            self.pollution_builder.build()
            self.browserPollution.setUrl(QUrl.fromLocalFile(os.path.abspath(self.path_pollutionmap)))
            
        except Exception as e:
            print("ERROR UPDATING POLLUTION MAP: ", e)
    
    # BTN LOGIC: ADD TEMPORAL WEATHER MAP
    def add_weather_marker(self,city,countryCode):
        
        try:
            
            #LOAD WEATHER INFO
            return_id = eweather.load_weather_lcities([[city,countryCode]])
            #ADD MARK INTO WEATHER MAP
            self.path_map = self.weather_builder.addMark(return_id)
            
            #REFRESH VIEW
            self.browserWeather.setUrl(QUrl.fromLocalFile(os.path.abspath(self.path_map)))
                    
        except exM.APIgetWeather as e:
            self.add_noticeWindows(str(e),f'Value/s incorrect.\n\n {city} - {countryCode} \n\n Please try again')    
        except Exception as e:
            self.add_noticeWindows('ALERT',str(e))
        
    # BTN LOGIC: REMOVE TEMPORAL WEATHER MAP
    def rmv_weather_marks(self):
        
        try:
            #REMOVE MARKS AND LOAD PATH
            self.path_map = self.weather_builder.removeMarks()
            #REFESH VIEW
            self.browserWeather.setUrl(QUrl.fromLocalFile(os.path.abspath(self.path_map))) 
        except Exception as e:
            print("ERROR REMOVING MARKS: ",e)
        
    # BTN LOGIC: ADD TEMPORAL POLLUTION MAP
    def add_pollution_marker(self,city):
                
        try:
            
            #LOAD POLLUTION INFO
            return_id = eweather.load_pollution_city(city)
            #ADD MARK INTO POLLUTION MAP
            self.path_pollutionmap = self.pollution_builder.addMark(return_id)
            
            #REFRESH VIEW
            self.browserPollution.setUrl(QUrl.fromLocalFile(os.path.abspath(self.path_pollutionmap)))
        
        except exM.APIgetLocation as e:
            self.add_noticeWindows(str(e),f'Value incorrect.\n\n {city} \n\n Please try again')
        except exM.APIgetPollution as e:
            self.add_noticeWindows(str(e),f'Value incorrect.\n\n {city} \n\n Please try again')    
        except Exception as e:
            self.add_noticeWindows('ALERT',str(e))  
            
    # BTN LOGIC: REMOVE TEMPORAL POLLUTION MAP
    def rmv_pollution_marks(self):
        
        try:
            #REMOVE MARKS AND LOAD PATH
            self.path_map = self.pollution_builder.removeMarks()
            #REFESH VIEW
            self.browserPollution.setUrl(QUrl.fromLocalFile(os.path.abspath(self.path_pollutionmap))) 
        except Exception as e:
            print("ERROR REMOVING MARKS: ",e)
        
    # BTN LOGIC: REMOVE FORECAST DATA
    def rmv_cityFcWeather(self):
        
        try:
            
            # DELETE DB FC WEATHER DATA
            esql.clean_cities_buffer_weather()
            
            #UPDATE FC PANEL
            self.recreate_fcWeather()

        except Exception as e:
            self.add_noticeWindows('ALERT',str(e)) 
            
            
    # BTN LOGIC: REMOVE FORECAST POLLUTION DATA
    def rmv_cityFcPollution(self):
        
        try:
            
            # DELETE DB FC WEATHER DATA
            esql.clean_cities_buffer_pollution()
            
            #UPDATE FC PANEL
            self.recreate_fcPollution()

        except Exception as e:
            self.add_noticeWindows('ALERT',str(e)) 
        
    # PROCEDURE TO MAKE A NOTICE WINDOWS   
    def add_noticeWindows(self,textName,textContainer):
        
        self.dwind = mk.StandarDialogWindow(textName,textContainer)
        self.dwind.show()
    
    # WINDOWS TO CREATE A TEMPORAL WEATHER MAP
    def load_cityWeather(self):
        
        title       = 'MARK WEATHER CITY'
        description = 'Please, include the City Name and Country Code that you want to mark in the map.'
        fields      = ['CITY NAME','COUNTRY CODE']
        helpTxt     = get_helpzipcode()
         
        windowscz = mk.IngestDialogWindow(title,description,fields,helpTxt)
        windowscz.show()
        
        result_windowscz = windowscz.exec_()
        
        if result_windowscz == QDialog.Accepted:
            
            #Get Values
            dic_results = windowscz.getResults()
            #Add Mark
            self.add_weather_marker(dic_results['city_name'],str(dic_results['country_code']).upper())
            #Update panel
            ####<<<<<<<<<<<<
    
    # REFRESH FORECAST WEATHER PANEL
    def recreate_fcWeather(self):
        ## DELETE LAST VERSION
        old_panel = self.forecastPanel_weather.parentWidget()
        self.PanelFCW.deleteLater()
        ## RE-CREATE OBJECTS
        self.PanelFCW = QWidget()
        self.forecastPanel_weather = mk.ForecastWeatherLayout()
        self.PanelFCW.setLayout(self.forecastPanel_weather)
        ## REPLACE PANEL LAYOUT
        self.layout_forecastW_total.replaceWidget(old_panel, self.PanelFCW)
        
    # REFRESH FORECAST POLLUTION PANEL
    def recreate_fcPollution(self):
        ## DELETE LAST VERSION
        old_panel = self.forecastPanel_pollution.parentWidget()
        self.PanelFCP.deleteLater()
        ## RE-CREATE OBJECTS
        self.PanelFCP = QWidget()
        self.forecastPanel_pollution = mk.ForecastPollutionLayout()
        self.PanelFCP.setLayout(self.forecastPanel_pollution)
        ## REPLACE PANEL LAYOUT
        self.layout_forecastP_total.replaceWidget(old_panel, self.PanelFCP)
    
    
    def load_cityFcWeather(self):
        self.load_cityFc(1)
        
    def load_cityFcPollution(self):    
        self.load_cityFc(2)
        
    def load_zipFcWeather(self):
        self.load_zipFc(1)
        
    def load_zipFcPollution(self):
        self.load_zipFc(2)
    
    
    # WINDOWS TO ADD A FORECAST [1 = WEATHER | 2 = POLLUTION]
    def load_cityFc(self,typeFc):
        
        # CREATE WINDOWS DATA INGEST
        title       = 'ADD FORECAST INFO'
        description = 'Please, include the City Name.'
        fields      = ['CITY']
            
        windowscz = mk.IngestDialogWindow(title,description,fields)
        windowscz.show()
            
        result_windowscz = windowscz.exec_()
            
        # EXECUTE LOGIC
        if result_windowscz == QDialog.Accepted:
                
            #Get Values
            dic_results = windowscz.getResults()
                
            if typeFc == 1:
                    
                #Load Info
                esql.create_buffer_weather()
                self.coreFcWeather_city(dic_results['city'])
                    
                #UPDATE FC PANEL
                self.recreate_fcWeather()
                    
            elif typeFc == 2:
                    
                #Load Info
                esql.create_buffer_pollution()
                self.coreFcPollution_city(dic_results['city'])
                    
                #UPDATE FC PANEL
                self.recreate_fcPollution()                   
                
            else:
                self.add_noticeWindows('ALERT','AN ERROR RAISE')
            

    # CORE TO GET FORECAST WEATHER BY CITY
    def coreFcWeather_city(self,city):
        try:
            eweather.load_fcweather_city(city)
        except exM.APIgetLocation as e:
            self.add_noticeWindows(str(e),f"Value incorrect.\n\n {city} \n\n Please try again")
        except Exception as e:
            self.add_noticeWindows('ALERT',str(e)) 

    # CORE TO GET FORECAST POLLUTION BY CITY
    def coreFcPollution_city(self,city):
        try:
            eweather.load_fcpollution_city(city)
        except exM.APIgetLocation as e:
            self.add_noticeWindows(str(e),f"Value incorrect.\n\n {city} \n\n Please try again")
        except Exception as e:
            self.add_noticeWindows('ALERT',str(e))   


    # CORE TO GET FORECAST WEATHER BY ZIP
    def coreFcWeather_zip(self,zip_code,country_code):
        try:
            eweather.load_fcweather_zip(zip_code,country_code)
        except exM.APIgetLocation as e:
            self.add_noticeWindows(str(e),f"Value incorrect.\n\n {zip_code} - {country_code} \n\n Please try again")
        except Exception as e:
            self.add_noticeWindows('ALERT',str(e)) 
    
    # CORE TO GET FORECAST POLLUTION BY ZIP
    def coreFcPollution_zip(self,zip_code,country_code):
        try:
            eweather.load_fcpollution_zip(zip_code,country_code)
        except exM.APIgetLocation as e:
            self.add_noticeWindows(str(e),f"Value incorrect.\n\n {zip_code} - {country_code} \n\n Please try again")
        except Exception as e:
            self.add_noticeWindows('ALERT',str(e))    


    # WINDOWS TO ADD A FORECAST [1 = WEATHER | 2 = POLLUTION] BY ZIP CODE
    def load_zipFc(self,typeFc):
            
        # CREATE WINDOWS DATA INGEST
        title       = 'ADD FORECAST INFO'
        description = 'Please, include the Zip Code and Country Code to get the forecast.'
        fields      = ['ZIP CODE','COUNTRY CODE']
        helpTxt     = get_helpzipcode()
            
        windowscz = mk.IngestDialogWindow(title,description,fields,helpTxt)
        windowscz.show()
            
        result_windowscz = windowscz.exec_()
            
        # EXECUTE LOGIC
        if result_windowscz == QDialog.Accepted:
                
            #Get Values
            dic_results = windowscz.getResults()
                
            if typeFc == 1:
                    
                #Load Info
                esql.create_buffer_weather()
                self.coreFcWeather_zip(dic_results['zip_code'],dic_results['country_code'])
                    
                #UPDATE FC PANEL
                self.recreate_fcWeather()
                    
            elif typeFc == 2:
                    
                #Load Info
                esql.create_buffer_pollution()
                self.coreFcPollution_zip(dic_results['zip_code'],dic_results['country_code'])
                
                #UPDATE FC PANEL
                self.recreate_fcPollution()   
                    
            else:
                self.add_noticeWindows('ALERT','AN ERROR RAISE')                             
                
    
    # WINDOWS TO CREATE A TEMPORAL POLLUTION MAP    
    def load_cityPollution(self):
        
        title       = 'MARK POLLUTION CITY'
        description = 'Please, include the City Name that you want to mark in the map.'
        fields      = ['CITY NAME']
         
        windowscz = mk.IngestDialogWindow(title,description,fields)
        windowscz.show()
        
        result_windowscz = windowscz.exec_()
        
        if result_windowscz == QDialog.Accepted:
            
            #Get Values
            dic_results = windowscz.getResults()
            #Add Mark
            self.add_pollution_marker(dic_results['city_name'])
        
    #TODO: format the windows (icons also)


    ##MISCELLANEOUS##
    
    # CHANGE VIEW TO DEM (ALTITUDE) MAP
    def show_dem_map(self):
        
        try:
            
            self.path_dem = self.dem_builder.get_map()
            self.browserMiscellaneous.setUrl(QUrl.fromLocalFile(os.path.abspath(self.path_dem)))
            
        except Exception as e:
            
            print("ERROR getting DEM map:", e)
            
    # CHANGE VIEW TO POPULATION MAP
    def show_pop_map(self):
        
        try:
            
            self.path_pop = self.pop_builder.get_map()
            self.browserMiscellaneous.setUrl(QUrl.fromLocalFile(os.path.abspath(self.path_pop)))
            
        except Exception as e:
            
            print("ERROR getting POP map:", e)
        
    # TODO: REMOVE WHERE NOT IT WILL NECESARY
    def update_dem_map(self):
        
        try:
            
            self.path_dem = self.dem_builder.build()
            self.browserMiscellaneous.setUrl(QUrl.fromLocalFile(os.path.abspath(self.path_dem)))
            
        except Exception as e:
            
            print("ERROR updating DEM map:", e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    #ventana.show()
    ventana.showMaximized()
    #ventana.showFullScreen()
    sys.exit(app.exec_())


#NXT TASKS
#TODO: RETHINK THE BUILDER MAP TO ADD THE MARKS LOGIC
#TODO: CREATE WIND MAP (WITH ORIENTATION)

