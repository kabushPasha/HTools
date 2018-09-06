import sd
import sdplugins
from sd.api.sdproperty import SDPropertyCategory

class ExportTextures(sdplugins.Plugin):
    sPluginDesc = sdplugins.PluginDesc(
        aLabel = 'Export Textures',
        aTooltip = 'Exports Selected Textures and outputs to the apropriate folder',
        aPluginLocation=sdplugins.PluginLocationToolbar(sdplugins.ToolBarId.SBSCompGraph, 1),
        aIconFileAbsPath = '')

    def run(self, aContext) :
        # Put your code here
        app = aContext.getSDApplication()
        location = app.getLocationContext()
        selectedNodes = location.getSelectedNodes()
        graph = location.getCurrentGraph()
        
        for node in selectedNodes:
            #print (node)
            '''            
            for sdOutputProperty in node.getProperties(SDPropertyCategory.Annotation):
                print (sdOutputProperty)            
                print(sdOutputProperty.getLabel())
                print(sdOutputProperty.getClassName())
                print("id: " + str(sdOutputProperty.getIdentifier()))
            '''
            nodeName = node.getPropertyValueFromIdentifier('label',SDPropertyCategory.Annotation).toString()
            print (nodeName)  
              
        print (graph)
        pass

# Register module classes
sd.getContext().getSDApplication().registerModule(__name__)

