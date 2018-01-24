import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication,QMenu,QAction,QComboBox,QInputDialog,QLineEdit,QFileDialog)
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5 import QtCore
from glob import glob
import os
import subprocess
import json
import shutil
from pathlib import Path

class Example(QWidget):

    def __init__(self):
        super().__init__()
        # Layouts
        self.vbox = QVBoxLayout()
        self.shotsBox = QVBoxLayout()

        # STRUCTURE
        self.structure = {
            "Anim": [],
            "Layout": ["mb", "ma"],
            "Houdini": ["hip"],
            "Nuke": ["nk"],
            "Render": []
        }


        # DATA
        self.inifile = 'settings.txt'
        self.initSettings()
        self.shotDict = dict()
        self.initUI()

    def initSettings(self):
        self.settings = json.load(open(self.inifile))
        self.projectsFolder = self.settings['projectsFolder'].replace("\\\\","\\")
        self.currProject = self.settings['currProject']
        self.projects = self.settings['projects']
        for key in self.projects.keys():
            self.projects[key].replace("\\\\","\\")

        self.size = int(self.settings['icon_size'])
        self.iconScale = 0.95

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
        # We need to check if our string matches the s000 pattern
        if len(dirName)==4 and dirName[1].isdigit():
            shotNum = int(dirName.split("s").pop())//10
            self.lastShot = max(self.lastShot,shotNum)

            # Directory Button
            dirButton = QPushButton(dirName)
            dirButton.clicked.connect(lambda state, _dir=dir: subprocess.Popen('explorer "' + _dir + '"'))
            shotBox.addWidget(dirButton)

            # Create Preview Icon
            previewImgPath = dir + "preview.jpg"
            previewImgFile = Path(previewImgPath)
            if previewImgFile.exists():
                previewImg = QLabel()
                pixMap = QPixmap(previewImgPath)
                pixMap = pixMap.scaled(self.size, self.size)
                previewImg.setPixmap(pixMap)
                previewImg.setFixedSize(self.size, self.size)
                shotBox.addWidget(previewImg)

            # create buttons and add calbacks
            buttonLabels =  self.structure.keys()
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
                ext =  self.structure[buttonLabel]
                button.customContextMenuRequested.connect(lambda point,button=button,_dir=dir + buttonLabel,_ext = ext:self.on_context_menu(point,button,_dir,_ext))

                # add button to current shot
                shotBox.addWidget(button)

            # add shot to shot box
            self.shotsBox.addLayout(shotBox)

    def createTopBar(self):
        #Create top bar
        self.topBar = QHBoxLayout()
        self.createProjectComboBox()

        # add projects button
        addProj = QPushButton("+")
        addProj.setFixedSize(self.size  , self.size )
        addProj.clicked.connect(self.addProjects)
        self.topBar.addWidget(addProj)

        # remove Project Button
        removeProj = QPushButton("-")
        removeProj.setFixedSize(self.size, self.size)
        removeProj.clicked.connect(self.removeProject)
        self.topBar.addWidget(removeProj)

        # update button
        update = QPushButton("Update")
        update.setFixedSize(self.size * 2 , self.size )
        update.clicked.connect(self.updateShotsBox)
        self.topBar.addWidget(update)

        self.vbox.addLayout(self.topBar)

    def createProjectComboBox(self):
        # select project
        self.ProjectComboBox = QComboBox();
        # Fill combo box new
        self.updateComboBox()

        if self.currProject is not "":
            self.ProjectComboBox.setCurrentIndex(list(self.projects.keys()).index(self.currProject))

        self.ProjectComboBox.currentIndexChanged.connect(self.projectChanged)
        self.topBar.addWidget(self.ProjectComboBox)

    def updateComboBox(self):
        self.ProjectComboBox.clear()
        for key in self.projects.keys():
             self.ProjectComboBox.addItem(key, self.projects[key])

        #if self.currProject is not "":
        #    self.ProjectComboBox.setCurrentIndex(self.projects.keys().index(self.currProject))

    def projectChanged(self):
        self.clearLayout(self.shotsBox)
        if self.ProjectComboBox.currentText() in self.projects.keys():
            self.currProject = self.ProjectComboBox.currentText()
            self.saveSettings()
            self.updateShotsBox()

    def updateShotsBox(self):
        self.clearLayout(self.shotsBox)
        self.lastShot = 0
        if self.currProject is not "":
            self.sourceFolder = self.projects[self.currProject]
            dirs = glob(self.sourceFolder + "\\s*\\")
            for dir in dirs:
                self.addShotButtons(dir)

    def addProjects(self):
        # Add Projects t oselectable projects
        # Ask user to select paths
        paths = []
        file_dialog = QFileDialog(directory=self.projectsFolder)
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        file_view = file_dialog.findChild(QListView, 'listView')

        # to make it possible to select multiple directories:
        if file_view:
            file_view.setSelectionMode(QAbstractItemView.MultiSelection)
        f_tree_view = file_dialog.findChild(QTreeView)
        if f_tree_view:
            f_tree_view.setSelectionMode(QAbstractItemView.MultiSelection)

        if file_dialog.exec():
            paths = file_dialog.selectedFiles()

        for path in paths:
            path = path.replace("/", "\\")
            self.projects[path.split("\\").pop()] = path

        self.saveSettings()
        self.updateComboBox()

    def removeProject(self):
        projToRemove = self.ProjectComboBox.currentText()
        self.currProject = ""
        self.ProjectComboBox.removeItem(self.ProjectComboBox.currentIndex())
        self.projects.pop(projToRemove,None)
        self.saveSettings()

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

    def createBotBar(self):
        self.botBar = QHBoxLayout()

        # add shots button
        addShot = QPushButton("+Add Shot")
        addShot.clicked.connect(self.addShot)
        self.botBar.addWidget(addShot)

        # add shots button
        createBase = QPushButton("CreateBase")
        createBase.clicked.connect(self.createBase)
        self.botBar.addWidget(createBase)

        self.vbox.addLayout(self.botBar)

    def addShot(self):
        if self.currProject is not "":
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

    def createBase(self):
        if self.currProject is not "":
            defaultFolders = ["Previs","Render","Assets"]
            for dir in defaultFolders:
                os.makedirs(self.sourceFolder + "/" + dir)
            shutil.copy2("seafile-ignore.txt",self.sourceFolder + "/")

    def initUI(self):
        self.createTopBar()
        self.createRootBar()
        self.createAssetsBar()

        # shots box
        self.updateShotsBox()
        self.vbox.addLayout(self.shotsBox)
        self.vbox.addStretch()

        self.createBotBar()

        # add test button
        test = QPushButton("test")
        test.clicked.connect(self.test)
        self.vbox.addWidget(test)

        self.setLayout(self.vbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Canoe:Harbor')
        self.show()

    def test(self):
        print ("test")

    def saveSettings(self):
        self.settings["projectsFolder"] = self.projectsFolder
        projects = dict()
        for key in self.projects.keys():
            projects[key] = self.projects[key]
        self.settings["projects"] = projects
        self.settings["currProject"] = self.currProject

        # write to file
        with open(self.inifile, 'w') as outfile:
            json.dump(self.settings, outfile)

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