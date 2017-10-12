# ADS-B Signal Renderer

This repository contains a tool to render encoded ADS-B signals to reveal more information about their structure. This tool is written in python and may have certain delays in for large iq8s files.

## Requirements

This tool requires pyModeS and matplotlib for running. This can be installed by:
```
$ pip install pyModeS
$ pip install matplotlib
```

## Usage and running instructions


This tool makes use of argparse and you can view the help text by:
```
$  ./ADSB-view.py -h
usage: ADSB-view.py [-h] -f FILE

[#] ADS-B Signal Renderer [#]

optional arguments:
  -h, --help            show this help message and exit
    -f FILE, --file FILE  Name of the iq8s file containing the ADS-B message

    [*] Author: 0xBADB01

```

An example of it's usage is as follows. This example is created using the testing files located under the ```test/``` directory

```
./ADSB-render.py -f test/Samples.iq8s 
[I] Rendering [=========================>] 100 %

[+] SUCCESS: Extracted Signal -> 110010001101101010111100110111101111010110001111100101110000001110100000011001001011101110000110000011110111100110011
[I] INFO: Preamble => 1100
[I] INFO: DF => 10001
[I] INFO: CA => 101
[I] INFO: ICAO => 101010111100110111101111 (0xabcdef)
[I] INFO: TYPE => 01011
[I] INFO: DATA => 000111110010111000000111010000001100100101110111000
[I] INFO: Interrogator ID => 011000001111011110011001

[+] SUCCESS: Extracted Signal -> 11001000110110101011110011011110111101011000111110010111010000010110111011111111101011110111011100000000010100111001
[I] INFO: Preamble => 1100
[I] INFO: DF => 10001
[I] INFO: CA => 101
[I] INFO: ICAO => 101010111100110111101111 (0xabcdef)
[I] INFO: TYPE => 01011
[I] INFO: DATA => 000111110010111010000010110111011111111101011110111
[I] INFO: Interrogator ID => 011100000000010100111001

[+] SUCCESS: Plot Created

```

Once the success message is received, you may view the rendered plot when the matplotlib window opens.
