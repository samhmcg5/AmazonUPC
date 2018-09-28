from PyQt5.QtWidgets import QWidget, QApplication
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtWebEngineWidgets as QtWebWid

import sys
from collections import namedtuple

Product = namedtuple('Product', ['link', 'title'])

X=0
def generateFakeStuff():
    global X
    items = []
    for i in range(X,X+20):
        items.append(Product("https://www.google.com/%i" % i, "Search %i" % i))
    X = X + 20
    return items


class SystemGui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.connectSignals()
        self.show()

    def initUI(self):
        # Top level container
        self.vbox = qtw.QVBoxLayout()
        # hold links and webview
        self.hbox = qtw.QHBoxLayout()

        # Components
        self.navBar = NavigationBar()
        self.navBar.setFixedHeight(100)
        self.vbox.addWidget(self.navBar)

        self.vbox.addLayout(self.hbox)

        self.sidebar = LinkSidebar()
        self.hbox.addWidget(self.sidebar)

        self.webView = WebView(self.navBar.upcLine)
        self.hbox.addWidget(self.webView)

        self.setLayout(self.vbox)
        self.setWindowTitle("Amazon Prime Bar Code Loader")

    def connectSignals(self):
        self.sidebar.itemClicked.connect(self.webView.handleItemCLick)
        self.navBar.refButton.clicked.connect(self.webView.handleRefreshClick)
        self.navBar.upcLine.returnPressed.connect(self.webView.handleEnter)
        self.webView.itemSig.connect(self.sidebar.updateItems)


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
        hNavBox.addWidget(self.refButton)
        hNavBox.addWidget(self.upcLine)

        self.checkNew = qtw.QCheckBox("New")
        self.checkUsed = qtw.QCheckBox("Like New")
        self.checkAcc = qtw.QCheckBox("Acceptable")
        self.checkNew.setChecked(True)
        self.checkAcc.setChecked(True)
        self.checkUsed.setChecked(True)
        hCheckBox.addWidget(self.checkNew, qtc.Qt.AlignLeft)
        hCheckBox.addWidget(self.checkUsed, qtc.Qt.AlignLeft)
        hCheckBox.addWidget(self.checkAcc, qtc.Qt.AlignLeft)

        vLayout.addLayout(hNavBox)
        vLayout.addLayout(hCheckBox)
        self.setLayout(vLayout)


class WebView(QtWebWid.QWebEngineView):
    itemSig = qtc.pyqtSignal(list)
    def __init__(self, upcLine):
        super().__init__()
        self.parentUPC = upcLine
        self.setUrl(qtc.QUrl('https://www.google.com'))

    def getParam(self):
        return self.parentUPC.text()

    def handleItemCLick(self, item):
        print("Clicked <WebView>", item.link)
        self.loadWebpage(item.link)

    def handleRefreshClick(self):
        print("Clicked <Refresh>", self.getParam())
        ###############
        self.itemSig.emit(generateFakeStuff())

    def handleEnter(self):
        print("Clicked <Enter>", self.getParam())
        ###############
        self.itemSig.emit(generateFakeStuff())

    def loadWebpage(self, url):
        self.setUrl(qtc.QUrl(url))
        

class LinkSidebar(qtw.QListWidget):
    def __init__(self):
        super().__init__()

    # def testItems(self):
    #     for i in range(40):
    #         LinkItem("text %i" % i, "Link%i"%i, self)

    def updateItems(self, items):
        self.items = items
        self.clear()
        for i in items:
            LinkItem(i.title, i.link, self)
    
            
class LinkItem(qtw.QListWidgetItem):
    def __init__(self, text, link, parent):
        super().__init__(text, parent)
        self.link = link


