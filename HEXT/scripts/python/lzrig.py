import hou


def clearWorldRotates(n):
	parent = n.inputs()[0]	
	n.parm("keeppos").set(1)
	n.setInput(0,None)

	n.setParmTransform(n.parmTransform()*n.preTransform())
	n.parmTuple("r").set((0,0,0))
	n.setPreTransform(n.parmTransform())
	n.setParmTransform(hou.Matrix4(1))

	n.setInput(0,parent)

# EXTRACT TRUE bone rotates from chopnet
def extractIKBoneRotates(n,use_asset_prefix):    
	ptg = n.parmTemplateGroup()
	if ptg.find('ir') is not None:
		n.parmTuple('ir').lock((0,0,0))
		ptg.remove('ir')
	parm = hou.FloatParmTemplate("ir","Real Rotate",3)
	ptg.addParmTemplate(parm)
	n.setParmTemplateGroup(ptg) 
    
	solver = n.parm('solver').eval()
	
	if use_asset_prefix:
		asset_prefix = "/" + n.parent().type().name()
	else:
		asset_prefix = ""
		
	base_expr = 'chop("' + solver + asset_prefix + "/" + n.name()
	base_expr = 'chop("' + solver + "/" + '"+oprelativepath("/obj/",".")+"'
	
	
	expression =  base_expr + ':rx")'
	n.parm('irx').setExpression(expression)
	expression =  base_expr + ':ry")'
	n.parm('iry').setExpression(expression)
	expression =  base_expr + ':rz")'
	n.parm('irz').setExpression(expression)
	
	n.parmTuple('ir').lock((1,1,1))

def createHelperBone(n,angle,use_asset_prefix):
	extractIKBoneRotates(n,use_asset_prefix)

	helper = n.inputs()[0].createOutputNode("bone",n.name() + "_helper")
	helper.setPosition(n.position() + hou.Vector2(-2.5 -2.5*(angle>0),0))
	
	pt = n.preTransform()
	helper.parmTuple("r").set(pt.extractRotates()*0.5 + hou.Vector3(angle,0,0))

	helper.parm("length").set(0.1)
	helper.useXray(1)

	createHelperBoneParms(helper,n)
	cleanTransfrom(helper)

	helper.parm('rx').setExpression('ch("driver")*0.5')

	
def createHelperBoneParms(bone,target):
	ptg = bone.parmTemplateGroup()
	
	parm = hou.FloatParmTemplate('correct_length','',2)
	ptg.addParmTemplate(parm)
	parm = hou.FloatParmTemplate('correct_angle','',2)
	ptg.addParmTemplate(parm)
	parm = hou.FloatParmTemplate('driver','',1)
	parm.setDefaultExpression(('ch("' + bone.relativePathTo(target) + '/irx")',))
	ptg.addParmTemplate(parm)
	
	parm = hou.FloatParmTemplate('corrected_length','',1)
	expr = 'fit(ch("driver"),ch("correct_anglex"),ch("correct_angley"),ch("correct_lengthx"),ch("correct_lengthy"))'
	parm.setDefaultExpression((expr,))
	ptg.addParmTemplate(parm)
	
	bone.setParmTemplateGroup(ptg)
	
	
	bone.parm('correct_lengthx').set(bone.parm('length').eval())
	bone.parm('correct_lengthy').set(bone.parm('length').eval()*1.5)
	bone.parm('correct_anglex').set(0)
	bone.parm('correct_angley').set(90)
	bone.parm('corrected_length').lock(1)
	bone.parm('length').setExpression('ch("corrected_length")')
	
def cleanTransfrom(n):
	n.setPreTransform(n.parmTransform()*n.preTransform())
	n.setParmTransform(hou.Matrix4(1))



def exportIKRotations(n):
	solver = n.parm('solver')
	if solver is not None:
		solver = n.node(solver.evalAsString())
		if solver is not None:
			#Create ir parm
			ptg = n.parmTemplateGroup()
			if ptg.find('ir') is not None:
				n.parmTuple('ir').lock((0,0,0))
				ptg.remove('ir')
			parm = hou.FloatParmTemplate("ir","Real Rotate",3)
			ptg.addParmTemplate(parm)
			n.setParmTemplateGroup(ptg) 	
			
			#create rename node
			rename = solver.createOutputNode("rename","rename_"  + n.name())
			rename.setPosition(solver.position() + hou.Vector2(0,-0.8))
			rename.parm("renamefrom").set('*' + n.name() + ':r*')
			rename.parm("renameto").set('ir*')
		
			
			#create export node
			export = rename.createOutputNode("export","export_" + n.name())
			export.setPosition(rename.position() + hou.Vector2(0,-0.8))
			export.parm("channels").set('ir*')
			export.parm("nodepath").set('../../' + n.name())
			export.parm("path").set('ir*')
			export.setExportFlag(1)


def createPerFaceHooks(n):
	end = n.displayNode()
	#create make_face_uvs node
	make_face_uvs = end.createOutputNode("attribwrangle","make_face_uvs")
	make_face_uvs.setPosition(end.position() + hou.Vector2(0,-1))
	make_face_uvs.parm("class").set(1)
	make_face_uvs.parm("snippet").set('int pts[] = primpoints(0,@primnum);\nsetpointattrib(0,"uv",pts[0],{0,0,0} + set(@primnum,0,0));\nsetpointattrib(0,"uv",pts[1],{0,1,0} + set(@primnum,0,0));\nsetpointattrib(0,"uv",pts[2],{1,1,0} + set(@primnum,0,0));\nsetpointattrib(0,"uv",pts[3],{1,0,0} + set(@primnum,0,0));')

	#create OUT_HOOKS node
	OUT_HOOKS = make_face_uvs.createOutputNode("null","OUT_HOOKS")
	OUT_HOOKS.setPosition(make_face_uvs.position() + hou.Vector2(0,-1))

	for prim in OUT_HOOKS.geometry().prims():		
		tasset_hook = n.createOutputNode("sticky",n.name() + "_hook1")
		tasset_hook.setPosition(n.position() + hou.Vector2(1.5*(hou.hscriptExpression('opdigits("' + tasset_hook.name() + '")')-1),-1))
		tasset_hook.parm("stickysop").set('../`opinput(".",0)`/OUT_HOOKS')
		tasset_hook.parm('stickyuv1').setExpression('opdigits($OS) - 0.5',language = hou.exprLanguage.Hscript)
		tasset_hook.setDisplayFlag(True)
		#kinda bad kinda lazy
		tasset_hook.parm("stickyurange2").set(100.0)
		tasset_hook.setDisplayFlag(0)
		
		#create tasset_hook_ctrl node
		tasset_hook_ctrl = tasset_hook.createOutputNode("null",tasset_hook.name() + "_ctrl")
		tasset_hook_ctrl.setPosition(tasset_hook.position() + hou.Vector2(0.0,-1))
		tasset_hook_ctrl.parm("geoscale").set(0.05)
		tasset_hook_ctrl.parm("controltype").set(1)		

		clearWorldRotates(tasset_hook_ctrl)

		
		
		
		
		

		
	






	