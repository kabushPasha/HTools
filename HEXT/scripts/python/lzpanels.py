from hutil.Qt import QtWidgets,QtGui
import lzutil
import os
import hou

class LZ_vex_interface(QtWidgets.QWidget):
	def __init__(self,scipt = 'lz_quick_vex',rows = 4):
		super(LZ_vex_interface, self).__init__() 
		#create Layout
		mainLayout = QtWidgets.QGridLayout()		
		self.callbackDict = {}

		# read json
		import json
		hext = hou.expandString('$HEXT')
		self.json = json.load(open(hext + '/' + scipt +'.txt'))
		
		i = 0
		# fill lists
		for list_key in sorted(self.json.keys()):
			# create list widget
			new_list = QtWidgets.QListWidget()
			items = self.json[list_key]
			
			for key in sorted(items.keys()):
				list_item = QtWidgets.QListWidgetItem(key)

				
				picName =  key.split(". ")[len(key.split(". "))-1].lower().replace(":","").replace(" ","")
				#print picNam
				pic_path = hou.expandString('$HEXT\pic') + '\\' + picName + r".svg"
				if os.path.isfile(pic_path):
					list_item.setIcon(QtGui.QIcon(pic_path))
				new_list.addItem(list_item)
				self.callbackDict[key] = items[key]
			new_list.doubleClicked.connect(self.doubleClickedList)
		   
			# create label
			label = QtWidgets.QLabel(list_key)
			
			#fill
			layout = QtWidgets.QVBoxLayout()			 
			layout.addWidget(label)
			layout.addWidget(new_list)
			mainLayout.addLayout(layout,i/rows,i%rows)
			i += 1
		 
		#set Layout
		self.setLayout(mainLayout)
		  
	# FUNCTIONS	
	def doubleClickedList(self,item):
		item = self.callbackDict[item.data()]
		# process view node
		n = lzutil.viewNode()
		self.processItem(item,n)
  
	def processItem(self,item,n):
		# add libs
		if item.has_key('lib'):
			for lib in item['lib']:
				lzutil.includeAddSafe(n,lib)
		# add code
		if item.has_key('code'):			
			lzutil.snippetAddCode(n,item['code']) 
		# execute an action
		if item.has_key('action'):
			exec(item['action'])
		# node	
		if item.has_key('node'):
			new_node = n.createOutputNode(item['node'])
			new_node.setSelected(1,1)
			new_node.setDisplayFlag(1)
			new_node.setRenderFlag(1)
		# clipboard
		if item.has_key('clip'):			
			lzutil.copyToClipboard(item['clip'])