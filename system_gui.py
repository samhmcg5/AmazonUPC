from PyQt5.QtWidgets import QWidget, QApplication
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtWebEngineWidgets as QtWebWid
from PyQt5.QtGui import QFont
import sys
from collections import namedtuple

from scrape import ScrapeThread

class SystemGui(QWidget):
    def __init__(self):
        super().__init__()
        self.scraper = ScrapeThread()
        self.scraper.start()
        self.initUI()
        self.connectSignals()
        self.show()

    def initUI(self):
        # Top level container
        self.vbox = qtw.QVBoxLayout()
        # hold links and webview
        self.hbox = qtw.QSplitter()

        # Components
        self.navBar = NavigationBar()
        self.navBar.setFixedHeight(75)
        self.vbox.addWidget(self.navBar)
        self.vbox.addWidget(self.hbox)

        self.sidebar = LinkSidebar(self.navBar)
        self.hbox.addWidget(self.sidebar)

        self.webView = WebView()
        self.hbox.addWidget(self.webView)

        self.setLayout(self.vbox)
        self.setWindowTitle("Amazon Prime Bar Code Loader")

    def connectSignals(self):
        self.sidebar.itemClicked.connect(self.webView.handleItemCLick)
        self.scraper.dataSig.connect(self.sidebar.updateItems)
        self.navBar.refButton.clicked.connect(self.requestData)
        self.navBar.upcLine.returnPressed.connect(self.requestData)

    def requestData(self):
        param = self.navBar.upcLine.text()
        self.scraper.pushTask(param)



class NavigationBar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # top level of this class
        vLayout = qtw.QVBoxLayout()
        hNavBox = qtw.QHBoxLayout()
        hCheckBox = qtw.QHBoxLayout()

        self.refButton = qtw.QPushButton("Refresh")
        self.upcLine = qtw.QLineEdit()
        # Force all keyboard input to the line edit
        self.upcLine.grabKeyboard()
        hNavBox.addWidget(self.refButton)
        hNavBox.addWidget(self.upcLine)

        self.searchLabel = qtw.QLabel("Search for:")
        font = self.searchLabel.font()
        font.setPointSize(14)
        self.searchLabel.setFont(font)
        hCheckBox.addWidget(self.searchLabel)

        vLayout.addLayout(hNavBox)
        vLayout.addLayout(hCheckBox)
        self.setLayout(vLayout)
    
    def getParam(self):
        return self.upcLine.text()

    def updateResults(self):
        self.searchLabel.setText("Search for: %s" % self.upcLine.text())
        self.upcLine.setText("")


class WebView(QtWebWid.QWebEngineView):
    itemSig = qtc.pyqtSignal(list)
    def __init__(self):
        super().__init__()
        html = open('home.html','r').read()
        self.setHtml(html)

    def handleItemCLick(self, item):
        print("Clicked <LinkList>", item.link)
        self.loadWebpage(item.link)

    def loadWebpage(self, url):
        self.setUrl(qtc.QUrl(url))
        

class LinkSidebar(qtw.QListWidget):
    def __init__(self, navBar):
        super().__init__()
        self.navBar = navBar

    def updateItems(self, items):
        self.items = items
        self.clear()
        for i in items:
            LinkItem(i.title, i.link, self)
        self.setCurrentRow(0)
        if self.count() > 0:
            self.itemClicked.emit(self.item(0))
        self.navBar.updateResults()
    
            
class LinkItem(qtw.QListWidgetItem):
    def __init__(self, text, link, parent):
        super().__init__(text, parent)
        self.link = link


