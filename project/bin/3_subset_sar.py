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
		if "LONMIN" in line:
			LONMIN = line.split('=')[1].strip()
                if "LATMIN" in line:
                        LATMIN = line.split('=')[1].strip()
                if "LONMAX" in line:
                        LONMAX = line.split('=')[1].strip()
                if "LATMAX" in line:
                        LATMAX = line.split('=')[1].strip()
		if "CACHE" in line:
			CACHE = line.split('=')[1].strip()
		if "CPU" in line:
			CPU = line.split('=')[1].strip()
finally:
        in_file.close()
        
polygon='POLYGON (('+LONMIN+' '+LATMIN+','+LONMAX+' '+LATMIN+','+LONMAX+' '+LATMAX+','+LONMIN+' '+LATMAX+','+LONMIN+' '+LATMIN+'))'

######################################################################################
################################### TSX Subsetting ###################################
##### Dont forget to move your master subset into a newly created master folder! #####
# Folders involved in this processing step
slavesplittedfolder=PROJECT+'/slaves'
outputsubsetfolder=PROJECT+'/subset'
logfolder=PROJECT+'/logs'

if not os.path.exists(outputsubsetfolder):
                os.makedirs(outputsubsetfolder)
if not os.path.exists(logfolder):
                os.makedirs(logfolder)

outlog=logfolder+'/subset_stdout.log'

# Original Snap graph and replaced Snap graph for subsettting
graphxml=GRAPH+'/3_TSX_Subset.xml'
print graphxml
graph2run=GRAPH+'/subset_2run.xml'

out_file = open(outlog, 'a')
err_file=out_file

# Processing layout
print bar_message
out_file.write(bar_message)
message='## Subsetting started:\n'
print message
out_file.write(message)
print bar_message 
out_file.write(bar_message)
k=0
timeStarted_global = time.time()
# Iterate trough all files in the slavefolder
for xmlfile in glob.iglob(slavesplittedfolder + '/*/*/*.xml'):
    print xmlfile
    k=k+1
    # Create name of the output subset file
    head, tail = os.path.split(os.path.join(slavesplittedfolder, xmlfile))
    message='['+str(k)+'] Processing subset file: '+tail+'\n'
    print message
    out_file.write(message)
    outputname=tail[28:36]+'_sub.dim'
    with open(graphxml, 'r') as file :
       filedata = file.read()
    # Replace the target string and generate a new file with replaced names for use in SNAP
    filedata = filedata.replace('INPUTXML',xmlfile)
    filedata = filedata.replace('OUTPUTSUBSETFOLDER',outputsubsetfolder)
    filedata = filedata.replace('OUTPUTFILE',outputname)
    filedata = filedata.replace('LATMIN', LATMIN)
    filedata = filedata.replace('LONMIN',LONMIN)
    filedata = filedata.replace('LATMAX',LATMAX)
    filedata = filedata.replace('LONMAX',LONMAX)
    filedata = filedata.replace('POLYGON',polygon)
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
        message='Error computing with subset of splitted slave '+str(xmlfile)
        err_file.write(message+'\n')
    else:
        message='Subsetting for data '+str(outputname)+' successfully completed.\n'
        print message
        out_file.write(message)
    print bar_message
    out_file.write(bar_message)
timeDelta_global = time.time() - timeStarted_global
print 'Finished subsetting in ' + str(timeDelta_global) + ' seconds.\n'
print 'IMPORTANT REMINDER: Dont forget to move your master subset into a newly created folder named master.'
out_file.close()

