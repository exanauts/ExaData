#!/usr/bin/env python

import os
import sys
import subprocess
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def usage():
    print('Usage: python interpolate.py filename mult')
    print('  filename: a file name containing data to interpolate')
    print('  mult    : a multiplication factor')

if len(sys.argv) < 3:
    usage()
    sys.exit(-1)

filename = sys.argv[1]
mult = int(sys.argv[2])

ps1 = subprocess.Popen(['sed', '-n', '$=', filename], stdout=subprocess.PIPE)
num_scales = int(subprocess.check_output(['awk', '{print $1}'], stdin=ps1.stdout).strip())

f = open(filename, 'r')
y = [0]*num_scales
for i, row in enumerate(f):
    y[i] = float(row.strip())
f.close()

x = np.linspace(1, num_scales, num=num_scales, endpoint=True)
ip = interp1d(x, y, kind='cubic')

xnew = np.linspace(1, num_scales, num=num_scales*mult, endpoint=True)
ynew = ip(xnew)
#fig, ax = plt.subplots()
#ax.plot(x, y, '.', xnew, ynew, '--')
#plt.show()

multfile = os.path.splitext(filename)[0] + '_mult_by_' + str(mult) + '.txt'
f = open(multfile, 'w')
f.write('\n'.join(format(v, '10.8f') for v in ynew))
f.write('\n')
f.close()
