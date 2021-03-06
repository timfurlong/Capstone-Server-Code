# Echo client module
import socket
import sys

class sockClient:
	# The remote host    daring.cwi.nl
	# HOST = socket.gethostbyname(socket.gethostname())
	HOST = "172.23.197.239"
	PORT = 5000              # The same port as used by the server
	sock = None

	def __init__(self):
		for res in socket.getaddrinfo(self.HOST, self.PORT,
									socket.AF_UNSPEC, socket.SOCK_STREAM):
			af, socktype, proto, canonname, sa = res
			try:
				self.sock = socket.socket(af, socktype, proto)
			except socket.error, msg:
				print 'socket error with msg: %s' % msg
				self.sock = None
				continue
			try:
				self.sock.connect(sa)
			except socket.error, msg:
				print 'socket error with msg: %s' % msg
				self.sock.close()
				self.sock = None
				continue
			break

		if self.sock is None:
			print 'could not open socket'
			sys.exit(1)

	def sendImgStr(self, imgName = None):
		img = open(imgName, 'r')
		while 1:
			line = img.readline(512)
			if not line:
				break
			self.sock.send( line )
		img.close()
		self.sock.close()

	def sendNumArray(self, array):
		done = False
		while not done:
			line = str(array)
			if not line:
				break
			self.sock.send( line )
			done = True
		self.sock.close()

if __name__ == '__main__':
	imgName = 'sky.jpg'
	client = sockClient()
	a = [1,2,3]
	# client.sendImgStr(imgName=imgName)
	client.sendNumArray( a )
