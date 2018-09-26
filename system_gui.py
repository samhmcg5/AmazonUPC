from PyQt5.QtWidgets import QWidget, QApplication
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtWebEngineWidgets as QtWebWid
import sys

from scrape import ScrapeAmazon

BASE_URL = "https://www.amazon.com/s/field-keywords=%s"
DEFAULT_SEARCH = "9780316040341"

###############################
### TOP LEVEL GUI COMPONENT ###
###############################
class SystemGui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.connectSignals()
        self.show()

    def initUI(self):
        self.navBar = NavigationBar()
        self.navBar.setFixedHeight(100)
        self.webView = WebView(DEFAULT_SEARCH)
        self.sidebar = LinkSidebar()
        self.scrollArea = qtw.QScrollArea()
        self.scrollArea.setWidget(self.sidebar)
        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        vbox.addWidget(self.navBar)
        hbox.addWidget(self.scrollArea)
        hbox.addWidget(self.webView)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.setWindowTitle("Amazon Prime UPC Reader")

    def connectSignals(self):
        # self.navBar.refButton.clicked.connect(self.webView.reload)
        self.navBar.refButton.clicked.connect(self.refreshPage)
        self.navBar.upcLine.returnPressed.connect(self.refreshPage)

    def refreshPage(self):
        param = self.navBar.upcLine.text()
        links = ScrapeAmazon.searchPageLinks(param)
        if len(links) > 0:
            self.webView.setUrl(qtc.QUrl(links[0]))
        else:
            self.webView.setParam(param)

class NavigationBar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.refButton = qtw.QPushButton("Refresh")
        self.upcLine = qtw.QLineEdit(DEFAULT_SEARCH)
        hNavBox = qtw.QHBoxLayout()
        hNavBox.addWidget(self.refButton)
        hNavBox.addWidget(self.upcLine)
        self.checkNew = qtw.QCheckBox("New")
        self.checkUsed = qtw.QCheckBox("Like New")
        self.checkAcc = qtw.QCheckBox("Acceptable")
        hCheckBox = qtw.QHBoxLayout()
        hCheckBox.addWidget(self.checkNew, qtc.Qt.AlignLeft)
        hCheckBox.addWidget(self.checkUsed, qtc.Qt.AlignLeft)
        hCheckBox.addWidget(self.checkAcc, qtc.Qt.AlignLeft)
        vLayout = qtw.QVBoxLayout()
        vLayout.addLayout(hNavBox)
        vLayout.addLayout(hCheckBox)
        self.setLayout(vLayout)


class WebView(QtWebWid.QWebEngineView):
    def __init__(self, param):
        super().__init__()
        self.param = param
        self.initUI()
    
    def initUI(self):
        self.setUrl(qtc.QUrl(BASE_URL % self.param))

    def setParam(self, param):
        self.param = param
        self.setUrl(qtc.QUrl(BASE_URL % self.param))


class LinkSidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.vbox = qtw.QVBoxLayout()
        for i in range(30):
            self.vbox.addWidget(qtw.QLabel("Label Number %s" % i))
        self.setLayout(self.vbox)
