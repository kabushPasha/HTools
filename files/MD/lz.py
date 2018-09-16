from PythonQt import QtCore, QtGui, MarvelousDesignerAPI
from PythonQt.MarvelousDesignerAPI import *
import MarvelousDesigner
from MarvelousDesigner import *

import PythonQt

def link(source):
	MarvelousDesigner().avatar_file_open(source + "\\cloth.obj",obj_type=2,scale = "m")
	MarvelousDesigner().avatar_file_open(source + "\\geo.obj",obj_type=0,scale = "m")	
	PythonQt.Qt.QApplication.clipboard().setText(source + "\\out.obj")
	
	
def loadAll(_scale = "m"):
	MarvelousDesigner().avatar_file_open("C:\\ProgramData\\Canoe\\MD\\cloth.obj",obj_type=2,scale = _scale )
	MarvelousDesigner().avatar_file_open("C:\\ProgramData\\Canoe\\MD\\geo.obj",obj_type=0,scale = _scale)
	savePath()

def loadCoat():
	loadAll("cm")
	
def loadCloth():
	MarvelousDesigner().avatar_file_open("C:\\ProgramData\\Canoe\\MD\\cloth.obj",obj_type=2,scale = "cm")
	
def loadGeo():	
	MarvelousDesigner().avatar_file_open("C:\\ProgramData\\Canoe\\MD\\geo.obj",obj_type=0,scale = "cm")	

def savePath():
	PythonQt.Qt.QApplication.clipboard().setText("C:\\ProgramData\\Canoe\\MD\\out.obj")
	