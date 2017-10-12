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
     

    signal = []
    signal_bin = ""
    signal_bin1 = ""
    mark = 0
    flag = False

    for i in range(len(m)):
 
        if m[i] == 2139029504:
            signal.append(0)
        elif m[i] == 32639:
            signal.append(1)
        else:
            signal.append(0)
        
        if len(signal_bin) <= 116:
            if m[i] == 2139029504:
                signal_bin += "0"
            elif m[i] == 32639:
                signal_bin += "1"
            if len(signal_bin) == 116:
                mark = i
                flag = True

        if len(signal_bin1) <= 116 and i > mark and flag:
            if m[i] == 2139029504:
                signal_bin1 += "0"
            elif m[i] == 32639:
                signal_bin1 += "1"

    log.success("Extracted Signal -> "+signal_bin)
    log.info("Preamble => "+signal_bin[0:4])
    log.info("DF => "+signal_bin[4:9])
    log.info("CA => "+signal_bin[9:12])
    log.info("ICAO => "+signal_bin[12:36]+" "+"\033[91m("+str(hex(int(signal_bin[12:36], 2)))+")\033[0m")
    log.info("TYPE => "+signal_bin[36:41])
    log.info("DATA => "+signal_bin[41:92])
    log.info("Interrogator ID => "+signal_bin[92:116]+"\n")

    log.success("Extracted Signal -> "+signal_bin1)
    log.info("Preamble => "+signal_bin1[0:4])
    log.info("DF => "+signal_bin1[4:9])
    log.info("CA => "+signal_bin1[9:12])
    log.info("ICAO => "+signal_bin1[12:36]+" "+"\033[91m("+str(hex(int(signal_bin1[12:36], 2)))+")\033[0m")
    log.info("TYPE => "+signal_bin1[36:41])
    log.info("DATA => "+signal_bin1[41:92])
    log.info("Interrogator ID => "+signal_bin1[92:116]+"\n")
    
    plt.ylim([-2, 2])
    plt.xlim([0,len(signal)])
    plt.plot(range(len(signal)), signal)
    
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
