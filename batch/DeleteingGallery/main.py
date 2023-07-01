import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,QPushButton, QApplication,QSizePolicy)
from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets
import json,os
from PyQt5 import QtCore,QtGui
import PyQt5.QtGui
import glob
import shutil

# PC
# Rigt click -> keep
# Left click -> remove
# MIddle click -> minimize
# Ctrl -> close


# Android
# swipe up -> remove (*later save)
# swipe down -> remove
# double click -> remove

class DraggableLabel(QtWidgets.QLabel):
	def __init__(self,my_app,image):
		super(QtWidgets.QLabel,self).__init__()

		self.image = image
		self.base_pixmap = QtGui.QPixmap(image)
		self.pixmap = self.base_pixmap.scaledToHeight(self.height())
		self.setPixmap(self.pixmap)

		self.my_app = my_app

	def mousePressEvent(self, event):
		self.drag_start_position = event.pos()

		if not self.my_app.is_mobile:
			if event.button() == QtCore.Qt.RightButton:
				self.my_app.processImage(self, False)
			if event.button() == QtCore.Qt.LeftButton:
				self.my_app.processImage(self, True)
			if event.button() ==  QtCore.Qt.MiddleButton:
				self.my_app.showMinimized()

	def mouseReleaseEvent(self, event):
		start = self.drag_start_position
		end = event.pos()
		delta = end.y()-start.y()
		if abs(delta) > 30:
			self.my_app.dragImage(self,delta)

	#def mouseDoubleClickEvent(self, event):
	#	if self.my_app.is_mobile:
	#		self.my_app.imageDoubleClicked(self)

	def resizeEvent(self, event):
		self.setPixmap(self.base_pixmap.scaledToHeight(self.height()))


class Example(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def keyPressEvent(self, event):
		key = event.key()
		if event.modifiers() == QtCore.Qt.ControlModifier:
			self.close()

	def resizeEvent(self, QResizeEvent):
		self.scroll_widget.setMaximumHeight(self.scroll_area.height()-50)
	  
	def mousePressEvent(self, event):
		print(event.button())
		if event.button() ==  QtCore.Qt.MiddleButton:
			self.showMinimized()
		super(Example, self).mousePressEvent(event)

	def initUI(self):
		self.delete_images = True
		
		# check if we have command line args, else open dialog
		if len(sys.argv)>1:
			self.image_dir = sys.argv[1]
		else:		
			self.image_dir = self.openFileNameDialog()

		# Load Top JSON
		self.top_json_path = self.image_dir + '/top.json'		
		if os.path.isfile(self.top_json_path):
			with open(self.top_json_path , 'r') as myfile:
				self.top_json= json.load(myfile)
		else:
			self.top_json=[]

		# check if we're mobile
		self.is_mobile = (sys.platform=="linux")
		# TESTING PURPOSES
		#self.is_mobile = True

		self.mainLayout = QtWidgets.QVBoxLayout()
		self.scroll_area = QtWidgets.QScrollArea()

		# Scroll area layout
		self.scroll_area = QtWidgets.QScrollArea()
		self.scroll_widget = QtWidgets.QWidget()
		self.scroll_layout = QtWidgets.QHBoxLayout()
		self.scroll_menu = []

		self.scroll_area.setWidgetResizable(True)

		self.loadImages()

		self.scroll_widget.setLayout(self.scroll_layout)
		self.scroll_area.setWidget(self.scroll_widget)

		QtWidgets.QScroller.grabGesture(self.scroll_area.viewport(), QtWidgets.QScroller.LeftMouseButtonGesture)
		self.scroll_area.verticalScrollBar().setEnabled(False)


		self.mainLayout.addWidget(self.scroll_area)

		self.setLayout(self.mainLayout)
		self.setGeometry(300, 300, 1500, 1500)
		self.setGeometry(300, 300, 300, 300)
		self.setWindowTitle('Deleteing_Gallery')
		self.show()


	def loadImages(self):
		self.images =  (glob.glob(self.image_dir + "/*"))
		self.filterImagesByTopJson()		
		self.top_images = []
		self.fillScrollView()

	def filterImagesByTopJson(self):			
		top_img_names = [os.path.basename(img_path) for img_path in self.top_json]
		print(top_img_names)
		
		self.images = [a for a in self.images if os.path.basename(a) not in top_img_names]		

	def fillScrollView(self):
		self.slice_index = 25

		self.current_images = self.images[0:self.slice_index]
		self.images = self.images[self.slice_index:]

		# Mobile Create TOP
		if self.current_images == [] and self.is_mobile:
			self.current_images = self.top_images
			self.top_images = []
			self.setStyleSheet("background-color: black;")

		# Fill Scroll View With Images
		for image in self.current_images:
			label = DraggableLabel(self, image)
			self.scroll_layout.addWidget(label)

		#add Scroll Menu
		self.addScrollMenu()

	def addScrollMenu(self):
		if  self.scroll_menu == []:
			self.scroll_menu = QtWidgets.QWidget()
			self.scroll_menu.setFixedWidth(300)
			self.scroll_menu_layout = QtWidgets.QGridLayout()
			self.scroll_menu.setLayout(self.scroll_menu_layout)

			#btn_saveTop = QtWidgets.QPushButton("SaveTop")
			#btn_saveTop.clicked.connect(self.saveTop)
			#btn_saveTop.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

			btn_removeAll = QtWidgets.QPushButton("RemoveAll")
			btn_removeAll.clicked.connect(self.removeAll)
			btn_removeAll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
			
			btn_switchAction = QtWidgets.QPushButton("SwitchAction")
			btn_switchAction.clicked.connect(self.switchAction)
			btn_switchAction.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
			
			btn_openNewFolder = QtWidgets.QPushButton("Open New Folder")
			btn_openNewFolder.clicked.connect(self.openNewFolder)
			btn_openNewFolder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

			#if self.is_mobile:
			#self.scroll_menu_layout.addWidget(btn_saveTop)
			self.scroll_menu_layout.addWidget(btn_removeAll)
			self.scroll_menu_layout.addWidget(btn_switchAction)
			self.scroll_menu_layout.addWidget(btn_openNewFolder)

			self.scroll_layout.addWidget(self.scroll_menu)
		else:
			self.scroll_menu.setParent(None)
			self.scroll_layout.addWidget(self.scroll_menu)

	def saveTop(self):
		self.top_dir = "/storage/emulated/0/TEMP/Z Top 001"
		if not os.path.isdir(self.top_dir):
			os.mkdir(self.top_dir)

		for child in self.scroll_widget.children():
			if (isinstance(child,DraggableLabel)):
				#print(child.image)
				shutil.copy(child.image, self.top_dir)

	def removeAll(self):
		for child in self.scroll_widget.children():
			if (isinstance(child,DraggableLabel)):
				self.removeImage(child)

	def switchAction(self):
		self.delete_images = not self.delete_images
		self.setWindowTitle('Deleteing_Gallery' if self.delete_images else 'Saving_Gallery')		

	def cleanScrollView(self):
		for child in self.scroll_widget.children():
			if (isinstance(child,DraggableLabel)):
				child.setParent(None)
		self.scroll_widget.adjustSize()

	def openNewFolder(self):
		self.cleanScrollView()
	
		# Better To Move Things into funcitons
		# open file dialogue
		self.image_dir = self.openFileNameDialog()
		
		# Load Top JSON
		self.top_json_path = self.image_dir + '/top.json'		
		if os.path.isfile(self.top_json_path):
			with open(self.top_json_path , 'r') as myfile:
				self.top_json= json.load(myfile)
		else:
			self.top_json=[]		
		
		self.loadImages()
		

	def imageDoubleClicked(self,image):
		self.saveImage(image)

	def processImage(self, image, result):
		if self.delete_images:
			if result:
				self.keepImage(image)
			else:
				self.deleteImage(image)
		else:
			if result:
				self.saveImage(image)
			else:
				self.removeImage(image)
	
	# saves image to the best subdir
	def saveImage(self,image):
		if not self.is_mobile:
			out_dir = self.image_dir + "/best"
			if not os.path.isdir(out_dir):
				os.mkdir(out_dir)
			shutil.copy(image.image, out_dir)
		else:
			self.top_images += [image.image]
			print(self.top_images)

		self.removeImage(image)
	
	def keepImage(self,image):
		# Update Json
		self.top_json+=[image.image]
		print(self.top_json)
		
		json_object = json.dumps(self.top_json, indent=4)
 
		# Writing to sample.json
		with open(self.top_json_path, "w") as outfile:
			outfile.write(json_object)		
	
		self.removeImage(image)

	def deleteImage(self,image):
		#print(image.image)
		os.remove(image.image)
		self.removeImage(image)
		
	def removeImage(self,image):
		image.setParent(None)
		self.scroll_widget.adjustSize()

		if (len(self.scroll_widget.children())) == 2:
			self.fillScrollView()

	def dragImage(self,image,delta):
		if(delta < 0):
			self.saveImage(image)
		else:
			self.removeImage(image)

	def openFileNameDialog(self):
		dialog = QtWidgets.QFileDialog()
		dialog.setFixedSize(1000,1000)
		return str(dialog.getExistingDirectory(self, "Select Directory","/storage/emulated/0/images/Y_Top_001"))

	def fileSelected(self, filename):
		print(filename)



if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())