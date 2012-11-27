import subprocess
from subprocess import call

shellCmds = ['matlab',
			'-nojvm',
			'-nodesktop',
			'-nodisplay',
			'-r',
			'cd /Users/cole_d/MATLAB/Capstone/SIFT; display_mosaic(\'/Users/cole_d/MATLAB/Capstone/SIFT/upload\',\'/Users/cole_d/MATLAB/Capstone/SIFT/output/thisisthetest.jpg\',0);exit;']
call(shellCmds)
