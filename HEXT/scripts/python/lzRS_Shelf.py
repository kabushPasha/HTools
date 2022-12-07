import hou
import lzutil
import subprocess,os

# Dictinonaris
aov_toggles = [
	["Light_components",["diffuse","specular","reflection","refraction","SSS"]],
	["Volume_components",["VolumeLighting","VolumeFogTint","VolumeFogEmission"]],
	["Crypto_components",["cryptomatte","cryptomatte_mat"]],	
	["Z_comp",["Z"]],
	["PN_comp",["P","N"]],	
	["GI_comp",["GI"]],
	["EM_comp",["emission"]],
	["Shadows_comp",["shadows"]]
	]
canoe_rs_parms = {
	'RS_renderAOVsToMPlay':1,
	# motion blur
	'MotionBlurDeformationEnabled':1,
	'RS_mbPoints':1,
	# output file
	'RS_outputFileNamePrefix': '$JOB/Render/001_InitRender/$F4.exr',
	# Aovs settings
	"RS_aovAllAOVsDisabled" : 1,
	"RS_renderCamera" : "/obj/RS_Cam",
	"RS_lights_candidate" : "RS_*",
	"RS_objects_candidate" : "RS_*",
	"RS_addDefaultLight" : 0,
	}
canoe_rs_parmExp = {
	"UnifiedMaxSamples":'ch("UnifiedMinSamples")*4',
	}

# Functions
def CreateCanoeRenderTabOld(n):
	ptg = n.parmTemplateGroup()
	
	folder = hou.FolderParmTemplate("shortcuts","CANOE")
	
	Render_Cam = hou.StringParmTemplate("Canoe_renderCamera", "Render Camera", 1, default_value=(["/obj/RS_Cam"]),string_type=hou.stringParmType.NodeReference)
	Render_Cam.setTags({"autoscope": "0000000000000000", "opfilter": "!!OBJ/CAMERA!!", "oprelative": "."})
	folder.addParmTemplate(Render_Cam)
	
	Output = hou.StringParmTemplate("Canoe_outputFileNamePrefix", "Common File Prefix", 1, default_value=(["$JOB/Render/001_InitRender/$F4.exr"]),string_type=hou.stringParmType.FileReference, item_generator_script="opmenu -l . RS_outputFileNamePrefix", item_generator_script_language=hou.scriptLanguage.Hscript, menu_type=hou.menuType.StringReplace)
	folder.addParmTemplate(Output)
	folder.addParmTemplate(hou.SeparatorParmTemplate("sep1"))
	
	arhive_toggle = hou.ToggleParmTemplate("Canoe_archive_enable", "Export .rs Proxy File", default_value=False)
	folder.addParmTemplate(arhive_toggle)
	
	archive = hou.StringParmTemplate(
		"Canoe_archive_file", 
		"Filename", 
		1,
		default_value=([""]), 
		default_expression_language=([hou.scriptLanguage.Python]), 
		naming_scheme=hou.parmNamingScheme.Base1, 
		string_type=hou.stringParmType.FileReference, 
		item_generator_script="opmenu -l . RS_archive_file", 
		menu_items=([]), menu_labels=([]), icon_names=([]),
		menu_type=hou.menuType.StringReplace,
		item_generator_script_language=hou.scriptLanguage.Hscript)
	archive.setDefaultExpression(["hou.pwd().parm('Canoe_outputFileNamePrefix').unexpandedString().rsplit('.',1)[0] + '.rs'"])
	folder.addParmTemplate(archive)
	

	folder.addParmTemplate(hou.SeparatorParmTemplate("sep2"))
	
	Motion_toggle = hou.ToggleParmTemplate("Canoe_MotionBlurEnabled", "Enable Motion Blur", default_value=False, default_expression='off', default_expression_language=hou.scriptLanguage.Hscript)
	folder.addParmTemplate(Motion_toggle)
	
	Fog_toggle = hou.ToggleParmTemplate("Canoe_VolLightingEnabled", "Enable Global Fog", default_value=False, default_expression='off', default_expression_language=hou.scriptLanguage.Hscript)
	folder.addParmTemplate(Fog_toggle)
	
	AOV_toggle = hou.ToggleParmTemplate("Canoe_aovAllAOVsDisabled", "Disable All AOVs", default_value=True, default_expression='on', default_expression_language=hou.scriptLanguage.Hscript)
	folder.addParmTemplate(AOV_toggle)
	
	Tesselation_Toggle = hou.ToggleParmTemplate("Canoe_TessellationDisplacementEnable", "Enable Tessellation And Displacement", default_value=True, default_expression='on', default_expression_language=hou.scriptLanguage.Hscript)
	folder.addParmTemplate(Tesselation_Toggle)
	
	folder.addParmTemplate(hou.SeparatorParmTemplate("sep3"))
	# Code for parameter template
	# Deadline Parameters
	deadline_priority = hou.IntParmTemplate("deadline_priority", "Deadline Priority", 1, default_value=([50]), min=1, max=90, min_is_strict=True, max_is_strict=True)
	folder.addParmTemplate(deadline_priority)	
	deadline_jobname = hou.StringParmTemplate("deadline_jobname", "Deadline Jobname", 1, default_value=(["$HIPNAME"]))
	folder.addParmTemplate(deadline_jobname)
	
	DeadlineFastRender_btn = hou.ButtonParmTemplate("submit_to_deadline_allGpus", "Deadline Render")
	DeadlineFastRender_btn.setScriptCallback("import lz;lz.lzDeadline.submitRS2Deadline(hou.pwd(),one_task_per_gpu=False)")
	DeadlineFastRender_btn.setScriptCallbackLanguage(hou.scriptLanguage.Python)
	folder.addParmTemplate(DeadlineFastRender_btn)
	
	DeadlineRender_btn = hou.ButtonParmTemplate("submit_to_deadline", "Deadline Render (1f per GPU)")
	DeadlineRender_btn.setScriptCallback("import lz;lz.lzDeadline.submitRS2Deadline(hou.pwd())")
	DeadlineRender_btn.setScriptCallbackLanguage(hou.scriptLanguage.Python)
	folder.addParmTemplate(DeadlineRender_btn)
	
	BatchProxy_btn = hou.ButtonParmTemplate("batch_proxy", "Batch Proxy")
	BatchProxy_btn.setScriptCallback("import hou;hou.hipFile.save();import lz;lz.lzRS_Shelf.BatchProxy(hou.pwd())")
	BatchProxy_btn.setScriptCallbackLanguage(hou.scriptLanguage.Python)
	folder.addParmTemplate(BatchProxy_btn)
	
	before = "RS_rrs2"
	ptg.insertAfter(before,folder)
	
	
	# Add AOV Toggles
	addQuickAovToggles(ptg)	
	
	n.setParmTemplateGroup(ptg)	
	link_aov_toggles_toCanoeTab(n)
	
	parms = ["RS_renderCamera","RS_outputFileNamePrefix","RS_archive_enable",
	"RS_archive_file","MotionBlurEnabled","VolLightingEnabled","RS_aovAllAOVsDisabled",
	"TessellationDisplacementEnable"]
	
	for parm in parms:
		n.parm(parm).set(n.parm("Canoe_" + parm.replace("RS_","")))

def CreateDeadlineButtons(folder):
	# Create Deadline Parameters
	deadline_priority = hou.IntParmTemplate("deadline_priority", "Deadline Priority", 1, default_value=([50]), min=1, max=90, min_is_strict=True, max_is_strict=True)
	folder.addParmTemplate(deadline_priority)	   
	deadline_jobname = hou.StringParmTemplate("deadline_jobname", "Deadline Jobname", 1, default_value=(["$HIPNAME"]))
	folder.addParmTemplate(deadline_jobname)
	
	DeadlineFastRender_btn = hou.ButtonParmTemplate("submit_to_deadline_allGpus", "Deadline Render")
	DeadlineFastRender_btn.setScriptCallback("import lz;lz.lzDeadline.submitRS2Deadline(hou.pwd(),one_task_per_gpu=False)")
	DeadlineFastRender_btn.setScriptCallbackLanguage(hou.scriptLanguage.Python)
	folder.addParmTemplate(DeadlineFastRender_btn)
	
	DeadlineRender_btn = hou.ButtonParmTemplate("submit_to_deadline", "Deadline Render (1f per GPU)")
	DeadlineRender_btn.setScriptCallback("import lz;lz.lzDeadline.submitRS2Deadline(hou.pwd())")
	DeadlineRender_btn.setScriptCallbackLanguage(hou.scriptLanguage.Python)
	folder.addParmTemplate(DeadlineRender_btn)
	
	BatchProxy_btn = hou.ButtonParmTemplate("batch_proxy", "Batch Proxy")
	BatchProxy_btn.setScriptCallback("import hou;hou.hipFile.save();import lz;lz.lzRS_Shelf.BatchProxy(hou.pwd())")
	BatchProxy_btn.setScriptCallbackLanguage(hou.scriptLanguage.Python)
	folder.addParmTemplate(BatchProxy_btn)

def CreateCanoeRenderTab(rs):
		ptg = rs.parmTemplateGroup()
		folder = hou.FolderParmTemplate("shortcuts","CANOE")
		sep = 0
		
		CanoeShortcutParms = [
			"RS_renderCamera",
			"RS_outputFileNamePrefix",
			"sep",
			"RS_archive_enable",
			"RS_archive_file",
			"sep",		
			"MotionBlurEnabled",
			"VolLightingEnabled",
			"RS_aovAllAOVsDisabled",
			"TessellationDisplacementEnable",
			"sep",
			"RS_overrideCameraRes",
			"RS_overrideResScale",
			"RS_overrideRes",				
			"sep"]
		CanoeShortcutNames = {
			"RS_archive_enable": "Export Proxy",
			"RS_archive_file": "Proxy Filename",
			"MotionBlurEnabled" : "Motion Blur",
			"VolLightingEnabled" : "Global Fog", 
			"RS_overrideResScale" : " "
			}
		CanoeShortcutsDefaultValues={
			"RS_renderCamera": ["/obj/RS_Cam" ],
			"RS_outputFileNamePrefix": ["$JOB/Render/001_InitRender/$F4.exr" ],
			"RS_aovAllAOVsDisabled": 1,
			"RS_overrideResScale" : 4,
			"RS_overrideRes" : [1920,1080],
			}
		CanoeShortcutsDefaultExpressions={
			"RS_archive_file" : "hou.pwd().parm('Canoe_RS_outputFileNamePrefix').eval().rsplit('.',1)[0] + '.rs'"
			}	   
		CanoeJoinWithNext=[
			"RS_overrideCameraRes"		
			]
		CanoeHideCondition={		
			"RS_overrideRes" : "{ Canoe_RS_overrideResScale < 7 }"
			}
		CanoeDisableCondition={
			"RS_overrideResScale" : "{ Canoe_RS_overrideCameraRes == 0 }"
			}
				
		# Copy Parameters
		for parm_name in CanoeShortcutParms:
			if parm_name == "sep":
				folder.addParmTemplate(hou.SeparatorParmTemplate(f"Canoe_separator_{sep}"))
				sep +=1
			else:
				pt = (rs.parm(parm_name) or rs.parmTuple(parm_name)).parmTemplate()
				pt.setName("Canoe_" + pt.name())
				if parm_name in CanoeShortcutNames: pt.setLabel(CanoeShortcutNames[parm_name])   
				if parm_name in CanoeShortcutsDefaultValues: pt.setDefaultValue(CanoeShortcutsDefaultValues[parm_name]) 
				if parm_name in CanoeShortcutsDefaultExpressions: 
					pt.setDefaultExpressionLanguage([hou.scriptLanguage.Python])
					pt.setDefaultExpression([CanoeShortcutsDefaultExpressions[parm_name]])  
				if parm_name in CanoeJoinWithNext: pt.setJoinWithNext(1)
				if parm_name in CanoeHideCondition: pt.setConditional( hou.parmCondType.HideWhen , CanoeHideCondition[parm_name]  )
				if parm_name in CanoeDisableCondition: pt.setConditional( hou.parmCondType.DisableWhen , CanoeDisableCondition[parm_name]  )
				folder.addParmTemplate(pt)
		# Create deadline buttons
		CreateDeadlineButtons(folder)
		# Insert our folder
		before = "RS_rrs2"
		ptg.insertAfter(before,folder)				
		# Add AOV Toggles
		addQuickAovToggles(ptg) 
		# Set PTG
		rs.setParmTemplateGroup(ptg)	 
				
		# LINK parameters
		link_aov_toggles_toCanoeTab(rs)
		for parm_name in CanoeShortcutParms:
			if parm_name == "sep" : continue
			if rs.parm(parm_name):
				 rs.parm(parm_name).set(rs.parm("Canoe_" + parm_name))
			else:
				 rs.parmTuple(parm_name).set(rs.parmTuple("Canoe_" + parm_name))	

def LZ_RS_Setup():
	########## MAIN ##################
	rs = hou.node("/out/Redshift_ROP1")

	if rs is None:
		rs = __import__('roptoolutils').createRenderNode('Redshift_ROP')
		ipr = __import__('roptoolutils').createRenderNode('Redshift_IPR')
		
		rs.parm('RS_renderAOVsToMPlay').set(1)
		
		rs.parm('MotionBlurDeformationEnabled').set(1)  
		rs.parm('RS_mbPoints').set(1)
		  
		rs.parm('RS_outputFileNamePrefix').set('$JOB/Render/001_InitRender/$F4.exr')
		rs.parm('IrradiancePointCloudFilename').set('$JOB/Cache/Redshift/IPC/$F4.rsmap')
		rs.parm('IrradianceCacheFilename').set('$JOB/Cache/Redshift/IRC/$F4.rsmap')
		
		rs.parm("UnifiedMaxSamples").setExpression('ch("UnifiedMinSamples")*4')	
		
		# AOV's
		rs.parm("RS_aov").set(13)
		rs.parm("RS_aovAllAOVsDisabled").set(1)
		
		rs.parm("RS_aovID_1").set(1)
		rs.parm("RS_aovSuffix_1").set('Z')
		rs.parm("RS_aovID_2").set(17)
		rs.parm("RS_aovSuffix_2").set('emission')
		rs.parm("RS_aovID_3").set(39)
		rs.parm("RS_aovSuffix_3").set('beauty')
		rs.parm("RS_aovLightAllGroups_3").set(1)
		rs.parm("RS_aovID_4").set(7)
		rs.parm("RS_aovSuffix_4").set('diffuseFilter')
		rs.parm("RS_aovID_5").set(0)
		rs.parm("RS_aovSuffix_5").set('P') 
		rs.parm("RS_aovID_6").set(18)
		rs.parm("RS_aovSuffix_6").set('GI')
		rs.parm("RS_aovID_7").set(23)
		rs.parm("RS_aovSuffix_7").set('shadows')
		rs.parm("RS_aovID_8").set(24)
		rs.parm("RS_aovSuffix_8").set('N')
		rs.parm("RS_aovID_9").set(9)
		rs.parm("RS_aovSuffix_9").set('SSS') 
		rs.parm("RS_aovID_10").set(41)
		rs.parm("RS_aovSuffix_10").set('cryptomatte')
		rs.parm("RS_aovID_11").set(27)
		rs.parm("RS_aovSuffix_11").set('VolumeLighting')
		rs.parm("RS_aovID_12").set(28)
		rs.parm("RS_aovSuffix_12").set('VolumeFogTint')
		rs.parm("RS_aovID_13").set(29)
		rs.parm("RS_aovSuffix_13").set('VolumeFogEmission')   
		
		rs.parm("RS_renderCamera").set("/obj/RS_Cam")
		rs.parm("RS_lights_candidate").set("RS_*")
		rs.parm("RS_objects_candidate").set("RS_*")
		rs.parm("RS_addDefaultLight").set(0)
		
		rs.parm('PrimaryGIEngine').set(3)
		rs.parm('SecondaryGIEngine').set(3)
		
		CreateCanoeRenderTab(rs)	
		
	# Check if we have parms and render view already
	has_render_panel = 0
	has_rs_parms = 0
	floatingPanels = hou.ui.floatingPanels()
	for panel in floatingPanels:
		if panel.name() == 'RenderView':
			has_render_panel = 1
		if panel.name() == 'Render_Settings':
			has_rs_parms = 1
		
	# Open Parms Window
	if has_rs_parms == 0:
		dy = [0.05,0.65];
		dx = [0.57,0.85];
		panel = lzutil.createFloatingPanel(hou.paneTabType.Parm,'Render_Settings',dx,dy)
		pane = panel.panes()[0]
		tab = pane.tabs()[0]
		tab.setCurrentNode(rs)
		tab.setPin(1)

	#create RenderView
	if has_render_panel == 0:
		lzutil.createRenderView()

def LZ_RS_Setup3():
	rs = hou.node("/out/Redshift_ROP1")

	if rs is None:
		rs = __import__('roptoolutils').createRenderNode('Redshift_ROP')
		ipr = __import__('roptoolutils').createRenderNode('Redshift_IPR')
		
		rs.setParms(canoe_rs_parms)
		AddBasicAovs(rs)
		rs.setParmExpressions(canoe_rs_parmExp)
		
		CreateCanoeRenderTab(rs)			

	addRenderSettingsPaneTab(rs)	
	
	'''
	# Create RENDER VIEW Floating Panels (currently using 1 monitor)
	# Check if we have parms and render view already
	has_render_panel = 0
	has_rs_parms = 0
	floatingPanels = hou.ui.floatingPanels()
	for panel in floatingPanels:
		if panel.name() == 'RenderView':
			has_render_panel = 1
		if panel.name() == 'Render_Settings':
			has_rs_parms = 1
		
	# Open Parms Window
	if has_rs_parms == 0:
		dy = [0.05,0.65];
		dx = [0.57,0.85];
		panel = lzutil.createFloatingPanel(hou.paneTabType.Parm,'Render_Settings',dx,dy)
		pane = panel.panes()[0]
		tab = pane.tabs()[0]
		tab.setCurrentNode(rs)
		tab.setPin(1)

	#create RenderView
	if has_render_panel == 0:
		lzutil.createRenderView()
	'''

def addRenderSettingsPaneTab(rs):
	tab = hou.ui.findPaneTab("rs_render_settings_tab")
	if tab: 
		tab.setPin(True)
		tab.setCurrentNode(rs)
	else :
		pane = hou.ui.findPane(28)
		if pane:
			curr_tab = pane.currentTab()
			
			tab = pane.createTab(hou.paneTabType.Parm)
			tab.setName("rs_render_settings_tab")
			tab.setPin(True)
			tab.setCurrentNode(rs)
			
			curr_tab.setIsCurrentTab()

def BatchProxy(n,threads = 5,sleep = 5):
	if n.type().name() == 'Redshift_Proxy_Output' or n.type().name() == 'Redshift_ROP':
		hython = hou.getenv('HB')+'/hython'
		file = hou.hipFile.path()
		
		for i in range(0,threads):  
			sf = int(n.parm("f1").eval())
			cmd = 'hou.parm("' + n.path() + '/f1").deleteAllKeyframes();'
			cmd += 'hou.parm("' + n.path() + '/f2").deleteAllKeyframes();'
			cmd += 'hou.parm("' + n.path() + '/f3").deleteAllKeyframes();'
			
			cmd += 'hou.parm("' + n.path() + '/f1").set(' +str(sf+i)+ ');'
			cmd += 'hou.parm("' + n.path() + '/f3").set(' +str(threads)+ ');'
		
			cmd += 'hou.parm("' + n.path() + '/execute").pressButton();'
			cmd += 'import time;print("SLEEPING");time.sleep('+str(sleep)+')'

			subprocess.Popen([hython,file,'-c',cmd])
			
def addCameraParms(cam,add_comment = False):
	ptg = cam.parmTemplateGroup()
	
	# Add Comment Folder
	if add_comment:
		comment_folder = hou.FolderParmTemplate("Comment","Comment")
		comment = hou.StringParmTemplate("vcomment", "Viewport Comment", 1)
		comment.setTags({"editor": "1"})
		comment_folder.addParmTemplate(comment)
		ptg.addParmTemplate(comment_folder)
	
	# Add custom Focal actions
	# focal point
	pt = hou.FloatParmTemplate("f", "Focus point",3)
	pt.setTags({"script_action": "n = kwargs[\"node\"]\n\nimport toolutils\nsv = toolutils.sceneViewer()\nsv.setSnappingMode(hou.snappingMode.Prim)\npos = sv.selectPositions(number_of_positions=1)\n\nif pos[0].length() > 0:\n	n.parmTuple(\"f\").set(pos[0])\nsv.setSnappingMode(hou.snappingMode.Off)"})
	ptg.addParmTemplate(pt)
	# focal distance
	pt = hou.FloatParmTemplate("f2t", "Focal2Target", 1)
	pt.setTags({"script_action": "n = kwargs[\'node\']\nn.parm(\'RS_campro_dofDistance\').set(n.parm(\"f2t\"))\n"})
	pt.setDefaultExpressionLanguage([hou.scriptLanguage.Python])
	pt.setDefaultExpression(["(hou.pwd().worldTransform().extractTranslates()-hou.Vector3(hou.pwd().parmTuple('f').eval())).length()"])
	ptg.addParmTemplate(pt)

	cam.setParmTemplateGroup(ptg)
	
	# use our custom dof
	#cam.parm("RS_campro_dofUseHoudiniCamera").set(0)
	cam.parm('RS_campro_dofDistance').set(cam.parm("f2t"))
	cam.parm("RS_campro_dofCoC").set(0.02)
	
def AddHDRLoader(newnode):
	# Add LZ Controlls
	ptg = newnode.parmTemplateGroup()
	# HDR IMAGE
	hdr_img = hou.StringParmTemplate("hdr_img",
								"HDR_img",
								1,
								default_value=([]),
								string_type=hou.stringParmType.FileReference,
								item_generator_script="""
	import os.path
	menuItems = []
	n = kwargs[\'node\']
	folder = n.parm(\'hdr_dir\').eval()
	folder = os.path.abspath(folder)
	
	from glob import glob
	items =  glob(folder + \"/*\")
	
	for i in items:
		path = i.split(\'\\\\\')
		tex = path.pop()
		if not tex.endswith('.rstexbin'):	
			menuItems += {i}
			menuItems += {tex}		
	return menuItems""",
								item_generator_script_language=hou.scriptLanguage.Python,
								menu_type=hou.menuType.Normal)							
	hdr_img.setTags({"script_action": """
n = kwargs['node']
if n.parm(\'xn__inputstexturefile_r3ah\'):
	n.parm(\'xn__inputstexturefile_r3ah\').set(kwargs['node'].parm(\'hdr_img\'))
if n.parm(\'env_map\'):
	n.parm(\'env_map\').set(kwargs['node'].parm(\'hdr_img\'))		
	"""})
	ptg.addParmTemplate(hdr_img)
	# HDR Folder
	default_folder = "S:/CloudStation/Assets/HDRI/Heaven/"
	if not os.path.isdir(default_folder):
		default_folder = "X:/Assets/HDRI/Heaven/"
	if not os.path.isdir(default_folder):
		default_folder = "S:/Temp/HDRI/Heaven/"	
	if not os.path.isdir(default_folder):
		default_folder = "S:/Assets/HDRI/Heaven3/" 
	
		
	hdr_dir = hou.StringParmTemplate("hdr_dir",
									"HDR_dir",
									1,
									default_value=([default_folder]),
									string_type=hou.stringParmType.FileReference,
									item_generator_script_language=hou.scriptLanguage.Python,
									menu_type=hou.menuType.StringReplace)
	hdr_dir.setFileType(hou.fileType.Directory)
	ptg.addParmTemplate(hdr_dir)
	# Next Button
	next_btn = hou.ButtonParmTemplate("next", "Next")
	next_btn.setScriptCallback("n = hou.pwd();p = n.parm(\"hdr_img\");mi = p.menuItems();p.set(mi[mi.index(p.eval())+1])")
	next_btn.setScriptCallbackLanguage(hou.scriptLanguage.Python)
	ptg.addParmTemplate(next_btn)
	# Prev Button
	prev_btn = hou.ButtonParmTemplate("prev", "Prev")
	prev_btn.setScriptCallback("n = hou.pwd();p = n.parm(\"hdr_img\");mi = p.menuItems();p.set(mi[mi.index(p.eval())-1])")
	prev_btn.setScriptCallbackLanguage(hou.scriptLanguage.Python)
	ptg.addParmTemplate(prev_btn)
	# Rotate Button
	rotate_btn = hou.ButtonParmTemplate("rotate", "Rotate")
	rotate_btn.setScriptCallback("hou.pwd().parm(\'ry\').setExpression(\'360*$F/$FEND\')")
	rotate_btn.setScriptCallbackLanguage(hou.scriptLanguage.Python)
	rotate_btn.setTags({"script_callback": "hou.pwd().parm(\'ry\').setExpression(\'360*$F/$FEND\')", "script_callback_language": "python"})
	ptg.addParmTemplate(rotate_btn)
	# Freeze Rotete button
	freeze_btn = hou.ButtonParmTemplate("freeze", "Freeze")
	freeze_btn.setScriptCallback("hou.pwd().parm(\'ry\').deleteAllKeyframes()")
	freeze_btn.setScriptCallbackLanguage(hou.scriptLanguage.Python)
	freeze_btn.setTags({"script_callback": "hou.pwd().parm(\'ry\').deleteAllKeyframes()", "script_callback_language": "python"})
	ptg.addParmTemplate(freeze_btn)
	
	newnode.setParmTemplateGroup(ptg)
	
	if len(newnode.parm("hdr_img").menuItems()) > 0:
		newnode.parm("hdr_img").set(newnode.parm("hdr_img").menuItems()[0])
	  
def AovIndexFromName(rs, aov_name):
	for i in range(0,rs.parm("RS_aov").eval()):
		if rs.parm(f"RS_aovSuffix_{i+1}").eval() == aov_name:
			return i+1
	return 0
	
def toggleAovs(rs, aovs , on):
	for aov in aovs: rs.parm("RS_aovEnable_" + str(AovIndexFromName(rs,aov))).set(on)

def AddBasicAovs(rs):
	aov_dict = [
	["beauty" , 39],
	["diffuse",18],
	["specular" , 8],
	["reflection" , 11],
	["refraction" , 14],
	["emission" , 17],
	["SSS" , 9],
	["GI" , 18],

	["diffuseFilter" , 7],
	["Z" , 1],
	["P" , 0],
	["N" , 24],
	["shadows" , 23],

	["VolumeLighting" , 27],
	["VolumeFogTint" , 28],
	["VolumeFogEmission" , 29],

	["cryptomatte" , 41],
	["cryptomatte_mat" , 41]
	]

	rs.parm("RS_cryptomatteFullPaths").set(1)
	rs.parm("RS_aovGUIHideOptions").set(1)

	# add basic aovs
	rs.parm("RS_aov").set(len(aov_dict))
	for index,item in enumerate(aov_dict,start=1):
		rs.parm(f"RS_aovID_{index}").set(item[1])
		rs.parm(f"RS_aovSuffix_{index}").set(item[0])
	
	# beauty all lights
	rs.parm("RS_aovLightAllGroups_" + str(AovIndexFromName(rs,"beauty"))).set(1)
	# cryptomatte matte
	rs.parm("RS_aovCryptomatteType_" + str(AovIndexFromName(rs,"cryptomatte_mat"))).set(1)
	# Z depth center sample
	rs.parm("RS_aovDeepFilter_" + str(AovIndexFromName(rs,"Z"))).set(3)

def addQuickAovToggles(rs):
	is_node = isinstance(rs, hou.Node)
	ptg = rs.parmTemplateGroup() if is_node else rs
	
	insert_parm = ptg.find('RS_cryptomatteFullPaths')
	insert_canoe =  ptg.find('Canoe_RS_aovAllAOVsDisabled')
	join = 0 
	for parm in reversed(aov_toggles):
		name = parm[0]
		label = name.split("_")[0]
		aovs = parm[1]
		script = f'import lzRS_Shelf;lzRS_Shelf.toggleAovs(hou.pwd(),{aovs},kwargs["script_value"]=="on")'
		toggle = hou.ToggleParmTemplate(name,label,1,script_callback = script)
		toggle.setScriptCallbackLanguage(hou.scriptLanguage.Python)	
		toggle.setJoinWithNext(join)	
		toggle.setConditional(hou.parmCondType.DisableWhen, "{ RS_aovAllAOVsDisabled == 1 }")		
		ptg.insertAfter(insert_parm , toggle)   
		
		# shortcut on canoe 
		sc = hou.ToggleParmTemplate("sc_" + name,label,1) 
		sc.setJoinWithNext(join)
		sc.setConditional(hou.parmCondType.DisableWhen, "{ Canoe_aovAllAOVsDisabled == 1 }")		
		ptg.insertAfter(insert_canoe , sc)
		join = 1
	
	if is_node : 
		rs.setParmTemplateGroup(ptg)
		link_aov_toggles_toCanoeTab(rs)
	
def link_aov_toggles_toCanoeTab(rs):
	# link shortcuts
	for parm in reversed(aov_toggles):
		rs.parm(parm[0]).set(rs.parm("sc_" + parm[0]))
		#rs.parm("sc_" + parm[0]).set(0)

def RopnetAddRS(ropnet):
    rs = ropnet.createNode("Redshift_ROP","Redshift")
    # IPR
    ipr = ropnet.createNode("Redshift_IPR","Redshift_Ipr")    
    ipr.moveToGoodPosition()
    ipr.parm("linked_rop").set("../Redshift")
    
    # RS
    rs.setParms(canoe_rs_parms)
    AddBasicAovs(rs)
    rs.setParmExpressions(canoe_rs_parmExp)
    CreateCanoeRenderTab(rs)       
    return rs
	
def RS_RopnetPromote(rs):
    # Promote RS parms to Subnet
    promote_list =  ["shortcuts" , "renderpreview","RS_IPRVP","trange","f"]
    lzutil.PromoteParmsToParent(rs, promote_list)       

    rs.setParms({ "RS_lights_candidate" : "../RS_*", "RS_objects_candidate" : "../RS_*"  })