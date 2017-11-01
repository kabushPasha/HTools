import hou
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