
import asyncio 
import websockets
import glob, json, os, subprocess, sys ,random,shutil
import urllib


src_folder = sys.argv[1].replace(os.sep,"/")

# Open Webpage
def open_webpage():
	html_file = os.path.dirname(__file__) + r"\TestGrid.html" 	
	page = "file:///" + html_file.replace("\\","/")
	open_command = r'start chrome --profile-directory="Default" '
	open_command += r'--app=' + page	
	os.system(open_command)


def get_src_files():
	src_vods = glob.glob( src_folder + "/*.mp4" )
	return src_vods

src_vods = get_src_files()


class CanoeAmbientServer():
	def __init__(self):	
		print("Starting GIF GAL Server")	
		print(src_vods)
		self.stop_event = asyncio.Event()
		self.startServer()		
		

	async def serve(self,websocket, path=None):
		try:
			while True:
				msg = await websocket.recv()			
				msg = json.loads(msg)
				print(msg)
				
				
				if msg[0] == 'GET_Files':				
					await websocket.send(json.dumps(src_vods))
					

				if msg[0] == "move":
					file_to_move = os.path.abspath(msg[1][0])
					src_abs = os.path.abspath(src_folder)
					if os.path.normcase(file_to_move).startswith(os.path.normcase(src_abs)) and os.path.isfile(file_to_move):
						out_dir = os.path.join(os.path.dirname(file_to_move), "Done")
						os.makedirs(out_dir, exist_ok=True)
						shutil.move(file_to_move, out_dir)
						print(f"Moved file: {file_to_move} to {out_dir}")
					else:
						print(f"Move blocked or file missing: {file_to_move}")

				if msg[0] == "delete":
					file_to_delete = os.path.abspath(msg[1][0])
					src_abs = os.path.abspath(src_folder)
					if os.path.normcase(file_to_delete).startswith(os.path.normcase(src_abs)) and os.path.isfile(file_to_delete):
						os.remove(file_to_delete)
						print(f"Deleted file: {file_to_delete}")
					else:
						print(f"Delete blocked or file missing: {file_to_delete}")
		except websockets.exceptions.ConnectionClosedOK:
			print("Client closed the connection (code 1001). Shutting down server.")
			self.stop_event.set()

	def startServer(self):
		async def run_server():
			server = await websockets.serve(self.serve, "localhost", 8000)
			print("Server started at ws://localhost:8000")
			await self.stop_event.wait() 
		asyncio.run(run_server())



open_webpage()
try:
	CanoeAmbientServer()
except Exception as e:
    import traceback
    print("An error occurred:")
    traceback.print_exc()
    input("Press Enter to exit...")  # Wait for user input before closing


