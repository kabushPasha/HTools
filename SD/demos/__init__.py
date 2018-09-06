import sd
import sdplugins
import os
from sd.api.sdproperty import SDPropertyCategory

class demoPlugin(sdplugins.Plugin):
	sPluginDesc = sdplugins.PluginDesc(
		aLabel = 'demo plugin',
		aTooltip = 'open an sbs and export the outputs',
		#aPluginLocation = sdplugins.PluginLocationMenu(sdplugins.MenuId.Scripts, 'demo', 0),
		aPluginLocation = sdplugins.PluginLocationToolbar(sdplugins.ToolBarId.SBSCompGraph,0),
		aIconFileAbsPath = '')


	def run(self, aContext) :
		# Put your code here
		sdContext = sd.getContext()
		sdApplication = sdContext.getSDApplication()		
		pkgManager = sdApplication.getPackageMgr()		
		#pkg = pkgManager.loadUserPackage("S:/MEGA/Projects/Substance/2018/01_MudGrass/Grass.sbs")	
		pkg = pkgManager.getUserPackageFromFilePath("S:/MEGA/Projects/Substance/2018/01_MudGrass/Grass.sbs")
		sbsCompGraph = 	pkg.findResourceFromUrl("Mud")
		sbsCompGraph.compute()
		
		for sbsCompOutputNode in sbsCompGraph.getOutputNodes():
			#print(sbsCompOutputNode)			
			for sdOutputProperty in sbsCompOutputNode.getProperties(SDPropertyCategory.Output):
				#print(sdOutputProperty.getLabel())			
				sdPropertyValue = sbsCompOutputNode.getPropertyValue(sdOutputProperty)
				#print(sdPropertyVale)
				sdTexture = sdPropertyValue.toSDTexture()
				filename = os.path.abspath('S:/MEGA/Projects/Substance/2018/01_MudGrass/tex/' +sdOutputProperty.getLabel() + ".png" )
				sdTexture.save(filename)
		pass

# Register module classes
sd.getContext().getSDApplication().registerModule(__name__)

