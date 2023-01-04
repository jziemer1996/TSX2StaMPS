### Python script to use SNAP as InSAR processor for TSX processing compatible with StaMPS PSI processing
# Author: Jonas Ziemer, adapted from Jose Manuel Delgado Blasco (snap2stamps package)
# Date: 01/01/2023
# Version: 1.1, Python 3.9

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
import tarfile
inputfile = sys.argv[1]

bar_message='\n#####################################################################\n'

# Getting configuration variables from inputfile
try:
        in_file = open(inputfile, 'r')
        for line in in_file.readlines():
                if "PROJECTFOLDER" in line:
                        PROJECT = line.split('=')[1].strip()
                        print(PROJECT)
finally:
        in_file.close()

##############################################################################
################### Unpack zipped files in the zipfolder ##################### 
##############################################################################
# Folders involved in this processing step
logfolder=PROJECT+'/logs'
zipfolder=PROJECT+'/zipfiles'
slavesfolder=PROJECT+'/slaves'

if not os.path.exists(logfolder):
                os.makedirs(logfolder)
if not os.path.exists(zipfolder):
                os.makedirs(zipfolder)
if not os.path.exists(slavesfolder):
                os.makedirs(slavesfolder)
                
errorlog=logfolder+'/unpack_proc_stderr.log'
outlog=logfolder+'/unpack_proc_stdout.log'
out_file = open(outlog, 'a')
err_file = open(errorlog, 'a')

timeStarted_global = time.time()
# Unpack .tar(.gz) files
try:
    for filename in os.listdir(zipfolder):
        os.chdir(zipfolder)
        filename = zipfolder + '/' + filename
        print(filename)
        if filename.endswith("tar.gz"):
            tar = tarfile.open(filename, "r:gz")
            if filename.endswith("tar"):
                tar = tarfile.open(filename, "r:")
        elif filename.endswith("tar"):
            tar = tarfile.open(filename, "r:")
        tar.extractall()
        tar.close()
except:
    raise Exception("The files have already been extracted!")

# Cut out the data folder only, to get the right naming of the files for later processing steps
for file in os.listdir(zipfolder):
    folder = os.path.join(zipfolder, file)
    if os.path.isdir(folder):
        for tsxmainfolder in glob.iglob(folder + '/*'):
            if tsxmainfolder.endswith('.L1B'):
                for tsxsubfolder in glob.iglob(tsxmainfolder + '/*'):
                    print(tsxsubfolder)
                    shutil.move(tsxsubfolder, slavesfolder)
timeDelta_global = time.time() - timeStarted_global
print('Finished unzipping in ' + str(timeDelta_global) + ' seconds.\n')