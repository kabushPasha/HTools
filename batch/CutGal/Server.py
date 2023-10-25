# COMMANDLINE ARGS
# o - open html page
# r - random order
# m - multitab open

import asyncio 
import websockets
import glob, json, os, subprocess, sys ,random
import urllib

if "o" in sys.argv:
	html_file = os.path.dirname(__file__) + "\TestGrid.html" 
	os.system(html_file.replace("\\","/") )

src_folder = sys.argv[1]

class CanoeAmbientServer():
	def __init__(self):	
		print("Starting Canoe Ambient Server")		
		self.startServer()

	async def serve(self,websocket, path):
		while True:
			msg = await websocket.recv()
			msg = json.loads(msg)
			
			if msg[0] == 'GET_Files':
				files = glob.glob( src_folder + "/*.json" )	
				all_items = []
				for file in files:					
					all_items.append(json.load(open(file)))				
				await websocket.send(json.dumps(all_items))
			if msg[0] == "save":
				print("save", msg[1])
				
				#subprocess.run(["ffmpeg","-ss",msg[1][1],"-to",msg[1][2],"-i",msg[1][0],"-c","copy",os.path.splitext(msg[1][0]) + "_" + str(msg[1][3]) + ".mkv"], shell=True)
				cmd = f'ffmpeg -ss {msg[1][1]} -to {msg[1][2]} -i "{msg[1][0]}" -c copy "{os.path.splitext(msg[1][0])[0]}_{str(msg[1][3])}.mkv"'
				print(cmd)
				subprocess.Popen(cmd)


	def startServer(self):
		start_server = websockets.serve(self.serve, "localhost", 8000)
		asyncio.get_event_loop().run_until_complete(start_server)
		asyncio.get_event_loop().run_forever()


CanoeAmbientServer()




# ffmpeg -skip_frame nokey -i KornBlitz.mp4 -vsync 0 -frame_pts true -r 1000 out%d.png