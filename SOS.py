import firebase_admin
from firebase_admin import credentials, db
from PyQt6 import QtCore, QtGui, QtWidgets 
import time


KEY = credentials.Certificate('key.json')

class Ui_SOS(object):
       
    def setupUi(self, SOS):
        SOS.setObjectName("SOS")
        SOS.setEnabled(True)
        SOS.resize(600, 504)
        SOS.setAutoFillBackground(True)
        SOS.setWindowIcon(QtGui.QIcon("sos-button-emoji.png"))

        self.old_Add = "0"
        self.old_Lat = "0"
        self.old_Lng = "0"
        
        self.pushButton = QtWidgets.QPushButton(SOS)
        self.pushButton.setGeometry(QtCore.QRect(250, 470, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.establish)
        
        self.enterkey = QtGui.QShortcut(QtGui.QKeySequence('Return'),SOS)
        self.enterkey.activated.connect(self.establish)
        
        self.listWidget = QtWidgets.QListWidget(SOS)
        self.listWidget.setGeometry(QtCore.QRect(5, 11, 591, 451))
        self.listWidget.setObjectName("listWidget")
        
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)

        self.label = QtWidgets.QLabel(SOS, text= "" )
        self.label.setGeometry(QtCore.QRect(475,473,120,20))
        
        


        self.retranslateUi(SOS)
        QtCore.QMetaObject.connectSlotsByName(SOS)

    def retranslateUi(self, SOS):
        _translate = QtCore.QCoreApplication.translate
        SOS.setWindowTitle(_translate("SOS", "SOS"))
        self.pushButton.setText(_translate("SOS", "Get Alerts..."))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("SOS", "Waiting for Alerts ..."))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        
    
    def connect(self):
        firebase_admin.initialize_app(KEY, {'databaseURL': 'https://save-our-souls-c4b32.firebaseio.com/'})
    
    def Locate(self):
        SOSloc = db.reference('SOS')
        location = SOSloc.get()
        return location
    
    def establish(self):
        ui.connect()
        self.start = time.perf_counter()
        self.pushButton.setDisabled(True)
        self.label.setText("Runnig for: ")
        fontlabel = QtGui.QFont()
        fontlabel.setFamily("Open Sans")
        fontlabel.setPixelSize(10)
        self.label.setFont(fontlabel)
        timer = QtCore.QTimer(SOS)
        timer.timeout.connect(self.listing)
        timer.start(10)

        
    def listing(self):    
        count = time.perf_counter()
        self.label.setText("Runnig for: "+ str(round(count-self.start,2))+" sec")

        Location = ui.Locate()
        Adress = Location['Adress']
        Latitude = Location['Latitude']
        Longitude = Location['Longitude']

        if Adress == "0" and Longitude == "0" and Latitude == "0":
            pass
        elif Adress == self.old_Add and Latitude == self.old_Lat and Longitude == self.old_Lng:
            pass
        else:  
            x=+1 
            self.listWidget.insertItem(x,"Adress: " + Adress)
            x=+1
            self.listWidget.insertItem(x,"Latitude: "+Latitude)
            x=+1
            self.listWidget.insertItem(x,"Longitude: "+Longitude)
            current_time = QtCore.QTime.currentTime()
            current_date = QtCore.QDate.currentDate()
            x=+1
            self.listWidget.insertItem(x,"Date: "+ current_date.toString() + " time: "+ current_time.toString('hh:mm:ss'))
            self.old_Add = Adress
            self.old_Lat = Latitude
            self.old_Lng = Longitude
        
            



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SOS = QtWidgets.QWidget()
    ui = Ui_SOS()
    ui.setupUi(SOS)
    SOS.show()
    x = 0
    sys.exit(app.exec())
