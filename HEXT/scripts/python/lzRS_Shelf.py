import hou
import lzutil
import subprocess

def CreateCanoeRenderTab(n):
	ptg = n.parmTemplateGroup()
	
	folder = hou.FolderParmTemplate("shortcuts","CANOE")
	
	Render_Cam = hou.StringParmTemplate("RS_renderCamera2", "Render Camera", 1, default_value=(["/obj/RS_Cam"]),string_type=hou.stringParmType.NodeReference)
	Render_Cam.setTags({"autoscope": "0000000000000000", "opfilter": "!!OBJ/CAMERA!!", "oprelative": "."})
	folder.addParmTemplate(Render_Cam)
	
	Output = hou.StringParmTemplate("RS_outputFileNamePrefix2", "Common File Prefix", 1, default_value=(["$JOB/Render/001_InitRender/$F4.exr"]),string_type=hou.stringParmType.FileReference, item_generator_script="opmenu -l . RS_outputFileNamePrefix", item_generator_script_language=hou.scriptLanguage.Hscript, menu_type=hou.menuType.StringReplace)
	folder.addParmTemplate(Output)
	folder.addParmTemplate(hou.SeparatorParmTemplate("sep1"))
	
	arhive_toggle = hou.ToggleParmTemplate("RS_archive_enable2", "Export .rs Proxy File", default_value=False, default_expression='off', default_expression_language=hou.scriptLanguage.Hscript)
	folder.addParmTemplate(arhive_toggle)
	
	archive = hou.StringParmTemplate("RS_archive_file2", "Filename", 1, default_value=(["$HIP/filename.$F4.rs"]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.FileReference, item_generator_script="opmenu -l . RS_archive_file", item_generator_script_language=hou.scriptLanguage.Hscript, menu_type=hou.menuType.StringReplace)
	folder.addParmTemplate(archive)
	folder.addParmTemplate(hou.SeparatorParmTemplate("sep2"))
	
	Motion_toggle = hou.ToggleParmTemplate("MotionBlurEnabled2", "Enable Motion Blur", default_value=False, default_expression='off', default_expression_language=hou.scriptLanguage.Hscript)
	folder.addParmTemplate(Motion_toggle)
	
	Fog_toggle = hou.ToggleParmTemplate("VolLightingEnabled2", "Enable Global Fog", default_value=False, default_expression='off', default_expression_language=hou.scriptLanguage.Hscript)
	folder.addParmTemplate(Fog_toggle)
	
	AOV_toggle = hou.ToggleParmTemplate("RS_aovAllAOVsDisabled2", "Disable All AOVs", default_value=True, default_expression='on', default_expression_language=hou.scriptLanguage.Hscript)
	folder.addParmTemplate(AOV_toggle)
	
	Tesselation_Toggle = hou.ToggleParmTemplate("TessellationDisplacementEnable2", "Enable Tessellation And Displacement", default_value=True, default_expression='on', default_expression_language=hou.scriptLanguage.Hscript)
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
	n.setParmTemplateGroup(ptg)    
	
	parms = ["RS_renderCamera","RS_outputFileNamePrefix","RS_archive_enable",
	"RS_archive_file","MotionBlurEnabled","VolLightingEnabled","RS_aovAllAOVsDisabled",
	"TessellationDisplacementEnable"]
	
	for parm in parms:
		n.parm(parm).set(n.parm(parm + "2"))


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
		rs.parm("RS_aovAllAOVsDisabled").set(1)
		rs.parm("RS_renderCamera").set("/obj/RS_Cam")
		rs.parm("RS_lights_candidate").set("RS_*")
		rs.parm("RS_objects_candidate").set("RS_*")
		rs.parm("RS_addDefaultLight").set(0)
		
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
		pane = hou.ui.findPane(25)
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
    pt.setTags({"script_action": "n = kwargs[\"node\"]\n\nimport toolutils\nsv = toolutils.sceneViewer()\nsv.setSnappingMode(hou.snappingMode.Prim)\npos = sv.selectPositions(number_of_positions=1)\n\nif pos[0].length() > 0:\n    n.parmTuple(\"f\").set(pos[0])\nsv.setSnappingMode(hou.snappingMode.Off)"})
    ptg.addParmTemplate(pt)
    # focal distance
    pt = hou.FloatParmTemplate("f2t", "Focal2Target", 1)
    pt.setTags({"script_action": "n = kwargs[\'node\']\nn.parm(\'RS_campro_dofDistance\').set(n.parm(\"f2t\"))\n"})
    pt.setDefaultExpressionLanguage([hou.scriptLanguage.Python])
    pt.setDefaultExpression(["(hou.pwd().worldTransform().extractTranslates()-hou.Vector3(hou.pwd().parmTuple('f').eval())).length()"])
    ptg.addParmTemplate(pt)

    cam.setParmTemplateGroup(ptg)
    
    # use our custom dof
    cam.parm("RS_campro_dofUseHoudiniCamera").set(0)
    cam.parm('RS_campro_dofDistance').set(cam.parm("f2t"))
    cam.parm("RS_campro_dofCoC").set(0.02)