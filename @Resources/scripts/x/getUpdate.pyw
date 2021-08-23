from requests import get
from time import sleep
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
import sys

r = get("https://api.github.com/repos/AdamWHY2K/Fa-apulu/releases")
latestVer = r.json()[0]["tag_name"][1:].replace(".", "")
with open("..\\InstalledVersion.txt", "r") as getVer:
    raw_installedVer = getVer.read()
    installedVer = raw_installedVer[1:].replace(".", "")

if latestVer > installedVer:
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    #Fixes UI bug that would cause users who have windows scaling enabled to have a smushed layout
    class Window(QMainWindow):
        def __init__(self):
            super(Window, self).__init__()
            self.setWindowFlags(Qt.FramelessWindowHint)
            #Removing the ugly windows title bar
            self.setWindowOpacity(0.94)
            #Making the app slightly see through
            width = 500
            height = 350
            self.setFixedSize(width, height)
            #Making the window unresizable

            self.pressing = False
            self.start = QPoint(0, 0)
            self.pressing = False
            #Enable window movement anywhere - https://stackoverflow.com/questions/44241612/custom-titlebar-with-frame-in-pyqt5

            radius = 20.0
            path = QPainterPath()
            path.addRoundedRect(QRectF(self.rect()), radius, radius)
            mask = QRegion(path.toFillPolygon().toPolygon())
            self.setMask(mask)
            self.move(QCursor.pos())
            #Rounding corners

            #labelTitle
            self.labelTitle = QLabel("Fa'apulu - Update available", self)
            #Create label widget
            self.labelTitle.resize(500, 30)
            self.labelTitle.setFont(QFont('Arial', 20, weight=QFont.Bold))
            #Setting labelTitle font, font size, and weight
            self.labelTitle.move((width - self.labelTitle.width()) / 2, 10)
            #Moving labelTitle to center
            self.labelTitle.setAlignment(Qt.AlignCenter)
            #Aligning text inside label to center

            #labelIVer
            self.labelIVer = QLabel("Installed: " + raw_installedVer, self)
            self.labelIVer.resize(200, 30)
            self.labelIVer.setFont(QFont('Arial', 15, weight=QFont.Bold))
            self.labelIVer.move(0, 60)
            self.labelIVer.setAlignment(Qt.AlignCenter)

            #labelAVer
            self.labelAVer = QLabel("Available: " + r.json()[0]["tag_name"], self)
            self.labelAVer.resize(200, 30)
            self.labelAVer.setFont(QFont('Arial', 15, weight=QFont.Bold))
            self.labelAVer.move(300, 60)
            self.labelAVer.setAlignment(Qt.AlignCenter)

            #labelChangelog
            self.labelChangelog = QLabel(r.json()[0]["body"], self)
            self.labelChangelog.resize(500, 233)
            self.labelChangelog.setFont(QFont('Arial', 13))
            self.labelChangelog.move(0, 50)
            self.labelChangelog.setStyleSheet("padding:7px")
            #Creating 7 pixels of space around the label
            self.labelChangelog.setAlignment(Qt.AlignCenter)
            self.labelChangelog.setWordWrap(True)
            #Making the text enter a new line once it reaches the edge
            
            #buttonUpdate
            self.buttonUpdate = QPushButton("Download update", self)
            #Create button widget
            self.buttonUpdate.resize(170, 40)
            self.buttonUpdate.move(40, 280)
            self.buttonUpdate.setFont(QFont('Arial', 12))
            self.buttonUpdate.clicked.connect(self.updateClicked)
            #Run updateClicked() when clicked

            #buttonPostpone
            self.buttonPostpone = QPushButton("Ask later", self)
            self.buttonPostpone.resize(170, 40)
            self.buttonPostpone.move(310, 280)
            self.buttonPostpone.setFont(QFont('Arial', 12))
            self.buttonPostpone.clicked.connect(self.close)
            #Closes the application when clicked

            #labelNote
            self.labelNote = QLabel("Note: Remember to re-run Setup.bat and restore NonSteamDict.txt from backup", self)
            self.labelNote.resize(490, 30)
            self.labelNote.setFont(QFont('Arial', 8, weight=QFont.Bold))
            self.labelNote.move(0, 320)
            self.labelNote.setAlignment(Qt.AlignCenter)
            self.labelNote.setStyleSheet("color: #ff0000")
            #Setting text colour to red

            self.show()
            #Show all widgets
        
        def updateClicked(self):
            QDesktopServices.openUrl(QUrl((r.json()[0]["assets"][0]["browser_download_url"])))
            #Open latest version download link in default browser
            QFile("..\\backup_NonSteamDict.txt").moveToTrash()
            #Moving previous backup to trash, note - on most systems this can be recovered.
            QFile("..\\NonSteamDict.txt").copy("..\\backup_NonSteamDict.txt")
            #Create backup of non steam games
            sleep(3)
            self.close()
            #Close after a short delay

        def mousePressEvent(self, event):
            self.start = self.mapToGlobal(event.pos())
            self.pressing = True

        def mouseMoveEvent(self, event):
            if self.pressing:
                self.end = self.mapToGlobal(event.pos())
                self.movement = self.end-self.start
                self.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.width(),
                                    self.height())
                self.start = self.end

        def mouseReleaseEvent(self, QMouseEvent):
            self.pressing = False
        #Enable window movement anywhere - https://stackoverflow.com/questions/44241612/custom-titlebar-with-frame-in-pyqt5

    App = QApplication(sys.argv)
    #Create app instance

    App.setStyle("Fusion")
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    qApp.setPalette(dark_palette)
    qApp.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
    #Setting dark fusion style - https://gist.github.com/mstuttgart/37c0e6d8f67a0611674e08294f3daef7

    window = Window()
    #Create window instance

    sys.exit(App.exec())
    #Exectute the app
else:
    print("Up to date")
