import sys
from PyQt4.QtCore import Qt
from PyQt4.QtGui import *


class TableWidget(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        quitAction = menu.addAction("Quit")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAction:
            qApp.quit()


app = QApplication([])
tableWidget = TableWidget()
tableWidget.show()
sys.exit(app.exec_())