hou.hscript("exread -v $HEXT/hscript.txt")

import glob
path = hou.expandString('$JOB/hda/')
hdas = glob.glob(path + '*.hda' )
for hda in hdas:
    hou.hda.installFile(hda)


