import hou
import toolutils
import subprocess

def createTopoHelper(topobuild):
	n = topobuild
	ref = n.inputs()[1]
	#create ref_vis node
	#ref_vis = ref.createOutputNode("null","ref_vis")
	#ref_vis.setPosition(n.position() + hou.Vector2(2.25,0))
	
	geo = n.parent().parent().createNode('geo',n.name()+'_temp_vis')
	geo.node('file1').destroy()
	
	object_merge1 = geo.createNode("object_merge","object_merge1")
	object_merge1.parm("objpath1").set('`opinputpath("' + n.path() + '",1)`')

def removeTopoHelper(topobuild):
	n = topobuild
	geo = n.parent().parent().node(n.name()+'_temp_vis').destroy()
	
	
# Snippets and noises	
def snippetAddCodeAtStart(n,code):
	snippet = n.parm('snippet')
	if snippet is not None:
		snippet.set(code + '\n' +  snippet.eval())

def snippetAddCode(n,code):
	snippet = n.parm('snippet')
	if snippet is not None:	
		snippet.set(snippet.eval() + '\n' + code)

		
def createNoiseFolderParmTemplate(id):
    a_parm = hou.FloatParmTemplate('a'+id,'a'+id,1,default_value = (1,))
    f_parm = hou.FloatParmTemplate('f'+id,'f'+id,1,default_value = (1,))   
    noise_folder = hou.FolderParmTemplate('noise'+id,'Noise'+id,parm_templates = (a_parm,f_parm),folder_type = hou.folderType.Simple)
    return noise_folder	

# checks if node is a snippet and if it has a folder with noises, adds a noise and creates spare amp and freq
def addNoiseScriptAndParmsToSnippet(n,dim = 'float',fun = 'pfn'):
	if n.parm('snippet') is not None:
	#if n.type().name() == 'attribwrangle' or n.type().name() =='volumewrangle': 
		includeAddSafe(n,'lzn')
		ptg = n.parmTemplateGroup()    
		parm = ptg.findFolder('Noises')
		if parm is None:
			parm = hou.FolderParmTemplate('noises','Noises',folder_type = hou.folderType.Simple)
			ptg.addParmTemplate(parm)
			
		noise_id = len(parm.parmTemplates()) + 1
		noise_folder =  createNoiseFolderParmTemplate(str(noise_id))
		
		new_code = "{n_dim} n{id} = ch('a{id}') * {n_fun}(@P * ch('f{id}'));".format(id = noise_id,n_dim = dim,n_fun=fun)
		snippetAddCode(n,new_code)   
		ptg.appendToFolder(parm,noise_folder)    
		n.setParmTemplateGroup(ptg)  	

def includeAddSafe(n,lib):
	snippet = n.parm('snippet')
	if snippet is not None:
		code = snippet.eval()
		if code.find('#include <' + lib +'.h>') == -1:
			snippetAddCodeAtStart(n,'#include <' + lib +'.h>')

def viewNode():
	return toolutils.sceneViewer().currentNode()

def openFolderFromEnv(env):
	dir = hou.expandString(env).replace('/','\\')
	subprocess.Popen('explorer "' + dir  + '"')

def setProject():
	import os
	# get root dir
	start_dir = hou.expandString("$HMEGA") + "/! Projects/"
	answer = hou.ui.selectFile(start_directory=start_dir,file_type=hou.fileType.Directory)

	if answer is not '':
		# Make dirs
		os.makedirs(answer)
		os.makedirs(answer + "/hip")
		os.makedirs(answer + "/flipbook")
		os.makedirs(answer + "/render")
		
		hipname = answer.split("/").pop()
		
		hou.appendSessionModuleSource("import lzutil\nlzutil.updateJobFromHipLocation()")
		
		hou.hscript('setenv JOBNAME ='+ hipname)
		#print answer
		hou.hscript('setenv JOB ='+ answer)    
		
		hou.hipFile.save(answer + "/hip/" + hipname +".000" +".hip")   

def updateJobFromHipLocation():
	import os
	hip = hou.expandString("$HIP")
	JOB = os.path.dirname(hip)
	hou.hscript('setenv JOB ='+ JOB)
	
def updateJobNameFromHipLocation():
	import os
	hip = hou.expandString("$HIP")
	JOB = os.path.dirname(hip)
	jobname = JOB.split("/").pop()
	hou.hscript('setenv JOBNAME ='+ jobname)		
	
			
def copyToClipboard(str):
	#import PySide.QtGui as qtg
	#app = qtg.QApplication.instance()
	#clipboard = app.clipboard()
	#clipboard.setText(str)
	from PySide2.QtWidgets  import  QApplication
	QApplication.clipboard().setText(str)
	
def updateSnippetFromClipboard(node):
	snippet = node.parm('snippet')
	if snippet is not None:
		from PySide2.QtWidgets  import  QApplication
		code =  QApplication.clipboard().text()
		code =  code.replace('\t', '    ')
		snippet.set(code)

# installs all hdas from a  lib directory in $hext/otls		
def installOtlLib(lib):
	import hou,glob

	hext = hou.expandString('$OTLS')

	path = hext + "/" + lib + "/*.hda"
	otls = glob.glob(path)
	for otl in otls:
		hou.hda.installFile(otl)

# shows a ui to install libs in current hip file, then adds their installation to the python source editor		
def installOtlLibsUI():
	import glob
	path = hou.expandString('$OTLS') + "\\*/"
	libs =  glob.glob(path)
	libs = [e.split("\\")[-2] for e in libs]
	print libs

	answer =  hou.ui.selectFromList(libs)
	for ans in answer:
		lib = libs[ans]
		installOtlLib(lib)
		print  "\nimport lzutil\nlzutil.installOtlLib('"+lib +"')"
		hou.appendSessionModuleSource( "import lzutil\nlzutil.installOtlLib('"+lib +"')" )



	