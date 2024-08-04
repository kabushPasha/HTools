from imp import reload

'''
import lzutil
reload(lzutil)

import lzDeadline
reload(lzDeadline)

import lzRS_Shelf
reload(lzRS_Shelf)

import lzModelling
reload(lzModelling)

import lzocl
reload(lzocl)

import lzftp
reload(lzftp)

def update():
	reload(lzutil)
	reload(lzDeadline)
	reload(lzRS_Shelf)
	reload(lzModelling)
	reload(lzocl)
	reload(lzftp)
	print("updated")
'''

def update():
	import glob,os,imp	
	loaded_modules = []
	script_path = os.getenv("HEXT") +"/scripts/python/*.py"
	for module in glob.glob(script_path):

		mod_name = os.path.basename(module)
		mod_name = os.path.splitext(mod_name)[0]

		if mod_name == "lz": continue
		if mod_name == "FbxCommon": continue
		
		fp, pathname, description = imp.find_module(mod_name)
		new_module = imp.load_module(mod_name,fp, pathname, description)
		
		loaded_modules.append(new_module)
		
update()