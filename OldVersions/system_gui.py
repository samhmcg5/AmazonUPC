from PyQt5.QtWidgets import QWidget, QApplication
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtWebEngineWidgets as QtWebWid
import sys

from scrape import ScrapeAmazon, TEST_ITEMS

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
        self.scrollArea.setWidgetResizable(True)
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
        items = ScrapeAmazon.getItems(param)
        # items = TEST_ITEMS
        if len(items) > 0:
            self.webView.setUrl(qtc.QUrl(items[0].link))
            self.sidebar.updateItems(items)
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
        # self.setUrl(qtc.QUrl("https://www.google.com"))

    def setParam(self, param):
        self.param = param
        self.setUrl(qtc.QUrl(BASE_URL % self.param))
        # self.setUrl(qtc.QUrl("https://www.google.com"))


class LinkSidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.widgets = []
        self.vbox = qtw.QVBoxLayout()
        self.vbox.addStretch()
        self.setLayout(self.vbox)

    def clearLayout(self):
        for i in self.widgets:
            i.deleteLater()
        self.widgets.clear()

    def updateItems(self, items):
        self.clearLayout()
        for i in items:
            label = SidebarItem(i)
            self.vbox.insertWidget(self.vbox.count()-1, label)
            self.widgets.append(label)


class SidebarItem(qtw.QLabel):
    def __init__(self, item):
        super().__init__()
        self.item = item
        self.setText(self.item.title)
        self.mousePressEvent = self.handleClick

    def handleClick(self, event):
        print("clicked")
