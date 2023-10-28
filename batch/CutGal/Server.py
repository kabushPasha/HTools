# COMMANDLINE ARGS
# o - open html page
# r - random order
# m - multitab open

import asyncio 
import websockets
import glob, json, os, subprocess, sys ,random,shutil
import urllib

if "o" in sys.argv:
	html_file = os.path.dirname(__file__) + "\TestGrid.html" 
	os.system(html_file.replace("\\","/") )

src_folder = sys.argv[1].replace(os.sep,"/")

class CanoeAmbientServer():
	def __init__(self):	
		print("Starting Canoe Ambient Server")		
		self.startServer()

	async def serve(self,websocket, path):
		while True:
			msg = await websocket.recv()
			msg = json.loads(msg)
			print(msg)
			
			if msg[0] == 'GET_Files':
				files = glob.glob( src_folder + "/*.json" )	
				all_items = []
				for file in files:					
					json_data = json.load(open(file))
					# change abs paths to relative
					json_data[0] = src_folder +"/" +os.path.basename(json_data[0])
					json_data[1] = src_folder +"/" +os.path.basename(json_data[1])
					all_items.append(json_data)						
					
				await websocket.send(json.dumps(all_items))
			if msg[0] == "save":
				print("save", msg[1])
				#out_file = '"{os.path.splitext(msg[1][0])[0]}_{str(msg[1][3])}.mkv"'
				out_dir = os.path.dirname(msg[1][0]) + "/Cuts/"
				if not os.path.isdir(out_dir) :  os.mkdir(out_dir)
				out_file = out_dir + os.path.splitext(os.path.basename(msg[1][0]))[0] + f"_{str(msg[1][3])}.mkv"
				
				#subprocess.run(["ffmpeg","-ss",msg[1][1],"-to",msg[1][2],"-i",msg[1][0],"-c","copy",os.path.splitext(msg[1][0]) + "_" + str(msg[1][3]) + ".mkv"], shell=True)
				cmd = f'ffmpeg -ss {msg[1][1]} -to {msg[1][2]} -i "{msg[1][0]}" -c copy "{out_file}"'
				print(cmd)
				subprocess.Popen(cmd)
			if msg[0] == "move":
				print("move", msg[1])				
				out_dir = os.path.dirname(msg[1]) + "/Done/"
				if not os.path.isdir(out_dir) :  os.mkdir(out_dir)
				
				files = glob.glob( os.path.splitext(msg[1])[0] + "*" )	
				for file in files:				
					shutil.move( file,out_dir );
				

	def startServer(self):
		start_server = websockets.serve(self.serve, "localhost", 8000)
		asyncio.get_event_loop().run_until_complete(start_server)
		asyncio.get_event_loop().run_forever()


CanoeAmbientServer()




# ffmpeg -skip_frame nokey -i KornBlitz.mp4 -vsync 0 -frame_pts true -r 1000 out%d.png