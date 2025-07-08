'''
MODULE TO CREATE STANDAR PyQt5
'''
import weatherApi.userInterface.icons_manager as icoM
import weatherApi.exeAux.exeForeCast          as eFc

import warnings
import os
import sys

from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton,QLabel,QDialog,QDialogButtonBox,QSizePolicy,QFrame,QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont,QIcon,QPixmap
from PyQt5.Qt import QLineEdit, QGroupBox,QGraphicsOpacityEffect


warnings.filterwarnings("ignore", category=DeprecationWarning)


#APPLY QFONT AN ALIGN CENTER
def set_boldAlign(PyQt5_object,check_align=False):
    # declare Font
    labelFont = QFont()
    # set bold font
    labelFont.setBold(True)
    PyQt5_object.setFont(labelFont)
    # Align Center (Optional)
    if check_align:
        PyQt5_object.setAlignment(Qt.AlignCenter)

#TRANSFORM OPACITY OBJECT
def set_Opacity(PyQt5_object,opacityNumber):
    # creating a opacity effect
    opacity_effect = QGraphicsOpacityEffect()
    # setting opacity level
    opacity_effect.setOpacity(opacityNumber)
    # adding opacity effect to the label
    PyQt5_object.setGraphicsEffect(opacity_effect)

#CREATE TAB AND ADD TO TABS WIDGET
def create_tab(tabs_Widget,tab_name):
    tab_map = QWidget()
    tabs_Widget.addTab(tab_map, tab_name)
    return tab_map

#CREATE PIX LABEL DEFAULT
def get_DEFAULT_labelPic(imgName,ObjName=None):
    
    #Set Pix Image and format
    pixImg     = QPixmap(icoM.get_static_ico(imgName))
    pixImg     = pixImg.scaled(20,20,Qt.KeepAspectRatio,Qt.SmoothTransformation)
    
    #Create Label and Atatch
    hIcon = QLabel()
    hIcon.setPixmap(pixImg)
    
    #Optional: put Object name
    if ObjName is not None:
        hIcon.setObjectName(ObjName)
        
    return hIcon

#CREATE PIX LABEL WEATHER
def get_WEATHER_labelPic(mDesc,desc,ObjName=None):
    
    #Set Pix Image and format
    pixImg     = QPixmap(icoM.get_weather_ico(mDesc,desc))
    pixImg     = pixImg.scaled(20,20,Qt.KeepAspectRatio,Qt.SmoothTransformation)
    
    #Create Label and Atatch
    hIcon = QLabel()
    hIcon.setPixmap(pixImg)
    
    #Optional: put Object name
    if ObjName is not None:
        hIcon.setObjectName(ObjName)
        
    return hIcon
    

#CREATE STRUCTURE
'''
|===============================|
| *LABEL * |                    |
| *BUTTON* |                    |
| *BUTTON* |                    |
| *...*    |       * MAP *      |
|          |                    |
| *Date L* |                    |
| *Upd Bu* |                    |
|===============================|
'''
class StandarLayoutBuilder(QHBoxLayout):
    
    def __init__(self,panel,labelControls='',lButtons=None,UpdButton=None,optLabel=None):
        
        super().__init__()
        
        #-Manual Var
        self.labelControls   = labelControls
        self.lButtons        = lButtons
        self.UpdButton       = UpdButton
        self.optLabel        = optLabel
        self.panel           = panel
        
        #-Standar Var
        self.layout_controls = QVBoxLayout()
        #self.layout_main     = QHBoxLayout(self)
        
        self.build()
        
        
    def build(self):
        
        # OPTIONAL ->SET LABEL LAYOUT
        if self.layout_controls != '':
            self.layout_controls.addWidget(QLabel(self.labelControls)) 
        
        # ADD BUTTONS IN THE LAYOUT CONTROL
        if self.lButtons:
            for button in self.lButtons:
                ##button.setStyleSheet("background-color: lightGray; color: black; padding:8px; border: 1px solid black; border-radius: 5px;")
                self.layout_controls.addWidget(button)
        
        # PUSH THE TO BACK
        self.layout_controls.addStretch()  
        
        # OPTIONAL -> BUTTON SUB-LAYOUT FOR BACK: (LABEL + BUTTON)
        if self.UpdButton is not None and self.optLabel and len(self.optLabel) > 0:
            
            layout_controls_bk = QVBoxLayout()
            
            # PLACE BUTTON SUB-LAYOUT
            
            ## SPACE BETWEEN ELEMENTS
            layout_controls_bk.setSpacing(2)
            
            ## NO MARGINS 
            layout_controls_bk.setContentsMargins(0, 0, 0, 0)
            
            # OPTIONAL LABEL DESCRIPTION
            if self.optLabel is not None:
                
                ## LABEL WITH THE LAST LOAD DATA
                lastDate        = str(datetime.fromtimestamp(self.optLabel[0]))
                self.label_date = QLabel(lastDate)
                
                #. APPLY BOLD FONT AND APLING
                set_boldAlign(self.label_date,True)
                
                #. APPLY BORDER AND CSS STYLE
                self.label_date.setStyleSheet("""
                QLabel {
                        border: 1px solid black;
                        padding: 2px;
                        margin: 0px;
                        background-color: #e0e0e0;
                        border-radius: 5px;
                    }
                """)
                
                # ADD ELEMENT
                layout_controls_bk.addWidget(self.label_date)
            
            ## ADD ELEMENT
            layout_controls_bk.addWidget(self.UpdButton)
            
            ## PUSH THE TO BACK
            self.layout_controls.addStretch()
            
            ## ADD THE SUB-LAYOUT INTO THE CONTOL LAYOUT
            self.layout_controls.addLayout(layout_controls_bk)
            
        # ADD PANELS AND ORGANICE HORIZONTAL
        self.addLayout(self.layout_controls, 1)  # LEFT COLUMNS
        self.addWidget(self.panel          , 8)  # RIGTH COLUMNS
                
        
    def update_dateLabel(self,optLabel):
        lastDate        = str(datetime.fromtimestamp(optLabel[0]))
        self.label_date.setText(lastDate)
        QApplication.processEvents()
        
        
#CREATE STRUCTURE
'''
|===============================|
|                               |
|           * TXT *             |
|                               |
|-------------------------------|
|      [*CLOSE BUTTON*]         |
|===============================|
'''
class StandarDialogWindow(QDialog):
    
    def __init__(self, title, txtContent):
        
        super().__init__()
        
        #INGEST VALUES
        self.title         = title
        self.txtContent    = txtContent
        
        #DEFAULT VARIABLES
        self.layout        = QVBoxLayout()
        self.widgetContent = QWidget()
        self.layoutContent = QVBoxLayout()
        self.widgetContent.setObjectName("mainWidget")
        #. Control mouse drag
        self._drag_pos     = None
        
        #CONSTRUCT OBJECT
        self.build()

    def build(self):
        
        # Set window title and size
        #self.setWindowTitle(self.title)
        #self.setFixedSize(300, 150)
        
        # Mask minimize, maximize and interrogation symbol
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)        
        
        # SET TITLE FROMAT
        self.title_bar = QLabel(self.title)
        set_boldAlign(self.title_bar,True)
        self.title_bar.setFixedHeight(30)
        
        # TITLE CSS STYLE
        self.title_bar.setStyleSheet("background-color: black; color: white; padding:8px; font-size: 18px;")
        
        # SET OPACITY
        set_Opacity(self.title_bar,0.7)

        # GIVE MOUSE COMPORTAMENT (MOVMENT)
        self.title_bar.setMouseTracking(True)
        self.title_bar.mousePressEvent   = self.title_bar_mouse_press
        self.title_bar.mouseMoveEvent    = self.title_bar_mouse_move
        self.title_bar.mouseReleaseEvent = self.title_bar_mouse_release
        
        # ADD TITLE INTO LAYOUT
        self.layout.addWidget(self.title_bar)
        
        # Add label with content
        self.placeholder = QLabel(self.txtContent)
        # Active text adjust
        self.placeholder.setWordWrap(True)
        # Set Bold Text and Align
        set_boldAlign(self.placeholder,True)
        # Allow vertical adjust 
        self.placeholder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        # Align text
        self.placeholder.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # Add text to layout
        self.layout.addWidget(self.placeholder)

        # Add exit button
        self.button_exit = QPushButton('CLOSE')
        self.button_exit.clicked.connect(self.close)
        self.layout.addWidget(self.button_exit)
        
        self.widgetContent.setLayout(self.layout)
        self.layoutContent.addWidget(self.widgetContent)
        
        # Set layout to the dialog
        self.setLayout(self.layoutContent)
        #border-radius: 10px;
        
        # Apply CSS Style
        self.setStyleSheet("""
        QDialog {
            background-color: MistyRose;
            border: 2px solid #888;
            border-radius: 10px;
        }
        
        QWidget#mainWidget {
            background-color: MistyRose;
            border: 2px solid black;
            border-radius: 15px;
        }

        QLabel {
            color: #333;
            font-size: 14px;
            padding: 10px;
            border-radius: 10px;
        }

        QPushButton {
            background-color: #005a9e;
            color: white;
            border-radius: 5px;
            padding: 4px 8px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: Azure;
            color: black;
        }

        QPushButton:pressed {
            background-color: #003d6b;
            color: white;
        }
        
        """)
    
    # PROCEDURES TO MOUSE CONTROL
    ## CALCULATE POSITION    
    def title_bar_mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    ## CALCULATE MOVEMNT
    def title_bar_mouse_move(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_pos:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()
    ## RESTART POSITION VALUE
    def title_bar_mouse_release(self, event):
        self._drag_pos = None
        event.accept()    
    
        
'''
|===============================|
| ----------------------------- |
| !         * TXT *           ! |
| !                           ! |
| ! *BOX TEXT WITH LABELS TO *! |
| !        * WRITE *          ! |
| !                           ! |
| ![OPT HELP] [*EXE*][*CLOSE*]! |
| ----------------------------- |
|===============================|
'''
class IngestDialogWindow(QDialog):
    
    def __init__(self, title, txtContent,listBox=None,optHelp=None):
        
        super().__init__()
        self.title      = title
        self.txtContent = txtContent
        self.listBox    = listBox
        self.optHelp    = optHelp
        self.dicValues  = {}

        self.layout = QVBoxLayout()
        
        self.build()

    def build(self):
        
        # Set window title and size
        self.setWindowTitle(self.title)
        self.setFixedSize(400, 300)
        
        # Create Group and group layout to organize
        groupb = QGroupBox()
        group_layout = QVBoxLayout()
        
        # Mask minimize, maximize and interrogation symbol
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        #self.setWindowFlags(Qt.FramelessWindowHint)
                
        # Add label with content
        self.placeholder = QLabel(self.txtContent)
        # Active text adjust
        self.placeholder.setWordWrap(True)
        
        # Permit vertical adjust 
        self.placeholder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        # Align text
        self.placeholder.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # Add text to layout
        group_layout.addWidget(self.placeholder)
        
        # Add Optional boxTexts
        if self.listBox:
            
            ## Layout to boxText - without margins
            boxText_layout = QVBoxLayout()
            boxText_layout.setSpacing(2)
            boxText_layout.setContentsMargins(0, 0, 0, 0)
            
            for e in self.listBox:
                labelName = QLabel(str(e))
                placeData = QLineEdit() 
                
                # Set Bold in labelName and Opacity in placeData
                set_boldAlign(labelName)
                set_boldAlign(placeData)
                
                # Set Object Name Label
                labelName.setObjectName('labelData')
                
                #Add in Dict
                self.dicValues[str(e).replace(' ', '_').lower()] = placeData
                
                #Add elements in layout
                boxText_layout.addWidget(labelName)
                boxText_layout.addWidget(placeData)
                
            ## Add layout to group
            group_layout.addLayout(boxText_layout)
        
        ## Same layout to buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # Add Optional help
        if self.optHelp is not None:
            
            self.helpbtn = QPushButton()
            self.helpbtn.setObjectName('helpButton')
            self.helpbtn.setIcon(QIcon(os.path.join('..', 'resources', 'icons', 'help.png')))
            # Determined width of button
            self.helpbtn.setFixedWidth(30)
            self.helpbtn.setFixedHeight(30)
            self.helpbtn.clicked.connect(self.openHelp)
            
            buttons_layout.addWidget(self.helpbtn)
        
        # Add Confirm button
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        
        # Connect Logic
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        # Move to Rigth
        buttons_layout.addStretch() 
        
        # AddButtons
        buttons_layout.addWidget(self.button_box)
        group_layout.addLayout(buttons_layout)
        
        # Assign layout to group box
        groupb.setLayout(group_layout)   
            
        self.layout.addWidget(groupb)
        
        # Set layout to the dialog
        self.setLayout(self.layout)
        
        self.setStyleSheet("""
        QDialog {
                  background-color: Azure;
        }
        QGroupBox {
                  border: 1px solid black;
        }
        QLabel {
                  font-size: 18px;
                  color: black;
        }
        QLabel#labelData {
                  font-size: 14px;
                  color: gray;
        }
        QLineEdit {
                  color: Coral;
        }
        QPushButton#helpButton {
                  background: transparent;
        }
        QPushButton:hover#helpButton {
                  background: transparent;
                  border: 1px solid gray;
                  border-radius: 15px;
        }
        """)

        
    # PROCEDURE TO OPEN A WINDOWS HELP
    def openHelp(self):
        
        valueText  = self.optHelp
        self.dwind = StandarDialogWindow('HELP',valueText)
        self.dwind.show()
            
    # PROCEDURE TU RETURN THE VALUES
    def getResults(self):
        print ({k: v.text() for k, v in self.dicValues.items()})
        return {k: v.text() for k, v in self.dicValues.items()}      
    

'''
|=====================|
| ------------------- |
| !  * MAIN ICON *  ! |
| !                 ! |
| ! [ DATAS LINES ] ! |
| ------------------- |
|                     |
| ------------------- |
| ! *ICON* [DATA L] ! |
| !                 ! |
| !       ...       ! |
| !                 ! |
| ------------------- |
|=====================|
'''
class CoreForecastWeatLayout(QVBoxLayout):
    
    def __init__(self,buffer_city,day,isFirst=False):
        
        super().__init__()
        
        #Dates
        self.buffer_city = buffer_city
        self.dates_city  = eFc.get_dtTransalor_weatherCity(self.buffer_city)
        self.day         = day
        self.isFirst     = isFirst
        
        #Main Frame
        self.main_frame     = QFrame()
        self.main_frame.setObjectName("mainFrame")
        
        #Header group
        self.header_frame   = QFrame()           
        self.main_frame.setObjectName("headerFrame")
        self.group_header   = QGroupBox()
        self.header_layout  = QVBoxLayout()
        
        #Details group
        self.details_frame  = QFrame()
        self.details_frame.setObjectName("detailFrame")
        self.group_details  = QGroupBox('HOURS')
        self.details_layout = QVBoxLayout()
        
        self.build()
        
    def build(self):
        
        # SET HOURS DATA
        hours = eFc.get_daykeys(self.dates_city,self.day)
                
        # GET FIRST HOUR
        raw_data = self.buffer_city[hours[0]]
        #['id','city','country','mainDesc','description','temperature','temp_min','temp_max','presure','humidity','wind_speed','rain','snow','dt']
        data = { 'mainDesc':raw_data[3], 'description':raw_data[4], 'temperature':raw_data[5]
               , 'temp_min':raw_data[6], 'temp_max':raw_data[7]   , 'presure':raw_data[8]
               , 'humidity':raw_data[9], 'wind_speed':raw_data[10], 'rain':raw_data[11] 
               , 'snow':raw_data[12]   , }
        
        
        # SET GROUPED HOURS VALORS (MIN-MAX,AVG)
        tMinimus = eFc.get_TempMin(self.buffer_city,hours)
        tMaximus = eFc.get_TempMax(self.buffer_city,hours)
        
        #. If is today, not sumarize, just the current values
        if self.isFirst:
            
            tempMean = data['temperature']
            weathDes = [data['mainDesc'],data['description']]
            presMean = data['presure']
            humMean  = data['humidity']
            windMean = data['wind_speed']
        
        #. Forecast type, sumarize
        else:
            
            tempMean = eFc.get_TempAvg(self.buffer_city,hours)
            weathDes = eFc.get_weatherCounter(self.buffer_city,hours)
            presMean = eFc.get_presAvg(self.buffer_city,hours)
            humMean  = eFc.get_humAvg(self.buffer_city,hours)
            windMean = eFc.get_windAvg(self.buffer_city,hours)
        
        # SET MARGINS
        self.header_layout.setContentsMargins(5, 15, 5, 5)
        
        #** 1 SEGMENT - LAYOUT TO HEADER PART **#
        header_labels_layout      = QVBoxLayout()
        header_labels_layout.setContentsMargins(5, 2, 5, 2)
        header_labels_layout.setSpacing(2)
        
        ##. CREATE ICONS LAYOUT AND ADD TO SEGMENT 
        header_icons_layout      = QVBoxLayout()
        header_icons_layout.setContentsMargins(0, 0, 0, 10)
        header_icons_layout.setSpacing(8)
        
        ## LABEL WITH THE LAST LOAD DATA
        label_date = QLabel(str(eFc.get_str_date(self.day)))
        # Add name to apply css
        label_date.setObjectName("mainDateLayout")
        #. APPLY BOLD FONT AND APLING
        set_boldAlign(label_date,True)
        ## LABEL WITH WEEKDAY
        self.group_header.setTitle(eFc.get_str_dayWeek(self.day))
        
        ## MAIN WEATHER IMG
        # Charge IMG
        pixImg = QPixmap(icoM.get_weather_ico(weathDes[0],weathDes[1]))
        
        # Check if img is found
        if pixImg.isNull():
            labelIcon_header = QLabel("Image not found")
        else:
            #Create img object class
            pixImg           = pixImg.scaled(100,100,Qt.KeepAspectRatio,Qt.SmoothTransformation)
            labelIcon_header = QLabel()
            #Load img into
            labelIcon_header.setPixmap(pixImg)
            
        #. Apply align Center
        labelIcon_header.setAlignment(Qt.AlignCenter)
        
        header_icons_layout.addWidget(label_date)
        header_icons_layout.addWidget(labelIcon_header)
        
        #. Add icons in header segment
        header_labels_layout.addLayout(header_icons_layout)
        
        ##. CREATE 4 LEVELS LABELS LAYOUT TO DATA HEADER
        
        ## LVL 1 - BIG TEMPERATURE - ONLY CURRENT DAY
        header_labels_lv1_layout  = QHBoxLayout()
        header_labels_lv1_layout.setAlignment(Qt.AlignCenter)
        
        # CHECK IF IS CURRENT DAY - PUT CURRENT TEMPERATURE
        # Data Labels
        hLabel_t    = QLabel(f"{tempMean:.1f}ºC")
        #. Apply Bold and big size
        labelFont = QFont()
        labelFont.setBold(True)
        labelFont.setPixelSize(20)
        hLabel_t.setFont(labelFont)
        #. Add labels to level 1
        header_labels_lv1_layout.addWidget(hLabel_t)
        
        ## LVL 2 - MAX/MIN TEMPERATURE
        header_labels_lv2_layout  = QHBoxLayout()
        header_labels_lv2_layout.setContentsMargins(0, 10, 0, 0)
        header_labels_lv2_layout.setAlignment(Qt.AlignCenter)
        
        # Temp Min
        hLabel_tMin = QLabel(f"{tMinimus:.1f}ºC")
        hLabel_tMin.setObjectName('tMinLabel')
        hIcon_tMin = get_DEFAULT_labelPic('tMin')
        
        #. Add labels to level 2 | First part
        header_labels_lv2_layout.addWidget(hIcon_tMin)
        header_labels_lv2_layout.addWidget(hLabel_tMin)
        
        # PUSH THE TO BACK
        header_labels_lv2_layout.addStretch()        
        
        # Temp Max
        hLabel_tMax = QLabel(f"{tMaximus:.1f}ºC")
        hLabel_tMax.setObjectName('tMaxLabel')
        hIcon_tMax = get_DEFAULT_labelPic('tMax')
        
        #. Add labels to level 2 | Second part
        header_labels_lv2_layout.addWidget(hIcon_tMax)
        header_labels_lv2_layout.addWidget(hLabel_tMax)

        ## LVL 3 - HUMIDITY AND PRESSURE
        header_labels_lv3_layout  = QHBoxLayout()
        header_labels_lv3_layout.setContentsMargins(0, 8, 0, 8)
        header_labels_lv3_layout.setAlignment(Qt.AlignCenter)
        
        # Humidity
        hLabel_hum  = QLabel(f"{humMean:.1f}%")
        hIcon_hum = get_DEFAULT_labelPic('humi')
        
        #. Add labels to level 3 | First part
        header_labels_lv3_layout.addWidget(hIcon_hum)
        header_labels_lv3_layout.addWidget(hLabel_hum)
        
        # PUSH THE TO BACK
        header_labels_lv3_layout.addStretch() 
        
        # Pressure
        hLabel_pres = QLabel(f"{presMean:.1f}")
        hIcon_pres = get_DEFAULT_labelPic('pres')
        
        #. Add labels to level 3 | Second part
        header_labels_lv3_layout.addWidget(hIcon_pres)
        header_labels_lv3_layout.addWidget(hLabel_pres)
        
        ## LVL 4 - WIND, RAIN AND SNOW
        header_labels_lv4_layout  = QHBoxLayout()
        header_labels_lv4_layout.setContentsMargins(0, 0, 0, 10)
        header_labels_lv4_layout.setAlignment(Qt.AlignCenter)
        
        hLabel_wspe = QLabel(f"{windMean:.1f} m/s")
        hIcon_wspe = get_DEFAULT_labelPic('wind')
        
        header_labels_lv4_layout.addWidget(hIcon_wspe)
        header_labels_lv4_layout.addWidget(hLabel_wspe) 
        
        # OPTIONALS DATA
        
        #. RAIN CASE
        if(data['rain']!='No Record'):
            
            # PUSH THE TO BACK
            header_labels_lv4_layout.addStretch()
            
            hIcon_rain  = get_DEFAULT_labelPic('rain')
            hLabel_rain = QLabel(str(data['rain']))
            header_labels_lv4_layout.addWidget(hIcon_rain)
            header_labels_lv4_layout.addWidget(hLabel_rain)
                
        elif(data['snow']!='No Record'):
            
            # PUSH THE TO BACK
            header_labels_lv4_layout.addStretch()
            
            hIcon_snow  = get_DEFAULT_labelPic('snow')
            hLabel_snow = QLabel(str(data['snow']))
            header_labels_lv4_layout.addWidget(hIcon_snow)
            header_labels_lv4_layout.addWidget(hLabel_snow)
        
        #. Add levels in header layout
        header_labels_layout.addLayout(header_labels_lv1_layout)
        header_labels_layout.addLayout(header_labels_lv2_layout)
        header_labels_layout.addLayout(header_labels_lv3_layout)
        header_labels_layout.addLayout(header_labels_lv4_layout)
        
        #. Add layout into a frame
        self.header_frame.setLayout(header_labels_layout)
        self.header_layout.addWidget(self.header_frame)
        
        #. APPLY CSS STYLE
        self.header_frame.setStyleSheet("""
            QFrame {
                    border: 1.5px dashed black;
                    padding: 5px 15px;
                    margin: 1px;
                    border-radius: 10px;
                    background-color:Azure;
                    }
      
            QLabel {
                    border: 0px solid black;
                    padding: 0px 0px;
                    margin: 0px;
                    border-radius: 5px;
                    background-color: Azure;
                    }
            
            QLabel#mainDateLayout {
                    border: 1px solid black;
                    padding: 2px;
                    margin: 0px;
                    border-radius: 10px;
                    background-color: white;
                    }
                    
            QLabel#tMinLabel {
                    padding: 0px 0px;
                    margin: 0px;
                    color: blue;
                    }
                    
            QLabel#tMaxLabel {
                    padding: 0px 0px;
                    margin: 0px;
                    color: red;
                    }
        """)
        
        #. Add header group in header
        self.group_header.setLayout(self.header_layout)
        
        #. Add group in the class
        self.addWidget(self.group_header)
                
        #** ENDS SEGMENT 1: HEADER **#
        
        #** 2 SEGMENT - LAYOUT TO DETAILS PART **#
        
        # START DETAILS FILES
        
        # main Details container
        detail_main_layout      = QVBoxLayout()
        detail_main_layout.setContentsMargins(5, 8, 5, 8)

        for hour in hours:
            
            #(763, 'Toledo', 'ES', 'Clear', 'clear sky', 22.42, 22.42, 1012, 53, 3.47, 'No Record', 'No Record', 1748908800)
            #['id','city','country','mainDesc','description','temperature','temp_min','temp_max','presure','humidity','wind_speed','rain','snow','dt']
            # Extract raw database Data into a dict
            raw_data = self.buffer_city[hour]
            
            data = { 'mainDesc':raw_data[3], 'description':raw_data[4]
                   , 'temp':raw_data[5]    , 'rain':raw_data[11]
                   , 'snow':raw_data[12]   , 'dt':raw_data[13] }

            # Detail contanier
            detail_line_container = QFrame()
            detail_line_container.setObjectName('detailLineFrame')
            detail_line_layout    = QHBoxLayout()
            
            #. Set Hour
            dLabel_hour = QLabel(eFc.get_str_hour(data['dt']))
            #. APPLY BOLD FONT
            set_boldAlign(dLabel_hour)
            #. Set HOUR
            detail_line_layout.addWidget(dLabel_hour)
            
            #. Set Weather Ico
            pIcon_w    = get_WEATHER_labelPic(data['mainDesc'],data['description'])
            detail_line_layout.addWidget(pIcon_w)
            detail_line_layout.addStretch()
            
            #. Set Temp
            dLabel_temp = QLabel(f"{data['temp']:.1f}º")
            detail_line_layout.addWidget(dLabel_temp)
            
            #. Select color by value
            if data['temp'] < 15:
                dLabel_temp.setObjectName('tMinLabel')
            elif 15 <= data['temp'] <=25:
                dLabel_temp.setObjectName('tMidLabel')
            elif data['temp'] > 25:
                dLabel_temp.setObjectName('tMaxLabel')
            
            # PUSH BACK
            detail_line_layout.addStretch()
            
            # Optionals data
            if(data['rain']!='No Record'):
                
                pIcon_rain  = get_DEFAULT_labelPic('rain')
                dLabel_rain = QLabel(f"{data['rain']:.2f}")
                detail_line_layout.addWidget(pIcon_rain)
                detail_line_layout.addSpacing(-8)
                detail_line_layout.addWidget(dLabel_rain)
                
            elif(data['snow']!='No Record'):
                
                pIcon_snow  = get_DEFAULT_labelPic('snow')
                dLabel_snow = QLabel(f"{data['snow']:.2f}")
                detail_line_layout.addWidget(pIcon_snow)
                detail_line_layout.addSpacing(-8)
                detail_line_layout.addWidget(dLabel_snow)
            
            # ADD ALL INTO CONTAINER LAYOUT
            detail_line_container.setLayout(detail_line_layout)
            detail_main_layout.addWidget(detail_line_container)
            
        # ADD STRETCH TO KEEP SIZE IN LOW HOURS NUMBERS    
        detail_main_layout.addStretch()
        
        # ADD ALL INTO FRAME
        self.details_frame.setLayout(detail_main_layout)
        self.details_layout.addWidget(self.details_frame)
        
        #. APPLY CSS STYLE
        self.details_frame.setStyleSheet("""
            QFrame#detailFrame {
                    border: 1.5px dashed black;
                    padding: 2px;
                    margin: 0px;
                    border-radius: 10px;
                    background-color:Azure;
                    }
            QFrame#detailLineFrame {
                    border: 1px solid black;
                    padding: 0px 0px;
                    margin: 0px;
                    border-radius: 5px;
                    background-color:white;
                    }
            QLabel {
                    border: 0px solid black;
                    padding: 0px 0px;
                    margin: 0px;
                    border-radius: 5px;
                    }
            QLabel#tMinLabel {
                    padding: 0px 0px;
                    margin: 0px;
                    color: blue;
                    }
            QLabel#tMidLabel {
                    padding: 0px 0px;
                    margin: 0px;
                    color: green;
                    }
            QLabel#tMaxLabel {
                    padding: 0px 0px;
                    margin: 0px;
                    color: red;
                    }
        """)
        
        ## CSS FOR GROUP BOX
        # GROUP HEADER
        self.group_header.setStyleSheet("""
            QGroupBox {
                    border: 2px solid white;
                    border-radius: 5px;
                    margin-top: 10px;
                    }
            QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    padding: 2 5px;
                    background-color: white;
                    border: 1px solid black;
                    border-radius: 5px;
                    color: black;
                    font-weight: bold;
                    }
        """)
        
        # GROUP HOURS
        self.group_details.setStyleSheet("""
            QGroupBox {
                    border: 2px solid white;
                    border-radius: 5px;
                    margin-top: 10px;
                    }
            QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top center;
                    padding: 1 3px;
                    background-color: white;
                    border: 1px solid black;
                    border-radius: 10px;
                    color: black;
                    font-weight: bold;
                    }
        """)
        #** ENDS SEGMENT 2: DETAILS **#
        
        #. Add details group in details
        self.group_details.setLayout(self.details_layout)
        
        #. Add group in the class
        self.addWidget(self.group_details)

    
''' CORE OF POLLUTION FORECAST '''
class CoreForecastPollLayout(QVBoxLayout):
    
    def __init__(self,buffer_city,day,isFirst=False):
        
        super().__init__()
        
        #Dates
        self.buffer_city = buffer_city
        self.dates_city  = eFc.get_dtTransalor_weatherCity(self.buffer_city)
        self.day         = day
        self.isFirst     = isFirst
        
        #Main Frame
        self.main_frame     = QFrame()
        self.main_frame.setObjectName("mainFrame")
        
        #Header group
        self.header_frame   = QFrame()           
        self.main_frame.setObjectName("headerFrame")
        self.group_header   = QGroupBox()
        self.header_layout  = QVBoxLayout()
        
        #Details group
        self.details_frame  = QFrame()
        self.details_frame.setObjectName("detailFrame")
        self.group_details  = QGroupBox('HOURS')
        self.details_layout = QVBoxLayout()
        
        self.build()
        
    def build(self):
        
        # SET HOURS DATA
        hours = eFc.get_daykeys(self.dates_city,self.day)
                
        # GET FIRST HOUR
        raw_data = self.buffer_city[hours[0]]
        #[Id|city|country|air_quality|dt]
        data = { 'air_quality':raw_data[3] }
                
        #. If is today, not sumarize, just the current values
        if self.isFirst:
            air_q = data['air_quality']
        
        #. Forecast type, sumarize
        else:
            air_q = eFc.get_pollutionCounter(self.buffer_city,hours)#data['air_quality']
            #weathDes = eFc.get_weatherCounter(self.buffer_city,hours)
        
        # SET MARGINS
        self.header_layout.setContentsMargins(5, 15, 5, 5)
        
        #** 1 SEGMENT - LAYOUT TO HEADER PART **#
        header_labels_layout      = QVBoxLayout()
        header_labels_layout.setContentsMargins(5, 2, 5, 2)
        header_labels_layout.setSpacing(2)
        
        ##. CREATE ICONS LAYOUT AND ADD TO SEGMENT 
        header_icons_layout      = QVBoxLayout()
        header_icons_layout.setContentsMargins(0, 0, 0, 10)
        header_icons_layout.setSpacing(8)
        
        ## LABEL WITH THE LAST LOAD DATA
        label_date = QLabel(str(eFc.get_str_date(self.day)))
        # Add name to apply css
        label_date.setObjectName("mainDateLayout")
        #. APPLY BOLD FONT AND ALIGN
        set_boldAlign(label_date,True)
        ## LABEL WITH WEEKDAY
        self.group_header.setTitle(eFc.get_str_dayWeek(self.day))
        
        ## MAIN WEATHER IMG
        # Charge IMG
        pixImg = QPixmap(icoM.get_pollution_ico(air_q))
        
        # Check if img is found
        if pixImg.isNull():
            labelIcon_header = QLabel("Image not found")
        else:
            #Create img object class
            pixImg           = pixImg.scaled(100,100,Qt.KeepAspectRatio,Qt.SmoothTransformation)
            labelIcon_header = QLabel()
            #Load img into
            labelIcon_header.setPixmap(pixImg)
            
        #. Apply align Center
        labelIcon_header.setAlignment(Qt.AlignCenter)
        
        header_icons_layout.addWidget(label_date)
        header_icons_layout.addWidget(labelIcon_header)
        
        #. Add icons in header segment
        header_labels_layout.addLayout(header_icons_layout)
        
        ##. CREATE 4 LEVELS LABELS LAYOUT TO DATA HEADER
        
        ## LVL 1 - BIG TEMPERATURE - ONLY CURRENT DAY
        #header_labels_lv1_layout  = QHBoxLayout()
        #header_labels_lv1_layout.setAlignment(Qt.AlignCenter)
        
        ## LVL 2 - MAX/MIN TEMPERATURE
        #header_labels_lv2_layout  = QHBoxLayout()
        #header_labels_lv2_layout.setContentsMargins(0, 10, 0, 0)
        #header_labels_lv2_layout.setAlignment(Qt.AlignCenter)
          
        ## LVL 3 - HUMIDITY AND PRESSURE
        #header_labels_lv3_layout  = QHBoxLayout()
        #header_labels_lv3_layout.setContentsMargins(0, 8, 0, 8)
        #header_labels_lv3_layout.setAlignment(Qt.AlignCenter)
        
        ## LVL 4 - WIND, RAIN AND SNOW
        #header_labels_lv4_layout  = QHBoxLayout()
        #header_labels_lv4_layout.setContentsMargins(0, 0, 0, 10)
        #header_labels_lv4_layout.setAlignment(Qt.AlignCenter)
          
        #. Add levels in header layout
        #header_labels_layout.addLayout(header_labels_lv1_layout)
        #header_labels_layout.addLayout(header_labels_lv2_layout)
        #header_labels_layout.addLayout(header_labels_lv3_layout)
        #header_labels_layout.addLayout(header_labels_lv4_layout)
        
        #. Add layout into a frame
        self.header_frame.setLayout(header_labels_layout)
        self.header_layout.addWidget(self.header_frame)
        
        #. APPLY CSS STYLE
        self.header_frame.setStyleSheet("""
            QFrame {
                    border: 1.5px dashed black;
                    padding: 5px 15px;
                    margin: 1px;
                    border-radius: 10px;
                    background-color:Azure;
                    }
      
            QLabel {
                    border: 0px solid black;
                    padding: 0px 0px;
                    margin: 0px;
                    border-radius: 5px;
                    background-color: Azure;
                    }
            
            QLabel#mainDateLayout {
                    border: 1px solid black;
                    padding: 2px;
                    margin: 0px;
                    border-radius: 10px;
                    background-color: white;
                    }
        """)
        
        #. Add header group in header
        self.group_header.setLayout(self.header_layout)
        
        #. Add group in the class
        self.addWidget(self.group_header)
                
        #** ENDS SEGMENT 1: HEADER **#
        
        #** 2 SEGMENT - LAYOUT TO DETAILS PART **#
        
        # START DETAILS FILES
        
        # main Details container
        detail_main_layout      = QVBoxLayout()
        detail_main_layout.setContentsMargins(5, 8, 5, 8)

        for hour in hours:
            
            raw_data = self.buffer_city[hour]
            
            #[Id|city|country|air_quality|dt]
            data = { 'air_quality':raw_data[3], 'dt':raw_data[4] }

            # Detail contanier
            detail_line_container = QFrame()
            detail_line_container.setObjectName('detailLineFrame')
            detail_line_layout    = QHBoxLayout()
            
            #. Set Hour
            dLabel_hour = QLabel(eFc.get_str_hour(data['dt']))
            #. APPLY BOLD FONT
            set_boldAlign(dLabel_hour)
            #. Set HOUR
            detail_line_layout.addWidget(dLabel_hour)
            
            #. Set Weather Ico
            pixImg    = QPixmap(icoM.get_pollution_ico(data['air_quality']))
            pixImg    = pixImg.scaled(32,32,Qt.KeepAspectRatio,Qt.SmoothTransformation)
            labelIcon = QLabel()
            #Load img into
            labelIcon.setPixmap(pixImg)
            
            detail_line_layout.addWidget(labelIcon)
            #detail_line_layout.addStretch()
            
            # ADD ALL INTO CONTAINER LAYOUT
            detail_line_container.setLayout(detail_line_layout)
            detail_main_layout.addWidget(detail_line_container)
            
        # ADD STRETCH TO KEEP SIZE IN LOW HOURS NUMBERS    
        detail_main_layout.addStretch()
        
        # ADD ALL INTO FRAME
        self.details_frame.setLayout(detail_main_layout)
        self.details_layout.addWidget(self.details_frame)
        
        #. APPLY CSS STYLE
        self.details_frame.setStyleSheet("""
            QFrame#detailFrame {
                    border: 1.5px dashed black;
                    padding: 2px;
                    margin: 0px;
                    border-radius: 10px;
                    background-color:Azure;
                    }
            QFrame#detailLineFrame {
                    border: 1px solid black;
                    padding: 0px 0px;
                    margin: 0px;
                    border-radius: 5px;
                    background-color:white;
                    }
            QLabel {
                    border: 0px solid black;
                    padding: 0px 0px;
                    margin: 0px;
                    border-radius: 5px;
                    }
        """)
        
        ## CSS FOR GROUP BOX
        # GROUP HEADER
        self.group_header.setStyleSheet("""
            QGroupBox {
                    border: 2px solid white;
                    border-radius: 5px;
                    margin-top: 10px;
                    }
            QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    padding: 2 5px;
                    background-color: white;
                    border: 1px solid black;
                    border-radius: 5px;
                    color: black;
                    font-weight: bold;
                    }
        """)
        
        # GROUP HOURS
        self.group_details.setStyleSheet("""
            QGroupBox {
                    border: 2px solid white;
                    border-radius: 5px;
                    margin-top: 10px;
                    }
            QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top center;
                    padding: 1 3px;
                    background-color: white;
                    border: 1px solid black;
                    border-radius: 10px;
                    color: black;
                    font-weight: bold;
                    }
        """)
        #** ENDS SEGMENT 2: DETAILS **#
        
        #. Add details group in details
        self.group_details.setLayout(self.details_layout)
        
        #. Add group in the class
        self.addWidget(self.group_details)

'''
Row of elemnts: CoreForecastLayout
'''
class RowForecastLayout(QHBoxLayout):
    
    def __init__(self,city,buffer_city,typeFc):
        
        super().__init__()
        
        #Datas
        self.city        = city
        self.buffer_city = buffer_city
        self.typeFc      = typeFc
        
        #Main Frame
        self.main_container     = QFrame()
        self.main_container.setObjectName("mainFrame")
        
        #Body Layout
        self.body_layout = QVBoxLayout()
        
        self.build()
        
    def build(self):
        
        ## Set Layouts
        row_layout   = QHBoxLayout()
        title_layout = QHBoxLayout()
        
        ## set city Label
        city_label = QLabel(str(self.city).upper()) #<
        city_label.setObjectName('titleLabel')
        #. Apply Bold and big size
        labelFont = QFont()
        labelFont.setBold(True)
        labelFont.setPixelSize(20)
        city_label.setFont(labelFont)
        city_label.setAlignment(Qt.AlignCenter)
        #. Add Title in title layout
        title_layout.addWidget(city_label)
        
        ## Set data information by days
        dates_city = eFc.get_dtTransalor_weatherCity(self.buffer_city)

        # Return days
        days = eFc.get_days(dates_city)
        
        ## Loop days and create objects
        for i,day in enumerate(days):
            
            # SELECT WEATHER OR POLLUTION CORE AND CHECH IF IS CURRENT DAY
            if i == 0:
                layout = CoreForecastWeatLayout(self.buffer_city,day,True) if self.typeFc == 1 else CoreForecastPollLayout(self.buffer_city,day,True)
            else:
                layout = CoreForecastWeatLayout(self.buffer_city,day)      if self.typeFc == 1 else CoreForecastPollLayout(self.buffer_city,day)
                
            row_layout.addLayout(layout)
            
        ## ADD elemnts into layouts
        self.body_layout.addLayout(title_layout) 
        self.body_layout.addLayout(row_layout)   
        self.main_container.setLayout(self.body_layout)
        
        #. Add CSS STYLE
        self.main_container.setStyleSheet("""
        
            QFrame#mainFrame {
                        border: 1px solid black;
                        padding: 0px 0px;
                        margin: 0px;
                        border-radius: 5px;
                        background-color:MistyRose;
                        }
                        
            QFrame#titleLabel {
                        border: 1px solid black;
                        padding: 5px 0px;
                        margin: 0px;
                        border-radius: 10px;
                        background-color:black;
                        color:white;
                        }


        """)
        
        # ADD ALL THE ELEMENTS INTO MAIN CLASS
        self.addWidget(self.main_container)
        
        
'''
list of rows of: RowForecastLayout
1= Weather
2= Pollution
'''
class ForecastLayout(QVBoxLayout):
    
    def __init__(self,buffer,cities,typeFc):
        
        super().__init__()
        
        #DATA
        self.buffer = buffer
        self.cities = cities
        self.typeFc = typeFc
        
        # MAIN CONTAINER WITH QScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # SET VERTICAL SCROLL 
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # FIT CONTAINER SCROLL
        self.scroll_content = QWidget()
        self.scroll_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) 
        self.scroll_content.setMinimumWidth(self.scroll_area.viewport().width())
        
        # LAYOUT INTO SCROLL
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        
        # BUILD
        self.build()
        
        # SET SCROLL IN CLASS
        self.scroll_area.setWidget(self.scroll_content)
        self.addWidget(self.scroll_area)
        
    # BUILDER
    def build(self):
        
        # LIST OF RowForecastLayout
        for city in self.cities:
            
            # Data City
            cty         = str(city[0])
            buffer_city = self.buffer.get(cty)
            
            # Add row layout into class. Depends of typeFC
            layout = RowForecastLayout(cty,buffer_city,1) if self.typeFc == 1 else RowForecastLayout(cty,buffer_city,2)
            self.scroll_layout.addLayout(layout)

            
''' Weather forecast WEATHER main layout'''
class ForecastWeatherLayout(ForecastLayout):
    
    def __init__(self):
        
        # GET BUFFER DATA
        buffer = eFc.get_WeatherDict()
        # LIST OF CITIES
        cities = eFc.get_bufferWeather_cities()
        # CREATE CLASS TYPE 1 (WEATHER CORE)
        super().__init__(buffer,cities,1)
        
        
''' Weather forecast POLLUTION main layout'''
class ForecastPollutionLayout(ForecastLayout):
    
    def __init__(self):
        
        # GET BUFFER DATA
        buffer = eFc.get_PollutionDict()
        # LIST OF CITIES
        cities = eFc.get_bufferPollution_cities()
        # CREATE CLASS TYPE 2 (POLLUTION CORE)
        super().__init__(buffer,cities,2)

####### TEST DEF
def run_test():
    
    app = QApplication(sys.argv)
    
    #Put own layout
    #layout = ForecastWeatherLayout()
    #layout = ForecastPollutionLayout()
    layout = StandarDialogWindow('TITLE - TLKALNDF','texto texto adskjfnkfjgnkdnagkafn \n\n dasjfnjb')
    layout.show()
    ##widget = QWidget()
    # MAIN SIZE
    #widget.setFixedSize(270, 400)
    ##widget.setLayout(layout)
    
    ##widget.setWindowTitle("Test Layout")
    ##widget.show()
    sys.exit(app.exec_())

#
#run_test()
