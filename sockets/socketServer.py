# Echo server program
import socket
import datetime
import sys
import os
import shutil
import time

sys.path.append('.')
sys.path.append('./Matlab')
from Logger import Logger
from config import config
from MatlabPython import call_mosaic

class sockServer:

	HOST       = ''     # Symbolic name meaning all available interfaces
	# HOST     = '172.23.198.147'
	PORT       = 5000  # Arbitrary non-privileged port
	BUFF_SIZE  = 512
	OUTPUT_DIR = 'outputFiles'
	OUTPUT_EXT = 'jpg'

	def __init__(self, debug=False):
		self.logger = Logger(logFile = 'sockServer', useStdOut=True)
		self.log    = self.logger.log
		self.debug  = debug
		if not os.path.isdir(self.OUTPUT_DIR):
		 	os.mkdir(self.OUTPUT_DIR)

	def runSocket(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.HOST, self.PORT))
		self.sock.listen(1)
		self.conn, self.addr = self.sock.accept()

		self.log( 'Connected by %s' % (self.addr,), debug=True)

	def recieveOne(self):
		self.runSocket()
		lines = []
		first = True
		while 1:
			line = self.conn.recv( self.BUFF_SIZE )
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

	def recieveMany(self):
		lines = []
		first = True
		numImgs = 0

		shutil.rmtree(self.OUTPUT_DIR)
		if not os.path.isdir(self.OUTPUT_DIR):
		 	os.mkdir(self.OUTPUT_DIR)

		while numImgs<config['num_sensors']:
			self.runSocket()
			lines = []
			while 1:
				line = self.conn.recv( self.BUFF_SIZE )
				if first:
					tic = time.time()
					first = False
				if not line:
					break
				lines.append(line)
			self.saveImg(lines)
			numImgs += 1
			print 'Total time taken = %f' % (time.time()-tic)
			first = True
			self.log('%d images received' % numImgs, debug=True)
			self.conn.close()
		self.log('Recived all images for this period', debug=True)

		call_mosaic()

	def reciveFileName(self):
	   filename = self.conn.recv( self.BUFF_SIZE )
	   return filename

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

	def recieveArray(self):
		self.runSocket()
		line = self.conn.recv( self.BUFF_SIZE )
		self.log(line, debug=True)
		self.conn.close()
		exit()

	def keepRecievingStrs(self):
		lines = []
		while 1:
			self.runSocket()
			try:
				while 1:
					line = self.conn.recv( self.BUFF_SIZE )
					if not line:
						break
					lines.append(line)
			except socket.error, e:
				print e
			if len(lines) == 1:
				self.log(lines[0], debug=True)
			else:
				self.log('%d lines received' % len(lines), debug=True)
				# print lines[:50]
			self.conn.close()
			self.runSocket()

if __name__ == '__main__':
	debug = False
	if 'debug' in sys.argv:
		debug = True
	print 'DEBUG MODE = %s' % debug
	server = sockServer(debug=debug)
	# server.keepRecievingStrs()
	# server.recieveArray()
	# server.recieveOne()
	server.recieveMany()

