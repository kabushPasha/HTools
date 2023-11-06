# COMMANDLINE ARGS
# o - open html page
# r - random order
# m - multitab open

import asyncio 
import websockets
import glob, json, os, subprocess, sys ,random,time
import urllib

if "o" in sys.argv:
	html_file = os.path.dirname(__file__) + "\client.html" 
	#os.system(html_file.replace("\\","/") )
	
	page = "file:///" + html_file.replace("\\","/")
	open_command = r'start chrome --profile-directory="Default" '
	open_command += r'--app=' + page	
	os.system(open_command)
	
if "m" in sys.argv:
	html_file = os.path.dirname(__file__) + "\client_Multi.html" 
	os.system(html_file.replace("\\","/") )

src_folder = sys.argv[1]

files = sorted(glob.glob( src_folder + "/*.mp4" ) + glob.glob( src_folder + "/*.mkv" ),reverse=True)
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
				current_file = msg[1].replace("file:///","")
				os.remove( urllib.parse.unquote(current_file) )
			if msg[0] == "save":
				print("save", msg[1])
				src_path = urllib.parse.unquote(msg[1].replace("file:///",""))
				dest_path = os.path.dirname(src_path) + "/picked/" + os.path.basename(src_path)
				if not os.path.isdir(os.path.dirname(dest_path)): os.mkdir(os.path.dirname(dest_path))
				time.sleep(0.1)
				os.rename(src_path, dest_path)

	def startServer(self):
		start_server = websockets.serve(self.serve, "localhost", 8000)
		asyncio.get_event_loop().run_until_complete(start_server)
		asyncio.get_event_loop().run_forever()


CanoeAmbientServer()

