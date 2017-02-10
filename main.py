#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================
# Author: Ana Paula Mello       apcomello@gmail.com
# Date: September 2016
# Project for INF1046 - Fundamentos de Processamento de Imagens
# UFRGS - Departamento de Informática
# Version 1.2
#===============================================

__author__ = "Ana Paula Mello"
__email__ = "apcomello@gmail.com"
__version__ = "1.2"

import Interface
from PyQt4 import QtGui
import sys

app = QtGui.QApplication(sys.argv)

teste = Interface.MainWindow()

teste.create_main_window()
sys.exit(app.exec_())
