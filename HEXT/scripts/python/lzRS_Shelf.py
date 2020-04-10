import lzutil
import hou

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
    
    # Code for parameter template
    DeadlineRender_btn = hou.ButtonParmTemplate("submit_to_deadline", "Deadline Render")
    DeadlineRender_btn.setScriptCallback("import lzutil;lzutil.lzDeadline.submitRS2Deadline(hou.pwd())")
    DeadlineRender_btn.setScriptCallbackLanguage(hou.scriptLanguage.Python)
    folder.addParmTemplate(DeadlineRender_btn)
    
    before = "RS_rrs2"
    ptg.insertAfter(before,folder)
    n.setParmTemplateGroup(ptg)
    
    
    parms = ["RS_renderCamera","RS_outputFileNamePrefix","RS_archive_enable",
    "RS_archive_file","MotionBlurEnabled","VolLightingEnabled","RS_aovAllAOVsDisabled",
    "TessellationDisplacementEnable"]
    
    for parm in parms:
        n.parm(parm).set(n.parm(parm + "2"))


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
    
    
