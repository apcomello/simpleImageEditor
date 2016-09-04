import Interface
from PyQt4 import QtGui
import sys

app = QtGui.QApplication(sys.argv)

teste = Interface.MainWindow()

teste.create_main_window()
sys.exit(app.exec_())
