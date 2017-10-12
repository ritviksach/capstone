#!/usr/bin/python

import matplotlib.pyplot as plt
import pyModeS as pms # Unused for now
from logs.logger import log
import struct
import sys
import argparse

def updateProgressBar(i, n):

    p = (float(i)/float(n-1))*100
    sys.stdout.write("\r\033[94m[I]\033[0m Rendering [{0}>] %d %%".format("="*((int(p)/4)+1)) % int(p+1))
    sys.stdout.flush()

def plotADSB(filename):
   
    try:
        with open(filename, 'rb') as f:
            msg = f.read()
    except Exception as e:
        log.err(str(e)+"\n")
        return

    m = []
    i=0
    size_m = len(msg)
    while i in range(size_m): 
        m.append(struct.unpack('i', msg[i:i+4])[0])
        updateProgressBar(i, size_m)
        i += 4

    print "\n"
     
    plt.xlim([0,len(m)])
    plt.plot(range(len(m)), m)
    
    log.success("Plot Created")
    plt.show()


if __name__ == '__main__':

    main_page = "\033[93m[#]\033[0m ADS-B Signal Renderer \033[93m[#]\033[0m\n"

    parser = argparse.ArgumentParser(description=main_page, epilog="\n\033[91m[*]\033[0m Author: 0xBADB01\n\n")

    parser.add_argument('-f', '--file', help='Name of the iq8s file containing the ADS-B message', required=True)

    args = parser.parse_args()

    if ".iq8s" not in args.file:
        log.err("File is not of type 'iq8s'\n")
        sys.exit(1)

    plotADSB(args.file)
