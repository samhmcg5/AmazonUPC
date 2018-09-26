from PyQt5.QtWidgets import QApplication
import sys

from system_gui import SystemGui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SystemGui()
    sys.exit(app.exec_())
