from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

# init server
import socket,pickle
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
	return kinect
def end():
	print ("ending kinect")
	kinect.close()
	print (kinect)
def capture():
	print ("captureing frame")
	print (kinect.has_new_body_frame())
	
	data = []
	
	if kinect.has_new_body_frame():
		bodies = kinect.get_last_body_frame()

		if bodies is not None: 			
			for i in range(0, kinect.max_body_count):
				body = bodies.bodies[i]
				#print ("body",i, "is itracked " , body.is_tracked)
				if not body.is_tracked: 
					continue 
				
				#body.engaged
				#b.hand_left_confidence
				#b.hand_left_state
				
				data = []
				joints = body.joints
				o = body.joint_orientations
				for i in range(0,25):
					x = joints[i].Position.x
					y = joints[i].Position.y
					z = joints[i].Position.z
					#trackingState = joints[i].TrackingState
					#orientations
					ox = o[i].Orientation.x
					oy = o[i].Orientation.y
					oz = o[i].Orientation.z
					ow = o[i].Orientation.w
					
					data += [[x,y,z,ox,oy,oz,ow]]
					#data += [[x,y,z]]
	#print(data)
	data_string = pickle.dumps(data,2)
	conn.sendall(data_string)




while True:
	data = conn.recv(1024*4)
	if len(data) > 0:
		#print(data)
		#conn.sendall(b"Answer")
		
		if data == b"start":
			kinect = start()
		if data == b"end":
			end()
		if data == b"capture":
			capture()