import hou

def extractIKBoneRotates(n):    
	ptg = n.parmTemplateGroup()
	if ptg.find('ir') is not None:
		n.parmTuple('ir').lock((0,0,0))
		ptg.remove('ir')
	parm = hou.FloatParmTemplate("ir","Real Rotate",3)
	ptg.addParmTemplate(parm)
	n.setParmTemplateGroup(ptg) 
    
	solver = n.parm('solver').eval()
	
	expression = 'chop("' + solver + "/" + n.name() + ':rx")'
	n.parm('irx').setExpression(expression)
	expression = 'chop("' + solver + "/" + n.name() + ':ry")'
	n.parm('iry').setExpression(expression)
	expression = 'chop("' + solver + "/" + n.name() + ':rz")'
	n.parm('irz').setExpression(expression)
	
	n.parmTuple('ir').lock((1,1,1))

	
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
	
	
	
	
	