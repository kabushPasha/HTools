import os
from glob import glob

print "LZ: PadZero4 for sequences"

# get Command Line Arguments
#import sys
#print sys.argv

cwd = os.getcwd()
#print cwd

renamed = 0
skipped = 0

for file in glob(cwd + "\\" + "*"):
	filename = os.path.basename(file)
	ext = filename.rsplit(".",1)[1]
	name = filename.rsplit(".",1)[0]
	if name.isdigit():
		newName =  os.path.dirname(file) +"\\" + name.zfill(4) + "." + ext		
		os.rename(file, newName)
		renamed += 1
	else:
		skipped += 1


print "Ranamed " + str(renamed) + " files"
print "Skipped " + str(skipped) + " files"