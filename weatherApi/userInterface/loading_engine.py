'''
CLASS - ENGINE TO MANAGE THE MASIVE LOAD
'''
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QPushButton, QProgressBar, QListWidget
)

from PyQt5.QtCore import Qt, QTimer
import weatherApi.exeAux.exeWeather as eweather

class ProgressDialog(QDialog):
    def __init__(self, total_steps):
        super().__init__()
        self.setWindowTitle("UPDATING MAP")
        self.resize(400, 250)

        self.total_steps = total_steps

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Starting city charge...")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.layout.addWidget(self.progress_bar)

        self.city_list = QListWidget()
        self.layout.addWidget(self.city_list)

        self.button_close = QPushButton("CLOSE")
        self.button_close.setEnabled(False)
        self.button_close.clicked.connect(self.accept)
        self.layout.addWidget(self.button_close)

    def update_status(self, current_index, city_name, err):
        
        self.label.setText(f"Processing city... \n[{current_index}/{self.total_steps}]")
        
        if err:
            self.city_list.addItem(f"{current_index}: {city_name} ❌")
        else:
            self.city_list.addItem(f"{current_index}: {city_name} ✅")
        
        self.city_list.scrollToBottom()
        # Calculate percent
        percent = int((current_index / self.total_steps) * 100)
        # Set value in progress bar
        self.progress_bar.setValue(percent)

    def finish(self):
        self.label.setText("✅ Done")
        self.button_close.setEnabled(True)

# CITY LOOP WEATHER
def city_loop_weather(list_of_cities):
    
    maxApiCall = 50
    total = len(list_of_cities)
    current_index = 0

    dialog = ProgressDialog(total)
    dialog.show()

    def process_next():
        nonlocal current_index

        if current_index >= total:
            dialog.finish()
            return

        stack = list_of_cities[current_index:current_index + maxApiCall]

        for city in stack:
            
            cty,country = city[0],city[1]
            cty = str(cty).replace('_',' ')
            
            try:
                
                current_index += 1
                name = f"{cty}, [{country}]"
                print([[cty,country]])
                
                eweather.load_weather_lcities([[cty,country]])    
                
                err = False
                
            except Exception as e:
                print(e)
                name = f"{cty}, [{country}]"
                err = True
                
            dialog.update_status(current_index, name, err)

            QTimer.singleShot(10, lambda: None)
            
        #QTimer.singleShot(10000, process_next)  # Whait to next stack
        QTimer.singleShot(55000, process_next)  # Whait to next stack

    QTimer.singleShot(0, process_next)
    
    return dialog

# CITY LOOP POLLUTION
def city_loop_pollution(list_of_cities):
    
    maxApiCall = 50
    total = len(list_of_cities)
    current_index = 0

    dialog = ProgressDialog(total)
    dialog.show()

    def process_next():
        nonlocal current_index

        if current_index >= total:
            dialog.finish()
            return

        stack = list_of_cities[current_index:current_index + maxApiCall]

        for city in stack:
            
            cty,country = city[0],city[1]
            cty = str(cty).replace('_',' ')
            
            try:
                
                current_index += 1
                name = f"{cty}, [{country}]"
                print([[cty,country]])
                
                eweather.load_pollution_city(cty)   
                
                err = False
                
            except Exception as e:
                print(e)
                name = f"{cty}, [{country}]"
                err = True
                
            dialog.update_status(current_index, name, err)

            QTimer.singleShot(10, lambda: None)
            
        #QTimer.singleShot(10000, process_next)  # Whait to next stack
        QTimer.singleShot(55000, process_next)  # Whait to next stack

    QTimer.singleShot(0, process_next)
    
    return dialog


'''
# --- TEST ---
if __name__ == "__main__":
    app = QApplication(sys.argv)

    sample_cities = [[f"City{i}", "NL"] for i in range(123)]
    progress_dialog = city_loop_async(sample_cities)

    sys.exit(app.exec_())
'''
'''
# --- TESTEO ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Lista de ejemplo
    sample_cities = [["City" + str(i), "NL"] for i in range(123)]
    ventana_dialogo = city_loop_async(sample_cities)
    sys.exit(app.exec_())
'''

'''
import time

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton,QLabel,QDialog,QDialogButtonBox,QSizePolicy,QFrame,QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont,QIcon,QPixmap
from PyQt5.Qt import QLineEdit, QGroupBox,QGraphicsOpacityEffect

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def get_numLoops(city_total,maxApiCall):
    return city_total // maxApiCall

def city_loop(list_of_cities):
    
    classWindows = StandarDialogWindow('Inicio','Test')
    classWindows.exec_()
    
    print("dentro engine")
    #list_of_cities = show_cities_NL()
    maxApiCall = 50
    city_total = len(list_of_cities)
    #Round the number of loops that it's necesary
    init       = 0
    loops      = get_numLoops(city_total,maxApiCall)
    
    # MAIN LOOP BY STACKS
    for x in range(0,city_total,maxApiCall):
        
        # SELECT STACK
        stack = list_of_cities[x:x + maxApiCall]
        
        # LOOP STACK
        for k in stack:
            print(k[0],k[1])
            #print(x)
        print(f"finish {maxApiCall} ------------------------------------")
        QApplication.processEvents()  # Deja respirar a la GUI
        time.sleep(2)


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
        #set_boldAlign(self.title_bar,True)
        self.title_bar.setFixedHeight(30)
        
        # TITLE CSS STYLE
        self.title_bar.setStyleSheet("background-color: black; color: white; padding:8px; font-size: 18px;")
        
        # SET OPACITY
        #set_Opacity(self.title_bar,0.7)

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
        #set_boldAlign(self.placeholder,True)
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