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
	import os
	dir = os.path.abspath(hou.expandString(env).replace('/','\\'))
	subprocess.Popen('explorer "' + dir  + '"')

def setProject():
	import os
	# get root dir
	start_dir = hou.expandString("$HMEGA") + "/! Projects/"
	answer = hou.ui.selectFile(start_directory=start_dir,file_type=hou.fileType.Directory)

	if answer is not '':
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
	hip = hou.expandString("$HIP")
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
	copyToClipboard(hou.expandString(str))
	
def updateSnippetFromClipboard(node):
	''' Sets the snippet parm on a node from the text n clipboard
	'''
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

	
def createParmWindow(n, dy = [0.1,0.95],dx = [0.05,0.35]):
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
	
	
	
	
