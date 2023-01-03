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
                if "GRAPHSFOLDER" in line:
                        GRAPH = line.split('=')[1].strip()
                        print GRAPH
                if "GPTBIN_PATH" in line:
                        GPT = line.split('=')[1].strip()
                        print GPT
		if "CACHE" in line:
			CACHE = line.split('=')[1].strip()
		if "CPU" in line:
			CPU = line.split('=')[1].strip()
finally:
        in_file.close()

######################################################################################
####################### TSX-SAR Interferogram generation #############################
######################################################################################
# Folders involved in this processing step
outputcoregfolder=PROJECT+'/coreg'
outputifgfolder=PROJECT+'/ifg'
logfolder=PROJECT+'/logs'

if not os.path.exists(outputifgfolder):
                os.makedirs(outputifgfolder)
if not os.path.exists(logfolder):
                os.makedirs(logfolder)

outlog=logfolder+'/ifg_proc_stdout.log'

# Original Snap graph and replaced Snap graph for Interferogram generation 
graphxml=GRAPH+'/5_Interferogram_TopoPhase.xml'
print graphxml
graph2run=GRAPH+'/ifg_2run.xml'

out_file = open(outlog, 'a')
err_file=out_file

# Processing layout
print bar_message
out_file.write(bar_message)
message='## Interferogram generation started:\n'
print message
out_file.write(message)
print bar_message 
out_file.write(bar_message)
k=0
timeStarted_global = time.time()
# Iterate trough all files in the coregfolder
for dimfile in glob.iglob(outputcoregfolder + '/*.dim'):
    print dimfile
    k=k+1
    # Create name of the output ifg file
    head, tail = os.path.split(os.path.join(outputcoregfolder, dimfile))
    message='['+str(k)+'] Processing coreg file: '+tail+'\n'
    print message
    out_file.write(message)
    outputname=tail[0:17]+'.dim'
    with open(graphxml, 'r') as file :
       filedata = file.read()
    # Replace the target string and generate a new file with replaced names for use in SNAP
    filedata = filedata.replace('COREGFILE',dimfile)
    filedata = filedata.replace('OUTPUTIFGFOLDER',outputifgfolder)    
    filedata = filedata.replace('OUTPUTFILE',outputname)
    with open(graph2run, 'w') as file:
       file.write(filedata)
    args = [ GPT, graph2run, '-c', CACHE, '-q', CPU]
    # Launch the processing
    process = subprocess.Popen(args, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    timeStarted = time.time()
    stdout = process.communicate()[0]
    print 'SNAP STDOUT:{}'.format(stdout)
    # Get execution time
    timeDelta = time.time() - timeStarted                     
    print('['+str(k)+'] Finished process in '+str(timeDelta)+' seconds.')
    out_file.write('['+str(k)+'] Finished process in '+str(timeDelta)+' seconds.\n')
    if process.returncode != 0 :
        message='Error computing with interferogram generation of coreg file '+str(dimfile)
        err_file.write(message+'\n')
    else:
        message='Interferogram computation for data '+str(outputname)+' successfully completed.\n'
        print message
        out_file.write(message)
    print bar_message
    out_file.write(bar_message)
timeDelta_global = time.time() - timeStarted_global
print 'Finished interferogram generation in ' + str(timeDelta_global) + ' seconds.\n'
out_file.close()
