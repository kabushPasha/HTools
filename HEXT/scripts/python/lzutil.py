import hou
import toolutils
import subprocess
import socket
import os
import string
import ftplib
import lzftp

import_hou_str = """
def enableHouModule():
	'''Set up the environment so that "import hou" works.'''
	import sys, os

	# Importing hou will load Houdini's libraries and initialize Houdini.
	# This will cause Houdini to load any HDK extensions written in C++.
	# These extensions need to link against Houdini's libraries,
	# so the symbols from Houdini's libraries must be visible to other
	# libraries that Houdini loads.  To make the symbols visible, we add the
	# RTLD_GLOBAL dlopen flag.
	if hasattr(sys, "setdlopenflags"):
		old_dlopen_flags = sys.getdlopenflags()
		sys.setdlopenflags(old_dlopen_flags | os.RTLD_GLOBAL)

	# For Windows only.
	# Add %HFS%/bin to the DLL search path so that Python can locate
	# the hou module's Houdini library dependencies.  Note that 
	# os.add_dll_directory() does not exist in older Python versions.
	# Python 3.7 users are expected to add %HFS%/bin to the PATH environment
	# variable instead prior to launching Python.
	if sys.platform == "win32" and hasattr(os, "add_dll_directory"):
		os.add_dll_directory("{}/bin".format(os.environ["HFS"]))

	try:
		import hou
	except ImportError:
		# If the hou module could not be imported, then add 
		# $HFS/houdini/pythonX.Ylibs to sys.path so Python can locate the
		# hou module.
		sys.path.append(os.environ['HHP'])
		import hou
	finally:
		# Reset dlopen flags back to their original value.
		if hasattr(sys, "setdlopenflags"):
			sys.setdlopenflags(old_dlopen_flags)

enableHouModule()
"""


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

def addCodeToPythonSnippet(n,code,code_name = "Python"):
	'''
	code_name = code_name.replace(" ","_")
	snippet = n.parm('code')
	if snippet is not None:	
		snippet.set(snippet.eval() + '\n' + code)
	else:	
		# if its a null create 	
		if n.type().name() == 'null':
			addPythonSnippet(n)
			n.parm('code').set(code)
		# else create output null
		else:
			new_null = n.createOutputNode("null",code_name)
			addPythonSnippet(new_null)
			new_null.parm('code').set(code)
	'''
	code_name = code_name.replace(" ","_")
	if n.type().name() != 'null':
		n = n.createOutputNode("null",code_name)
		
	for code_snippet in code:
		index = addPythonSnippet(n)
		index_str = str(index) if index > 0 else ""
		n.parm("lzPython_code" + index_str).set(code_snippet)
		RenamePythonSnippetFromFirstLine(n,index)



	
	
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
	t_parm = hou.IntParmTemplate('t'+id,'t'+id,1,default_value = (3,))   
	r_parm = hou.FloatParmTemplate('r'+id,'r'+id,1,default_value = (0.5,))   
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
# Curl Noise(ALL PARAMETERS)
def createCurlNoiseFolderParmTemplate(id):
	a_parm = hou.FloatParmTemplate('a'+id,'Amp'+id,1,default_value = (1,))
	f_parm = hou.FloatParmTemplate('f'+id,'Freq'+id,1,default_value = (1,))   
	t_parm = hou.IntParmTemplate('t'+id,'Turb'+id,1,default_value = (3,))   
	o_parm = hou.FloatParmTemplate('o'+id,'Offset'+id,1,default_value = (0,)) 
	r_parm = hou.FloatParmTemplate('r'+id,'Rough'+id,1,default_value = (0.5,))   
	at_parm = hou.FloatParmTemplate('at'+id,'Atten'+id,1,default_value = (0.5,))   
	ef_parm = hou.FloatParmTemplate('ef'+id,'Effect'+id,1,default_value = (1,))   
	type_parm = hou.StringParmTemplate('type'+id,'NoiseType'+id,1,default_value = ("p",),\
	menu_items =("p","o","s","a","x"),\
	menu_labels =("Perlin","OriginalPerlin","SparseConvultion","Alligator","Simplex"),\
	join_with_next=True)   
	sdf_parm = hou.StringParmTemplate('sdf'+id,'SDF'+id,1,default_value = ("",),\
	default_expression=("i2()",)) 

	noise_folder = hou.FolderParmTemplate('noise'+id,'Noise'+id,\
	parm_templates = (a_parm,f_parm,t_parm,o_parm,r_parm,at_parm,type_parm,sdf_parm,ef_parm),\
	folder_type = hou.folderType.Simple)

	return noise_folder	
	
def createTurbNoiseFolderParmTemplate(id):
	a_parm = hou.FloatParmTemplate('a'+id,'Amp'+id,1,default_value = (1,))
	f_parm = hou.FloatParmTemplate('f'+id,'Freq'+id,1,default_value = (1,))   
	t_parm = hou.IntParmTemplate('t'+id,'Turb'+id,1,default_value = (5,))   
	r_parm = hou.FloatParmTemplate('r'+id,'Rough'+id,1,default_value = (0.5,))   
	at_parm = hou.FloatParmTemplate('at'+id,'Atten'+id,1,default_value = (1.0,))   
  
	type_parm = hou.StringParmTemplate('type'+id,'NoiseType'+id,1,default_value = ("a",),\
	menu_items =("p","o","s","a","x","c"),\
	menu_labels =("Perlin","OriginalPerlin","SparseConvultion","Alligator","Simplex","CorrectedPerlin"),\
	join_with_next=True)   

	noise_folder = hou.FolderParmTemplate('noise'+id,'Noise'+id,\
	parm_templates = (a_parm,f_parm,t_parm,r_parm,at_parm,type_parm),\
	folder_type = hou.folderType.Simple)

	return noise_folder	
	
def createFlowNoiseFolderParmTemplate(id):
	a_parm = hou.FloatParmTemplate('a'+id,'Amp'+id,1,default_value = (1,))
	f_parm = hou.FloatParmTemplate('f'+id,'Freq'+id,1,default_value = (1,))   
	t_parm = hou.IntParmTemplate('t'+id,'Turb'+id,1,default_value = (3,))   
	o_parm = hou.FloatParmTemplate('o'+id,'Offset'+id,1,default_value = (0,)) 
	r_parm = hou.FloatParmTemplate('r'+id,'Rough'+id,1,default_value = (0.5,))   
	flow = hou.FloatParmTemplate('flow'+id,'Flow'+id,1,default_value = (0,))   
	flowrate = hou.FloatParmTemplate('flowrate'+id,'FlowRate'+id,1,default_value = (1,))   
	selfAdvect = hou.FloatParmTemplate('selfAdvect'+id,'SelfAdvect'+id,1,default_value = (0,))   
		

	noise_folder = hou.FolderParmTemplate('noise'+id,'Noise'+id,\
	parm_templates = (a_parm,f_parm,t_parm,o_parm,r_parm,flow,flowrate,selfAdvect),\
	folder_type = hou.folderType.Simple)

	return noise_folder		
	
def createAaNoiseFolderParmTemplate(id):
	a_parm = hou.FloatParmTemplate('a'+id,'Amp'+id,1,default_value = (1,))
	f_parm = hou.FloatParmTemplate('f'+id,'Freq'+id,1,default_value = (1,))   
	t_parm = hou.IntParmTemplate('t'+id,'Turb'+id,1,default_value = (3,))   
	o_parm = hou.FloatParmTemplate('o'+id,'Offset'+id,1,default_value = (0,)) 
	r_parm = hou.FloatParmTemplate('r'+id,'Rough'+id,1,default_value = (0.5,))   
	xnoise = hou.ToggleParmTemplate('type'+id,'Xnoise'+id,1) 
	
	noise_folder = hou.FolderParmTemplate('noise'+id,'Noise'+id,\
	parm_templates = (a_parm,f_parm,t_parm,o_parm,r_parm,xnoise),\
	folder_type = hou.folderType.Simple)

	return noise_folder		
	
def addCurlNoiseToSnippet(n):
	if n.parm('snippet') is not None:
		includeAddSafe(n,'lzn')
		ptg = n.parmTemplateGroup()	
		parm = ptg.findFolder('Noises')
		if parm is None:
			parm = hou.FolderParmTemplate('noises','Noises',folder_type = hou.folderType.Simple)
			ptg.addParmTemplate(parm)
			
		noise_id = len(parm.parmTemplates()) + 1
		noise_folder =  createCurlNoiseFolderParmTemplate(str(noise_id))
		
		new_code = "vector4 pos{id} = set(@P,ch('o{id}'));\nvector n{id} = ch('a{id}')*curl(pos{id},ch('f{id}'),chi('t{id}'),ch('r{id}'),ch('at{id}'),chs('type{id}'),chs('sdf{id}'),chf('ef{id}'));\nv@vel = n1;".format(id = noise_id)
		snippetAddCode(n,new_code)   
		ptg.appendToFolder(parm,noise_folder)	
		n.setParmTemplateGroup(ptg)		



def addNoiseToSnippet(n,type,v = 1):
	if n.parm('snippet') is not None:
		includeAddSafe(n,'lzn')
		ptg = n.parmTemplateGroup()	
		parm = ptg.findFolder('Noises')
		if parm is None:
			parm = hou.FolderParmTemplate('noises','Noises',folder_type = hou.folderType.Simple)
			ptg.addParmTemplate(parm)
			
		noise_id = len(parm.parmTemplates()) + 1
				
		if type=="curl":
			noise_folder =  createCurlNoiseFolderParmTemplate(str(noise_id))
			new_code = "vector4 pos{id} = set(@P,ch('o{id}'));\nvector n{id} = ch('a{id}')*curl(pos{id},ch('f{id}'),chi('t{id}'),ch('r{id}'),ch('at{id}'),chs('type{id}'),chs('sdf{id}'),chf('ef{id}'));\nv@vel = n1;".format(id = noise_id)
		if type=="turb":
			noise_folder =  createTurbNoiseFolderParmTemplate(str(noise_id))
			new_code = "vector n{id} = ch('a{id}')*turbv(v@P*chf('f{id}'),chi('t{id}'),ch('r{id}'),ch('at{id}'),chs('type{id}'));".format(id = noise_id)
			if v==0:
				new_code = "float n{id} = ch('a{id}')*turb(v@P*chf('f{id}'),chi('t{id}'),ch('r{id}'),ch('at{id}'),chs('type{id}'));".format(id = noise_id)
		if type=="flow":
			noise_folder =  createFlowNoiseFolderParmTemplate(str(noise_id))
			new_code = "vector4 pos{id} = set(@P*chf('f{id}'),ch('o{id}'));\nvector n{id} = ch('a{id}')*flowv(pos{id},chi('t{id}'),ch('r{id}'),ch('flow{id}'),ch('flowrate{id}'),ch('selfAdvect{id}'));".format(id = noise_id)
			if v==0:
				new_code = "vector4 pos{id} = set(@P*chf('f{id}'),ch('o{id}'));\nfloat n{id} = ch('a{id}')*flow(pos{id},chi('t{id}'),ch('r{id}'),ch('flow{id}'),ch('flowrate{id}'),ch('selfAdvect{id}'));".format(id = noise_id)
		if type=="aa":
			noise_folder =  createAaNoiseFolderParmTemplate(str(noise_id))
			new_code = "vector4 pos{id} = set(@P*chf('f{id}'),ch('o{id}'));\nvector n{id} = ch('a{id}')*aav(pos{id},chi('t{id}'),ch('r{id}'),chi('type{id}'));".format(id = noise_id)
			if v==0:
				new_code = "vector4 pos{id} = set(@P*chf('f{id}'),ch('o{id}'));\nfloat n{id} = ch('a{id}')*aa(pos{id},chi('t{id}'),ch('r{id}'),chi('type{id}'));".format(id = noise_id)
		
		
		
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
	dir = os.path.abspath(hou.text.expandString(env).replace('/','\\'))
	subprocess.Popen('explorer "' + dir  + '"')

def setProject():
	import os
	# get root dir
	start_dir = hou.text.expandString("$HMEGA") + "/! Projects/"
	answer = hou.ui.selectFile(start_directory=start_dir,file_type=hou.fileType.Directory)

	if answer != '':
		# Make dirs
		os.makedirs(answer)
		os.makedirs(answer + "/Hip")
		os.makedirs(answer + "/Flipbook")
		os.makedirs(answer + "/Render")
		os.makedirs(answer + "/Cache")
		os.makedirs(answer + "/Cache/Abc")
		os.makedirs(answer + "/Cache/Sim")
		os.makedirs(answer + "/Cache/Stash")
		os.makedirs(answer + "/Cache/Redshift")
		
		hipname = answer.split("/").pop()
		
		hou.appendSessionModuleSource("import lzutil\nlzutil.updateJobFromHipLocation()")
		
		hou.hscript('setenv JOBNAME ='+ hipname)
		#print answer
		hou.hscript('setenv JOB ='+ answer)	
		
		hou.hipFile.save(answer + "/hip/" + hipname +".000" +".hip")  
		
		print("Updated JOBNAME to: " + hipname)
		print("Updated JOB to: " + answer)
		

def updateJobFromHipLocation():
	import os
	hip = hou.hipFile.path()
	JOB = os.path.abspath(os.path.dirname(os.path.dirname(hip))).replace("\\","/")
	hou.hscript('setenv JOB ='+ JOB)	
	print("Updated JOB to: " + JOB)
	
def updateJobNameFromHipLocation():
	import os
	hip = hou.text.expandString("$HIP")
	JOB = os.path.dirname(hip)
	jobname = JOB.split("/").pop()
	hou.hscript('setenv JOBNAME ='+ jobname)	
	print("Updated JOBNAME to: " + jobname)
	
			
def copyToClipboard(str):
	'''Copies str argument to clipboard
	'''
	#import PySide.QtGui as qtg
	#app = qtg.QApplication.instance()
	#clipboard = app.clipboard()
	#clipboard.setText(str)
	from PySide2.QtWidgets  import  QApplication
	QApplication.clipboard().setText(str)
	
def copyToClipboardExpanded(str):
	''' Expands str and copies it to clipboard
	'''
	copyToClipboard(hou.text.expandString(str))
	
def updateSnippetFromClipboard(node):
	''' Sets the snippet parm on a node from the text n clipboard
	'''
	snippet = node.parm('snippet')
	if snippet is not None:
		from PySide2.QtWidgets  import  QApplication
		code =  QApplication.clipboard().text()
		code =  code.replace('\t', '	')
		snippet.set(code)

# installs all hdas from a  lib directory in $hext/otls		
def installOtlLib(lib):
	import hou,glob

	hext = hou.text.expandString('$OTLS')

	path = hext + "/" + lib + "/*.hda"
	otls = glob.glob(path)
	for otl in otls:
		hou.hda.installFile(otl)

# shows a ui to install libs in current hip file, then adds their installation to the python source editor		
def installOtlLibsUI():
	import glob
	path = hou.text.expandString('$OTLS') + "\\*/"
	libs =  glob.glob(path)
	libs = [e.split("\\")[-2] for e in libs]
	print( libs )

	answer =  hou.ui.selectFromList(libs)
	for ans in answer:
		lib = libs[ans]
		installOtlLib(lib)
		print(  "\nimport lzutil\nlzutil.installOtlLib('"+lib +"')")
		hou.appendSessionModuleSource( "import lzutil\nlzutil.installOtlLib('"+lib +"')" )

def explorer(dir):
	'''Open dir in explorer
	'''
	subprocess.Popen('explorer "' + dir.replace('/','\\')  + '"')

def FixPtgFolders(node):
	ptg = node.parmTemplateGroup()
	folders = ptg.entries()
	for folder in folders:
		folder.setFolderType(hou.folderType.Simple)
		ptg.replace(folder.name(),folder)
	node.setParmTemplateGroup(ptg)  
	
	
# Execute script from a shelf
def execTool(shelf,toolName,locals = {}):
	rs = hou.shelves.shelves()[shelf]
	for tool in rs.tools():	
		if tool.name() == toolName:
			exec("import hou\n" + tool.script(),{},locals)

# Update All Bboxes
def updateBbox(n):
	''' Set the box center and size from its curren bbox.
	Use if you need to adjust a box from a bboxed geo used as starting point.
	'''
	g = n.geometry()
	bb = g.boundingBox()
	
	n.parm("sizex").set(bb.sizevec()[0])
	n.parm("sizey").set(bb.sizevec()[1])
	n.parm("sizez").set(bb.sizevec()[2])
	
	n.parm("tx").set(bb.center()[0])
	n.parm("ty").set(bb.center()[1])
	n.parm("tz").set(bb.center()[2])

			
			
# Construction plane Functions			
# set origin of a contruction plane
def cpSetOrigin(new_origin,construction_plane = []):
	if construction_plane == []:
		construction_plane = toolutils.sceneViewer().constructionPlane()
	# revert center offset
	t = hou.hmath.buildTranslate(hou.Vector3([-2,-2,0]))
	construction_plane.setTransform(t.inverted()*construction_plane.transform())
	# process
	translation = hou.hmath.buildTranslate(hou.Vector3(new_origin) - cpOrigin(construction_plane))
	construction_plane.setTransform(construction_plane.transform() * translation)
	# apply center offset
	construction_plane.setTransform(t*construction_plane.transform())
# set_normal
def cpSetNormal(normal_vector,construction_plane = []):
	if construction_plane == []:
		construction_plane = toolutils.sceneViewer().constructionPlane()
	# revert center offset
	t = hou.hmath.buildTranslate(hou.Vector3([-2,-2,0]))
	construction_plane.setTransform(t.inverted()*construction_plane.transform())
	# process
	existing_rotation = hou.Matrix4(construction_plane.transform().extractRotationMatrix3())
	rotation = existing_rotation * cpNormal(construction_plane).matrixToRotateTo(normal_vector)
	translation = hou.hmath.buildTranslate(cpOrigin(construction_plane))
	construction_plane.setTransform(rotation * translation) 
	# apply center offset
	construction_plane.setTransform(t*construction_plane.transform())

	
# contruction plane N and origin
def cpNormal(construction_plane = []):
	if construction_plane == []:
		construction_plane = toolutils.sceneViewer().constructionPlane()
	return hou.Vector3(0, 0, 1) * construction_plane.transform().inverted().transposed()
# Set Origin
def cpOrigin(construction_plane = []):
	if construction_plane == []:
		construction_plane = toolutils.sceneViewer().constructionPlane()
	return hou.Vector3(0, 0, 0) * construction_plane.transform()  
	
		
# Float Ramp To Color Ramp
# Fix for redshift
# import lzutil;n = hou.pwd();lzutil.copyFloatRampToColorRamp(n.parm("cramp"),n.parm("ramp"))
def copyFloatRampToColorRamp(r,cd):
	ramp = r.evalAsRamp()
	basis = ramp.basis()
	keys = ramp.keys()
	values = ramp.values()	
   
	cdValues = []
	for val in values:
		cdValues += [[val,val,val]]
	
	cdRamp = hou.Ramp(basis,keys,cdValues)
	cd.set(cdRamp)

def preset(n,preset_name):
	op_path = n.path()
	cmd = 'oppresetload %s "%s"' % (op_path, preset_name)
	hou.hscript(cmd)

	
def createParmWindow(n, dy = [0.1,0.9],dx = [0.05,0.35]):
	# create Size and Center
	#dy = [0.1,0.95];
	#dx = [0.05,0.35];
	
	pname = n.path().replace('/','_')
	for fp in hou.ui.floatingPanels():
		if fp.name() == pname:
			fp.close()
	
	import ctypes
	user32 = ctypes.windll.user32
	sz = int (user32.GetSystemMetrics(0)),int( user32.GetSystemMetrics(1))
	pos = (sz[0]+ int(sz[0]*dx[0]),int(sz[1]*(dy[0])))
	size = int(sz[0]*(dx[1] - dx[0])),int(sz[1]*(dy[1]-dy[0]))

	d = hou.ui.curDesktop() 

	panel = d.createFloatingPanel(hou.paneTabType.Parm,pos,size)	
	tab = panel.paneTabs()[0]
	tab.setCurrentNode(n)
	tab.linkGroup = hou.paneLinkType.Pinned
	panel.setName(pname)
	
def promoteParm(p):
	n = p.node()
	pr = n.parent()

	pt = p.parmTemplate()
	pt.setName(n.name() + "_" + pt.name())
	pt.setLabel(n.name() + " " + pt.label())
	if pt.type() == hou.parmTemplateType.Menu:
		pt.setDefaultValue(p.eval())
	else:
		pt.setDefaultValue((p.eval(),))

	ptg = pr.parmTemplateGroup()
	ptg.addParmTemplate(pt)

	pr.setParmTemplateGroup(ptg)

	np = pr.parm(pt.name())
	p.set(np)

def dublicateParm(p):
	n = p.node()
	pt = p.parmTemplate()
	pt.setName(pt.name() + "_copy")
	if pt.type() == hou.parmTemplateType.Menu:
		pt.setDefaultValue(p.eval())
	else:
		pt.setDefaultValue((p.eval(),))

	ptg = n.parmTemplateGroup()
	ptg.addParmTemplate(pt)
	n.setParmTemplateGroup(ptg)
	np = n.parm(pt.name())
	p.set(np)

def setNodePreset(n,preset_name):
	op_path = n.path()
	cmd = 'oppresetload %s "%s"' % (op_path, preset_name)
	hou.hscript(cmd)

def installMyShelves():
	d = hou.ui.curDesktop()
	sd = d.shelfDock()
	ssets = sd.shelfSets()

	ss1 = ssets[0]
	shelves = list(ss1.shelves())
	lz_main = hou.shelves.shelves()['LZ Main']
	if lz_main not in shelves:
		shelves = [lz_main] + shelves
		ss1.setShelves(shelves)

	ss2 = ssets[1]
	shelves = list(ss2.shelves())
	lz_rs = hou.shelves.shelves()['LZ_Redshift']
	if lz_rs not in shelves:
		shelves = [lz_rs] + shelves
		ss2.setShelves(shelves)

def createFloatingPanel(panel_type,panel_name,dx,dy):
	from PySide2.QtWidgets  import  QApplication

	d = hou.ui.curDesktop()
	screen = QApplication.screens()[-1]
	geo = screen.geometry()
	x = geo.x()
	y = geo.y()
	w = geo.width()
	h = geo.height()

	pos  = [int(x+dx[0]*w)			  , int(h*(1 - dy[1] - dy[0])) ]
	size = [int(w*(dx[1] - dx[0]))	  , int(h*(dy[1] - dy[0]))]


	panel = d.createFloatingPanel(panel_type,pos,size)
	panel.setPosition(pos)
	panel.setName(panel_name)
	
	return panel

def createRenderView():
	dy = [0.05,0.65]
	dx = [0.025,0.55]
	panel_type = hou.paneTabType.IPRViewer
	panel_name = 'RenderView'
	return createFloatingPanel(panel_type,panel_name,dx,dy)

#		_____	 _____	 _____						  _			  
#	   |  __ \   / ____|   |  __ \						(_)			 
#	   | |__) | | (___	 | |__) |  _ __	___   __  __  _	___   ___ 
#	   |  _  /   \___ \	|  ___/  | '__|  / _ \  \ \/ / | |  / _ \ / __|
#	   | | \ \   ____) |   | |	  | |	| (_) |  >  <  | | |  __/ \__ \
#	   |_|  \_\ |_____/	|_|	  |_|	 \___/  /_/\_\ |_|  \___| |___/
#																		  

def addParm(n,parm):
	ptg = n.parmTemplateGroup()
	ptg.addParmTemplate(parm) 
	n.setParmTemplateGroup(ptg)

# Function To Load Assets and sequences
def loadRsAssetSimple(path = "",animated = False,versions = 1):
	# Check if file on disk
	if not (animated or versions > 1):
		if not os.path.isfile(path):
			print ("File not found: \n" + path)
			return	
	
	# Create Holder Node
	obj_node = hou.node("/obj")
	name = os.path.basename(os.path.dirname(path)) 
	holder = obj_node.createNode("geo","RS_Proxy_" + name)	
	holder.moveToGoodPosition()		
	
	fixed_path = path
	if animated:
		holder.parm("RS_objprop_proxy_prevAnimated").set(1)
		fixed_path = re.sub(regex,r'\1$F4\3',path)
	if versions > 1:
		# create versions spare parm
		version_parm = hou.IntParmTemplate("asset_version", "Asset Version", 1, default_value=([1]), min=1, max=int(versions),min_is_strict=True, max_is_strict=True)
		ptg = holder.parmTemplateGroup()
		ptg.addParmTemplate(version_parm)
		holder.setParmTemplateGroup(ptg)
		fixed_path = regex_replace(path,r'`padzero(4,ch("asset_version"))`')
	
	holder.parm("RS_objprop_proxy_enable").set(1)
	holder.parm("RS_objprop_proxy_file").set(fixed_path)
	holder.parm("RS_objprop_inst_ignorePivot").set(1)
	
	# def check Filesize (only if the file exists)
	if os.path.isfile(path):
		filesize  = os.path.getsize(path) * 1e-6
		if filesize < 50 :	
			holder.parm("RS_objprop_proxy_preview").set(2)	
			
	# Create Preview Geometry
	# if we have animated geo there's no point in createing LZRSLOADPROXIES
	if not animated:
		load_proxy = holder.createNode("attribwrangle","load_proxy")
		load_proxy.parm("class").set(0)
		load_proxy.parm("snippet").set('int pt = addpoint(0,@P);\nstring instancefile = chs("file");\nsetpointattrib(0,\'instancefile\',pt,instancefile);')
	
		rs_file_parm = hou.StringParmTemplate("file", "File", 1, string_type=hou.stringParmType.FileReference)
		addParm(load_proxy,rs_file_parm)
		
		load_proxy.parm("file").set('`chs("../RS_objprop_proxy_file")`')
		load_proxy.setDisplayFlag(True) 
		
		LZ_RS_InstanceProxies = load_proxy.createOutputNode('LZ_RS_InstanceProxies')
		LZ_RS_InstanceProxies.setDisplayFlag(1)			  
	else:
		# load preview geometry
		if os.path.isfile(path.replace(".rs",".bgeo.sc")):
			file = holder.createNode('file')
			file.parm("file").set( path.replace(".rs",".bgeo.sc"))
			# make it packed
			file.parm("loadtype").set(4)
			file.parm("viewportlod").set(0)
		else:
			holder.createNode('redshift_proxySOP') 
	
	return holder

#----------------------------------

def getCurrentContextNode():
	current_node = toolutils.networkEditor().currentNode()
	if current_node.type().name() == 'geo':
		return current_node
	else:
		return current_node.parent()

		
	
#-----------------------------------------
# PARMS AND MENUS
def changeRampType(p):
	n = p.node()
	ptg = n.parmTemplateGroup()
	pt = p.parmTemplate()
	if pt.type().name() == "Ramp":
		if pt.parmType().name() == "Float":
			pt.setParmType(hou.rampParmType.Color)
		else:
			pt.setParmType(hou.rampParmType.Float)
			
		ptg.replace(pt.name(),pt)
		n.setParmTemplateGroup(ptg)
			
def openInExplorer(filepath):		
	if not os.path.isdir(filepath): filepath = os.path.dirname(filepath)
	openFolderFromEnv(filepath)


#-----------------------------
# LOPS / SOLARIS / USD
def load_asset_to_LayoutAssetGallery(filepath):
	asset_name = os.path.splitext(os.path.basename(filepath))[0]
	thumbnail = os.path.dirname(filepath) + "/" + asset_name + ".jpg"
	hou.qt.AssetGallery.addAsset(asset_name, filepath,thumbnail)

def splitpath(filepath):
	dir = os.path.dirname(filepath)
	[f,ext] = os.path.splitext(os.path.basename(filepath))
	return [dir,f,ext]


def PythonSnippet_CreateParmTemplates( index = 0 ):
	index = str(index) if index>0 else ""	

	code_name = "lzPython_code" + index
	
	lzPython_code = hou.StringParmTemplate(code_name, "Code", 1, default_value=([""]), string_type=hou.stringParmType.Regular, item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
	run_in_console_script = f"""import subprocess,os
n = kwargs['node']
python_path = os.path.abspath(hou.text.expandString("$PYTHONHOME\python.exe"))
code = "_shell=True\\n" + n.parm("{code_name}").eval()
subprocess.Popen([python_path,"-i","-c",code])
"""
	lzPython_code.setTags({"editor": "1", "editorlang": "python", "editorlines": "30-50", "script_action": run_in_console_script})
  

	lzPython_run = hou.ButtonParmTemplate("lzPython_run" + index, "Run")
	script_callback = f"exec( \"_shell=False\\n\" + hou.pwd().parm(\"{code_name}\").eval())"
	lzPython_run.setScriptCallback(script_callback)
	lzPython_run.setScriptCallbackLanguage(hou.scriptLanguage.Python)
	#lzPython_run.setTags({"script_callback": script_callback, "script_callback_language": "python"})
	
	return [lzPython_code,lzPython_run]

def PythonSnippet_addFolderWithParmTemplates(ptg,index = 0):
	# create script and run buttons
	pts = PythonSnippet_CreateParmTemplates(index)
	pts[1].setJoinWithNext(True)
	
	# create rename buttons
	rename_button_pt = hou.ButtonParmTemplate("lzPyhton_updateName" + (str(index) if index > 0 else ""), "Update Name")
	rename_button_pt.setHelp("updates name from first line comment")
	rename_button_script = f"import lzutil;lzutil.RenamePythonSnippetFromFirstLine(hou.pwd(),{index})"
	rename_button_pt.setScriptCallback(rename_button_script)
	rename_button_pt.setScriptCallbackLanguage(hou.scriptLanguage.Python)
	rename_button_pt.setJoinWithNext(True)
	pts.append(rename_button_pt)
	
	# create Delete Button
	delete_button_pt = hou.ButtonParmTemplate("lzPyhton_delete" + (str(index) if index > 0 else ""), "Delete")
	delete_button_script = f"import lzutil;lzutil.deletePythonSnippet(hou.pwd(),{index})"
	delete_button_pt.setScriptCallback(delete_button_script)
	delete_button_pt.setScriptCallbackLanguage(hou.scriptLanguage.Python)
	pts.append(delete_button_pt)
	
	index = str(index) if index>0 else ""	
	folder_pt = hou.FolderParmTemplate("lzPython_folder" + index,"Python" + index,folder_type = hou.folderType.Tabs,parm_templates = pts)
	ptg.append(folder_pt) 
 
def RenamePythonSnippetFromFirstLine(n,index):
	index = str(index) if index>0 else ""   
	code_name = "lzPython_code" + index
	folder_name = "lzPython_folder" + ("_" + index if index else "")
	new_name = n.parm(code_name).eval().splitlines()[0].replace("#","").strip()
	ptg = n.parmTemplateGroup()
	folder_pt = ptg.find(folder_name)
	if folder_pt:
		folder_pt.setLabel(new_name)
		ptg.replace(folder_name, folder_pt)
		n.setParmTemplateGroup(ptg)

def addPythonSnippet(n):
	ptg = n.parmTemplateGroup()

	# Check if we already have code
	if n.parm("lzPython_code"):
		# check if we have a folder
		index = 1
		if ptg.find("lzPython_folder"):
			# find index to insert newfolder at	  
			while n.parm("lzPython_code" + str(index)): index += 1 
		else:
			# remove old par,s
			ptg.remove("lzPython_code")
			ptg.remove("lzPython_run")
			# add folder with old parms
			PythonSnippet_addFolderWithParmTemplates(ptg)   
		# Add A new folder
		PythonSnippet_addFolderWithParmTemplates(ptg,index)
	else:   
		# add simple snippet
		[lzPython_code,lzPython_run] = PythonSnippet_CreateParmTemplates()	
		ptg.append(lzPython_code)
		ptg.append(lzPython_run)	
		index = 0
		
	n.setParmTemplateGroup(ptg)
	return index
	
def deletePythonSnippet(n,index):
	ptg = n.parmTemplateGroup()
	folder_index_str = "_" + str(index) if index > 0 else ""
	folder = ptg.find("lzPython_folder" +  folder_index_str  )
	ptg.remove(folder)
	
	snippets = {}
	index += 1
	while ptg.find("lzPython_folder_" + str(index)): 
		folder = ptg.find("lzPython_folder_" + str(index)) 
		new_index_str =  str(index-1) if index-1 > 0 else ""
		folder.setName("lzPython_folder" + new_index_str )
		ptg.replace("lzPython_folder_" + str(index),folder)
		snippets[index-1] = n.parm("lzPython_code" + str(index)).eval()
		
		for parm in folder.parmTemplates():		
			old_name = parm.name()
			name = parm.name().rstrip(string.digits) + new_index_str
			parm.setName(name)
			# replace script callbacks
			if name.startswith("lzPython_run"):				  
				parm.setScriptCallback( parm.scriptCallback().replace( "lzPython_code" + str(index),"lzPython_code" +new_index_str) )			
			if  name.startswith("lzPyhton_updateName"):
				parm.setScriptCallback(f"import lzutil;lzutil.RenamePythonSnippetFromFirstLine(hou.pwd(),{index-1})")
			if  name.startswith("lzPyhton_delete"):
				parm.setScriptCallback(f"import lzutil;lzutil.deletePythonSnippet(hou.pwd(),{index-1})")
			if name.startswith("lzPython_code"):
				tags = parm.tags()
				tags['script_action'] = tags['script_action'].replace( "lzPython_code" + str(index),"lzPython_code" +new_index_str)
				parm.setTags(tags)			
			ptg.replace(old_name,parm)
		index += 1
		
	n.setParmTemplateGroup(ptg)
	
	# update scripts
	for key in snippets.keys():
		str_key = str(key) if key>0 else ""
		n.parm("lzPython_code" + str_key ).set(snippets[key])
	
def updateNodeToLatestDefinition(n):
	type = n.type()
	definition = type.definition()
	hda = definition.libraryFilePath()

	max_v = ""
	for d in hou.hda.definitionsInFile(hda) :	 
		v = d.nodeTypeName().split('::')
		if len(v) > 1:
			if (v[1] > max_v):
				max_v = v[1]
		
	max_version = n.type().name().split("::")[0] +"::" +max_v 

	n = n.changeNodeType(max_version, keep_network_contents=False)
	
	
#-------------------------------------------
# NODE Saving and Loading
def getCurrentContextNode():
	current_node = toolutils.networkEditor().currentNode()
	if current_node.type().name() in ['geo','obj']:
		return current_node
	else:
		return current_node.parent()
		
def load_nodes(filename):
	filename = hou.text.expandString(filename)	
	n = getCurrentContextNode()
	if os.path.isfile(filename):
		n.loadChildrenFromFile(filename)	

	# Move to center of screen
	center = toolutils.networkEditor().visibleBounds().center()
	if len(hou.selectedNodes()) == 1:
		hou.selectedNodes()[0].setPosition(center)	
	for nitem in hou.selectedItems():
		if (isinstance(nitem,hou.NetworkBox)):
			nitem.setPosition(center)
		
def save_selected_nodes(filename):
	filename = hou.text.expandString(filename)
	nodes = hou.selectedNodes()	
	if filename != "":
		contextnode = nodes[0].parent()
		contextnode.saveChildrenToFile(nodes, [], filename)
		
def CamFocusPlane(cam):
	filename = "$HEXT/megavex/nodes/Focus_plane.cpio"	
	filename = hou.text.expandString(filename)	
	n = cam.parent()
	if os.path.isfile(filename):
		n.loadChildrenFromFile(filename,True)  
	sn = hou.selectedNodes()
	sn[1].setInput(0,cam)
   
def InsertParmTemplateBefore(n,new_parm,parm_name):
	ptg = n.parmTemplateGroup()
	divsize = ptg.find(parm_name)
	ptg.insertBefore(divsize,new_parm)
	n.setParmTemplateGroup(ptg)
	
def sopPyroAddDivisionsParm(n):	
	p = hou.IntParmTemplate("usd","Divisions",1,[150],150,600)
	InsertParmTemplateBefore(n,p,"divsize")	
	n.parm("divsize").setExpression(f'max(max(ch("maxsizex"),ch("maxsizey")),ch("maxsizez"))/ch("usd")')

def renameFolderParm(folder,new_name = ""):
	n = folder.node()
	ptg = n.parmTemplateGroup()
	folder_name = folder.parmTemplate().name()
	
	folder_pt = ptg.find(folder_name)
	result = 0
	if new_name == "":
		[result,new_name] = hou.ui.readInput("New Folder Name", buttons=('OK',"Cancel"), title="New Folder Name", initial_contents=folder_pt.label(),close_choice=1)

	if result == 0 and new_name != "": 
		folder_pt.setLabel(new_name)
		ptg.replace(folder_name, folder_pt)
		n.setParmTemplateGroup(ptg)

### FTP SCRIPTS ###

def ftp_subprocessFile(local_file,ftp_file,function = "ftp_downloadFile"):
	# Generate Code
	login_str = ftp_getLoginStr()
	lz_scripts_path = os.path.dirname(os.path.abspath(lzftp.__file__))	
	code = f"""
import sys
sys.path.append("{lz_scripts_path}")
import lzftp
lzftp.{function}("{login_str}","{local_file}","{ftp_file}")"""
	
	# Run this code
	python_path = os.path.abspath(hou.text.expandString("$PYTHONHOME\python.exe"))
	subprocess.Popen([python_path,"-i","-c",code])	

def ftp_getLoginStr():
	return hou.text.expandString("$FTP_LOGIN")

def ftp_downloadFile(local_file,ftp_file, load_in_subprocess = True):
	if load_in_subprocess:
		ftp_subprocessFile(local_file,ftp_file,"ftp_downloadFile")	
	else:
		lzftp.ftp_downloadFile(ftp_getLoginStr(),local_file,ftp_file)

def ftp_uploadFile(local_file,ftp_file, load_in_subprocess = True):
	if load_in_subprocess:
		ftp_subprocessFile(local_file,ftp_file,"ftp_uploadFile")	
	else:
		lzftp.ftp_uploadFile(ftp_getLoginStr(),local_file,ftp_file)

def ftp_downloadFolder(local_file,ftp_file, load_in_subprocess = True):
	if load_in_subprocess:
		ftp_subprocessFile(local_file,ftp_file,"ftp_downloadFolder")	
	else:
		lzftp.ftp_downloadFolder(ftp_getLoginStr(),local_file,ftp_file)

def ftp_uploadFolder(local_file,ftp_file, load_in_subprocess = True):
	if load_in_subprocess:
		ftp_subprocessFile(local_file,ftp_file,"ftp_uploadFolder")	
	else:
		lzftp.ftp_uploadFolder(ftp_getLoginStr(),local_file,ftp_file)

	
def ftp_downloadFromCanoeServer(local_file):
	local_file = os.path.normpath(local_file).replace(os.sep,"/")
	ftp_file = local_file.replace("Z:/","/Fileserver/Projects/")	
	ftp_downloadFile(local_file,ftp_file)

### LZ PYTHON ###
	
def lzPython_createParmsFromCode(code_parm):
	# replaces all parms of type
	# test_parm = "path to file" #defparm file	
	n = code_parm.node()
	ptg = n.parmTemplateGroup()
	code_name = code_parm.name()
	code_str = code_parm.unexpandedString()
	for code_line in reversed(code_str.splitlines()):
		if "#defparm" in code_line:				
				parm_options = code_line.split("#defparm")[-1].strip().split()
				parm_type = parm_options[0]
				[parm_name,default_value] = code_line.split("#defparm")[0].split("=")
				parm_name = parm_name.strip()
				# If we have a file type parameter
				if parm_type == 'file':
					# if parm already transformed 
					if 'parm("' in default_value:
						default_value = parm_options[1]					  
					else:				
						default_value = default_value.strip().replace('"',"")						
						new_code_line = f'{parm_name} = hou.pwd().parm("{parm_name}").eval() #defparm {parm_type} {default_value}' 
						code_str = code_str.replace(code_line,new_code_line)
						
					if not n.parm(parm_name):	
						new_parm = hou.StringParmTemplate(parm_name,parm_name,1,string_type = hou.stringParmType.FileReference,default_value = [default_value])					
						ptg.insertAfter(code_name,new_parm)  

	code_parm.set(code_str)
	n.setParmTemplateGroup(ptg)	
	
	