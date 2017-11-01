import hou
import toolutils

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
	if n.type().name() == 'attribwrangle': 
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



	
			
			
			
			
		