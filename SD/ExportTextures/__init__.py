import sd
import sdplugins
from sd.api.sdproperty import SDPropertyCategory
import os

class ExportTextures(sdplugins.Plugin):
    sPluginDesc = sdplugins.PluginDesc(
        aLabel = 'Export Textures',
        aTooltip = 'Exports Selected Textures and outputs to the apropriate folder',
        aPluginLocation=sdplugins.PluginLocationToolbar(sdplugins.ToolBarId.SBSCompGraph, 1),
        aIconFileAbsPath = '')

    def run(self, aContext) :
        print ("---")         
        # Put your code here
        app = aContext.getSDApplication()
        location = app.getLocationContext()
        selectedNodes = location.getSelectedNodes()
        graph = location.getCurrentGraph()
        
        sdContext = sd.getContext()
        sdApplication = sdContext.getSDApplication()
        pkgManager = sdApplication.getPackageMgr()
        
        pkgPath = pkgManager.getUserPackages()[0].getFilePath()
        graphname = graph.getIdentifier()
        print ("Graph: " + graphname)
        outdir = pkgPath.rsplit("/",1)[0] + "/Textures/" + graphname + "/"
        print ("OUTdir: " + outdir)

        if len(selectedNodes) == 0:
            # Export output Textures
            for sbsCompOutputNode in graph.getOutputNodes():
                    for sdOutputProperty in sbsCompOutputNode.getProperties(SDPropertyCategory.Output):
                        print(sdOutputProperty.getIdentifier())			
                        sdPropertyValue = sbsCompOutputNode.getPropertyValue(sdOutputProperty)
                        sdTexture = sdPropertyValue.toSDTexture()
                        filename = os.path.abspath(outdir +sdOutputProperty.getIdentifier() + ".png" )
                        sdTexture.save(filename)
        else:    
            for node in selectedNodes:
                '''
                for sdOutputProperty in node.getProperties(SDPropertyCategory.Annotation):
                    print (sdOutputProperty)            
                    print(sdOutputProperty.getLabel())
                    print(sdOutputProperty.getClassName())
                    print("id: " + str(sdOutputProperty.getIdentifier()))
                '''
                nodeName = node.getPropertyValueFromIdentifier('label',SDPropertyCategory.Annotation).toString()
                print (nodeName)
                
                for sdOutputProperty in node.getProperties(SDPropertyCategory.Output):
                    print(sdOutputProperty.getIdentifier())			
                    sdPropertyValue = node.getPropertyValue(sdOutputProperty)
                    sdTexture = sdPropertyValue.toSDTexture()
                    filename = os.path.abspath(outdir +sdOutputProperty.getIdentifier() + ".png" )
                    sdTexture.save(filename)
    
        pass

# Register module classes
sd.getContext().getSDApplication().registerModule(__name__)

