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

######################################################################################
############################## TSX-SAR Coregistration ################################
######################################################################################
# Folders involved in this processing step
subsetfolder=PROJECT+'/subset'
outputcoregfolder=PROJECT+'/coreg'
logfolder=PROJECT+'/logs'

if not os.path.exists(outputcoregfolder):
                os.makedirs(outputcoregfolder)
if not os.path.exists(logfolder):
                os.makedirs(logfolder)

outlog=logfolder+'/coreg_proc_stdout.log'

# Original Snap graph and replaced Snap graph for Coregistration 
graphxml=GRAPH+'/4_DEM_Assisted_Coregistration.xml'
print(graphxml)
graph2run=GRAPH+'/coreg_2run.xml'

out_file = open(outlog, 'a')
err_file=out_file

# Processing layout
print(bar_message)
out_file.write(bar_message)
message='## Coregistration started:\n'
print(message)
out_file.write(message)
print(bar_message)
out_file.write(bar_message)
k=0
timeStarted_global = time.time()
# Iterate trough all files in the subsetfolder
for dimfile in glob.iglob(subsetfolder + '/*.dim'):
    print(dimfile)
    k=k+1
    # Create name of the output coreg file
    head, tail = os.path.split(os.path.join(subsetfolder, dimfile))
    message='['+str(k)+'] Processing slave file: '+tail+'\n'
    print(message)
    out_file.write(message)
    head , tailm = os.path.split(MASTER)
    outputname=tailm[0:8]+'_'+tail[0:8]+'.dim'
    print(outputname)
    with open(graphxml, 'r') as file :
       filedata = file.read()
    # Replace the target string and generate a new file with replaced names for use in SNAP
    filedata = filedata.replace('MASTER',MASTER)
    filedata = filedata.replace('SLAVE',dimfile)
    filedata = filedata.replace('OUTPUTCOREGFOLDER',outputcoregfolder)
    filedata = filedata.replace('OUTPUTFILE',outputname)
    with open(graph2run, 'w') as file:
       file.write(filedata)
    args = [ GPT, graph2run, '-c', CACHE, '-q', CPU]
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
        message='Error computing with coregistration of splitted slave '+str(dimfile)
        err_file.write(message+'\n')
    else:
        message='Coregistration for data '+str(outputname)+' successfully completed.\n'
        print(message)
        out_file.write(message)
    print(bar_message)
    out_file.write(bar_message)
timeDelta_global = time.time() - timeStarted_global
print('Finished coregistration in ' + str(timeDelta_global) + ' seconds.\n')
out_file.close()
