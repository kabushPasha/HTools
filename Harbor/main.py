import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication,QMenu,QAction,QComboBox,QInputDialog,QLineEdit)
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5 import QtCore
from glob import glob
import os
import subprocess

class Example(QWidget):

    def __init__(self):
        super().__init__()
        # Layouts
        self.vbox = QVBoxLayout()
        self.shotsBox = QVBoxLayout()

        # DATA
        #self.projectsFolder = "D:\Pasha\Test"
        self.projectsFolder = "S:"
        self.sourceFolder = ""
        self.shotDict = dict()

        self.size = 50
        self.iconScale = 0.95

        self.initUI()

    def addShot(self):
        newShotName = 's{0:02d}0'.format(self.lastShot+1)
        # Create Fodler Structure
        os.makedirs(self.sourceFolder + "/" + newShotName)
        os.makedirs(self.sourceFolder + "/" + newShotName + "/Houdini")
        os.makedirs(self.sourceFolder + "/" + newShotName + "/Anim")
        os.makedirs(self.sourceFolder + "/" + newShotName + "/Render")
        os.makedirs(self.sourceFolder + "/" + newShotName + "/Layout")
        os.makedirs(self.sourceFolder + "/" + newShotName + "/Nuke")

        addShot = QPushButton("+Add Shot")
        self.addShotButtons(self.sourceFolder + "\\"+ newShotName +"\\")

    def on_context_menu(self, point,button,dir,ext):
        self.popMenu = QMenu(self)
        # Find all files that match the extension
        files = []
        if ext == []:
            files = glob(dir + "\*")
        else:
            for e in ext:
                files += glob(dir + "\*." + e)

        for file in files:
            fileName =  file.split("\\").pop(-1)
            fileAction = QAction(fileName, self)
            fileAction.setData(file)
            self.popMenu.addAction(fileAction)
        self.popMenu.triggered[QAction].connect(self.processContextMenu)
        self.popMenu.exec_(button.mapToGlobal(point))

    def processContextMenu(self,q):
        print(q.text() + " is triggered")
        print(q.data())

    def addShotButtons(self,dir):
        shotBox = QHBoxLayout()
        dirName = dir.split("\\").pop(-2)

        self.shotDict[dirName] = dir;
        shotNum = int(dirName.split("s").pop())//10
        self.lastShot = max(self.lastShot,shotNum)

        # Create Buttons
        # Directory Button
        dirButton = QPushButton(dirName)
        dirButton.clicked.connect(lambda state, _dir=dir: subprocess.Popen('explorer "' + _dir + '"'))
        shotBox.addWidget(dirButton)


        buttonLabels = ["Anim","Layout","Houdini","Nuke","Render"]
        extensions = {
                        "Anim":[],
                        "Layout":["mb","ma"],
                        "Houdini":["hip"],
                        "Nuke":["nk"],
                        "Render":[]
        }

        # create buttons and add calbacks
        for buttonLabel in buttonLabels:
            # Create button
            button = QPushButton("")
            # Add callback
            button.clicked.connect(lambda state, _dir=dir + buttonLabel: subprocess.Popen('explorer "' + _dir + '"'))
            # set icon and icon size
            button.setFixedSize(self.size, self.size)
            button.setIcon(QIcon(QPixmap('icons/' + buttonLabel + '.png')))
            button.setIconSize(QtCore.QSize(self.size ** self.iconScale, self.size * self.iconScale));

            # Context Menus
            button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            ext = extensions[buttonLabel]
            button.customContextMenuRequested.connect(lambda point,button=button,_dir=dir + buttonLabel,_ext = ext:self.on_context_menu(point,button,_dir,_ext))

            # add button to current shot
            shotBox.addWidget(button)

        # add shot to shot box
        self.shotsBox.addLayout(shotBox)

    def updateShotsBox(self):
        self.clearLayout(self.shotsBox)
        self.lastShot = 0
        dirs = glob(self.sourceFolder + "/s*/")
        for dir in dirs:
            self.addShotButtons(dir)


    def createProjectComboBox(self):
        # select project
        self.ProjectComboBox = QComboBox();
        dirs = glob(self.projectsFolder + "/*/")
        for dir in dirs:
            print(dir)
            dirName = dir.split("\\")[-2]
            self.ProjectComboBox.addItem(dirName, dir)
        self.ProjectComboBox.currentIndexChanged.connect(self.projectChanged)
        self.sourceFolder = dirs[0]

        self.topBar.addWidget(self.ProjectComboBox)


    def projectChanged(self):
        print(self.ProjectComboBox.currentData())
        print(self.sourceFolder )
        self.sourceFolder = self.ProjectComboBox.currentData()
        print(self.sourceFolder)
        self.updateShotsBox()

    def createTopBar(self):
        #Create top bar
        self.topBar = QHBoxLayout()
        self.createProjectComboBox()

        # update button
        update = QPushButton("Update")
        update.setFixedSize(self.size * 2 , self.size )
        update.clicked.connect(self.updateShotsBox)
        self.topBar.addWidget(update)

        self.vbox.addLayout(self.topBar)

    def createRootBar(self):
        self.rootBar = QHBoxLayout()

        # open proj button
        openProj = QPushButton("Open")
        openProj.clicked.connect(lambda:subprocess.Popen('explorer "' + self.sourceFolder))
        self.rootBar.addWidget(openProj)

        # open previs button
        previs = QPushButton("Previs")
        previs.clicked.connect(lambda: subprocess.Popen('explorer "' + self.sourceFolder + 'Previs"'))
        self.rootBar.addWidget(previs)

        # open render
        render = QPushButton("Render")
        render.clicked.connect(lambda: subprocess.Popen('explorer "' + self.sourceFolder + 'Render"'))
        self.rootBar.addWidget(render)
        self.vbox.addLayout(self.rootBar)


    def createAssetsBar(self):
        self.assetsBar = QHBoxLayout()
        char = QPushButton("Char")

        char.clicked.connect(lambda:subprocess.Popen('explorer "' + self.sourceFolder + 'Assets\Char"'))
        env = QPushButton("Env")
        env.clicked.connect(lambda: subprocess.Popen('explorer "' + self.sourceFolder + 'Assets\Env"'))

        newchar = QPushButton("CreateChar")
        newchar.clicked.connect(lambda :self.createChar("Char"))
        newenv = QPushButton("CreateEnv")
        newenv.clicked.connect(lambda :self.createChar("Env"))

        self.assetsBar.addWidget(char)
        self.assetsBar.addWidget(env)
        self.assetsBar.addWidget(newchar)
        self.assetsBar.addWidget(newenv)
        self.vbox.addLayout(self.assetsBar)

    def createChar(self,type):
        (text, truth) = QInputDialog.getText(self, "AssetName", "AssetName", QLineEdit.Normal, "NewAsset")
        if truth:
            assetPath = self.sourceFolder +'Assets\\'+ type +"\\" + text
            os.makedirs(assetPath)
            folders = ["Lookdev","Models","Textures"]
            if type is "Char":
                folders.append("Groom")
            for folder in folders:
                os.makedirs(assetPath + "\\" + folder)

    def initUI(self):
        self.createTopBar()
        self.createRootBar()
        self.createAssetsBar()


        # shots box
        self.updateShotsBox()
        self.vbox.addLayout(self.shotsBox)
        self.vbox.addStretch()

        # add shots button
        addShot = QPushButton("+Add Shot")
        addShot.clicked.connect(self.addShot)
        self.vbox.addWidget(addShot)

        # add shots button
        test = QPushButton("test")
        test.clicked.connect(self.test)
        self.vbox.addWidget(test)

        self.setLayout(self.vbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Canoe:Harbor')
        self.show()

    def test(self):
        #(text, truth) = QInputDialog.getText(self, "Get text", "User name", QLineEdit.Normal, "NoName")
        #if truth:
            # The user has accepted the edit, he/she has clicked OK
        #    print(text)
        print(self.sourceFolder)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())