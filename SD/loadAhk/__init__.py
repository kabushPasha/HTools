import sd
import sdplugins
import os

class AHK(sdplugins.Plugin):
    sPluginDesc = sdplugins.PluginDesc(
        aLabel = 'AHK',
        aTooltip = 'Load The AutoHotkey Substance designer file',
        aPluginLocation=sdplugins.PluginLocationToolbar(sdplugins.ToolBarId.Main, 0),
        aIconFileAbsPath = '')

    def run(self, aContext) :
        ahk = "S:/HTools/SD/LZAHK.ahk"
        os.system("start " + ahk)
        pass

# Register module classes
sd.getContext().getSDApplication().registerModule(__name__)

