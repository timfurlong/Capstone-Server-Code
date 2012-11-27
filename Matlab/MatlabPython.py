from subprocess import call


INPUT_DIR   = '/Users/cole_d/MATLAB/Capstone/SIFT/upload'
OUTPUT_DIR  = '/Users/cole_d/MATLAB/Capstone/SIFT/output/thisisthetest.jpg'
WORKING_DIR = '/Users/cole_d/MATLAB/Capstone/SIFT'

def call_mosaic():
	shellCmds = ['matlab',
				'-nojvm',
				'-nodesktop',
				'-nodisplay',
				'-r',
				'cd %s; display_mosaic(\'%s\',\'%s\',0);exit;'
				% (WORKING_DIR, INPUT_DIR, OUTPUT_DIR)]
	call(shellCmds)
