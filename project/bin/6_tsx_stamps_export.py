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
from pathlib import Path
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
                        print(PROJECT)
                if "MASTER" in line:
                        MASTER = line.split('=')[1].strip()
                        print(MASTER)
                if "GRAPHSFOLDER" in line:
                        GRAPH = line.split('=')[1].strip()
                        print(GRAPH)
                if "GPTBIN_PATH" in line:
                        GPT = line.split('=')[1].strip()
                        print(GPT)
                if "CACHE" in line:
                        CACHE = line.split('=')[1].strip()
                if "CPU" in line:
                        CPU = line.split('=')[1].strip()
finally:
        in_file.close()

###################################################################################
############################# StaMPS PSI export ###################################
###################################################################################
# Folders involved in this processing step
coregfolder=PROJECT+'/coreg'
ifgfolder=PROJECT+'/ifg'
head, tail = os.path.split(MASTER)
outputexportfolder=PROJECT+'/INSAR_'+tail[0:8]
logfolder=PROJECT+'/logs'

if not os.path.exists(outputexportfolder):
                os.makedirs(outputexportfolder)
if not os.path.exists(logfolder):
                os.makedirs(logfolder)

outlog=logfolder+'/export_proc_stdout.log'

# Original Snap graph and replaced Snap graph for subsettting
graphxml=GRAPH+'/6_TSX_Export.xml'
print(graphxml)
graph2run=GRAPH+'/export2run.xml'

out_file = open(outlog, 'a')
err_file=out_file

# Processing layout
print(bar_message)
out_file.write(bar_message)
message='## StaMPS PSI export started:\n'
print(message)
out_file.write(message)
print(bar_message)
out_file.write(bar_message)
k=0
timeStarted_global = time.time()
# Iterate trough all files in the coreg- and ifg folder
for dimfile in glob.iglob(coregfolder + '/*.dim'):
    head, tail = os.path.split(os.path.join(coregfolder, dimfile))
    k=k+1
    message='['+str(k)+'] Exporting pair: master-slave pair '+tail+'\n'
    ifgdim = Path(ifgfolder+'/'+tail)
    print(ifgdim)
    if ifgdim.is_file():
        print(message)
        out_file.write(message)
    with open(graphxml, 'r') as file:
        filedata = file.read()
    # Replace the target string and generate a new file with replaced names for use in SNAP
    filedata = filedata.replace('COREGFILE',dimfile)
    filedata = filedata.replace('IFGFILE',str(ifgdim))
    filedata = filedata.replace('OUTPUTFOLDER',outputexportfolder)
    with open(graph2run, 'w') as file:
            file.write(filedata)
    args = [ GPT, graph2run, '-c', CACHE, '-q', CPU]
    print(args)
    # Launch the processing
    process = subprocess.Popen(args, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    timeStarted = time.time()
    stdout = process.communicate()[0]
    print('SNAP STDOUT:{}'.format(stdout))
    # Get execution time
    timeDelta = time.time() - timeStarted                     
    print('['+str(k)+'] Finished process in '+str(timeDelta)+' seconds.')
    out_file.write('['+str(k)+'] Finished process in '+str(timeDelta)+' seconds.\n')
    if process.returncode != 0 :
       message='Error exporting '+str(tail)+'\n' 
       err_file.write(message)
    else:
       message='Stamps export of '+str(tail)+' successfully completed.\n'
       print(message)
       out_file.write(message)
    print(bar_message)
    out_file.write(bar_message)
timeDelta_global = time.time() - timeStarted_global
print('Finished Stamps export in ' + str(timeDelta_global) + ' seconds.\n')
out_file.close()
err_file.close()
