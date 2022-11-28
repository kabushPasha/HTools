import os,ftplib,time,datetime

def ftp_normpath(path):
	return os.path.normpath(path).replace(os.sep,"/")

def ftp_login(login_str = ""):
	# Needs Environment variable in the form of 
	# FTP_LOGIN = username:password@ftpserver
	login = login_str.replace(":","@").split("@")
	print("Logging in to:",login[2])
	return ftplib.FTP(login[2],login[0],login[1]) 

def ftp_canUploadFile(ftp,local_file,ftp_filename):
	if ftp_filename in ftp.nlst():
		# Check timestamp
		remote_timestamp = ftp.voidcmd(f"MDTM {ftp_filename}")[4:].strip()
		remote_timestamp = time.mktime(time.strptime(remote_timestamp, '%Y%m%d%H%M%S'))
		local_timestamp = time.mktime(time.gmtime(os.path.getmtime(local_file)))
		if (local_timestamp < remote_timestamp):
			print("Newer version on FTP")
			return False
	return True
	
def ftp_canDownloadFile(ftp,local_file,ftp_filename):
	if os.path.isfile(local_file):
		# Check timestamp
		remote_timestamp = ftp.voidcmd(f"MDTM {ftp_filename}")[4:].strip()
		remote_timestamp = time.mktime(time.strptime(remote_timestamp, '%Y%m%d%H%M%S'))
		local_timestamp = time.mktime(time.gmtime(os.path.getmtime(local_file)))
		if (local_timestamp >= remote_timestamp):
			print("Newer version on Disk")
			return False
	return True
	

def ftp_downloadFile(login_str,local_file,ftp_file):
	ftp = ftp_login(login_str)
	local_file = ftp_normpath(local_file)
	ftp_file = ftp_normpath(ftp_file)	
	[ftp_dir,ftp_filename] = os.path.split(ftp_file)
	print("Downloading file: ", ftp_filename)
	print("From: ", ftp_dir)	
	print("To: ", local_file)	
	ftp.cwd(ftp_dir)
	if ftp_filename in ftp.nlst():
		os.makedirs(os.path.dirname(local_file), exist_ok=True)
		
		# check Local file
		if not ftp_canDownloadFile(ftp,local_file,ftp_filename):
			ftp.quit()
			return
			
		# download file
		ftp.retrbinary("RETR " + ftp_filename, open(local_file, 'wb').write)
		
		# fix timestamp
		remote_timestamp = ftp.voidcmd(f"MDTM {ftp_filename}")[4:].strip()
		remote_timestamp = time.mktime(time.strptime(remote_timestamp, '%Y%m%d%H%M%S'))
		# fix utc offset
		remote_timestamp -= time.mktime(time.gmtime(remote_timestamp)) - remote_timestamp
		os.utime(local_file, (remote_timestamp, remote_timestamp))		
		print("Downloaded")
	else:
		print("ERROR:File not on ftp")
	ftp.quit()

def ftp_uploadFile(login_str,local_file,ftp_file):
	ftp = ftp_login(login_str)
	local_file = ftp_normpath(local_file)
	ftp_file = ftp_normpath(ftp_file)
	[ftp_dir,ftp_filename] = os.path.split(ftp_file)
	print("Uploading file: ", ftp_filename)
	print("From: ", local_file)		
	print("To: ", ftp_dir) 
	
	# cwd and create dir
	ftp_cwdAndCreateDir(ftp,ftp_dir)
	
	# Check if the file is on FTP
	if not ftp_canUploadFile(ftp,local_file,ftp_filename):
		ftp.quit()
		return
	
	ftp.storbinary("STOR " + ftp_filename, open(local_file,'rb'))
	print("Uploaded")
	ftp.quit()
	
def ftp_cwdAndCreateDir(ftp,ftp_dir):	
	# go to root
	ftp.cwd("/")
	# make path safe
	ftp_dir = os.path.normpath(ftp_dir).replace(os.sep,"/")
	for dr in ftp_dir.split("/"):
		if dr:
			if dr in ftp.nlst():
				ftp.cwd(dr)
			else:
				ftp.mkd(dr)
				ftp.cwd(dr)
				
def ftp_walkAndDownload(ftp,local_dir,ftp_dir,subpath = ""):
	start_dir = ftp.pwd()  
	ftp.cwd(ftp_dir)
	for item in ftp.mlsd():
		[filename,filetype,size] = [item[0],item[1]["type"],item[1]["size"]]
		if filetype == "dir":
			print(subpath + filename)
			ftp_walkAndDownload(ftp,local_dir,filename,subpath + filename + "/" )
		else:					   
			os.makedirs(os.path.join(local_dir,subpath), exist_ok=True)
			local_file = os.path.join(local_dir,subpath,filename)
			print("Downloading file: ",subpath + filename, "to: ",local_file) 
			ftp.retrbinary("RETR " + filename, open(local_file, 'wb').write)  
	ftp.cwd(start_dir)	

def ftp_downloadFolder(login_str,local_dir,ftp_dir):
	print("Downloading Folder: ")
	print("From: ", ftp_dir)	
	print("To: ", local_dir)
	local_dir = ftp_normpath(local_dir)
	ftp_dir = ftp_normpath(ftp_dir)
	with ftp_login(login_str) as ftp:
		ftp_walkAndDownload(ftp,local_dir,ftp_dir)
	print("DONE!")

def ftp_uploadFolder(login_str,local_dir,ftp_dir):
	print("Uploading Folder: ")
	print("From: ", local_dir)	
	print("To: ", ftp_dir)
	local_dir = ftp_normpath(local_dir)
	ftp_dir = ftp_normpath(ftp_dir)
	with ftp_login(login_str) as ftp:		
		for (dirpath, dirnames, filenames) in os.walk(local_dir):
			#print(dirpath, dirnames, filenames)  
			print(dirpath.replace(local_dir,""))
			ftp_cwdAndCreateDir(ftp,dirpath.replace(local_dir,ftp_dir))
			for filename in filenames:
				local_file = os.path.join( dirpath,filename)
				print("Uploading: ",local_file)	
				
				if not ftp_canUploadFile(ftp,local_file,filename):
					continue		
					
				ftp.storbinary("STOR " + filename, open(local_file,'rb'))
	print("DONE!")
