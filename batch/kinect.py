from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

# init server
import socket
print("Starting Kinect Server")
HOST = '127.0.0.1';PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print("waiting for connections")
s.listen()
conn, addr = s.accept()
print("Conencted")

kinect  = None

def start():
	print ("starting kinect")
	kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Body)
	print (kinect)
def end():
	print ("ending kinect")
	kinect.close()
def capture():
	print ("captureing frame")
	print (kinect.has_new_body_frame())
	'''
	if self._kinect.has_new_body_frame():            
            self._bodies = self._kinect.get_last_body_frame()
                        
            if self._bodies is not None: 
                for i in range(0, self._kinect.max_body_count):
                    body = self._bodies.bodies[i]
                    n.parm("b" + str(i)).set(body.is_tracked)
                    if not body.is_tracked: 
                        continue 
                    
                    #hou.playbar.stop()    
                        
                    joints = body.joints 
                    # convert joint coordinates to color space 
                    #joint_points = self._kinect.body_joints_to_color_space(joints)
                    #print joints
                    #self.draw_body(joints, joint_points, SKELETON_COLORS[i])
                    for i in range(0,25):
                        x = joints[i].Position.x
                        y = joints[i].Position.y
                        z = joints[i].Position.z
                        
                        n.parm("usept" + str(i)).set(1)
                        n.parm("pt" + str(i) + "x").set(x)
                        n.parm("pt" + str(i) + "y").set(y)
                        n.parm("pt" + str(i) + "z").set(z)
                        
                        print ("updatet Joints")
                        n.node("add1").cook()
                        n.cook()
	'''




while True:
	data = conn.recv(1024)
	if len(data) > 0:
		print(data)
		#conn.sendall(b"Answer")
		
		if data == b"start":
			start()
		if data == b"end":
			end()
		if data == b"capture":
			capture()