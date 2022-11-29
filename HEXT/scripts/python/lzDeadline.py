import socket
import os
import subprocess
import hou

def submitRS2Deadline(n, one_task_per_gpu = True):
	hostname = socket.gethostname()
	# Frame Range
	[frameStart,frameEnd] = [int(n.parm("f1").eval()),int(n.parm("f2").eval())]

	render_dir = os.path.dirname(n.parm("RS_outputFileNamePrefix").eval())
	out_dir = os.path.dirname(n.parm("RS_archive_file").eval())
	out_path = out_dir + "/0001.rs"

	# PLUGIN INFO FILE
	#gpus_per_task = 1
	gpus_per_task = 1 if one_task_per_gpu else 0
	output_dir = render_dir.replace('/','\\')
	scene_file = out_path.replace('/','\\').replace("####","0001")

	# JOB INFO FILE
	#concurrent_tasks = 4
	concurrent_tasks = 4 if one_task_per_gpu else 1
	frames = str(frameStart) + "-" + str(frameEnd)
	#task_name = hou.hipFile.basename()
	task_name = n.parm("deadline_jobname").eval()
	start_time = "04/09/2019 16:43"
	priority = n.parm("deadline_priority").eval()

	# FILL IN
	plugin_info = """GPUsPerTask={}
	ImageOutputDirectory=
	RenderOptionsFile=
	SceneFile={}
	SelectGPUDevices=
	TextureCacheBudget=0
	Version=1
	""".format(gpus_per_task , scene_file)

	job_info = """Blacklist=pavel,renderfarm2,server-canoe
	ConcurrentTasks={}
	Department={}
	EventOptIns=
	Frames={}
	Group=render
	LimitTasksToNumberOfCpus=False
	MachineName={}
	Name={}
	OutputDirectory0={}
	OverrideTaskExtraInfoNames=False
	Plugin=Redshift
	Priority={}
	Region=
	ScheduledStartDateTime={}
	UserName={}
	""".format(concurrent_tasks,hostname,frames,hostname,task_name,output_dir,priority,start_time,hostname)

	deadline_files_dir = os.path.dirname(out_dir)
	if not os.path.isdir(deadline_files_dir):
		os.makedirs(deadline_files_dir)

	# Write Files
	plugin_info_file = deadline_files_dir + "/plugin_info.txt"
	with open(plugin_info_file, "w") as text_file:
			text_file.write(plugin_info) 
			
	job_info_file = deadline_files_dir + "/job_info.txt"
	with open(job_info_file, "w") as text_file:
			text_file.write(job_info)
		   
	# Create Task with deadline
	deadline = "C:/Program Files/Thinkbox/Deadline10/bin/deadlinecommand.exe"
	p = subprocess.Popen([deadline,job_info_file,plugin_info_file],stdout=subprocess.PIPE)
	(output, err) = p.communicate()
	p_status = p.wait()
	output = output.decode('ascii')
	print(output)
	job_id = output.split("JobID=")[-1].split("\n")[0]
	return job_id