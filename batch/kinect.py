import socket

print("Starting Kinect Server")
HOST = '127.0.0.1';PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print("waiting for connections")
s.listen()
conn, addr = s.accept()
print("Conencted")


while True:
	data = conn.recv(1024)
	if len(data) > 0:
		print(data)
		conn.sendall(b"Answer")
