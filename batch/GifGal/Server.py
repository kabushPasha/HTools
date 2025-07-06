
import asyncio 
import websockets
import glob, json, os, subprocess, sys ,random,shutil
import urllib

try:
	src_folder = sys.argv[1].replace(os.sep,"/")

	# Open Webpage
	def open_webpage():
		html_file = os.path.dirname(__file__) + r"\TestGrid.html" 	
		page = "file:///" + html_file.replace("\\","/")
		open_command = r'start chrome --profile-directory="Default" '
		open_command += r'--app=' + page	
		os.system(open_command)

	def get_keyframe_timestamps(video_file):
		# Run ffprobe to extract keyframe timestamps
		cmd = [
			"ffprobe",
			"-select_streams", "v",
			"-skip_frame", "nokey",
			"-show_frames",
			"-print_format", "csv",
			video_file,
		]
		result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		lines = result.stdout.splitlines()
	
		timestamps = []
		for line in lines:
			#print(line)
			parts = line.split(',')
			if len(parts) > 4:
				try:
					ts = parts[5]
					timestamps.append(ts)
				except ValueError:
					pass
		return ",".join(timestamps)

	def get_kf_path(video_path):
		temp_dir = os.path.join(os.path.dirname(video_path), "temp")
		os.makedirs(temp_dir, exist_ok=True)
		return os.path.join(temp_dir, os.path.basename(video_path) + ".kf.txt")

	def create_kf_txt(video_path):
		kf_string = get_keyframe_timestamps(video_path)
		kf_path = get_kf_path(video_path)
		with open(kf_path, "w") as file:
			file.write(kf_string)
		return kf_string

	def get_video_kf_string(video_path):
		if os.path.isfile(get_kf_path(video_path)):
			with open(get_kf_path(video_path), "r") as file:
				kf_string = file.read()
				return kf_string 
		else:
			kf_string = create_kf_txt(video_path)
			return kf_string 

	def get_proxy_path(video_path):
		return os.path.dirname(video_path)+"/temp/" + os.path.basename(video_path) + ".proxy.mp4"

	def get_source_path_from_proxy(proxy_path):
		proxy_path = proxy_path.replace("\\", "/")  # Normalize slashes
		dir_path = os.path.dirname(os.path.dirname(proxy_path))  # Go one level up from /temp
		file_name = os.path.basename(proxy_path).replace(".proxy.mp4", "")
		return os.path.join(dir_path, file_name)

	def create_proxy(video_path):
		output_file = get_proxy_path(video_path)
		os.makedirs(os.path.dirname(output_file), exist_ok=True)
		
		command = [
			"ffmpeg",
			"-i", video_path,
			"-vf", "scale=w=1280:h=720:force_original_aspect_ratio=decrease,scale=trunc(iw/2)*2:trunc(ih/2)*2",
			output_file
		]

		try:
			subprocess.run(command, check=True)
			print("Video resized successfully.")
		except subprocess.CalledProcessError as e:
			print("Error occurred:", e)

	def get_src_files():
		files = glob.glob( src_folder + "/*.mp4" ) + glob.glob( src_folder + "/*.mkv" )
		src_vods = dict()
		for file in files:				
			kf_string = get_video_kf_string(file)
			proxy_path = get_proxy_path(file)
			if not os.path.isfile(proxy_path):
				create_proxy(file)				
			src_vods[proxy_path] = {"kf":kf_string}
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
				msg = await websocket.recv()			
				msg = json.loads(msg)
				print(msg)				
				
				if msg["type"] == 'GET_Files':				
					await websocket.send(json.dumps(src_vods))


				elif msg["type"] == "SAVE_KeyframeSegment":
					video_path = msg.get("path")
					video_path = get_source_path_from_proxy(video_path)
					
					start_time = float(msg.get("start", 0)) + 1
					end_time = float(msg.get("end", 0))
					segment_index = msg.get("segment")
					if video_path and end_time > start_time:
						output_folder = os.path.join(os.path.dirname(video_path), "segments")
						os.makedirs(output_folder, exist_ok=True)

						# Create output filename with timestamp or random suffix
						base_name = os.path.basename(video_path)
						name, ext = os.path.splitext(base_name)
						output_file = os.path.join(output_folder, f"{name}_segment_{segment_index}_{ext}")

						# Build ffmpeg command to extract segment losslessly
						# Using -c copy for stream copy (no re-encoding)
						command = [
							"ffmpeg",
							"-ss", str(start_time),
							"-to", str(end_time),
							"-i", video_path,
							"-c", "copy",
							output_file,
							"-y"  # overwrite if exists
						]

						print(f"Saving segment: {command}")

						try:
							subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
							print(f"Segment saved: {output_file}")
							await websocket.send(json.dumps({"type": "SAVE_Success", "path": output_file}))
						except subprocess.CalledProcessError as e:
							print(f"Error saving segment: {e}")
							await websocket.send(json.dumps({"type": "SAVE_Error", "error": str(e)}))
			except websockets.exceptions.ConnectionClosedOK:
				print("Client closed the connection (code 1001). Shutting down server.")
				self.stop_event.set()

		def startServer(self):
			async def run_server():
				server = await websockets.serve(self.serve, "localhost", 8000)
				print("Server started at ws://localhost:8000")
				await self.stop_event.wait() 
			asyncio.run(run_server())



	#open_webpage()


	CanoeAmbientServer()
	
except Exception as e:
	import traceback
	print("An error occurred:")
	traceback.print_exc()
	input("Press Enter to exit...")  # Wait for user input before closing







