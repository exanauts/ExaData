#!/usr/bin/env python

import os
import sys
import subprocess

sys.path.append('../src')
import parse_matpower as pm

def usage():
    print('Usage: python interpolate_load.py case scalefile')
    print('  case     : case name')
    print('  scalefile: filename containing scaling factors')

if len(sys.argv) < 3:
    usage()
    sys.exit(-1)

data = pm.parse(sys.argv[1])
scalefile = sys.argv[2]
base = os.path.basename(sys.argv[1])
case = os.path.splitext(base)[0]

ps1 = subprocess.Popen(['sed', '-n', '$=', scalefile], stdout=subprocess.PIPE)
num_scales = int(subprocess.check_output(['awk', '{print $1}'], stdin=ps1.stdout).strip())

scales = [0]*num_scales

f = open(scalefile, 'r')
for i, row in enumerate(f):
    scales[i] = float(row.strip())
f.close()

prefix = case + "_" + str(num_scales)
pdout = open(prefix + '.Pd', 'w')
qdout = open(prefix + '.Qd', 'w')

for i in range(len(data["bus"])):
    pdline = [data["bus"][i]["Pd"]*scales[j] for j in range(num_scales)]
    qdline = [data["bus"][i]["Qd"]*scales[j] for j in range(num_scales)]

    pdout.write('\t'.join(format(x, '10.8f') for x in pdline))
    qdout.write('\t'.join(format(x, '10.8f') for x in qdline))
    pdout.write('\n')
    qdout.write('\n')
pdout.close()
qdout.close()
