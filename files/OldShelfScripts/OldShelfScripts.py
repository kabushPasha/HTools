#OLD SHELF TOOLS
# To remove:
# LZ Dops - setups for cutting glue in sop network
# LZ Fracture - some setups for fractureing



#======================================================================
# Create Visualisers 
import lzutil
import toolutils
n = lzutil.viewNode()
geo = n.geometry()
pt_attribs = geo.pointAttribs()

sv = toolutils.sceneViewer()
vp = sv.curViewport()

att_names = []
pt_attribs_filtered = []

for att in pt_attribs:
    if att.name()!='P' and att.name()!='N' and att.name()!='v':
        att_names += [att.name()]
        pt_attribs_filtered += [att]

ans = hou.ui.selectFromList(att_names)

for id  in ans:
    att = pt_attribs_filtered[id]
    size = att.size()        
    v = hou.viewportVisualizers.createVisualizer(hou.viewportVisualizers.type('vis_marker'))
    v.setName(att.name())
    v.setLabel(att.name())
    v.setParm('attrib',att.name())
    if size > 2:
        v.setParm('style','vector')
    v.setIsActive(1,vp)    


#======================================================================
# LZ Flipbook
import toolutils
import os
if kwargs['ctrlclick'] == True:
    import subprocess
    dir = hou.expandString('$HC') +"\\"+ hou.expandString('$HIPNAME') + "\\FB"
    subprocess.Popen('explorer "' + dir  + '"');
else:
    dir = hou.expandString("$HC/$HIPNAME/FB")
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    dir += "/"
    
    files = os.listdir(dir)
    if len(files) > 0:
        increment = int(files[len(files)-1].split("_")[0]) + 1
    else:
        increment = 1
        
        
    user_input = hou.ui.readInput("Flipbook name",buttons=('Render','Cancel'),initial_contents=str(increment).zfill(3)+" " )
    if user_input[0] == 0:
        name = str(user_input[1])
        name = "_".join(name.split())
        
        sv = toolutils.sceneViewer()
        
        fbs =  sv.flipbookSettings().stash()
        fbs.output(dir + name + "_$F.pic")
        sv.flipbook(None,fbs)    
        
        import subprocess
        ip = hou.expandString('$HB/mplay')
        seq = hou.expandString(dir + name + '_*.pic')
        subprocess.Popen([ip, seq])



#=================================================================================
# LZ Background Image
# save sreenshot
import toolutils
import os,subprocess
import lzutil

# Set directory for screenshots
unexpandedDir = "$JOB/Flipbook/BG_Snapshots"
dir = hou.expandString(unexpandedDir)  + '/'

# Ask User For a name
if not os.path.exists(dir):
    os.makedirs(dir)
files = os.listdir(dir)
increment = 1
if len(files) > 0:
    increment += int(files[len(files)-1].split("_")[0])    
user_input = hou.ui.readInput("SnapshotName",buttons=('Snapshot','Cancel'),initial_contents=str(increment).zfill(3)+" " )


if user_input[0] == 0:
    name = str(user_input[1])
    name = "_".join(name.split()) + ".png"
    
    # Capture a flipbook
    sv = toolutils.sceneViewer()
    fbs =  sv.flipbookSettings().stash()
    fbs.output(dir + name)
    fbs.frameRange(hou.Vector2(hou.frame(),hou.frame()))
    fbs.beautyPassOnly(True)
    fbs.outputZoom(25)
    fbs.outputToMPlay(1)
    sv.flipbook(None,fbs)  
    
    
        
    #create new network image
    editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    path =  unexpandedDir + "/" + name
    lzutil.copyToClipboard(path)
    
    position = hou.Vector2(editor.visibleBounds().center() + hou.Vector2(0,0));
    w = editor.visibleBounds().size().x()* 0.45
    h = w
    
    image = hou.NetworkImage()
    image.setPath(path)
    image.setRect(hou.BoundingRect(position[0]-w, position[1]-h, position[0]+w, position[1]+h))
    images = editor.backgroundImages()
    images = images + tuple([image])    
    editor.setBackgroundImages(images)



#=================================================================================
# Substance Designer Autohotkey
import os
ahk = hou.expandString("$HEXT/LZAHK.ahk")
#print ahk
os.system("start " + ahk)





#=================================================================================
# Convert a video with FFmpeg
## OLD way with djv-view
from glob import glob
import os
f = hou.ui.selectFile(collapse_sequences=True,multiple_select=True)
# Find First and Last Frames
fslpit = f.split("$F4")
gstring =  hou.expandString(fslpit[0]) + "*" + fslpit[1]
max = -1e6;
min = 1e6;
maxs = "";
mins = "";

frames = []

for frame in glob(gstring):
    frame = frame.replace('\\',"/")
    fstr = frame.replace(hou.expandString(fslpit[0]),"").replace(fslpit[1],"")
   
    print frame + "  " + fstr + " " + frame.replace(hou.expandString(fslpit[0]),"")
    
    if int(fstr) < int(min):
        min = fstr
        mins = fstr
    if int(fstr) > int(max):
        max = fstr
        maxs = fstr
# Create Script        
seq =  hou.expandString(fslpit[0]) + mins+"-"+maxs + fslpit[1]

print seq
converter = r"C:\Program Files\djv-1.1.0-Windows-64\bin\djv_convert.exe"
#outName = hou.expandString(fslpit[0]).rsplit("/",2)[-2] + ".mp4"
out = os.path.dirname(hou.expandString(fslpit[0])) +  ".mp4"

print out

import subprocess
subprocess.Popen([converter,seq,out])
import lzutil
lzutil.openFolderFromEnv(os.path.dirname(os.path.dirname(hou.expandString(fslpit[0]))))

"""
# New way with ffmpeg
f = hou.ui.selectFile(collapse_sequences=False,multiple_select=False)
f = hou.expandString(f)
import os
start_frame = int(os.path.basename(f).rsplit(".")[0])
folderName = os.path.basename(os.path.dirname(f))
path = os.path.dirname(f) + "/%4d.jpg"
out = os.path.dirname(f) + ".mp4";

t = '"'

#cmd = ["ffmpeg","-i",path,"-c:v","libx264","-preset","veryslow","-crf","0","-vf",'"scale=trunc(iw/2)*2:trunc(ih/2)*2"',out]
cmd = ["ffmpeg","-i",t + path + t,t+out+t]

code = ""
for line in cmd:
    code += " " + line
    print line
    
print code    

import subprocess
subprocess.Popen(cmd)

#os.system(code)
"""

#=================================================================================
# LZ Hair Utils Mesh Prepare
#create timeshift node
source = hou.selectedNodes()[0]
timeshift = source.createOutputNode("timeshift","timeshift")
timeshift.setPosition(source.position() + hou.Vector2(0,-1))
timeshift.parm("frame").set(1.0)

#create vdbfrompolygons node
vdbfrompolygons = source.createOutputNode("vdbfrompolygons","vdbfrompolygons")
vdbfrompolygons.setPosition(source.position() + hou.Vector2(3,-1))

#create OUT_vdb node
OUT_vdb = vdbfrompolygons.createOutputNode("null","OUT_vdb")
OUT_vdb.setPosition(vdbfrompolygons.position() + hou.Vector2(0,-1))

#create OUT_animated node
OUT_animated = source.createOutputNode("null","OUT_animated")
OUT_animated.setPosition(source.position() + hou.Vector2(-3,-1))

#create OUT_static node
OUT_static = timeshift.createOutputNode("null","OUT_static")
OUT_static.setPosition(timeshift.position() + hou.Vector2(0,-1))

#=================================================================================
# LZ Compare nodes (now we have better hilights)
nodes = hou.selectedNodes()
parm_dicts = ()
    
for node in nodes:
    node_parms = {}
    parm_tuple = [(node.name(), node.parmTuples())]
    node_parms.update(parm_tuple)
    parm_dicts += (node_parms,)

a_parm_vals = []
b_parm_vals = []
parm_labels = []    
    
node = nodes[0]
for parm_tuple in parm_dicts[nodes.index(node)][node.name()]:
    for parm in parm_tuple:
            a_parm_vals.append(parm.evalAsString())
            parm_labels.append(parm.name())

node = nodes[1]            
for parm_tuple in parm_dicts[nodes.index(node)][node.name()]:
    for parm in parm_tuple:
            b_parm_vals.append(parm.evalAsString())

            
if a_parm_vals != b_parm_vals:
    message = "Changed parameters :" + '\n'
    for val in range(0, len(parm_labels) - 1):
        if a_parm_vals[val] != b_parm_vals[val]:
            message += parm_labels[val] + '\n'
            message += '\t' + nodes[0].name() +" = " + a_parm_vals[val] + '\n' 
            message += '\t' + nodes[1].name() +" = " + b_parm_vals[val] + '\n'
else:
    message = "nodes are the same"

print message

#=================================================================================
# Send to nuke
# (no idea what i wanted to do)
ipr =  hou.ui.paneTabOfType(hou.paneTabType.IPRViewer,0);

import os
dir = hou.expandString("$HC/$HIPNAME/render") 
if not os.path.exists(dir):
    os.makedirs(dir)
dir += "/"

files = os.listdir(dir)
if len(files) > 0:
    increment = int(files[len(files)-1].split("_")[0]) + 1
else:
    increment = 1

name = str(increment).zfill(3)+"_screenshot.pic"

path = dir + name + ".exr"

ipr.saveFrame(path)
# copy dir to clipboard
import PySide.QtGui as qtg
app = qtg.QApplication.instance()
clipboard = app.clipboard()
clipboard.setText(path)

#=================================================================================
# LZ Create Chopnet
# now we have an hda
if hou.selectedNodes() is not ():
    for node in hou.selectedNodes():
        if node.type().name()=='channel':
            chopnet = node.parent().createNode("chopnet")
            chopnet.setPosition(node.position() + hou.Vector2(2,0))
            
            geo = chopnet.createNode('geometry')
            geo.parm("soppath").set('`opinputpath("../../' + node.name() + '",0)`')
            geo.parm("method").setExpression('ch("../../' + node.name() + '/method")')
            
            #geo.parm("attribscope").set('`chs("../../' + node.name() + '/attscope")`')
            #geo.parm("renamescope").set('`chs("../../' + node.name() + '/chanscope")`')
            node.parm("attscope").set('`chs("../' + chopnet.name() + "/" + geo.name() + '/attribscope")`')
            node.parm("chanscope").set('`chs("../' + chopnet.name() + "/" + geo.name() + '/renamescope")`')
                        
            node.parm("attscope").lock(True)
            node.parm("chanscope").lock(True)
            
            out = geo.createOutputNode('null')
            
            node.parm('choppath').set("../" + chopnet.name() + "/" + out.name())
            
#=================================================================================
# Cheack Shelf Paaths
# (in case we saved our tool to our home directory)
from PySide2.QtWidgets  import  QApplication
shelf = QApplication.clipboard().text()

sh = hou.shelves.shelves()[shelf]
for t in sh.tools():
    if sh.filePath() != t.filePath():
        print t.name()
        
        
shelf = QApplication.clipboard().setText(sh.filePath())










