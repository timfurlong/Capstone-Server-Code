# Echo server program
import socket
import datetime
import sys
import os
import time

sys.path.append('..')
from Logger import Logger

class sockServer:

	HOST = ''     # Symbolic name meaning all available interfaces
	PORT = 5000  # Arbitrary non-privileged port
	OUTPUT_DIR = 'outputFiles'
	OUTPUT_EXT = 'jpg'

	def __init__(self, debug=False):
		self.logger = Logger(logFile = 'sockServer', useStdOut=True)
		self.log    = self.logger.log
		self.debug  = debug

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((self.HOST, self.PORT))
		self.sock.listen(1)
		self.conn, self.addr = self.sock.accept()

		self.log( 'Connected by %s' % (self.addr,), debug=True)

	def recieveOne(self):
		lines = []
		first = True
		while 1:
			line = self.conn.recv(512)
			if first:
				tic = time.time()
				first = False
			lines.append( line )
			if not line:
				break
		self.saveImg(lines)
		print 'Total time taken = %f' % (time.time()-tic)
		self.conn.close()
		exit()

	def recieveMany(self, numImgs = 2):
		lines = []
		first = True
		while 1:
			line = self.conn.recv(512)
			if first:
				tic = time.time()
				first = False
			lines.append( line )
			if not line:
				break
		self.saveImg(lines)
		print 'Total time taken = %f' % (time.time()-tic)
		self.conn.close()
		exit()

	def saveImg(self, dataLines):
		now    = datetime.datetime.now()
		nowStr = now.strftime("%h%d_%Y %H_%M_%S")
		outputFilePath = os.path.join(self.OUTPUT_DIR, '%s.%s' %
																		(nowStr,self.OUTPUT_EXT))
		fp = open(outputFilePath, 'w')
		for line in dataLines:
			fp.write( line )
		fp.close()
		self.log('%s written successfully' % outputFilePath, debug=False)


if __name__ == '__main__':
	debug = False
	if 'debug' in sys.argv:
		debug = True
	print 'DEBUG MODE = %s' % debug
	server = sockServer()
	server.recieveOne()