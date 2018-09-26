import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

app = QApplication(sys.argv)

web = QWebEngineView()
web.setUrl(QUrl("https://pythonspot.com"))
web.show()

sys.exit(app.exec_())
