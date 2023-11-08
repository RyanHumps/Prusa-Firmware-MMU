#!/usr/bin/env python3
import sys
import re
import os
import fnmatch

# declarations
sourceFile=sys.argv[1]
eLen = 0.0
slackInterval = 250.0
zLayer = 0.0

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

			# write original line       
            of.write(line)

            # check command starts with G1
            command = parts[0].strip()
            if command:

                g1Match = re.search ('^G1', command)
                if g1Match:
                    # split G1 axes
                    axes = command.split(' ', -1)

                    # check G1 command has z axis, to compensate slacking as z height increases.
                    # prefer parsing the G1 command over the generated layer comments.
                    zAxis = fnmatch.filter(axes, 'Z*')
                    if len(zAxis) > 0:
                        #keep track of the layer height
                        zLayer = float(zAxis[0].replace('Z',''))

                    # check G1 command has e axis
                    eAxis = fnmatch.filter(axes, 'E*')
                    if len(eAxis) > 0:

                        #add extrusion length to running total
                        eLen += float(eAxis[0].replace('E',''))

                        # if running total exceeds slack interval and zLayer comp,
                        # write a Ts command and reduce the running total.
                        # when the z height increases, we have essentially negative-extruded that amount.
                        # since the Ts command is a static length based on layer 0, 
                        # we compensate the height each Ts command by making sure we have extruded the height length as well
                        if eLen > slackInterval + zLayer:
                            eLen -= slackInterval
                            of.write('Ts ; Slack {} mm\n'.format(slackInterval))
                            
of.close()
