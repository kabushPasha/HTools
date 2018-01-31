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
import errno

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
        self.sourceFolder = ""
        self.initSettings()
        self.shotDict = dict()
        self.shotsInfo = dict()

        self.initUI()

    def initSettings(self):
        self.settings = json.load(open(self.inifile))
        self.projectsFolder = self.settings['projectsFolder'].replace("\\\\","\\")
        self.currProject = self.settings['currProject']
        self.projects = self.settings['projects']
        self.MayaVersion = self.settings['MayaVersion']
        self.MayaInstallDir = self.settings['MayaInstallDir']
        self.MplayFormats = self.settings['MplayFormats']
        self.StatusDict = self.settings['StatusDict']

        self.Utils = self.settings['Utils']


        for key in self.projects.keys():
            self.projects[key].replace("\\\\","\\")

        self.size = int(self.settings['icon_size'])
        self.iconScale = 0.95

    def on_context_menu(self, point,button,dir,ext,buttonLabel,shotName):
        if buttonLabel == "Render":
            self.popMenu = QMenu(self)

            folders = glob(dir + "/*/")
            for folder in folders:
                folderName = folder.split("\\").pop(-2)
                subfolders = glob(folder + "*/")
                # if it has no subfodlers add this thing as an action
                if subfolders == []:
                    openFolder = QAction(folderName, self)
                    openFolder.setData(["file",folder])
                    self.popMenu.addAction(openFolder)
                # else create an action for every pass
                else:
                    folderMenu = self.popMenu.addMenu(folderName)

                    for subfolder in subfolders:
                        subFolderName = subfolder.split("\\").pop(-2)
                        openFolder = QAction(subFolderName, self)
                        openFolder.setData(["file",subfolder])
                        folderMenu.addAction(openFolder)

            self.popMenu.addSeparator()
            # create change status actions
            for status in self.StatusDict.keys():
                setFinishedStatus = QAction(status, self)
                setFinishedStatus.setData(["status",shotName,status,buttonLabel])
                self.popMenu.addAction(setFinishedStatus)

            self.popMenu.triggered[QAction].connect(self.processRenderMenu)
            self.popMenu.exec_(button.mapToGlobal(point))

        else:
            self.popMenu = QMenu(self)
            # Find all files that match the extension
            files = []
            if ext == []:
                files = glob(dir + "\*")
            else:
                for e in ext:
                    files += glob(dir + "\*." + e)

            # create open file actions
            for file in files:
                fileName =  file.split("\\").pop(-1)
                fileAction = QAction(fileName, self)
                fileAction.setData([file,buttonLabel,"file"])
                self.popMenu.addAction(fileAction)

            self.popMenu.addSeparator()
            # create change status actions
            for status in self.StatusDict.keys():
                setFinishedStatus = QAction(status, self)
                setFinishedStatus.setData([status, buttonLabel,"status",shotName])
                self.popMenu.addAction(setFinishedStatus)



            self.popMenu.triggered[QAction].connect(self.processContextMenu)
            self.popMenu.exec_(button.mapToGlobal(point))

    # Open sequences in Mplay
    def processRenderMenu(self,q):
        type = q.data()[0]
        if type == "file":
            folder = q.data()[1]
            hinst = os.environ['HINST']

            command = []
            command += [hinst + "/bin/mplay.exe"]
            for format in self.MplayFormats:
                command += [folder + "*." + format]

            subprocess.Popen(command)
        elif type == "status":
            status = q.data()[2]
            shotName = q.data()[1]
            button = q.data()[3]

            self.shotsInfo[shotName]['shotProgress'][button] = status;
            self.saveShotsInfo()
            self.updateShotsBox()

    def processContextMenu(self,q):
        file = q.data()[0]
        button = q.data()[1]
        action = q.data()[2]

        if action == "file":
            #kinda bad but we'll see if we can wrap it in any other way
            if button == "Layout":
                self.statusBar.showMessage("Openning Maya Scene: " + file)
                command = []
                command += [self.MayaInstallDir + "\\Maya20" +self.MayaVersion + "\\bin\\maya.exe"]
                command += ["-command"]
                command += ['loadPlugin "AbcExport";loadPlugin "AbcImport";file -f -open \"'+ file.replace("\\","/") +'\";']
                command += ["-proj"]
                command += [os.path.dirname(os.path.dirname(file))]

                subprocess.Popen(command,shell=True)
            elif button == "Houdini":
                self.statusBar.showMessage("Opening Houdini Scene: " + file)
                subprocess.Popen([file],shell=True)
            elif button == "Render":
                self.statusBar.showMessage("Opening Sequence in mplay")
            elif button == "Nuke":
                self.statusBar.showMessage("Opening Nuke Project: " + file)
                subprocess.Popen([file], shell=True)
        elif action == "status":
            status = file;
            shotName = q.data()[3]

            self.shotsInfo[shotName]['shotProgress'][button] = status;
            self.saveShotsInfo()
            self.updateShotsBox()



    def addShotButtons(self,dir):
        shotBox = QHBoxLayout()
        dirName = dir.split("\\").pop(-2)
        self.shotDict[dirName] = dir;
        # We need to check if our string matches the s000 pattern
        if len(dirName)==4 and dirName[1].isdigit():
            # update last available shot in this project(used for adding new shots)
            shotNum = int(dirName.split("s").pop())//10
            self.lastShot = max(self.lastShot,shotNum)

            # Process Shots info
            frameRange = [0,240]
            shotLabel = "untitled"
            shotProgress = {}
            for step in self.structure.keys():
                shotProgress[step] = "";
            #  check there is info about current shot,if not save shots info
            if dirName in self.shotsInfo.keys():
                shotInfo = self.shotsInfo[dirName]
                shotLabel = shotInfo['Label']
                frameRange = shotInfo['FrameRange']
                shotProgress = shotInfo['shotProgress']
            else:
                shotInfo = {}
                shotInfo['Label'] = shotLabel
                shotInfo['FrameRange'] = frameRange
                shotInfo['shotProgress'] = shotProgress
                self.shotsInfo[dirName] = shotInfo
                self.saveShotsInfo()

            # Directory Button
            frameRangeText = str(frameRange[0]) + "-" + str(frameRange[1]) + " ("  + str(frameRange[1] - frameRange[0]) + ")"
            frameRangeText = frameRangeText

            vbox = QVBoxLayout()

            dirButton = QPushButton(" " + dirName +": " + shotLabel)
            dirButton.setStyleSheet("Text-align:left;")
            dirButton.clicked.connect(lambda state, _dir=dir: self.safeOpen(_dir))
            # Set shot status to finished if all the steps are finished

            if all(value == "finished" for value in shotProgress.values()):
                dirButton.setStyleSheet("Text-align:left;background-color:rgb(" + self.StatusDict["finished"] + ")");

            vbox.addWidget(dirButton)

            frameRangeWidget = QLabel(frameRangeText)
            frameRangeWidget.setStyleSheet("font: 6pt")
            vbox.addWidget(frameRangeWidget)

            shotBox.addLayout(vbox)



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
                button.clicked.connect(lambda state, _dir=dir + buttonLabel: self.safeOpen(_dir))
                # set icon and icon size
                button.setFixedSize(self.size, self.size)
                button.setIcon(QIcon(QPixmap('icons/' + buttonLabel + '.png')))
                button.setIconSize(QtCore.QSize(self.size ** self.iconScale, self.size * self.iconScale));

                status = shotProgress[buttonLabel]
                if status != "":
                    color = self.StatusDict[status]
                    button.setStyleSheet("background-color:rgb(" + color + ")");

                # Context Menus
                button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                ext =  self.structure[buttonLabel]
                button.customContextMenuRequested.connect(lambda point,button=button,_dir=dir + buttonLabel,_ext = ext,_buttonLabel = buttonLabel,_dirName = dirName:self.on_context_menu(point,button,_dir,_ext,_buttonLabel,_dirName))

                # add button to current shot
                shotBox.addWidget(button)

            # add shot to shot box
            self.shotsBox.addLayout(shotBox)

    def AddIcon(self,button,icon):
        # Process Icon
        button.setText("")
        button.setFixedSize(self.size, self.size)
        button.setIcon(QIcon(QPixmap('icons/' + self.settings['Theme'] + '/' + icon + '.png')))
        button.setIconSize(QtCore.QSize(self.size ** self.iconScale, self.size * self.iconScale));
        button.setToolTip(icon)

    def createTopBar(self):
        #Create top bar
        self.topBar = QHBoxLayout()
        self.createProjectComboBox()

        # add projects button
        addProj = QPushButton("+")
        addProj.clicked.connect(self.addProjects)
        self.AddIcon(addProj,"AddProj")
        self.topBar.addWidget(addProj)

        # remove Project Button
        removeProj = QPushButton("-")
        removeProj.clicked.connect(self.removeProject)
        self.AddIcon(removeProj, "RemProj")
        self.topBar.addWidget(removeProj)

        # update button
        update = QPushButton("Update")
        update.clicked.connect(self.updateShotsBox)
        self.AddIcon(update, "Update")
        self.topBar.addWidget(update)

        # move to bottom right
        moveToBR = QPushButton(">")
        moveToBR.clicked.connect(self.moveToBottomRight)
        self.AddIcon(moveToBR, "Dock")
        self.topBar.addWidget(moveToBR)

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
        tempCurrProject = self.currProject
        self.ProjectComboBox.clear()
        for key in self.projects.keys():
             self.ProjectComboBox.addItem(key, self.projects[key])

        if tempCurrProject is not "":
            self.currProject = tempCurrProject
            #self.ProjectComboBox.setCurrentText(self.currProject)
            index = self.ProjectComboBox.findText(self.currProject, QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.ProjectComboBox.setCurrentIndex(index)

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
            self.updateShotsInfo()
            dirs = glob(self.sourceFolder + "\\s*\\")
            for dir in dirs:
                self.addShotButtons(dir)
        self.moveToBottomRight()

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
            projName = path.split("\\").pop()
            self.projects[projName] = path
            self.currProject = projName
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

        # pick Maya Version
        self.MayaVersionComboBox = QComboBox();
        self.MayaVersionComboBox.addItem("Maya2018","18")
        self.MayaVersionComboBox.addItem("Maya2017","17")
        index = self.MayaVersionComboBox.findText("Maya20" + self.MayaVersion, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.MayaVersionComboBox.setCurrentIndex(index)
        self.MayaVersionComboBox.currentIndexChanged.connect(self.mayaVersionChanged)

        # open proj button
        openProj = QPushButton("Open")
        openProj.clicked.connect(lambda:self.safeOpen(""))
        self.AddIcon(openProj, "Open")

        # open previs button
        previs = QPushButton("Previs")
        previs.clicked.connect(lambda: self.safeOpen('\Previs'))
        self.AddIcon(previs, "Previs")

        # open render
        render = QPushButton("Render")
        render.clicked.connect(lambda: self.safeOpen('\Render'))
        self.AddIcon(render, "Render")

        #self.rootBar.addStretch()
        self.rootBar.addWidget(self.MayaVersionComboBox)
        self.rootBar.addWidget(openProj)
        self.rootBar.addWidget(previs)
        self.rootBar.addWidget(render)

        self.vbox.addLayout(self.rootBar)

    def mayaVersionChanged(self):
        self.MayaVersion = self.MayaVersionComboBox.currentData()
        self.saveSettings()

    def createAssetsBar(self):
        self.assetsBar = QHBoxLayout()
        char = QPushButton("Char")
        self.AddIcon(char, "Char")

        char.clicked.connect(lambda:self.safeOpen('\Assets\Char'))
        env = QPushButton("Env")
        self.AddIcon(env, "Env")
        env.clicked.connect(lambda: self.safeOpen('\Assets\Env'))

        newchar = QPushButton("CreateChar")
        self.AddIcon(newchar, "CreateChar")
        newchar.clicked.connect(lambda :self.createChar("Char"))
        newenv = QPushButton("CreateEnv")
        self.AddIcon(newenv, "CreateEnv")
        newenv.clicked.connect(lambda :self.createChar("Env"))

        #self.assetsBar.addWidget(char)
        #self.assetsBar.addWidget(env)
        #self.assetsBar.addWidget(newchar)
        #self.assetsBar.addWidget(newenv)

        self.rootBar.addWidget(char)
        self.rootBar.addWidget(env)
        self.rootBar.addWidget(newchar)
        self.rootBar.addWidget(newenv)

        #self.assetsBar.addStretch()
        #self.assetsBar.addWidget(self.MayaVersionComboBox)

        self.vbox.addLayout(self.assetsBar)

    def createChar(self,type):
        if self.currProject is not "":
            (text, truth) = QInputDialog.getText(self, "AssetName", "AssetName", QLineEdit.Normal, "NewAsset")
            if truth:
                assetPath = self.sourceFolder +'\\Assets\\'+ type +"\\" + text
                self.makedirs(assetPath)
                folders = ["Lookdev","Models","Textures"]
                if type is "Char":
                    folders.append("Groom")
                for folder in folders:
                    self.makedirs(assetPath + "\\" + folder)

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
            self.makedirs(self.sourceFolder + "/" + newShotName)
            self.makedirs(self.sourceFolder + "/" + newShotName + "/Houdini")
            self.makedirs(self.sourceFolder + "/" + newShotName + "/Anim")
            self.makedirs(self.sourceFolder + "/" + newShotName + "/Render")
            self.makedirs(self.sourceFolder + "/" + newShotName + "/Layout")
            self.makedirs(self.sourceFolder + "/" + newShotName + "/Nuke")

            addShot = QPushButton("+Add Shot")
            self.addShotButtons(self.sourceFolder + "\\"+ newShotName +"\\")

    def createBase(self):
        if self.currProject is not "":
            defaultFolders = ["Previs","Render","Assets","Assets/Char","Assets/Env"]
            for dir in defaultFolders:
                self.makedirs(self.sourceFolder + "/" + dir)
            shutil.copy2("seafile-ignore.txt",self.sourceFolder + "/")

    def createUtilsBar(self):
        self.UtilsBar = QHBoxLayout()

        for key in self.Utils.keys():
            button = QPushButton(key)
            if type(self.Utils[key]) == list:
                button.clicked.connect(lambda state,_key = key: subprocess.Popen(self.Utils[_key]))
            else:
                button.clicked.connect(lambda state, _key=key: os.system(self.Utils[_key]))
            self.AddIcon(button,key)

            button.setFixedSize(self.size, self.size)
            self.UtilsBar.addWidget(button)

        # Edit Shots Info
        editShotInfo = QPushButton("EditShotInfo")
        editShotInfo.clicked.connect(lambda:subprocess.Popen(["C:\\Program Files (x86)\\Notepad++\\notepad++.exe",self.sourceFolder + '\shots.info']))
        editShotInfo.setFixedSize(self.size, self.size)
        self.AddIcon(editShotInfo, "EditShotInfo")
        self.UtilsBar.addWidget(editShotInfo)

        # Update Project
        svn = "C:\\Program Files\\TortoiseSVN\\bin\\svn.exe"
        updateProject = QPushButton("UpdateProject")
        updateProject.clicked.connect(lambda :subprocess.Popen([svn,"update",self.sourceFolder]))
        #updateProject.clicked.connect(lambda _dir=self.sourceFolder:print([svn,"update",self.sourceFolder]))
        updateProject.setFixedSize(self.size, self.size)
        self.AddIcon(updateProject,"UpdateProject")
        self.UtilsBar.addWidget(updateProject)

        # Commit Project
        commitProject = QPushButton("CommitProject")
        commitProject.clicked.connect(lambda :subprocess.Popen([ "TortoiseProc.exe","/command:commit","/path:" + self.sourceFolder]))
        commitProject.setFixedSize(self.size, self.size)
        self.UtilsBar.addWidget(commitProject)
        self.AddIcon(commitProject, "CommitProject")
        self.vbox.addLayout(self.UtilsBar)

    # INIT UI
    def initUI(self):
        # Status bar
        self.statusBar = QStatusBar()

        self.createTopBar()
        self.createRootBar()
        self.createAssetsBar()

        # shots box
        self.updateShotsBox()
        self.vbox.addLayout(self.shotsBox)
        self.vbox.addStretch()

        self.createBotBar()
        self.createUtilsBar()

        # add test button
        test = QPushButton("test")
        test.clicked.connect(self.test)
        #self.vbox.addWidget(test)

        # Add status bar
        #self.vbox.addWidget(self.statusBar)

        self.setLayout(self.vbox)
        self.setGeometry(600, 600, 300, 150)
        self.setWindowTitle('Canoe:Harbor')
        self.show()
        self.moveToBottomRight()

    def test(self):
        self.statusBar.showMessage("INFO: " + str(self.sourceFolder))

    def moveToBottomRight(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()

        widget = self.geometry()
        x = ag.width() - widget.width() - 30
        y = 2 * ag.height() - sg.height() - widget.height() - 20
        self.move(x, y)

    def safeOpen(self,dir):
        if self.currProject is not "":
            # kinda clumsy but will fork for now
            if not dir.startswith(self.sourceFolder):
                dir = self.sourceFolder + dir
            if os.path.isdir(dir):
                subprocess.Popen('explorer "' + dir)
            else:
                self.statusBar.showMessage("WARNING: directory does not exist")
        else:
            self.statusBar.showMessage("WARNING: project not set,cant open folder")

    def updateShotsInfo(self):
        self.statusBar.showMessage("updated shots info")
        # Create Preview Icon
        shotInfoPath = self.sourceFolder + "\\shots.info"
        shotInfoFile = Path(shotInfoPath)
        if shotInfoFile.exists():
            self.shotsInfo = json.load(open(shotInfoPath))
        else:
            self.statusBar.showMessage("No Shots Info")
            self.shotsInfo = {}

    def saveSettings(self):
        self.settings["projectsFolder"] = self.projectsFolder
        projects = dict()
        for key in self.projects.keys():
            projects[key] = self.projects[key]
        self.settings["projects"] = projects
        self.settings["currProject"] = self.currProject
        self.settings['MayaVersion'] = self.MayaVersion
        # write to file
        with open(self.inifile, 'w') as outfile:
            json.dump(self.settings, outfile, indent=4)

    def saveShotsInfo(self):
        shotInfoPath = self.sourceFolder + "\\shots.info"
        with open(shotInfoPath, 'w') as outfile:
            json.dump(self.shotsInfo, outfile, indent=4)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def makedirs(self,dir):
        if self.currProject is not "":
            try:
                os.makedirs(dir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                else:
                    self.statusBar.showMessage("WARNING: " + dir + " already_exists!")

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())