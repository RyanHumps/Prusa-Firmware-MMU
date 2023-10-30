#!/usr/bin/env python3
import sys
import re
import os
import fnmatch

# declarations
sourceFile=sys.argv[1]
eLen = 0.0
slackInterval = 250.0

# read file into memory
with open(sourceFile, "r") as f:
    lines = f.readlines()
f.close()

# "write-in-place" the result
destFile = sourceFile
os.remove(sourceFile)


with open(destFile, "w") as of:
    for i in range(len(lines)):
        line = lines[i]

        # get non-comment portion of line
        parts = line.split(';', 1)
        if len(parts) > 0:

            command = parts[0].strip()
            
			# write original line       
            of.write(line)

            # check command starts with G1
            if command:
                g1Match = re.search ('^G1', command)

                # check G1 command has extrusion
                if g1Match:
                    axes = command.split(' ', -1)
                    eAxis = fnmatch.filter(axes, 'E*')
                    if len(eAxis) > 0:

                        #add extrusion length to running total
                        eLen += float(eAxis[0].replace('E',''))

                        # if running total exceeds slack interval
                        # write a Ts command and reduce the running total
                        if eLen>slackInterval:
                            eLen -= slackInterval
                            of.write('Ts ; Slack {} mm\n'.format(slackInterval))
                            
of.close()
