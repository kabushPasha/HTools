import hou
import os

def getAcesConverter():
    # Check If texture Converter Exists
    converter  = hou.node('/obj/ACES_Converter')

    if converter is None:
        converter = hou.node('/obj').createNode("cop2net","ACES_Converter")
        
        IN_srgb = converter.createNode("file","IN_srgb")
        IN_srgb.parm("linearize").set(0)
        vopFilter = IN_srgb.createOutputNode("vopcop2filter","Filter")
        
        vop_global = vopFilter.node('global1')
        vop_output = vopFilter.node('output1')
        vop_f2v = vopFilter.createNode('floattovec')
        vop_f2v.setInput(0,vop_global,3)
        vop_f2v.setInput(1,vop_global,4)
        vop_f2v.setInput(2,vop_global,5)
        vop_ocioT = vop_f2v.createOutputNode('ocio_transform')
        vop_ocioT.parm("fromspace").set('Output - Rec.709')
        vop_ocioT.parm("tospace").set('ACES - ACEScg')
        vop_v2f = vop_ocioT.createOutputNode('vectofloat')
        vop_output.setInput(0,vop_v2f,0)
        vop_output.setInput(1,vop_v2f,1)
        vop_output.setInput(2,vop_v2f,2)
        
        out_Aces = vopFilter.createOutputNode("rop_comp","OUT_ACES")
        out_Aces.parm("trange").set(0)
        out_Aces.parm("convertcolorspace").set(0)
    return converter
	
	
def convertToAces(in_path,out_path):
	converter = getAcesConverter()		
	converter.node("IN_srgb").parm("filename1").set(in_path) 
	converter.node("OUT_ACES").parm("copoutput").set(out_path) 	
	converter.node("OUT_ACES").parm("execute").pressButton()
	
	
def convertToAces_srgbFolder(file_path):	
	path = os.path.abspath(file_path)  
	if not os.path.isdir(os.path.dirname(path) + "/sRGB"):
		os.mkdir(os.path.dirname(path) + "/sRGB")

	new_path = os.path.dirname(path) + "/sRGB/" + os.path.basename(path)
	if os.path.isfile(new_path):
		print (os.path.basename(path) + " already converted")
	else:
		print ("Converting " + path)
		os.rename(path, new_path)
		convertToAces(new_path,path)