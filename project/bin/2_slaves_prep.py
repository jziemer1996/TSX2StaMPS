### Python script to use SNAP as InSAR processor for TSX processing compatible with StaMPS PSI processing
# Author: Jonas Ziemer, adapted from Jose Manuel Delgado Blasco (snap2stamps package)
# Date: 10/11/2022
# Version: 1.0

# Step 1: unzip downloaded TSX scenes (.tar; .tar.gz)
# Step 2: preparing slaves in folder structure
# Step 3: subset TSX scenes 
# Step 4: Coregistration 
# Step 5: Interferogram generation
# Step 6: StaMPS export


import os
import shutil
import sys
import glob
import subprocess
import shlex
import time
inputfile = sys.argv[1]

bar_message='\n#####################################################################\n'

# Getting configuration variables from inputfile
try:
        in_file = open(inputfile, 'r')
        for line in in_file.readlines():
                if "PROJECTFOLDER" in line:
                        PROJECT = line.split('=')[1].strip()
                        print PROJECT
finally:
        in_file.close()

##############################################################################
######################## Slaves sortering in folders #########################
##############################################################################
# Folders involved in this processing step
logfolder=PROJECT+'/logs'
slavesfolder=PROJECT+'/slaves'

if not os.path.exists(logfolder):
                os.makedirs(logfolder)

errorlog=logfolder+'/slave_proc_stderr.log'
outlog=logfolder+'/slave_proc_stdout.log'
out_file = open(outlog, 'a')
err_file = open(errorlog, 'a')

timeStarted_global = time.time()
# Iterate trough all files in the slavesfolder
for filename in os.listdir(slavesfolder):
    if filename.startswith("TDX1_SAR__SSC______SM_S_SRA") or filename.startswith("TSX1_SAR__SSC______SM_S_SRA"): 
       print(os.path.join(slavesfolder, filename))
       # Create name of the output slave folder
       head, tail = os.path.split(os.path.join(slavesfolder, filename))
       print tail[28:36]
       subdirectory=slavesfolder + '/' + tail[28:36]
       if not os.path.exists(subdirectory):
		os.makedirs(subdirectory)
       # Create subdirectories
       source=os.path.join(slavesfolder, filename)
       destination=os.path.join(subdirectory, tail)
       print 'Moving '+source+' to '+ destination
       shutil.move(source,destination)
    else:
        continue
timeDelta_global = time.time() - timeStarted_global
print 'Finished preparation in ' + str(timeDelta_global) + ' seconds.\n'