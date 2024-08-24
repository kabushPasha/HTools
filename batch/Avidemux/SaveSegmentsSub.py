adm = Avidemux()
ed=Editor()
gui=Gui()

adm.setContainer("MKV", "forceAspectRatio=False", "displayWidth=1280", "displayAspectRatio=2", "addColourInfo=False", "colMatrixCoeff=2", "colRange=0", "colTransfer=2", "colPrimaries=2")
ext = "mkv"

Counter = 0
mark1 = 0
mark2 = 0

nbSeg = ed.nbSegments()

if not nbSeg:
    gui.displayError("Error", "No video loaded, nothing to do, bye")
    return

if nbSeg > 100:
    gui.displayInfo("Warning", "Maximum of 100 segments supported, but got " + str(nbSeg))
    nbSeg = 100

filename = ed.getRefVideoName(0)
if filename is None:
    gui.displayError("Error", "Cannot obtain reference video filename")
    return

filename = (splitext(filename))[0]
filename = basename(filename)

if filename is None:
    gui.displayError("Error", "Cannot obtain input basename")
    return

# Replace gui.dirSelect() below with output directory path for unattended operation.
#outdir = gui.dirSelect("Select output folder")
#if outdir is None:
#    gui.displayInfo("Warning", "No output folder selected, cannot proceed")
#    return

outdir = dirname(ed.getRefVideoName(0)) 
#if not os.path.isdir(outdir):
#	mkdir(outdir)

leadingZero = ""

for segmentIdx in range(nbSeg):
    mark2 += ed.getDurationForSegment(segmentIdx)
    if segmentIdx < 10:
        leadingZero = "0"
    adm.markerA = mark1
    adm.markerB = mark2
    Counter += adm.save(outdir + "/" + "CUT_" + filename + "-segment-" + leadingZero + str(segmentIdx) + "." + ext)
    mark1 = mark2

gui.displayInfo("Finished", str(Counter) + " files out of " + str(nbSeg) + " segments converted")