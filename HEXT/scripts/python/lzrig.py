import hou

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
	
	



	