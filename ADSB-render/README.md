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
$ ./ADSB-view.py --file test/Samples.iq8s 
[I] Rendering [=========================>] 100 %

[+] SUCCESS: Plot Created

```

Once the success message is received, you may view the rendered plot when the matplotlib window opens.
