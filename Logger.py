import os

class Logger:
	logFile     = None
	logDir      = 'logs'
	# SERVER_ROOT  = os.path.abspath( 'Capstone' )
	SERVER_ROOT = os.getcwd()

	def __init__(self, logFile=None, useStdOut=True):
		self.useStdOut   = useStdOut
		if logFile:
			if '.' in logFile and '.log' not in logFile:
				print 'logFile=%s must be specified without an extension or with the .log extension' % logFile
				raise
			if '.log' not in logFile:
				self.logFile     = '%s.log' % logFile
			else:
				self.logFile = logFile
			if not os.path.isdir( self.logDir ):
				os.mkdir( self.logDir )
			self.logPath = os.path.join(self.SERVER_ROOT, self.logDir, self.logFile)

	def log(self, msg, debug=False):
		if debug:
			level = 'DEBUG'
		else:
			level = 'INFO'
		logMsg = '%s -- %s\n' % (level, msg)

		if self.useStdOut:
			print logMsg
		if self.logFile:
			self.appendLogFile( logMsg )


	def appendLogFile(self, msg):
		try:
			f = open(self.logPath, 'a')
		except IOError:
			f = open(self.logPath, 'w+')
		f.write(msg)
		f.close()

if __name__ == '__main__':
	l = Logger(logFile='scratch.log')
	l.log('Testing', 'debug')