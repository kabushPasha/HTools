# COMMANDLINE ARGS
# o - open html page
# r - random order
# m - multitab open

import asyncio 
import websockets
import glob, json, os, subprocess, sys ,random,time,shutil
import urllib



#if "o" in sys.argv:
if True:
	html_file = os.path.dirname(__file__) + "\client.html" 
	
	if "k" in sys.argv:
		html_file = os.path.dirname(__file__) + "\clientKoh.html" 
		
	if "a" in sys.argv:
		html_file = os.path.dirname(__file__) + "\clientA.html" 
	
	page = "file:///" + html_file.replace("\\","/")
	open_command = r'start chrome --profile-directory="Default" '
	open_command += r'--app=' + page	
	os.system(open_command)
	
	
src_folder = os.path.normpath(sys.argv[1])
print("src folder",src_folder)

files = sorted(glob.glob( src_folder + "/*.jpg" ) + glob.glob( src_folder + "/*.jpeg" ),reverse=True)
print("olf_dilfes",files)

# NEW GLOB SUB folders
if "s" in sys.argv or files==[]:
	my_exts = ['*.jpg', 'jpeg', '*.png']
	files = [glob.glob(src_folder + '/**/'+ x, recursive=True) for x in my_exts] 
	files = sum(files, [])
	
	if not "k" in sys.argv:
		print("pres_sort",files)
		files = [file for file in files if '\\picked\\' not in file]
		files = [file for file in files if '\\copy\\' not in file]	
		print("post_sort",files)
	
	files = sorted(files,reverse=True)
	
	

if "r" in sys.argv: random.shuffle(files)

class CanoeAmbientServer():
	def __init__(self):
		print("Starting Canoe Ambient Server")
		self.startServer()

	async def serve(self,websocket, path):
		while True:
			msg = await websocket.recv()
			#print(msg,websocket,path)
			msg = json.loads(msg)
			
			if msg[0] == 'GET_Files':
				await websocket.send(json.dumps(files))
			if msg[0] == "delete":
				print("delete", msg[1])
				current_file = urllib.parse.unquote(msg[1].replace("file:///",""))				
				current_file = os.path.normpath(current_file)
				time.sleep(0.1)			
					
				if current_file.startswith(src_folder):
					os.remove( current_file )
					print("deleted :", msg[1])
			if msg[0] == "save":
				print("save", msg[1])
				src_path = urllib.parse.unquote(msg[1].replace("file:///",""))
				src_path = os.path.normpath(src_path)
				#dest_path = os.path.dirname(src_path) + "/picked/" + os.path.basename(src_path)				
				#dest_path = src_folder + "/picked/" + os.path.basename(src_path)
				dest_name = src_path.replace(src_folder + os.path.sep,"").replace(os.path.sep,"_")
				dest_path = src_folder + "/picked/"  + dest_name
				if not os.path.isdir(os.path.dirname(dest_path)): os.mkdir(os.path.dirname(dest_path))
				time.sleep(0.1)
				
				# move if the file is in the same folder
				#if os.path.dirname(src_path) == src_folder:	
				if src_path.startswith(src_folder):				
					os.rename(src_path, dest_path)
					
			if msg[0] == "copy":
				print("copy", msg);
				
				sub_folder = "/copy/"
				if len(msg) > 2: 
					if msg[2]:
						sub_folder = "/" + msg[2]	+ "/"
				src_path = urllib.parse.unquote(msg[1].replace("file:///",""))
				src_path = os.path.normpath(src_path)
				#dest_path = os.path.dirname(src_path) + sub_folder + os.path.basename(src_path)
				#dest_path = src_folder + sub_folder + os.path.basename(src_path)
				dest_name = src_path.replace(src_folder + os.path.sep,"").replace(os.path.sep,"_")
				dest_path = src_folder + sub_folder + dest_name
				print(dest_path)
				if not os.path.isdir(os.path.dirname(dest_path)): os.mkdir(os.path.dirname(dest_path))
				time.sleep(0.1)
				
				# move if the file is in the same folder
				#if os.path.dirname(src_path) == src_folder:	
				if src_path.startswith(src_folder):					
					shutil.copyfile(src_path, dest_path)
				
				
			if msg[0] == 'CLOSE':
				asyncio.get_event_loop().stop()

	def startServer(self):
		start_server = websockets.serve(self.serve, "localhost", 8000)
		asyncio.get_event_loop().run_until_complete(start_server)
		asyncio.get_event_loop().run_forever()


CanoeAmbientServer()

