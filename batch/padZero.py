import os,sys
from glob import glob
print "LZ: PadZero4 for sequences"


# Set The Mode
mode = "brackets"
if len(sys.argv) > 1:
	if sys.argv[1] == 'mp':
		mode = "mplay"
	elif sys.argv[1] == 'rn':
		mode = "rename"
	elif sys.argv[1] == 'ma':
		mode = "magick"
	elif sys.argv[1] == 'br':
		mode = "brackets"
	else:
		print "Use:"
		print "rn - simply rename files to pad 0" 
		print "ma - use image magick to convert to jpgs" 
		print "mp - use play to convert files based on creation date" 
		mode  = "help"


if mode != "help":
	print "Mode is " + mode		
	cwd = os.getcwd()
	folderName = cwd.split("\\")[-1]
	renamed = 0
	skipped = 0
	files = glob(cwd + "\\" + "*")

	if mode == "mplay":
		files.sort(key=os.path.getmtime)

		if not os.path.exists(cwd + "\\" + folderName):
			os.makedirs(cwd + "\\" + folderName)

		i = 1;
		for file in files:
			filename = os.path.basename(file)
			ext = filename.rsplit(".",1)[1]
			newName = os.path.dirname(file) +"\\" +folderName+ "\\" + str(i).zfill(4) + ".jpg"
			if ext != ".jpg":
				cmd = "iconvert \"" + file + "\" \"" + newName + "\""
				print cmd
				os.system(cmd)
			else:
				os.rename(file, newName)
				
			i += 1
		# move to a new dir	
		os.chdir(folderName)	

	# In magick mode we convert images from any format to jpegs in s new folder
	if mode == "magick"	:
		# Create folder for new jpgs
		if not os.path.exists(cwd + "\\" + folderName):
			os.makedirs(cwd + "\\" + folderName)
		# convert all to jpgs with magick
		os.system("magick mogrify -format jpg -path ./" + folderName + "  *")
		# move to newly created fodler and switch mode to rename
		os.chdir(folderName)	
		mode = "rename"
	
	print mode 	
		
	if mode == "rename":
		for file in files:
			filename = os.path.basename(file)
			ext = filename.rsplit(".",1)[1]
			name = filename.rsplit(".",1)[0]
			if name.isdigit():
				if ext == "jpeg" : ext = "jpg"
				newName =  os.path.dirname(file) +"\\" + name.zfill(4) + "." + ext		
				os.rename(file, newName)
				renamed += 1
			else:
				skipped += 1

		print "Ranamed " + str(renamed) + " files"
		print "Skipped " + str(skipped) + " files"

	if mode == "brackets":
		for file in files:
			filename = os.path.basename(file)
			ext = filename.rsplit(".",1)[1]
			name = filename.rsplit(".",1)[0]
			name = name.replace(")","").replace("(","").replace(" ","")
			print len("name")
			if name.isdigit():
				if ext == "jpeg" : ext = "jpg"
				newName =  os.path.dirname(file) +"\\" + name.zfill(4) + "." + ext		
				os.rename(file, newName)
				renamed += 1
			else:
				skipped += 1

		print "Ranamed " + str(renamed) + " files"
		print "Skipped " + str(skipped) + " files"	
		
		
	# Run lzFF that would convert jpgs to a h262.mp4	
	#print os.getcwd()
	os.system("lzff")
