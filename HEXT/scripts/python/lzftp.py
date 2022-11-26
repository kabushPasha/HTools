import os,ftplib

def ftp_login(login_str = ""):
	# Needs Environment variable in the form of 
	# FTP_LOGIN = username:password@ftpserver
	login = login_str.replace(":","@").split("@")
	print("Logging in to:",login[2])
	return ftplib.FTP(login[2],login[0],login[1]) 

def ftp_downloadFile(login_str,local_file,ftp_file):
	ftp = ftp_login(login_str)
	[ftp_dir,ftp_filename] = os.path.split(ftp_file)
	print("Downloading file: ", ftp_filename)
	print("From: ", ftp_dir)	
	print("To: ", local_file)	
	ftp.cwd(ftp_dir)
	if ftp_filename in ftp.nlst():
		os.makedirs(os.path.dirname(local_file), exist_ok=True)
		ftp.retrbinary("RETR " + ftp_filename, open(local_file, 'wb').write)
		print("Downloaded")
	else:
		print("ERROR:File not on ftp")
	ftp.quit()
	
