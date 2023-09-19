#!/usr/bin/env python3
import sys
import re
import os
import fnmatch

sourceFile=sys.argv[1]
myFloat = 0.0

# Read the ENTIRE g-code file into memory
with open(sourceFile, "r") as f:
    lines = f.readlines()
f.close()

destFile = sourceFile
os.remove(sourceFile)

with open(destFile, "w") as of:
    for lIndex in range(len(lines)):
        oline = lines[lIndex]
        # Parse gcode line
        parts = oline.split(';', 1)
        if len(parts) > 0:
            
		    # Parse command
            command = parts[0].strip()
            
			# Write original line       
            of.write(oline)

            if command:
                stringMatch = re.search ('^G1', command)
                if stringMatch:
                    splice = command.split(' ', -1)
                    eMatch = fnmatch.filter(splice, 'E*')
                    if len(eMatch) > 0:
                        myFloat += float(eMatch[0].replace('E',''))
                        if myFloat>250:
                            myFloat -= 250
                            of.write('Ts\n')
                            
of.close()
